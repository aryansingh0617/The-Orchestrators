from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any


class SessionStatus(StrEnum):
    DRAFT = "draft"
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class EvidencePolarity(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass(frozen=True, slots=True)
class Competency:
    name: str
    description: str = ""
    priority: int = 3


@dataclass(frozen=True, slots=True)
class Mission:
    id: str
    session_id: str
    title: str
    scenario: str
    competency_targets: tuple[str, ...] = ()
    difficulty: int = 1


@dataclass(frozen=True, slots=True)
class CandidateTurn:
    id: str
    session_id: str
    sequence_number: int
    prompt_text: str
    candidate_response: str
    created_at: datetime
    mission_id: str | None = None


@dataclass(frozen=True, slots=True)
class WorldState:
    id: str
    session_id: str
    state: dict[str, Any] = field(default_factory=dict)
    visible_summary: str = ""
    version: int = 1


@dataclass(frozen=True, slots=True)
class Evidence:
    id: str
    session_id: str
    turn_id: str
    competency: str
    observation: str
    polarity: EvidencePolarity
    strength: int
    confidence: float
    rationale: str


@dataclass(frozen=True, slots=True)
class Evaluation:
    id: str
    session_id: str
    competency: str
    score: float | None
    confidence: float
    evidence_ids: tuple[str, ...]
    rationale: str
    improvement_guidance: str


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    id: str
    session_id: str
    memory_type: str
    summary: str
    evidence_ids: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(slots=True)
class AssessmentSession:
    id: str
    external_session_id: str
    candidate_id: str | None
    role_title: str
    seniority: str
    status: SessionStatus
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class Candidate:
    id: str
    display_name: str | None
    email: str | None
    profile_summary: str | None
    created_at: datetime
    updated_at: datetime

