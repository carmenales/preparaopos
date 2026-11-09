"""Historial de sesiones, borrado y estadísticas por temario."""

from __future__ import annotations

import re

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from config import SQLITE_PATH
from domain.sessions.generator import GeneratorFilters
from infrastructure.db.repositories.question_repository import QuestionRepository
from infrastructure.db.repositories.stats_repository import StatsRepository
from presentation.app import app


@pytest.fixture
def db():
    engine = create_engine(f"sqlite:///{SQLITE_PATH}")
    with Session(engine) as session:
        yield session


@pytest.fixture
def client():
    return TestClient(app, follow_redirects=False)


def _new_practice_session(client) -> str:
    res = client.post("/generator/", data={"syllabus_id": "age-gsi-official", "count": "10", "mode": "practice"})
    return re.search(r"/sessions/([0-9a-f]+)", res.headers["location"]).group(1)


def test_history_lists_sessions_with_labels(client):
    sid = _new_practice_session(client)
    res = client.get("/history/")
    assert res.status_code == 200
    assert res.headers.get("cache-control") == "no-store"
    assert "Generado: AGE A2 GSI" in res.text
    # sesión abierta: se continúa, no se abre el resultado (eso la cerraría)
    assert f'href="/sessions/{sid}"' in res.text  # «Continuar» abre la pantalla del test
    assert f"/sessions/{sid}/result" not in res.text


def test_delete_session_removes_attempts(client, db):
    sid = _new_practice_session(client)
    qid = db.execute(text("SELECT question_ids FROM test_sessions WHERE id = :i"), {"i": sid}).scalar()
    first = int(re.search(r"\d+", qid).group())
    option = db.execute(text("SELECT id FROM question_options WHERE question_id = :q LIMIT 1"), {"q": first}).scalar()
    client.post(f"/sessions/{sid}/answer", data={"question_id": first, "selected_option_id": option, "n": 1},
                headers={"HX-Request": "true"})
    db.expire_all()
    assert db.execute(text("SELECT COUNT(*) FROM test_attempts WHERE test_session_id = :i"), {"i": sid}).scalar() == 1

    res = client.post(f"/history/{sid}/delete")
    assert res.status_code == 303
    assert res.headers["location"].endswith("/history/?deleted=1")
    db.expire_all()
    assert db.execute(text("SELECT COUNT(*) FROM test_sessions WHERE id = :i"), {"i": sid}).scalar() == 0
    assert db.execute(text("SELECT COUNT(*) FROM test_attempts WHERE test_session_id = :i"), {"i": sid}).scalar() == 0
    assert "Sesión borrada" in client.get(res.headers["location"]).text


def test_stats_are_consistent_with_generator(client, db):
    sid = _new_practice_session(client)
    qids = [int(x) for x in re.findall(r"\d+", db.execute(
        text("SELECT question_ids FROM test_sessions WHERE id = :i"), {"i": sid}).scalar())][:3]
    for n, qid in enumerate(qids, start=1):
        wrong = db.execute(text("SELECT id FROM question_options WHERE question_id = :q AND is_correct = 0 LIMIT 1"),
                           {"q": qid}).scalar()
        client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": wrong, "n": n},
                    headers={"HX-Request": "true"})

    stats = StatsRepository(db).syllabus_stats("age-gsi-official")
    failed = QuestionRepository(db).count_for_generator(GeneratorFilters("age-gsi-official", failed_only=True))
    assert stats["pending"] == failed
    assert stats["pending"] >= 3
    assert stats["answered"] >= 3
    priorities = [t["priority_score"] for t in stats["topics"]]
    assert priorities == sorted(priorities, reverse=True)        # áreas débiles: lo más urgente primero

    page = client.get("/stats/?syllabus_id=age-gsi-official")
    assert page.status_code == 200
    assert "falladas pendientes" in page.text.lower()
    assert "failed=1" in page.text


def test_stats_without_activity_for_unknown_syllabus_falls_back(client):
    assert client.get("/stats/?syllabus_id=no-existe").status_code == 200


def test_history_and_stats_urls_are_prefixed_behind_gateway(client, monkeypatch):
    import config

    _new_practice_session(client)
    monkeypatch.setenv("ROOT_PATH", "/tests")
    monkeypatch.setattr(config, "ROOT_PATH", "/tests")
    pattern = re.compile(r"""(?:href|src|action|hx-get|hx-post)=["']/(?!tests/|#)([^"']*)["']""")
    for path in ("/history/", "/stats/"):
        html = client.get(path).text
        assert pattern.findall(html) == [], path


def _exam_session_failing_first_question(client, db, exam_id: int = 53) -> tuple[str, int]:
    res = client.post("/sessions/", data={"source": "exam", "source_ref": str(exam_id), "mode": "exam"})
    sid = re.search(r"/sessions/([0-9a-f]+)", res.headers["location"]).group(1)
    ids = db.execute(text("SELECT question_ids FROM test_sessions WHERE id = :i"), {"i": sid}).scalar()
    qid = int(re.search(r"\d+", ids).group())
    wrong = db.execute(text("SELECT id FROM question_options WHERE question_id = :q AND is_correct = 0 LIMIT 1"),
                       {"q": qid}).scalar()
    client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": wrong})
    client.post(f"/sessions/{sid}/close")
    return sid, qid


def test_stats_show_exam_progress_recurrent_mistakes_and_charts(client, db):
    _, qid = _exam_session_failing_first_question(client, db)
    _exam_session_failing_first_question(client, db)
    db.expire_all()

    stats = StatsRepository(db).syllabus_stats("age-gsi-official")
    exam = next(e for e in stats["exams"] if e["id"] == 53)
    assert exam["attempts"] >= 2 and exam["last"] == 0 and exam["best"] >= exam["last"]
    assert exam["direction"] in ("up", "down", "same")
    recurrent = next(q for q in stats["recurrent"] if q["id"] == qid)
    assert recurrent["wrong"] >= 2 and recurrent["last_correct"] is False and recurrent["error"] > 0
    d = stats["distribution"]
    assert d["wrong"] >= 2 and d["blank"] >= 2 * 90                  # el resto de cada examen, en blanco
    assert stats["trend"]["latest"] is not None
    assert {b["block"] for b in stats["blocks"]} and all(b["answered"] for b in stats["blocks"])

    page = client.get("/stats/?syllabus_id=age-gsi-official").text
    for section in ("Diagnóstico rápido", "Área prioritaria", "Examen a repetir", "Tendencia reciente",
                    "Progreso por examen", "Preguntas con fallos recurrentes", "Áreas débiles",
                    'id="chart-evolution"', 'id="stats-data"', "AGE A2 GSI LIBRE 2024"):
        assert section in page, section
    assert f'href="/manage/questions/{qid}/edit"' in page
