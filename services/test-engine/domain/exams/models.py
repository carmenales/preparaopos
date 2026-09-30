"""Modelos de dominio de exámenes oficiales."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExamQuestion:
    question_id: int
    position: int


@dataclass
class Exam:
    id: int | None
    name: str
    year: int | None
    convocatoria: str | None
    syllabus_id: str | None = None
    scoring_rule_id: int | None = None
    duration_seconds: int | None = None
    questions: list[ExamQuestion] = field(default_factory=list)
