from __future__ import annotations

from app.application.dtos import FeedbackDTO, InterviewCommand, InterviewResult
from app.application.runtime_state import InterviewRuntimeState
from app.core.clock import Clock
from app.core.ids import IdGenerator
from app.domain.entities.assessment import (
    AssessmentSession,
    CandidateTurn,
    Evidence,
    EvidencePolarity,
    MemoryRecord,
    Mission,
    SessionStatus,
    WorldState,
)
from app.domain.errors import NotFoundError, ValidationError
from app.domain.interfaces import (
    AIProvider,
    EvidenceRepository,
    MemoryRepository,
    MissionRepository,
    SessionRepository,
    TurnRepository,
    WorldStateRepository,
)
from app.modules.candidate_analyzer import CandidateAnalyzer
from app.modules.curriculum_analyzer import CurriculumAnalyzer
from app.modules.evaluation_engine import EvaluationEngine
from app.modules.feedback_generator import FeedbackGenerator
from app.modules.interview_planner import InterviewPlanner, PlannerInput
from app.modules.memory_engine import MemoryEngine
from app.modules.mission_generator import MissionGenerator
from app.modules.world_state_engine import WorldStateEngine


class InterviewService:
    """Orchestrates the adaptive Chimera interview loop behind POST /api/interview."""

    MIN_QUESTIONS = 8
    MIN_CURRICULUM_DAYS = 4

    def __init__(
        self,
        sessions: SessionRepository,
        ai_provider: AIProvider,
        clock: Clock,
        id_generator: IdGenerator,
        turns: TurnRepository | None = None,
        evidence: EvidenceRepository | None = None,
        memory_repo: MemoryRepository | None = None,
        missions: MissionRepository | None = None,
        world_states: WorldStateRepository | None = None,
    ) -> None:
        self._sessions = sessions
        self._ai_provider = ai_provider
        self._clock = clock
        self._id_generator = id_generator
        self._turns = turns
        self._evidence = evidence
        self._memory_repo = memory_repo
        self._missions = missions
        self._world_states = world_states

        self._candidate_analyzer = CandidateAnalyzer(ai_provider)
        self._curriculum_analyzer = CurriculumAnalyzer(ai_provider)
        self._planner = InterviewPlanner(ai_provider)
        self._mission_generator = MissionGenerator(ai_provider)
        self._world_engine = WorldStateEngine()
        self._memory_engine = MemoryEngine()
        self._evaluation_engine = EvaluationEngine(ai_provider)
        self._feedback_generator = FeedbackGenerator()
        self._runtime: dict[str, InterviewRuntimeState] = {}

    def handle(self, command: InterviewCommand) -> InterviewResult:
        existing = self._sessions.get_by_external_id(command.session_id)
        if command.candidate is not None and existing is None:
            return self._start_interview(command)
        if existing is None:
            raise NotFoundError(
                "Start the interview with candidate data before sending messages.",
                details={"sessionId": command.session_id},
            )
        runtime = self._load_runtime(existing)
        if runtime.done:
            return self._completion_result(runtime)
        if not command.message or not command.message.strip():
            raise ValidationError(
                "A non-empty message is required for an active interview turn.",
                details={"sessionId": command.session_id},
            )
        return self._continue_interview(existing, runtime, command.message.strip())

    def _start_interview(self, command: InterviewCommand) -> InterviewResult:
        if command.candidate is None:
            raise ValidationError("Candidate data is required to start an interview.")

        now = self._clock.now()
        member = command.candidate.member
        role_title = member.jobRole or "AI Engineer"
        seniority = self._infer_seniority(member.yearsExperience)

        candidate_analysis = self._candidate_analyzer.analyze(command.candidate)
        curriculum_analysis = self._curriculum_analyzer.analyze(
            role_title=role_title,
            seniority=seniority,
        )

        session = AssessmentSession(
            id=self._id_generator.new_id(),
            external_session_id=command.session_id,
            candidate_id=member.id,
            role_title=role_title,
            seniority=seniority,
            status=SessionStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        self._sessions.save(session)

        runtime = InterviewRuntimeState(
            session_id=command.session_id,
            internal_session_id=session.id,
            role_title=role_title,
            seniority=seniority,
            candidate_analysis=candidate_analysis,
            curriculum_analysis=curriculum_analysis,
            memory=self._memory_engine.empty(),
            current_difficulty=self._difficulty_label(candidate_analysis.starting_difficulty),
        )

        decision = self._planner.plan(self._planner_input(runtime))
        mission = self._mission_generator.generate(
            competency=decision.competency,
            curriculum_day=decision.next_curriculum_day,
            difficulty=decision.difficulty,
            evidence_needed=decision.evidence_needed,
            topic=self._topic_for_day(runtime, decision.next_curriculum_day),
            learning_objective=self._objective_for_day(runtime, decision.next_curriculum_day),
            mode=decision.mode,
        )
        world = self._world_engine.initialize(
            mission_title=mission.title,
            difficulty=decision.difficulty,
            constraints=mission.constraints,
        )

        runtime.current_mission = mission
        runtime.current_competency = decision.competency
        runtime.current_curriculum_day = decision.next_curriculum_day
        runtime.current_difficulty = decision.difficulty
        runtime.world = world
        runtime.previous_question = mission.candidate_facing_prompt()
        runtime.progression.append(
            f"start: day {decision.next_curriculum_day} / {decision.competency} / {decision.mode}"
        )

        self._persist_mission(session.id, mission)
        self._persist_world(session.id, world)
        self._save_runtime(runtime)

        reply = (
            f"Welcome. Let's begin your interview.\n\n"
            f"{mission.candidate_facing_prompt()}\n\n"
            f"Current system state: {world.visible_summary}"
        )
        return InterviewResult(reply=reply, done=False)

    def _continue_interview(
        self,
        session: AssessmentSession,
        runtime: InterviewRuntimeState,
        message: str,
    ) -> InterviewResult:
        mission = runtime.current_mission
        if mission is None:
            raise ValidationError("Interview mission is missing; restart the session.")

        evaluation = self._evaluation_engine.evaluate(
            mission=mission,
            candidate_answer=message,
            previous_outcome=(
                runtime.previous_evaluation.outcome if runtime.previous_evaluation else None
            ),
        )
        evidence_ids = self._persist_evidence(session.id, evaluation, mission.competency)
        runtime.evidence_ids.extend(evidence_ids)

        runtime.memory = self._memory_engine.update(
            runtime.memory,
            competency=mission.competency,
            curriculum_day=mission.curriculum_day,
            evaluation_outcome=evaluation.outcome,
            evaluation_rationale=evaluation.rationale,
            evidence_ids=evidence_ids,
            claim_labels=evaluation.claim_labels,
        )

        runtime.question_count += 1
        covered = set(runtime.covered_curriculum_days)
        covered.add(mission.curriculum_day)
        runtime.covered_curriculum_days = sorted(covered)

        scores = runtime.competency_scores.setdefault(mission.competency, [])
        scores.append(evaluation.overall_score)
        for dim, value in evaluation.engineering_dna.items():
            runtime.engineering_dna_accum.setdefault(dim, []).append(value)

        runtime.world = self._world_engine.transition(
            runtime.world,
            candidate_answer=message,
            evaluation_outcome=evaluation.outcome,
            mission_title=mission.title,
            difficulty=runtime.current_difficulty,
            evidence=evidence_ids,
            progress={
                "questions": runtime.question_count,
                "curriculum_days": len(runtime.covered_curriculum_days),
            },
        )

        turn_id = self._id_generator.new_id()
        if self._turns is not None:
            self._turns.save(
                CandidateTurn(
                    id=turn_id,
                    session_id=session.id,
                    sequence_number=runtime.question_count,
                    prompt_text=runtime.previous_question or mission.title,
                    candidate_response=message,
                    created_at=self._clock.now(),
                )
            )

        if self._memory_repo is not None:
            self._memory_repo.save(
                MemoryRecord(
                    id=self._id_generator.new_id(),
                    session_id=session.id,
                    memory_type="turn_summary",
                    summary=(
                        f"{mission.competency}: {evaluation.outcome}. "
                        f"Gaps={runtime.memory.knowledge_gaps[:3]}"
                    ),
                    evidence_ids=tuple(evidence_ids),
                    confidence=runtime.memory.confidence,
                )
            )

        runtime.previous_evaluation = evaluation
        runtime.progression.append(
            f"q{runtime.question_count}: {mission.competency} -> {evaluation.outcome}"
        )

        decision = self._planner.plan(self._planner_input(runtime, message, evaluation))

        if decision.mode == "completion":
            return self._complete(session, runtime)

        next_mission = self._mission_generator.generate(
            competency=decision.competency,
            curriculum_day=decision.next_curriculum_day,
            difficulty=decision.difficulty,
            evidence_needed=decision.evidence_needed,
            topic=self._topic_for_day(runtime, decision.next_curriculum_day),
            learning_objective=self._objective_for_day(runtime, decision.next_curriculum_day),
            mode=decision.mode,
            previous_answer=message,
            world_summary=runtime.world.visible_summary,
        )

        if decision.mode in {"follow_up", "deepen"}:
            runtime.follow_up_history.append(decision.mode)
        else:
            runtime.follow_up_history = []

        runtime.current_mission = next_mission
        runtime.current_competency = decision.competency
        runtime.current_curriculum_day = decision.next_curriculum_day
        runtime.current_difficulty = decision.difficulty
        runtime.previous_question = next_mission.candidate_facing_prompt()
        runtime.progression.append(
            f"plan: {decision.mode} day {decision.next_curriculum_day} ({decision.reason})"
        )

        self._persist_mission(session.id, next_mission)
        self._persist_world(session.id, runtime.world)
        session.updated_at = self._clock.now()
        self._sessions.save(session)
        self._save_runtime(runtime)

        reply = (
            f"{runtime.world.visible_summary}\n\n"
            f"{next_mission.candidate_facing_prompt()}"
        )
        return InterviewResult(reply=reply, done=False)

    def _complete(
        self,
        session: AssessmentSession,
        runtime: InterviewRuntimeState,
    ) -> InterviewResult:
        report = self._feedback_generator.generate(
            memory=runtime.memory,
            engineering_dna=runtime.average_dna(),
            competency_scores=runtime.average_competency_scores(),
            progression=runtime.progression,
            role_title=runtime.role_title,
            seniority=runtime.seniority,
        )
        runtime.done = True
        session.status = SessionStatus.COMPLETED
        session.updated_at = self._clock.now()
        self._sessions.save(session)
        self._persist_world(session.id, runtime.world)
        self._save_runtime(runtime)

        feedback = FeedbackDTO(
            summary=report.summary,
            strengths=report.strengths,
            gaps=report.gaps,
            next=report.next,
        )
        reply = (
            "Interview completed.\n\n"
            f"{report.executive_summary}\n\n"
            f"Hiring assessment: {report.hiring_assessment}"
        )
        return InterviewResult(reply=reply, done=True, feedback=feedback)

    def _completion_result(self, runtime: InterviewRuntimeState) -> InterviewResult:
        report = self._feedback_generator.generate(
            memory=runtime.memory,
            engineering_dna=runtime.average_dna(),
            competency_scores=runtime.average_competency_scores(),
            progression=runtime.progression,
            role_title=runtime.role_title,
            seniority=runtime.seniority,
        )
        return InterviewResult(
            reply="Interview completed.",
            done=True,
            feedback=FeedbackDTO(
                summary=report.summary,
                strengths=report.strengths,
                gaps=report.gaps,
                next=report.next,
            ),
        )

    def _planner_input(
        self,
        runtime: InterviewRuntimeState,
        message: str | None = None,
        evaluation=None,
    ) -> PlannerInput:
        day_map = runtime.day_competency_map()
        analysis = runtime.candidate_analysis
        curriculum = runtime.curriculum_analysis
        return PlannerInput(
            candidate_strengths=(analysis.baseline_strengths if analysis else []),
            areas_to_probe=(analysis.areas_to_probe if analysis else []),
            starting_difficulty=(analysis.starting_difficulty if analysis else 2),
            competencies=(
                [c.name for c in curriculum.competencies] if curriculum else list(day_map.values())
            ),
            curriculum_days=sorted(day_map.keys()),
            day_competency_map=day_map,
            covered_curriculum_days=list(runtime.covered_curriculum_days),
            current_competency=runtime.current_competency,
            current_curriculum_day=runtime.current_curriculum_day,
            previous_question=runtime.previous_question,
            candidate_answer=message,
            evaluation_outcome=evaluation.outcome if evaluation else None,
            evaluation_score=evaluation.overall_score if evaluation else None,
            evidence_collected=list(runtime.evidence_ids),
            knowledge_gaps=list(runtime.memory.knowledge_gaps),
            demonstrated_concepts=list(runtime.memory.demonstrated_concepts),
            misunderstood_concepts=list(runtime.memory.misunderstood_concepts),
            difficulty=runtime.current_difficulty,
            follow_up_history=list(runtime.follow_up_history),
            question_count=runtime.question_count,
            curriculum_day_coverage_count=len(runtime.covered_curriculum_days),
            minimum_question_count=self.MIN_QUESTIONS,
            minimum_curriculum_days=self.MIN_CURRICULUM_DAYS,
            unresolved_issues=list(runtime.memory.unresolved_issues),
        )

    def _load_runtime(self, session: AssessmentSession) -> InterviewRuntimeState:
        cached = self._runtime.get(session.external_session_id)
        if cached is not None:
            return cached
        if self._world_states is not None:
            latest = self._world_states.get_latest_for_session(session.id)
            if latest and isinstance(latest.state, dict) and latest.state.get("runtime"):
                runtime = InterviewRuntimeState.model_validate(latest.state["runtime"])
                self._runtime[session.external_session_id] = runtime
                return runtime
        raise NotFoundError(
            "Interview runtime state was not found for this session.",
            details={"sessionId": session.external_session_id},
        )

    def _save_runtime(self, runtime: InterviewRuntimeState) -> None:
        self._runtime[runtime.session_id] = runtime
        if self._world_states is not None:
            payload = {
                **runtime.world.model_dump(mode="json"),
                "runtime": runtime.to_persistable(),
            }
            self._world_states.save(
                WorldState(
                    id=self._id_generator.new_id(),
                    session_id=runtime.internal_session_id,
                    state=payload,
                    visible_summary=runtime.world.visible_summary,
                    version=runtime.world.version,
                )
            )

    def _persist_mission(self, session_id: str, mission) -> None:
        if self._missions is None:
            return
        self._missions.save(
            Mission(
                id=self._id_generator.new_id(),
                session_id=session_id,
                title=mission.title,
                scenario=mission.scenario,
                competency_targets=(mission.competency,),
                difficulty={"basic": 1, "intermediate": 2, "advanced": 3, "expert": 4}.get(
                    mission.difficulty, 2
                ),
            )
        )

    def _persist_world(self, session_id: str, world) -> None:
        if self._world_states is None:
            return
        # Runtime save handles persistence with embedded runtime blob.
        _ = (session_id, world)

    def _persist_evidence(self, session_id: str, evaluation, competency: str) -> list[str]:
        ids: list[str] = []
        if self._evidence is None:
            return [self._id_generator.new_id() for _ in evaluation.evidence or [None]]
        for item in evaluation.evidence:
            eid = self._id_generator.new_id()
            ids.append(eid)
            polarity = {
                "positive": EvidencePolarity.POSITIVE,
                "negative": EvidencePolarity.NEGATIVE,
            }.get(item.polarity, EvidencePolarity.NEUTRAL)
            self._evidence.save(
                Evidence(
                    id=eid,
                    session_id=session_id,
                    turn_id="",
                    competency=item.competency or competency,
                    observation=item.observation,
                    polarity=polarity,
                    strength=item.strength,
                    confidence=item.confidence,
                    rationale=item.rationale,
                )
            )
        return ids

    def _topic_for_day(self, runtime: InterviewRuntimeState, day: int) -> str | None:
        if not runtime.curriculum_analysis:
            return None
        for item in runtime.curriculum_analysis.curriculum_days:
            if item.day == day:
                return item.topic
        return None

    def _objective_for_day(self, runtime: InterviewRuntimeState, day: int) -> str | None:
        if not runtime.curriculum_analysis:
            return None
        for item in runtime.curriculum_analysis.curriculum_days:
            if item.day == day:
                return item.learning_objective
        return None

    @staticmethod
    def _difficulty_label(starting: int) -> str:
        return {1: "basic", 2: "intermediate", 3: "advanced", 4: "expert", 5: "expert"}.get(
            starting, "intermediate"
        )

    @staticmethod
    def _infer_seniority(years_experience: int | None) -> str:
        if years_experience is None:
            return "mid"
        if years_experience >= 12:
            return "staff"
        if years_experience >= 6:
            return "senior"
        if years_experience >= 2:
            return "mid"
        return "junior"
