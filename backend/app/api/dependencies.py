from typing import Annotated

from fastapi import Depends, Request

from app.application.services import InterviewService
from app.core.clock import Clock, SystemClock
from app.core.ids import IdGenerator, UuidGenerator
from app.core.settings import Settings
from app.domain.interfaces import (
    AIProvider,
    EvidenceRepository,
    MemoryRepository,
    MissionRepository,
    SessionRepository,
    TurnRepository,
    WorldStateRepository,
)
from app.infrastructure.ai import StubProvider


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
    turns: Annotated[TurnRepository | None, Depends(get_turn_repository)],
    evidence: Annotated[EvidenceRepository | None, Depends(get_evidence_repository)],
    memory_repo: Annotated[MemoryRepository | None, Depends(get_memory_repository)],
    missions: Annotated[MissionRepository | None, Depends(get_mission_repository)],
    world_states: Annotated[WorldStateRepository | None, Depends(get_world_state_repository)],
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
    )
