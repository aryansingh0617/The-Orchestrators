from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies import get_interview_service
from app.application.dtos import CandidateDTO, InterviewCommand, InterviewResult
from app.application.services import InterviewService


class InterviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sessionId: str = Field(min_length=1, description="Caller-provided interview session key.")
    candidate: CandidateDTO | None = Field(
        default=None,
        description="Candidate object required when starting a new session.",
    )
    message: str | None = Field(
        default=None,
        description="Candidate response for an existing session.",
    )


class FeedbackResponse(BaseModel):
    summary: str
    strengths: list[str]
    gaps: list[str]
    next: list[str]


class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: FeedbackResponse | None = None


router = APIRouter(prefix="/api", tags=["interview"])


@router.post(
    "/interview",
    response_model=InterviewResponse,
    summary="Run a Chimera interview turn",
    description=(
        "Required hackathon endpoint. Starts a session when candidate data is supplied, "
        "or processes a candidate message for an existing session."
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
) -> InterviewResult:
    command = InterviewCommand(
        session_id=request.sessionId,
        candidate=request.candidate,
        message=request.message,
    )
    return service.handle(command)
