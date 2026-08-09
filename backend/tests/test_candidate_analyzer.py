from app.application.dtos import (
    CandidateDTO,
    CandidateMemberDTO,
    CandidateMissionDTO,
    CandidateSignalsDTO,
)
from app.infrastructure.ai import StubProvider
from app.modules.candidate_analyzer import CandidateAnalyzer


class FailingProvider:
    provider_name = "failing"

    def generate_structured(self, *args, **kwargs):
        raise RuntimeError("provider down")


def test_candidate_analyzer_uses_missions_and_signals() -> None:
    analyzer = CandidateAnalyzer(StubProvider())
    candidate = CandidateDTO(
        member=CandidateMemberDTO(
            id="CAND-1",
            name="Emily Chen",
            jobRole="AI Engineer",
            yearsExperience=6,
        ),
        missions=[
            CandidateMissionDTO(day=1, title="RAG Basics", passed=True, attempts=1),
            CandidateMissionDTO(day=7, title="Agents", passed=False, attempts=3),
            CandidateMissionDTO(day=9, title="MCP", skipped=True, attempts=0),
        ],
        signals=CandidateSignalsDTO(commitDays=31, missionsCompleted=20, missionsFirstTry=18),
    )

    result = analyzer.analyze(candidate)
    assert result.role_target == "AI Engineer"
    assert result.seniority == "senior"
    assert 1 in result.completed_mission_days
    assert "Agents" in result.possible_weaknesses or "Agents" in result.areas_to_probe
    assert "MCP" in result.skipped_topics or "MCP" in result.areas_to_probe
    assert 1 <= result.starting_difficulty <= 5
    assert 0.0 <= result.confidence <= 1.0


def test_candidate_analyzer_provider_failure_is_deterministic() -> None:
    analyzer = CandidateAnalyzer(FailingProvider())  # type: ignore[arg-type]
    result = analyzer.analyze(
        profile_summary="Built RAG systems",
        role_target="AI Engineer",
        seniority="mid",
        completed_missions=[CandidateMissionDTO(day=2, title="Chunking", passed=True, attempts=1)],
    )
    assert result.starting_difficulty >= 1
    assert result.baseline_strengths
    assert result.confidence > 0
