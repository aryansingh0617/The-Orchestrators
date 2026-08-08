from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check API process health",
)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="chimera-api", version="0.1.0")
