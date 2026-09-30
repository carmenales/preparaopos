"""Cálculo de nota puro, sin BD. La fórmula se cubrirá con TDD en test_scoring_service."""

from __future__ import annotations

from decimal import Decimal

from domain.scoring.models import ScoringRule


class ScoringService:
    def score(
        self,
        *,
        correct: int,
        wrong: int,
        blank: int,
        rule: ScoringRule,
    ) -> Decimal:
        """(correct * correct_score) - (wrong * wrong_penalty) + (blank * blank_score)."""
        raw = (
            Decimal(correct) * rule.correct_score
            - Decimal(wrong) * rule.wrong_penalty
            + Decimal(blank) * rule.blank_score
        )
        if rule.min_score_zero and raw < 0:
            return Decimal("0")
        return raw
