"""
Pruebas unitarias para ScoringService siguiendo TDD.

Cubre:
1. Puntuación directa de aciertos sin penalización.
2. Fórmula oficial AGE (Acierto = 1, Fallo = -1/3, Blanco = 0).
3. Aritmética exacta con Decimal (sin pérdidas de precisión de punto flotante).
4. Suelo de calificación mínima cero (min_score_zero).
5. Escalado de nota al baremo de la convocatoria (score_scale).
6. Redondeo configurable (ROUND_HALF_UP provisional).
7. Examen con preguntas anuladas (caso AGE GSI 2024: 4 anuladas, 96 computables).
"""

from decimal import Decimal, ROUND_HALF_UP
import pytest

from domain.scoring.models import ScoringRule
from domain.scoring.service import ScoringService


@pytest.fixture
def scoring_service() -> ScoringService:
    return ScoringService()


@pytest.fixture
def age_official_rule() -> ScoringRule:
    """Regla estándar AGE: A - F/3, blanco = 0, escala 100, min 0."""
    return ScoringRule(
        id=1,
        code="age-oficial-tercio",
        name="AGE oficial A - F/3",
        correct_score=Decimal("1"),
        wrong_penalty=Decimal("1") / Decimal("3"),
        blank_score=Decimal("0"),
        score_scale=Decimal("100"),
        min_score_zero=True,
        # TODO: confirmar regla de redondeo oficial de la convocatoria específica,
        # asumido ROUND_HALF_UP provisionalmente
        round_decimals=2,
        rounding_mode=ROUND_HALF_UP,
    )


def test_score_all_correct_no_penalty(scoring_service: ScoringService):
    """Test 1: Todos aciertos sin fallos ni blancos."""
    rule = ScoringRule(
        id=None,
        code="simple",
        name="Sin penalización",
        correct_score=Decimal("1"),
        wrong_penalty=Decimal("0"),
        blank_score=Decimal("0"),
        score_scale=Decimal("10"),
        min_score_zero=True,
    )
    res = scoring_service.score(correct=10, wrong=0, blank=0, rule=rule)
    assert res == Decimal("10")


def test_score_official_age_formula_exact(scoring_service: ScoringService, age_official_rule: ScoringRule):
    """Test 2: 60 aciertos, 15 fallos, 25 blancos -> 60 - (15/3) = 55 netos."""
    rule_exact = ScoringRule(
        id=None,
        code="age-exact",
        name="AGE sin redondeo forzado",
        correct_score=Decimal("1"),
        wrong_penalty=Decimal("1") / Decimal("3"),
        blank_score=Decimal("0"),
        score_scale=Decimal("100"),
        min_score_zero=True,
        round_decimals=None,
    )
    res = scoring_service.score(correct=60, wrong=15, blank=25, rule=rule_exact)
    assert res == Decimal("55")


def test_decimal_precision_no_float_artifacts(scoring_service: ScoringService):
    """Test 3: Decimal exacto: 1 acierto y 1 fallo con penalización 1/3 debe ser exactamente 2/3."""
    rule = ScoringRule(
        id=None,
        code="frac",
        name="Fracción",
        correct_score=Decimal("1"),
        wrong_penalty=Decimal("1") / Decimal("3"),
        blank_score=Decimal("0"),
        score_scale=Decimal("10"),
        min_score_zero=True,
        round_decimals=None,
    )
    res = scoring_service.score(correct=1, wrong=1, blank=0, rule=rule)
    expected = Decimal("1") - (Decimal("1") / Decimal("3"))
    assert res == expected
    assert str(res).startswith("0.6666666666666666")


def test_min_score_zero_floor(scoring_service: ScoringService):
    """Test 4: Nota bruta negativa queda en 0 si min_score_zero es True; si es False, es negativa."""
    rule_min_zero = ScoringRule(
        id=None,
        code="floor-zero",
        name="Suelo cero",
        correct_score=Decimal("1"),
        wrong_penalty=Decimal("1"),
        blank_score=Decimal("0"),
        score_scale=Decimal("10"),
        min_score_zero=True,
    )
    rule_allow_negative = ScoringRule(
        id=None,
        code="allow-neg",
        name="Permite negativos",
        correct_score=Decimal("1"),
        wrong_penalty=Decimal("1"),
        blank_score=Decimal("0"),
        score_scale=Decimal("10"),
        min_score_zero=False,
    )

    assert scoring_service.score(correct=2, wrong=10, blank=0, rule=rule_min_zero) == Decimal("0")
    assert scoring_service.score(correct=2, wrong=10, blank=0, rule=rule_allow_negative) == Decimal("-8")


def test_scaled_score_to_scale(scoring_service: ScoringService):
    """Test 5: Escalado a baremo de convocatoria (ej. escala 50 puntos sobre 100 preguntas)."""
    rule_scale_50 = ScoringRule(
        id=None,
        code="scale-50",
        name="Escala 50",
        correct_score=Decimal("1"),
        wrong_penalty=Decimal("1") / Decimal("3"),
        blank_score=Decimal("0"),
        score_scale=Decimal("50"),
        min_score_zero=True,
        round_decimals=2,
    )
    # 70 aciertos, 15 fallos, 15 blancos en 100 preguntas
    # Netas = 70 - 5 = 65 netas sobre 100.
    # En escala 50: (65 / 100) * 50 = 32.50 puntos.
    scaled = scoring_service.score_scaled(
        correct=70,
        wrong=15,
        blank=15,
        total_questions=100,
        rule=rule_scale_50,
    )
    assert scaled == Decimal("32.50")


def test_rounding_mode_half_up(scoring_service: ScoringService):
    """Test 6: Redondeo provisional a 2 decimales con ROUND_HALF_UP."""
    # TODO: confirmar regla de redondeo oficial, asumido ROUND_HALF_UP provisionalmente
    rule_round = ScoringRule(
        id=None,
        code="round-test",
        name="Redondeo test",
        correct_score=Decimal("1"),
        wrong_penalty=Decimal("1") / Decimal("3"),
        blank_score=Decimal("0"),
        score_scale=Decimal("100"),
        min_score_zero=True,
        round_decimals=2,
        rounding_mode=ROUND_HALF_UP,
    )
    # 70 aciertos, 11 fallos, 0 blancos:
    # 70 - (11/3) = 70 - 3.666666... = 66.333333... -> 66.33
    res = scoring_service.score(correct=70, wrong=11, blank=0, rule=rule_round)
    assert res == Decimal("66.33")


def test_annulled_questions_excluded_from_total(scoring_service: ScoringService):
    """Test 7: Preguntas anuladas excluidas del denominador evaluable (Caso real AGE GSI 2024: 96 válidas)."""
    rule_scale_100 = ScoringRule(
        id=None,
        code="gsi-2024",
        name="AGE GSI 2024 Real",
        correct_score=Decimal("1"),
        wrong_penalty=Decimal("1") / Decimal("3"),
        blank_score=Decimal("0"),
        score_scale=Decimal("100"),
        min_score_zero=True,
        round_decimals=2,
        rounding_mode=ROUND_HALF_UP,
    )
    # Examen con 100 preguntas originales y 4 anuladas por el tribunal -> 96 evaluables.
    # Opositor responde: 72 aciertos, 24 fallos, 0 blancos (y 4 anuladas).
    # Netas = 72 - 24/3 = 72 - 8 = 64 netas sobre 96 válidas.
    # Escalado sobre 100: (64 / 96) * 100 = 66.6666... -> redondeado a 2 decimales: 66.67 puntos.
    scaled = scoring_service.score_scaled(
        correct=72,
        wrong=24,
        blank=0,
        annulled=4,
        total_questions=100,
        rule=rule_scale_100,
    )
    assert scaled == Decimal("66.67")
