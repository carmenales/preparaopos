"""Repositorio de sesiones e intentos (SQLAlchemy)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from domain.sessions.models import TestAttempt, TestSession
from infrastructure.db import orm_models as orm


def _ensure_utc(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


class SessionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save_session(self, test_session: TestSession) -> None:
        """Crea o actualiza una sesión de test en la BD."""
        row = self._session.get(orm.TestSession, test_session.id)
        if row is None:
            row = orm.TestSession(
                id=test_session.id,
                mode=test_session.mode,
                source=test_session.source,
                source_ref=test_session.source_ref,
                question_ids=json.dumps(test_session.question_ids),
                started_at=test_session.started_at,
                duration_seconds=test_session.duration_seconds,
                closed_at=test_session.closed_at,
                finished_at=test_session.closed_at,
                final_score=test_session.final_score,
                scoring_rule_id=test_session.scoring_rule_id,
                exam_id=test_session.exam_id,
                status=test_session.status,
                instant_feedback=test_session.instant_feedback,
                timer_elapsed_seconds=test_session.timer_elapsed_seconds,
                timer_running_since=test_session.timer_running_since,
                training=test_session.training,
                question_filter=json.dumps(test_session.question_filter) if test_session.question_filter else None,
            )
            self._session.add(row)
        else:
            row.mode = test_session.mode
            row.source = test_session.source
            row.source_ref = test_session.source_ref
            row.question_ids = json.dumps(test_session.question_ids)
            row.started_at = test_session.started_at
            row.duration_seconds = test_session.duration_seconds
            row.closed_at = test_session.closed_at
            row.finished_at = test_session.closed_at
            row.final_score = test_session.final_score
            row.scoring_rule_id = test_session.scoring_rule_id
            row.exam_id = test_session.exam_id
            row.status = test_session.status
            row.instant_feedback = test_session.instant_feedback
            row.timer_elapsed_seconds = test_session.timer_elapsed_seconds
            row.timer_running_since = test_session.timer_running_since
            row.training = test_session.training
            row.question_filter = json.dumps(test_session.question_filter) if test_session.question_filter else None
        self._session.commit()

    def get_by_id(self, session_id: str) -> TestSession | None:
        row = self._session.scalar(
            select(orm.TestSession)
            .options(selectinload(orm.TestSession.attempts))
            .where(orm.TestSession.id == session_id)
        )
        if row is None:
            return None
        return self._to_domain(row)

    def list_all(self, limit: int = 50) -> list[TestSession]:
        rows = self._session.scalars(
            select(orm.TestSession)
            .options(selectinload(orm.TestSession.attempts))
            .order_by(orm.TestSession.started_at.desc())
            .limit(limit)
        ).all()
        return [self._to_domain(row) for row in rows]

    def save_attempt(self, attempt: TestAttempt) -> None:
        """Inserta o actualiza un intento de respuesta por (test_session_id, question_id)."""
        existing = self._session.scalar(
            select(orm.TestAttempt).where(
                orm.TestAttempt.test_session_id == attempt.session_id,
                orm.TestAttempt.question_id == attempt.question_id,
            )
        )
        marked = json.dumps(attempt.marked_option_ids) if len(attempt.marked_option_ids) > 1 else None
        if existing is not None:
            existing.selected_option_id = attempt.selected_option_id
            existing.is_correct = attempt.is_correct
            existing.answered_at = attempt.answered_at
            existing.marked_option_ids = marked
        else:
            new_att = orm.TestAttempt(
                test_session_id=attempt.session_id,
                question_id=attempt.question_id,
                selected_option_id=attempt.selected_option_id,
                is_correct=attempt.is_correct,
                answered_at=attempt.answered_at,
                marked_option_ids=marked,
            )
            self._session.add(new_att)
        self._session.commit()

    def delete_attempt(self, session_id: str, question_id: int) -> bool:
        """Quita la respuesta de una pregunta (vuelve a estar sin contestar). Devuelve si había."""
        result = self._session.execute(delete(orm.TestAttempt).where(
            orm.TestAttempt.test_session_id == session_id, orm.TestAttempt.question_id == question_id))
        self._session.commit()
        return result.rowcount > 0

    @staticmethod
    def _to_domain(row: orm.TestSession) -> TestSession:
        q_ids = []
        if row.question_ids:
            try:
                q_ids = json.loads(row.question_ids)
            except Exception:
                q_ids = []

        return TestSession(
            id=row.id,
            mode=row.mode,
            source=row.source,
            source_ref=row.source_ref,
            question_ids=q_ids,
            started_at=_ensure_utc(row.started_at),
            duration_seconds=row.duration_seconds,
            closed_at=_ensure_utc(row.closed_at or row.finished_at),
            final_score=row.final_score,
            scoring_rule_id=row.scoring_rule_id,
            exam_id=row.exam_id,
            status=row.status,
            instant_feedback=row.instant_feedback,
            timer_elapsed_seconds=row.timer_elapsed_seconds,
            timer_running_since=_ensure_utc(row.timer_running_since),
            training=row.training,
            question_filter=json.loads(row.question_filter) if row.question_filter else None,
            attempts=[
                TestAttempt(
                    id=att.id,
                    session_id=att.test_session_id,
                    question_id=att.question_id,
                    selected_option_id=att.selected_option_id,
                    is_correct=att.is_correct,
                    answered_at=_ensure_utc(att.answered_at) or datetime.now(timezone.utc),
                    marked_option_ids=json.loads(att.marked_option_ids) if att.marked_option_ids else [],
                )
                for att in row.attempts
            ],
        )
