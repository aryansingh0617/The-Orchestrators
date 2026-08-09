from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    competency: str
    observation: str
    polarity: str = "neutral"
    strength: int = Field(default=3, ge=1, le=5)
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)
    rationale: str = ""
    claim_label: str = "partial"


class EvaluationResult(BaseModel):
    outcome: str = Field(
        description="correct|partial|incorrect|unsupported|false_claim|shallow|strong"
    )
    technical_correctness: float = Field(default=0.5, ge=0.0, le=1.0)
    reasoning: float = Field(default=0.5, ge=0.0, le=1.0)
    depth: float = Field(default=0.5, ge=0.0, le=1.0)
    systems_thinking: float = Field(default=0.5, ge=0.0, le=1.0)
    tradeoffs: float = Field(default=0.5, ge=0.0, le=1.0)
    reliability: float = Field(default=0.5, ge=0.0, le=1.0)
    problem_solving: float = Field(default=0.5, ge=0.0, le=1.0)
    communication: float = Field(default=0.5, ge=0.0, le=1.0)
    adaptability: float = Field(default=0.5, ge=0.0, le=1.0)
    overall_score: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    rationale: str = ""
    engineering_dna: dict[str, float] = Field(default_factory=dict)
    claim_labels: list[str] = Field(default_factory=list)
