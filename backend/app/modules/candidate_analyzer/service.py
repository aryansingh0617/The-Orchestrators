from __future__ import annotations

from typing import Any

from app.application.dtos import CandidateDTO, CandidateMissionDTO, CandidateSignalsDTO
from app.domain.interfaces import AIProvider, StructuredGenerationOptions
from app.modules.candidate_analyzer.schemas import CandidateAnalysisResult


class CandidateAnalyzer:
    """Derive role-relevant interview baselines from candidate learning state."""

    def __init__(self, ai_provider: AIProvider) -> None:
        self._ai_provider = ai_provider

    def analyze(
        self,
        candidate: CandidateDTO | None = None,
        *,
        profile_summary: str | None = None,
        role_target: str = "AI Engineer",
        seniority: str = "mid",
        completed_missions: list[CandidateMissionDTO] | None = None,
        skipped_topics: list[str] | None = None,
        learning_signals: dict[str, Any] | CandidateSignalsDTO | None = None,
        known_strengths: list[str] | None = None,
        possible_weaknesses: list[str] | None = None,
    ) -> CandidateAnalysisResult:
        if candidate is not None:
            member = candidate.member
            role_target = member.jobRole or role_target
            seniority = self._infer_seniority(member.yearsExperience, seniority)
            completed_missions = list(candidate.missions)
            learning_signals = candidate.signals
            profile_summary = profile_summary or self._build_profile_summary(candidate)

        missions = completed_missions or []
        signals = self._normalize_signals(learning_signals)
        completed_days = sorted({m.day for m in missions if m.passed})
        skipped = skipped_topics or [
            m.title for m in missions if m.skipped or m.passed is False
        ]
        strengths = known_strengths or [
            m.title for m in missions if m.passed and (m.attempts or 1) <= 1
        ]
        weaknesses = possible_weaknesses or [
            m.title for m in missions if m.skipped or (m.attempts or 0) >= 3 or m.passed is False
        ]

        heuristic = self._heuristic_analysis(
            role_target=role_target,
            seniority=seniority,
            completed_days=completed_days,
            skipped=skipped,
            strengths=strengths,
            weaknesses=weaknesses,
            signals=signals,
            profile_summary=profile_summary,
        )

        if not profile_summary and not missions and not signals:
            return heuristic

        prompt = (
            "Analyze candidate learning state for an adaptive technical interview.\n"
            f"Role target: {seniority} {role_target}\n"
            f"Profile: {profile_summary or 'n/a'}\n"
            f"Completed mission days: {completed_days}\n"
            f"Skipped/failed topics: {skipped}\n"
            f"Known strengths: {strengths}\n"
            f"Possible weaknesses: {weaknesses}\n"
            f"Learning signals: {signals}\n"
            "Return baseline strengths, areas to probe, starting difficulty (1-5), and confidence."
        )

        try:
            res = self._ai_provider.generate_structured(
                prompt=prompt,
                schema=CandidateAnalysisResult,
                options=StructuredGenerationOptions(
                    metadata={"prompt_id": "candidate.baseline.v1"}
                ),
            )
            parsed = CandidateAnalysisResult.model_validate(res.data)
            return parsed.model_copy(
                update={
                    "completed_mission_days": completed_days or parsed.completed_mission_days,
                    "skipped_topics": skipped or parsed.skipped_topics,
                    "known_strengths": strengths or parsed.known_strengths or parsed.baseline_strengths,
                    "possible_weaknesses": weaknesses or parsed.possible_weaknesses,
                    "role_target": role_target,
                    "seniority": seniority,
                    "starting_difficulty": max(
                        1,
                        min(
                            5,
                            heuristic.starting_difficulty
                            if not profile_summary and not missions
                            else parsed.starting_difficulty,
                        ),
                    ),
                    "baseline_strengths": parsed.baseline_strengths or heuristic.baseline_strengths,
                    "areas_to_probe": parsed.areas_to_probe or heuristic.areas_to_probe,
                    "confidence": parsed.confidence or heuristic.confidence,
                }
            )
        except Exception:
            return heuristic

    def _heuristic_analysis(
        self,
        *,
        role_target: str,
        seniority: str,
        completed_days: list[int],
        skipped: list[str],
        strengths: list[str],
        weaknesses: list[str],
        signals: dict[str, Any],
        profile_summary: str | None,
    ) -> CandidateAnalysisResult:
        starting = {"junior": 1, "mid": 2, "senior": 3, "staff": 4}.get(seniority.lower(), 2)
        completed_count = int(signals.get("missionsCompleted") or len(completed_days) or 0)
        first_try = int(signals.get("missionsFirstTry") or 0)
        if completed_count >= 20 and first_try >= max(1, completed_count - 2):
            starting = min(5, starting + 1)
        if weaknesses and len(weaknesses) >= 3:
            starting = max(1, starting - 1)

        baseline = strengths[:4] or [
            f"Foundational knowledge matching {seniority} bar",
        ]
        if profile_summary:
            baseline = list(dict.fromkeys([*baseline, "Documented professional background"]))

        areas = weaknesses[:4] or [
            "Practical production tradeoffs",
            "Failure recovery strategies",
        ]
        if skipped:
            areas = list(dict.fromkeys([*skipped[:3], *areas]))[:5]

        confidence = 0.55
        if completed_days or strengths or signals:
            confidence = 0.75
        if profile_summary and (completed_days or signals):
            confidence = 0.85

        return CandidateAnalysisResult(
            baseline_strengths=baseline,
            areas_to_probe=areas,
            starting_difficulty=starting,
            confidence=confidence,
            known_strengths=strengths or baseline,
            possible_weaknesses=weaknesses or areas,
            completed_mission_days=completed_days,
            skipped_topics=skipped,
            role_target=role_target,
            seniority=seniority,
        )

    @staticmethod
    def _normalize_signals(
        learning_signals: dict[str, Any] | CandidateSignalsDTO | None,
    ) -> dict[str, Any]:
        if learning_signals is None:
            return {}
        if isinstance(learning_signals, CandidateSignalsDTO):
            return learning_signals.model_dump(exclude_none=True)
        return dict(learning_signals)

    @staticmethod
    def _build_profile_summary(candidate: CandidateDTO) -> str:
        member = candidate.member
        parts = [
            member.name or "",
            member.jobRole or "",
            f"{member.yearsExperience} years" if member.yearsExperience is not None else "",
            member.education or "",
            member.status or "",
        ]
        return ", ".join(p for p in parts if p)

    @staticmethod
    def _infer_seniority(years: int | None, fallback: str) -> str:
        if years is None:
            return fallback
        if years >= 12:
            return "staff"
        if years >= 6:
            return "senior"
        if years >= 2:
            return "mid"
        return "junior"

    @staticmethod
    def get_default_analysis(seniority: str) -> CandidateAnalysisResult:
        return CandidateAnalyzer(ai_provider=_NullProvider())._heuristic_analysis(
            role_target="AI Engineer",
            seniority=seniority,
            completed_days=[],
            skipped=[],
            strengths=[],
            weaknesses=[],
            signals={},
            profile_summary=None,
        )


class _NullProvider:
    provider_name = "null"

    def generate_structured(self, *args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("null provider")
