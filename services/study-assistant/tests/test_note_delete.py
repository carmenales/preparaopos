"""Borrar un apunte: confirmación, borrado por ruta, enlaces y fallos de los servicios."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import pytest
from starlette.testclient import TestClient

from domain.notes.models import Note
from domain.notes.service import NoteService
from infrastructure.knowledge_service.client import KnowledgeServiceError
from main import app
from presentation.routes.ingest import get_knowledge_client
from presentation.routes.note_delete import get_linking_client

GSI = "knowledge/processes/age/a2-gsi/apuntes"
NOTES = [
    Note(id="tema-i-01", title="Tema I.01 Constitución", path=f"{GSI}/tema-i-01.md", processes=["age/a2-gsi"]),
    Note(id="dup", title="Tema 16 ampliado", path=f"{GSI}/dup-ampliado.md", processes=["age/a2-gsi"]),
    Note(id="dup", title="Tema 16", path=f"{GSI}/dup.md", processes=["age/a2-gsi"]),
]


class FakeKnowledge:
    def __init__(self):
        self.deleted: list[str] = []
        self.fail = False

    def delete_note(self, path):
        if self.fail:
            raise KnowledgeServiceError("No se puede contactar con el servicio de ingesta (knowledge-service).")
        self.deleted.append(path)
        return {"success": True, "file_path": path, "index_rebuilt": True, "warnings": []}


class FakeLinking:
    def __init__(self, count=3, down=False):
        self.count, self.down = count, down
        self.purged: list[str] = []

    def count_links_by_note(self, note_id):
        return None if self.down else self.count

    def delete_links_by_note(self, note_id):
        if self.down:
            return False
        self.purged.append(note_id)
        return True


@pytest.fixture
def env(monkeypatch):
    knowledge, linking = FakeKnowledge(), FakeLinking()
    app.dependency_overrides[get_knowledge_client] = lambda: knowledge
    app.dependency_overrides[get_linking_client] = lambda: linking
    with TestClient(app, follow_redirects=False) as client:
        original = app.state.note_service
        app.state.note_service = NoteService(list(NOTES))

        def reload_notes():  # lo que haría recargar el índice que regenera knowledge-service
            app.state.note_service = NoteService([n for n in NOTES if n.path not in knowledge.deleted])

        monkeypatch.setattr(app.state, "reload_notes", reload_notes)
        client.real_notes = original
        yield client, knowledge, linking
        app.state.note_service = original
    app.dependency_overrides.pop(get_knowledge_client, None)
    app.dependency_overrides.pop(get_linking_client, None)


def test_confirmation_page_warns_about_linked_questions(env):
    client, knowledge, _ = env
    res = client.get("/notes/tema-i-01/delete", params={"path": f"{GSI}/tema-i-01.md"})
    assert res.status_code == 200
    assert "Se borra definitivamente" in res.text and "3 preguntas enlazadas" in res.text
    assert f'name="path" value="{GSI}/tema-i-01.md"' in res.text
    assert knowledge.deleted == []  # la página de confirmación no borra nada


def test_delete_removes_file_links_and_returns_to_its_process(env):
    client, knowledge, linking = env
    res = client.post("/notes/tema-i-01/delete", data={"path": f"{GSI}/tema-i-01.md"})
    assert res.status_code == 303
    query = parse_qs(urlparse(res.headers["location"]).query)
    assert query == {"deleted": ["Tema I.01 Constitución"], "process": ["age/a2-gsi"]}
    assert knowledge.deleted == [f"{GSI}/tema-i-01.md"] and linking.purged == ["tema-i-01"]
    assert app.state.note_service.find_by_id("tema-i-01") is None
    assert client.get("/notes/tema-i-01/delete").status_code == 404


def test_duplicate_id_deletes_only_that_file_and_keeps_links(env):
    client, knowledge, linking = env
    page = client.get("/notes/dup/delete", params={"path": f"{GSI}/dup-ampliado.md"}).text
    assert "1 apunte más con el mismo id" in page
    client.post("/notes/dup/delete", data={"path": f"{GSI}/dup-ampliado.md"})
    assert knowledge.deleted == [f"{GSI}/dup-ampliado.md"]
    assert linking.purged == []  # siguen siendo los enlaces del otro apunte «dup»
    assert app.state.note_service.find_by_id("dup").path == f"{GSI}/dup.md"


def test_path_must_belong_to_the_note(env):
    client, knowledge, _ = env
    assert client.post("/notes/tema-i-01/delete", data={"path": f"{GSI}/dup.md"}).status_code == 404
    assert knowledge.deleted == []


def test_knowledge_service_down_keeps_the_note(env):
    client, knowledge, linking = env
    knowledge.fail = True
    res = client.post("/notes/tema-i-01/delete", data={"path": f"{GSI}/tema-i-01.md"})
    assert res.status_code == 502 and "No se ha borrado" in res.text
    assert linking.purged == [] and app.state.note_service.find_by_id("tema-i-01") is not None


def test_linking_down_still_deletes_and_warns(env):
    client, knowledge, linking = env
    linking.down = True
    assert "No se sabe cuántas preguntas" in client.get("/notes/tema-i-01/delete").text
    res = client.post("/notes/tema-i-01/delete", data={"path": f"{GSI}/tema-i-01.md"})
    assert knowledge.deleted == [f"{GSI}/tema-i-01.md"]
    home = client.get(res.headers["location"]).text
    assert "Apunte «Tema I.01 Constitución» borrado." in home and "No se han podido borrar sus enlaces" in home


def test_note_page_links_to_delete(env):
    client, _, _ = env
    # El visor lee el fichero del disco: se usa un apunte real del índice.
    app.state.note_service = client.real_notes
    note = next((n for n in client.real_notes.notes if client.real_notes.find_by_id(n.id) is n), None)
    if note is None:
        pytest.skip("Índice de apuntes vacío en este entorno")
    res = client.get(f"/notes/{note.id}")
    if res.status_code == 404:
        pytest.skip("El fichero del apunte no está en este entorno")
    assert f"/notes/{note.id}/delete?path=" in res.text
