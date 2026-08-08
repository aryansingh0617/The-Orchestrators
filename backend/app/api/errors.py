from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.errors import (
    ChimeraError,
    ConflictError,
    NotFoundError,
    PersistenceError,
    PolicyError,
    ProviderError,
    ValidationError,
)

ERROR_STATUS_CODES = {
    ValidationError: 400,
    NotFoundError: 404,
    ConflictError: 409,
    ProviderError: 503,
    PersistenceError: 503,
    PolicyError: 400,
}


def error_payload(
    *,
    code: str,
    message: str,
    trace_id: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
            "trace_id": trace_id,
        }
    }


def _trace_id(request: Request) -> str:
    settings = getattr(request.app.state, "settings", None)
    header_name = getattr(settings, "request_id_header", "X-Request-ID")
    return request.headers.get(header_name) or str(uuid4())


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ChimeraError)
    async def handle_chimera_error(request: Request, exc: ChimeraError) -> JSONResponse:
        status_code = 500
        for error_type, mapped_status in ERROR_STATUS_CODES.items():
            if isinstance(exc, error_type):
                status_code = mapped_status
                break
        return JSONResponse(
            status_code=status_code,
            content=error_payload(
                code=exc.code,
                message=exc.message,
                details=exc.details,
                trace_id=_trace_id(request),
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=error_payload(
                code="request_validation_error",
                message="The request body is invalid.",
                details={"errors": exc.errors()},
                trace_id=_trace_id(request),
            ),
        )
