"""Modelos de dominio para enlaces entre preguntas y notas."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class QuestionNoteLink:
    question_id: int
    note_id: str
    syllabus_id: str
    source: str
    confidence: float | None = None
    id: int | None = None
    created_at: str | None = None


@dataclass
class NoteLinkResult:
    note_id: str
    title: str
    official_topic: str | None
    confidence: float | None


@dataclass
class QuestionLinkResult:
    question_id: int
    text_excerpt: str
    exam_name: str | None
    confidence: float | None
