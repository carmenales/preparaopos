"""Nombres de los bloques y temas de un temario, para mostrarlos en las listas de tests.

La BD solo guarda el código (``A1``, ``95``). Los nombres están en ``syllabi/<syllabus_id>.json``
(por ahora solo el de PreparaTIC A1). Si un temario no tiene fichero, se muestra el código.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

SYLLABI_DIR = Path(__file__).resolve().parent.parent / "syllabi"


@lru_cache(maxsize=None)
def _load(syllabus_id: str) -> dict:
    path = SYLLABI_DIR / f"{syllabus_id}.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def block_title(syllabus_id: str, block: str | None) -> str:
    """«I. Marco Constitucional Español y Unión Europea», o «Bloque A1» si no se conoce."""
    if not block:
        return ""
    return _load(syllabus_id).get("blocks", {}).get(block) or f"Bloque {block}"


def topic_name(syllabus_id: str, topic: str | None) -> str:
    """«Videoconferencia.», o «Tema 130» si no se conoce."""
    if not topic:
        return ""
    return _load(syllabus_id).get("topics", {}).get(str(topic)) or f"Tema {topic}"
