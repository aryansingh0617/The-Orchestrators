from __future__ import annotations

from app.modules.memory_engine.schemas import InterviewMemory


class MemoryEngine:
    """Structured interview memory that influences planner decisions."""

    def empty(self) -> InterviewMemory:
        return InterviewMemory()

    def update(
        self,
        memory: InterviewMemory,
        *,
        competency: str,
        curriculum_day: int,
        evaluation_outcome: str,
        evaluation_rationale: str,
        evidence_ids: list[str],
        claim_labels: list[str] | None = None,
    ) -> InterviewMemory:
        demonstrated = list(memory.demonstrated_concepts)
        misunderstood = list(memory.misunderstood_concepts)
        repeated = list(memory.repeated_mistakes)
        strengths = list(memory.strengths)
        weaknesses = list(memory.weaknesses)
        gaps = list(memory.knowledge_gaps)
        unresolved = list(memory.unresolved_issues)
        coverage = list(dict.fromkeys([*memory.curriculum_coverage, curriculum_day]))
        evidence = list(dict.fromkeys([*memory.evidence, *evidence_ids]))
        labels = claim_labels or []

        outcome = evaluation_outcome.lower()
        if outcome in {"correct", "strong"}:
            demonstrated = _unique([*demonstrated, competency, *labels])
            strengths = _unique([*strengths, competency])
            gaps = [g for g in gaps if g != competency]
            unresolved = [u for u in unresolved if competency.lower() not in u.lower()]
        elif outcome in {"partial", "shallow"}:
            weaknesses = _unique([*weaknesses, competency])
            gaps = _unique([*gaps, competency])
            unresolved = _unique([*unresolved, f"Shallow coverage of {competency}"])
            if competency in misunderstood:
                repeated = _unique([*repeated, competency])
        elif outcome in {"incorrect", "false_claim", "unsupported"}:
            misunderstood = _unique([*misunderstood, competency, *labels])
            weaknesses = _unique([*weaknesses, competency])
            gaps = _unique([*gaps, competency])
            if competency in memory.misunderstood_concepts or competency in memory.weaknesses:
                repeated = _unique([*repeated, competency])
            unresolved = _unique([*unresolved, f"Unresolved misconception: {competency}"])

        confidence = min(
            0.95,
            0.4
            + 0.05 * len(demonstrated)
            + 0.03 * len(coverage)
            - 0.04 * len(repeated),
        )
        confidence = max(0.2, confidence)

        return InterviewMemory(
            demonstrated_concepts=demonstrated,
            misunderstood_concepts=misunderstood,
            repeated_mistakes=repeated,
            strengths=strengths,
            weaknesses=weaknesses,
            evidence=evidence,
            confidence=round(confidence, 2),
            curriculum_coverage=coverage,
            knowledge_gaps=gaps,
            unresolved_issues=unresolved,
        )


def _unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys([i for i in items if i]))
