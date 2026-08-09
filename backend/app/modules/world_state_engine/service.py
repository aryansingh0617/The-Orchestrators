from __future__ import annotations

import re
from typing import Any

from app.modules.world_state_engine.rag_mitigation import RAGIncidentMitigator
from app.modules.world_state_engine.schemas import WorldStateSnapshot


class WorldStateEngine:
    """Apply candidate decisions to a dynamic interview world state."""

    def initialize(
        self,
        *,
        mission_title: str,
        difficulty: str,
        constraints: list[str] | None = None,
    ) -> WorldStateSnapshot:
        return WorldStateSnapshot(
            current_mission=mission_title,
            constraints=constraints or [],
            system_state={
                "latency_ms": 320,
                "memory_usage_pct": 55,
                "cache_hit_pct": 62,
                "recall_score": 0.71,
                "error_rate_pct": 2.4,
            },
            candidate_decisions=[],
            unresolved_problems=["Root cause not yet confirmed"],
            evidence=[],
            difficulty=difficulty,
            progress={"questions": 0, "curriculum_days": 0},
            visible_summary=(
                "Production dashboard: latency 320ms, cache hit 62%, recall 0.71, error rate 2.4%."
            ),
            version=1,
        )

    def transition(
        self,
        current: WorldStateSnapshot,
        *,
        candidate_answer: str,
        evaluation_outcome: str,
        mission_title: str | None = None,
        difficulty: str | None = None,
        evidence: list[str] | None = None,
        progress: dict[str, Any] | None = None,
    ) -> WorldStateSnapshot:
        state = dict(current.system_state)
        decisions = list(current.candidate_decisions)
        unresolved = list(current.unresolved_problems)
        answer_l = candidate_answer.lower()
        applied: list[str] = []

        if re.search(r"\bretry|backoff|exponential|fallback|downstream|circuit\b", answer_l):
            mitigations = RAGIncidentMitigator.apply_error_rate_mitigation(state)
            applied.extend(mitigations)
        elif re.search(r"\bcanary|rollback|feature flag\b", answer_l):
            state["error_rate_pct"] = round(max(0.2, float(state.get("error_rate_pct", 2.0)) - 0.8), 2)
            applied.append("Introduced canary/rollback controls")

        if re.search(r"\bhybrid|bm25|sparse|dense|exact-match|keyword\b", answer_l):
            mitigations = RAGIncidentMitigator.apply_recall_mitigation(state)
            applied.extend(mitigations)
        elif re.search(r"\breindex|re-embed|refresh index|chunk\b", answer_l):
            state["recall_score"] = round(min(0.95, float(state.get("recall_score", 0.7)) + 0.08), 2)
            state["latency_ms"] = int(state.get("latency_ms", 300) + 40)
            applied.append("Adjusted indexing/chunking")

        if re.search(r"\bsimilarity|threshold|semantic cache|lower threshold|lowering threshold\b", answer_l):
            mitigations = RAGIncidentMitigator.apply_cache_mitigation(state)
            applied.extend(mitigations)
        elif re.search(r"\bcache|caching|redis\b", answer_l):
            state["latency_ms"] = max(80, int(state.get("latency_ms", 300) * 0.7))
            state["memory_usage_pct"] = min(95, int(state.get("memory_usage_pct", 50) + 12))
            state["cache_hit_pct"] = min(95, int(state.get("cache_hit_pct", 60) + 15))
            applied.append("Enabled caching")

        if re.search(r"\brerate|rate limit|guardrail|moderation\b", answer_l):
            state["error_rate_pct"] = round(max(0.2, float(state.get("error_rate_pct", 2.0)) - 0.5), 2)
            applied.append("Added safety controls")
        if re.search(r"\bobservab|trace|metric|log\b", answer_l):
            applied.append("Improved observability")
            if "Insufficient telemetry" in unresolved:
                unresolved.remove("Insufficient telemetry")
        if not applied:
            applied.append("Recorded analytical response without direct system mutation")

        decisions.extend(applied)

        outcome = evaluation_outcome.lower()
        if outcome in {"correct", "strong"}:
            unresolved = [u for u in unresolved if u != "Root cause not yet confirmed"]
            if "Validate mitigation in production" not in unresolved:
                unresolved.append("Validate mitigation in production")
        elif outcome in {"incorrect", "false_claim", "unsupported"}:
            if "Hypothesis conflict with observed symptoms" not in unresolved:
                unresolved.append("Hypothesis conflict with observed symptoms")
        elif outcome in {"partial", "shallow"}:
            if "Incomplete mitigation plan" not in unresolved:
                unresolved.append("Incomplete mitigation plan")

        visible = (
            f"System state after your decision(s) [{', '.join(applied)}]: "
            f"latency {state.get('latency_ms')}ms, memory {state.get('memory_usage_pct')}%, "
            f"cache hit {state.get('cache_hit_pct')}%, recall {state.get('recall_score')}, "
            f"error rate {state.get('error_rate_pct')}%."
        )

        return WorldStateSnapshot(
            current_mission=mission_title or current.current_mission,
            constraints=list(current.constraints),
            system_state=state,
            candidate_decisions=decisions,
            unresolved_problems=unresolved,
            evidence=list(dict.fromkeys([*(evidence or []), *current.evidence])),
            difficulty=difficulty or current.difficulty,
            progress=progress or dict(current.progress),
            visible_summary=visible,
            version=current.version + 1,
        )
