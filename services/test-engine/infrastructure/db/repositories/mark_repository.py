"""Marcas del usuario sobre preguntas («dudosa»), comunes a todos sus tests."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.db import orm_models as orm


class MarkRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def doubtful_ids(self, question_ids: list[int] | None = None) -> set[int]:
        stmt = select(orm.QuestionMark.question_id).where(orm.QuestionMark.doubtful.is_(True))
        if question_ids is not None:
            if not question_ids:
                return set()
            stmt = stmt.where(orm.QuestionMark.question_id.in_(question_ids))
        return set(self._session.scalars(stmt))

    def set_doubtful(self, question_id: int, doubtful: bool) -> None:
        row = self._session.get(orm.QuestionMark, question_id)
        now = datetime.now(timezone.utc)
        if row is None:
            if doubtful:
                self._session.add(orm.QuestionMark(question_id=question_id, doubtful=True, marked_at=now))
        else:
            row.doubtful = doubtful
            row.marked_at = now
        self._session.commit()

    def toggle_doubtful(self, question_id: int) -> bool:
        """Cambia la marca y devuelve cómo queda."""
        marked = question_id not in self.doubtful_ids([question_id])
        self.set_doubtful(question_id, marked)
        return marked
