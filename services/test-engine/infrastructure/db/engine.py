"""Motor SQLite (journal_mode configurable, WAL por defecto) y fábrica de sesiones SQLAlchemy."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, event, func, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

import logging
import os

from infrastructure.db.orm_models import Base, Question, ScoringRule, Syllabus
from infrastructure.db.seed import SEED_SCORING_RULES, SEED_SYLLABI

logger = logging.getLogger(__name__)


def sqlite_url(path: Path) -> str:
    return f"sqlite:///{path.as_posix()}"


def create_sqlite_engine(path: Path, journal_mode: str | None = None) -> Engine:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = (journal_mode or os.getenv("SQLITE_JOURNAL_MODE", "WAL")).upper()
    engine = create_engine(
        sqlite_url(path),
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def _enable_sqlite_pragmas(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute(f"PRAGMA journal_mode={mode}")
            row = cursor.fetchone()
            effective = str(row[0]).upper() if row else None
            if effective != mode:
                logger.warning(
                    "SQLite %s: journal_mode pedido=%s, efectivo=%s", path, mode, effective
                )
        except Exception as exc:
            logger.warning(
                "SQLite %s: no se pudo aplicar journal_mode=%s (%s)", path, mode, exc
            )
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def create_memory_engine() -> Engine:
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def _enable_sqlite_pragmas(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def seed_master_data(session: Session) -> None:
    for row in SEED_SYLLABI:
        if session.get(Syllabus, row["id"]) is None:
            session.add(Syllabus(**row))

    for row in SEED_SCORING_RULES:
        exists = session.scalar(select(ScoringRule).where(ScoringRule.code == row["code"]))
        if exists is None:
            session.add(ScoringRule(**row))

    session.commit()


def init_schema(engine: Engine) -> None:
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)
    with SessionLocal() as session:
        seed_master_data(session)


def count_questions(session: Session) -> int:
    return int(session.scalar(select(func.count()).select_from(Question)) or 0)


@contextmanager
def session_scope(engine: Engine) -> Generator[Session, None, None]:
    SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def wal_mode(engine: Engine) -> str | None:
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA journal_mode")).scalar()
        return str(result) if result is not None else None
