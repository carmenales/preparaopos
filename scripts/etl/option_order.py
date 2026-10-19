"""Orden de presentación de las opciones de una pregunta (``question_options.display_order``).

Los importadores de MariaDB (``ptype`` + ``incorrectas``) reciben la respuesta correcta
separada de las incorrectas, así que no traen el orden A, B, C... del examen. Este
módulo lo resuelve de dos formas:

- ``official_positions``: cuando las justificaciones traen la letra oficial
  ("Respuesta correcta: opción D", "Opción A incorrecta según plantilla...").
- ``stable_positions``: cuando el orden original se ha perdido. Baraja de forma
  determinista por pregunta (mismo resultado en cada ejecución), para que la
  correcta no quede siempre en primera posición. Si la explicación cita una única
  letra ("opción C"), la correcta se coloca en esa letra.

Ambas reciben las opciones como ``[correcta, incorrecta_1, incorrecta_2, ...]`` y
devuelven el ``display_order`` (0 = A) de cada una, en ese mismo orden.
"""

from __future__ import annotations

import random
import re

LETTERS = "ABCDEFG"

_CORRECT_RE = re.compile(r"respuesta\s+correcta:?\s*opci[oó]n\s+([A-G])\b", re.IGNORECASE)
_WRONG_RE = re.compile(r"^\s*opci[oó]n\s+([A-G])\s+incorrecta\b", re.IGNORECASE)
_HINT_RE = re.compile(r"\bopci[oó]n\s+([A-G])\b", re.IGNORECASE)


def official_positions(question_justification: str | None, wrong_justifications: list[str | None]) -> list[int] | None:
    """Posiciones oficiales a partir de las letras de las justificaciones, o None si no están completas."""
    n = 1 + len(wrong_justifications)
    wrong_letters = []
    for justif in wrong_justifications:
        m = _WRONG_RE.match(justif or "")
        if not m:
            return None
        wrong_letters.append(m.group(1).upper())

    m = _CORRECT_RE.search(question_justification or "")
    if m:
        correct_letter = m.group(1).upper()
    else:
        remaining = set(LETTERS[:n]) - set(wrong_letters)
        if len(remaining) != 1:
            return None
        correct_letter = remaining.pop()

    letters = [correct_letter, *wrong_letters]
    if sorted(letters) != list(LETTERS[:n]):
        return None
    return [LETTERS.index(letter) for letter in letters]


def letter_hint(question_justification: str | None, n_options: int) -> int | None:
    """Posición de la correcta si la explicación cita una única letra válida ("opción C")."""
    letters = {m.upper() for m in _HINT_RE.findall(question_justification or "")}
    if len(letters) != 1:
        return None
    index = LETTERS.index(letters.pop())
    return index if index < n_options else None


def stable_positions(key: str, n_options: int, correct_position: int | None = None) -> list[int]:
    """Permutación determinista de ``range(n_options)`` para la clave dada."""
    positions = list(range(n_options))
    random.Random(key).shuffle(positions)
    if correct_position is not None and positions[0] != correct_position:
        other = positions.index(correct_position)
        positions[0], positions[other] = positions[other], positions[0]
    return positions
