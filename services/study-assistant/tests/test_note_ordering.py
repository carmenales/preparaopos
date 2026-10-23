"""Orden de los apuntes por bloque, tema y subparte (y no por el texto de official_topic)."""

from __future__ import annotations

from domain.notes.models import Note
from domain.notes.service import NoteService, parse_topic_position


def _note(note_id: str, official_topic: str | None = None, title: str | None = None) -> Note:
    return Note(id=note_id, title=title or official_topic or note_id, path=f"{note_id}.md",
                official_topic=official_topic)


def _order(notes: list[Note]) -> list[str]:
    return [n.id for n in NoteService(notes).sort_sequentially(notes)]


def test_mixed_topic_formats_share_position():
    assert parse_topic_position(_note("a", "I.05_Estructura")) == parse_topic_position(_note("b", "Tema I.05 Estructura"))
    assert parse_topic_position(_note("c", "TEMA III.01 CONCEPTO DEL CICLO DE VIDA.")) == ((0, 3), 1, 0)
    assert parse_topic_position(_note("d", "II.16.")) == ((0, 2), 16, 0)
    assert parse_topic_position(_note("e", "I.06.II_Identidad")) == ((0, 1), 6, 2)
    assert parse_topic_position(_note("f", "Tema 11. Real Decreto 311/2022")) == ((0, 0), 11, 0)
    assert parse_topic_position(_note("g", "B4.03 Redes")) == ((ord("B"), 4), 3, 0)
    # Respaldo con el id cuando el tema oficial no trae numeración
    assert parse_topic_position(_note("tema-ii-09-lenguajes", "Lenguajes de marcas")) == ((0, 2), 9, 0)
    assert parse_topic_position(_note("cm-ad-ia-p01-tema-006-arquitectura", "Arquitectura")) == ((0, 0), 6, 0)
    assert parse_topic_position(_note("ens", "ESQUEMA NACIONAL DE SEGURIDAD")) is None


def test_blocks_topics_subparts_and_unnumbered_last():
    notes = [
        _note("ens", "ESQUEMA NACIONAL DE SEGURIDAD"),
        _note("tema-ii-01", "II.01_Tecnologi"),
        _note("tema-i-10", "Tema I.10 Administración Digital"),
        _note("introduccion", "Introducción"),
        _note("tema-i-06-ii", "I.06.II_Identidad"),
        _note("tema-i-02", "Tema I.02 Derecho Constitucional"),
        _note("tema-i-06-i", "I.06.I_La"),
        _note("agenda", "PLAN DE DIGITALIZACIÓN DE LAS AAPP"),
        _note("tema-iv-01", "IV.01"),
        _note("tema-i-05", "I.05_Estructura"),
    ]
    assert _order(notes) == ["tema-i-02", "tema-i-05", "tema-i-06-i", "tema-i-06-ii", "tema-i-10", "tema-ii-01",
                             "tema-iv-01", "ens", "introduccion", "agenda"]


def test_numeric_topics_are_not_sorted_as_text():
    notes = [_note(f"maj-tema-{n}", f"Tema {n}. Algo") for n in (10, 2, 1, 11)]
    assert _order(notes) == ["maj-tema-1", "maj-tema-2", "maj-tema-10", "maj-tema-11"]


def test_each_profile_stays_together_where_its_numbering_starts():
    notes = [
        _note("cm-ad-ia-p02-tema-004-etica", "Tema 4. Ética"),
        _note("cm-ad-ia-tema-008-igualdad", "Tema 8. Igualdad"),
        _note("cm-ad-ia-p01-tema-005-ciclo", "Tema 5. Ciclo"),
        _note("cm-ad-ia-tema-001-fundamentos", "Tema 1. Fundamentos"),
        _note("cm-ad-ia-p01-tema-004-gobierno", "Tema 4. Gobierno"),
        _note("cm-ad-ia-p02-tema-005-marco", "Tema 5. Marco"),
        _note("p01-preguntas-repaso", "Preguntas tipo test de repaso"),
    ]
    assert _order(notes) == ["cm-ad-ia-tema-001-fundamentos", "cm-ad-ia-p01-tema-004-gobierno",
                             "cm-ad-ia-p01-tema-005-ciclo", "cm-ad-ia-p02-tema-004-etica", "cm-ad-ia-p02-tema-005-marco",
                             "cm-ad-ia-tema-008-igualdad", "p01-preguntas-repaso"]
