from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


def test_alembic_upgrade_creates_schema(tmp_path: Path) -> None:
    db_path = tmp_path / "migrate.db"
    backend_root = Path(__file__).resolve().parents[1]
    ini = backend_root / "alembic.ini"
    cfg = Config(str(ini))
    cfg.set_main_option("script_location", str(backend_root / "migrations"))
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path.as_posix()}")

    command.upgrade(cfg, "head")

    engine = create_engine(f"sqlite:///{db_path.as_posix()}")
    tables = set(inspect(engine).get_table_names())
    expected = {
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
        "alembic_version",
    }
    assert expected.issubset(tables)
