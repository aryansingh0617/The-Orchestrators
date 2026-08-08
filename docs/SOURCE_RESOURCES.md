# Source Resources

## Purpose

This document records the attached resources that refine the implementation contract for Project Chimera. These resources are authoritative for the hackathon-facing interface.

## Attached Files

| File | Role |
| --- | --- |
| `technical-spec.md` | Defines required public API contract |
| `candidates.json` | Provides candidate profiles, mission history, and learning signals |
| `curriculum.json` | Provides the 31-day AI cohort curriculum used for assessment context |

## Technical Spec Requirements

The submission must expose one endpoint:

```text
POST /api/interview
```

Requirements:

- no authentication
- maintain state with `sessionId`
- first request includes `candidate`
- later requests include `message`
- response always includes `reply` and `done`
- final response includes `feedback`

Final feedback shape:

```json
{
  "summary": "...",
  "strengths": [],
  "gaps": [],
  "next": []
}
```

## Candidate Data Shape

The candidate resource contains a `candidates` array. Each candidate has:

- `member`: identity, role, years of experience, education, completion status
- `missions`: completed, failed, or skipped curriculum missions with attempts
- `signals`: aggregate commitment and completion metrics

Observed resource count:

- 20 candidates

Implementation implications:

- Candidate Analyzer should infer role-relevant baseline only from provided professional and learning data.
- Skipped or failed missions are evidence for probing areas, not final negative judgments.
- Attempts and first-try completion should influence starting difficulty, not final recommendation by themselves.
- The system must avoid protected-attribute or personality inference.

## Curriculum Data Shape

The curriculum resource contains:

- cohort label
- eight modules
- 31 day-level learning units
- tools and objectives for each day

Observed resource count:

- 8 modules
- 31 days

Implementation implications:

- Curriculum Analyzer should map days and objectives into competencies.
- Mission Generator should use curriculum titles and objectives to build realistic engineering missions.
- Interview Planner should emphasize gaps between candidate mission history and target role needs.

## Alignment Decision

The documented multi-module architecture remains valid, but the public HTTP surface is constrained to the required single endpoint. Internal modules are orchestrated by `POST /api/interview`.

This preserves the ambitious assessment operating system while satisfying the exact technical submission contract.
