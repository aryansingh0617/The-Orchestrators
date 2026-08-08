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
    session_id: str = Field(min_length=1)
    candidate: CandidateDTO | None = None
    message: str | None = None


class FeedbackDTO(BaseModel):
    summary: str
    strengths: list[str]
    gaps: list[str]
    next: list[str]


class InterviewResult(BaseModel):
    reply: str
    done: bool
    feedback: FeedbackDTO | None = None
