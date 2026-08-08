from fastapi import FastAPI

from app.api.errors import register_exception_handlers
from app.api.routes.health import router as health_router
from app.api.routes.interview import router as interview_router
from app.core.settings import Settings, get_settings
from app.infrastructure.repositories.in_memory_sessions import (
    InMemoryEvidenceRepository,
    InMemoryMemoryRepository,
    InMemoryMissionRepository,
    InMemorySessionRepository,
    InMemoryTurnRepository,
    InMemoryWorldStateRepository,
)


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    app = FastAPI(
        title=resolved_settings.app_name,
        version=resolved_settings.app_version,
        description=(
            "Project Chimera API. Adaptive AI engineering interview behind POST /api/interview."
        ),
    )
    app.state.settings = resolved_settings

    if resolved_settings.environment == "test":
        app.state.session_repository = InMemorySessionRepository()
        app.state.turn_repository = InMemoryTurnRepository()
        app.state.evidence_repository = InMemoryEvidenceRepository()
        app.state.memory_repository = InMemoryMemoryRepository()
        app.state.mission_repository = InMemoryMissionRepository()
        app.state.world_state_repository = InMemoryWorldStateRepository()
    else:
        from app.infrastructure.database.base import Base
        from app.infrastructure.database.session import create_db_engine, get_session_factory
        from app.infrastructure.repositories import (
            SqlEvidenceRepository,
            SqlMemoryRepository,
            SqlMissionRepository,
            SqlSessionRepository,
            SqlTurnRepository,
            SqlWorldStateRepository,
        )

        engine = create_db_engine(resolved_settings.database_url)
        Base.metadata.create_all(bind=engine)
        session_factory = get_session_factory(resolved_settings.database_url)
        db_session = session_factory()
        app.state.db_session = db_session
        app.state.session_repository = SqlSessionRepository(db_session)
        app.state.turn_repository = SqlTurnRepository(db_session)
        app.state.evidence_repository = SqlEvidenceRepository(db_session)
        app.state.memory_repository = SqlMemoryRepository(db_session)
        app.state.mission_repository = SqlMissionRepository(db_session)
        app.state.world_state_repository = SqlWorldStateRepository(db_session)

    register_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(interview_router)
    return app


app = create_app()
