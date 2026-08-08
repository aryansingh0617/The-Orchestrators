"""initial chimera schema

Revision ID: 1969bf990e87
Revises:
Create Date: 2026-08-09 00:12:35.385711
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "1969bf990e87"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "candidates",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True, unique=True),
        sa.Column("profile_summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "assessment_sessions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("external_session_id", sa.String(length=255), nullable=False),
        sa.Column("candidate_id", sa.String(length=36), sa.ForeignKey("candidates.id"), nullable=True),
        sa.Column("role_title", sa.String(length=255), nullable=False),
        sa.Column("seniority", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("curriculum_source", sa.Text(), nullable=False),
        sa.Column("assessment_mode", sa.String(length=50), nullable=False),
        sa.Column("time_budget_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_assessment_sessions_external_session_id", "assessment_sessions", ["external_session_id"], unique=True)
    op.create_index("ix_assessment_sessions_candidate_id", "assessment_sessions", ["candidate_id"])
    op.create_index("ix_assessment_sessions_status", "assessment_sessions", ["status"])
    op.create_index("ix_assessment_sessions_created_at", "assessment_sessions", ["created_at"])

    op.create_table(
        "competency_targets",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=36), sa.ForeignKey("assessment_sessions.id"), nullable=False),
        sa.Column("competency", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("expected_level", sa.String(length=100), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.UniqueConstraint("session_id", "competency", name="uq_session_competency"),
    )
    op.create_table(
        "mission_plans",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=36), sa.ForeignKey("assessment_sessions.id"), nullable=False),
        sa.Column("plan_version", sa.Integer(), nullable=False),
        sa.Column("strategy", sa.Text(), nullable=False),
        sa.Column("coverage_map", sa.JSON(), nullable=False),
        sa.Column("difficulty_curve", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "missions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=36), sa.ForeignKey("assessment_sessions.id"), nullable=False),
        sa.Column("plan_id", sa.String(length=36), sa.ForeignKey("mission_plans.id"), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("scenario", sa.Text(), nullable=False),
        sa.Column("mission_type", sa.String(length=100), nullable=False),
        sa.Column("difficulty", sa.Integer(), nullable=False),
        sa.Column("competency_targets", sa.JSON(), nullable=False),
        sa.Column("constraints", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("sequence_order", sa.Integer(), nullable=False),
    )
    op.create_table(
        "turns",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=36), sa.ForeignKey("assessment_sessions.id"), nullable=False),
        sa.Column("mission_id", sa.String(length=36), sa.ForeignKey("missions.id"), nullable=True),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("prompt_text", sa.Text(), nullable=False),
        sa.Column("candidate_response", sa.Text(), nullable=False),
        sa.Column("processing_status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("session_id", "sequence_number", name="uq_session_turn_seq"),
    )
    op.create_table(
        "world_state_snapshots",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=36), sa.ForeignKey("assessment_sessions.id"), nullable=False),
        sa.Column("turn_id", sa.String(length=36), sa.ForeignKey("turns.id"), nullable=True),
        sa.Column("snapshot_type", sa.String(length=50), nullable=False),
        sa.Column("state_version", sa.Integer(), nullable=False),
        sa.Column("state_json", sa.JSON(), nullable=False),
        sa.Column("visible_summary", sa.Text(), nullable=False),
        sa.Column("hidden_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("turn_id", "snapshot_type", name="uq_turn_snapshot_type"),
    )
    op.create_table(
        "evidence_items",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=36), sa.ForeignKey("assessment_sessions.id"), nullable=False),
        sa.Column("turn_id", sa.String(length=36), sa.ForeignKey("turns.id"), nullable=True),
        sa.Column("competency", sa.String(length=255), nullable=False),
        sa.Column("observation", sa.Text(), nullable=False),
        sa.Column("polarity", sa.String(length=50), nullable=False),
        sa.Column("strength", sa.Integer(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index("idx_evidence_session_competency", "evidence_items", ["session_id", "competency"])
    op.create_index("idx_evidence_turn_id", "evidence_items", ["turn_id"])
    op.create_table(
        "memory_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=36), sa.ForeignKey("assessment_sessions.id"), nullable=False),
        sa.Column("memory_type", sa.String(length=100), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("last_seen_turn", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "evaluations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=36), sa.ForeignKey("assessment_sessions.id"), nullable=False),
        sa.Column("competency", sa.String(length=255), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("improvement_guidance", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("session_id", "competency", name="uq_eval_session_competency"),
    )
    op.create_table(
        "reports",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=36), sa.ForeignKey("assessment_sessions.id"), nullable=False),
        sa.Column("report_type", sa.String(length=100), nullable=False),
        sa.Column("content_json", sa.JSON(), nullable=False),
        sa.Column("generated_by", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "provider_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=36), nullable=True),
        sa.Column("provider", sa.String(length=100), nullable=False),
        sa.Column("operation", sa.String(length=100), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("error_code", sa.String(length=100), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("provider_events")
    op.drop_table("reports")
    op.drop_table("evaluations")
    op.drop_table("memory_records")
    op.drop_index("idx_evidence_turn_id", table_name="evidence_items")
    op.drop_index("idx_evidence_session_competency", table_name="evidence_items")
    op.drop_table("evidence_items")
    op.drop_table("world_state_snapshots")
    op.drop_table("turns")
    op.drop_table("missions")
    op.drop_table("mission_plans")
    op.drop_table("competency_targets")
    op.drop_index("ix_assessment_sessions_created_at", table_name="assessment_sessions")
    op.drop_index("ix_assessment_sessions_status", table_name="assessment_sessions")
    op.drop_index("ix_assessment_sessions_candidate_id", table_name="assessment_sessions")
    op.drop_index("ix_assessment_sessions_external_session_id", table_name="assessment_sessions")
    op.drop_table("assessment_sessions")
    op.drop_table("candidates")
