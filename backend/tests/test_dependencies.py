from app.api.dependencies import (
    get_ai_provider,
    get_clock,
    get_id_generator,
    get_interview_service,
)
from app.core.settings import Settings
from app.infrastructure.repositories import (
    InMemoryEvidenceRepository,
    InMemoryMemoryRepository,
    InMemoryMissionRepository,
    InMemorySessionRepository,
    InMemoryTurnRepository,
    InMemoryWorldStateRepository,
)


def test_dependency_wiring_creates_interview_service() -> None:
    settings = Settings(environment="test", ai_provider="stub")
    service = get_interview_service(
        sessions=InMemorySessionRepository(),
        ai_provider=get_ai_provider(settings),
        clock=get_clock(),
        id_generator=get_id_generator(),
        turns=InMemoryTurnRepository(),
        evidence=InMemoryEvidenceRepository(),
        memory_repo=InMemoryMemoryRepository(),
        missions=InMemoryMissionRepository(),
        world_states=InMemoryWorldStateRepository(),
    )

    assert service is not None
