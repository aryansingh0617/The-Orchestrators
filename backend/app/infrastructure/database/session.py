from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import Settings, get_settings


def create_db_engine(db_url: str | None = None):
    url = db_url or get_settings().database_url
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args)


def get_session_factory(db_url: str | None = None) -> sessionmaker[Session]:
    engine = create_db_engine(db_url)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session(settings: Settings | None = None) -> Generator[Session, None, None]:
    s = settings or get_settings()
    session_factory = get_session_factory(s.database_url)
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
