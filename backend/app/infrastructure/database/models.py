from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class CandidateModel(Base):
    __tablename__ = "candidates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    profile_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sessions: Mapped[list["AssessmentSessionModel"]] = relationship(back_populates="candidate")


class AssessmentSessionModel(Base):
    __tablename__ = "assessment_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    external_session_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    candidate_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("candidates.id"), nullable=True, index=True)
    role_title: Mapped[str] = mapped_column(String(255), nullable=False)
    seniority: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, index=True, default="draft")
    curriculum_source: Mapped[str] = mapped_column(Text, nullable=False, default="default")
    assessment_mode: Mapped[str] = mapped_column(String(50), nullable=False, default="standard")
    time_budget_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=45)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    candidate: Mapped["CandidateModel | None"] = relationship(back_populates="sessions")


class CompetencyTargetModel(Base):
    __tablename__ = "competency_targets"
    __table_args__ = (UniqueConstraint("session_id", "competency", name="uq_session_competency"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessment_sessions.id"), nullable=False)
    competency: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    expected_level: Mapped[str] = mapped_column(String(100), nullable=False, default="senior")
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="curriculum")


class MissionPlanModel(Base):
    __tablename__ = "mission_plans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessment_sessions.id"), nullable=False)
    plan_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    strategy: Mapped[str] = mapped_column(Text, nullable=False, default="adaptive")
    coverage_map: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    difficulty_curve: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MissionModel(Base):
    __tablename__ = "missions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessment_sessions.id"), nullable=False)
    plan_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("mission_plans.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario: Mapped[str] = mapped_column(Text, nullable=False)
    mission_type: Mapped[str] = mapped_column(String(100), nullable=False, default="debugging")
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    competency_targets: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    constraints: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    sequence_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


class TurnModel(Base):
    __tablename__ = "turns"
    __table_args__ = (UniqueConstraint("session_id", "sequence_number", name="uq_session_turn_seq"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessment_sessions.id"), nullable=False)
    mission_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("missions.id"), nullable=True)
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    candidate_response: Mapped[str] = mapped_column(Text, nullable=False)
    processing_status: Mapped[str] = mapped_column(String(50), nullable=False, default="accepted")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WorldStateSnapshotModel(Base):
    __tablename__ = "world_state_snapshots"
    __table_args__ = (UniqueConstraint("turn_id", "snapshot_type", name="uq_turn_snapshot_type"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessment_sessions.id"), nullable=False)
    turn_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("turns.id"), nullable=True)
    snapshot_type: Mapped[str] = mapped_column(String(50), nullable=False, default="after")
    state_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    state_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    visible_summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    hidden_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class EvidenceItemModel(Base):
    __tablename__ = "evidence_items"
    __table_args__ = (
        Index("idx_evidence_session_competency", "session_id", "competency"),
        Index("idx_evidence_turn_id", "turn_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessment_sessions.id"), nullable=False)
    turn_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("turns.id"), nullable=True)
    competency: Mapped[str] = mapped_column(String(255), nullable=False)
    observation: Mapped[str] = mapped_column(Text, nullable=False)
    polarity: Mapped[str] = mapped_column(String(50), nullable=False, default="positive")
    strength: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    rationale: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MemoryRecordModel(Base):
    __tablename__ = "memory_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessment_sessions.id"), nullable=False)
    memory_type: Mapped[str] = mapped_column(String(100), nullable=False, default="pattern")
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    last_seen_turn: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EvaluationModel(Base):
    __tablename__ = "evaluations"
    __table_args__ = (UniqueConstraint("session_id", "competency", name="uq_eval_session_competency"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessment_sessions.id"), nullable=False)
    competency: Mapped[str] = mapped_column(String(255), nullable=False)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    evidence_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    rationale: Mapped[str] = mapped_column(Text, nullable=False, default="")
    improvement_guidance: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("assessment_sessions.id"), nullable=False)
    report_type: Mapped[str] = mapped_column(String(100), nullable=False, default="candidate_feedback")
    content_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    generated_by: Mapped[str] = mapped_column(String(100), nullable=False, default="stub")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ProviderEventModel(Base):
    __tablename__ = "provider_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    operation: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="success")
    error_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
