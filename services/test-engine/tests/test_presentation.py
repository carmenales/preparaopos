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


def _start(client, mode="practice", ref="53"):
    res = client.post("/sessions/", data={"mode": mode, "source": "exam", "source_ref": ref})
    assert res.status_code == 303
    return res, res.headers["location"].rstrip("/").split("/sessions/")[1]


def _card_html(html, n):
    """La etiqueta de apertura y el contenido de la tarjeta n (sin las vecinas)."""
    return re.search(rf'<li class="tq[^"]*"\s+id="q-{n}">.*?</li>', html, re.S).group(0)


def _first_question(html):
    """(id de la pregunta, ids de sus opciones) de la primera tarjeta de la página."""
    card = re.search(r'<li class="tq[^"]*"\s+id="q-1">(.*?)</li>', html, re.S).group(1)
    pairs = re.findall(r'"question_id": "(\d+)", "selected_option_id": "(\d+)"', card)
    return int(pairs[0][0]), [int(o) for _, o in pairs]


def _question(qid):
    from config import SQLITE_PATH
    from infrastructure.db.engine import create_sqlite_engine, session_scope
    from infrastructure.db.repositories.question_repository import QuestionRepository

    with session_scope(create_sqlite_engine(SQLITE_PATH)) as db:
        return QuestionRepository(db).get_by_id(qid)


def test_create_session_opens_the_whole_test_in_one_page(client):
    res, sid = _start(client)
    assert res.headers["location"] == f"/sessions/{sid}"
    page = client.get(res.headers["location"])
    assert page.status_code == 200
    assert page.headers.get("cache-control") == "no-store"
    assert page.text.count('class="tq__statement"') == len(re.findall(r'id="q-\d+"', page.text)) > 1
    assert "Dejar en blanco" not in page.text                  # no es una opción más
    assert 'id="test-summary"' in page.text and "Corregir" in page.text
    assert 'name="instant" value="1"' in page.text and "checked" in page.text   # práctica: corrige al responder
    assert 'data-running="false"' in page.text                  # práctica: cronómetro parado hasta «Empezar»


def test_old_question_links_go_to_the_question_inside_the_page(client):
    _, sid = _start(client)
    res = client.get(f"/sessions/{sid}/question/7")
    assert res.status_code == 303 and res.headers["location"] == f"/sessions/{sid}#q-7"
    assert client.get(f"/sessions/{sid}/question/1?requested=200").headers["location"] == f"/sessions/{sid}?requested=200#q-1"


def test_click_answers_and_click_again_leaves_it_blank_when_correcting_at_the_end(client):
    _, sid = _start(client, mode="exam")
    qid, options = _first_question(client.get(f"/sessions/{sid}").text)
    question = _question(qid)
    wrong = next(o for o in question.options if not o.is_correct)

    res = client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": wrong.id})
    assert res.status_code == 200 and res.headers.get("cache-control") == "no-store"
    assert 'id="q-1"' in res.text and 'hx-swap-oob="true"' in res.text
    assert re.search(r"<strong>1</strong>/\d+ contestadas", res.text)
    # Corrección al final: ni veredicto, ni la correcta, ni la explicación (sin filtraciones)
    assert "Correcta" not in res.text and "Incorrecta" not in res.text and "opt--right" not in res.text
    if question.justification:
        assert question.justification not in res.text
    assert "↺ Borrar respuesta" in res.text

    again = client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": wrong.id})
    assert re.search(r"<strong>0</strong>/\d+ contestadas", again.text)
    assert "opt--selected" not in again.text

    client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": wrong.id})
    cleared = client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": ""})
    assert re.search(r"<strong>0</strong>/\d+ contestadas", cleared.text)


def test_practice_corrects_on_answer_and_locks_the_question(client):
    _, sid = _start(client)
    qid, _ = _first_question(client.get(f"/sessions/{sid}").text)
    question = _question(qid)
    correct = next(o for o in question.options if o.is_correct)
    wrong = next(o for o in question.options if not o.is_correct)

    res = client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": wrong.id})
    assert "❌ Incorrecta" in res.text and "opt--right" in res.text and "opt--bad" in res.text
    assert "Nota ahora:" in res.text
    assert "no se puede cambiar" in res.text and "↺ Borrar respuesta" not in res.text
    # Ya corregida: pulsar otra opción no cambia la respuesta
    locked = client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": correct.id})
    assert "❌ Incorrecta" in locked.text


def test_option_must_belong_to_the_question(client):
    _, sid = _start(client)
    qid, _ = _first_question(client.get(f"/sessions/{sid}").text)
    assert client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": 1}).status_code == 400
    assert client.post(f"/sessions/{sid}/answer", data={"question_id": 1, "selected_option_id": ""}).status_code == 404


def test_reveal_shows_the_answer_without_counting(client):
    _, sid = _start(client, mode="exam")
    qid, _ = _first_question(client.get(f"/sessions/{sid}").text)
    res = client.get(f"/sessions/{sid}/questions/{qid}/card", params={"reveal": "1"})
    assert "👁 Respuesta correcta:" in res.text and "no cuenta para la nota" in res.text and "opt--right" in res.text
    assert re.search(r"<strong>0</strong>/\d+ contestadas", res.text)
    assert "Ocultar respuesta" in res.text and "hx-post" in res.text        # se puede contestar igualmente
    hidden = client.get(f"/sessions/{sid}/questions/{qid}/card")
    assert "opt--right" not in hidden.text


def test_doubtful_mark_is_kept_across_tests(client):
    from config import SQLITE_PATH
    from infrastructure.db.engine import create_sqlite_engine, session_scope
    from infrastructure.db.repositories.mark_repository import MarkRepository

    _, sid = _start(client)
    qid, _ = _first_question(client.get(f"/sessions/{sid}").text)
    with session_scope(create_sqlite_engine(SQLITE_PATH)) as db:  # otros tests pueden haberla marcado
        MarkRepository(db).set_doubtful(qid, False)
    res = client.post(f"/sessions/{sid}/questions/{qid}/doubtful")
    assert "🔖 Dudosa" in res.text and "tq--doubtful" in res.text and re.search(r"🔖 \d+ dudosas?<", res.text)
    _, other = _start(client)
    assert "tq--doubtful" in _card_html(client.get(f"/sessions/{other}").text, 1)
    client.post(f"/sessions/{other}/questions/{qid}/doubtful")
    assert "tq--doubtful" not in _card_html(client.get(f"/sessions/{sid}").text, 1)


def test_feedback_mode_can_change_mid_test(client):
    _, sid = _start(client, mode="exam")
    assert not re.search(r'name="instant" value="1"[^>]*checked', client.get(f"/sessions/{sid}").text)
    res = client.post(f"/sessions/{sid}/feedback-mode", data={"instant": "1"})
    assert res.status_code == 303 and res.headers["location"] == f"/sessions/{sid}"
    assert re.search(r'name="instant" value="1"[^>]*checked', client.get(f"/sessions/{sid}").text)
    client.post(f"/sessions/{sid}/feedback-mode", data={})
    assert not re.search(r'name="instant" value="1"[^>]*checked', client.get(f"/sessions/{sid}").text)


def test_timer_never_starts_by_itself(client):
    """Como PreparaTIC: el cronómetro lo arranca el usuario con «Empezar», también en simulacro."""
    _, sid = _start(client, mode="exam")
    page = client.get(f"/sessions/{sid}").text
    assert 'id="timer"' in page and 'data-limit="6000"' in page and 'data-running="false"' in page
    assert "▶ Empezar" in page and "Ocultar Tiempo" in page and "⏹ Detener" in page
    assert "✔ Corregir" in page and "⛃ Filtrar" in page and "Modo Entrenamiento" in page
    assert 'id="timeout-dialog"' in page and "Un poquito más" in page

    _, practice = _start(client)
    page = client.get(f"/sessions/{practice}").text
    assert 'data-running="false"' in page and "▶ Empezar" in page
    assert re.search(r'data-limit="(\d+)"', page).group(1) == str(60 * len(re.findall(r'id="q-\d+"', page)))


def test_timer_endpoint_pauses_resumes_and_resets(client):
    _, sid = _start(client)
    started = client.post(f"/sessions/{sid}/timer", data={"action": "start"}).json()
    assert started["running"] is True and started["started"] is True
    paused = client.post(f"/sessions/{sid}/timer", data={"action": "pause"}).json()
    assert paused["running"] is False and paused["elapsed"] >= 0
    assert 'data-running="false"' in client.get(f"/sessions/{sid}").text    # no se reanuda solo
    reset = client.post(f"/sessions/{sid}/timer", data={"action": "reset"}).json()
    assert reset == {"limit": started["limit"], "elapsed": 0, "running": False, "started": True}
    assert client.post(f"/sessions/{sid}/timer", data={"action": "explode"}).status_code == 400
    assert client.post("/sessions/no-existe/timer", data={"action": "start"}).status_code == 404

    client.post(f"/sessions/{sid}/timer", data={"action": "start"})
    client.post(f"/sessions/{sid}/close")
    assert "⏱ 00:00:0" in client.get(f"/sessions/{sid}/result").text


def test_correct_any_time_and_result_shows_every_answer(client):
    _, sid = _start(client, mode="exam")
    qid, _ = _first_question(client.get(f"/sessions/{sid}").text)
    wrong = next(o for o in _question(qid).options if not o.is_correct)
    client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": wrong.id})

    res = client.post(f"/sessions/{sid}/close")
    assert res.status_code == 303 and res.headers["location"] == f"/sessions/{sid}/result"
    sheet = client.get(res.headers["location"])
    assert sheet.status_code == 200 and sheet.headers.get("cache-control") == "no-store"
    assert "scoreboard" in sheet.text and "Desglose" in sheet.text and "Resultado del simulacro" in sheet.text
    assert "❌ Incorrecta" in sheet.text and "⬜ Sin contestar" in sheet.text
    # También las preguntas en blanco muestran la correcta
    assert "opt--right" in _card_html(sheet.text, 2)
    assert "hx-post" not in _card_html(sheet.text, 1).split('class="tq__tools"')[0]   # ya no se responde
    # Cerrada: la pantalla del test y los enlaces antiguos llevan a resultados
    assert client.get(f"/sessions/{sid}").headers["location"] == f"/sessions/{sid}/result"
    late = client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": wrong.id})
    assert late.headers.get("HX-Redirect") == f"/sessions/{sid}/result"
    assert client.get("/sessions/no-existe/result").status_code == 404


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

        option_of = {qid: _question(qid).options[0].id for qid in (18012, 18044)}

        # 2. Responder pregunta 18012 (un apunte enlazado)
        ans_single = client.post(f"/sessions/{session_id}/answer",
                                 data={"question_id": 18012, "selected_option_id": option_of[18012]})
        assert ans_single.status_code == 200
        notes = re.search(r'<p class="tq__notes">(.*?)</p>', ans_single.text, re.S).group(1)
        assert "/notes/tema-i-01-derecho-constitucional" in notes and notes.count("<a ") == 1

        # 3. Responder pregunta 18044 (dos apuntes enlazados)
        ans_multi = client.post(f"/sessions/{session_id}/answer",
                                data={"question_id": 18044, "selected_option_id": option_of[18044]})
        notes = re.search(r'<p class="tq__notes">(.*?)</p>', ans_multi.text, re.S).group(1)
        assert notes.count("<a ") == 2
        assert "tema-i-09-admin-digital" in notes and "tema-i-09-ens-eni" in notes

        # 4. Ver hoja de resultados y comprobar que incluye los enlaces
        res_sheet = client.get(f"/sessions/{session_id}/result")
        assert res_sheet.status_code == 200
        assert "/notes/tema-i-01-derecho-constitucional" in res_sheet.text
        assert "/notes/tema-i-09-ens-eni" in res_sheet.text

        # 5. Práctica por apunte: POST /sessions/practice/by-note/tema-i-01-derecho-constitucional
        # 5a. Sin seguir redirecciones: verifica el 303 que lleva a la pantalla del test
        res_by_note = client.post("/sessions/practice/by-note/tema-i-01-derecho-constitucional")
        assert res_by_note.status_code == 303
        assert re.search(r"/sessions/[0-9a-f]+$", res_by_note.headers["location"])

        # 5b. Cadena completa (POST 303 -> GET 200 a /sessions/{id})
        res_full_chain = client.post("/sessions/practice/by-note/tema-i-01-derecho-constitucional", follow_redirects=True)
        assert res_full_chain.status_code == 200
        assert re.search(r"/sessions/[0-9a-f]+$", str(res_full_chain.url))
        assert "tq__statement" in res_full_chain.text

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

        # Al responder, responde 200 sin lanzar 500 y sin enlaces a apuntes
        ans_res = client.post(f"/sessions/{session_id}/answer",
                              data={"question_id": 18012, "selected_option_id": _question(18012).options[0].id})
        assert ans_res.status_code == 200
        assert "tq__notes" not in ans_res.text

        # 3. Al ver resultados, responde 200 sin lanzar 500 y sin enlaces
        res_sheet = client.get(f"/sessions/{session_id}/result")
        assert res_sheet.status_code == 200
        assert "tq__notes" not in res_sheet.text

    finally:
        app.dependency_overrides.pop(get_linking_client, None)


@pytest.mark.real_db
def test_root_path_prefix_guardian(monkeypatch):
    """Test guardián: renderizar cada página con ROOT_PATH=/tests y comprobar por regex que no queda ninguna URL interna sin el prefijo."""
    import config
    from presentation.dependencies import get_linking_client

    monkeypatch.setenv("ROOT_PATH", "/tests")
    monkeypatch.setattr(config, "ROOT_PATH", "/tests")
    # El enlace a Study Assistant cruza de servicio: debe salir de su URL pública
    # configurada, no de una ruta escrita a mano en la plantilla.
    monkeypatch.setattr(config, "STUDY_ASSISTANT_PUBLIC_URL", "http://study-assistant.example")

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
        assert 'href="http://study-assistant.example/"' in res_cat.text
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
        session_id = loc_create.rstrip("/").split("/sessions/")[1]

        # 3. Pantalla del test en modo examen con cronómetro
        res_q = t_client.get(f"/sessions/{session_id}")
        assert res_q.status_code == 200
        assert_no_unprefixed_urls(res_q.text, "Pantalla del test")
        assert f'hx-post="/tests/sessions/{session_id}/answer"' in res_q.text
        assert f'action="/tests/sessions/{session_id}/close"' in res_q.text
        assert f'data-url="/tests/sessions/{session_id}/timer"' in res_q.text

        # 4. Enviar respuesta por htmx (POST /sessions/{id}/answer)
        qid, options = _first_question(res_q.text)
        res_ans = t_client.post(f"/sessions/{session_id}/answer",
                                data={"question_id": qid, "selected_option_id": options[0]})
        assert res_ans.status_code == 200
        assert_no_unprefixed_urls(res_ans.text, "Tarjeta tras responder")
        assert f'hx-post="/tests/sessions/{session_id}/questions/{qid}/doubtful"' in res_ans.text

        # 5. Enlaces antiguos a una pregunta
        res_old = t_client.get(f"/sessions/{session_id}/question/3")
        assert res_old.status_code == 303
        assert res_old.headers["location"] == f"/tests/sessions/{session_id}#q-3"

        # 6. Hoja de resultados (/sessions/{id}/result)
        res_res = t_client.get(f"/sessions/{session_id}/result")
        assert res_res.status_code == 200
        assert_no_unprefixed_urls(res_res.text, "Hoja de resultados")
        assert 'href="/tests/"' in res_res.text

        # 7. Práctica por apunte - resolución canónica y prefijada
        res_by_note_proc = t_client.post("/sessions/practice/by-note/tema-i-01")
        assert res_by_note_proc.status_code == 303
        assert re.fullmatch(r"/tests/sessions/[0-9a-f]+", res_by_note_proc.headers["location"])

    finally:
        app.dependency_overrides.pop(get_linking_client, None)




def test_training_mode_and_filter_from_the_test_screen(client):
    _, sid = _start(client, mode="exam")
    qid, options = _first_question(client.get(f"/sessions/{sid}").text)
    assert client.post(f"/sessions/{sid}/training", data={"on": "1"}).status_code == 303
    page = client.get(f"/sessions/{sid}").text
    assert re.search(r'name="on" value="1"[^>]*checked', page)
    assert re.search(r'name="instant" value="1"[^>]*disabled', page)     # entrenamiento: corrige al final
    client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": options[0]})
    two = client.post(f"/sessions/{sid}/answer", data={"question_id": qid, "selected_option_id": options[1]})
    assert two.text.count("opt--selected") == 2 and "🤔 Dudosa: 2 opciones marcadas" in two.text
    assert "🔖 Dudosa" in two.text                                       # queda marcada para repasarla

    # En el examen 53 ninguna pregunta está marcada como de examen oficial (ver docs/ESTADO.md)
    client.post(f"/sessions/{sid}/filter", data={"exam": "only"})
    assert "El filtro no deja ninguna pregunta" in client.get(f"/sessions/{sid}").text
    assert client.post(f"/sessions/{sid}/filter", data={"exam": "none", "count": "3"}).status_code == 303
    page = client.get(f"/sessions/{sid}").text
    assert len(re.findall(r'id="q-\d+"', page)) == 3 and "(activo)" in page and "3 de " in page
    assert re.search(r'name="exam" value="none" checked', page)
    client.post(f"/sessions/{sid}/filter", data={"reset": "1"})
    assert "(activo)" not in client.get(f"/sessions/{sid}").text

    client.post(f"/sessions/{sid}/close")
    sheet = client.get(f"/sessions/{sid}/result").text
    assert "Has tenido un acierto del" in sheet and "dudosas" in sheet
