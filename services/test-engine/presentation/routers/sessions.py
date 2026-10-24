"""Router de sesiones: crear, responder preguntas y ver resultados."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config import STUDY_ASSISTANT_URL, TEMPLATES_DIR, prefix_url
from presentation.dependencies import LinkingClientDep, MarkRepoDep, QuestionRepoDep, SessionServiceDep
from presentation.templating import templates

router = APIRouter(prefix="/sessions")

# Cabeceras para rutas GET que pueden producir escritura (cierre perezoso de sesiones)
NO_CACHE = {"Cache-Control": "no-store"}


# ---------------------------------------------------------------------------
# Práctica por apunte (navegación cruzada desde Study Assistant)
# ---------------------------------------------------------------------------

@router.post("/practice/by-note/{note_id}", response_class=HTMLResponse)
def practice_by_note(
    request: Request,
    note_id: str,
    svc: SessionServiceDep,
    linking_client: LinkingClientDep,
):
    """Inicia una sesión de práctica con las preguntas vinculadas a un apunte."""
    q_ids = linking_client.get_question_ids_by_note(note_id)
    if not q_ids:
        return RedirectResponse(url=prefix_url("/"), status_code=303)

    session = svc.start_session(
        mode="practice",
        source="note",
        source_ref=note_id,
        explicit_question_ids=q_ids,
    )
    return RedirectResponse(url=prefix_url(f"/sessions/{session.id}"), status_code=303)



# ---------------------------------------------------------------------------
# Crear sesión
# ---------------------------------------------------------------------------

@router.post("/", response_class=HTMLResponse)
def create_session(
    request: Request,
    svc: SessionServiceDep,
    mode: Annotated[str, Form()],
    source: Annotated[str, Form()],
    source_ref: Annotated[str | None, Form()] = None,
):
    """Crea una sesión nueva y abre la pantalla del test."""
    session = svc.start_session(
        mode=mode,  # type: ignore[arg-type]
        source=source,  # type: ignore[arg-type]
        source_ref=source_ref or None,
    )
    return RedirectResponse(url=prefix_url(f"/sessions/{session.id}"), status_code=303)


# ---------------------------------------------------------------------------
# Pantalla del test: todas las preguntas en una página (como PreparaTIC y preparadortai)
# ---------------------------------------------------------------------------
#
# Se responde pulsando una opción (htmx) y se guarda al momento; volver a pulsarla la desmarca.
# Cada respuesta devuelve la tarjeta de esa pregunta y, fuera de banda, el marcador de la barra.

MODE_LABELS = {"practice": "Práctica", "exam": "Simulacro"}


def _correct_option(question):
    return next((o for o in question.options if o.is_correct), None) if question else None


def _explanation(question):
    if not question:
        return None
    correct = _correct_option(question)
    return question.justification or (correct.justification if correct else None)


def _card(session, question, n, *, attempt=None, doubtful=False, reveal=False, notes=None) -> dict:
    """Estado de la tarjeta de una pregunta para la plantilla."""
    closed = session.closed_at is not None
    selected = attempt.selected_option_id if attempt else None
    answered = selected is not None
    show = closed or reveal or (session.feedback_now and answered)
    return {
        "n": n, "q": question, "selected": selected, "answered": answered, "doubtful": doubtful,
        "reveal": reveal, "show_correction": show, "graded": answered and (closed or session.feedback_now),
        "is_correct": bool(attempt.is_correct) if answered else None,
        "locked": closed or (session.feedback_now and answered),
        "correct_option": _correct_option(question), "explanation": _explanation(question) if show else None,
        "notes": notes or [],
    }


def _summary_context(session, svc, questions_map, doubtful_ids) -> dict:
    attempts = {a.question_id: a for a in session.attempts if a.selected_option_id is not None}
    index = []
    for i, qid in enumerate(session.question_ids, start=1):
        a = attempts.get(qid)
        state = "blank" if a is None else ("answered" if not session.feedback_now else
                                          ("correct" if a.is_correct else "wrong"))
        index.append({"n": i, "state": state, "doubtful": qid in doubtful_ids})
    return {"summary": svc.live_summary(session, questions_map), "index": index,
            "doubtful_count": sum(1 for qid in session.question_ids if qid in doubtful_ids)}


def _base_context(session) -> dict:
    return {"session": session, "mode_label": MODE_LABELS.get(session.mode, session.mode),
            "study_assistant_url": STUDY_ASSISTANT_URL}


def _card_response(request, session, svc, q_repo, marks, linking_client, question_id, n, *, reveal=False):
    """Tarjeta de una pregunta + marcador de la barra (fuera de banda)."""
    questions_map = q_repo.get_by_ids(session.question_ids)
    doubtful_ids = marks.doubtful_ids(session.question_ids)
    attempt = next((a for a in session.attempts if a.question_id == question_id), None)
    card = _card(session, questions_map.get(question_id), n, attempt=attempt,
                 doubtful=question_id in doubtful_ids, reveal=reveal)
    if card["show_correction"]:
        card["notes"] = linking_client.get_links_by_question(question_id)
    if session.closed_at is not None:  # desde la hoja de resultados: no hay barra que repintar
        return templates.TemplateResponse(request, "partials/question_card.html",
                                          _base_context(session) | {"card": card}, headers=NO_CACHE)
    return templates.TemplateResponse(
        request, "partials/question_card_response.html",
        _base_context(session) | {"card": card} | _summary_context(session, svc, questions_map, doubtful_ids),
        headers=NO_CACHE,
    )


def _closed_redirect(session_id: str) -> HTMLResponse:
    """La sesión se cerró (tiempo agotado o ya corregida): htmx lleva a resultados."""
    return HTMLResponse("", headers=NO_CACHE | {"HX-Redirect": prefix_url(f"/sessions/{session_id}/result")})


def _position(session, question_id: int) -> int:
    try:
        return session.question_ids.index(question_id) + 1
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="La pregunta no es de este test") from exc


@router.get("/{session_id}", response_class=HTMLResponse)
def show_test(
    request: Request,
    session_id: str,
    svc: SessionServiceDep,
    q_repo: QuestionRepoDep,
    marks: MarkRepoDep,
    linking_client: LinkingClientDep,
    requested: int | None = None,
):
    session = svc.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    if session.closed_at is not None:
        return RedirectResponse(url=prefix_url(f"/sessions/{session_id}/result"), status_code=303)

    questions_map = q_repo.get_by_ids(session.question_ids)
    doubtful_ids = marks.doubtful_ids(session.question_ids)
    attempts = {a.question_id: a for a in session.attempts}
    graded_ids = [qid for qid, a in attempts.items() if a.selected_option_id is not None]
    notes_map = linking_client.get_links_by_questions(graded_ids) if session.feedback_now and graded_ids else {}
    cards = [
        _card(session, questions_map.get(qid), n, attempt=attempts.get(qid), doubtful=qid in doubtful_ids,
              notes=notes_map.get(qid))
        for n, qid in enumerate(session.question_ids, start=1)
    ]
    total = len(session.question_ids)
    return templates.TemplateResponse(
        request, "test.html",
        _base_context(session) | _summary_context(session, svc, questions_map, doubtful_ids) | {
            "cards": cards,
            "remaining_seconds": svc.remaining_seconds(session),
            # Test generado con menos preguntas de las pedidas (ver routers/generator.py)
            "requested": requested if (requested and requested > total) else None,
            "total": total,
        },
        headers=NO_CACHE,
    )


@router.get("/{session_id}/question/{n}", response_class=HTMLResponse)
def show_question(session_id: str, n: int, requested: int | None = None):
    """Enlaces antiguos (una pregunta por página): llevan a la pregunta dentro de la pantalla del test."""
    query = f"?requested={requested}" if requested else ""
    return RedirectResponse(url=prefix_url(f"/sessions/{session_id}{query}#q-{max(n, 1)}"), status_code=303)


@router.post("/{session_id}/answer", response_class=HTMLResponse)
def submit_answer(
    request: Request,
    session_id: str,
    svc: SessionServiceDep,
    q_repo: QuestionRepoDep,
    marks: MarkRepoDep,
    linking_client: LinkingClientDep,
    question_id: Annotated[int, Form()],
    selected_option_id: Annotated[str, Form()] = "",
):
    """Pulsar una opción: la marca, o la desmarca si ya estaba marcada. Sin opción, borra la respuesta."""
    session = svc.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    n = _position(session, question_id)
    if session.closed_at is not None:
        return _closed_redirect(session_id)
    option_id = int(selected_option_id) if selected_option_id.strip().isdigit() else None
    question = q_repo.get_by_id(question_id)
    if option_id is not None and (question is None or option_id not in {o.id for o in question.options}):
        raise HTTPException(status_code=400, detail="Esa opción no es de esta pregunta")
    if svc.answer_or_clear(session_id=session_id, question_id=question_id, option_id=option_id) is None:
        return _closed_redirect(session_id)
    return _card_response(request, svc.get_session(session_id), svc, q_repo, marks, linking_client, question_id, n)


@router.post("/{session_id}/questions/{question_id}/doubtful", response_class=HTMLResponse)
def toggle_doubtful(request: Request, session_id: str, question_id: int, svc: SessionServiceDep,
                    q_repo: QuestionRepoDep, marks: MarkRepoDep, linking_client: LinkingClientDep):
    """Marca o desmarca la pregunta como dudosa (vale para todos los tests; no afecta a la nota)."""
    session = svc.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    n = _position(session, question_id)
    marks.toggle_doubtful(question_id)
    return _card_response(request, session, svc, q_repo, marks, linking_client, question_id, n)


@router.get("/{session_id}/questions/{question_id}/card", response_class=HTMLResponse)
def question_card(request: Request, session_id: str, question_id: int, svc: SessionServiceDep,
                  q_repo: QuestionRepoDep, marks: MarkRepoDep, linking_client: LinkingClientDep,
                  reveal: str | None = None):
    """Tarjeta de una pregunta; con reveal=1 muestra la respuesta correcta (no cuenta para la nota)."""
    session = svc.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    n = _position(session, question_id)
    return _card_response(request, session, svc, q_repo, marks, linking_client, question_id, n,
                          reveal=reveal == "1")


@router.post("/{session_id}/feedback-mode", response_class=HTMLResponse)
def set_feedback_mode(session_id: str, svc: SessionServiceDep, instant: Annotated[str | None, Form()] = None):
    """Interruptor «Corregir al responder»: se puede cambiar a mitad del test."""
    session = svc.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    if session.closed_at is None:
        svc.set_feedback_mode(session_id, instant == "1")
    return RedirectResponse(url=prefix_url(f"/sessions/{session_id}"), status_code=303)


@router.post("/{session_id}/close", response_class=HTMLResponse)
def close_test(session_id: str, svc: SessionServiceDep):
    """«Corregir»: cierra el test cuando quieras (lo no contestado cuenta como blanco)."""
    if svc.get_session(session_id) is None:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    svc.close_session(session_id)
    return RedirectResponse(url=prefix_url(f"/sessions/{session_id}/result"), status_code=303)


# ---------------------------------------------------------------------------
# Resultados
# ---------------------------------------------------------------------------

@router.get("/{session_id}/result", response_class=HTMLResponse)
def show_result(
    request: Request,
    session_id: str,
    svc: SessionServiceDep,
    q_repo: QuestionRepoDep,
    marks: MarkRepoDep,
    linking_client: LinkingClientDep,
):
    """Hoja de resultados. Cierra la sesión si aún estaba abierta (lazy close).

    El desglose usa las mismas tarjetas que la pantalla del test, ya corregidas: la respuesta
    correcta de todas (también de las que quedaron en blanco), la explicación y los apuntes.
    """
    if svc.get_session(session_id) is None:
        raise HTTPException(status_code=404, detail="Test no encontrado")
    result = svc.get_result(session_id)
    session = svc.get_session(session_id)

    question_ids = [qr.question_id for qr in result.questions]
    questions_map = q_repo.get_by_ids(question_ids)
    linked_notes_map = linking_client.get_links_by_questions(question_ids)
    doubtful_ids = marks.doubtful_ids(question_ids)
    attempts = {a.question_id: a for a in session.attempts}
    cards = [
        _card(session, questions_map.get(qid), n, attempt=attempts.get(qid), doubtful=qid in doubtful_ids,
              notes=linked_notes_map.get(qid))
        for n, qid in enumerate(session.question_ids, start=1)
    ]

    return templates.TemplateResponse(
        request,
        "result.html",
        _base_context(session) | {
            "result": result,
            "cards": cards,
            "doubtful_count": len(doubtful_ids),
            # Temario para «Repasar dudosas»: el de la primera pregunta con etiqueta.
            "review_syllabus": next((q.tags[0].syllabus_id for q in questions_map.values() if q and q.tags), ""),
        },
        headers=NO_CACHE,
    )
