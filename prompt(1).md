# CHIMERA --- Prompt Log

> **Project:** CHIMERA --- Adaptive AI Interviewer\
> **Repository:** `The-Orchestrators`\
> **Purpose:** Consolidated AI-assisted development prompt log for the
> hackathon submission.

## Important note

This is a consolidated prompt log reconstructed from the CHIMERA
development workflow retained in the conversation history. Exact wording
is preserved where it was retained; where only the task/result was
retained, the prompt is a faithful reconstruction rather than a claim of
verbatim transcript. This avoids inventing wording that is not
available.

------------------------------------------------------------------------

## 1. Product and Architecture

``` text
You are a senior AI systems architect and full-stack engineer.

We are building CHIMERA, an Adaptive AI Interviewer for a hackathon.

The goal is NOT to create a generic chatbot. The system must treat an interview as an evolving stateful system where every candidate response can influence what happens next.

Design the project as a production-quality monorepo with a polished frontend, FastAPI backend, clear domain/application/infrastructure separation, AI provider abstraction, persistent interview state, candidate analysis, curriculum-aware interview planning, evidence extraction, evaluation, memory, mission generation, world-state tracking, feedback generation, tests, documentation, and deployment readiness.

Before changing code:
1. Inspect the existing repository.
2. Preserve working functionality.
3. Do not blindly redesign existing modules.
4. Reuse existing conventions where appropriate.
5. Identify dependencies between components.
6. Plan the implementation before editing.

Implement incrementally and keep the repository runnable after every milestone.
```

## 2. Hackathon / Vibe Coding Strategy

``` text
We are not trying to write the most code—we are trying to maximize the judging score.

Optimize CHIMERA around originality, prompt engineering, and working deployment.

The project should demonstrate a unique and memorable idea, a real problem, strong technical wow factor, AI as a core feature, clear architecture decisions, iterative AI-assisted development, debugging/refinement, polished UX, and stable deployment.

Do not use giant one-shot prompts for the entire project. Use an iterative workflow:
1. Planning
2. Architecture
3. UI design
4. Features
5. AI integration
6. Fixes
7. Optimization
8. Final polish

Prioritize stability over feature count.
```

## 3. Milestone 3 --- Backend Architecture

``` text
You are implementing Milestone 3 of CHIMERA in the existing repository.

Do NOT redesign or restart the project.

First inspect the current repository and implement the pending backend architecture in-place.

Requirements:
- FastAPI application
- Application settings/configuration
- Domain entities
- Domain interfaces
- Application services
- Dependency injection
- AI provider abstraction
- StubProvider for deterministic/local/demo operation
- Provider error handling
- Health endpoint
- Interview endpoint foundation
- Clear separation between domain, application, infrastructure, and API layers
- Automated tests for the architecture

The backend must remain runnable after the changes.
Do not hard-code secrets.
Add useful configuration through environment variables.

At the end run tests, fix failures, run formatting/lint/type checks where available, show changed files, and commit the milestone.
```

## 4. Milestones 4--12 Master Prompt

``` text
Continue development of CHIMERA from the existing repository.

Do NOT restart or redesign the project.

Implement the remaining milestones sequentially.

For every milestone:
1. Inspect the existing implementation.
2. Plan the change.
3. Implement only the required scope.
4. Preserve existing functionality.
5. Add or update tests.
6. Run the relevant test suite.
7. Fix all failures caused by the change.
8. Update documentation if the architecture/API changes.
9. Create a dedicated commit.

Progress through persistence, AI integration, interview planning, candidate analysis, curriculum analysis, memory, mission generation, world-state tracking, evaluation, feedback generation, API completion, frontend integration, end-to-end testing, and deployment preparation.

The interview must remain adaptive. A candidate response must be capable of changing the next interview action based on accumulated evidence and state.

Do not fake adaptive behavior with a static list of questions.
Use deterministic stubs for tests and demos where external AI access is unavailable.
```

## 5. Milestones 5--17 Master Prompt

``` text
Continue CHIMERA from the current implementation and complete the remaining engineering milestones without restarting the repository.

Work sequentially and keep every milestone independently testable.

Milestone 5: database foundation, SQLAlchemy models, database sessions, Alembic, initial migration, repositories, persistence tests.
Milestone 6: interview planner, curriculum-aware planning, candidate-aware planning, adaptive next-step selection.
Milestone 7: candidate analyzer and structured candidate profile.
Milestone 8: memory engine and persistent interview memory.
Milestone 9: mission generator and dynamic technical missions.
Milestone 10: world-state engine and explicit interview state transitions.
Milestone 11: evaluation engine and evidence-based scoring.
Milestone 12: feedback generator and explainable candidate feedback.
Milestone 13: OpenAI provider, StubProvider, provider abstraction, timeouts, retries, configuration.
Milestone 14: complete API integration and POST /api/interview contract.
Milestone 15: frontend integration and interview flow.
Milestone 16: full/adversarial/end-to-end testing.
Milestone 17: deployment, environment variables, README, migrations, demo script, security review, and final verification.

Do not sacrifice stability for unnecessary features.
```

## 6. Database / Persistence

``` text
Implement persistent storage for CHIMERA in the existing backend.

Requirements:
- SQLAlchemy database layer
- Declarative Base
- Assessment session model
- Interview turn persistence
- Evidence persistence
- Memory persistence
- Mission persistence
- World-state persistence
- Repository implementations matching existing domain interfaces
- Session factory
- Alembic configuration
- Initial migration
- Persistence tests

IMPORTANT: Do NOT use one global SQLAlchemy ORM Session for the whole FastAPI application. Database Sessions must be request-scoped.

The application must safely handle concurrent HTTP requests. Do not store a live SQLAlchemy Session inside app.state as a shared mutable request resource.
```

## 7. SQLAlchemy Concurrency Bug Fix

``` text
Fix the CHIMERA backend's SQLAlchemy session concurrency error end-to-end.

Current error:
sqlalchemy.exc.InvalidRequestError: This session is provisioning a new connection; concurrent operations are not permitted

The current architecture creates a global SQLAlchemy Session during application startup and reuses it across HTTP requests. This is incorrect for FastAPI.

Change the implementation so that:
1. SQLAlchemy Engine is created once.
2. Session factory is created once.
3. A fresh SQLAlchemy Session is created per request.
4. The request-scoped Session is closed in finally.
5. Every SQL repository receives the request-scoped Session.
6. No ORM Session is stored as a global shared request resource.
7. app.state may store the Engine/session factory, but not a reusable live ORM Session.
8. Dependency injection provides the DB Session.
9. Test mode continues using in-memory repositories.
10. Existing domain interfaces are preserved.

Also remove the warning caused by unsafe Session.add() behavior.

Run all backend tests, manually test POST /api/interview, test sequential and practical concurrent requests, and verify persistence.
```

## 8. `dependencies.py` Full Replacement

``` text
Replace the current CHIMERA backend dependency wiring with proper request-scoped SQLAlchemy dependency injection.

Use:
from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.orm import Session

The DB dependency must retrieve the session factory from app.state, create a fresh Session for each request, yield it, and always close it in finally.

Repository dependencies must receive that Session and instantiate:
- SqlSessionRepository
- SqlTurnRepository
- SqlEvidenceRepository
- SqlMemoryRepository
- SqlMissionRepository
- SqlWorldStateRepository

Keep test/demo AI provider selection unchanged.
Keep InterviewService dependency injection intact.
Do not use a global ORM Session.
Return the complete edited dependencies.py file, not a patch.
```

## 9. `main.py` Full Replacement

``` text
Replace CHIMERA's app.main implementation so database resources have application lifetime while ORM Sessions have request lifetime.

Requirements:
- Create FastAPI app normally.
- Store settings on app.state.
- Configure CORS.
- In test environment use in-memory repositories.
- In non-test environments create the SQLAlchemy Engine once, create the SQLAlchemy Session factory once, and create the schema for local development.
- Store the engine on app.state.
- Store the session factory on app.state.
- DO NOT create a global SQLAlchemy Session.
- DO NOT instantiate SQL repositories with a shared Session during startup.
- Dependency injection must create repositories per request using a fresh DB Session.

Preserve health router, interview router, exception handlers, settings, and repository interfaces.
Return the complete edited main.py file so it can be copied directly into the project.
```

## 10. API 404 Debugging

``` text
The frontend is displaying:
[PROMPT] "Candidate Sarah Johnson, demonstrate how your MCP server architecture handles tool timeouts under load."
[USER_MSG] "hi"
[SYS_ERROR] Request failed: HTTP 404 - Not Found

The backend is running on http://127.0.0.1:8000.
The expected endpoint is POST /api/interview.

Debug this end-to-end.

Inspect frontend API URL, fetch/axios request code, FastAPI route declaration, router prefix, router inclusion in main.py, CORS configuration, environment variables, localhost vs 127.0.0.1, trailing paths, and HTTP method.

Do not redesign the application. Fix the smallest correct integration issue.

Verify GET /health works, POST /api/interview reaches the correct route, the frontend no longer reports 404, and the request/response schema matches the backend.
```

## 11. Frontend API Integration

``` text
Fix the CHIMERA production frontend/backend integration.

The frontend reaches the UI successfully but POST /api/interview can return 404.

Inspect the existing frontend and connect it to FastAPI without changing the established visual design.

Requirements:
- configurable backend API base URL
- local development support for http://127.0.0.1:8000
- no hard-coded production-only URL
- POST /api/interview
- request JSON matches backend DTO
- correct response parsing
- clear API errors
- preserve the futuristic interview-room UI

Verify the complete browser → frontend → FastAPI → service → repository/provider → response flow.
```

## 12. AI Provider

``` text
Implement CHIMERA's AI provider abstraction.

Requirements:
- AIProvider interface/protocol
- StubProvider for deterministic tests/demo
- OpenAIProvider
- credentials from environment configuration
- never hard-code API keys
- configurable model
- timeout
- retries
- provider failures converted to domain-level ProviderError
- application service independent of concrete vendor

The application must run in test/demo mode without an API key.
Add tests for stub behavior, missing key, successful provider response, failure, timeout, and retry behavior.
```

## 13. Candidate Analyzer

``` text
Implement CHIMERA's candidate analyzer as a dedicated module.

Create schemas.py, service.py, and __init__.py.

Transform candidate information and interview evidence into structured candidate information useful for adaptive planning.

Use strongly typed input/output models, no UI concerns, no direct FastAPI dependency, deterministic tests, evidence-based outputs, and no unsupported claims.
```

## 14. Curriculum Analyzer

``` text
Implement CHIMERA's curriculum analyzer.

Use the repository's curriculum resource to determine relevant technical concepts, competencies, and interview areas.

Create schemas.py, service.py, and __init__.py.

Requirements: structured schemas, deterministic behavior, role/seniority-aware analysis, no frontend logic, and tests for valid roles, missing data, and edge cases.
```

## 15. Interview Planner

``` text
Implement CHIMERA's adaptive interview planner.

The planner must NOT simply return questions from a fixed list.

Consider candidate profile, role, seniority, curriculum, previous turns, extracted evidence, evaluation state, current world state, and mission state.

Determine the next interview action. Possible actions include probing deeper, changing topic, increasing/decreasing difficulty, clarifying an answer, testing a weak/strong competency, introducing a mission, or concluding.

Use strongly typed schemas and deterministic tests.

Make the planner explainable: the resulting action must contain enough structured information to understand why it was selected.
```

## 16. Memory Engine

``` text
Implement CHIMERA's memory engine.

Maintain useful interview memory rather than treating every turn as isolated.

Store/retrieve structured information such as candidate strengths, weaknesses, evidence, topics tested, unresolved uncertainties, mission outcomes, and relevant interview state.

Persist memory through the repository abstraction.

Test creation, updates, retrieval, persistence, empty state, and repeated updates.
```

## 17. Mission Generator

``` text
Implement CHIMERA's mission generator.

A mission is a technical assessment task introduced dynamically based on the candidate's current state.

Consider role, seniority, curriculum, candidate evidence, weaknesses, current interview state, and previously completed missions.

Missions must be structured and deterministic in tests.
Avoid random meaningless tasks.
Add schema, service, and tests.
```

## 18. World-State Engine

``` text
Implement CHIMERA's world-state engine.

Maintain structured current interview state, including current phase, competency, difficulty, mission state, evidence state, evaluation state, candidate uncertainty where supported, and next-step constraints.

State transitions must be explicit and testable.
Do not hide complete interview state inside frontend state.
Persist important state through repositories.
```

## 19. Evaluation Engine

``` text
Implement CHIMERA's evaluation engine.

Evaluation must be evidence-based. Do not assign arbitrary scores without supporting evidence.

Evaluate technical correctness, depth, reasoning, communication, competency evidence, consistency, and mission performance where available.

Produce structured evaluation output for the feedback generator and final report.

Test strong, weak, incomplete, conflicting, and insufficient evidence cases.
```

## 20. Feedback Generator

``` text
Implement CHIMERA's feedback generator.

Generate structured candidate feedback from evaluation evidence.

Explain strengths, weaknesses, evidence, improvement areas, competency-level observations, and final recommendations.

Avoid generic AI filler. Every meaningful conclusion should be traceable to interview evidence.
Add deterministic tests.
```

## 21. API Contract / Adversarial Testing

``` text
Add comprehensive API contract and adversarial tests for CHIMERA.

Test valid requests, malformed JSON, missing fields, empty messages, oversized messages, invalid session IDs, repeated sessions, concurrent requests, provider failure, database failure, missing optional data, unexpected state, and invalid transitions.

The API must return controlled errors rather than uncaught internal exceptions.
Do not weaken validation merely to make tests pass.
Keep the public API contract documented.
```

## 22. End-to-End Interview Test

``` text
Create a complete CHIMERA interview end-to-end test.

Simulate:
1. Candidate/session initialization
2. Interview prompt
3. Candidate response
4. Evidence extraction
5. Candidate analysis
6. Evaluation
7. Memory update
8. Mission/world-state update
9. Next-step planning
10. Persistence
11. Subsequent request using the same session
12. Final result/report state

Verify that state from an earlier turn actually influences later behavior.
The test must work without a real OpenAI API key by using StubProvider.
```

## 23. Minimum Requirements

``` text
Create a minimum-requirements test suite that verifies CHIMERA cannot regress into a non-adaptive static chatbot.

Verify POST /api/interview, request validation, session state retention, evidence retention, evaluation, memory updates, planner invocation, state/evidence-driven next action, persistence, StubProvider operation without an external API, and environment-driven OpenAI configuration.
```

## 24. Migration Support

``` text
Add production-quality database migration support to CHIMERA.

Requirements:
- Alembic configuration
- env.py
- migration template
- initial schema migration
- migration documentation
- migration test

Document the difference between local development schema creation and production schema migration.
Do not rely on destructive database recreation.
```

## 25. Security Review

``` text
Perform a security review of the CHIMERA repository.

Inspect environment variables, API keys, .gitignore, .env.example, CORS, request validation, error exposure, database configuration, provider credentials, logging, frontend exposure of secrets, and dependencies.

Never print or commit real API credentials.
Identify security gaps honestly.
Fix appropriate hackathon-scope issues without destabilizing the application.
Document anything intentionally out of scope.
```

## 26. Environment Configuration

``` text
Create a safe CHIMERA .env.example.

Include configuration names only, never real secrets.
Include environment, demo mode, AI provider, OpenAI API key, model, timeout, retries, database URL, CORS origins, request ID header, and maximum message length.

Add comments explaining each setting and ensure the real .env remains ignored by Git.
```

## 27. Frontend Polish

``` text
Polish the existing CHIMERA frontend for a hackathon final demo.

Do NOT replace the current visual identity.
Preserve the established futuristic simulation-room aesthetic.

Improve hierarchy, spacing, typography, loading states, error states, responsiveness, accessibility, interaction feedback, interview status visibility, evaluation visibility, candidate context, and mission state.

The frontend should feel like a professional AI assessment system rather than a generic chatbot.
Do not add visual effects that reduce performance or readability.
```

## 28. Frontend Stability

``` text
Audit the CHIMERA frontend for final-demo stability.

Check routes, dynamic candidate/session pages, report page, API requests, loading states, error states, null/undefined handling, TypeScript errors, ESLint, package scripts, production build, and browser console errors.

Do not redesign working components.
Fix actual bugs and verify the production build succeeds.
```

## 29. README

``` text
Create a professional GitHub README for CHIMERA — Adaptive AI Interviewer.

Explain what CHIMERA is, the problem, why traditional interviewers are limited, how CHIMERA differs, architecture, adaptive interview loop, major modules, frontend, backend, AI provider abstraction, persistence, API, project structure, setup, environment variables, database/migrations, testing, demo flow, deployment, limitations, and future improvements.

Keep technical claims accurate to the implementation. Do not claim features that are not actually implemented.
```

## 30. Demo Script

``` text
Create a short hackathon demo script for CHIMERA.

Show candidate selection, interview initialization, AI-generated/interview prompt, candidate response, evidence extraction, evaluation, adaptive next action, mission or difficulty change, persistent state, and final assessment/report.

The most important moment should demonstrate that the next step changes because of candidate evidence.
Avoid spending the demo on setup or code.
```

## 31. Final Repository Audit

``` text
Perform a final end-to-end audit of the CHIMERA repository.

Frontend: build, routes, API integration, console/runtime errors, polished UI, loading/error states.

Backend: startup, health endpoint, POST /api/interview, dependency injection, request-scoped DB sessions, no global ORM Session, AI abstraction, StubProvider, OpenAI configuration, persistence, migrations, controlled errors.

Tests: unit, integration, API contract, persistence, migration, end-to-end, adversarial.

Repository: .gitignore, no secrets, .env.example, README, demo script, migration docs, package configuration.

Do not merely report problems. For every problem: explain root cause, fix it, test it, and verify the result.
Do not introduce unrelated redesigns.
```

## 32. Git Merge / Conflict Resolution

``` text
Safely integrate the CHIMERA backend work with the existing production frontend.

Before merging inspect both branches, identify overlapping files and frontend differences, preserve the production frontend and CHIMERA backend, and do not blindly accept one side of every conflict.

If branches contain fundamentally different frontend structures, stop and analyze before destructive resolution.
Create a backup branch before risky merge operations.
Do not delete working functionality just to make Git report a clean merge.

After the merge verify frontend/src remains complete, backend modules remain complete, and tests/builds pass.
```

## 33. Git Verification

``` text
Before pushing CHIMERA, verify the Git repository end-to-end.

Run:
git status
git status --short
git diff --check
git diff --cached --name-status
git log --oneline --decorate -5
git ls-tree -r --name-only HEAD

Verify expected frontend/backend/tests/docs are tracked, no .env secrets are tracked, no accidental files are committed, and the working tree is clean after commit.
```

## 34. Commit / Push

``` text
After all CHIMERA changes are tested and verified:
1. Stage intended files.
2. Inspect staged diff.
3. Run git diff --check --cached.
4. Commit with a meaningful message.
5. Verify git status.
6. Verify commit log.
7. Push main to origin.
8. Verify origin/main points to the new commit.
9. Confirm the working tree is clean.

Do not force push unless explicitly required.
```

## 35. Final Deployment

``` text
Prepare CHIMERA for final deployment.

Frontend:
- production build succeeds
- production API URL is configurable
- no local-only endpoint remains hard-coded
- no secrets in client-side code

Backend:
- production environment configuration
- production database URL
- migrations ready
- OpenAI provider configuration
- request-scoped database sessions
- CORS restricted to deployed frontend origin
- controlled error handling

Repository:
- README
- .env.example
- migration documentation
- demo script
- tests
- clean Git history
- no secrets

Perform a final smoke test of:
Frontend → API → InterviewService → AI provider → repositories → database → response.

Only call the application deployment-ready after the complete flow works.
```

## 36. Final Judge-Readiness

``` text
Act as a ruthless hackathon judge and senior AI systems architect.

Evaluate CHIMERA as if it were being submitted today.

Score originality, real-world relevance, AI depth, adaptive behavior, architecture quality, prompt engineering, technical feasibility, UX, reliability, deployment readiness, demo impact, and documentation.

For every weak area identify the exact weakness, explain why a judge would care, and recommend the smallest high-impact fix.

Prioritize improvements that increase judge score while preserving stability.
The goal is not maximum code. The goal is a technically credible, memorable, polished, working AI system.
```

## 37. Final Code-Repair Prompt

``` text
You are the final senior engineer responsible for shipping CHIMERA.

Do not rebuild the project.

Inspect the entire existing repository and make the application production-ready.

Find broken imports, broken routes, incorrect dependency injection, database lifecycle problems, API contract mismatches, frontend/backend integration problems, TypeScript/ESLint/build errors, test failures, migration issues, configuration issues, security mistakes, and missing documentation.

For every issue:
1. reproduce it
2. identify root cause
3. implement the smallest correct fix
4. add/update a regression test
5. rerun affected tests
6. verify the complete application flow

Do not replace functioning architecture with a simpler but less capable implementation.
Do not remove CHIMERA's adaptive behavior.
Do not introduce fake/mock behavior into production paths merely to hide failures.
Demo mode may use StubProvider, but production AI configuration must remain real and environment-driven.

Finish only when backend starts, frontend builds, health works, interview endpoint works, persistence works, adaptive flow works, tests pass, repository is clean, and deployment configuration is documented.
```

## 38. Prompt Log Submission Prompt

``` text
Create a prompt.md file for the CHIMERA hackathon submission.

Document the AI-assisted development process chronologically.

Include prompts for product definition, architecture, backend, AI provider, database, adaptive planning, candidate analysis, memory, missions, world state, evaluation, feedback, API, frontend, testing, debugging, security, documentation, Git, deployment, and final audit.

Do not fabricate implementation results.
Clearly separate planning prompts from debugging/fix prompts.
The prompt log should demonstrate iterative prompt engineering rather than a single giant prompt.
```

## 39. Engineering Philosophy Prompt

``` text
Think before you code.
Inspect before you modify.
Preserve working functionality.
Prefer small, testable changes.
Use AI as an engineering collaborator, not as a replacement for verification.

Every major feature should have a plan, implementation, test, and verification step.
Every bug should produce a diagnosis, targeted fix, and regression test.
Every deployment change should be verified end-to-end.

Stability first.
Quality over feature count.
Adaptive behavior over chatbot theatrics.
Evidence over unsupported claims.
```

## 40. Final Submission Checklist

``` text
CHIMERA FINAL CHECKLIST

[ ] Product concept clearly explained
[ ] Adaptive behavior demonstrable
[ ] Candidate evidence affects future interview behavior
[ ] Backend architecture modular
[ ] AI provider abstracted
[ ] StubProvider works for demo/tests
[ ] OpenAI provider environment-driven
[ ] Database persistence works
[ ] SQLAlchemy Session is request-scoped
[ ] No global ORM Session
[ ] Alembic migration exists
[ ] API contract documented
[ ] POST /api/interview works
[ ] Frontend calls correct backend URL
[ ] Frontend production build succeeds
[ ] Loading states work
[ ] Error states work
[ ] End-to-end interview flow works
[ ] Persistence tests pass
[ ] API tests pass
[ ] Adversarial tests pass
[ ] Migration tests pass
[ ] No real API keys committed
[ ] .env ignored
[ ] .env.example exists
[ ] README complete
[ ] Demo script complete
[ ] Prompt log complete
[ ] Git working tree clean
[ ] origin/main contains final commit
[ ] Production deployment configuration documented
[ ] Final demo rehearsed
```

------------------------------------------------------------------------

## End of Prompt Log

**Project:** CHIMERA --- Adaptive AI Interviewer\
**Repository:** `The-Orchestrators`\
**Development approach:** Iterative AI-assisted engineering, testing,
debugging, and verification.
