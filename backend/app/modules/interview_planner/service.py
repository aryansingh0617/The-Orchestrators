from __future__ import annotations

from app.domain.interfaces import AIProvider, StructuredGenerationOptions
from app.modules.interview_planner.schemas import PlannerInput, PlanningDecision

DIFFICULTY_RANK = {"basic": 1, "intermediate": 2, "advanced": 3, "expert": 4}
RANK_DIFFICULTY = {v: k for k, v in DIFFICULTY_RANK.items()}


class InterviewPlanner:
    """Adaptive planner that chooses follow-ups, deepening, gaps, or new missions."""

    def __init__(self, ai_provider: AIProvider | None = None) -> None:
        self._ai_provider = ai_provider

    def plan(self, state: PlannerInput) -> PlanningDecision:
        decision = self._deterministic_plan(state)
        # Evaluation-driven local modes must not be overridden by model suggestions.
        if decision.mode in {"follow_up", "deepen"} or self._ai_provider is None:
            return decision

        try:
            prompt = (
                "Decide the next adaptive interview action.\n"
                f"State: {state.model_dump_json()}\n"
                "Modes: new_mission, follow_up, deepen, revisit_gap, completion.\n"
                "Enforce minimum questions and curriculum-day coverage before completion."
            )
            res = self._ai_provider.generate_structured(
                prompt=prompt,
                schema=PlanningDecision,
                options=StructuredGenerationOptions(
                    metadata={"prompt_id": "planner.create_plan.v1"}
                ),
            )
            parsed = PlanningDecision.model_validate(res.data)
            return self._sanitize(parsed, state, fallback=decision)
        except Exception:
            return decision

    def _deterministic_plan(self, state: PlannerInput) -> PlanningDecision:
        covered = set(state.covered_curriculum_days)
        days = state.curriculum_days or sorted(state.day_competency_map.keys()) or [1, 3, 5, 7]
        day_map = state.day_competency_map or {
            d: (state.competencies[(i % len(state.competencies))] if state.competencies else "General AI Engineering")
            for i, d in enumerate(days)
        }
        competencies = state.competencies or list(dict.fromkeys(day_map.values()))
        current_day = state.current_curriculum_day or (days[0] if days else 1)
        current_comp = state.current_competency or day_map.get(current_day, competencies[0])
        difficulty = state.difficulty or self._difficulty_from_start(state.starting_difficulty)

        can_complete = (
            state.question_count >= state.minimum_question_count
            and state.curriculum_day_coverage_count >= state.minimum_curriculum_days
        )

        outcome = (state.evaluation_outcome or "").lower()
        followups = len(state.follow_up_history)
        gaps = list(dict.fromkeys([*state.knowledge_gaps, *state.misunderstood_concepts, *state.unresolved_issues]))

        if can_complete and not gaps:
            return PlanningDecision(
                next_curriculum_day=current_day,
                competency=current_comp,
                difficulty=difficulty,
                mode="completion",
                reason="Minimum coverage met and no unresolved knowledge gaps remain.",
                evidence_needed=[],
            )

        if can_complete and gaps and followups >= 2:
            next_gap_day = self._day_for_gap(gaps[0], day_map, days, covered) or current_day
            return PlanningDecision(
                next_curriculum_day=next_gap_day,
                competency=day_map.get(next_gap_day, current_comp),
                difficulty=difficulty,
                mode="completion",
                reason="Coverage targets met; closing interview with remaining gaps noted.",
                evidence_needed=gaps[:2],
            )

        # Evaluation-driven local decisions before switching curriculum day.
        if state.candidate_answer and state.previous_question:
            if outcome in {"incorrect", "false_claim", "unsupported"} and followups < 2:
                return PlanningDecision(
                    next_curriculum_day=current_day,
                    competency=current_comp,
                    difficulty=self._adjust_difficulty(difficulty, -1),
                    mode="follow_up",
                    reason=f"Evaluation outcome '{outcome}' requires clarifying follow-up.",
                    evidence_needed=["corrected reasoning", "concrete mitigation"],
                )
            if outcome in {"partial", "shallow"} and followups < 2:
                return PlanningDecision(
                    next_curriculum_day=current_day,
                    competency=current_comp,
                    difficulty=difficulty,
                    mode="deepen",
                    reason="Partial or shallow reasoning needs deeper probing on the same competency.",
                    evidence_needed=["systems tradeoff", "failure mode analysis"],
                )
            if outcome in {"correct", "strong"} and followups < 1:
                return PlanningDecision(
                    next_curriculum_day=current_day,
                    competency=current_comp,
                    difficulty=self._adjust_difficulty(difficulty, 1),
                    mode="deepen",
                    reason="Strong answer; deepen to test production judgment before moving on.",
                    evidence_needed=["production constraint handling"],
                )

        if gaps and state.curriculum_day_coverage_count >= 2 and followups == 0:
            gap_day = self._day_for_gap(gaps[0], day_map, days, covered)
            if gap_day is not None:
                return PlanningDecision(
                    next_curriculum_day=gap_day,
                    competency=day_map.get(gap_day, current_comp),
                    difficulty=difficulty,
                    mode="revisit_gap",
                    reason=f"Revisit unresolved gap: {gaps[0]}",
                    evidence_needed=[gaps[0]],
                )

        next_day = self._next_uncovered_day(days, covered, current_day)
        if next_day is None:
            if can_complete:
                return PlanningDecision(
                    next_curriculum_day=current_day,
                    competency=current_comp,
                    difficulty=difficulty,
                    mode="completion",
                    reason="All planned curriculum days covered and minimum questions satisfied.",
                    evidence_needed=[],
                )
            # Force intelligent depth on an existing day rather than cycling blindly.
            return PlanningDecision(
                next_curriculum_day=current_day,
                competency=current_comp,
                difficulty=self._adjust_difficulty(difficulty, 1),
                mode="deepen",
                reason="Curriculum days exhausted early; deepen current competency for coverage quality.",
                evidence_needed=["edge-case handling", "observability plan"],
            )

        return PlanningDecision(
            next_curriculum_day=next_day,
            competency=day_map.get(next_day, competencies[len(covered) % len(competencies)]),
            difficulty=difficulty,
            mode="new_mission",
            reason="Open a new mission on an uncovered curriculum day using evaluation signals.",
            evidence_needed=["architecture choice", "debugging approach"],
        )

    def _sanitize(
        self,
        parsed: PlanningDecision,
        state: PlannerInput,
        *,
        fallback: PlanningDecision,
    ) -> PlanningDecision:
        allowed = {"new_mission", "follow_up", "deepen", "revisit_gap", "completion"}
        mode = parsed.mode if parsed.mode in allowed else fallback.mode
        can_complete = (
            state.question_count >= state.minimum_question_count
            and state.curriculum_day_coverage_count >= state.minimum_curriculum_days
        )
        if mode == "completion" and not can_complete:
            return fallback.model_copy(update={"mode": "new_mission", "reason": fallback.reason})
        if can_complete and not state.knowledge_gaps:
            return PlanningDecision(
                next_curriculum_day=fallback.next_curriculum_day,
                competency=fallback.competency,
                difficulty=fallback.difficulty,
                mode="completion",
                reason="Coverage targets met.",
                evidence_needed=[],
            )
        # Prefer deterministic day/competency selection to avoid model day-cycling.
        return PlanningDecision(
            next_curriculum_day=fallback.next_curriculum_day,
            competency=fallback.competency,
            difficulty=(
                parsed.difficulty if parsed.difficulty in DIFFICULTY_RANK else fallback.difficulty
            ),
            mode=fallback.mode if mode == "new_mission" else mode,
            reason=fallback.reason,
            evidence_needed=fallback.evidence_needed or parsed.evidence_needed,
        )

    @staticmethod
    def _difficulty_from_start(starting: int) -> str:
        return RANK_DIFFICULTY.get(max(1, min(4, starting)), "intermediate")

    @staticmethod
    def _adjust_difficulty(current: str, delta: int) -> str:
        rank = DIFFICULTY_RANK.get(current, 2) + delta
        return RANK_DIFFICULTY[max(1, min(4, rank))]

    @staticmethod
    def _next_uncovered_day(days: list[int], covered: set[int], current_day: int) -> int | None:
        remaining = [d for d in days if d not in covered]
        if not remaining:
            return None
        if not covered:
            return remaining[0]
        # Prefer a day different from current when possible, but do not blindly cycle.
        for d in remaining:
            if d != current_day:
                return d
        return remaining[0]

    @staticmethod
    def _day_for_gap(
        gap: str,
        day_map: dict[int, str],
        days: list[int],
        covered: set[int],
    ) -> int | None:
        gap_l = gap.lower()
        for day, competency in day_map.items():
            if gap_l in competency.lower() or competency.lower() in gap_l:
                return day
        for day in days:
            if day in covered:
                return day
        return days[0] if days else None
