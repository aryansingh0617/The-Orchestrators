from app.domain.entities import AssessmentSession


class InMemorySessionRepository:
    def __init__(self) -> None:
        self._sessions_by_external_id: dict[str, AssessmentSession] = {}

    def get_by_external_id(self, external_session_id: str) -> AssessmentSession | None:
        return self._sessions_by_external_id.get(external_session_id)

    def save(self, session: AssessmentSession) -> AssessmentSession:
        self._sessions_by_external_id[session.external_session_id] = session
        return session
