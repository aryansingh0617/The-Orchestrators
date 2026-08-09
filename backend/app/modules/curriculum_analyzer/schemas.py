from pydantic import BaseModel, Field


class CurriculumDayDetail(BaseModel):
    day: int
    topic: str
    learning_objective: str = ""
    tools: list[str] = Field(default_factory=list)
    prerequisites: list[int] = Field(default_factory=list)
    module: str = ""


class CompetencyDetail(BaseModel):
    name: str = Field(description="Name of the competency/skill")
    description: str = Field(description="Description of what this competency measures")
    priority: int = Field(description="Priority rating from 1 (highest) to 5 (lowest)")
    related_days: list[int] = Field(default_factory=list)


class CurriculumAnalysisResult(BaseModel):
    competencies: list[CompetencyDetail] = Field(default_factory=list)
    priority_levels: dict[str, int] = Field(default_factory=dict)
    expected_seniority_bar: str = Field(default="mid")
    mission_family_recommendations: list[str] = Field(default_factory=list)
    out_of_scope_topics: list[str] = Field(default_factory=list)
    curriculum_days: list[CurriculumDayDetail] = Field(default_factory=list)
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
