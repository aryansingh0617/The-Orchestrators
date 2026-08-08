from typing import Annotated

from fastapi import Depends, Request

from app.application.services import InterviewService
from app.core.clock import Clock, SystemClock
from app.core.ids import IdGenerator, UuidGenerator
from app.core.settings import Settings
from app.domain.errors import ProviderError
from app.domain.interfaces import (
    AIProvider,
    EvidenceRepository,
    MemoryRepository,
    MissionRepository,
    SessionRepository,
    TurnRepository,
    WorldStateRepository,
)
from app.infrastructure.ai import OpenAIProvider, StubProvider


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_session_repository(request: Request) -> SessionRepository:
    return request.app.state.session_repository


def get_turn_repository(request: Request) -> TurnRepository | None:
    return getattr(request.app.state, "turn_repository", None)


def get_evidence_repository(request: Request) -> EvidenceRepository | None:
    return getattr(request.app.state, "evidence_repository", None)


def get_memory_repository(request: Request) -> MemoryRepository | None:
    return getattr(request.app.state, "memory_repository", None)


def get_mission_repository(request: Request) -> MissionRepository | None:
    return getattr(request.app.state, "mission_repository", None)


def get_world_state_repository(request: Request) -> WorldStateRepository | None:
    return getattr(request.app.state, "world_state_repository", None)


def build_ai_provider(settings: Settings) -> AIProvider:
    if settings.demo_mode or settings.environment == "test":
        return StubProvider()
    if settings.ai_provider == "openai":
        if not settings.openai_api_key:
            raise ProviderError(
                "CHIMERA_OPENAI_API_KEY is required when CHIMERA_AI_PROVIDER=openai."
            )
        return OpenAIProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            timeout_seconds=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,
        )
    return StubProvider()


def get_ai_provider(settings: Annotated[Settings, Depends(get_settings)]) -> AIProvider:
    return build_ai_provider(settings)


def get_clock() -> Clock:
    return SystemClock()


def get_id_generator() -> IdGenerator:
    return UuidGenerator()


def get_interview_service(
    sessions: Annotated[SessionRepository, Depends(get_session_repository)],
    ai_provider: Annotated[AIProvider, Depends(get_ai_provider)],
    clock: Annotated[Clock, Depends(get_clock)],
    id_generator: Annotated[IdGenerator, Depends(get_id_generator)],
    turns: Annotated[TurnRepository | None, Depends(get_turn_repository)],
    evidence: Annotated[EvidenceRepository | None, Depends(get_evidence_repository)],
    memory_repo: Annotated[MemoryRepository | None, Depends(get_memory_repository)],
    missions: Annotated[MissionRepository | None, Depends(get_mission_repository)],
    world_states: Annotated[WorldStateRepository | None, Depends(get_world_state_repository)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> InterviewService:
    return InterviewService(
        sessions=sessions,
        ai_provider=ai_provider,
        clock=clock,
        id_generator=id_generator,
        turns=turns,
        evidence=evidence,
        memory_repo=memory_repo,
        missions=missions,
        world_states=world_states,
        max_message_length=settings.max_message_length,
    )
