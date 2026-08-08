from typing import Annotated, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import get_interview_service
from app.application.dtos import (
    CandidateDTO,
    EvaluationSummaryDTO,
    FeedbackDTO,
    InterviewCommand,
    InterviewResult,
    MissionPublicDTO,
    ProgressDTO,
    WorldStatePublicDTO,
)
from app.application.services import InterviewService


class InterviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sessionId: str = Field(
        min_length=1,
        max_length=128,
        description="Caller-provided interview session key.",
    )
    candidate: CandidateDTO | None = Field(
        default=None,
        description="Candidate object required when starting a new session.",
    )
    message: str | None = Field(
        default=None,
        max_length=8000,
        description="Candidate response for an existing session.",
    )


class FeedbackResponse(BaseModel):
    summary: str
    strengths: list[str]
    gaps: list[str]
    next: list[str]
    engineering_dna: dict[str, float] = Field(default_factory=dict)
    hiring_assessment: str | None = None


class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: FeedbackResponse | None = None
    session_id: str | None = None
    question_number: int | None = None
    curriculum_day: int | None = None
    competency: str | None = None
    mission: MissionPublicDTO | None = None
    world_state: WorldStatePublicDTO | None = None
    progress: ProgressDTO | None = None
    evaluation_summary: EvaluationSummaryDTO | None = None
    mode: str | None = None


router = APIRouter(prefix="/api", tags=["interview"])


@router.post(
    "/interview",
    response_model=InterviewResponse,
    summary="Run a Chimera interview turn",
    description=(
        "Required hackathon endpoint. Starts a session when candidate data is supplied, "
        "or processes a candidate message for an existing session. "
        "Core fields reply/done/feedback remain required for compatibility; "
        "structured mission/world/progress fields are additive and candidate-safe."
    ),
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "start": {
                            "summary": "Start interview",
                            "value": {
                                "sessionId": "abc-123",
                                "candidate": {
                                    "member": {
                                        "id": "CAND-003",
                                        "name": "Emily Chen",
                                        "jobRole": "AI Engineer",
                                        "yearsExperience": 6,
                                        "education": "MS Artificial Intelligence",
                                        "status": "COMPLETED",
                                    },
                                    "missions": [],
                                    "signals": {
                                        "commitDays": 31,
                                        "missionsCompleted": 31,
                                        "missionsFirstTry": 30,
                                    },
                                },
                            },
                        },
                        "turn": {
                            "summary": "Conversation turn",
                            "value": {
                                "sessionId": "abc-123",
                                "message": "I would inspect retrieval logs first.",
                            },
                        },
                    }
                }
            }
        }
    },
)
def interview(
    request: InterviewRequest,
    service: Annotated[InterviewService, Depends(get_interview_service)],
) -> dict[str, Any]:
    command = InterviewCommand(
        session_id=request.sessionId,
        candidate=request.candidate,
        message=request.message,
    )
    result: InterviewResult = service.handle(command)
    payload = result.model_dump()
    if result.feedback is not None:
        payload["feedback"] = FeedbackDTO.model_validate(result.feedback).model_dump()
    return payload
