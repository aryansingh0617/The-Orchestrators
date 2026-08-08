from typing import Annotated

from fastapi import Depends, Request

from app.application.services import InterviewService
from app.core.clock import Clock, SystemClock
from app.core.ids import IdGenerator, UuidGenerator
from app.core.settings import Settings
from app.domain.interfaces import AIProvider, SessionRepository
from app.infrastructure.ai import StubProvider


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_session_repository(request: Request) -> SessionRepository:
    return request.app.state.session_repository


def get_ai_provider(settings: Annotated[Settings, Depends(get_settings)]) -> AIProvider:
    if settings.ai_provider == "stub":
        return StubProvider()
    return StubProvider()


def get_clock() -> Clock:
    return SystemClock()


def get_id_generator() -> IdGenerator:
    return UuidGenerator()


def get_interview_service(
    sessions: Annotated[SessionRepository, Depends(get_session_repository)],
    ai_provider: Annotated[AIProvider, Depends(get_ai_provider)],
    clock: Annotated[Clock, Depends(get_clock)],
    id_generator: Annotated[IdGenerator, Depends(get_id_generator)],
) -> InterviewService:
    return InterviewService(
        sessions=sessions,
        ai_provider=ai_provider,
        clock=clock,
        id_generator=id_generator,
    )
