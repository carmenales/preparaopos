"""Modelos de dominio de sesión de test e intentos."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TestAttempt:
    id: int | None
    test_session_id: str
    question_id: int
    selected_option_id: int | None
    is_correct: bool | None
    answered_at: datetime | None


@dataclass
class TestSession:
    id: str
    started_at: datetime
    duration_seconds: int | None
    finished_at: datetime | None
    mode: str
    status: str
    scoring_rule_id: int | None = None
    exam_id: int | None = None
    attempts: list[TestAttempt] = field(default_factory=list)
