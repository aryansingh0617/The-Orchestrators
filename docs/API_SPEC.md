# API Specification

## API Style

The backend exposes REST endpoints through FastAPI. All request and response bodies use Pydantic models. OpenAPI documentation must include descriptions, examples, response codes, and validation constraints.

Base URL:

- local backend: `http://localhost:8000`

## Common Error Envelope

```json
{
  "error": {
    "code": "validation_error",
    "message": "The request body is invalid.",
    "details": {},
    "trace_id": "trace_123"
  }
}
```

## Status Codes

| Code | Meaning |
| --- | --- |
| 200 | Successful read or command result |
| 201 | Resource created |
| 400 | Invalid domain command |
| 404 | Resource not found |
| 409 | State conflict |
| 422 | Request validation error |
| 503 | AI provider or dependency unavailable |

## Endpoints

## GET /health

Purpose: Verify service availability.

Response example:

```json
{
  "status": "ok",
  "service": "chimera-api",
  "version": "0.1.0"
}
```

## POST /api/sessions

Purpose: Create an assessment session.

Request:

```json
{
  "candidate": {
    "display_name": "Riya Shah",
    "email": "riya@example.com",
    "profile_summary": "Backend engineer with LLM application experience."
  },
  "role_title": "AI Engineer",
  "seniority": "senior",
  "curriculum_source": "RAG systems, evaluation, observability, deployment tradeoffs.",
  "assessment_mode": "demo",
  "time_budget_minutes": 30
}
```

Response:

```json
{
  "session_id": "session_123",
  "status": "draft",
  "candidate_id": "candidate_123"
}
```

Validation:

- `role_title` is required
- `seniority` must be supported
- `curriculum_source` cannot be empty
- `time_budget_minutes` must be between 10 and 180

Errors:

- `422` for malformed request
- `400` for unsupported assessment mode

## POST /api/sessions/{session_id}/plan

Purpose: Analyze curriculum and create a mission plan.

Request:

```json
{
  "force_replan": false
}
```

Response:

```json
{
  "session_id": "session_123",
  "plan_id": "plan_123",
  "status": "planned",
  "competencies": [
    {
      "name": "debugging",
      "priority": 1,
      "expected_level": "senior"
    }
  ],
  "missions": [
    {
      "mission_id": "mission_123",
      "title": "Diagnose a failing RAG incident",
      "difficulty": 3,
      "targets": ["debugging", "systems_thinking"]
    }
  ]
}
```

Errors:

- `404` if session is missing
- `409` if session is already active and `force_replan` is false
- `503` if provider fails and no fallback is available

## POST /api/sessions/{session_id}/start

Purpose: Start a planned assessment.

Response:

```json
{
  "session_id": "session_123",
  "status": "active",
  "current_mission": {
    "mission_id": "mission_123",
    "title": "Diagnose a failing RAG incident",
    "prompt": "A support assistant is producing plausible but unsupported answers after a retrieval deployment. Walk through your investigation."
  },
  "world_state": {
    "visible_summary": "Customer escalations increased after yesterday's retrieval index refresh."
  }
}
```

Errors:

- `409` if the session has not been planned

## POST /api/sessions/{session_id}/turns

Purpose: Submit a candidate response and receive the next mission update.

Request:

```json
{
  "mission_id": "mission_123",
  "candidate_response": "I would first compare retrieved chunks before and after the index refresh, inspect eval failures, and check whether citations map to source documents.",
  "client_sequence_number": 1
}
```

Response:

```json
{
  "turn_id": "turn_123",
  "session_id": "session_123",
  "mission_id": "mission_123",
  "accepted": true,
  "visible_world_update": "The retrieval logs show the new index returns shorter chunks with weaker source coverage.",
  "next_prompt": "Given those logs, what mitigation would you ship today and what would you measure after release?",
  "evidence_preview": [
    {
      "competency": "debugging",
      "observation": "Candidate asked to compare retrieval outputs before proposing a fix.",
      "polarity": "positive"
    }
  ]
}
```

Validation:

- `candidate_response` cannot be empty
- `client_sequence_number` must match the expected next turn

Errors:

- `404` if session or mission is missing
- `409` for stale sequence number or completed session
- `503` when processing cannot complete

## GET /api/sessions/{session_id}

Purpose: Get session state and progress.

Response:

```json
{
  "session_id": "session_123",
  "status": "active",
  "role_title": "AI Engineer",
  "seniority": "senior",
  "progress": {
    "turns_completed": 3,
    "competencies_touched": 4,
    "estimated_minutes_remaining": 12
  }
}
```

## GET /api/sessions/{session_id}/evidence

Purpose: Retrieve evidence collected during the session.

Response:

```json
{
  "items": [
    {
      "evidence_id": "evidence_123",
      "turn_id": "turn_123",
      "competency": "debugging",
      "observation": "Candidate proposed validating retrieval outputs before changing prompts.",
      "polarity": "positive",
      "strength": 4,
      "confidence": 0.88
    }
  ]
}
```

## POST /api/sessions/{session_id}/complete

Purpose: Complete assessment and generate final reports.

Response:

```json
{
  "session_id": "session_123",
  "status": "completed",
  "report_ids": {
    "engineering_profile": "report_profile_123",
    "hiring_recommendation": "report_hiring_123",
    "candidate_feedback": "report_feedback_123"
  }
}
```

Errors:

- `409` if required evidence coverage is insufficient and forced completion is not allowed

## GET /api/sessions/{session_id}/reports/{report_type}

Purpose: Retrieve a report.

Supported report types:

- `engineering_profile`
- `hiring_recommendation`
- `candidate_feedback`

Response:

```json
{
  "report_type": "hiring_recommendation",
  "content": {
    "recommendation": "lean_hire",
    "confidence": 0.78,
    "rationale": "Strong debugging and systems evidence; weaker cost analysis evidence.",
    "evidence_ids": ["evidence_123", "evidence_456"],
    "human_review_required": true
  }
}
```

Report rules:

- `hiring_recommendation` must include `human_review_required`.
- Numeric competency scores must include evidence references.
- Low-coverage reports must return caveats or an insufficient-evidence recommendation.
- Candidate feedback responses must exclude hidden evaluator notes.

## OpenAPI Requirements

Every endpoint implementation must include:

- summary
- description
- request examples
- success response examples
- documented error responses
- Pydantic field constraints
