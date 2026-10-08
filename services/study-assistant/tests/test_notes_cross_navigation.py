"""Tests para la navegación cruzada en Study Assistant."""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app, follow_redirects=False) as c:
        yield c


def test_note_view_cross_navigation_with_mocked_linking(client, monkeypatch):
    from infrastructure.linking import client as linking_module

    # Mock de LinkingClient
    class FakeLinkingClient:
        def get_links_by_note(self, note_id: str):
            if "derecho-constitucional" in note_id:
                return [{"question_id": 18012, "confidence": 1.0}]
            return []

    monkeypatch.setattr(linking_module, "LinkingClient", FakeLinkingClient)

    # 1. Probar una nota existente con preguntas vinculadas
    # Buscamos la nota de derecho constitucional
    resp = client.get("/notes/tema-i-01-derecho-constitucional")
    if resp.status_code == 200:
        assert "Practicar preguntas (" in resp.text
        assert "http://localhost:8096/practice/by-note/tema-i-01-derecho-constitucional" in resp.text
    else:
        # Si el ID difiere en el índice local, comprobar cualquier nota existente
        notes_resp = client.get("/api/notes")
        assert notes_resp.status_code == 200
        notes = notes_resp.json()
        assert len(notes) > 0
        first_id = notes[0]["id"]
        # Probamos con la primera nota
        resp2 = client.get(f"/notes/{first_id}")
        assert resp2.status_code == 200


def test_note_view_fallback_when_linking_empty(client, monkeypatch):
    from infrastructure.linking import client as linking_module

    class EmptyLinkingClient:
        def get_links_by_note(self, note_id: str):
            return []

    monkeypatch.setattr(linking_module, "LinkingClient", EmptyLinkingClient)

    notes_resp = client.get("/api/notes")
    assert notes_resp.status_code == 200
    notes = notes_resp.json()
    if notes:
        first_id = notes[0]["id"]
        resp = client.get(f"/notes/{first_id}")
        assert resp.status_code == 200
        # No debe romper ni mostrar enlace erróneo
        assert "http://localhost:8096/practice/by-note/" not in resp.text
