from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.modules.candidate_analyzer.schemas import CandidateAnalysisResult
from app.modules.curriculum_analyzer.schemas import CurriculumAnalysisResult
from app.modules.evaluation_engine.schemas import EvaluationResult
from app.modules.memory_engine.schemas import InterviewMemory
from app.modules.mission_generator.schemas import MissionBrief
from app.modules.world_state_engine.schemas import WorldStateSnapshot


class InterviewRuntimeState(BaseModel):
    session_id: str
    internal_session_id: str
    role_title: str
    seniority: str
    question_count: int = 0
    covered_curriculum_days: list[int] = Field(default_factory=list)
    current_curriculum_day: int | None = None
    current_competency: str | None = None
    current_difficulty: str = "intermediate"
    follow_up_history: list[str] = Field(default_factory=list)
    previous_question: str | None = None
    previous_evaluation: EvaluationResult | None = None
    candidate_analysis: CandidateAnalysisResult | None = None
    curriculum_analysis: CurriculumAnalysisResult | None = None
    memory: InterviewMemory = Field(default_factory=InterviewMemory)
    world: WorldStateSnapshot = Field(default_factory=WorldStateSnapshot)
    current_mission: MissionBrief | None = None
    competency_scores: dict[str, list[float]] = Field(default_factory=dict)
    engineering_dna_accum: dict[str, list[float]] = Field(default_factory=dict)
    progression: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    done: bool = False

    def average_competency_scores(self) -> dict[str, float]:
        return {
            key: sum(vals) / len(vals)
            for key, vals in self.competency_scores.items()
            if vals
        }

    def average_dna(self) -> dict[str, float]:
        return {
            key: sum(vals) / len(vals)
            for key, vals in self.engineering_dna_accum.items()
            if vals
        }

    def day_competency_map(self) -> dict[int, str]:
        if not self.curriculum_analysis:
            return {}
        mapping: dict[int, str] = {}
        for day in self.curriculum_analysis.curriculum_days:
            mapping[day.day] = day.module or day.topic
        for comp in self.curriculum_analysis.competencies:
            for day in comp.related_days:
                mapping.setdefault(day, comp.name)
        return mapping

    def to_persistable(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
