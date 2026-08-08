from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ChimeraError(Exception):
    message: str
    code: str = "chimera_error"
    details: dict[str, Any] = field(default_factory=dict)


class ValidationError(ChimeraError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="validation_error", details=details or {})


class NotFoundError(ChimeraError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="not_found", details=details or {})


class ConflictError(ChimeraError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="conflict", details=details or {})


class ProviderError(ChimeraError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="provider_error", details=details or {})


class PersistenceError(ChimeraError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="persistence_error", details=details or {})


class PolicyError(ChimeraError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="policy_error", details=details or {})
