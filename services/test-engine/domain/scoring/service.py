"""Cálculo de nota puro, sin BD. Implementación cubierta por TDD."""

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
        """Puntuación bruta directa: (correct * correct_score) - (wrong * wrong_penalty) + (blank * blank_score)."""
        raw = (
            Decimal(correct) * rule.correct_score
            - Decimal(wrong) * rule.wrong_penalty
            + Decimal(blank) * rule.blank_score
        )
        if rule.min_score_zero and raw < 0:
            raw = Decimal("0")

        if rule.round_decimals is not None:
            exp = Decimal("10") ** -rule.round_decimals
            return raw.quantize(exp, rounding=rule.rounding_mode)

        return raw

    def score_scaled(
        self,
        *,
        correct: int,
        wrong: int,
        blank: int,
        annulled: int = 0,
        total_questions: int | None = None,
        rule: ScoringRule,
    ) -> Decimal:
        """Puntuación escalada al baremo oficial (rule.score_scale).
        
        Las preguntas anuladas se descuentan del denominador evaluable.
        Si total_questions no se especifica, se infiere de la suma de respuestas válidas.
        """
        evaluable = (
            (total_questions - annulled)
            if total_questions is not None
            else (correct + wrong + blank)
        )
        if evaluable <= 0:
            return Decimal("0")

        raw = (
            Decimal(correct) * rule.correct_score
            - Decimal(wrong) * rule.wrong_penalty
            + Decimal(blank) * rule.blank_score
        )
        if rule.min_score_zero and raw < 0:
            raw = Decimal("0")

        scaled = (raw / Decimal(evaluable)) * rule.score_scale
        if rule.min_score_zero and scaled < 0:
            scaled = Decimal("0")

        if rule.round_decimals is not None:
            exp = Decimal("10") ** -rule.round_decimals
            return scaled.quantize(exp, rounding=rule.rounding_mode)

        return scaled
