from fastapi import FastAPI

from app.api.errors import register_exception_handlers
from app.api.routes.health import router as health_router
from app.api.routes.interview import router as interview_router
from app.core.settings import Settings, get_settings
from app.infrastructure.repositories.in_memory_sessions import InMemorySessionRepository


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    app = FastAPI(
        title=resolved_settings.app_name,
        version=resolved_settings.app_version,
        description=(
            "Project Chimera API. Milestone 3 exposes the backend shell, health check, "
            "and the required interview endpoint contract."
        ),
    )
    app.state.settings = resolved_settings

    if resolved_settings.environment == "test":
        app.state.session_repository = InMemorySessionRepository()
    else:
        from app.infrastructure.database.base import Base
        from app.infrastructure.database.session import create_db_engine, get_session_factory
        from app.infrastructure.repositories import SqlSessionRepository

        engine = create_db_engine(resolved_settings.database_url)
        Base.metadata.create_all(bind=engine)
        session_factory = get_session_factory(resolved_settings.database_url)
        
        # Open a session for the singleton session repository (or handle session per request later)
        db_session = session_factory()
        app.state.db_session = db_session
        app.state.session_repository = SqlSessionRepository(db_session)

    register_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(interview_router)
    return app


app = create_app()
