from app.modules.world_state_engine import WorldStateEngine


def test_world_state_changes_with_caching_decision() -> None:
    engine = WorldStateEngine()
    world = engine.initialize(mission_title="Latency Incident", difficulty="intermediate")
    before_latency = world.system_state["latency_ms"]
    before_memory = world.system_state["memory_usage_pct"]

    updated = engine.transition(
        world,
        candidate_answer="I would add Redis caching in front of retrieval to cut latency.",
        evaluation_outcome="correct",
    )

    assert updated.version == world.version + 1
    assert updated.system_state["latency_ms"] < before_latency
    assert updated.system_state["memory_usage_pct"] > before_memory
    assert "caching" in updated.visible_summary.lower() or "Enabled caching" in str(
        updated.candidate_decisions
    )
