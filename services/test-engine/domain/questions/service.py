"""Filtrado de preguntas por bloque, tema, syllabus y examen."""

from __future__ import annotations

from domain.questions.models import Question


class QuestionService:
    """Orquesta filtros de catálogo. La persistencia vive en el repositorio."""

    def __init__(self, question_repository) -> None:
        self._questions = question_repository

    def list_by_filters(
        self,
        *,
        syllabus_id: str | None = None,
        block: str | None = None,
        topic: str | None = None,
        exam_id: int | None = None,
        pending_classification: bool | None = None,
    ) -> list[Question]:
        return self._questions.list_by_filters(
            syllabus_id=syllabus_id,
            block=block,
            topic=topic,
            exam_id=exam_id,
            pending_classification=pending_classification,
        )
