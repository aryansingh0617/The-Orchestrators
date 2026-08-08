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


class InMemorySessionRepository:
    def __init__(self) -> None:
        self._sessions_by_external_id: dict[str, AssessmentSession] = {}

    def get_by_external_id(self, external_session_id: str) -> AssessmentSession | None:
        return self._sessions_by_external_id.get(external_session_id)

    def save(self, session: AssessmentSession) -> AssessmentSession:
        self._sessions_by_external_id[session.external_session_id] = session
        return session


class InMemoryCandidateRepository:
    def __init__(self) -> None:
        self._items: dict[str, Candidate] = {}

    def get_by_id(self, candidate_id: str) -> Candidate | None:
        return self._items.get(candidate_id)

    def save(self, candidate: Candidate) -> Candidate:
        self._items[candidate.id] = candidate
        return candidate


class InMemoryTurnRepository:
    def __init__(self) -> None:
        self._items: dict[str, CandidateTurn] = {}

    def get_turns_for_session(self, session_id: str) -> list[CandidateTurn]:
        turns = [t for t in self._items.values() if t.session_id == session_id]
        return sorted(turns, key=lambda t: t.sequence_number)

    def save(self, turn: CandidateTurn) -> CandidateTurn:
        self._items[turn.id] = turn
        return turn


class InMemoryEvidenceRepository:
    def __init__(self) -> None:
        self._items: dict[str, Evidence] = {}

    def get_evidence_for_session(self, session_id: str) -> list[Evidence]:
        return [e for e in self._items.values() if e.session_id == session_id]

    def save(self, evidence: Evidence) -> Evidence:
        self._items[evidence.id] = evidence
        return evidence


class InMemoryMemoryRepository:
    def __init__(self) -> None:
        self._items: dict[str, MemoryRecord] = {}

    def get_memory_for_session(self, session_id: str) -> list[MemoryRecord]:
        return [m for m in self._items.values() if m.session_id == session_id]

    def save(self, record: MemoryRecord) -> MemoryRecord:
        self._items[record.id] = record
        return record


class InMemoryEvaluationRepository:
    def __init__(self) -> None:
        self._items: dict[str, Evaluation] = {}

    def get_evaluations_for_session(self, session_id: str) -> list[Evaluation]:
        return [e for e in self._items.values() if e.session_id == session_id]

    def save(self, evaluation: Evaluation) -> Evaluation:
        self._items[evaluation.id] = evaluation
        return evaluation


class InMemoryWorldStateRepository:
    def __init__(self) -> None:
        self._items: list[WorldState] = []

    def get_latest_for_session(self, session_id: str) -> WorldState | None:
        matches = [w for w in self._items if w.session_id == session_id]
        if not matches:
            return None
        return max(matches, key=lambda w: w.version)

    def save(self, world_state: WorldState) -> WorldState:
        self._items.append(world_state)
        return world_state


class InMemoryMissionRepository:
    def __init__(self) -> None:
        self._items: dict[str, Mission] = {}

    def get_missions_for_session(self, session_id: str) -> list[Mission]:
        return [m for m in self._items.values() if m.session_id == session_id]

    def save(self, mission: Mission) -> Mission:
        self._items[mission.id] = mission
        return mission
