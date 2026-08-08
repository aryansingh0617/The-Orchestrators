from fastapi.testclient import TestClient


def test_interview_start_contract(client: TestClient) -> None:
    response = client.post(
        "/api/interview",
        json={
            "sessionId": "abc-123",
            "candidate": {
                "member": {
                    "id": "CAND-003",
                    "name": "Emily Chen",
                    "jobRole": "AI Engineer",
                    "yearsExperience": 6,
                    "education": "MS Artificial Intelligence",
                    "status": "COMPLETED",
                },
                "missions": [],
                "signals": {
                    "commitDays": 31,
                    "missionsCompleted": 31,
                    "missionsFirstTry": 30,
                },
            },
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "reply": "Welcome. Let's begin your interview.",
        "done": False,
        "feedback": None,
    }


def test_interview_turn_contract_after_start(client: TestClient) -> None:
    client.post(
        "/api/interview",
        json={
            "sessionId": "abc-123",
            "candidate": {"member": {"id": "CAND-003"}, "missions": [], "signals": {}},
        },
    )

    response = client.post(
        "/api/interview",
        json={
            "sessionId": "abc-123",
            "message": "I would inspect retrieval logs before changing prompts.",
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["done"] is False
    assert body["feedback"] is None
    assert "Milestone 3 backend is wired." in body["reply"]


def test_interview_requires_candidate_for_unknown_session(client: TestClient) -> None:
    response = client.post(
        "/api/interview",
        json={"sessionId": "missing-session", "message": "Hello"},
        headers={"X-Request-ID": "trace-test"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "not_found",
            "message": "Start the interview with candidate data before sending messages.",
            "details": {"sessionId": "missing-session"},
            "trace_id": "trace-test",
        }
    }
