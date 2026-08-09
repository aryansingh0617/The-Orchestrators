"""
Deterministic Chimera demo runner (stub provider).

Showcase:
1) Candidate onboarding
2) Personalized first mission
3) Candidate answer
4) Adaptive follow-up
5) World-state consequence
6) New curriculum area
7) Knowledge-gap revisit (when signals create gaps)
8) Final Engineering DNA
9) Actionable feedback

Usage (from backend/):
  python -m scripts.demo_interview
"""

from __future__ import annotations

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

STRONG = (
    "I would form a root-cause hypothesis from retrieval traces and metrics, "
    "compare latency and recall before/after the index refresh, avoid prompt-only fixes, "
    "add caching carefully while watching memory usage, define a canary rollback trigger, "
    "and measure p95 latency plus groundedness after release."
)
WEAK = "Just rewrite the prompt; embeddings guarantee correctness anyway."
PARTIAL = "I would check logs and maybe change chunk size, but I am unsure what to measure."


def build_service() -> InterviewService:
    return InterviewService(
        sessions=InMemorySessionRepository(),
        ai_provider=StubProvider(),
        clock=SystemClock(),
        id_generator=UuidGenerator(),
        turns=InMemoryTurnRepository(),
        evidence=InMemoryEvidenceRepository(),
        memory_repo=InMemoryMemoryRepository(),
        missions=InMemoryMissionRepository(),
        world_states=InMemoryWorldStateRepository(),
    )


def main() -> None:
    service = build_service()
    session_id = "demo-session-001"
    start = service.handle(
        InterviewCommand(
            session_id=session_id,
            candidate=CandidateDTO(
                member=CandidateMemberDTO(
                    id="CAND-DEMO",
                    name="Emily Chen",
                    jobRole="AI Engineer",
                    yearsExperience=6,
                    education="MS Artificial Intelligence",
                ),
                missions=[],
                signals={"commitDays": 31, "missionsCompleted": 20, "missionsFirstTry": 18},
            ),
        )
    )
    print("=== 1/2 ONBOARDING + FIRST MISSION ===")
    print(f"mode={start.mode} day={start.curriculum_day} competency={start.competency}")
    print(start.mission.model_dump_json(indent=2) if start.mission else "no mission")
    print(start.world_state.visible_summary if start.world_state else "")

    scripted = [WEAK, PARTIAL, STRONG, STRONG, WEAK, STRONG, STRONG, STRONG, STRONG, STRONG]
    for idx, answer in enumerate(scripted, start=1):
        result = service.handle(InterviewCommand(session_id=session_id, message=answer))
        print(f"\n=== TURN {idx} mode={result.mode} q={result.question_number} ===")
        print(f"day={result.curriculum_day} competency={result.competency}")
        if result.evaluation_summary:
            print(f"eval={result.evaluation_summary.outcome} score={result.evaluation_summary.overall_score}")
        if result.world_state:
            print(result.world_state.visible_summary)
        if result.progress:
            print(
                "progress:",
                result.progress.question_number,
                "questions /",
                result.progress.curriculum_days_covered,
                "days",
                result.progress.covered_curriculum_days,
            )
        if result.done:
            print("\n=== FINAL FEEDBACK / ENGINEERING DNA ===")
            print(result.feedback.model_dump_json(indent=2) if result.feedback else "{}")
            break
    else:
        raise SystemExit("Demo did not reach completion; check planner thresholds.")


if __name__ == "__main__":
    main()
