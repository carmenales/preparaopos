"""Filas maestras de syllabi (decisión f) y baremo por defecto A - F/3."""

from decimal import Decimal

SEED_SYLLABI = [
    {
        "id": "preparatic-a1",
        "code": "preparatic-a1",
        "name": "A1 TIC AGE",
        "organism": "AGE",
    },
    {
        "id": "preparatic-b-gsi",
        "code": "preparatic-b-gsi",
        "name": "A2 GSI AGE",
        "organism": "AGE",
    },
    {
        "id": "tai-legacy",
        "code": "tai-legacy",
        "name": "TAI AGE",
        "organism": "AGE",
    },
]

SEED_SCORING_RULES = [
    {
        "code": "age-oficial-tercio",
        "name": "AGE oficial A − F/3",
        "correct_score": Decimal(1),
        "wrong_penalty": Decimal(1) / Decimal(3),
        "blank_score": Decimal(0),
        "score_scale": Decimal(10),
        "min_score_zero": True,
    },
]
