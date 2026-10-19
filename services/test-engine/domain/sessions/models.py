"""Modelos de dominio de sesión de test e intentos (sin SQLAlchemy)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Literal


@dataclass
class TestAttempt:
    session_id: str
    question_id: int
    selected_option_id: int | None  # None = en blanco
    answered_at: datetime
    id: int | None = None
    is_correct: bool | None = None


@dataclass
class TestSession:
    id: str
    mode: Literal["practice", "exam"]
    source: Literal["block", "exam", "random", "questions", "note"]
    source_ref: str | None  # código de bloque/tema, o exam_id — según 'source'
    question_ids: list[int]  # orden fijado al crear la sesión, no se recalcula después
    started_at: datetime
    duration_seconds: int | None  # solo en modo 'exam'; None = sin límite (modo práctica)
    closed_at: datetime | None = None
    final_score: Decimal | None = None
    scoring_rule_id: int | None = None
    exam_id: int | None = None
    status: str = "open"
    attempts: list[TestAttempt] = field(default_factory=list)


@dataclass
class AnswerResult:
    session_id: str
    question_id: int
    selected_option_id: int | None
    is_saved: bool = True
    # Solo en modo práctica (en modo examen permanecen None hasta cerrar la sesión):
    is_correct: bool | None = None
    correct_option_id: int | None = None
    explanation: str | None = None


@dataclass
class QuestionResult:
    question_id: int
    selected_option_id: int | None
    correct_option_id: int | None
    is_correct: bool | None  # True = acierto, False = fallo, None = en blanco
    is_blank: bool
    explanation: str | None


@dataclass
class SessionResult:
    session_id: str
    mode: str
    final_score: Decimal | None
    correct_count: int
    wrong_count: int
    blank_count: int
    annulled_count: int
    total_evaluable: int
    questions: list[QuestionResult]
