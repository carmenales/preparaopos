"""Tests de integración de la capa de presentación (FastAPI + Jinja2 + htmx)."""

from __future__ import annotations

import re
import pytest
from starlette.testclient import TestClient

from presentation.app import app


@pytest.fixture(scope="module")
def client():
    # follow_redirects=False para inspeccionar códigos 303 y cabeceras Location/Cache-Control
    return TestClient(app, follow_redirects=False)


def test_catalog_lists_available_exams(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Exámenes disponibles" in response.text
    # El examen 53 (AGE GSI 2024) debe aparecer en el catálogo
    assert "Simulacro oficial" in response.text
    assert "Práctica con corrección" in response.text


def test_create_practice_session_and_show_first_question(client):
    # 1. Crear sesión de práctica
    res = client.post(
        "/sessions/",
        data={"mode": "practice", "source": "exam", "source_ref": "53"},
    )
    assert res.status_code == 303
    location = res.headers["location"]
    assert location.endswith("/question/1")

    # 2. Cargar pregunta 1
    q_res = client.get(location)
    assert q_res.status_code == 200
    assert q_res.headers.get("cache-control") == "no-store"
    assert "question-card" in q_res.text
    # En modo práctica NO debe aparecer el temporizador visual
    assert 'id="timer"' not in q_res.text


def test_question_bounds_checking(client):
    # Crear sesión
    res = client.post(
        "/sessions/",
        data={"mode": "practice", "source": "exam", "source_ref": "53"},
    )
    location = res.headers["location"]
    session_id = location.split("/sessions/")[1].split("/")[0]

    # Bounds check: n < 1 -> /question/1
    res_under = client.get(f"/sessions/{session_id}/question/0")
    assert res_under.status_code == 303
    assert res_under.headers["location"] == f"/sessions/{session_id}/question/1"

    # Bounds check: n > total -> /result
    res_over = client.get(f"/sessions/{session_id}/question/9999")
    assert res_over.status_code == 303
    assert res_over.headers["location"] == f"/sessions/{session_id}/result"


def test_practice_mode_htmx_submit_returns_inline_feedback(client):
    # Crear sesión práctica
    res = client.post(
        "/sessions/",
        data={"mode": "practice", "source": "exam", "source_ref": "53"},
    )
    location = res.headers["location"]
    session_id = location.split("/sessions/")[1].split("/")[0]

    q_res = client.get(location)
    opts = re.findall(r'name="selected_option_id" value="(\d+)"', q_res.text)
    qid_match = re.search(r'name="question_id" value="(\d+)"', q_res.text)
    assert opts and qid_match

    qid = int(qid_match.group(1))
    opt_id = int(opts[0])

    # Enviar respuesta vía htmx
    ans_res = client.post(
        f"/sessions/{session_id}/answer",
        data={"question_id": qid, "selected_option_id": opt_id, "n": 1},
        headers={"HX-Request": "true"},
    )
    assert ans_res.status_code == 200
    assert ans_res.headers.get("cache-control") == "no-store"
    # En modo práctica se revela feedback inmediato
    assert "feedback--correct" in ans_res.text or "feedback--wrong" in ans_res.text
    assert "Siguiente →" in ans_res.text


def test_exam_mode_timer_and_no_inline_correction(client):
    # 1. Crear sesión de examen
    res = client.post(
        "/sessions/",
        data={"mode": "exam", "source": "exam", "source_ref": "53"},
    )
    assert res.status_code == 303
    location = res.headers["location"]
    session_id = location.split("/sessions/")[1].split("/")[0]

    # 2. Verificar que en modo examen SÍ tiene timer y datos de tiempo
    q_res = client.get(location)
    assert q_res.status_code == 200
    assert 'id="timer"' in q_res.text
    assert "data-seconds=" in q_res.text

    opts = re.findall(r'name="selected_option_id" value="(\d+)"', q_res.text)
    qid_match = re.search(r'name="question_id" value="(\d+)"', q_res.text)
    assert opts and qid_match

    qid = int(qid_match.group(1))

    # Obtenemos la pregunta de BD para conocer la opción correcta real
    from infrastructure.db.engine import create_sqlite_engine, session_scope
    from infrastructure.db.repositories.question_repository import QuestionRepository
    from config import SQLITE_PATH
    engine = create_sqlite_engine(SQLITE_PATH)
    with session_scope(engine) as db:
        q_repo = QuestionRepository(db)
        question = q_repo.get_by_id(qid)

    correct_opt = next(o for o in question.options if o.is_correct)
    # Elegimos deliberadamente una opción incorrecta distinta de la correcta
    wrong_opt = next(o for o in question.options if not o.is_correct)

    # 3. Enviar respuesta errónea vía htmx
    ans_res = client.post(
        f"/sessions/{session_id}/answer",
        data={"question_id": qid, "selected_option_id": wrong_opt.id, "n": 1},
        headers={"HX-Request": "true"},
    )
    assert ans_res.status_code == 200
    assert ans_res.headers.get("cache-control") == "no-store"

    # En modo examen solo se confirma guardado, NUNCA se muestra corrección ni texto de la opción correcta
    assert "feedback--saved" in ans_res.text or "Respuesta guardada" in ans_res.text
    assert "feedback--correct" not in ans_res.text
    assert "feedback--wrong" not in ans_res.text
    assert "Respuesta correcta:" not in ans_res.text
    assert "Respuesta incorrecta" not in ans_res.text

    # Anti-leak estricto: el texto de la opción correcta NO debe aparecer en el HTML devuelto
    assert correct_opt.text not in ans_res.text
    if question.justification:
        assert question.justification not in ans_res.text



def test_result_sheet_and_subsequent_question_access_redirects(client):
    # Crear sesión examen
    res = client.post(
        "/sessions/",
        data={"mode": "exam", "source": "exam", "source_ref": "53"},
    )
    location = res.headers["location"]
    session_id = location.split("/sessions/")[1].split("/")[0]

    # Ver resultados (cierra la sesión perezosamente)
    result_res = client.get(f"/sessions/{session_id}/result")
    assert result_res.status_code == 200
    assert result_res.headers.get("cache-control") == "no-store"
    assert "scoreboard" in result_res.text
    assert "Desglose" in result_res.text
    assert "Total evaluable:" in result_res.text

    # Al haber cerrado la sesión, cualquier intento de ir a una pregunta redirige a resultados
    q_after_close = client.get(f"/sessions/{session_id}/question/1")
    assert q_after_close.status_code == 303
    assert q_after_close.headers["location"] == f"/sessions/{session_id}/result"


def test_cross_navigation_ui_components(client):
    from presentation.dependencies import get_linking_client

    class FakeLinkingClient:
        def get_links_by_question(self, q_id):
            if q_id == 18012:
                return [{
                    "note_id": "tema-i-01-derecho-constitucional",
                    "title": "Tema I.01 Derecho Constitucional",
                    "official_topic": "I.01 Derecho Constitucional",
                    "confidence": 1.0,
                }]
            elif q_id == 18044:
                return [
                    {
                        "note_id": "tema-i-09-admin-digital",
                        "title": "Tema I.09 Administración Digital",
                        "official_topic": "I.09.II Administración Digital",
                        "confidence": 0.8,
                    },
                    {
                        "note_id": "tema-i-09-ens-eni",
                        "title": "Tema I.09 ENS-ENI",
                        "official_topic": "I.09.II ENS-ENI",
                        "confidence": 0.8,
                    },
                ]
            return []

        def get_links_by_questions(self, q_ids):
            return {qid: self.get_links_by_question(qid) for qid in q_ids}

        def get_links_by_note(self, note_id):
            if note_id == "tema-i-01-derecho-constitucional":
                return [{"question_id": 18012, "confidence": 1.0}]
            return []

    app.dependency_overrides[get_linking_client] = lambda: FakeLinkingClient()

    try:
        # 1. Crear sesión de práctica
        res = client.post("/sessions/", data={"mode": "practice", "source": "exam", "source_ref": "53"})
        session_id = res.headers["location"].split("/sessions/")[1].split("/")[0]

        # 2. Responder pregunta 18012 (enlace único -> note-pill)
        ans_single = client.post(
            f"/sessions/{session_id}/answer",
            data={"question_id": 18012, "selected_option_id": 1, "n": 1},
        )
        assert ans_single.status_code == 200
        assert "note-pill" in ans_single.text
        assert "tema-i-01-derecho-constitucional" in ans_single.text
        assert "note-dropdown" not in ans_single.text

        # 3. Responder pregunta 18044 (enlace múltiple -> note-dropdown)
        ans_multi = client.post(
            f"/sessions/{session_id}/answer",
            data={"question_id": 18044, "selected_option_id": 1, "n": 2},
        )
        assert ans_multi.status_code == 200
        assert "note-dropdown" in ans_multi.text
        assert "Ver apuntes relacionados (2)" in ans_multi.text
        assert "tema-i-09-admin-digital" in ans_multi.text
        assert "tema-i-09-ens-eni" in ans_multi.text

        # 4. Ver hoja de resultados y comprobar que incluye los enlaces
        res_sheet = client.get(f"/sessions/{session_id}/result")
        assert res_sheet.status_code == 200
        assert "note-pill" in res_sheet.text
        assert "note-dropdown" in res_sheet.text

        # 5. Práctica por apunte: GET /practice/by-note/tema-i-01-derecho-constitucional
        res_by_note = client.get("/practice/by-note/tema-i-01-derecho-constitucional")
        assert res_by_note.status_code == 303
        loc = res_by_note.headers["location"]
        # Redirige a /sessions/practice/... o /sessions/{id}/question/1
        assert "/question/1" in loc or "/sessions/practice" in loc

        # 6. Práctica por apunte sin preguntas vinculadas -> redirige a /
        res_empty = client.get("/practice/by-note/no-existe")
        assert res_empty.status_code == 303

    finally:
        app.dependency_overrides.pop(get_linking_client, None)

