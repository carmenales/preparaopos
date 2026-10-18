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

        def get_question_ids_by_note(self, note_id):
            if note_id in ("tema-i-01-derecho-constitucional", "tema-i-01"):
                return [18012]
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

        # 5. Práctica por apunte: POST /sessions/practice/by-note/tema-i-01-derecho-constitucional
        # 5a. Sin seguir redirecciones: verifica el 303 que redirige a la pregunta 1
        res_by_note = client.post("/sessions/practice/by-note/tema-i-01-derecho-constitucional")
        assert res_by_note.status_code == 303
        assert re.search(r"/sessions/[^/]+/question/1$", res_by_note.headers["location"])

        # 5b. Cadena completa (POST 303 -> GET 200 a /sessions/{id}/question/1)
        res_full_chain = client.post("/sessions/practice/by-note/tema-i-01-derecho-constitucional", follow_redirects=True)
        assert res_full_chain.status_code == 200
        assert re.search(r"/sessions/[^/]+/question/1$", str(res_full_chain.url))
        assert "Pregunta" in res_full_chain.text

        # 6. Práctica por apunte sin preguntas vinculadas -> redirige a / con 303
        res_empty = client.post("/sessions/practice/by-note/no-existe", follow_redirects=True)
        assert res_empty.status_code == 200
        assert str(res_empty.url).endswith("/")

    finally:
        app.dependency_overrides.pop(get_linking_client, None)


def test_cross_navigation_graceful_degradation_when_linking_offline(client):
    """Comprueba que si linking-service está apagado, no se produce ningún error 500 y se degrada elegantemente."""
    from presentation.dependencies import get_linking_client
    from infrastructure.clients.linking_client import LinkingClient

    # Cliente real apuntando a un puerto sin servicio escuchando y con timeout corto
    dead_client = LinkingClient(base_url="http://127.0.0.1:59999", timeout=0.05)
    app.dependency_overrides[get_linking_client] = lambda: dead_client

    try:
        # 1. POST /sessions/practice/by-note con linking-service caído:
        # No debe lanzar 500; debe degradar elegantemente y terminar en GET 200 en / (POST 303 -> GET 200)
        res_dead_note = client.post("/sessions/practice/by-note/tema-i-01-derecho-constitucional", follow_redirects=True)
        assert res_dead_note.status_code == 200
        assert str(res_dead_note.url).endswith("/")

        # 2. Crear sesión de práctica y responder con linking-service caído
        res_session = client.post("/sessions/", data={"mode": "practice", "source": "exam", "source_ref": "53"})
        session_id = res_session.headers["location"].split("/sessions/")[1].split("/")[0]

        # Al responder, responde 200 sin lanzar 500 y sin pintar píldoras de apuntes
        ans_res = client.post(
            f"/sessions/{session_id}/answer",
            data={"question_id": 18012, "selected_option_id": 1, "n": 1},
        )
        assert ans_res.status_code == 200
        assert "note-pill" not in ans_res.text
        assert "note-dropdown" not in ans_res.text

        # 3. Al ver resultados, responde 200 sin lanzar 500 y sin píldoras
        res_sheet = client.get(f"/sessions/{session_id}/result")
        assert res_sheet.status_code == 200
        assert "note-pill" not in res_sheet.text
        assert "note-dropdown" not in res_sheet.text

    finally:
        app.dependency_overrides.pop(get_linking_client, None)


def test_root_path_prefix_guardian(monkeypatch):
    """Test guardián: renderizar cada página con ROOT_PATH=/tests y comprobar por regex que no queda ninguna URL interna sin el prefijo."""
    import config
    from presentation.dependencies import get_linking_client

    monkeypatch.setenv("ROOT_PATH", "/tests")
    monkeypatch.setattr(config, "ROOT_PATH", "/tests")

    class FakeLinkingClient:
        def get_links_by_question(self, question_id):
            return [{"note_id": "tema-i-01", "title": "Nota 1", "official_topic": "I.01", "confidence": 1.0}]

        def get_links_by_questions(self, q_ids):
            return {qid: self.get_links_by_question(qid) for qid in q_ids}

        def get_links_by_note(self, note_id):
            return [{"question_id": 18012, "confidence": 1.0}]

        def get_question_ids_by_note(self, note_id):
            return [18012]

    app.dependency_overrides[get_linking_client] = lambda: FakeLinkingClient()

    unprefixed_attr_pattern = re.compile(
        r"""(?:href|src|action|hx-get|hx-post)=["']/(?!tests/|#)([^"']*)["']""",
        re.IGNORECASE,
    )
    unprefixed_js_pattern = re.compile(
        r"""window\.location(?:\.href)?\s*=\s*["']/(?!tests/)([^"']*)["']""",
        re.IGNORECASE,
    )

    def assert_no_unprefixed_urls(html_content: str, context: str):
        attr_matches = unprefixed_attr_pattern.findall(html_content)
        js_matches = unprefixed_js_pattern.findall(html_content)
        assert not attr_matches, f"Encontradas URLs de atributo sin prefijo /tests/ en {context}: {attr_matches}"
        assert not js_matches, f"Encontradas URLs de JavaScript sin prefijo /tests/ en {context}: {js_matches}"

    t_client = TestClient(app, follow_redirects=False)

    try:
        # 1. Catálogo (/)
        res_cat = t_client.get("/")
        assert res_cat.status_code == 200
        assert_no_unprefixed_urls(res_cat.text, "Catálogo (/)")
        assert 'href="/tests/static/style.css"' in res_cat.text
        assert 'href="/tests/"' in res_cat.text
        assert 'action="/tests/sessions/"' in res_cat.text

        # 2. Redirección de inicio de sesión: POST /sessions/
        res_create = t_client.post(
            "/sessions/",
            data={"mode": "exam", "source": "exam", "source_ref": "53"},
        )
        assert res_create.status_code == 303
        loc_create = res_create.headers["location"]
        assert loc_create.startswith("/tests/sessions/"), f"Location sin prefijo: {loc_create}"
        assert loc_create.endswith("/question/1")
        session_id = loc_create.split("/sessions/")[1].split("/")[0]

        # 3. Pregunta 1 en modo examen con cronómetro
        res_q = t_client.get(f"/sessions/{session_id}/question/1")
        assert res_q.status_code == 200
        assert_no_unprefixed_urls(res_q.text, "Pregunta examen")
        assert f'hx-post="/tests/sessions/{session_id}/answer"' in res_q.text
        assert f'window.location.href = "/tests/sessions/{session_id}/result"' in res_q.text

        # 4. Enviar respuesta por htmx (POST /sessions/{id}/answer)
        res_ans = t_client.post(
            f"/sessions/{session_id}/answer",
            data={"question_id": 18012, "selected_option_id": 1, "n": 1},
        )
        assert res_ans.status_code == 200
        assert_no_unprefixed_urls(res_ans.text, "Feedback respuesta")
        assert f'href="/tests/sessions/{session_id}/question/2"' in res_ans.text

        # 5. Redirecciones bounds checking
        res_under = t_client.get(f"/sessions/{session_id}/question/0")
        assert res_under.status_code == 303
        assert res_under.headers["location"] == f"/tests/sessions/{session_id}/question/1"

        res_over = t_client.get(f"/sessions/{session_id}/question/9999")
        assert res_over.status_code == 303
        assert res_over.headers["location"] == f"/tests/sessions/{session_id}/result"

        # 6. Hoja de resultados (/sessions/{id}/result)
        res_res = t_client.get(f"/sessions/{session_id}/result")
        assert res_res.status_code == 200
        assert_no_unprefixed_urls(res_res.text, "Hoja de resultados")
        assert 'href="/tests/"' in res_res.text

        # 7. Práctica por apunte - resolución canónica y prefijada
        res_by_note_proc = t_client.post("/sessions/practice/by-note/tema-i-01")
        assert res_by_note_proc.status_code == 303
        assert res_by_note_proc.headers["location"].startswith("/tests/sessions/")
        assert res_by_note_proc.headers["location"].endswith("/question/1")

    finally:
        app.dependency_overrides.pop(get_linking_client, None)


