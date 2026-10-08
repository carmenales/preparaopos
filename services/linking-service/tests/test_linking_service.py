"""Tests unitarios y de integración para linking-service."""

from __future__ import annotations

import sqlite3
import pytest
from starlette.testclient import TestClient

from domain.service import LinkingService, extract_block_and_topic
from infrastructure.db.repository import QuestionNoteLinkRepository


class FakeApuntesClient:
    def __init__(self, notes: list[dict] | None = None) -> None:
        self.notes = notes or [
            {
                "id": "tema-i-01-constitución",
                "title": "La Constitución Española de 1978",
                "official_topic": "I.01 Derecho Constitucional",
                "processes": ["age/a2-gsi"],
            },
            {
                "id": "tema-i-09-admin-digital",
                "title": "Administración Digital",
                "official_topic": "TEMA I.09 ADMINISTRACIÓN DIGITAL",
                "processes": ["age/a2-gsi"],
            },
            {
                "id": "tema-i-09-ens-eni",
                "title": "ENS y ENI",
                "official_topic": "TEMA I.09.II ENS Y ENI",
                "processes": ["age/a2-gsi"],
            },
        ]

    def get_notes_by_process(self, process: str = "") -> list[dict]:
        return self.notes

    def get_note(self, note_id: str) -> dict | None:
        return next((n for n in self.notes if n["id"] == note_id), None)


class FakeTestEngineClient:
    def __init__(self, tags: list[dict] | None = None, questions: dict | None = None) -> None:
        self.tags = tags or [
            {"question_id": 101, "syllabus_id": "age-gsi-official", "block": "I", "topic": "1"},
            {"question_id": 102, "syllabus_id": "age-gsi-official", "block": "I", "topic": "9"},
            {"question_id": 103, "syllabus_id": "age-gsi-official", "block": "IV", "topic": "99"},  # Sin nota
        ]
        self.questions = questions or {
            101: {"id": 101, "statement": "¿Quién sanciona las leyes?", "excerpt": "¿Quién sanciona...", "exam_name": "AGE GSI 2024"},
            102: {"id": 102, "statement": "¿Qué es el ENS?", "excerpt": "¿Qué es el ENS?...", "exam_name": "AGE GSI 2024"},
            103: {"id": 103, "statement": "Pregunta sin tema", "excerpt": "Pregunta...", "exam_name": "AGE GSI 2024"},
        }

    def get_syllabus_tags(self, syllabus_id: str) -> list[dict]:
        return self.tags

    def get_question(self, question_id: int) -> dict | None:
        return self.questions.get(question_id)


@pytest.fixture
def memory_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE question_note_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            note_id TEXT NOT NULL,
            syllabus_id TEXT NOT NULL,
            confidence REAL,
            source TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(question_id, note_id)
        );
    """)
    yield conn
    conn.close()


def test_extract_block_and_topic():
    assert extract_block_and_topic("TEMA III.12 APLICACIONES WEB") == ("III", "12")
    assert extract_block_and_topic("Tema I.02 Derecho Constitucional") == ("I", "2")
    assert extract_block_and_topic("I.01_DerechoConstitucional") == ("I", "1")
    assert extract_block_and_topic("TEMA I.09.II ENS") == ("I", "9")
    assert extract_block_and_topic("ESQUEMA NACIONAL DE SEGURIDAD") == (None, None)
    assert extract_block_and_topic(None, "Tema_III.02.1_Gestion") == ("III", "2")


def test_repository_upsert_and_query(memory_db):
    repo = QuestionNoteLinkRepository(memory_db)
    assert repo.count() == 0

    repo.upsert_link(
        question_id=1,
        note_id="note-1",
        syllabus_id="age-gsi-official",
        confidence=1.0,
        source="topic-match",
    )
    assert repo.count() == 1

    # Idempotencia: el segundo upsert no duplica filas
    repo.upsert_link(
        question_id=1,
        note_id="note-1",
        syllabus_id="age-gsi-official",
        confidence=0.9,
        source="manual",
    )
    assert repo.count() == 1

    links_q = repo.get_by_question_id(1)
    assert len(links_q) == 1
    assert links_q[0]["confidence"] == 0.9
    assert links_q[0]["source"] == "manual"

    links_n = repo.get_by_note_id("note-1")
    assert len(links_n) == 1
    assert links_n[0]["question_id"] == 1


def test_linking_service_resolution_rules(memory_db):
    repo = QuestionNoteLinkRepository(memory_db)
    ap_client = FakeApuntesClient()
    te_client = FakeTestEngineClient()

    service = LinkingService(repo, ap_client, te_client)
    res = service.resolve_topic_matches(
        syllabus_id="age-gsi-official",
        process_slug="age/a2-gsi",
    )

    assert res["total_evaluated"] == 3
    # Pregunta 101: tema I.1 coincide con exactamente 1 nota -> confianza 1.0
    assert res["exact_matches"] == 1
    links_101 = repo.get_by_question_id(101)
    assert len(links_101) == 1
    assert links_101[0]["confidence"] == 1.0
    assert links_101[0]["source"] == "topic-match"

    # Pregunta 102: tema I.9 coincide con 2 notas (admin digital y ens-eni) -> confianza 0.8
    assert res["multi_matches"] == 1
    links_102 = repo.get_by_question_id(102)
    assert len(links_102) == 2
    for l in links_102:
        assert l["confidence"] == 0.8
        assert l["source"] == "topic-match"

    # Pregunta 103: tema IV.99 no coincide con ninguna nota -> 0 matches
    assert res["zero_matches"] == 1
    assert len(repo.get_by_question_id(103)) == 0


def test_linking_api_endpoints(memory_db):
    from presentation.app import app

    repo = QuestionNoteLinkRepository(memory_db)
    ap_client = FakeApuntesClient()
    te_client = FakeTestEngineClient()
    service = LinkingService(repo, ap_client, te_client)

    # Poblamos algunos enlaces
    repo.upsert_link(question_id=101, note_id="tema-i-01-constitución", syllabus_id="age-gsi-official", confidence=1.0, source="topic-match")

    # Inyectamos en el estado de la app
    app.state.db_conn = memory_db
    app.state.repo = repo
    app.state.linking_service = service

    client = TestClient(app)

    # 1. GET /links/by-question/{id}
    resp_q = client.get("/links/by-question/101")
    assert resp_q.status_code == 200
    data_q = resp_q.json()
    assert len(data_q) == 1
    assert data_q[0]["note_id"] == "tema-i-01-constitución"
    assert data_q[0]["title"] == "La Constitución Española de 1978"
    assert data_q[0]["confidence"] == 1.0

    # 2. GET /links/by-note/{note_id}
    resp_n = client.get("/links/by-note/tema-i-01-constitución")
    assert resp_n.status_code == 200
    data_n = resp_n.json()
    assert len(data_n) == 1
    assert data_n[0]["question_id"] == 101
    assert data_n[0]["exam_name"] == "AGE GSI 2024"
    assert data_n[0]["confidence"] == 1.0

    # 3. POST /links/by-questions
    resp_batch = client.post("/links/by-questions", json={"question_ids": [101, 999]})
    assert resp_batch.status_code == 200
    data_batch = resp_batch.json()
    assert "101" in data_batch
    assert len(data_batch["101"]) == 1
    assert data_batch["101"][0]["note_id"] == "tema-i-01-constitución"
    assert "999" in data_batch
    assert len(data_batch["999"]) == 0

    # 4. GET /health
    resp_h = client.get("/health")
    assert resp_h.status_code == 200
    assert resp_h.json()["links_count"] == 1
