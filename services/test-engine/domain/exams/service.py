"""Generación de simulacro oficial a partir de un examen catalogado."""

from __future__ import annotations

from domain.exams.models import Exam


class ExamService:
    def __init__(self, exam_repository) -> None:
        self._exams = exam_repository

    def get_exam(self, exam_id: int) -> Exam | None:
        return self._exams.get_by_id(exam_id)
