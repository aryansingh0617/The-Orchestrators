# Risks

## Risk Register

| Risk | Severity | Likelihood | Mitigation |
| --- | --- | --- | --- |
| Product becomes a chatbot instead of operating system | High | Medium | Mission-first UX, world state engine, evidence trail |
| Modules become tightly coupled | High | Medium | Application orchestration and typed contracts |
| AI outputs are inconsistent | High | High | Structured schemas, validation, retry, stub fallback |
| Scores are not defensible | High | Medium | Evidence-first evaluation and evidence ID requirements |
| Hidden evaluator notes leak to candidate | High | Low | Separate DTOs, leakage tests |
| Scope is too large for hackathon | High | Medium | Modular MVP and deterministic demo path |
| Provider credentials unavailable | Medium | Medium | Stub provider and template fallback |
| Frontend duplicates backend logic | Medium | Medium | API-owned scoring and frontend render-only rule |
| Database design blocks auditability | High | Low | Immutable turns, snapshots, evidence tables |
| Demo depends on flaky model behavior | High | Medium | Deterministic demo mode |
| Recommendation is mistaken for automated decision | High | Medium | Human review flag, caveats, and evidence references |

## Architecture Weakness Review

## Reviewer Lens: OpenAI Staff Engineer

Weakness found:

- The system could over-rely on model judgment without enough deterministic validation.

Refinement:

- Prompt outputs must be schema-validated.
- Evaluation scores must cite evidence IDs.
- Stub provider must support deterministic tests.
- Provider failures must have explicit fallback behavior.

## Reviewer Lens: Anthropic Principal Engineer

Weakness found:

- Adaptive interviews can become unfair if the model changes difficulty too aggressively or infers unsupported traits.

Refinement:

- Adaptive Difficulty Engine must cap jumps and provide rationale.
- Candidate Analyzer must avoid protected or unsupported inferences.
- Hiring Recommendation Engine must return "insufficient evidence" when coverage is weak.
- Feedback must be evidence-based and candidate-safe.
- Reports must preserve human hiring ownership.

## Reviewer Lens: Google DeepMind Technical Lead

Weakness found:

- The initial design could lack experimental rigor and reproducibility.

Refinement:

- Every turn stores before/after world state snapshots.
- Provider events are logged with latency and fallback status.
- Prompt versions are stable.
- Demo mode uses deterministic fixtures.

## Remaining Risks

## Assessment Fairness

Risk:

- The system may adapt differently for candidates in ways that are hard to compare.

Mitigation:

- Store mission plan, adaptation rationale, evidence, and difficulty changes.
- Report confidence and coverage.
- Use role bars and coverage requirements.

## Hallucinated Evaluation

Risk:

- AI evaluator may invent observations not present in candidate response.

Mitigation:

- Evidence Collector must quote or summarize source turn context.
- Evaluation Engine requires evidence IDs.
- Low-confidence evidence is flagged instead of scored strongly.

## Hackathon Time Pressure

Risk:

- Building all modules fully may exceed time.

Mitigation:

- Implement thin but real module contracts.
- Use deterministic templates where full AI behavior is not essential.
- Prioritize end-to-end demo path over exhaustive scenario library.

## Production Claims

Risk:

- The product may appear production-ready before privacy, auth, and retention are complete.

Mitigation:

- Documentation distinguishes MVP from production hardening.
- Final demo should state current security posture honestly.

## No Major Architectural Weaknesses Remaining

After review, the remaining risks are implementation and scope risks rather than unresolved architectural contradictions. The architecture has explicit boundaries, evidence traceability, provider abstraction, deterministic fallback, state auditability, fairness controls, human-review positioning, and safety constraints.
