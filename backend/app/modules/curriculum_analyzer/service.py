from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.domain.interfaces import AIProvider, StructuredGenerationOptions
from app.modules.curriculum_analyzer.schemas import (
    CompetencyDetail,
    CurriculumAnalysisResult,
    CurriculumDayDetail,
)

DEFAULT_CURRICULUM_PATH = Path(__file__).resolve().parents[2] / "resources" / "curriculum.json"

MISSION_FAMILIES = [
    "architecture",
    "debugging",
    "incident_response",
    "tradeoff",
    "scaling",
    "reliability",
    "security",
    "optimization",
]


class CurriculumAnalyzer:
    """Analyze supplied curriculum structure into assessment competencies."""

    def __init__(
        self,
        ai_provider: AIProvider,
        curriculum_path: Path | None = None,
    ) -> None:
        self._ai_provider = ai_provider
        self._curriculum_path = curriculum_path or DEFAULT_CURRICULUM_PATH

    def analyze(
        self,
        role_title: str,
        seniority: str,
        curriculum_text: str | None = None,
        curriculum_data: dict[str, Any] | None = None,
        assessment_mode: str = "standard",
    ) -> CurriculumAnalysisResult:
        payload = curriculum_data
        if payload is None:
            if curriculum_text and curriculum_text.strip():
                try:
                    payload = json.loads(curriculum_text)
                except json.JSONDecodeError:
                    payload = {"raw_text": curriculum_text}
            else:
                payload = self.load_default_curriculum()

        days = self._extract_days(payload)
        if not days and isinstance(payload, dict) and "raw_text" in payload:
            return self._analyze_with_provider(
                role_title=role_title,
                seniority=seniority,
                curriculum_text=str(payload["raw_text"]),
                assessment_mode=assessment_mode,
                days=[],
            )

        structured = self._structure_from_days(days, seniority)
        if not days:
            return self.get_default_analysis(role_title, seniority)

        # Prefer deterministic structure from supplied curriculum; AI may enrich metadata.
        try:
            prompt = (
                f"Analyze curriculum for a {seniority} {role_title} role.\n"
                f"Assessment Mode: {assessment_mode}\n"
                f"Curriculum days: {json.dumps([d.model_dump() for d in days])}\n"
                "Extract competencies, priority levels, seniority bar, mission families, "
                "and out-of-scope topics. Preserve curriculum day metadata."
            )
            res = self._ai_provider.generate_structured(
                prompt=prompt,
                schema=CurriculumAnalysisResult,
                options=StructuredGenerationOptions(
                    metadata={"prompt_id": "curriculum.analyze.v1"}
                ),
            )
            parsed = CurriculumAnalysisResult.model_validate(res.data)
            return structured.model_copy(
                update={
                    "mission_family_recommendations": (
                        parsed.mission_family_recommendations
                        or structured.mission_family_recommendations
                    ),
                    "out_of_scope_topics": (
                        parsed.out_of_scope_topics or structured.out_of_scope_topics
                    ),
                    "expected_seniority_bar": seniority,
                    "confidence": max(structured.confidence, parsed.confidence or 0.0),
                }
            )
        except Exception:
            return structured

    def _analyze_with_provider(
        self,
        *,
        role_title: str,
        seniority: str,
        curriculum_text: str,
        assessment_mode: str,
        days: list[CurriculumDayDetail],
    ) -> CurriculumAnalysisResult:
        try:
            prompt = (
                f"Analyze curriculum for a {seniority} {role_title} role.\n"
                f"Assessment Mode: {assessment_mode}\n"
                f"Curriculum Content: {curriculum_text}\n"
                "Extract competencies, priorities, seniority bar, mission families, out-of-scope topics."
            )
            res = self._ai_provider.generate_structured(
                prompt=prompt,
                schema=CurriculumAnalysisResult,
                options=StructuredGenerationOptions(
                    metadata={"prompt_id": "curriculum.analyze.v1"}
                ),
            )
            return CurriculumAnalysisResult.model_validate(res.data)
        except Exception:
            return self.get_default_analysis(role_title, seniority)

    def load_default_curriculum(self) -> dict[str, Any]:
        if self._curriculum_path.exists():
            return json.loads(self._curriculum_path.read_text(encoding="utf-8"))
        return {"modules": []}

    def _extract_days(self, payload: dict[str, Any] | None) -> list[CurriculumDayDetail]:
        if not payload:
            return []
        days: list[CurriculumDayDetail] = []
        for module in payload.get("modules", []):
            module_name = module.get("name", "")
            for item in module.get("days", []):
                days.append(
                    CurriculumDayDetail(
                        day=int(item["day"]),
                        topic=str(item.get("topic") or item.get("title") or f"Day {item['day']}"),
                        learning_objective=str(item.get("learning_objective") or ""),
                        tools=list(item.get("tools") or []),
                        prerequisites=list(item.get("prerequisites") or []),
                        module=module_name,
                    )
                )
        if not days and "days" in payload:
            for item in payload["days"]:
                days.append(
                    CurriculumDayDetail(
                        day=int(item["day"]),
                        topic=str(item.get("topic") or item.get("title") or f"Day {item['day']}"),
                        learning_objective=str(item.get("learning_objective") or ""),
                        tools=list(item.get("tools") or []),
                        prerequisites=list(item.get("prerequisites") or []),
                        module=str(item.get("module") or ""),
                    )
                )
        return sorted(days, key=lambda d: d.day)

    def _structure_from_days(
        self,
        days: list[CurriculumDayDetail],
        seniority: str,
    ) -> CurriculumAnalysisResult:
        competencies: list[CompetencyDetail] = []
        for index, day in enumerate(days):
            name = day.module or day.topic
            existing = next((c for c in competencies if c.name == name), None)
            if existing:
                existing.related_days.append(day.day)
                continue
            competencies.append(
                CompetencyDetail(
                    name=name,
                    description=day.learning_objective or day.topic,
                    priority=min(5, 1 + index // 2),
                    related_days=[day.day],
                )
            )
        priority_levels = {c.name: c.priority for c in competencies}
        return CurriculumAnalysisResult(
            competencies=competencies,
            priority_levels=priority_levels,
            expected_seniority_bar=seniority,
            mission_family_recommendations=MISSION_FAMILIES[:5],
            out_of_scope_topics=["general frontend styling", "HR soft-skill quizzes"],
            curriculum_days=days,
            confidence=0.9 if days else 0.4,
        )

    @staticmethod
    def get_default_analysis(role_title: str, seniority: str) -> CurriculumAnalysisResult:
        competencies = [
            CompetencyDetail(
                name="RAG Architecture",
                description="Design and debug retrieval augmented generation architectures.",
                priority=1,
                related_days=[1, 2],
            ),
            CompetencyDetail(
                name="Vector Databases",
                description="Vector storage, indexing strategies, and hybrid search.",
                priority=2,
                related_days=[3, 4],
            ),
            CompetencyDetail(
                name="Prompt Engineering",
                description="Structured prompting and evaluation of prompt changes.",
                priority=3,
                related_days=[5, 6],
            ),
            CompetencyDetail(
                name="Agentic AI & MCP",
                description="Tool-using agents and secure MCP integrations.",
                priority=2,
                related_days=[7, 8, 9, 10],
            ),
            CompetencyDetail(
                name="Production AI Systems",
                description="Deployment, observability, reliability, and cost tradeoffs.",
                priority=1,
                related_days=[11, 12, 13, 14],
            ),
        ]
        days = [
            CurriculumDayDetail(
                day=d,
                topic=c.name,
                learning_objective=c.description,
                tools=[],
                prerequisites=[],
                module=c.name,
            )
            for c in competencies
            for d in c.related_days
        ]
        return CurriculumAnalysisResult(
            competencies=competencies,
            priority_levels={c.name: c.priority for c in competencies},
            expected_seniority_bar=seniority,
            mission_family_recommendations=MISSION_FAMILIES[:5],
            out_of_scope_topics=["general frontend", "css styling"],
            curriculum_days=sorted(days, key=lambda x: x.day),
            confidence=0.5,
        )
