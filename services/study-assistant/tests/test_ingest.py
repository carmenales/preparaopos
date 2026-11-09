"""Asistente de ingesta: subir PDF, revisar, refinar y publicar (knowledge-service simulado)."""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from infrastructure.knowledge_service.client import KnowledgeServiceError
from main import app
from presentation.routes.ingest import get_knowledge_client

PDF = b"%PDF-1.4 contenido de prueba"


class FakeKnowledgeClient:
    def __init__(self, fail: str | None = None):
        self.fail = fail
        self.published: list[dict] = []

    def extract_pdf(self, pdf_bytes, filename, normalize=True):
        if self.fail == "extract":
            raise KnowledgeServiceError("No se puede contactar con el servicio de ingesta (knowledge-service).")
        return {"markdown": "## Tema 9\n\nTexto **extraído**.\n\n| a | b |\n|---|---|\n| 1 | 2 |",
                "detected_title": "Tema 9 Prueba", "official_topic": "I.09", "page_count": 3,
                "headings": ["Tema 9"], "warnings": []}

    def refine(self, markdown, instructions=""):
        if self.fail == "refine":
            raise KnowledgeServiceError("El servicio de ingesta ha devuelto un error (502): Ollama no responde")
        return {"refined_markdown": markdown + "\n\nREFINADO", "warnings": []}

    def publish(self, payload):
        self.published.append(payload)
        return {"success": True, "note_id": "nota-publicada", "slug": "nota-publicada", "file_path": "x.md",
                "index_rebuilt": True, "note_url": "", "warnings": []}


@pytest.fixture
def fake():
    return FakeKnowledgeClient()


@pytest.fixture
def client(fake, monkeypatch):
    app.dependency_overrides[get_knowledge_client] = lambda: fake
    with TestClient(app, follow_redirects=False) as c:
        reloads = []
        monkeypatch.setattr(app.state, "reload_notes", lambda: reloads.append(1))
        c.reloads = reloads
        yield c
    app.dependency_overrides.pop(get_knowledge_client, None)


def _extract(client, **data):
    return client.post("/ingest/extract", files={"pdf_file": ("tema.pdf", PDF, "application/pdf")},
                       data={"process_slug": "age/a2-gsi", "source": "cetic", "normalize": "true"} | data)


def test_upload_page_and_nav_link(client):
    res = client.get("/ingest/")
    assert res.status_code == 200
    assert 'name="pdf_file"' in res.text
    assert 'value="age/a2-gsi"' in res.text
    assert 'href="/ingest/"' in client.get("/").text


def test_extract_shows_review_with_preview(client):
    res = _extract(client)
    assert res.status_code == 200
    assert 'value="Tema 9 Prueba"' in res.text
    assert 'value="I.09"' in res.text
    assert "<table" in res.text  # vista previa renderizada
    assert 'name="process_slug" value="age/a2-gsi"' in res.text


def test_extract_validations(client):
    assert _extract(client, process_slug="").status_code == 422
    res = client.post("/ingest/extract", files={"pdf_file": ("x.txt", b"hola", "text/plain")},
                      data={"process_slug": "age/a2-gsi"})
    assert res.status_code == 422
    assert "debe ser un PDF" in res.text


def test_custom_process(client):
    res = _extract(client, process_slug="__otro__", custom_process="/age/c1-tai/")
    assert 'name="process_slug" value="age/c1-tai"' in res.text


def test_extract_when_service_is_down(client, fake):
    fake.fail = "extract"
    res = _extract(client)
    assert res.status_code == 502
    assert "No se puede contactar" in res.text


def test_preview_fragment(client):
    res = client.post("/ingest/preview", data={"markdown": "## Hola\n\n- uno"})
    assert res.status_code == 200
    assert "<h2" in res.text and "<li>uno</li>" in res.text


def test_refine_ok_and_failure_keeps_text(client, fake):
    ok = client.post("/ingest/refine", data={"markdown": "Texto original"})
    assert "REFINADO" in ok.text and "Texto refinado" in ok.text
    fake.fail = "refine"
    ko = client.post("/ingest/refine", data={"markdown": "Texto original"})
    assert ko.status_code == 200
    assert "Texto original" in ko.text and "Se conserva el texto sin refinar" in ko.text


def test_publish_reloads_index_and_redirects_to_note(client, fake):
    res = client.post("/ingest/publish", data={
        "process_slug": "age/a2-gsi", "source": "cetic", "title": "Tema 9", "official_topic": "I.09",
        "tags": "ENS, Seguridad , ", "status": "revisado", "markdown": "## Tema 9"})
    assert res.status_code == 303
    assert res.headers["location"] == "/notes/nota-publicada?published=1"
    assert fake.published[0]["tags"] == ["ens", "seguridad"]
    assert fake.published[0]["status"] == "revisado"
    assert client.reloads == [1]


def test_publish_validation_keeps_form(client, fake):
    res = client.post("/ingest/publish", data={"process_slug": "age/a2-gsi", "title": "", "markdown": "Mi texto"})
    assert res.status_code == 422
    assert "El título es obligatorio." in res.text
    assert "Mi texto" in res.text
    assert fake.published == []


def test_ai_cleaned_only_after_refine_and_review_flag_from_user(client, fake):
    base = {"process_slug": "age/a2-gsi", "source": "cetic", "title": "Tema 9", "status": "borrador",
            "markdown": "## Tema 9"}
    client.post("/ingest/publish", data=base)
    assert fake.published[-1]["ai_cleaned"] is False
    assert fake.published[-1]["needs_human_review"] is False

    refined = client.post("/ingest/refine", data={"markdown": "## Tema 9"}).text
    assert 'name="ai_cleaned" value="1"' in refined
    client.post("/ingest/publish", data=base | {"ai_cleaned": "1", "needs_human_review": "1"})
    assert fake.published[-1]["ai_cleaned"] is True
    assert fake.published[-1]["needs_human_review"] is True

    failed = FakeKnowledgeClient(fail="refine")
    app.dependency_overrides[get_knowledge_client] = lambda: failed
    assert 'name="ai_cleaned"' not in client.post("/ingest/refine", data={"markdown": "x"}).text
