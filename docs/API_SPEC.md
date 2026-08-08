# API Specification

## Hackathon Contract

The required public API exposes exactly one unauthenticated endpoint:

```text
POST /api/interview
```

The endpoint maintains interview state with the provided `sessionId`. All internal planning, mission generation, world state, memory, evidence, evaluation, and feedback services operate behind this endpoint for the hackathon submission.

No authentication is required for the hackathon contract.

## Design Decision

Chimera keeps the assessment operating-system architecture internally while presenting the simple required agent API externally.

- Public API: single `POST /api/interview` endpoint.
- Internal services: session management, planner, memory, world state, evidence, evaluation, and feedback modules.
- Persistence key: `sessionId` from the request.
- Candidate source: first request contains the supplied candidate object.
- Curriculum source: loaded from the supplied curriculum resource or configured fixture.

## Start Interview

The first request initializes a new interview session.

```json
{
  "sessionId": "abc-123",
  "candidate": {
    "member": {
      "id": "CAND-003",
      "name": "Emily Chen",
      "jobRole": "AI Engineer",
      "yearsExperience": 6,
      "education": "MS Artificial Intelligence",
      "status": "COMPLETED"
    },
    "missions": [
      {
        "day": 7,
        "title": "Embeddings Explained",
        "passed": true,
        "attempts": 1
      }
    ],
    "signals": {
      "commitDays": 31,
      "missionsCompleted": 31,
      "missionsFirstTry": 30
    }
  }
}
```

Rules:

- `sessionId` is required.
- `candidate` is required only on the first request for a session.
- The candidate object follows the attached `candidates.json` candidate-entry schema.
- The backend initializes internal session state, candidate baseline, curriculum targets, and first mission prompt.

Response:

```json
{
  "reply": "Welcome. Let's begin your interview.",
  "done": false
}
```

Chimera may include a more specific first mission in `reply` as long as the response shape remains compatible.

## Conversation Turn

Subsequent requests contain the candidate's latest response.

```json
{
  "sessionId": "abc-123",
  "message": "I would compare retrieval outputs before and after the index refresh, then inspect failed evaluation examples."
}
```

Rules:

- `sessionId` must match an existing session.
- `message` is required for non-initial turns.
- The backend loads world state, memory, mission progress, and evidence for the session.
- The backend returns the next adaptive interview reply.

Response:

```json
{
  "reply": "Good. The retrieval logs show shorter chunks after the refresh. What mitigation would you ship today, and what would you measure after release?",
  "done": false
}
```

## End Interview

When the interview is complete, the endpoint returns `done: true` and feedback.

```json
{
  "reply": "Interview completed.",
  "done": true,
  "feedback": {
    "summary": "The candidate showed strong retrieval debugging and production awareness, with some opportunity to deepen cost analysis.",
    "strengths": [
      "Compared retrieval behavior before proposing prompt changes.",
      "Connected mitigation choices to measurable production signals."
    ],
    "gaps": [
      "Could quantify latency and cost tradeoffs earlier."
    ],
    "next": [
      "Practice designing evaluation sets for RAG regressions.",
      "Prepare examples of observability dashboards for AI systems."
    ]
  }
}
```

## Response Schema

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| reply | string | Yes | Candidate-facing interviewer response |
| done | boolean | Yes | Whether the interview is complete |
| feedback | object | Only when done is true | Final candidate feedback |

## Feedback Schema

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| summary | string | Yes | Concise overall assessment |
| strengths | string[] | Yes | Actionable positive observations |
| gaps | string[] | Yes | Actionable improvement areas |
| next | string[] | Yes | Recommended next steps |

## Validation and Error Handling

The hackathon contract does not define a formal error schema, but Chimera should return predictable JSON.

Recommended error response:

```json
{
  "reply": "I could not process that request because the sessionId is missing.",
  "done": false
}
```

Validation rules:

- Missing `sessionId`: return a helpful error reply.
- Unknown `sessionId` without `candidate`: ask the caller to start with candidate data.
- Initial request without valid candidate object: return a helpful error reply.
- Empty `message` on a conversation turn: ask for a response.
- Provider failure: use deterministic fallback instead of failing the session where possible.

## Internal Service Mapping

`POST /api/interview` maps to internal use cases:

| API Condition | Internal Use Case |
| --- | --- |
| `candidate` present and session is new | Create session, analyze candidate, analyze curriculum, plan first mission |
| `message` present and session active | Process turn, collect evidence, update memory/world state, generate next reply |
| stopping criteria reached | Generate feedback and complete session |
| provider unavailable | Use stub/template fallback |

## OpenAPI Requirements

The FastAPI implementation must document:

- `POST /api/interview` summary and description
- start request example
- turn request example
- completion response example
- validation notes
- feedback schema

## Non-MVP Internal APIs

Earlier planning documents describe session, evidence, and report resources as internal architectural concepts. They should not be exposed as public HTTP endpoints for the hackathon submission unless the technical specification changes.

