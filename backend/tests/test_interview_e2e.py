from fastapi.testclient import TestClient

STRONG_ANSWER = (
    "I would form a root-cause hypothesis from retrieval traces and metrics, "
    "compare latency and recall before/after the index refresh, avoid prompt-only fixes, "
    "add caching carefully while watching memory usage, define a canary rollback trigger, "
    "and measure p95 latency plus groundedness after release."
)

WEAK_ANSWER = "Just rewrite the prompt."


def test_full_adaptive_interview_reaches_feedback(client: TestClient) -> None:
    session_id = "e2e-adaptive-001"
    start = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "candidate": {
                "member": {
                    "id": "CAND-E2E",
                    "name": "Alex Rivera",
                    "jobRole": "AI Engineer",
                    "yearsExperience": 5,
                },
                "missions": [
                    {"day": 1, "title": "RAG", "passed": True, "attempts": 1},
                    {"day": 7, "title": "Agents", "skipped": True, "attempts": 0},
                ],
                "signals": {"commitDays": 20, "missionsCompleted": 12, "missionsFirstTry": 10},
            },
        },
    )
    assert start.status_code == 200
    assert start.json()["done"] is False

    days_seen: set[int] = set()
    modes_seen: set[str] = set()
    final = None

    for i in range(14):
        answer = STRONG_ANSWER if i % 3 else WEAK_ANSWER
        response = client.post(
            "/api/interview",
            json={"sessionId": session_id, "message": answer},
        )
        assert response.status_code == 200
        body = response.json()
        reply = body["reply"]
        for token in reply.split():
            if token.isdigit():
                pass
        if "Curriculum Day" in reply:
            # Extract day numbers mentioned after 'Curriculum Day'
            import re

            found = re.findall(r"Curriculum Day\s+(\d+)", reply)
            days_seen.update(int(x) for x in found)
        if "Follow-up:" in reply:
            modes_seen.add("follow_up")
        if "Gap Revisit:" in reply:
            modes_seen.add("revisit_gap")
        if body["done"]:
            final = body
            break

    assert final is not None, "Interview did not complete within turn budget"
    assert final["done"] is True
    assert final["feedback"] is not None
    assert final["feedback"]["summary"]
    assert final["feedback"]["strengths"]
    assert final["feedback"]["gaps"]
    assert final["feedback"]["next"]
    assert len(days_seen) >= 4
