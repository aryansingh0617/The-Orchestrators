from unittest.mock import MagicMock, patch
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.main import app
from app.application.services.ai_service import AIService


def test_ai_service_live_execution_success() -> None:
    service = AIService(api_key="valid_api_key")
    mock_model = MagicMock()
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Live Gemini Technical Interviewer response for candidate evaluation."
    mock_chat.send_message.return_value = mock_response
    mock_model.start_chat.return_value = mock_chat
    service._model = mock_model

    res = service.handle_chat_session(
        session_id="test-session-live-1",
        message="I implemented hybrid search using BM25 and dense vectors to improve recall.",
        candidate_info={"name": "Test Candidate"},
    )
    assert res["session_id"] == "test-session-live-1"
    assert res["reply"] == "Live Gemini Technical Interviewer response for candidate evaluation."
    assert res["provider"] == "google-gemini"
    assert res["status"] == "success"


def test_ai_service_unconfigured_key_raises_http_500() -> None:
    service = AIService(api_key="your_api_key_here")
    with pytest.raises(HTTPException) as exc_info:
        service.handle_chat_session(
            session_id="test-unconfigured",
            message="Test message",
        )
    assert exc_info.value.status_code == 500
    assert "GEMINI_API_KEY is not configured" in exc_info.value.detail


def test_api_interview_chat_endpoint_live_flow() -> None:
    client = TestClient(app)
    with patch("app.application.services.ai_service.ai_service.handle_chat_session") as mock_handle:
        mock_handle.return_value = {
            "session_id": "chat-session-live-2",
            "reply": "Live Gemini Response",
            "provider": "google-gemini",
            "status": "success",
        }
        response = client.post(
            "/api/interview/chat",
            json={
                "sessionId": "chat-session-live-2",
                "message": "We adjusted the semantic cache similarity threshold to boost cache hits.",
                "chat_history": [
                    {"role": "user", "parts": ["How do you fix high query latency?"]},
                    {"role": "model", "parts": ["We can apply caching or indexing."]},
                ],
                "candidate_info": {"name": "Alex Turner"},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "chat-session-live-2"
        assert data["reply"] == "Live Gemini Response"
        assert data["status"] == "success"
