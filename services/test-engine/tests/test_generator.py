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


# --- Test ponderado por frecuencia histórica ------------------------------------

def test_weighted_flag_roundtrips_and_is_omitted_when_off():
    f = GeneratorFilters("preparatic-a1", weighted=True, count=20)
    assert "weighted=1" in f.to_source_ref()
    assert GeneratorFilters.from_source_ref(f.to_source_ref()) == f
    assert "weighted" not in GeneratorFilters("preparatic-a1").to_source_ref()


def test_question_weight_is_topic_frequency_over_available_questions():
    from domain.sessions.generator import question_weights

    tagged = [(1, "A", "1"), (2, "A", "1"), (3, "A", "1"), (4, "B", "2"), (5, "C", "3")]
    weights = question_weights(tagged, {("A", "1"): 30, ("B", "2"): 10})
    assert weights == {1: 10.0, 2: 10.0, 3: 10.0, 4: 10.0, 5: 0.0}  # cada tema suma su frecuencia


def test_weighted_sample_follows_weights_without_repeats():
    import random

    from domain.sessions.generator import weighted_sample

    rng = random.Random(1234)
    weights = {1: 9.0, 2: 1.0, 3: 0.0}
    firsts = [weighted_sample(weights, 1, rng)[0] for _ in range(4000)]
    assert 0.87 < firsts.count(1) / 4000 < 0.93
    assert 3 not in firsts  # peso 0: solo para completar
    full = weighted_sample(weights, 3, rng)
    assert sorted(full) == [1, 2, 3] and full[-1] == 3
    assert weighted_sample(weights, 10, rng).__len__() == 3


def test_weighted_test_favours_frequent_topics(svc, db):
    """PreparaTIC A1: los temas que más han caído salen más que en un test aleatorio."""
    import random

    repo = QuestionRepository(db)
    freq = repo.topic_frequencies("preparatic-a1")
    assert len(freq) == 133
    top = {k for k, _ in sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:13]}  # el 10 % de temas
    topic_of = {qid: (b, t) for qid, b, t in repo.list_tagged_for_generator(GeneratorFilters("preparatic-a1"))}
    share = sum(freq[k] for k in top) / sum(freq.values())

    random.seed(42)
    picked = []
    for _ in range(5):
        s = svc.start_session(mode="practice", source="generated",
                              source_ref=GeneratorFilters("preparatic-a1", weighted=True, count=200).to_source_ref())
        assert len(s.question_ids) == len(set(s.question_ids)) == 200
        assert "weighted=1" in s.source_ref
        picked += s.question_ids
    weighted_share = sum(topic_of[q] in top for q in picked) / len(picked)
    uniform_share = sum(topic_of[q] in top for q in topic_of) / len(topic_of)
    # Con la BD real: histórico 27,4 %, ponderado ≈26 %, aleatorio 22,8 % para el 10 % de temas que más caen.
    assert abs(weighted_share - share) < 0.03
    assert abs(weighted_share - share) < abs(uniform_share - share)


def test_weighted_combines_with_other_filters(svc):
    s = svc.start_session(mode="practice", source="generated", source_ref=GeneratorFilters(
        "preparatic-a1", block="B4", weighted=True, count=30).to_source_ref())
    assert len(s.question_ids) == 30
    with pytest.raises(NoQuestionsForFilters):
        svc.start_session(mode="practice", source="generated", source_ref=GeneratorFilters(
            "preparatic-a1", year=1999, weighted=True).to_source_ref())


def test_weighted_option_only_where_there_is_history(client):
    page = client.get("/generator/?syllabus_id=preparatic-a1").text
    assert re.search(r'name="weighted" value="1"\s*>', page)
    assert "preguntas\n        oficiales de 133 temas" in page or "oficiales de 133 temas" in page
    other = client.get("/generator/?syllabus_id=tai-legacy").text
    assert re.search(r'name="weighted" value="1" disabled', other)
    res = client.post("/generator/", data={"syllabus_id": "preparatic-a1", "weighted": "1", "count": "10",
                                           "mode": "practice"})
    assert res.status_code == 303
    history = client.get("/history/").text
    assert "ponderado por frecuencia" in history


# --- Números de las opciones condicionados a los demás filtros -----------------------

def _options(html: str, name: str) -> dict[str, int]:
    select = re.search(rf'<select id="{name}" name="{name}">(.*?)</select>', html, re.S).group(1)
    return {m.group(1): int(m.group(2))
            for m in re.finditer(r'<option value="([^"]+)"[^>]*>[^<]*\((\d+)\)</option>', select)}


def test_option_counts_match_what_you_get_when_choosing_them(client, db):
    """Con un tema elegido, cada año dice cuántas preguntas de ese tema hay ese año, y al revés."""
    repo = QuestionRepository(db)
    html = client.get("/generator/fields", params={"syllabus_id": "preparatic-a1", "scope": "B3|107"}).text
    years = _options(html, "year")
    assert years and all(n > 0 for n in years.values())            # los años sin preguntas no se ofrecen
    for year, n in years.items():
        assert n == repo.count_for_generator(GeneratorFilters("preparatic-a1", block="B3", topic="107",
                                                              year=int(year)))
    assert sum(years.values()) <= repo.count_for_generator(GeneratorFilters("preparatic-a1", block="B3", topic="107"))
    official = int(re.search(r"Solo preguntas de examen oficial \((\d+)\)", html).group(1))
    assert official == repo.count_for_generator(GeneratorFilters("preparatic-a1", block="B3", topic="107",
                                                                 official_only=True))

    html = client.get("/generator/fields", params={"syllabus_id": "preparatic-a1", "year": "2004"}).text
    scopes = _options(html, "scope")
    assert scopes["B3|107"] == 0 if "B3|107" in scopes else True   # no se ofrece un tema sin preguntas en 2004
    some = next(k for k in scopes if "|" in k)
    block, topic = some.split("|")
    assert scopes[some] == repo.count_for_generator(GeneratorFilters("preparatic-a1", block=block, topic=topic,
                                                                     year=2004))
    assert "<strong>" in html and 'id="generator-fields"' in html


def test_fields_keep_the_selection_even_when_it_leaves_no_questions(client):
    html = client.get("/generator/fields", params={"syllabus_id": "preparatic-a1", "scope": "B3|107",
                                                   "year": "2001", "official": "1", "weighted": "1",
                                                   "count": "50"}).text
    assert re.search(r'<option value="B3\|107" selected', html)
    assert re.search(r'<option value="2001" selected', html)
    assert re.search(r'name="official" value="1" checked', html)
    assert re.search(r'name="weighted" value="1" checked', html)
    assert re.search(r'<option value="50" selected', html)
    assert "ninguna cumple" in html


def test_generator_page_reacts_to_changes_with_htmx(client):
    html = client.get("/generator/?syllabus_id=preparatic-a1&scope=B3&failed=1").text
    assert 'hx-get="/generator/fields"' in html and 'hx-target="#generator-fields"' in html
    assert re.search(r'<option value="B3" selected', html)
