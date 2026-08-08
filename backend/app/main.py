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
    app.state.session_repository = InMemorySessionRepository()

    register_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(interview_router)
    return app


app = create_app()
