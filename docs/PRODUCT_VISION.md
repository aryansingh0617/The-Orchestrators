# Product Vision

## Executive Summary

Project Chimera is an AI Engineering Assessment Operating System. It evaluates engineering judgment through adaptive technical missions, not static interview questions. The product behaves like a realistic engineering environment where each candidate decision changes the future interview path, evidence collection, difficulty, and final hiring recommendation.

The system is designed for hackathon judges, hiring teams, and candidates who need to see more than answer correctness. Chimera assesses reasoning, debugging, systems thinking, production engineering, tradeoff analysis, and communication under changing constraints.

## Problem

Traditional technical interviews often reward memorized patterns, isolated trivia, and confidence under artificial conditions. They usually fail to capture how engineers:

- clarify ambiguous requirements
- debug partial systems
- reason about architecture under constraints
- communicate tradeoffs
- recover from wrong assumptions
- make production-minded decisions

AI interview chatbots often reproduce the same limitation with a friendlier interface. They ask questions, score answers, and summarize performance. That is not enough for AI engineering roles where the work involves systems, data, prompts, evaluations, deployment risk, and model behavior.

## Product Thesis

The best assessment is a simulated engineering mission with evolving state.

Instead of asking "What is retrieval augmented generation?", Chimera can place the candidate inside a failing AI support system and ask them to diagnose retrieval quality, latency, hallucination risk, and observability gaps. If they focus only on prompts, the world state changes differently than if they identify data quality or deployment issues. The interview becomes adaptive, evidence-based, and closer to real engineering work.

## Target Users

## Hiring Teams

Hiring teams use Chimera to evaluate AI engineering candidates consistently while preserving rich qualitative signal.

Needs:

- defensible scoring
- clear evidence trails
- role-specific difficulty
- actionable hiring recommendations
- minimized interviewer bias

## Candidates

Candidates use Chimera as an assessment environment that rewards thoughtful engineering behavior.

Needs:

- clear mission context
- fair adaptation
- opportunity to explain tradeoffs
- feedback that helps them grow

## Hackathon Judges

Judges use Chimera to evaluate product ambition, technical architecture, AI integration quality, and demo clarity.

Needs:

- memorable live flow
- visible AI adaptation
- credible system design
- production-aware implementation plan

## Core Experience

1. A user creates an assessment session for a target role, seniority, and curriculum.
2. The Curriculum Analyzer converts role material into competency targets.
3. The Interview Planner creates an adaptive mission arc.
4. The Mission Generator presents realistic AI engineering scenarios.
5. The candidate responds with investigation steps, design choices, debugging hypotheses, or implementation plans.
6. The World State Engine updates the simulated environment based on the response.
7. The Memory Engine tracks claims, assumptions, strengths, gaps, and recurring behaviors.
8. The Evaluation Engine maps evidence to competencies.
9. The Feedback and Profile Generators produce a hiring profile, recommendation, and candidate feedback.

## Differentiators

- Adaptive world state: candidate actions change future mission conditions.
- Evidence-first evaluation: scores must cite collected evidence.
- Engineering mission format: scenarios simulate debugging, architecture, production incidents, and tradeoff discussions.
- Modular AI architecture: models are provider-agnostic and swappable.
- Clean separation of concerns: analyzers, planners, engines, and generators are independent modules.
- Demo-ready narrative: the product tells a coherent story in a live hackathon setting.

## Assessment Dimensions

| Dimension | What Chimera Evaluates | Example Evidence |
| --- | --- | --- |
| Reasoning | Structured problem decomposition and inference quality | Candidate isolates root cause before proposing fixes |
| Debugging | Hypothesis formation, instrumentation, and iteration | Candidate asks for logs, traces, or reproduction steps |
| Systems Thinking | Understanding of dependencies and failure propagation | Candidate identifies data/model/API boundaries |
| Production Engineering | Reliability, security, monitoring, and deployment judgment | Candidate proposes rollback, alerts, and test coverage |
| Tradeoff Analysis | Ability to compare options under constraints | Candidate weighs latency, quality, cost, and risk |
| Communication | Clarity, humility, and stakeholder framing | Candidate explains uncertainty and next steps |

## Non-Goals

- Chimera is not a generic chatbot.
- Chimera is not a trivia quiz engine.
- Chimera is not a replacement for all human hiring judgment.
- Chimera does not claim perfect candidate ranking.
- Chimera does not make irreversible employment decisions without human review.

## Product Principles

- Evidence before score.
- Missions before questions.
- Adaptation before scripted flow.
- Transparent reasoning before black-box judgment.
- Production realism before toy examples.
- Human hiring ownership before automation.

## Human Review Positioning

Chimera produces assessment evidence and decision support. It does not make final employment decisions. The final hiring recommendation must always include confidence, caveats, and a human review flag. This is both an ethical product constraint and a practical quality control: adaptive AI assessments are useful because they reveal signal, not because they remove human accountability.

## MVP Scope

The MVP should support:

- creating an assessment session
- configuring role, seniority, and curriculum inputs
- generating a mission plan
- running adaptive mission turns
- collecting evidence
- updating world state and memory
- producing competency scores
- generating feedback and hiring recommendation
- displaying an operator dashboard

## Success Metrics

- A judge can understand the product in under one minute.
- A demo can show adaptation after one candidate response.
- Every score in the final report cites evidence.
- Every hiring recommendation includes caveats and human review language.
- Modules can be tested independently.
- The system can run without a specific AI provider through a stub implementation.
- The architecture supports future providers, scenarios, and scoring rubrics without rewrites.
