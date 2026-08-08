from __future__ import annotations

import re

from app.domain.interfaces import AIProvider, StructuredGenerationOptions
from app.modules.evaluation_engine.schemas import EvaluationResult, EvidenceItem
from app.modules.mission_generator.schemas import MissionBrief

SIGNAL_PATTERNS = {
    "systems_thinking": r"\b(latency|throughput|bottleneck|cascade|dependency|end-to-end)\b",
    "tradeoffs": r"\b(trade-?off|cost|latency vs|quality vs|budget|compromise)\b",
    "reliability": r"\b(rollback|canary|retry|timeout|circuit|sla|slo|failover)\b",
    "debugging": r"\b(root cause|reproduc|hypothesis|log|trace|metric|bisect)\b",
    "architecture": r"\b(architect|component|pipeline|interface|boundary|layer)\b",
    "optimization": r"\b(cache|batch|index|compress|quantize|approximate)\b",
    "security": r"\b(auth|least privilege|injection|exfiltrat|guardrail|redact)\b",
    "measurement": r"\b(measure|evaluat|metric|dashboard|recall|precision|p95)\b",
}

FALSE_CLAIM_PATTERNS = [
    r"embeddings?\s+guarantee\s+correctness",
    r"vector\s+db\s+eliminates\s+hallucin",
    r"prompt\s+alone\s+solves\s+retrieval",
]


class EvaluationEngine:
    def __init__(self, ai_provider: AIProvider | None = None) -> None:
        self._ai_provider = ai_provider

    def evaluate(
        self,
        *,
        mission: MissionBrief,
        candidate_answer: str,
        previous_outcome: str | None = None,
    ) -> EvaluationResult:
        heuristic = self._heuristic(mission, candidate_answer, previous_outcome)
        if self._ai_provider is None:
            return heuristic
        try:
            prompt = (
                "Evaluate the candidate answer with evidence-based scoring.\n"
                f"Mission: {mission.model_dump_json()}\n"
                f"Answer: {candidate_answer}\n"
                "Do not expose chain-of-thought; return concise rationale and evidence."
            )
            res = self._ai_provider.generate_structured(
                prompt=prompt,
                schema=EvaluationResult,
                options=StructuredGenerationOptions(
                    metadata={"prompt_id": "evaluation.score.v1"}
                ),
            )
            parsed = EvaluationResult.model_validate(res.data)
            # Keep deterministic evidence-based outcome; allow provider to refine rationale.
            return heuristic.model_copy(
                update={
                    "rationale": parsed.rationale or heuristic.rationale,
                    "evidence": heuristic.evidence or parsed.evidence,
                }
            )
        except Exception:
            return heuristic

    def _heuristic(
        self,
        mission: MissionBrief,
        candidate_answer: str,
        previous_outcome: str | None,
    ) -> EvaluationResult:
        text = candidate_answer.strip()
        if not text:
            return EvaluationResult(
                outcome="incorrect",
                overall_score=0.0,
                rationale="Empty answer provided no evaluable evidence.",
                evidence=[
                    EvidenceItem(
                        competency=mission.competency,
                        observation="No candidate response content.",
                        polarity="negative",
                        strength=5,
                        confidence=1.0,
                        rationale="Empty answers cannot demonstrate competency.",
                        claim_label="incorrect",
                    )
                ],
                engineering_dna=self._dna(0.1),
                claim_labels=["empty_response"],
            )

        lowered = text.lower()
        hits = {name: bool(re.search(pat, lowered)) for name, pat in SIGNAL_PATTERNS.items()}
        hit_count = sum(1 for v in hits.values() if v)
        word_count = len(re.findall(r"\w+", text))
        false_claim = any(re.search(pat, lowered) for pat in FALSE_CLAIM_PATTERNS)

        if false_claim:
            outcome = "false_claim"
            score = 0.25
        elif hit_count >= 4 and word_count >= 40:
            outcome = "strong"
            score = 0.88
        elif hit_count >= 3:
            outcome = "correct"
            score = 0.78
        elif hit_count >= 2:
            outcome = "partial"
            score = 0.58
        elif hit_count == 1 or word_count >= 25:
            outcome = "shallow"
            score = 0.42
        else:
            outcome = "unsupported"
            score = 0.3

        # Repeated shallow answers should not be rewarded by length alone.
        if previous_outcome in {"shallow", "partial"} and outcome == "shallow":
            score = max(0.2, score - 0.1)

        evidence = [
            EvidenceItem(
                competency=mission.competency,
                observation=f"Detected signals: {[k for k, v in hits.items() if v] or ['none']}",
                polarity="positive" if score >= 0.6 else "negative" if score < 0.4 else "neutral",
                strength=min(5, max(1, hit_count + 1)),
                confidence=0.75,
                rationale=f"Outcome classified as {outcome} from technical signal coverage.",
                claim_label=outcome,
            )
        ]
        if "measure" not in lowered and outcome in {"partial", "shallow", "correct"}:
            evidence.append(
                EvidenceItem(
                    competency=mission.competency,
                    observation="Limited discussion of post-change measurement.",
                    polarity="negative",
                    strength=2,
                    confidence=0.65,
                    rationale="Production judgment usually includes measurement.",
                    claim_label="gap",
                )
            )

        dna = self._dna(score)
        dna["Systems Thinking"] = 0.2 + 0.8 * float(hits["systems_thinking"])
        dna["Debugging"] = 0.2 + 0.8 * float(hits["debugging"])
        dna["Architecture"] = 0.2 + 0.8 * float(hits["architecture"])
        dna["Reliability"] = 0.2 + 0.8 * float(hits["reliability"])
        dna["Optimization"] = 0.2 + 0.8 * float(hits["optimization"])
        dna["Trade-off Quality"] = 0.2 + 0.8 * float(hits["tradeoffs"])
        dna["AI Engineering"] = score
        dna["Communication"] = min(1.0, word_count / 80)
        dna["Adaptability"] = 0.55 if previous_outcome and outcome != previous_outcome else 0.45

        return EvaluationResult(
            outcome=outcome,
            technical_correctness=score,
            reasoning=min(1.0, 0.3 + 0.15 * hit_count),
            depth=min(1.0, word_count / 100),
            systems_thinking=dna["Systems Thinking"],
            tradeoffs=dna["Trade-off Quality"],
            reliability=dna["Reliability"],
            problem_solving=dna["Debugging"],
            communication=dna["Communication"],
            adaptability=dna["Adaptability"],
            overall_score=score,
            evidence=evidence,
            rationale=f"Evidence-based classification: {outcome}.",
            engineering_dna={k: round(v, 2) for k, v in dna.items()},
            claim_labels=[outcome, *[k for k, v in hits.items() if v]],
        )

    @staticmethod
    def _dna(base: float) -> dict[str, float]:
        return {
            "Systems Thinking": base,
            "AI Engineering": base,
            "Debugging": base,
            "Architecture": base,
            "Reliability": base,
            "Optimization": base,
            "Trade-off Quality": base,
            "Communication": base,
            "Adaptability": base,
        }
