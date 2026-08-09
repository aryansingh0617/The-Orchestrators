from __future__ import annotations

from app.domain.interfaces import AIProvider, StructuredGenerationOptions
from app.modules.mission_generator.schemas import MissionBrief

MISSION_TEMPLATES: dict[str, dict[str, str]] = {
    "RAG Architecture": {
        "title": "RAG Index Refresh Incident",
        "scenario": (
            "After an embedding index refresh, customer queries show lower recall and "
            "occasional ungrounded answers."
        ),
        "type": "debugging",
    },
    "Vector Databases": {
        "title": "Vector Search Latency Spike",
        "scenario": (
            "HNSW query latency jumped after a large upsert batch while recall stayed acceptable."
        ),
        "type": "scaling",
    },
    "Prompt Engineering": {
        "title": "Prompt Regression in Structured Outputs",
        "scenario": (
            "A prompt change improved tone but increased JSON schema validation failures by 18%."
        ),
        "type": "tradeoff",
    },
    "Agentic AI & MCP": {
        "title": "Agent Tool Loop Divergence",
        "scenario": (
            "A tool-using agent retries the same failing MCP call and exceeds the latency SLO."
        ),
        "type": "reliability",
    },
    "Production AI Systems": {
        "title": "Canary Model Quality Drop",
        "scenario": (
            "A canary deployment reduced p95 latency but increased unsupported factual claims."
        ),
        "type": "incident_response",
    },
}


class MissionGenerator:
    def __init__(self, ai_provider: AIProvider) -> None:
        self._ai_provider = ai_provider

    def generate(
        self,
        *,
        competency: str,
        curriculum_day: int,
        difficulty: str,
        evidence_needed: list[str] | None = None,
        topic: str | None = None,
        learning_objective: str | None = None,
        mode: str = "new_mission",
        previous_answer: str | None = None,
        world_summary: str | None = None,
    ) -> MissionBrief:
        fallback = self._fallback(
            competency=competency,
            curriculum_day=curriculum_day,
            difficulty=difficulty,
            evidence_needed=evidence_needed or [],
            topic=topic,
            learning_objective=learning_objective,
            mode=mode,
            previous_answer=previous_answer,
            world_summary=world_summary,
        )
        prompt = (
            "Generate a realistic AI engineering interview mission.\n"
            f"Competency: {competency}\n"
            f"Curriculum day: {curriculum_day}\n"
            f"Difficulty: {difficulty}\n"
            f"Mode: {mode}\n"
            f"Topic: {topic or competency}\n"
            f"Learning objective: {learning_objective or ''}\n"
            f"Evidence needed: {evidence_needed or []}\n"
            f"Previous answer: {previous_answer or ''}\n"
            f"World state: {world_summary or ''}\n"
            "Include hidden_evaluation_criteria for evaluators only."
        )
        try:
            res = self._ai_provider.generate_structured(
                prompt=prompt,
                schema=MissionBrief,
                options=StructuredGenerationOptions(
                    metadata={"prompt_id": "mission.generate.v1"}
                ),
            )
            mission = MissionBrief.model_validate(res.data)
            title = mission.title if mission.title and mission.title != "Stub Mission" else fallback.title
            scenario = (
                mission.scenario
                if mission.scenario and "Stub" not in mission.scenario
                else fallback.scenario
            )
            return mission.model_copy(
                update={
                    "title": title,
                    "scenario": scenario,
                    "context": mission.context or fallback.context,
                    "constraints": mission.constraints or fallback.constraints,
                    "objective": mission.objective or fallback.objective,
                    "competency": competency,
                    "curriculum_day": curriculum_day,
                    "difficulty": difficulty,
                    "mission_type": mission.mission_type or fallback.mission_type,
                    "hidden_evaluation_criteria": (
                        mission.hidden_evaluation_criteria
                        or fallback.hidden_evaluation_criteria
                    ),
                    "expected_evidence": mission.expected_evidence or fallback.expected_evidence,
                    "followup_options": mission.followup_options or fallback.followup_options,
                }
            )
        except Exception:
            return fallback

    def _fallback(
        self,
        *,
        competency: str,
        curriculum_day: int,
        difficulty: str,
        evidence_needed: list[str],
        topic: str | None,
        learning_objective: str | None,
        mode: str,
        previous_answer: str | None,
        world_summary: str | None,
    ) -> MissionBrief:
        template = None
        for key, value in MISSION_TEMPLATES.items():
            if key.lower() in competency.lower() or competency.lower() in key.lower():
                template = value
                break
        if template is None:
            template = {
                "title": f"{competency} Challenge",
                "scenario": (
                    f"You are on-call for a production AI system related to {topic or competency}."
                ),
                "type": "architecture",
            }

        if mode in {"follow_up", "deepen"}:
            title = f"Follow-up: {template['title']}"
            scenario = (
                f"Based on your previous response, the system state is now: "
                f"{world_summary or 'partially mitigated'}. "
                f"Push deeper on {competency}."
            )
            if previous_answer:
                scenario += " Address the gaps implied by your last answer."
        elif mode == "revisit_gap":
            title = f"Gap Revisit: {template['title']}"
            scenario = (
                f"Earlier evidence suggested a gap in {competency}. "
                f"Revisit the scenario with a fresh constraint set."
            )
        else:
            title = template["title"]
            scenario = template["scenario"]

        return MissionBrief(
            title=title,
            scenario=scenario,
            context=learning_objective or f"Assess {competency} for curriculum day {curriculum_day}.",
            constraints=[
                "Do not invent telemetry you were not given",
                "Prefer measurable mitigations",
                "Call out tradeoffs explicitly",
            ],
            objective="Diagnose, propose a mitigation, and define success metrics.",
            competency=competency,
            curriculum_day=curriculum_day,
            difficulty=difficulty,
            mission_type=template["type"],
            expected_evidence=evidence_needed
            or ["root-cause hypothesis", "mitigation", "measurement plan"],
            hidden_evaluation_criteria=[
                "Separates retrieval/model/prompt failure modes",
                "Ties actions to measurable production signals",
                "Surfaces tradeoffs (latency, cost, quality, safety)",
            ],
            followup_options=[
                "What would you measure after shipping?",
                "What is the rollback trigger?",
                "How does this change under 10x traffic?",
            ],
        )
