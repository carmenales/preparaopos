"""Repositorio de sesiones e intentos."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from domain.sessions.models import TestAttempt, TestSession
from infrastructure.db import orm_models as orm


class SessionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, session_id: str) -> TestSession | None:
        row = self._session.scalar(
            select(orm.TestSession)
            .options(selectinload(orm.TestSession.attempts))
            .where(orm.TestSession.id == session_id)
        )
        if row is None:
            return None
        return TestSession(
            id=row.id,
            started_at=row.started_at,
            duration_seconds=row.duration_seconds,
            finished_at=row.finished_at,
            mode=row.mode,
            status=row.status,
            scoring_rule_id=row.scoring_rule_id,
            exam_id=row.exam_id,
            attempts=[
                TestAttempt(
                    id=att.id,
                    test_session_id=att.test_session_id,
                    question_id=att.question_id,
                    selected_option_id=att.selected_option_id,
                    is_correct=att.is_correct,
                    answered_at=att.answered_at,
                )
                for att in row.attempts
            ],
        )
