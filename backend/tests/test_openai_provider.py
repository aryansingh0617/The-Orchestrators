import json

import httpx
import pytest
from pydantic import BaseModel, Field

from app.core.settings import Settings
from app.domain.errors import ProviderError
from app.infrastructure.ai.openai_provider import OpenAIProvider


class TinySchema(BaseModel):
    answer: str = Field(default="ok")


def test_openai_provider_requires_api_key() -> None:
    with pytest.raises(ProviderError):
        OpenAIProvider(api_key="")


def test_openai_provider_structured_success(monkeypatch) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer test-key"
        body = json.loads(request.content.decode("utf-8"))
        assert body["model"] == "gpt-4o-mini"
        assert "api_key" not in body
        return httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"content": json.dumps({"answer": "structured"})}}
                ]
            },
        )

    transport = httpx.MockTransport(handler)

    class FakeClient(httpx.Client):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)

    monkeypatch.setattr("app.infrastructure.ai.openai_provider.httpx.Client", FakeClient)
    provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini", max_retries=0)
    result = provider.generate_structured("return json", TinySchema)
    assert result.provider == "openai"
    assert result.data["answer"] == "structured"


def test_openai_provider_maps_timeout(monkeypatch) -> None:
    class TimeoutClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def post(self, *args, **kwargs):
            raise httpx.TimeoutException("timeout")

    monkeypatch.setattr("app.infrastructure.ai.openai_provider.httpx.Client", TimeoutClient)
    provider = OpenAIProvider(api_key="test-key", max_retries=0)
    with pytest.raises(ProviderError, match="timed out"):
        provider.generate_structured("x", TinySchema)


def test_settings_support_openai_provider_config(monkeypatch) -> None:
    monkeypatch.setenv("CHIMERA_AI_PROVIDER", "openai")
    monkeypatch.setenv("CHIMERA_OPENAI_MODEL", "gpt-4o")
    settings = Settings()
    assert settings.ai_provider == "openai"
    assert settings.openai_model == "gpt-4o"
