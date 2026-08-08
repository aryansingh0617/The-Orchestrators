from app.application.dtos import InterviewResult
from app.domain.interfaces import StructuredGenerationOptions
from app.infrastructure.ai import StubProvider


def test_stub_provider_is_deterministic() -> None:
    provider = StubProvider()

    first = provider.generate_structured(
        prompt="inspect retrieval logs",
        schema=InterviewResult,
        options=StructuredGenerationOptions(),
    )
    second = provider.generate_structured(
        prompt="inspect retrieval logs",
        schema=InterviewResult,
        options=StructuredGenerationOptions(),
    )

    assert first == second
    assert first.provider == "stub"
    assert first.model == "chimera-deterministic-stub"


def test_stub_provider_returns_schema_valid_output() -> None:
    result = StubProvider().generate_structured(
        prompt="anything",
        schema=InterviewResult,
    )

    parsed = InterviewResult.model_validate(result.data)
    assert parsed.done is False
    assert "Milestone 3 backend is wired." in parsed.reply
