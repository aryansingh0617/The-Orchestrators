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


def test_ai_service_evasion_detection() -> None:
    service = AIService(api_key="test_key")
    res = service.handle_chat_session(
        session_id="test-session-evasion",
        message="idk man whatever",
        candidate_info={"name": "Evasive Candidate"},
    )
    assert "does not answer" in res["reply"].lower() or "focus" in res["reply"].lower()


def test_ai_service_honest_evaluation_fail() -> None:
    service = AIService(api_key="test_key")
    evasive_history = [
        {"role": "user", "content": "idk"},
        {"role": "assistant", "content": "Please answer the technical question."},
        {"role": "user", "content": "whatever"},
    ]
    res = service.handle_chat_session(
        session_id="test-session-fail",
        message="Can I get my final evaluation feedback now?",
        chat_history=evasive_history,
        candidate_info={"name": "Weak Candidate"},
    )
    assert "NEEDS IMPROVEMENT" in res["reply"] or "FAIL" in res["reply"]
    assert "Weak Candidate" in res["reply"]


def test_api_interview_chat_endpoint_with_parts_history() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/interview/chat",
        json={
            "sessionId": "chat-session-parts",
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
    assert data["session_id"] == "chat-session-parts"
    assert "reply" in data
    assert data["status"] == "success"
