from app.modules.world_state_engine import WorldStateEngine
from app.modules.world_state_engine.rag_mitigation import RAGIncidentMitigator


def test_rag_mitigator_sla_targets() -> None:
    state = dict(RAGIncidentMitigator.INITIAL_STATE)
    assert state["error_rate_pct"] == 2.4
    assert state["recall_score"] == 0.71
    assert state["cache_hit_pct"] == 62
    assert not RAGIncidentMitigator.is_incident_resolved(state)

    # 1. Apply Error Rate Mitigation (Retry + Exponential Backoff + Graceful Fallback)
    RAGIncidentMitigator.apply_error_rate_mitigation(state)
    assert state["error_rate_pct"] < 0.5
    assert state["error_rate_pct"] == 0.3

    # 2. Apply Recall Mitigation (Hybrid Search + BM25 + Dense Embeddings)
    RAGIncidentMitigator.apply_recall_mitigation(state)
    assert state["recall_score"] > 0.85
    assert state["recall_score"] == 0.88

    # 3. Apply Cache Hit Mitigation (Adjust Similarity Threshold)
    RAGIncidentMitigator.apply_cache_mitigation(state)
    assert state["cache_hit_pct"] > 75
    assert state["cache_hit_pct"] == 78

    assert RAGIncidentMitigator.is_incident_resolved(state)


def test_world_state_engine_rag_incident_transitions() -> None:
    engine = WorldStateEngine()
    world = engine.initialize(mission_title="RAG Production Incident", difficulty="advanced")

    # Candidate answer implementing retry with exponential backoff & fallback
    updated_1 = engine.transition(
        world,
        candidate_answer="Implement retry logic with exponential backoff for Vector DB and LLM calls with graceful fallback.",
        evaluation_outcome="strong",
    )
    assert updated_1.system_state["error_rate_pct"] < 0.5

    # Candidate answer implementing Hybrid Search with BM25
    updated_2 = engine.transition(
        updated_1,
        candidate_answer="Update retrieval pipeline to Hybrid Search combining dense vector embeddings and BM25 sparse search.",
        evaluation_outcome="strong",
    )
    assert updated_2.system_state["recall_score"] > 0.85

    # Candidate answer lowering semantic cache similarity threshold
    updated_3 = engine.transition(
        updated_2,
        candidate_answer="Adjust semantic cache configuration by lowering the similarity threshold to capture identical queries.",
        evaluation_outcome="strong",
    )
    assert updated_3.system_state["cache_hit_pct"] > 75

    # Confirm incident resolution
    assert RAGIncidentMitigator.is_incident_resolved(updated_3.system_state)
