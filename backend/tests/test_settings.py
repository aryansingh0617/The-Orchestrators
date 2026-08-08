from app.core.settings import Settings


def test_settings_have_safe_development_defaults() -> None:
    settings = Settings()

    assert settings.ai_provider == "stub"
    assert settings.openai_api_key is None
    assert settings.database_url == "sqlite:///./local.db"


def test_settings_load_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("CHIMERA_ENVIRONMENT", "test")
    monkeypatch.setenv("CHIMERA_APP_NAME", "Test Chimera")

    settings = Settings()

    assert settings.environment == "test"
    assert settings.app_name == "Test Chimera"
