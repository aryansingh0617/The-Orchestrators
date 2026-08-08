from fastapi import FastAPI

from app.main import app, create_app


def test_app_imports() -> None:
    assert isinstance(app, FastAPI)


def test_create_app_has_expected_metadata() -> None:
    created = create_app()
    assert created.title == "Project Chimera API"
    assert created.version == "0.1.0"
