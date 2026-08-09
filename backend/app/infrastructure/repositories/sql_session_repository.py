from sqlalchemy.orm import Session as DbSession

from app.domain.entities.assessment import AssessmentSession, SessionStatus
from app.infrastructure.database.models import AssessmentSessionModel


class SqlSessionRepository:
    def __init__(self, db: DbSession) -> None:
        self._db = db

    def get_by_external_id(self, external_session_id: str) -> AssessmentSession | None:
        model = (
            self._db.query(AssessmentSessionModel)
            .filter(AssessmentSessionModel.external_session_id == external_session_id)
            .first()
        )
        if not model:
            return None
        return self._to_domain(model)

    def save(self, session: AssessmentSession) -> AssessmentSession:
        model = (
            self._db.query(AssessmentSessionModel)
            .filter(AssessmentSessionModel.external_session_id == session.external_session_id)
            .first()
        )
        if not model:
            model = AssessmentSessionModel(
                id=session.id,
                external_session_id=session.external_session_id,
                candidate_id=session.candidate_id,
                role_title=session.role_title,
                seniority=session.seniority,
                status=session.status.value if isinstance(session.status, SessionStatus) else str(session.status),
                created_at=session.created_at,
                updated_at=session.updated_at,
            )
            self._db.add(model)
        else:
            model.status = session.status.value if isinstance(session.status, SessionStatus) else str(session.status)
            model.role_title = session.role_title
            model.seniority = session.seniority
            model.updated_at = session.updated_at

        self._db.commit()
        self._db.refresh(model)
        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: AssessmentSessionModel) -> AssessmentSession:
        status_enum = SessionStatus(model.status) if model.status in SessionStatus._value2member_map_ else SessionStatus.ACTIVE
        return AssessmentSession(
            id=model.id,
            external_session_id=model.external_session_id,
            candidate_id=model.candidate_id,
            role_title=model.role_title,
            seniority=model.seniority,
            status=status_enum,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
