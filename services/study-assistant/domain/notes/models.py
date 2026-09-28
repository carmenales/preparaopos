"""Modelos de dominio para notas y métricas del dashboard."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Note:
    """Representa un apunte del temario cargado desde knowledge_index.json."""

    id: str
    title: str
    path: str
    processes: list[str] = field(default_factory=list)
    official_topic: str | None = None
    block: str | None = None
    tags: list[str] = field(default_factory=list)
    status: str = "borrador"
    excerpt: str = ""
    content_text: str = ""
    headings: list[dict] = field(default_factory=list)
    practice: dict = field(default_factory=dict)
    reading_time: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Note:
        """Crea una Note desde un diccionario del índice JSON."""
        return cls(
            id=data.get("id", ""),
            title=data.get("title", "Sin título"),
            path=data.get("path", ""),
            processes=data.get("processes", []),
            official_topic=data.get("official_topic"),
            block=data.get("block"),
            tags=data.get("tags", []),
            status=data.get("status", "borrador"),
            excerpt=data.get("excerpt", ""),
            content_text=data.get("content_text", ""),
            headings=data.get("headings", []),
            practice=data.get("practice", {}),
            reading_time=data.get("reading_time", ""),
        )


@dataclass
class ProcessSummary:
    """Resumen de métricas de un proceso selectivo."""

    slug: str
    title: str
    total: int = 0
    reviewed: int = 0
    draft: int = 0
    top_tags: list[str] = field(default_factory=list)


@dataclass
class DashboardMetrics:
    """KPIs globales del dashboard."""

    total_notes: int = 0
    total_processes: int = 0
    reviewed_count: int = 0
    draft_count: int = 0
    process_summaries: list[ProcessSummary] = field(default_factory=list)
