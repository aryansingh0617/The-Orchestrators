from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class StructuredGenerationOptions:
    temperature: float = 0.0
    max_tokens: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class StructuredGenerationResult:
    data: dict[str, Any]
    provider: str
    model: str
    raw_text: str | None = None


class AIProvider(Protocol):
    provider_name: str

    def generate_structured(
        self,
        prompt: str,
        schema: type[Any],
        options: StructuredGenerationOptions | None = None,
    ) -> StructuredGenerationResult:
        """Generate schema-valid structured output from a provider-neutral prompt."""
