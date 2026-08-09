import traceback
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
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
        description="Unique external identifier for the interview session.",
    )
    candidate: CandidateDTO = Field(
        description="Complete candidate context payload."
    )
    message: str = Field(
        default="",
        max_length=8000,
        description="Latest candidate response or message text.",
    )


class ProgressResponse(BaseModel):
    summary: EvaluationSummaryDTO
    progress: ProgressDTO
    worldState: WorldStatePublicDTO
    activeMission: MissionPublicDTO | None = None
    reply: str | None = None
    feedback: FeedbackDTO | None = None


router = APIRouter(tags=["interview"])


@router.post(
    "/interview",
    response_model=ProgressResponse,
    summary="Process an interview turn and update world state",
    description="Primary evaluation endpoint accepting candidate context and messages. Runs evaluation pipeline and transitions state.",
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


class ChatSessionRequest(BaseModel):
    sessionId: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=8000)
    chat_history: list[dict[str, Any]] | None = Field(default_factory=list)
    candidate_info: dict[str, Any] | None = None


class ChatSessionResponse(BaseModel):
    session_id: str
    reply: str
    provider: str
    status: str


@router.post(
    "/interview/chat",
    response_model=ChatSessionResponse,
    summary="Interactive AI Chat Interviewer powered by Google Gemini",
    description="Adaptive technical interviewer evaluating completed concepts, posing intelligent follow-ups, and providing actionable feedback.",
)
def interview_chat(request: ChatSessionRequest) -> Any:
    from app.application.services.ai_service import ai_service

    try:
        return ai_service.handle_chat_session(
            session_id=request.sessionId,
            message=request.message,
            chat_history=request.chat_history,
            candidate_info=request.candidate_info,
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "message": "Gemini API Execution Error",
                "detail": str(e),
            },
        )
