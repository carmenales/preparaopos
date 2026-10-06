"""Repositorio de exámenes oficiales."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from domain.exams.models import Exam, ExamQuestion
from infrastructure.db import orm_models as orm


class ExamRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, exam_id: int) -> Exam | None:
        row = self._session.scalar(
            select(orm.Exam)
            .options(selectinload(orm.Exam.questions))
            .where(orm.Exam.id == exam_id)
        )
        if row is None:
            return None
        return Exam(
            id=row.id,
            name=row.name,
            year=row.year,
            convocatoria=row.convocatoria,
            syllabus_id=row.syllabus_id,
            scoring_rule_id=row.scoring_rule_id,
            duration_seconds=row.duration_seconds,
            questions=[
                ExamQuestion(
                    question_id=eq.question_id,
                    position=eq.position,
                    is_reserve=eq.is_reserve,
                )
                for eq in row.questions
            ],
        )
