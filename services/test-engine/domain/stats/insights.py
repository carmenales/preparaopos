"""Diagnóstico de estudio: las reglas de estadisticas.php de preparadortai (prioridad y tendencia)."""

from __future__ import annotations

from statistics import mean

# Diferencias menores que esta se consideran «igual» (como en preparadortai).
TREND_EPSILON = 0.01


def priority_score(answered: int, correct: int) -> float:
    """Cuánto conviene repasar un tema: fallos × lo que falta para el 100 % de acierto."""
    if not answered:
        return 0.0
    wrong = answered - correct
    return wrong * max(0.0, 100 - 100 * correct / answered)


def priority_label(answered: int, correct: int) -> str:
    """«alta», «media» o «baja», con los umbrales de preparadortai."""
    wrong = answered - correct
    accuracy = 100 * correct / answered if answered else 0
    if (answered >= 10 and accuracy < 60) or wrong >= 10:
        return "alta"
    if (answered >= 5 and accuracy < 75) or wrong >= 5:
        return "media"
    return "baja"


def trend(values: list[float], window: int) -> dict:
    """Media de los últimos ``window`` valores frente a los ``window`` anteriores.

    ``values`` va del más antiguo al más reciente. ``delta`` es None si no hay con qué comparar.
    """
    latest = values[-window:]
    previous = values[-2 * window:-window]
    latest_avg = mean(latest) if latest else None
    previous_avg = mean(previous) if previous else None
    delta = latest_avg - previous_avg if latest_avg is not None and previous_avg is not None else None
    return {"latest": latest_avg, "previous": previous_avg, "delta": delta, "direction": direction(delta)}


def direction(delta: float | None) -> str | None:
    """«up», «down», «same» o None (sin comparación)."""
    if delta is None:
        return None
    if delta > TREND_EPSILON:
        return "up"
    if delta < -TREND_EPSILON:
        return "down"
    return "same"
