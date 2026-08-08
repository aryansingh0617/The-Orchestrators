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
    body = response.json()
    assert body["done"] is False
    assert body["feedback"] is None
    assert "Welcome" in body["reply"]
    assert "Mission:" in body["reply"]


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
            "message": (
                "I would inspect retrieval logs and traces before changing prompts, "
                "compare recall metrics, and consider a rollback if quality drops."
            ),
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["done"] is False
    assert body["feedback"] is None
    assert "Mission:" in body["reply"] or "Follow-up" in body["reply"] or "System state" in body["reply"]


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


def test_interview_empty_message_rejected(client: TestClient) -> None:
    client.post(
        "/api/interview",
        json={
            "sessionId": "empty-msg",
            "candidate": {"member": {"id": "CAND-1"}, "missions": [], "signals": {}},
        },
    )
    response = client.post(
        "/api/interview",
        json={"sessionId": "empty-msg", "message": "   "},
    )
    assert response.status_code == 400
