# Demo Script

## Demo Goal

Show that Chimera is not an interview chatbot. It is an adaptive AI engineering assessment operating system where candidate responses change the mission, world state, evidence, and final recommendation.

## Demo Duration

Target: 5 to 7 minutes.

## Setup

Persona:

- Candidate: Senior AI Engineer
- Role focus: RAG systems, evaluation, observability, production deployment
- Assessment mode: demo
- Time budget: 30 minutes

Demo seed curriculum:

```text
Evaluate senior AI engineers on RAG debugging, LLM evaluation, production observability, latency/cost tradeoffs, prompt and retrieval design, and communication during incidents.
```

Hackathon API:

```text
POST /api/interview
```

## Story Arc

## 1. Open With the Product Thesis

Narration:

"This is Project Chimera. It does not ask static interview questions. It runs adaptive engineering missions and collects evidence from how a candidate reasons through changing technical conditions."

Show:

- session setup screen
- role and curriculum fields
- assessment mode

## 2. Generate the Mission Plan

Action:

- send the first `POST /api/interview` request with `sessionId` and a candidate object
- initialize the session, analyze the candidate, and generate the first mission internally

Show:

- competency targets
- planned mission arc
- difficulty curve

Narration:

"The system turns the role curriculum into assessment objectives, then plans missions that cover debugging, systems thinking, production tradeoffs, and communication."

## 3. Start Mission One

Mission:

"A customer support assistant began producing plausible but unsupported answers after yesterday's retrieval index refresh. Customer escalations are rising."

Prompt:

"Walk through your investigation and what you would check first."

Show:

- candidate prompt
- world state summary

## 4. Submit Weak Candidate Response

Candidate response:

```text
I would improve the system prompt to tell the model to be more accurate and refuse uncertain answers.
```

Expected adaptation:

- Evidence Collector records narrow prompt-only reasoning.
- World State Engine reveals retrieval logs showing chunk quality changed.
- Difficulty stays stable or decreases slightly.
- Next prompt probes debugging depth.

Narration:

"A chatbot would just score this answer. Chimera changes the simulated world and asks a better follow-up."

## 5. Submit Stronger Candidate Response

Candidate response:

```text
Before changing prompts, I would compare retrieved chunks before and after the index refresh, inspect failed eval examples, verify citation-source alignment, and check whether chunking or embedding configuration changed. For mitigation, I would roll back the index or gate the new retriever while tracking groundedness and escalation rate.
```

Expected adaptation:

- Evidence Collector records positive debugging, systems, and production evidence.
- Memory Engine notes structured investigation.
- Difficulty increases.
- Next prompt introduces latency/cost tradeoff.

Narration:

"The same session adapts when the candidate demonstrates stronger engineering behavior."

## 6. Show Evidence Trail

Show:

- evidence items by competency
- source turn references
- confidence
- positive and negative observations

Narration:

"Every score is built from evidence. The system can explain what it observed and where it came from."

## 7. Complete Assessment

Action:

- complete session
- generate reports

Show:

- engineering profile
- hiring recommendation
- candidate feedback

Expected report:

- strengths in debugging and systems thinking
- caveat around initial over-focus on prompt changes
- lean hire or proceed recommendation with confidence
- human review required

Narration:

"The recommendation is not an automated hiring decision. It is an evidence-backed assessment artifact for human review."

## Judge Talking Points

- Modular clean architecture
- Provider abstraction and deterministic demo mode
- Evidence-first scoring
- Adaptive world state
- Independent engines
- Production-minded audit trail

## Backup Demo Path

If live AI provider is unavailable:

- use stub provider
- run deterministic seeded scenario
- show the same adaptation flow

If frontend is unavailable:

- use API docs or scripted HTTP flow
- show JSON evidence and report outputs

If final report generation fails:

- show collected evidence and explain recommendation engine fallback

## Closing Line

"Chimera evaluates how engineers think inside changing systems. That is the difference between asking interview questions and running an assessment operating system."
