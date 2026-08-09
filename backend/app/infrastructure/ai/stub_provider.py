from __future__ import annotations

import hashlib
from typing import Any, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from app.domain.errors import ProviderError
from app.domain.interfaces import StructuredGenerationOptions, StructuredGenerationResult


class StubProvider:
    """Deterministic provider that satisfies arbitrary Pydantic schemas for tests."""

    provider_name = "stub"
    model_name = "chimera-deterministic-stub"

    def generate_structured(
        self,
        prompt: str,
        schema: type[Any],
        options: StructuredGenerationOptions | None = None,
    ) -> StructuredGenerationResult:
        digest = hashlib.sha256(prompt.strip().encode("utf-8")).hexdigest()[:8]
        try:
            if isinstance(schema, type) and issubclass(schema, BaseModel):
                payload = self._build_for_schema(schema, prompt, digest)
                validated = schema.model_validate(payload).model_dump()
            else:
                validated = {"reply": f"Stub output {digest}", "done": False}
        except Exception as exc:
            raise ProviderError(
                "Stub provider could not validate structured output.",
                details={"schema": getattr(schema, "__name__", str(schema))},
            ) from exc
        return StructuredGenerationResult(
            data=validated,
            provider=self.provider_name,
            model=self.model_name,
            raw_text=str(validated),
        )

    def _build_for_schema(self, schema: type[BaseModel], prompt: str, digest: str) -> dict[str, Any]:
        name = schema.__name__
        if name == "InterviewResult":
            return {
                "reply": (
                    "Milestone 3 backend is wired. Future milestones will adapt this "
                    f"interview from collected evidence. Stub trace: {digest}."
                ),
                "done": False,
                "feedback": None,
            }
        if name == "CandidateAnalysisResult":
            return {
                "baseline_strengths": ["Retrieval debugging", "Production awareness"],
                "areas_to_probe": ["Cost/latency tradeoffs", "Evaluation harness design"],
                "starting_difficulty": 3,
                "confidence": 0.72,
                "known_strengths": ["Retrieval debugging"],
                "possible_weaknesses": ["Cost/latency tradeoffs"],
                "completed_mission_days": [1, 2, 3],
                "skipped_topics": [],
                "role_target": "AI Engineer",
                "seniority": "senior",
            }
        if name == "CurriculumAnalysisResult":
            return {
                "competencies": [
                    {
                        "name": "RAG Architecture",
                        "description": "Retrieval systems design",
                        "priority": 1,
                        "related_days": [1, 2],
                    }
                ],
                "priority_levels": {"RAG Architecture": 1},
                "expected_seniority_bar": "senior",
                "mission_family_recommendations": ["debugging", "architecture", "tradeoff"],
                "out_of_scope_topics": ["css styling"],
                "curriculum_days": [],
                "confidence": 0.8,
            }
        if name == "PlanningDecision":
            return {
                "next_curriculum_day": 1,
                "competency": "RAG Architecture",
                "difficulty": "intermediate",
                "mode": "new_mission",
                "reason": f"Stub planner decision {digest}",
                "evidence_needed": ["root-cause hypothesis"],
            }
        if name == "MissionBrief":
            return {
                "title": "Stub Mission",
                "scenario": "A production AI incident requires diagnosis.",
                "context": "Stub context",
                "constraints": ["Stay evidence-based"],
                "objective": "Propose a mitigation with metrics",
                "competency": "RAG Architecture",
                "curriculum_day": 1,
                "difficulty": "intermediate",
                "mission_type": "debugging",
                "expected_evidence": ["hypothesis"],
                "hidden_evaluation_criteria": ["Separates failure modes"],
                "followup_options": ["What would you measure?"],
            }
        if name == "EvaluationResult":
            return {
                "outcome": "partial",
                "technical_correctness": 0.6,
                "reasoning": 0.6,
                "depth": 0.5,
                "systems_thinking": 0.55,
                "tradeoffs": 0.5,
                "reliability": 0.5,
                "problem_solving": 0.55,
                "communication": 0.6,
                "adaptability": 0.5,
                "overall_score": 0.58,
                "evidence": [
                    {
                        "competency": "RAG Architecture",
                        "observation": "Mentioned logs and mitigation",
                        "polarity": "positive",
                        "strength": 3,
                        "confidence": 0.7,
                        "rationale": "Partial production reasoning",
                        "claim_label": "partial",
                    }
                ],
                "rationale": "Partial evidence-based response",
                "engineering_dna": {
                    "Systems Thinking": 0.55,
                    "AI Engineering": 0.58,
                    "Debugging": 0.6,
                    "Architecture": 0.5,
                    "Reliability": 0.5,
                    "Optimization": 0.45,
                    "Trade-off Quality": 0.5,
                    "Communication": 0.6,
                    "Adaptability": 0.5,
                },
                "claim_labels": ["partial"],
            }

        # Generic schema fill for any other BaseModel.
        payload: dict[str, Any] = {}
        for field_name, field in schema.model_fields.items():
            payload[field_name] = self._default_for_field(field_name, field, digest)
        return payload

    def _default_for_field(self, name: str, field: FieldInfo, digest: str) -> Any:
        if field.default is not None and field.default is not Ellipsis:
            return field.default
        if field.default_factory is not None:
            return field.default_factory()
        annotation = field.annotation
        origin = get_origin(annotation)
        args = get_args(annotation)
        if origin is list:
            return []
        if origin is dict:
            return {}
        if annotation is str or str in args:
            if name in {"mode"}:
                return "new_mission"
            if name in {"difficulty"}:
                return "intermediate"
            if name in {"outcome"}:
                return "partial"
            if name in {"polarity"}:
                return "neutral"
            return f"stub-{name}-{digest}"
        if annotation is int or int in args:
            return 1
        if annotation is float or float in args:
            return 0.5
        if annotation is bool or bool in args:
            return False
        return None
