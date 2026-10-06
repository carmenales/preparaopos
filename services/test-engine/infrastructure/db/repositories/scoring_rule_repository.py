"""Repositorio de reglas de puntuación (SQLAlchemy)."""

from __future__ import annotations

from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.scoring.models import ScoringRule
from infrastructure.db import orm_models as orm


class ScoringRuleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, rule_id: int) -> ScoringRule | None:
        row = self._session.get(orm.ScoringRule, rule_id)
        if row is None:
            return None
        return self._to_domain(row)

    def get_by_code(self, code: str) -> ScoringRule | None:
        row = self._session.scalar(select(orm.ScoringRule).where(orm.ScoringRule.code == code))
        if row is None:
            return None
        return self._to_domain(row)

    @staticmethod
    def _to_domain(row: orm.ScoringRule) -> ScoringRule:
        return ScoringRule(
            id=row.id,
            code=row.code,
            name=row.name,
            correct_score=Decimal(str(row.correct_score)),
            wrong_penalty=Decimal(str(row.wrong_penalty)),
            blank_score=Decimal(str(row.blank_score)),
            score_scale=Decimal(str(row.score_scale)),
            min_score_zero=row.min_score_zero,
            round_decimals=2,
        )
