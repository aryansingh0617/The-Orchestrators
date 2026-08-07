# Implementation Plan

## Milestone Strategy

Development proceeds one milestone at a time. Each milestone ends with tests, build verification where applicable, documentation updates, one Conventional Commit, push when configured, and a stop for human confirmation.

## Milestone 1: Repository Scaffolding

Status: complete.

Scope:

- initialize Git repository
- add root metadata files
- create backend, frontend, docs, scripts, and tests directories
- avoid application code

Exit criteria:

- repository has clean structure
- scaffold commit exists
- remote branch is pushed

## Milestone 2: Documentation

Status: in progress.

Scope:

- product vision
- architecture
- system design
- implementation plan
- database schema
- API spec
- prompt architecture
- folder structure
- testing strategy
- Git workflow
- risks
- demo script

Exit criteria:

- all required docs exist
- docs define module boundaries
- docs define data, API, prompt, testing, and workflow contracts
- self-review weaknesses are addressed
- no application code is added

## Milestone 3: Backend Architecture

Scope:

- create Python package structure
- add FastAPI app shell
- add Pydantic settings
- define domain models and interfaces
- wire dependency injection placeholders
- add stub AI provider

Tests:

- app import test
- health endpoint test
- dependency wiring test

Commit:

- `feat(api): scaffold backend architecture`

## Milestone 4: Frontend Architecture

Scope:

- initialize Next.js TypeScript app
- configure TailwindCSS
- add shadcn/ui foundation
- create application shell
- define API client boundary

Tests:

- lint/build
- basic page rendering

Commit:

- `feat(ui): scaffold frontend architecture`

## Milestone 5: Database

Scope:

- add SQLAlchemy models
- add migrations
- implement repository interfaces
- create SQLite local configuration

Tests:

- migration up/down test
- repository CRUD tests

Commit:

- `feat(db): add assessment persistence schema`

## Milestone 6: Interview Planner

Scope:

- implement Curriculum Analyzer baseline
- implement Candidate Analyzer baseline
- implement Interview Planner service
- create mission plan DTOs

Tests:

- coverage planning
- time budget handling
- deterministic stub scenarios

Commit:

- `feat(planner): implement adaptive interview planner`

## Milestone 7: Memory Engine

Scope:

- implement memory records
- add evidence-linked memory updates
- add memory summarization

Tests:

- memory accumulation
- deduplication
- evidence links

Commit:

- `feat(memory): add reasoning memory engine`

## Milestone 8: Mission Generator

Scope:

- implement prompt registry
- add mission templates
- integrate AI provider abstraction
- support deterministic fallback

Tests:

- schema validation
- fallback behavior
- competency mapping

Commit:

- `feat(missions): implement adaptive mission generator`

## Milestone 9: World State Engine

Scope:

- implement state snapshot model
- add transition rules
- integrate visible candidate updates

Tests:

- valid transitions
- invalid transition rejection
- state immutability

Commit:

- `feat(world): implement dynamic interview state`

## Milestone 10: Evaluation Engine

Scope:

- implement Evidence Collector
- implement Evaluation Engine
- add rubric definitions
- enforce evidence-cited scoring

Tests:

- evidence extraction
- scoring references evidence
- insufficient evidence handling

Commit:

- `feat(eval): add evidence-based evaluation`

## Milestone 11: Feedback Engine

Scope:

- implement Engineering Profile Generator
- implement Hiring Recommendation Engine
- implement Feedback Generator

Tests:

- recommendation thresholds
- hidden notes do not leak
- feedback maps to evidence

Commit:

- `feat(feedback): generate candidate profile and recommendation`

## Milestone 12: REST API

Scope:

- implement session endpoints
- implement turn processing endpoint
- implement report endpoint
- add OpenAPI examples

Tests:

- endpoint validation
- error envelopes
- integration flow

Commit:

- `feat(api): implement assessment endpoints`

## Milestone 13: Frontend Integration

Scope:

- connect setup form to API
- add mission dashboard
- add candidate turn flow
- render report

Tests:

- build
- browser smoke test
- API integration test with stub backend

Commit:

- `feat(ui): integrate mission dashboard`

## Milestone 14: UI Polish

Scope:

- improve responsive layouts
- add loading and error states
- add evidence and world state visualization
- refine demo path

Tests:

- visual browser verification
- accessibility checks

Commit:

- `feat(ui): polish assessment experience`

## Milestone 15: Testing

Scope:

- expand unit tests
- add integration tests
- add critical E2E tests
- add coverage reporting

Tests:

- full backend test suite
- frontend build and tests
- E2E demo scenario

Commit:

- `test(core): add assessment integration coverage`

## Milestone 16: Deployment

Scope:

- configure production environment
- add deployment documentation
- verify frontend/backend deployment path

Tests:

- production build
- health check
- smoke tests

Commit:

- `chore(deploy): configure production deployment`

## Milestone 17: Performance Optimization

Scope:

- profile slow paths
- add caching where justified
- optimize prompt and provider calls
- review database indexes

Tests:

- latency checks
- load smoke tests
- regression tests

Commit:

- `perf(core): optimize assessment turn latency`

## Implementation Guardrails

- No module may depend directly on FastAPI request objects.
- No score may be generated without evidence.
- No AI provider SDK may be imported into domain or application services.
- No frontend component may duplicate backend scoring rules.
- No milestone may proceed with a dirty worktree.
- No push should overwrite remote history.

