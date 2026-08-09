from datetime import datetime

from sqlalchemy.orm import Session as DbSession

from app.domain.entities import (
    Candidate,
    CandidateTurn,
    Evaluation,
    Evidence,
    MemoryRecord,
    Mission,
    WorldState,
)
from app.domain.entities.assessment import EvidencePolarity
from app.infrastructure.database.models import (
    CandidateModel,
    EvaluationModel,
    EvidenceItemModel,
    MemoryRecordModel,
    MissionModel,
    TurnModel,
    WorldStateSnapshotModel,
)


class SqlCandidateRepository:
    def __init__(self, db: DbSession) -> None:
        self._db = db

    def get_by_id(self, candidate_id: str) -> Candidate | None:
        model = self._db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
        if not model:
            return None
        return Candidate(
            id=model.id,
            display_name=model.display_name,
            email=model.email,
            profile_summary=model.profile_summary,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def save(self, candidate: Candidate) -> Candidate:
        model = self._db.query(CandidateModel).filter(CandidateModel.id == candidate.id).first()
        if not model:
            model = CandidateModel(
                id=candidate.id,
                display_name=candidate.display_name,
                email=candidate.email,
                profile_summary=candidate.profile_summary,
                created_at=candidate.created_at,
                updated_at=candidate.updated_at,
            )
            self._db.add(model)
        else:
            model.display_name = candidate.display_name
            model.email = candidate.email
            model.profile_summary = candidate.profile_summary
            model.updated_at = candidate.updated_at
        self._db.commit()
        self._db.refresh(model)
        return candidate


class SqlTurnRepository:
    def __init__(self, db: DbSession) -> None:
        self._db = db

    def get_turns_for_session(self, session_id: str) -> list[CandidateTurn]:
        models = (
            self._db.query(TurnModel)
            .filter(TurnModel.session_id == session_id)
            .order_by(TurnModel.sequence_number)
            .all()
        )
        return [
            CandidateTurn(
                id=m.id,
                session_id=m.session_id,
                sequence_number=m.sequence_number,
                prompt_text=m.prompt_text,
                candidate_response=m.candidate_response,
                created_at=m.created_at,
                mission_id=m.mission_id,
            )
            for m in models
        ]

    def save(self, turn: CandidateTurn) -> CandidateTurn:
        model = self._db.query(TurnModel).filter(TurnModel.id == turn.id).first()
        if not model:
            model = TurnModel(
                id=turn.id,
                session_id=turn.session_id,
                mission_id=turn.mission_id,
                sequence_number=turn.sequence_number,
                prompt_text=turn.prompt_text,
                candidate_response=turn.candidate_response,
                created_at=turn.created_at,
            )
            self._db.add(model)
        else:
            model.mission_id = turn.mission_id
            model.sequence_number = turn.sequence_number
            model.prompt_text = turn.prompt_text
            model.candidate_response = turn.candidate_response
        self._db.commit()
        self._db.refresh(model)
        return turn


class SqlEvidenceRepository:
    def __init__(self, db: DbSession) -> None:
        self._db = db

    def get_evidence_for_session(self, session_id: str) -> list[Evidence]:
        models = self._db.query(EvidenceItemModel).filter(EvidenceItemModel.session_id == session_id).all()
        return [
            Evidence(
                id=m.id,
                session_id=m.session_id,
                turn_id=m.turn_id or "",
                competency=m.competency,
                observation=m.observation,
                polarity=EvidencePolarity(m.polarity),
                strength=m.strength,
                confidence=m.confidence,
                rationale=m.rationale,
            )
            for m in models
        ]

    def save(self, evidence: Evidence) -> Evidence:
        model = self._db.query(EvidenceItemModel).filter(EvidenceItemModel.id == evidence.id).first()
        if not model:
            model = EvidenceItemModel(
                id=evidence.id,
                session_id=evidence.session_id,
                turn_id=evidence.turn_id,
                competency=evidence.competency,
                observation=evidence.observation,
                polarity=evidence.polarity.value,
                strength=evidence.strength,
                confidence=evidence.confidence,
                rationale=evidence.rationale,
            )
            self._db.add(model)
        else:
            model.turn_id = evidence.turn_id
            model.competency = evidence.competency
            model.observation = evidence.observation
            model.polarity = evidence.polarity.value
            model.strength = evidence.strength
            model.confidence = evidence.confidence
            model.rationale = evidence.rationale
        self._db.commit()
        self._db.refresh(model)
        return evidence


class SqlMemoryRepository:
    def __init__(self, db: DbSession) -> None:
        self._db = db

    def get_memory_for_session(self, session_id: str) -> list[MemoryRecord]:
        models = self._db.query(MemoryRecordModel).filter(MemoryRecordModel.session_id == session_id).all()
        return [
            MemoryRecord(
                id=m.id,
                session_id=m.session_id,
                memory_type=m.memory_type,
                summary=m.summary,
                evidence_ids=tuple(m.evidence_ids),
                confidence=m.confidence,
            )
            for m in models
        ]

    def save(self, record: MemoryRecord) -> MemoryRecord:
        model = self._db.query(MemoryRecordModel).filter(MemoryRecordModel.id == record.id).first()
        if not model:
            model = MemoryRecordModel(
                id=record.id,
                session_id=record.session_id,
                memory_type=record.memory_type,
                summary=record.summary,
                evidence_ids=list(record.evidence_ids),
                confidence=record.confidence,
            )
            self._db.add(model)
        else:
            model.memory_type = record.memory_type
            model.summary = record.summary
            model.evidence_ids = list(record.evidence_ids)
            model.confidence = record.confidence
        self._db.commit()
        self._db.refresh(model)
        return record


class SqlEvaluationRepository:
    def __init__(self, db: DbSession) -> None:
        self._db = db

    def get_evaluations_for_session(self, session_id: str) -> list[Evaluation]:
        models = self._db.query(EvaluationModel).filter(EvaluationModel.session_id == session_id).all()
        return [
            Evaluation(
                id=m.id,
                session_id=m.session_id,
                competency=m.competency,
                score=m.score,
                confidence=m.confidence,
                evidence_ids=tuple(m.evidence_ids),
                rationale=m.rationale,
                improvement_guidance=m.improvement_guidance,
            )
            for m in models
        ]

    def save(self, evaluation: Evaluation) -> Evaluation:
        model = self._db.query(EvaluationModel).filter(EvaluationModel.id == evaluation.id).first()
        if not model:
            model = EvaluationModel(
                id=evaluation.id,
                session_id=evaluation.session_id,
                competency=evaluation.competency,
                score=evaluation.score,
                confidence=evaluation.confidence,
                evidence_ids=list(evaluation.evidence_ids),
                rationale=evaluation.rationale,
                improvement_guidance=evaluation.improvement_guidance,
            )
            self._db.add(model)
        else:
            model.score = evaluation.score
            model.confidence = evaluation.confidence
            model.evidence_ids = list(evaluation.evidence_ids)
            model.rationale = evaluation.rationale
            model.improvement_guidance = evaluation.improvement_guidance
        self._db.commit()
        self._db.refresh(model)
        return evaluation


class SqlWorldStateRepository:
    def __init__(self, db: DbSession) -> None:
        self._db = db

    def get_latest_for_session(self, session_id: str) -> WorldState | None:
        model = (
            self._db.query(WorldStateSnapshotModel)
            .filter(WorldStateSnapshotModel.session_id == session_id)
            .order_by(WorldStateSnapshotModel.state_version.desc())
            .first()
        )
        if not model:
            return None
        return WorldState(
            id=model.id,
            session_id=model.session_id,
            state=model.state_json,
            visible_summary=model.visible_summary,
            version=model.state_version,
        )

    def save(self, world_state: WorldState) -> WorldState:
        model = (
            self._db.query(WorldStateSnapshotModel)
            .filter(
                WorldStateSnapshotModel.session_id == world_state.session_id,
                WorldStateSnapshotModel.state_version == world_state.version,
            )
            .first()
        )
        if not model:
            model = WorldStateSnapshotModel(
                id=world_state.id,
                session_id=world_state.session_id,
                state_version=world_state.version,
                state_json=world_state.state,
                visible_summary=world_state.visible_summary,
                created_at=datetime.utcnow(),
            )
            self._db.add(model)
        else:
            model.state_json = world_state.state
            model.visible_summary = world_state.visible_summary
        self._db.commit()
        self._db.refresh(model)
        return world_state


class SqlMissionRepository:
    def __init__(self, db: DbSession) -> None:
        self._db = db

    def get_missions_for_session(self, session_id: str) -> list[Mission]:
        models = (
            self._db.query(MissionModel)
            .filter(MissionModel.session_id == session_id)
            .order_by(MissionModel.sequence_order)
            .all()
        )
        return [
            Mission(
                id=m.id,
                session_id=m.session_id,
                title=m.title,
                scenario=m.scenario,
                competency_targets=tuple(m.competency_targets.get("targets", [])),
                difficulty=m.difficulty,
            )
            for m in models
        ]

    def save(self, mission: Mission) -> Mission:
        model = self._db.query(MissionModel).filter(MissionModel.id == mission.id).first()
        if not model:
            model = MissionModel(
                id=mission.id,
                session_id=mission.session_id,
                title=mission.title,
                scenario=mission.scenario,
                competency_targets={"targets": list(mission.competency_targets)},
                difficulty=mission.difficulty,
                sequence_order=1,
            )
            self._db.add(model)
        else:
            model.title = mission.title
            model.scenario = mission.scenario
            model.competency_targets = {"targets": list(mission.competency_targets)}
            model.difficulty = mission.difficulty
        self._db.commit()
        self._db.refresh(model)
        return mission
