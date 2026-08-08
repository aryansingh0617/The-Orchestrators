from typing import Any

from pydantic import BaseModel, Field


class WorldStateSnapshot(BaseModel):
    current_mission: str = ""
    constraints: list[str] = Field(default_factory=list)
    system_state: dict[str, Any] = Field(default_factory=dict)
    candidate_decisions: list[str] = Field(default_factory=list)
    unresolved_problems: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    difficulty: str = "intermediate"
    progress: dict[str, Any] = Field(default_factory=dict)
    visible_summary: str = ""
    version: int = 1
