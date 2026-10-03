"""Repositorio de preguntas (SQLAlchemy)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from domain.questions.models import Option, Question as QuestionDTO, SyllabusTag
from infrastructure.db import orm_models as orm


class QuestionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_by_filters(
        self,
        *,
        syllabus_id: str | None = None,
        block: str | None = None,
        topic: str | None = None,
        exam_id: int | None = None,
        is_reserve: bool | None = None,
        pending_classification: bool | None = None,
    ) -> list[QuestionDTO]:
        stmt = select(orm.Question).options(
            selectinload(orm.Question.options),
            selectinload(orm.Question.tags),
        )

        if pending_classification is not None:
            stmt = stmt.where(orm.Question.pending_classification == pending_classification)

        if exam_id is not None:
            stmt = stmt.join(orm.ExamQuestion, orm.ExamQuestion.question_id == orm.Question.id).where(
                orm.ExamQuestion.exam_id == exam_id
            )
            if is_reserve is not None:
                stmt = stmt.where(orm.ExamQuestion.is_reserve == is_reserve)
            stmt = stmt.order_by(orm.ExamQuestion.position)

        if syllabus_id or block or topic:
            stmt = stmt.join(orm.QuestionSyllabusTag)
            if syllabus_id:
                stmt = stmt.where(orm.QuestionSyllabusTag.syllabus_id == syllabus_id)
            if block:
                stmt = stmt.where(orm.QuestionSyllabusTag.block == block)
            if topic:
                stmt = stmt.where(orm.QuestionSyllabusTag.topic == topic)

        rows = self._session.scalars(stmt).unique().all()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, question_id: int) -> QuestionDTO | None:
        stmt = (
            select(orm.Question)
            .options(
                selectinload(orm.Question.options),
                selectinload(orm.Question.tags),
            )
            .where(orm.Question.id == question_id)
        )
        row = self._session.scalar(stmt)
        return self._to_domain(row) if row else None

    def get_by_ids(self, question_ids: list[int]) -> dict[int, QuestionDTO]:
        if not question_ids:
            return {}
        stmt = (
            select(orm.Question)
            .options(
                selectinload(orm.Question.options),
                selectinload(orm.Question.tags),
            )
            .where(orm.Question.id.in_(question_ids))
        )
        rows = self._session.scalars(stmt).unique().all()
        return {row.id: self._to_domain(row) for row in rows}

    def count(self) -> int:
        from sqlalchemy import func

        return int(self._session.scalar(select(func.count()).select_from(orm.Question)) or 0)

    @staticmethod
    def _to_domain(row: orm.Question) -> QuestionDTO:
        return QuestionDTO(
            id=row.id,
            statement=row.statement,
            source=row.source,
            source_id=row.source_id,
            justification=row.justification,
            img_path=row.img_path,
            is_annulled=row.is_annulled,
            annulment_reason=row.annulment_reason,
            pending_classification=row.pending_classification,
            options=[
                Option(
                    id=opt.id,
                    text=opt.option_text,
                    is_correct=opt.is_correct,
                    display_order=opt.display_order,
                    justification=opt.justification,
                )
                for opt in row.options
            ],
            tags=[
                SyllabusTag(
                    syllabus_id=tag.syllabus_id,
                    block=tag.block,
                    topic=tag.topic,
                )
                for tag in row.tags
            ],
        )
