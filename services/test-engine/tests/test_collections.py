"""Tests fijos por colección (menú «Tests»: Aleatorios, Relevancia, Bloques, Temas, Años) e Inicio."""

from __future__ import annotations

import json
import re

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from config import SQLITE_PATH
from domain.sessions.collections import COLLECTION_SIZE, RELEVANCE_TESTS, build_collection, fixed_test_title
from domain.sessions.generator import GeneratorFilters, fixed_part, stable_order

A1 = "preparatic-a1"


# --- Dominio (sin BD) -----------------------------------------------------------

def test_part_roundtrips_and_fits_in_source_ref():
    f = GeneratorFilters(A1, block="B3", topic="106", weighted=True, count=100, part=50)
    assert GeneratorFilters.from_source_ref(f.to_source_ref()) == f
    assert len(f.to_source_ref()) <= 128
    assert GeneratorFilters(A1, part=3).collection_seed == GeneratorFilters(A1, part=7).collection_seed
    with pytest.raises(ValueError):
        GeneratorFilters(A1, part=0)


def test_stable_order_is_fixed_and_keeps_relative_order_when_questions_are_added():
    ids = list(range(1, 500))
    order = stable_order(ids, "seed")
    assert order == stable_order(list(reversed(ids)), "seed") and sorted(order) == ids
    assert order != ids and order != stable_order(ids, "otra")
    with_new = stable_order(ids + [1000, 1001], "seed")
    assert [i for i in with_new if i < 1000] == order


def test_fixed_parts_split_the_pool_without_repeating():
    ids = list(range(1, 251))
    parts = [fixed_part(ids, GeneratorFilters(A1, count=100, part=p)) for p in (1, 2, 3)]
    assert [len(p) for p in parts] == [100, 100, 50]
    assert sorted(sum(parts, [])) == ids
    assert fixed_part(ids, GeneratorFilters(A1, count=100, part=4)) == []


def test_titles_and_collection_sizes():
    facets = {"blocks": [{"block": "A1", "count": 250, "topics": [{"topic": "1", "count": 120}]}],
              "years": [{"year": 2024, "count": 80}], "weighted": {"questions": 10}}
    random_tests = build_collection("random", A1, 250, facets)
    assert [t.title for t in random_tests] == ["Test Aleatorio #1", "Test Aleatorio #2", "Test Aleatorio #3"]
    assert [t.questions for t in random_tests] == [100, 100, 50]
    assert [t.title for t in build_collection("blocks", A1, 250, facets)][-1] == "Test Bloque A1 #3"
    assert [t.title for t in build_collection("topics", A1, 250, facets)] == ["Test Tema 1 #1", "Test Tema 1 #2"]
    assert [t.title for t in build_collection("years", A1, 250, facets)] == ["Test 2024 #1"]
    assert len(build_collection("relevance", A1, 250, facets)) == RELEVANCE_TESTS
    assert build_collection("relevance", A1, 250, {**facets, "weighted": None}) == []
    assert fixed_test_title(GeneratorFilters(A1, weighted=True, part=2)) == "Test Ponderado #2"
    with pytest.raises(ValueError):
        build_collection("nope", A1, 1, facets)


# --- Páginas y sesiones (BD real) -------------------------------------------------

@pytest.fixture
def client():
    from presentation.app import app

    created: list[str] = []
    with TestClient(app) as c:
        c.created = created
        yield c
    engine = create_engine(f"sqlite:///{SQLITE_PATH}")
    with Session(engine) as db:
        for sid in created:
            db.execute(text("DELETE FROM test_attempts WHERE test_session_id = :id"), {"id": sid})
            db.execute(text("DELETE FROM test_sessions WHERE id = :id"), {"id": sid})
        db.commit()


def _start(client, ref):
    res = client.post("/collections/start", data={"ref": ref}, follow_redirects=False)
    assert res.status_code == 303
    sid = res.headers["location"].rsplit("/", 1)[-1]
    if sid not in client.created:
        client.created.append(sid)
    return sid


def _question_ids(sid):
    engine = create_engine(f"sqlite:///{SQLITE_PATH}")
    with Session(engine) as db:
        return json.loads(db.execute(text("SELECT question_ids FROM test_sessions WHERE id = :id"), {"id": sid}).scalar())


def test_random_collection_page_start_continue_and_repeat(client):
    page = client.get(f"/collections/random?syllabus_id={A1}")
    assert page.status_code == 200 and "Tests aleatorios" in page.text
    assert "Test Aleatorio #1" in page.text and "Sin hacer" in page.text
    assert page.cookies.get("te_syllabus") == A1 or "te_syllabus" in page.headers.get("set-cookie", "")
    ref = re.search(r'name="ref" value="([^"]+)"', page.text)[1].replace("&amp;", "&")
    assert GeneratorFilters.from_source_ref(ref).part == 1

    sid = _start(client, ref)
    first = _question_ids(sid)
    assert len(first) == COLLECTION_SIZE
    assert _start(client, ref) == sid                       # sin terminar: «Continuar» lo retoma
    assert "En curso" in client.get(f"/collections/random?syllabus_id={A1}").text

    client.post(f"/sessions/{sid}/close")
    page = client.get(f"/collections/random?syllabus_id={A1}").text
    assert "Repetir" in page and "pill--red" in page           # nota 0: todo en blanco
    again = _start(client, ref)
    assert again != sid and _question_ids(again) == first      # mismo test, mismas preguntas

    history = client.get("/history/").text
    assert "A1 TIC AGE · Test Aleatorio #1" in history
    assert "Test Aleatorio #1" in client.get(f"/sessions/{again}").text


def test_block_topic_and_year_pages_use_syllabus_names(client):
    blocks = client.get(f"/collections/blocks?syllabus_id={A1}").text
    assert "Test Bloque A1 #1" in blocks and "I. Marco Constitucional Español y Unión Europea" in blocks
    topics = client.get(f"/collections/topics?syllabus_id={A1}").text
    assert "Test Tema 130 #1" in topics and "Videoconferencia." in topics
    assert "Test 2024 #1" in client.get(f"/collections/years?syllabus_id={A1}").text
    assert "Test Ponderado #1" in client.get(f"/collections/relevance?syllabus_id={A1}").text


def test_collection_without_data_and_unknown_kind(client):
    page = client.get("/collections/blocks?syllabus_id=uc3m-a2-gsi").text
    assert "no están clasificadas por bloque" in page
    assert client.get("/collections/nope").status_code == 404
    assert client.post("/collections/start", data={"ref": f"syllabus={A1}&n=100"}).status_code == 400


def test_home_explains_the_app_and_lists_unfinished_tests(client):
    page = client.get(f"/collections/years?syllabus_id={A1}").text
    sid = _start(client, re.search(r'name="ref" value="([^"]+)"', page)[1].replace("&amp;", "&"))
    home = client.get("/home").text
    assert "Cómo funciona" in home and "Modo Entrenamiento" in home
    assert "Tests sin terminar" in home and f'href="/sessions/{sid}"' in home
    assert 'href="/collections/relevance"' in client.get("/").text   # menú «Tests»
