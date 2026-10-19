"""Gestión de preguntas y cuestionarios."""

from __future__ import annotations

import re

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from config import SQLITE_PATH
from domain.management.forms import OptionInput, QuestionInput, ValidationError
from presentation.app import app


@pytest.fixture
def db():
    engine = create_engine(f"sqlite:///{SQLITE_PATH}")
    with Session(engine) as session:
        yield session


@pytest.fixture
def client():
    return TestClient(app, follow_redirects=False)


def _scalar(db, sql, **params):
    db.expire_all()
    return db.execute(text(sql), params).scalar()


NEW_QUESTION = {
    "statement": "¿Qué puerto usa HTTPS por defecto?",
    "opt_id": ["", "", "", "", "", ""],
    "opt_text": ["80", "443", "21", "", "", ""],
    "opt_just": ["", "HTTP sobre TLS", "", "", "", ""],
    "correct": "1",
    "syllabus_id": "uc3m-a2-gsi",
    "block": "",
    "topic": "",
    "year": "2026",
}


def _create(client, **extra) -> int:
    res = client.post("/manage/questions/new", data=NEW_QUESTION | extra)
    assert res.status_code == 303, res.text[:300]
    return int(re.search(r"/questions/(\d+)/edit", res.headers["location"]).group(1))


# --- Validación ------------------------------------------------------------------

def test_question_input_validation():
    with pytest.raises(ValidationError) as exc:
        QuestionInput(statement=" ", options=[OptionInput("a")], correct_index=None, syllabus_id=None, topic="3").validate()
    assert len(exc.value.errors) == 5
    with pytest.raises(ValidationError):
        QuestionInput(statement="x", options=[OptionInput("a"), OptionInput("A")], correct_index=0,
                      syllabus_id="s").validate()
    with pytest.raises(ValidationError):
        QuestionInput(statement="x", options=[OptionInput("a"), OptionInput("b")], correct_index=0,
                      syllabus_id="s", is_annulled=True).validate()


def test_invalid_form_is_rerendered_with_errors(client):
    res = client.post("/manage/questions/new", data=NEW_QUESTION | {"statement": "", "correct": "4"})
    assert res.status_code == 422
    assert "El enunciado es obligatorio." in res.text
    assert "Marca cuál es la opción correcta" in res.text
    assert 'value="443"' in res.text  # conserva lo escrito


# --- Preguntas ---------------------------------------------------------------------

def test_create_question_with_tag_and_exam(client, db):
    exam_id = _scalar(db, "SELECT id FROM exams WHERE syllabus_id = 'uc3m-a2-gsi' ORDER BY id LIMIT 1")
    before = _scalar(db, "SELECT COUNT(*) FROM exam_questions WHERE exam_id = :e", e=exam_id)
    qid = _create(client, add_to_exam_id=str(exam_id))
    assert _scalar(db, "SELECT source FROM questions WHERE id = :q", q=qid) == "manual"
    assert _scalar(db, "SELECT COUNT(*) FROM question_options WHERE question_id = :q", q=qid) == 3
    assert _scalar(db, "SELECT display_order FROM question_options WHERE question_id = :q AND is_correct = 1", q=qid) == 1
    assert _scalar(db, "SELECT syllabus_id FROM question_syllabus_tags WHERE question_id = :q", q=qid) == "uc3m-a2-gsi"
    assert _scalar(db, "SELECT COUNT(*) FROM exam_questions WHERE exam_id = :e", e=exam_id) == before + 1
    assert client.get(f"/manage/questions/{qid}/edit").status_code == 200


def test_edit_keeps_option_ids_and_changes_correct(client, db):
    qid = _create(client)
    ids = [str(i) for i in db.execute(text(
        "SELECT id FROM question_options WHERE question_id = :q ORDER BY display_order"), {"q": qid}).scalars()]
    res = client.post(f"/manage/questions/{qid}/edit", data=NEW_QUESTION | {
        "opt_id": ids + ["", "", ""], "opt_text": ["80", "443", "21", "22", "", ""], "correct": "3",
        "block": "IV", "topic": "5"})
    assert res.status_code == 303
    db.expire_all()
    rows = db.execute(text("SELECT id, option_text, is_correct FROM question_options WHERE question_id = :q "
                           "ORDER BY display_order"), {"q": qid}).all()
    assert [str(r.id) for r in rows[:3]] == ids
    assert [r.option_text for r in rows if r.is_correct] == ["22"]
    assert _scalar(db, "SELECT pending_classification FROM questions WHERE id = :q", q=qid) == 0
    assert _scalar(db, "SELECT block || '|' || topic FROM question_syllabus_tags WHERE question_id = :q", q=qid) == "IV|5"


def test_option_chosen_in_an_attempt_cannot_be_removed_nor_question_deleted(client, db):
    qid = _create(client)
    s = client.post("/sessions/", data={"mode": "practice", "source": "questions", "source_ref": str(qid)})
    sid = re.search(r"/sessions/([0-9a-f]+)/", s.headers["location"]).group(1)
    chosen = _scalar(db, "SELECT id FROM question_options WHERE question_id = :q AND option_text = '80'", q=qid)
    client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": chosen, "n": 1},
                headers={"HX-Request": "true"})
    ids = [str(i) for i in db.execute(text(
        "SELECT id FROM question_options WHERE question_id = :q ORDER BY display_order"), {"q": qid}).scalars()]

    res = client.post(f"/manage/questions/{qid}/edit", data=NEW_QUESTION | {
        "opt_id": ids + ["", "", ""], "opt_text": ["", "443", "21", "", "", ""]})
    assert res.status_code == 422
    assert "No se puede quitar" in res.text
    assert _scalar(db, "SELECT COUNT(*) FROM question_options WHERE question_id = :q", q=qid) == 3

    res = client.post(f"/manage/questions/{qid}/delete")
    assert "an%C3%BAlala" in res.headers["location"] or "anúlala" in res.headers["location"]
    assert _scalar(db, "SELECT COUNT(*) FROM questions WHERE id = :q", q=qid) == 1


def test_delete_question_without_attempts(client, db):
    qid = _create(client)
    res = client.post(f"/manage/questions/{qid}/delete")
    assert res.status_code == 303
    for table in ("questions", "question_options", "question_syllabus_tags"):
        column = "id" if table == "questions" else "question_id"
        assert _scalar(db, f"SELECT COUNT(*) FROM {table} WHERE {column} = :q", q=qid) == 0


def test_annulled_question_leaves_the_generator(client, db):
    qid = _create(client)
    ids = [str(i) for i in db.execute(text(
        "SELECT id FROM question_options WHERE question_id = :q ORDER BY display_order"), {"q": qid}).scalars()]
    client.post(f"/manage/questions/{qid}/edit", data=NEW_QUESTION | {
        "opt_id": ids + ["", "", ""], "is_annulled": "1", "annulment_reason": "Errata"})
    from domain.sessions.generator import GeneratorFilters
    from infrastructure.db.repositories.question_repository import QuestionRepository
    db.expire_all()
    assert qid not in QuestionRepository(db).list_ids_for_generator(GeneratorFilters("uc3m-a2-gsi"))


def test_search_and_pagination(client):
    res = client.get("/manage/questions/?syllabus_id=tai-legacy&page=2")
    assert res.status_code == 200
    assert "página 2" in res.text


# --- Cuestionarios ---------------------------------------------------------------------

def test_exam_lifecycle(client, db):
    res = client.post("/manage/exams/new", data={"name": "Repaso propio", "syllabus_id": "tai-legacy",
                                                 "duration_minutes": "30"})
    assert res.status_code == 303
    exam_id = int(re.search(r"/exams/(\d+)/edit", res.headers["location"]).group(1))
    assert _scalar(db, "SELECT duration_seconds FROM exams WHERE id = :e", e=exam_id) == 1800
    assert client.post("/manage/exams/new", data={"name": "Repaso propio", "syllabus_id": "tai-legacy"}).status_code == 422

    qid = _create(client, syllabus_id="tai-legacy", add_to_exam_id=str(exam_id))
    assert "Repaso propio" in client.get("/").text
    client.post(f"/manage/exams/{exam_id}/questions/{qid}/remove")
    assert _scalar(db, "SELECT COUNT(*) FROM exam_questions WHERE exam_id = :e", e=exam_id) == 0
    assert _scalar(db, "SELECT COUNT(*) FROM questions WHERE id = :q", q=qid) == 1

    client.post(f"/manage/exams/{exam_id}/delete")
    assert _scalar(db, "SELECT COUNT(*) FROM exams WHERE id = :e", e=exam_id) == 0


def test_exam_with_sessions_cannot_be_deleted(client, db):
    client.post("/sessions/", data={"mode": "practice", "source": "exam", "source_ref": "53"})
    client.post("/manage/exams/53/delete")
    assert _scalar(db, "SELECT COUNT(*) FROM exams WHERE id = 53") == 1


def test_management_urls_are_prefixed_behind_gateway(client, monkeypatch):
    import config

    qid = _create(client)
    monkeypatch.setenv("ROOT_PATH", "/tests")
    monkeypatch.setattr(config, "ROOT_PATH", "/tests")
    pattern = re.compile(r"""(?:href|src|action|hx-get|hx-post)=["']/(?!tests/|#)([^"']*)["']""")
    for path in ("/manage/questions/", f"/manage/questions/{qid}/edit", "/manage/questions/new",
                 "/manage/exams/", "/manage/exams/53/edit", "/manage/exams/new"):
        assert pattern.findall(client.get(path).text) == [], path
