from typing import Protocol

from app.domain.entities import (
    AssessmentSession,
    Candidate,
    CandidateTurn,
    Evaluation,
    Evidence,
    MemoryRecord,
    Mission,
    WorldState,
)


class SessionRepository(Protocol):
    def get_by_external_id(self, external_session_id: str) -> AssessmentSession | None:
        """Return a session by public sessionId."""

    def save(self, session: AssessmentSession) -> AssessmentSession:
        """Persist and return an assessment session."""


class CandidateRepository(Protocol):
    def get_by_id(self, candidate_id: str) -> Candidate | None:
        """Return a candidate by id."""

    def save(self, candidate: Candidate) -> Candidate:
        """Persist and return a candidate."""


class TurnRepository(Protocol):
    def get_turns_for_session(self, session_id: str) -> list[CandidateTurn]:
        """Return all turns for a session, ordered by sequence_number."""

    def save(self, turn: CandidateTurn) -> CandidateTurn:
        """Persist and return a candidate turn."""


class EvidenceRepository(Protocol):
    def get_evidence_for_session(self, session_id: str) -> list[Evidence]:
        """Return all evidence collected for a session."""

    def save(self, evidence: Evidence) -> Evidence:
        """Persist and return an evidence item."""


class MemoryRepository(Protocol):
    def get_memory_for_session(self, session_id: str) -> list[MemoryRecord]:
        """Return all memory records for a session."""

    def save(self, record: MemoryRecord) -> MemoryRecord:
        """Persist and return a memory record."""


class EvaluationRepository(Protocol):
    def get_evaluations_for_session(self, session_id: str) -> list[Evaluation]:
        """Return all competency evaluations for a session."""

    def save(self, evaluation: Evaluation) -> Evaluation:
        """Persist and return an evaluation."""


class WorldStateRepository(Protocol):
    def get_latest_for_session(self, session_id: str) -> WorldState | None:
        """Return the latest world state for a session."""

    def save(self, world_state: WorldState) -> WorldState:
        """Persist and return a world state snapshot."""


class MissionRepository(Protocol):
    def get_missions_for_session(self, session_id: str) -> list[Mission]:
        """Return all missions generated for a session."""

    def save(self, mission: Mission) -> Mission:
        """Persist and return a mission."""

