from typing import Protocol

from app.domain.entities import AssessmentSession


class SessionRepository(Protocol):
    def get_by_external_id(self, external_session_id: str) -> AssessmentSession | None:
        """Return a session by public sessionId."""

    def save(self, session: AssessmentSession) -> AssessmentSession:
        """Persist and return an assessment session."""
