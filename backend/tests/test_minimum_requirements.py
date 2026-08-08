from fastapi.testclient import TestClient

STRONG = (
    "I would form a root-cause hypothesis from retrieval traces and metrics, "
    "compare latency and recall before/after the index refresh, avoid prompt-only fixes, "
    "add caching carefully while watching memory usage, define a canary rollback trigger, "
    "and measure p95 latency plus groundedness after release."
)
WEAK = "Just rewrite the prompt."


def test_minimum_requirements_are_enforced(client: TestClient) -> None:
    session_id = "min-req-001"
    start = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "candidate": {
                "member": {
                    "id": "CAND-MIN",
                    "name": "Sam Patel",
                    "jobRole": "AI Engineer",
                    "yearsExperience": 4,
                },
                "missions": [],
                "signals": {"commitDays": 10, "missionsCompleted": 8, "missionsFirstTry": 6},
            },
        },
    ).json()

    assert start["done"] is False
    assert start["mission"] is not None
    assert start["competency"]
    assert start["world_state"] is not None

    modes: set[str] = set()
    days: set[int] = set()
    saw_follow_up = False
    world_versions: list[int] = []
    final = None

    if start.get("curriculum_day") is not None:
        days.add(int(start["curriculum_day"]))
    if start.get("world_state"):
        world_versions.append(int(start["world_state"]["version"]))

    for i in range(16):
        answer = WEAK if i in {0, 3, 6} else STRONG
        body = client.post(
            "/api/interview",
            json={"sessionId": session_id, "message": answer},
        ).json()
        modes.add(body.get("mode") or "")
        if body.get("curriculum_day") is not None:
            days.add(int(body["curriculum_day"]))
        if body.get("mode") in {"follow_up", "deepen", "revisit_gap"}:
            saw_follow_up = True
        if body.get("world_state"):
            world_versions.append(int(body["world_state"]["version"]))
        if body.get("progress"):
            assert body["progress"]["minimum_questions"] == 8
            assert body["progress"]["minimum_curriculum_days"] == 4
        if body["done"]:
            final = body
            break

    assert final is not None, "Interview must complete"
    assert final["feedback"] is not None
    assert final["feedback"]["summary"]
    assert final["feedback"]["strengths"]
    assert final["feedback"]["gaps"]
    assert final["feedback"]["next"]
    assert final["progress"]["question_number"] >= 8
    assert final["progress"]["curriculum_days_covered"] >= 4
    assert len(days) >= 4
    assert saw_follow_up, "Expected at least one adaptive follow-up/deepen/revisit"
    assert max(world_versions) > min(world_versions), "World state must evolve"
    assert "hidden_evaluation_criteria" not in str(final).lower()
    assert "chain-of-thought" not in str(final).lower()
