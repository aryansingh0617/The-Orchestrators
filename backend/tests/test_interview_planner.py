from app.modules.interview_planner import InterviewPlanner, PlannerInput


def test_planner_requires_minimum_coverage_before_completion() -> None:
    planner = InterviewPlanner()
    decision = planner.plan(
        PlannerInput(
            competencies=["RAG", "Vectors", "Prompts", "Agents"],
            curriculum_days=[1, 3, 5, 7],
            day_competency_map={1: "RAG", 3: "Vectors", 5: "Prompts", 7: "Agents"},
            covered_curriculum_days=[1],
            current_competency="RAG",
            current_curriculum_day=1,
            question_count=3,
            curriculum_day_coverage_count=1,
            evaluation_outcome="correct",
            previous_question="Explain RAG failure modes",
            candidate_answer="I would inspect retrieval logs and measure recall.",
            follow_up_history=["deepen"],
        )
    )
    assert decision.mode != "completion"
    assert decision.mode in {"new_mission", "follow_up", "deepen", "revisit_gap"}


def test_planner_follow_up_on_incorrect_evaluation() -> None:
    planner = InterviewPlanner()
    decision = planner.plan(
        PlannerInput(
            competencies=["RAG"],
            curriculum_days=[1, 3, 5, 7],
            day_competency_map={1: "RAG", 3: "Vectors", 5: "Prompts", 7: "Agents"},
            covered_curriculum_days=[1],
            current_competency="RAG",
            current_curriculum_day=1,
            question_count=2,
            curriculum_day_coverage_count=1,
            evaluation_outcome="incorrect",
            previous_question="Diagnose the recall drop",
            candidate_answer="Just change the prompt.",
            follow_up_history=[],
        )
    )
    assert decision.mode == "follow_up"
    assert decision.next_curriculum_day == 1


def test_planner_does_not_blindly_cycle_days() -> None:
    planner = InterviewPlanner()
    first = planner.plan(
        PlannerInput(
            competencies=["RAG", "Vectors", "Prompts", "Agents"],
            curriculum_days=[1, 3, 5, 7],
            day_competency_map={1: "RAG", 3: "Vectors", 5: "Prompts", 7: "Agents"},
            covered_curriculum_days=[1, 3],
            current_competency="Vectors",
            current_curriculum_day=3,
            question_count=4,
            curriculum_day_coverage_count=2,
            evaluation_outcome="strong",
            previous_question="q",
            candidate_answer="strong production answer with metrics",
            follow_up_history=["deepen"],
            knowledge_gaps=["Prompts"],
        )
    )
    assert first.mode in {"revisit_gap", "new_mission", "deepen"}
    if first.mode == "new_mission":
        assert first.next_curriculum_day not in {1, 3}


def test_planner_completion_when_targets_met() -> None:
    planner = InterviewPlanner()
    decision = planner.plan(
        PlannerInput(
            competencies=["RAG", "Vectors", "Prompts", "Agents"],
            curriculum_days=[1, 3, 5, 7],
            day_competency_map={1: "RAG", 3: "Vectors", 5: "Prompts", 7: "Agents"},
            covered_curriculum_days=[1, 3, 5, 7],
            current_competency="Agents",
            current_curriculum_day=7,
            question_count=8,
            curriculum_day_coverage_count=4,
            knowledge_gaps=[],
            unresolved_issues=[],
        )
    )
    assert decision.mode == "completion"
