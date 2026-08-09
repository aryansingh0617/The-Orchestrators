from pydantic import BaseModel, Field


class InterviewMemory(BaseModel):
    demonstrated_concepts: list[str] = Field(default_factory=list)
    misunderstood_concepts: list[str] = Field(default_factory=list)
    repeated_mistakes: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    curriculum_coverage: list[int] = Field(default_factory=list)
    knowledge_gaps: list[str] = Field(default_factory=list)
    unresolved_issues: list[str] = Field(default_factory=list)
