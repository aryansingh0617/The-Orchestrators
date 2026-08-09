from pydantic import BaseModel, Field


class MissionBrief(BaseModel):
    title: str
    scenario: str
    context: str = ""
    constraints: list[str] = Field(default_factory=list)
    objective: str = ""
    competency: str
    curriculum_day: int
    difficulty: str = "intermediate"
    mission_type: str = "debugging"
    expected_evidence: list[str] = Field(default_factory=list)
    hidden_evaluation_criteria: list[str] = Field(default_factory=list)
    followup_options: list[str] = Field(default_factory=list)

    def candidate_facing_prompt(self) -> str:
        constraints = "; ".join(self.constraints) if self.constraints else "None specified"
        return (
            f"Mission: {self.title}\n"
            f"Curriculum Day {self.curriculum_day} · {self.competency} · {self.difficulty}\n"
            f"Scenario: {self.scenario}\n"
            f"Context: {self.context or 'Production AI engineering assessment.'}\n"
            f"Constraints: {constraints}\n"
            f"Objective: {self.objective or 'Diagnose the issue and propose a production-ready plan.'}"
        )
