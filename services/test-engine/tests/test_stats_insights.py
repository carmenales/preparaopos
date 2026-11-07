"""Reglas del diagnóstico de estudio (prioridad y tendencia), como en preparadortai."""

from domain.stats.insights import direction, priority_label, priority_score, trend


def test_priority_label_uses_preparadortai_thresholds():
    assert priority_label(10, 5) == "alta"      # 10 respuestas y 50 % de acierto
    assert priority_label(40, 30) == "alta"     # 10 fallos
    assert priority_label(5, 3) == "media"      # 5 respuestas y 60 %
    assert priority_label(30, 25) == "media"    # 5 fallos
    assert priority_label(4, 0) == "baja"       # pocas respuestas todavía
    assert priority_label(0, 0) == "baja"


def test_priority_score_weights_mistakes_by_what_is_missing():
    assert priority_score(0, 0) == 0
    assert priority_score(10, 10) == 0
    assert priority_score(10, 5) == 5 * 50
    assert priority_score(20, 5) > priority_score(10, 5)


def test_trend_compares_the_last_window_with_the_previous_one():
    t = trend([4, 4, 4, 6, 6, 6], 3)
    assert t["latest"] == 6 and t["previous"] == 4 and t["delta"] == 2 and t["direction"] == "up"
    assert trend([5, 5], 3)["delta"] is None and trend([5, 5], 3)["direction"] is None
    assert trend([], 5)["latest"] is None
    assert direction(-0.5) == "down" and direction(0.005) == "same"
