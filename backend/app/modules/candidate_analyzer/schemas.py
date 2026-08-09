from pydantic import BaseModel, Field


class CandidateAnalysisResult(BaseModel):
    baseline_strengths: list[str] = Field(default_factory=list)
    areas_to_probe: list[str] = Field(default_factory=list)
    starting_difficulty: int = Field(default=2, ge=1, le=5)
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    known_strengths: list[str] = Field(default_factory=list)
    possible_weaknesses: list[str] = Field(default_factory=list)
    completed_mission_days: list[int] = Field(default_factory=list)
    skipped_topics: list[str] = Field(default_factory=list)
    role_target: str = ""
    seniority: str = "mid"
