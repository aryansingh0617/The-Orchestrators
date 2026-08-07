# System Design

## System Overview

Chimera is organized around an assessment session. A session contains configuration, candidate profile, mission plan, turns, world state snapshots, memory records, evidence, evaluations, and final reports.

The backend is the source of truth. The frontend renders state and sends candidate/operator commands.

## Core Domain Objects

## Assessment Session

Represents one candidate assessment.

Fields:

- session ID
- candidate ID
- role target
- seniority target
- curriculum source
- status
- created and updated timestamps

States:

- draft
- planned
- active
- completed
- cancelled
- failed

## Mission

A realistic engineering scenario used to evaluate competencies.

Fields:

- mission ID
- session ID
- title
- scenario summary
- competency targets
- difficulty
- constraints
- expected evidence types
- current status

## Turn

One candidate interaction.

Fields:

- turn ID
- sequence number
- prompt shown to candidate
- candidate response
- module outputs
- world state before and after
- created timestamp

## World State

The simulated engineering environment.

Examples:

- service health
- latency
- incident timeline
- model behavior
- data quality indicators
- stakeholder constraints
- budget or deployment pressure

World state updates must be explainable and linked to candidate actions.

## Memory Record

Persistent assessment memory.

Examples:

- candidate used structured debugging
- candidate ignored security concern twice
- candidate communicates uncertainty clearly
- candidate over-indexes on prompt changes

Memory records inform future mission turns and final evaluation.

## Evidence

Atomic observed signal used for scoring.

Fields:

- evidence ID
- source turn ID
- competency
- observation
- polarity
- strength
- confidence
- evaluator rationale

Scores cannot exist without evidence.

## Evaluation

Competency-level score with evidence references.

Fields:

- evaluation ID
- session ID
- competency
- score
- confidence
- evidence IDs
- rationale
- improvement guidance

## Rubric Scale

Scores use a 1-5 competency scale:

| Score | Meaning | Evidence Standard |
| --- | --- | --- |
| 1 | Significant concern | Repeated negative evidence or inability to engage competency |
| 2 | Below bar | Some relevant attempts, but major gaps or unsafe reasoning |
| 3 | Meets baseline | Adequate evidence for role expectations with manageable gaps |
| 4 | Strong | Consistent positive evidence with production-aware reasoning |
| 5 | Exceptional | Deep, transferable judgment across ambiguous constraints |

Confidence is separate from score. A high score with low confidence is not acceptable for final recommendation. The Hiring Recommendation Engine must consider both score and coverage.

## Module Contracts

## Curriculum Analyzer

Purpose: Convert role and curriculum input into target competencies and mission constraints.

Inputs:

- role title
- seniority
- curriculum text or structured skills
- company/context hints

Outputs:

- competency map
- assessment objectives
- disallowed or out-of-scope areas
- recommended mission families

Error handling:

- reject empty curriculum
- flag ambiguous seniority
- fallback to standard AI engineering competency map

Unit tests:

- parses known curriculum into competencies
- handles sparse input
- preserves out-of-scope constraints

## Candidate Analyzer

Purpose: Normalize candidate background and calibrate starting difficulty.

Inputs:

- resume/profile summary
- target role
- optional self-reported strengths

Outputs:

- candidate baseline
- risk areas to probe
- initial difficulty recommendation

Error handling:

- support anonymous candidate mode
- avoid inferring protected attributes

Unit tests:

- produces baseline from minimal profile
- avoids forbidden demographic inference

## Interview Planner

Purpose: Create a mission arc that covers required competencies while allowing adaptation.

Inputs:

- competency map
- candidate baseline
- time budget
- assessment mode

Outputs:

- mission plan
- coverage map
- difficulty progression
- stopping criteria

Error handling:

- reject impossible time budgets
- fallback to compact mission plan

Unit tests:

- covers required competencies
- balances mission diversity
- respects time budget

## Mission Generator

Purpose: Generate the next mission prompt from plan, memory, and world state.

Inputs:

- mission plan
- current world state
- memory summary
- difficulty target

Outputs:

- candidate-facing mission prompt
- hidden evaluator notes
- expected evidence hooks

Error handling:

- retry invalid structured generation
- fallback to template mission

Unit tests:

- output follows schema
- prompt maps to competencies

## World State Engine

Purpose: Update the simulated engineering environment after each response.

Inputs:

- previous world state
- candidate response analysis
- mission constraints

Outputs:

- new world state
- state transition rationale
- visible updates for candidate

Error handling:

- reject invalid state transitions
- preserve previous state on failure

Unit tests:

- state transitions are deterministic under stub mode
- invalid transition is rejected

## Memory Engine

Purpose: Track durable behavioral signals across turns.

Inputs:

- existing memory
- candidate response
- evidence
- evaluation deltas

Outputs:

- updated memory records
- memory summary for planning

Error handling:

- deduplicate repeated observations
- decay weak stale signals

Unit tests:

- accumulates repeated behavior
- preserves evidence links

## Adaptive Difficulty Engine

Purpose: Adjust challenge level based on performance, uncertainty, and coverage.

Inputs:

- current difficulty
- evidence summary
- confidence
- remaining competencies

Outputs:

- next difficulty
- adaptation reason
- safeguards

Error handling:

- avoid drastic jumps without strong evidence
- cap difficulty by role target

Unit tests:

- increases difficulty after strong evidence
- decreases or stabilizes after confusion

## Evidence Collector

Purpose: Extract structured evidence from candidate responses and module observations.

Inputs:

- candidate response
- mission context
- evaluator rubric

Outputs:

- evidence items
- confidence scores
- extraction rationale

Error handling:

- mark low-confidence evidence
- require human-readable observation

Unit tests:

- extracts competency evidence
- rejects unsupported claims

## Evaluation Engine

Purpose: Convert evidence into competency evaluations.

Inputs:

- evidence items
- rubric
- session context

Outputs:

- competency scores
- score rationales
- confidence levels

Error handling:

- no score without evidence
- flag insufficient evidence

Unit tests:

- score cites evidence IDs
- insufficient evidence remains unresolved

## Engineering Profile Generator

Purpose: Summarize candidate engineering style and capability profile.

Inputs:

- evaluations
- memory records
- mission outcomes

Outputs:

- strengths
- growth areas
- role fit narrative

Error handling:

- avoid unsupported personality claims
- cite evidence groups

Unit tests:

- uses only supported claims
- separates observation from recommendation

## Hiring Recommendation Engine

Purpose: Produce a hiring recommendation with confidence and caveats.

Inputs:

- competency evaluations
- role bar
- confidence thresholds

Outputs:

- recommendation
- confidence
- rationale
- caveats

Error handling:

- return "insufficient evidence" when required competencies are missing
- require human review warning

Unit tests:

- rejects recommendation without required coverage
- handles mixed evidence

## Feedback Generator

Purpose: Generate candidate-facing feedback that is useful and fair.

Inputs:

- evaluations
- evidence summaries
- candidate level

Outputs:

- strengths
- improvement areas
- practice recommendations

Error handling:

- avoid exposing hidden evaluator prompts
- remove sensitive internal labels

Unit tests:

- feedback maps to evidence
- no hidden notes leak

## Key Design Invariants

- Every turn has exactly one before and after world state snapshot.
- Every evaluation score references at least one evidence item.
- Candidate-facing feedback never includes hidden evaluator notes.
- AI provider failures can fall back to deterministic templates where possible.
- A completed session is immutable except for administrative annotations.

## Fairness and Consistency Controls

- Adaptation rationale is stored for every difficulty change.
- Required competencies must meet minimum evidence coverage before final recommendation.
- Candidate Analyzer cannot infer protected attributes or penalize missing optional profile data.
- The same role and seniority share a stable role bar even when missions adapt.
- Final reports distinguish observation, interpretation, and recommendation.
- Human review is required when confidence or coverage is below threshold.
