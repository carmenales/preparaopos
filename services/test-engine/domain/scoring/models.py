"""Regla de corrección parametrizable (baremo oficial)."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class ScoringRule:
    id: int | None
    code: str
    name: str
    correct_score: Decimal
    wrong_penalty: Decimal
    blank_score: Decimal
    score_scale: Decimal
    min_score_zero: bool = True
    round_decimals: int | None = None
    rounding_mode: str = ROUND_HALF_UP
