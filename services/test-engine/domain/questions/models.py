"""Modelos de dominio de preguntas y etiquetas de temario."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Option:
    id: int | None
    text: str
    is_correct: bool
    display_order: int
    justification: str | None = None


@dataclass(frozen=True)
class SyllabusTag:
    syllabus_id: str
    block: str | None
    topic: str | None


@dataclass
class Question:
    id: int | None
    statement: str
    source: str
    source_id: str
    options: list[Option] = field(default_factory=list)
    tags: list[SyllabusTag] = field(default_factory=list)
    justification: str | None = None
    img_path: str | None = None
    is_annulled: bool = False
    annulment_reason: str | None = None
    pending_classification: bool = False
    year: int | None = None
    is_official_exam: bool = False
