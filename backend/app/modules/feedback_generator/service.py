from __future__ import annotations

from app.modules.feedback_generator.schemas import FeedbackReport
from app.modules.memory_engine.schemas import InterviewMemory


class FeedbackGenerator:
    def generate(
        self,
        *,
        memory: InterviewMemory,
        engineering_dna: dict[str, float],
        competency_scores: dict[str, float],
        progression: list[str],
        role_title: str,
        seniority: str,
    ) -> FeedbackReport:
        strengths = memory.strengths[:5] or memory.demonstrated_concepts[:5] or [
            "Engaged with technical scenario prompts"
        ]
        gaps = memory.knowledge_gaps[:5] or memory.weaknesses[:5] or [
            "Needs deeper production measurement plans"
        ]
        learning = [
            f"Practice production drills for: {gap}" for gap in gaps[:3]
        ] or ["Revisit RAG evaluation and incident response labs."]

        avg = (
            sum(engineering_dna.values()) / len(engineering_dna)
            if engineering_dna
            else sum(competency_scores.values()) / max(1, len(competency_scores))
        )
        if avg >= 0.75:
            hiring = (
                f"Promising {seniority} {role_title} signal with strong evidence coverage. "
                "Recommend advance with standard panel confirmation."
            )
        elif avg >= 0.55:
            hiring = (
                f"Mixed {seniority} {role_title} signal. "
                "Recommend additional deep-dive on unresolved gaps before hiring decision."
            )
        else:
            hiring = (
                f"Below target bar for {seniority} {role_title} on demonstrated evidence. "
                "Recommend learning-path follow-up before re-interview."
            )

        summary = (
            f"Candidate demonstrated {', '.join(strengths[:2]) or 'foundational skills'} "
            f"across {len(memory.curriculum_coverage)} curriculum days, "
            f"with gaps in {', '.join(gaps[:2]) or 'production hardening'}."
        )

        return FeedbackReport(
            summary=summary,
            strengths=strengths,
            gaps=gaps,
            next=learning,
            executive_summary=summary,
            engineering_dna={k: round(v, 2) for k, v in engineering_dna.items()},
            curriculum_coverage=list(memory.curriculum_coverage),
            competency_scores={k: round(v, 2) for k, v in competency_scores.items()},
            evidence=memory.evidence[:12],
            knowledge_gaps=gaps,
            recommended_learning_path=learning,
            interview_progression=progression[-12:],
            hiring_assessment=hiring,
        )
