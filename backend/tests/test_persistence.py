from datetime import UTC, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as DbSession

from app.domain.entities.assessment import AssessmentSession, SessionStatus
from app.infrastructure.database.base import Base
from app.infrastructure.database.models import (
    AssessmentSessionModel,
    EvidenceItemModel,
)
from app.infrastructure.repositories.sql_session_repository import SqlSessionRepository


def test_schema_creation() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    tables = Base.metadata.tables
    expected_tables = {
        "candidates",
        "assessment_sessions",
        "competency_targets",
        "mission_plans",
        "missions",
        "turns",
        "world_state_snapshots",
        "evidence_items",
        "memory_records",
        "evaluations",
        "reports",
        "provider_events",
    }
    assert expected_tables.issubset(set(tables.keys()))


def test_sql_session_repository_save_and_get() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with DbSession(engine) as db:
        repo = SqlSessionRepository(db)
        now = datetime.now(UTC)
        session = AssessmentSession(
            id="sql-id-1",
            external_session_id="ext-sql-001",
            candidate_id="cand-001",
            role_title="AI Systems Engineer",
            seniority="senior",
            status=SessionStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

        saved = repo.save(session)
        assert saved.external_session_id == "ext-sql-001"
        assert saved.role_title == "AI Systems Engineer"

        fetched = repo.get_by_external_id("ext-sql-001")
        assert fetched is not None
        assert fetched.id == "sql-id-1"
        assert fetched.status == SessionStatus.ACTIVE


def test_models_json_field_storage() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with DbSession(engine) as db:
        session_model = AssessmentSessionModel(
            id="s1",
            external_session_id="ext-1",
            role_title="AI Engineer",
            seniority="mid",
            status="active",
        )
        db.add(session_model)
        db.commit()

        evidence_model = EvidenceItemModel(
            id="e1",
            session_id="s1",
            competency="Retrieval Systems",
            observation="Identified chunk size mismatch",
            polarity="positive",
            strength=4,
            confidence=0.9,
            rationale="Analyzed index settings first",
        )
        db.add(evidence_model)
        db.commit()

        fetched = db.query(EvidenceItemModel).filter_by(id="e1").first()
        assert fetched is not None
        assert fetched.competency == "Retrieval Systems"
        assert fetched.confidence == 0.9


def test_sql_repositories_crud() -> None:
    from app.domain.entities import (
        Candidate,
        CandidateTurn,
        Evaluation,
        Evidence,
        MemoryRecord,
        Mission,
        WorldState,
    )
    from app.domain.entities.assessment import EvidencePolarity
    from app.infrastructure.repositories import (
        SqlCandidateRepository,
        SqlEvaluationRepository,
        SqlEvidenceRepository,
        SqlMemoryRepository,
        SqlMissionRepository,
        SqlSessionRepository,
        SqlTurnRepository,
        SqlWorldStateRepository,
    )

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with DbSession(engine) as db:
        session_repo = SqlSessionRepository(db)
        cand_repo = SqlCandidateRepository(db)
        turn_repo = SqlTurnRepository(db)
        evidence_repo = SqlEvidenceRepository(db)
        memory_repo = SqlMemoryRepository(db)
        eval_repo = SqlEvaluationRepository(db)
        world_repo = SqlWorldStateRepository(db)
        mission_repo = SqlMissionRepository(db)

        now = datetime.now(UTC)
        candidate = Candidate(
            id="c1",
            display_name="John Doe",
            email="john@doe.com",
            profile_summary="Senior ML Engineer",
            created_at=now,
            updated_at=now,
        )
        cand_repo.save(candidate)
        assert cand_repo.get_by_id("c1").display_name == "John Doe"

        session = AssessmentSession(
            id="s1",
            external_session_id="ext-s1",
            candidate_id="c1",
            role_title="AI Engineer",
            seniority="mid",
            status=SessionStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        session_repo.save(session)

        mission = Mission(
            id="m1",
            session_id="s1",
            title="Design a Vector DB",
            scenario="Design vector DB for 1B items",
            competency_targets=("RAG Architecture",),
            difficulty=4,
        )
        mission_repo.save(mission)
        assert len(mission_repo.get_missions_for_session("s1")) == 1

        turn = CandidateTurn(
            id="t1",
            session_id="s1",
            sequence_number=1,
            prompt_text="Describe vector indexing",
            candidate_response="I would use HNSW",
            created_at=now,
            mission_id="m1",
        )
        turn_repo.save(turn)
        assert len(turn_repo.get_turns_for_session("s1")) == 1

        evidence = Evidence(
            id="e1",
            session_id="s1",
            turn_id="t1",
            competency="RAG Architecture",
            observation="Observed understanding of HNSW graph indexing",
            polarity=EvidencePolarity.POSITIVE,
            strength=4,
            confidence=0.95,
            rationale="Specifically mentioned graph density trades",
        )
        evidence_repo.save(evidence)
        assert len(evidence_repo.get_evidence_for_session("s1")) == 1

        memory = MemoryRecord(
            id="mem1",
            session_id="s1",
            memory_type="pattern",
            summary="Candidate favors graph index over quant",
            evidence_ids=("e1",),
            confidence=0.8,
        )
        memory_repo.save(memory)
        assert len(memory_repo.get_memory_for_session("s1")) == 1

        evaluation = Evaluation(
            id="eval1",
            session_id="s1",
            competency="RAG Architecture",
            score=4.0,
            confidence=0.9,
            evidence_ids=("e1",),
            rationale="Proven deep understanding of graph density trades",
            improvement_guidance="Focus on cost calculations for 1B vectors",
        )
        eval_repo.save(evaluation)
        assert len(eval_repo.get_evaluations_for_session("s1")) == 1

        world = WorldState(
            id="w1",
            session_id="s1",
            state={"index_type": "HNSW", "recall": 0.95},
            visible_summary="System running with HNSW index.",
            version=1,
        )
        world_repo.save(world)
        assert world_repo.get_latest_for_session("s1").version == 1

