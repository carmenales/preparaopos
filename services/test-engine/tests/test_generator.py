"""Generador de tests: filtros, refuerzo con falladas y pantalla /generator."""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from config import SQLITE_PATH
from domain.scoring.service import ScoringService
from domain.sessions.generator import GeneratorFilters, NoQuestionsForFilters
from domain.sessions.service import TestSessionService
from infrastructure.db.repositories.exam_repository import ExamRepository
from infrastructure.db.repositories.question_repository import QuestionRepository
from infrastructure.db.repositories.scoring_rule_repository import ScoringRuleRepository
from infrastructure.db.repositories.session_repository import SessionRepository
from presentation.app import app


@pytest.fixture
def db():
    engine = create_engine(f"sqlite:///{SQLITE_PATH}")
    with Session(engine) as session:
        yield session
        session.commit()


@pytest.fixture
def svc(db):
    return TestSessionService(
        session_repository=SessionRepository(db),
        question_repository=QuestionRepository(db),
        scoring_service=ScoringService(),
        exam_repository=ExamRepository(db),
        scoring_rule_repository=ScoringRuleRepository(db),
    )


def _ids_sql(ids):
    return ",".join(str(i) for i in ids)


# --- Filtros ------------------------------------------------------------------

def test_filters_roundtrip_through_source_ref():
    f = GeneratorFilters("age-gsi-official", block="I", topic="9", year=2024,
                         official_only=True, failed_only=True, count=50)
    assert GeneratorFilters.from_source_ref(f.to_source_ref()) == f
    assert len(f.to_source_ref()) <= 128


@pytest.mark.parametrize("kwargs", [
    {"syllabus_id": ""},
    {"syllabus_id": "x", "topic": "9"},
    {"syllabus_id": "x", "count": 0},
    {"syllabus_id": "x", "count": 201},
])
def test_invalid_filters(kwargs):
    with pytest.raises(ValueError):
        GeneratorFilters(**kwargs)


def test_block_and_topic_filter(svc, db):
    s = svc.start_session(mode="practice", source="generated",
                          source_ref=GeneratorFilters("age-gsi-official", block="I", topic="9").to_source_ref())
    assert s.question_ids
    tagged = db.execute(text(
        "SELECT COUNT(DISTINCT question_id) FROM question_syllabus_tags WHERE syllabus_id='age-gsi-official' "
        f"AND block='I' AND topic='9' AND question_id IN ({_ids_sql(s.question_ids)})"
    )).scalar()
    assert tagged == len(s.question_ids)
    assert s.duration_seconds is None


def test_year_official_count_and_exam_duration(svc, db):
    f = GeneratorFilters("preparatic-a1", year=2023, official_only=True, count=40)
    s = svc.start_session(mode="exam", source="generated", source_ref=f.to_source_ref())
    assert len(s.question_ids) == 40
    assert len(set(s.question_ids)) == 40
    matching = db.execute(text(
        f"SELECT COUNT(*) FROM questions WHERE year=2023 AND is_official_exam=1 AND id IN ({_ids_sql(s.question_ids)})"
    )).scalar()
    assert matching == 40
    assert s.duration_seconds == 40 * 60


def test_scoring_rule_of_syllabus_is_used(svc, db):
    s = svc.start_session(mode="practice", source="generated",
                          source_ref=GeneratorFilters("uc3m-a2-gsi", count=5).to_source_ref())
    code = db.execute(text("SELECT code FROM scoring_rules WHERE id = :i"), {"i": s.scoring_rule_id}).scalar()
    assert code == "oficial-cuarto"


def test_annulled_questions_are_excluded(svc, db):
    db.execute(text("UPDATE questions SET is_annulled = 1 WHERE id = (SELECT MIN(question_id) FROM "
                    "question_syllabus_tags WHERE syllabus_id='uc3m-a2-gsi')"))
    db.commit()
    annulled = db.execute(text("SELECT MIN(question_id) FROM question_syllabus_tags WHERE syllabus_id='uc3m-a2-gsi'")).scalar()
    ids = QuestionRepository(db).list_ids_for_generator(GeneratorFilters("uc3m-a2-gsi"))
    assert annulled not in ids
    assert len(ids) == 269


def test_no_matching_questions_raises(svc):
    with pytest.raises(NoQuestionsForFilters):
        svc.start_session(mode="practice", source="generated",
                          source_ref=GeneratorFilters("age-gsi-official", year=1999).to_source_ref())


# --- Refuerzo con falladas ------------------------------------------------------

def _answer(svc, db, qid, correct: bool, when: datetime):
    s = svc.start_session(mode="practice", source="questions", source_ref=str(qid))
    option = db.execute(text(
        "SELECT id FROM question_options WHERE question_id = :q AND is_correct = :c LIMIT 1"
    ), {"q": qid, "c": int(correct)}).scalar()
    svc.submit_answer(session_id=s.id, question_id=qid, selected_option_id=option, now=when)
    db.commit()


def test_failed_only_uses_last_answer(svc, db):
    qid = db.execute(text(
        "SELECT q.id FROM questions q JOIN question_syllabus_tags t ON t.question_id = q.id "
        "WHERE t.syllabus_id = 'cm-madrid-digital-ia' ORDER BY q.id LIMIT 1"
    )).scalar()
    failed = GeneratorFilters("cm-madrid-digital-ia", failed_only=True, count=200)
    repo = QuestionRepository(db)
    base = datetime.now(timezone.utc)

    _answer(svc, db, qid, correct=False, when=base)
    assert qid in repo.list_ids_for_generator(failed)

    _answer(svc, db, qid, correct=True, when=base + timedelta(minutes=1))
    assert qid not in repo.list_ids_for_generator(failed)

    _answer(svc, db, qid, correct=False, when=base + timedelta(minutes=2))
    s = svc.start_session(mode="practice", source="generated", source_ref=failed.to_source_ref())
    assert qid in s.question_ids


# --- Pantalla --------------------------------------------------------------------

@pytest.fixture
def client():
    return TestClient(app, follow_redirects=False)


def test_generator_page_lists_syllabi_and_facets(client):
    res = client.get("/generator/?syllabus_id=age-gsi-official")
    assert res.status_code == 200
    assert res.headers.get("cache-control") == "no-store"
    assert 'value="uc3m-a2-gsi"' in res.text
    assert re.search(r'value="I\|9"', res.text)


def test_count_fragment(client):
    res = client.get("/generator/count", params={"syllabus_id": "preparatic-a1", "year": "2023", "official": "1"})
    assert res.status_code == 200
    assert "<strong>1171</strong>" in res.text


def test_post_creates_session_and_redirects(client):
    res = client.post("/generator/", data={"syllabus_id": "age-gsi-official", "scope": "I", "count": "10",
                                           "mode": "practice"})
    assert res.status_code == 303
    assert re.search(r"/sessions/[0-9a-f]+/question/1$", res.headers["location"])
    assert client.get(res.headers["location"]).status_code == 200


def test_post_without_results_returns_to_form_with_message(client):
    res = client.post("/generator/", data={"syllabus_id": "age-gsi-official", "year": "1999", "mode": "practice"})
    assert res.status_code == 303
    assert "/generator/?" in res.headers["location"]
    assert "Ninguna pregunta cumple" in client.get(res.headers["location"]).text


def test_generator_urls_are_prefixed_behind_gateway(client, monkeypatch):
    import config

    monkeypatch.setenv("ROOT_PATH", "/tests")
    monkeypatch.setattr(config, "ROOT_PATH", "/tests")
    html = client.get("/generator/?syllabus_id=age-gsi-official").text
    unprefixed = re.findall(r"""(?:href|src|action|hx-get|hx-post)=["']/(?!tests/|#)([^"']*)["']""", html)
    assert unprefixed == []
    res = client.post("/generator/", data={"syllabus_id": "age-gsi-official", "count": "10", "mode": "practice"})
    assert res.headers["location"].startswith("/tests/sessions/")


# --- Aviso cuando hay menos preguntas de las pedidas --------------------------------

def test_count_fragment_warns_when_fewer_than_requested(client):
    params = {"syllabus_id": "age-gsi-official", "scope": "I|9"}
    available = int(re.search(r"<strong>(\d+)</strong>", client.get("/generator/count", params=params).text).group(1))
    warned = client.get("/generator/count", params=params | {"count": str(available + 5)}).text
    assert f"has pedido {available + 5}, pero solo hay {available}" in warned
    assert "has pedido" not in client.get("/generator/count", params=params | {"count": str(available)}).text
    assert "ninguna cumple" in client.get("/generator/count", params={"syllabus_id": "age-gsi-official",
                                                                       "year": "1999"}).text


def test_short_test_shows_n_of_requested_on_first_question(client):
    res = client.post("/generator/", data={"syllabus_id": "age-gsi-official", "scope": "I|9", "count": "200",
                                           "mode": "practice"})
    assert res.headers["location"].endswith("/question/1?requested=200")
    page = client.get(res.headers["location"]).text
    assert "pedidas" in page and "de 200 pedidas" in page
    full = client.post("/generator/", data={"syllabus_id": "age-gsi-official", "count": "10", "mode": "practice"})
    assert "requested" not in full.headers["location"]
