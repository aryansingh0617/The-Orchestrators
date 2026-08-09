from app.application.dtos import CandidateDTO, CandidateMemberDTO, InterviewCommand
from app.application.services import InterviewService
from app.core.clock import SystemClock
from app.core.ids import UuidGenerator
from app.infrastructure.ai import StubProvider
from app.infrastructure.repositories.in_memory_sessions import (
    InMemoryEvidenceRepository,
    InMemoryMemoryRepository,
    InMemoryMissionRepository,
    InMemorySessionRepository,
    InMemoryTurnRepository,
    InMemoryWorldStateRepository,
)
from app.modules.mission_generator import MissionGenerator


def test_mission_hides_evaluation_criteria_from_candidate_prompt() -> None:
    mission = MissionGenerator(StubProvider()).generate(
        competency="RAG Architecture",
        curriculum_day=1,
        difficulty="intermediate",
    )
    prompt = mission.candidate_facing_prompt()
    assert "hidden_evaluation_criteria" not in prompt
    assert mission.hidden_evaluation_criteria
    for criterion in mission.hidden_evaluation_criteria:
        assert criterion not in prompt


def test_interview_service_persists_turns_and_evidence() -> None:
    sessions = InMemorySessionRepository()
    turns = InMemoryTurnRepository()
    evidence = InMemoryEvidenceRepository()
    memory = InMemoryMemoryRepository()
    missions = InMemoryMissionRepository()
    worlds = InMemoryWorldStateRepository()
    service = InterviewService(
        sessions=sessions,
        ai_provider=StubProvider(),
        clock=SystemClock(),
        id_generator=UuidGenerator(),
        turns=turns,
        evidence=evidence,
        memory_repo=memory,
        missions=missions,
        world_states=worlds,
    )

    start = service.handle(
        InterviewCommand(
            session_id="persist-1",
            candidate=CandidateDTO(member=CandidateMemberDTO(id="C1", jobRole="AI Engineer")),
        )
    )
    assert start.done is False

    service.handle(
        InterviewCommand(
            session_id="persist-1",
            message=(
                "I would inspect logs and metrics, hypothesize a retrieval regression, "
                "and measure recall after a canary rollback plan."
            ),
        )
    )

    session = sessions.get_by_external_id("persist-1")
    assert session is not None
    assert turns.get_turns_for_session(session.id)
    assert evidence.get_evidence_for_session(session.id)
    assert missions.get_missions_for_session(session.id)
    assert worlds.get_latest_for_session(session.id) is not None
