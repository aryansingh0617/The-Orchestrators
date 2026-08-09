from pydantic import BaseModel, Field


class FeedbackReport(BaseModel):
    summary: str
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    next: list[str] = Field(default_factory=list)
    executive_summary: str = ""
    engineering_dna: dict[str, float] = Field(default_factory=dict)
    curriculum_coverage: list[int] = Field(default_factory=list)
    competency_scores: dict[str, float] = Field(default_factory=dict)
    evidence: list[str] = Field(default_factory=list)
    knowledge_gaps: list[str] = Field(default_factory=list)
    recommended_learning_path: list[str] = Field(default_factory=list)
    interview_progression: list[str] = Field(default_factory=list)
    hiring_assessment: str = ""
