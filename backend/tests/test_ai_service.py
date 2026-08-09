from fastapi.testclient import TestClient
from app.main import app
from app.application.services.ai_service import AIService


def test_ai_service_initialization_and_fallback() -> None:
    service = AIService(api_key="test_key")
    res = service.handle_chat_session(
        session_id="test-session-101",
        message="I implemented hybrid search using BM25 and dense vectors to improve recall.",
        candidate_info={"name": "Test Candidate"},
    )
    assert res["session_id"] == "test-session-101"
    assert "reply" in res
    assert res["status"] == "success"
    assert "bm25" in res["reply"].lower() or "hybrid" in res["reply"].lower() or "reciprocity" in res["reply"].lower()


def test_ai_service_feedback_generation() -> None:
    service = AIService(api_key="test_key")
    res = service.handle_chat_session(
        session_id="test-session-102",
        message="Can you provide my final interview feedback and conclude the session?",
        candidate_info={"name": "Sarah Johnson"},
    )
    assert "Strengths" in res["reply"] or "Feedback" in res["reply"]
    assert "Sarah Johnson" in res["reply"] or "Candidate" in res["reply"]


def test_api_interview_chat_endpoint() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/interview/chat",
        json={
            "sessionId": "chat-session-999",
            "message": "We adjusted the semantic cache similarity threshold to boost cache hits.",
            "candidate_info": {"name": "Alex Turner"},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "chat-session-999"
    assert "reply" in data
    assert data["status"] == "success"
    assert "provider" in data
