# Database Schema

## Goals

The database stores the assessment audit trail. It must preserve enough context to explain how a final recommendation was produced.

Schema priorities:

- evidence traceability
- immutable turn history
- reproducible reports
- role and curriculum configuration
- provider-agnostic storage

## Technology

- SQLAlchemy ORM
- Alembic migrations
- SQLite for local development
- PostgreSQL-compatible schema for production

## Tables

## candidates

Stores candidate identity and optional profile data.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| display_name | String | Optional |
| email | String | Optional, unique when present |
| profile_summary | Text | Optional resume/profile summary |
| created_at | DateTime | Required |
| updated_at | DateTime | Required |

## assessment_sessions

Stores one assessment instance.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| external_session_id | String | Supplied `sessionId`, unique |
| candidate_id | UUID | FK to candidates |
| role_title | String | Required |
| seniority | String | Required |
| status | String | draft, planned, active, completed, cancelled, failed |
| curriculum_source | Text | Required |
| assessment_mode | String | demo, standard, deep_dive |
| time_budget_minutes | Integer | Required |
| created_at | DateTime | Required |
| updated_at | DateTime | Required |
| completed_at | DateTime | Nullable |

Indexes:

- `idx_sessions_external_session_id`
- `idx_sessions_candidate_id`
- `idx_sessions_status`
- `idx_sessions_created_at`

## competency_targets

Stores target skills derived from curriculum.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| session_id | UUID | FK to assessment_sessions |
| competency | String | Required |
| description | Text | Required |
| priority | Integer | 1 high, 5 low |
| expected_level | String | junior, mid, senior, staff |
| source | String | curriculum, default, operator |

Unique constraint:

- `session_id`, `competency`

## mission_plans

Stores the planned assessment arc.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| session_id | UUID | FK to assessment_sessions |
| plan_version | Integer | Required |
| strategy | Text | Required |
| coverage_map | JSON | Required |
| difficulty_curve | JSON | Required |
| status | String | active, superseded |
| created_at | DateTime | Required |

## missions

Stores individual mission definitions.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| session_id | UUID | FK |
| plan_id | UUID | FK to mission_plans |
| title | String | Required |
| scenario | Text | Required |
| mission_type | String | debugging, design, incident, tradeoff, review |
| difficulty | Integer | 1-5 |
| competency_targets | JSON | Required |
| constraints | JSON | Required |
| status | String | pending, active, completed, skipped |
| sequence_order | Integer | Required |

## turns

Stores immutable candidate interactions.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| session_id | UUID | FK |
| mission_id | UUID | FK |
| sequence_number | Integer | Required |
| prompt_text | Text | Candidate-facing prompt |
| candidate_response | Text | Candidate response |
| processing_status | String | accepted, failed, retryable |
| created_at | DateTime | Required |

Unique constraint:

- `session_id`, `sequence_number`

## world_state_snapshots

Stores before/after state for each turn.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| session_id | UUID | FK |
| turn_id | UUID | FK |
| snapshot_type | String | before, after |
| state_version | Integer | Required |
| state_json | JSON | Required |
| visible_summary | Text | Candidate-visible state |
| hidden_notes | Text | Evaluator-only notes |
| created_at | DateTime | Required |

Unique constraint:

- `turn_id`, `snapshot_type`

## evidence_items

Stores atomic evaluation evidence.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| session_id | UUID | FK |
| turn_id | UUID | FK |
| competency | String | Required |
| observation | Text | Required |
| polarity | String | positive, negative, neutral |
| strength | Integer | 1-5 |
| confidence | Float | 0.0-1.0 |
| rationale | Text | Required |
| created_at | DateTime | Required |

Indexes:

- `idx_evidence_session_competency`
- `idx_evidence_turn_id`

## memory_records

Stores durable candidate behavior signals.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| session_id | UUID | FK |
| memory_type | String | strength, gap, pattern, assumption |
| summary | Text | Required |
| evidence_ids | JSON | Required |
| confidence | Float | Required |
| last_seen_turn | Integer | Required |
| created_at | DateTime | Required |
| updated_at | DateTime | Required |

## evaluations

Stores competency-level evaluations.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| session_id | UUID | FK |
| competency | String | Required |
| score | Float | Nullable when insufficient evidence |
| confidence | Float | Required |
| evidence_ids | JSON | Required |
| rationale | Text | Required |
| improvement_guidance | Text | Required |
| created_at | DateTime | Required |
| updated_at | DateTime | Required |

Unique constraint:

- `session_id`, `competency`

## reports

Stores generated final reports.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| session_id | UUID | FK |
| report_type | String | engineering_profile, hiring_recommendation, candidate_feedback |
| content_json | JSON | Required |
| generated_by | String | provider or stub |
| created_at | DateTime | Required |

## provider_events

Stores AI provider calls for debugging and cost/latency analysis. Prompt contents may be redacted depending on environment.

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| session_id | UUID | Nullable |
| provider | String | Required |
| operation | String | structured_generation, embedding, moderation |
| model | String | Nullable |
| latency_ms | Integer | Required |
| status | String | success, failed, fallback |
| error_code | String | Nullable |
| metadata_json | JSON | Required |
| created_at | DateTime | Required |

## Data Integrity Rules

- A turn cannot be deleted after creation.
- A completed session cannot accept new turns.
- An evaluation with a numeric score must reference at least one evidence item.
- A report must reference a completed or active session.
- World state snapshots are append-only.

## Retention

MVP retention is manual. Production retention should support:

- configurable candidate data deletion
- anonymized aggregate analytics
- report export before deletion
- audit logs for deletion actions
