# Prompt Architecture

## Goals

Prompting in Chimera must be structured, testable, and provider-agnostic. Prompts are not scattered across services. They are versioned templates with declared inputs, output schemas, failure modes, and fallback behavior.

## Principles

- Prompts produce structured outputs whenever possible.
- Every prompt has a named purpose.
- Every prompt declares required inputs.
- Every prompt output is validated with Pydantic.
- Failed validation triggers retry or deterministic fallback.
- Hidden evaluator prompts never appear in candidate-facing responses.
- Prompts must request evidence, uncertainty, and rationale, not just scores.

## Prompt Registry

Prompt templates are addressed by stable IDs:

- `curriculum.analyze.v1`
- `candidate.baseline.v1`
- `planner.create_plan.v1`
- `mission.generate.v1`
- `world.transition.v1`
- `memory.update.v1`
- `difficulty.adjust.v1`
- `evidence.extract.v1`
- `evaluation.score.v1`
- `profile.generate.v1`
- `recommendation.generate.v1`
- `feedback.generate.v1`

Each prompt record includes:

- ID
- version
- owner module
- purpose
- input schema
- output schema
- model options
- failure modes
- fallback strategy
- test fixtures

## Prompt Contract Template

```text
Prompt ID:
Purpose:
Inputs:
Output Schema:
Evaluation Criteria:
Failure Modes:
Fallback Strategy:
Safety Notes:
```

## Prompt Contracts

## curriculum.analyze.v1

Purpose: Convert curriculum text into role competencies and assessment objectives.

Inputs:

- role title
- seniority
- curriculum text
- assessment mode

Outputs:

- competencies
- priority levels
- expected seniority bar
- mission family recommendations
- out-of-scope topics

Failure modes:

- curriculum too vague
- model invents unsupported requirements
- seniority bar mismatch

Fallback strategy:

- use default AI engineering competency map
- mark curriculum confidence as low

## candidate.baseline.v1

Purpose: Summarize candidate background without making forbidden inferences.

Inputs:

- candidate profile summary
- role target
- seniority

Outputs:

- baseline strengths
- areas to probe
- starting difficulty
- confidence

Failure modes:

- infers protected attributes
- overstates experience
- treats missing information as negative evidence

Fallback strategy:

- anonymous baseline
- default starting difficulty from role seniority

## planner.create_plan.v1

Purpose: Build a mission arc that covers target competencies.

Inputs:

- competency map
- candidate baseline
- time budget
- assessment mode

Outputs:

- mission sequence
- coverage map
- difficulty curve
- adaptation rules

Failure modes:

- misses required competencies
- creates too many missions
- repeats same mission pattern

Fallback strategy:

- deterministic plan templates by role and time budget

## mission.generate.v1

Purpose: Generate candidate-facing mission prompt and hidden evaluator notes.

Inputs:

- current mission plan item
- world state
- memory summary
- difficulty target

Outputs:

- candidate prompt
- hidden evaluator notes
- expected evidence hooks
- allowed world updates

Failure modes:

- asks trivia instead of mission
- reveals hidden scoring
- produces unrealistic constraints

Fallback strategy:

- use curated mission template
- remove hidden content from candidate response

## world.transition.v1

Purpose: Update simulated environment based on candidate action.

Inputs:

- previous world state
- candidate response analysis
- mission constraints
- allowed transition rules

Outputs:

- new state JSON
- visible state update
- hidden transition rationale
- risk flags

Failure modes:

- impossible state transition
- punishes correct answer unfairly
- leaks hidden evaluator notes

Fallback strategy:

- preserve previous state
- emit neutral clarification prompt

## memory.update.v1

Purpose: Update durable candidate behavior memory.

Inputs:

- existing memory
- evidence items
- candidate response
- mission context

Outputs:

- new memory records
- updated memory records
- memory summary

Failure modes:

- duplicates records
- overgeneralizes from one weak signal
- records unsupported personality claims

Fallback strategy:

- only record high-confidence evidence-linked observations

## difficulty.adjust.v1

Purpose: Decide the next difficulty level.

Inputs:

- current difficulty
- latest evidence
- confidence
- coverage gaps
- role target

Outputs:

- next difficulty
- adaptation rationale
- guardrails applied

Failure modes:

- jumps difficulty too aggressively
- reduces difficulty based on one ambiguous response
- ignores coverage needs

Fallback strategy:

- keep current difficulty unless evidence is strong

## evidence.extract.v1

Purpose: Extract atomic evidence from a candidate turn.

Inputs:

- candidate response
- mission prompt
- rubric
- world state

Outputs:

- evidence items
- confidence
- rationale

Failure modes:

- treats eloquence as correctness
- scores unsupported claims
- misses negative evidence

Fallback strategy:

- require evaluator-visible low-confidence flag
- produce no evidence when unsupported

## evaluation.score.v1

Purpose: Convert evidence into competency-level evaluations.

Inputs:

- evidence items
- rubric
- role bar
- prior evaluations

Outputs:

- score
- confidence
- rationale
- evidence IDs
- insufficient evidence flag

Failure modes:

- score without evidence
- inconsistent scoring across competencies
- excessive confidence

Fallback strategy:

- return insufficient evidence
- require additional mission coverage

## profile.generate.v1

Purpose: Generate engineering profile summary.

Inputs:

- evaluations
- memory records
- evidence summary

Outputs:

- strengths
- risk areas
- engineering style
- role fit summary

Failure modes:

- unsupported personality claims
- hidden note leakage
- overconfident narrative

Fallback strategy:

- evidence-only bullet summary

## recommendation.generate.v1

Purpose: Produce hiring recommendation.

Inputs:

- evaluations
- role bar
- coverage requirements
- confidence thresholds

Outputs:

- recommendation
- confidence
- rationale
- caveats
- human review flag

Failure modes:

- recommendation without coverage
- ignores caveats
- implies fully automated decision
- treats score as more certain than evidence supports

Fallback strategy:

- insufficient evidence recommendation
- human review required

## feedback.generate.v1

Purpose: Produce candidate-facing feedback.

Inputs:

- evaluations
- evidence summaries
- role target

Outputs:

- strengths
- improvement areas
- practice suggestions

Failure modes:

- exposes internal scoring prompts
- uses harsh or unsupported language
- reveals hidden world state

Fallback strategy:

- templated evidence-based feedback

## Prompt Testing

Each prompt must have:

- golden fixture input
- expected output schema
- invalid output test
- fallback test
- hidden content leakage test when relevant

## Prompt Versioning

Prompt changes that alter behavior require:

- version increment
- changelog entry in code or prompt registry
- regression test updates
- sample output review

## Safety Review Checklist

Before enabling a prompt in an assessment flow:

- Does the output schema require evidence or rationale?
- Can the prompt leak hidden evaluator notes?
- Does it avoid protected attribute inference?
- Does it distinguish uncertainty from negative evidence?
- Is there a deterministic fallback?
- Does the candidate-facing output remain respectful and useful?
