from pydantic import BaseModel, Field


class PlanningDecision(BaseModel):
    next_curriculum_day: int = Field(description="The curriculum day for the next turn")
    competency: str = Field(description="The competency to target")
    difficulty: str = Field(description="Difficulty: basic, intermediate, advanced, expert")
    mode: str = Field(
        description="Mode: new_mission, follow_up, deepen, revisit_gap, completion"
    )
    reason: str = Field(description="Planner rationale")
    evidence_needed: list[str] = Field(default_factory=list)


class PlannerInput(BaseModel):
    candidate_strengths: list[str] = Field(default_factory=list)
    areas_to_probe: list[str] = Field(default_factory=list)
    starting_difficulty: int = Field(default=2, ge=1, le=5)
    competencies: list[str] = Field(default_factory=list)
    curriculum_days: list[int] = Field(default_factory=list)
    day_competency_map: dict[int, str] = Field(default_factory=dict)
    covered_curriculum_days: list[int] = Field(default_factory=list)
    current_competency: str | None = None
    current_curriculum_day: int | None = None
    previous_question: str | None = None
    candidate_answer: str | None = None
    evaluation_outcome: str | None = None
    evaluation_score: float | None = None
    evidence_collected: list[str] = Field(default_factory=list)
    knowledge_gaps: list[str] = Field(default_factory=list)
    demonstrated_concepts: list[str] = Field(default_factory=list)
    misunderstood_concepts: list[str] = Field(default_factory=list)
    difficulty: str = "intermediate"
    follow_up_history: list[str] = Field(default_factory=list)
    question_count: int = 0
    curriculum_day_coverage_count: int = 0
    minimum_question_count: int = 8
    minimum_curriculum_days: int = 4
    unresolved_issues: list[str] = Field(default_factory=list)
