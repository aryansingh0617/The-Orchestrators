# Testing Strategy

## Goals

Testing must prove that Chimera is modular, evidence-based, adaptive, and safe to demo. The test suite should catch architectural regressions as well as normal code defects.

## Test Pyramid

| Level | Purpose | Examples |
| --- | --- | --- |
| Unit | Validate isolated domain logic and module contracts | scoring, planning, memory updates |
| Integration | Validate use cases across repositories and providers | process turn, generate report |
| API | Validate FastAPI endpoints and error envelopes | session lifecycle endpoints |
| Frontend | Validate UI rendering and user flows | setup form, mission dashboard |
| E2E | Validate complete demo path | create session to final report |

## Backend Unit Tests

Required for each module:

- valid input produces expected structured output
- invalid input raises domain-specific error
- fallback path works
- output references required IDs
- no forbidden framework dependency is imported

Module-specific examples:

- Interview Planner covers all required competencies.
- World State Engine preserves immutable snapshots.
- Evidence Collector does not create evidence for unsupported claims.
- Evaluation Engine refuses to score without evidence.
- Feedback Generator does not leak hidden evaluator notes.

## AI Provider Tests

The AI provider abstraction must be tested with:

- deterministic stub provider
- structured output validation
- invalid provider output retry
- timeout fallback
- provider event logging

Production provider tests should be optional and skipped unless credentials are configured.

## Prompt Tests

Each prompt requires:

- schema validation test
- golden fixture test
- fallback test
- hidden content leakage test where applicable
- insufficient evidence test for evaluators

Prompt tests should run without network calls by using stub outputs.

## Repository Tests

Repository tests validate:

- create/read/update flows
- constraints and indexes
- transaction rollback on errors
- immutable turn behavior
- evidence and evaluation relationships

SQLite is acceptable for local tests. Production compatibility should be checked before deployment if PostgreSQL is used.

## API Tests

API tests validate:

- request validation
- documented response shape
- error envelope consistency
- session lifecycle state conflicts
- OpenAPI generation

Critical API flows:

1. create session
2. plan session
3. start session
4. submit turn
5. inspect evidence
6. complete session
7. retrieve report

## Frontend Tests

Frontend tests validate:

- setup form validation
- mission prompt rendering
- loading and error states
- evidence/report presentation
- responsive layout smoke checks

The frontend must not duplicate scoring decisions. Tests should verify that it renders API-provided evaluation data.

## E2E Demo Test

The demo test should run against deterministic backend mode.

Scenario:

1. Create senior AI Engineer assessment.
2. Plan missions from RAG/evaluation curriculum.
3. Start assessment.
4. Submit candidate response focused on prompt-only fix.
5. Verify world state adapts to expose data quality issue.
6. Submit improved debugging response.
7. Complete assessment.
8. Verify report includes evidence-cited scores.

## Quality Gates

Before each milestone commit:

- run relevant tests
- run lint/format when configured
- run build when app packages exist
- inspect `git status`
- inspect staged diff

Milestone 2 exception:

- no application tests exist yet
- verification is docs-only scope and clean Git state

## Coverage Targets

Initial targets:

- domain and application modules: 85 percent line coverage
- API routes: 80 percent route coverage
- frontend critical flows: smoke coverage

Coverage is a signal, not the only quality measure. Evidence traceability and fallback behavior are higher priority than raw percentages.

## Regression Risks to Test

- scoring without evidence
- hidden note leakage
- provider outage breaks full session
- stale turn sequence accepted
- world state changes without rationale
- candidate profile creates unsupported sensitive inference
- hiring recommendation omits human review language
- confidence is treated as equivalent to score
