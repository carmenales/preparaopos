"""Inyección de dependencias FastAPI para la capa de presentación."""

from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from config import SQLITE_PATH
from infrastructure.clients.linking_client import LinkingClient
from infrastructure.clients.notes_catalog_client import NotesCatalogClient
from infrastructure.db.engine import create_sqlite_engine
from infrastructure.db.repositories.exam_repository import ExamRepository
from infrastructure.db.repositories.question_repository import QuestionRepository
from infrastructure.db.repositories.scoring_rule_repository import ScoringRuleRepository
from infrastructure.db.repositories.session_repository import SessionRepository
from infrastructure.db.repositories.stats_repository import StatsRepository
from domain.scoring.service import ScoringService
from domain.sessions.service import TestSessionService


@lru_cache(maxsize=1)
def _engine():
    return create_sqlite_engine(SQLITE_PATH)


def get_db():
    SessionLocal = sessionmaker(bind=_engine(), autoflush=False, future=True)
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


DbDep = Annotated[Session, Depends(get_db)]


def get_question_repo(db: DbDep) -> QuestionRepository:
    return QuestionRepository(db)


QuestionRepoDep = Annotated[QuestionRepository, Depends(get_question_repo)]


def get_stats_repo(db: DbDep) -> StatsRepository:
    return StatsRepository(db)


StatsRepoDep = Annotated[StatsRepository, Depends(get_stats_repo)]


def get_session_service(db: DbDep) -> TestSessionService:
    return TestSessionService(
        session_repository=SessionRepository(db),
        question_repository=QuestionRepository(db),
        scoring_service=ScoringService(),
        exam_repository=ExamRepository(db),
        scoring_rule_repository=ScoringRuleRepository(db),
    )


SessionServiceDep = Annotated[TestSessionService, Depends(get_session_service)]


@lru_cache(maxsize=1)
def get_linking_client() -> LinkingClient:
    return LinkingClient()


LinkingClientDep = Annotated[LinkingClient, Depends(get_linking_client)]


@lru_cache(maxsize=1)
def get_notes_catalog_client() -> NotesCatalogClient:
    return NotesCatalogClient()


NotesCatalogDep = Annotated[NotesCatalogClient, Depends(get_notes_catalog_client)]

