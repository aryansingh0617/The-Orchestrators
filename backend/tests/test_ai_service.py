from fastapi.testclient import TestClient
from app.main import app
from app.application.services.ai_service import AIService


def test_ai_service_initialization_and_live_contract() -> None:
    service = AIService(api_key="test_key")
    res = service.handle_chat_session(
        session_id="test-session-live-1",
        message="I implemented hybrid search using BM25 and dense vectors to improve recall.",
        candidate_info={"name": "Test Candidate"},
    )
    assert res["session_id"] == "test-session-live-1"
    assert "reply" in res
    assert res["status"] == "success"
    assert "provider" in res


def test_api_interview_chat_endpoint_live_flow() -> None:
    client = TestClient(app)
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
    assert "reply" in data
    assert data["status"] == "success"
