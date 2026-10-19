"""Filtros del generador de tests (origen de sesión ``generated``).

Sustituye a los modos de práctica de preparadortai (temas, práctica temática,
refuerzo) y a los de PreparaTIC V3 (aleatorio, por bloque, por tema, por año).
Los filtros se serializan en ``test_sessions.source_ref`` para que cada sesión
quede autodescrita.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qsl, urlencode

DEFAULT_COUNT = 30
MAX_COUNT = 200
# Misma proporción que el simulacro AGE A2 GSI 2024 (100 preguntas en 6.000 s).
SECONDS_PER_QUESTION = 60


@dataclass(frozen=True)
class GeneratorFilters:
    syllabus_id: str
    block: str | None = None
    topic: str | None = None
    year: int | None = None
    official_only: bool = False
    failed_only: bool = False
    count: int = DEFAULT_COUNT

    def __post_init__(self) -> None:
        if not self.syllabus_id:
            raise ValueError("El generador necesita un temario")
        if self.topic and not self.block:
            raise ValueError("Para filtrar por tema hay que indicar también el bloque")
        if not 1 <= self.count <= MAX_COUNT:
            raise ValueError(f"El número de preguntas debe estar entre 1 y {MAX_COUNT}")

    def to_source_ref(self) -> str:
        params: dict[str, str] = {"syllabus": self.syllabus_id, "n": str(self.count)}
        if self.block:
            params["block"] = self.block
        if self.topic:
            params["topic"] = self.topic
        if self.year is not None:
            params["year"] = str(self.year)
        if self.official_only:
            params["official"] = "1"
        if self.failed_only:
            params["failed"] = "1"
        return urlencode(params)

    @classmethod
    def from_source_ref(cls, source_ref: str) -> "GeneratorFilters":
        p = dict(parse_qsl(source_ref or ""))
        return cls(
            syllabus_id=p.get("syllabus", ""),
            block=p.get("block") or None,
            topic=p.get("topic") or None,
            year=int(p["year"]) if p.get("year") else None,
            official_only=p.get("official") == "1",
            failed_only=p.get("failed") == "1",
            count=int(p.get("n", DEFAULT_COUNT)),
        )


class NoQuestionsForFilters(ValueError):
    """Ninguna pregunta cumple los filtros: no se crea una sesión vacía."""
