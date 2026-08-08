import hashlib
from typing import Any

from pydantic import BaseModel

from app.domain.errors import ProviderError
from app.domain.interfaces import StructuredGenerationOptions, StructuredGenerationResult


class StubProvider:
    provider_name = "stub"
    model_name = "chimera-deterministic-stub"

    def generate_structured(
        self,
        prompt: str,
        schema: type[Any],
        options: StructuredGenerationOptions | None = None,
    ) -> StructuredGenerationResult:
        digest = hashlib.sha256(prompt.strip().encode("utf-8")).hexdigest()[:8]
        payload = {
            "reply": (
                "Milestone 3 backend is wired. Future milestones will adapt this "
                f"interview from collected evidence. Stub trace: {digest}."
            ),
            "done": False,
        }
        try:
            if isinstance(schema, type) and issubclass(schema, BaseModel):
                validated = schema.model_validate(payload).model_dump()
            else:
                validated = payload
        except Exception as exc:
            raise ProviderError(
                "Stub provider could not validate structured output.",
                details={"schema": getattr(schema, "__name__", str(schema))},
            ) from exc
        return StructuredGenerationResult(
            data=validated,
            provider=self.provider_name,
            model=self.model_name,
            raw_text=str(payload),
        )
