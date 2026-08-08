from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CandidateMemberDTO(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str = Field(min_length=1)
    name: str | None = None
    jobRole: str | None = None
    yearsExperience: int | None = Field(default=None, ge=0)
    education: str | None = None
    status: str | None = None


class CandidateMissionDTO(BaseModel):
    model_config = ConfigDict(extra="allow")

    day: int = Field(ge=1)
    title: str = Field(min_length=1)
    passed: bool | None = None
    skipped: bool | None = None
    attempts: int | None = Field(default=None, ge=0)


class CandidateSignalsDTO(BaseModel):
    model_config = ConfigDict(extra="allow")

    commitDays: int | None = Field(default=None, ge=0)
    missionsCompleted: int | None = Field(default=None, ge=0)
    missionsFirstTry: int | None = Field(default=None, ge=0)


class CandidateDTO(BaseModel):
    model_config = ConfigDict(extra="allow")

    member: CandidateMemberDTO
    missions: list[CandidateMissionDTO] = Field(default_factory=list)
    signals: CandidateSignalsDTO | dict[str, Any] = Field(default_factory=dict)


class InterviewCommand(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    candidate: CandidateDTO | None = None
    message: str | None = Field(default=None, max_length=8000)


class FeedbackDTO(BaseModel):
    summary: str
    strengths: list[str]
    gaps: list[str]
    next: list[str]
    engineering_dna: dict[str, float] = Field(default_factory=dict)
    hiring_assessment: str | None = None


class MissionPublicDTO(BaseModel):
    title: str
    scenario: str
    context: str = ""
    constraints: list[str] = Field(default_factory=list)
    objective: str = ""
    competency: str
    curriculum_day: int
    difficulty: str
    mission_type: str = "debugging"


class WorldStatePublicDTO(BaseModel):
    visible_summary: str = ""
    system_state: dict[str, Any] = Field(default_factory=dict)
    version: int = 1
    candidate_decisions: list[str] = Field(default_factory=list)


class ProgressDTO(BaseModel):
    question_number: int = 0
    curriculum_days_covered: int = 0
    covered_curriculum_days: list[int] = Field(default_factory=list)
    minimum_questions: int = 8
    minimum_curriculum_days: int = 4


class EvaluationSummaryDTO(BaseModel):
    outcome: str
    overall_score: float | None = None
    rationale: str = ""


class InterviewResult(BaseModel):
    """Hackathon-compatible response with optional structured extensions."""

    reply: str
    done: bool
    feedback: FeedbackDTO | None = None
    session_id: str | None = None
    question_number: int | None = None
    curriculum_day: int | None = None
    competency: str | None = None
    mission: MissionPublicDTO | None = None
    world_state: WorldStatePublicDTO | None = None
    progress: ProgressDTO | None = None
    evaluation_summary: EvaluationSummaryDTO | None = None
    mode: str | None = None
