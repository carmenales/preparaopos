"""Filtros del generador de tests (origen de sesión ``generated``).

Sustituye a los modos de práctica de preparadortai (temas, práctica temática,
refuerzo) y a los de PreparaTIC V3 (aleatorio, ponderado, por bloque, por tema, por año).
Los filtros se serializan en ``test_sessions.source_ref`` para que cada sesión
quede autodescrita.
"""

from __future__ import annotations

import math
import random
from collections import Counter
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
    weighted: bool = False
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
        if self.weighted:
            params["weighted"] = "1"
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
            weighted=p.get("weighted") == "1",
            count=int(p.get("n", DEFAULT_COUNT)),
        )


# ---------------------------------------------------------------------------
# Test ponderado por frecuencia histórica (modo «ponderado» de PreparaTIC V3)
# ---------------------------------------------------------------------------
#
# Cada tema pesa lo que ha caído en exámenes oficiales: el número de preguntas de examen
# oficial de ese tema en el temario. Como en el generador de PreparaTIC, el peso de una
# pregunta es el de su tema dividido entre las preguntas disponibles de ese tema, para que
# un tema con muchas preguntas en el banco no salga más solo por tener más.

TopicKey = tuple[str | None, str | None]


def question_weights(tagged: list[tuple[int, str | None, str | None]],
                     frequencies: dict[TopicKey, int]) -> dict[int, float]:
    """Peso de cada pregunta del conjunto disponible.

    ``tagged``: (id, bloque, tema) de las preguntas que cumplen los filtros (una fila por etiqueta).
    ``frequencies``: preguntas de examen oficial por (bloque, tema) en el temario.
    Las preguntas de temas que nunca han caído pesan 0.
    """
    available = Counter((block, topic) for _, block, topic in tagged)
    weights: dict[int, float] = {}
    for qid, block, topic in tagged:
        key = (block, topic)
        weights[qid] = weights.get(qid, 0.0) + frequencies.get(key, 0) / available[key]
    return weights


def weighted_sample(weights: dict[int, float], k: int, rng: random.Random | None = None) -> list[int]:
    """k ids sin repetición, cada uno con probabilidad proporcional a su peso (Efraimidis-Spirakis).

    Si no hay bastantes con peso positivo, se completa al azar con los de peso 0: el test
    tiene siempre todas las preguntas que se puedan dar.
    """
    rng = rng or random
    keyed = []
    for qid, w in weights.items():
        u = 1.0 - rng.random()  # en (0, 1]
        key = math.log(u) / w if w > 0 else -math.inf
        keyed.append((key, rng.random(), qid))
    keyed.sort(reverse=True)
    return [qid for _, _, qid in keyed[:k]]


class NoQuestionsForFilters(ValueError):
    """Ninguna pregunta cumple los filtros: no se crea una sesión vacía."""
