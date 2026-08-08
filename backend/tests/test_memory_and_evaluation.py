from app.modules.evaluation_engine import EvaluationEngine
from app.modules.interview_planner import InterviewPlanner, PlannerInput
from app.modules.memory_engine import MemoryEngine
from app.modules.mission_generator import MissionBrief


def test_memory_update_changes_planner_decision() -> None:
    memory_engine = MemoryEngine()
    planner = InterviewPlanner()
    memory = memory_engine.empty()

    before = planner.plan(
        PlannerInput(
            competencies=["RAG Architecture", "Vector Databases", "Prompt Engineering", "Agents"],
            curriculum_days=[1, 3, 5, 7],
            day_competency_map={
                1: "RAG Architecture",
                3: "Vector Databases",
                5: "Prompt Engineering",
                7: "Agents",
            },
            covered_curriculum_days=[1, 3],
            current_competency="RAG Architecture",
            current_curriculum_day=1,
            question_count=4,
            curriculum_day_coverage_count=2,
            evaluation_outcome="correct",
            previous_question="mission",
            candidate_answer="solid answer",
            follow_up_history=["deepen"],
            knowledge_gaps=[],
        )
    )

    memory = memory_engine.update(
        memory,
        competency="RAG Architecture",
        curriculum_day=1,
        evaluation_outcome="incorrect",
        evaluation_rationale="False claim about embeddings guaranteeing correctness",
        evidence_ids=["e1"],
        claim_labels=["false_claim"],
    )
    memory = memory_engine.update(
        memory,
        competency="RAG Architecture",
        curriculum_day=1,
        evaluation_outcome="incorrect",
        evaluation_rationale="Repeated misconception",
        evidence_ids=["e2"],
        claim_labels=["false_claim"],
    )

    after = planner.plan(
        PlannerInput(
            competencies=["RAG Architecture", "Vector Databases", "Prompt Engineering", "Agents"],
            curriculum_days=[1, 3, 5, 7],
            day_competency_map={
                1: "RAG Architecture",
                3: "Vector Databases",
                5: "Prompt Engineering",
                7: "Agents",
            },
            covered_curriculum_days=[1, 3],
            current_competency="Vector Databases",
            current_curriculum_day=3,
            question_count=5,
            curriculum_day_coverage_count=2,
            evaluation_outcome="partial",
            previous_question="mission",
            candidate_answer="partial answer",
            follow_up_history=["deepen"],
            knowledge_gaps=list(memory.knowledge_gaps),
            misunderstood_concepts=list(memory.misunderstood_concepts),
            unresolved_issues=list(memory.unresolved_issues),
        )
    )

    assert "RAG Architecture" in memory.knowledge_gaps
    assert memory.repeated_mistakes
    assert after.mode in {"revisit_gap", "follow_up", "deepen", "new_mission"}
    assert after.mode != before.mode or after.next_curriculum_day != before.next_curriculum_day or after.reason != before.reason


def test_evaluation_empty_answer() -> None:
    engine = EvaluationEngine()
    result = engine.evaluate(
        mission=MissionBrief(
            title="t",
            scenario="s",
            competency="RAG",
            curriculum_day=1,
        ),
        candidate_answer="",
    )
    assert result.outcome == "incorrect"
    assert result.overall_score == 0.0
