"""Router de sesiones: crear, responder preguntas y ver resultados."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config import STUDY_ASSISTANT_URL, TEMPLATES_DIR, prefix_url
from presentation.dependencies import LinkingClientDep, QuestionRepoDep, SessionServiceDep
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
    links = linking_client.get_links_by_note(note_id)
    if not links:
        return RedirectResponse(url=prefix_url("/"), status_code=303)

    q_ids = [str(l["question_id"]) for l in links if "question_id" in l]
    if not q_ids:
        return RedirectResponse(url=prefix_url("/"), status_code=303)

    session = svc.start_session(
        mode="practice",
        source="questions",
        source_ref=",".join(q_ids),
    )
    return RedirectResponse(
        url=prefix_url(f"/sessions/{session.id}/question/1"),
        status_code=303,
    )


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
    """Crea una sesión nueva y redirige a la primera pregunta."""
    session = svc.start_session(
        mode=mode,  # type: ignore[arg-type]
        source=source,  # type: ignore[arg-type]
        source_ref=source_ref or None,
    )
    return RedirectResponse(
        url=prefix_url(f"/sessions/{session.id}/question/1"),
        status_code=303,
    )


# ---------------------------------------------------------------------------
# Pregunta (práctica y examen comparten plantilla, flag mode)
# ---------------------------------------------------------------------------

@router.get("/{session_id}/question/{n}", response_class=HTMLResponse)
def show_question(
    request: Request,
    session_id: str,
    n: int,
    svc: SessionServiceDep,
    q_repo: QuestionRepoDep,
):
    """Muestra la pregunta n-ésima de la sesión (1-indexed).

    Bounds-checking:
      - n < 1  → redirige a /question/1
      - n > total → redirige a /result
    """
    session = svc.get_session(session_id)
    if session is None:
        return RedirectResponse(url=prefix_url("/"), status_code=303)

    total = len(session.question_ids)

    if n < 1:
        return RedirectResponse(
            url=prefix_url(f"/sessions/{session_id}/question/1"),
            status_code=303,
        )
    if n > total:
        return RedirectResponse(
            url=prefix_url(f"/sessions/{session_id}/result"),
            status_code=303,
        )

    # Si la sesión ya está cerrada, saltar directo a resultados
    if session.closed_at is not None:
        return RedirectResponse(
            url=prefix_url(f"/sessions/{session_id}/result"),
            status_code=303,
        )

    question_id = session.question_ids[n - 1]
    question = q_repo.get_by_id(question_id)

    if question is None:
        # Pregunta no encontrada — pasar a la siguiente
        return RedirectResponse(
            url=prefix_url(f"/sessions/{session_id}/question/{n + 1}"),
            status_code=303,
        )

    # Intento anterior para esta pregunta (para marcar la opción ya seleccionada)
    previous_attempt = next(
        (att for att in session.attempts if att.question_id == question_id),
        None,
    )

    remaining_seconds = svc.remaining_seconds(session)

    return templates.TemplateResponse(
        request,
        "question.html",
        {
            "session": session,
            "question": question,
            "n": n,
            "total": total,
            "previous_attempt": previous_attempt,
            "remaining_seconds": remaining_seconds,
        },
        headers=NO_CACHE,
    )


# ---------------------------------------------------------------------------
# Registrar respuesta (htmx POST — devuelve fragmento HTML)
# ---------------------------------------------------------------------------

@router.post("/{session_id}/answer", response_class=HTMLResponse)
def submit_answer(
    request: Request,
    session_id: str,
    svc: SessionServiceDep,
    q_repo: QuestionRepoDep,
    linking_client: LinkingClientDep,
    question_id: Annotated[int, Form()],
    selected_option_id: Annotated[int | None, Form()] = None,
    n: Annotated[int, Form()] = 1,
):
    """Registra la respuesta vía htmx y devuelve el fragmento de feedback.

    En modo práctica devuelve corrección inline y notas relacionadas.
    En modo examen solo confirma que la respuesta se guardó.
    """
    result = svc.submit_answer(
        session_id=session_id,
        question_id=question_id,
        selected_option_id=selected_option_id,
    )

    session = svc.get_session(session_id)

    # Si la sesión expiró durante el submit, redirigir a resultados
    if result is None or (session and session.closed_at is not None):
        res_url = prefix_url(f"/sessions/{session_id}/result")
        return HTMLResponse(
            content=f"""<div id="feedback" class="feedback feedback--expired">
                Tiempo agotado. <a href="{res_url}">Ver resultados →</a>
            </div>""",
            headers=NO_CACHE,
        )

    # En modo examen no se carga ni se pasa el objeto question al contexto (defensa en profundidad)
    question = q_repo.get_by_id(question_id) if (session and session.mode == "practice") else None
    total = len(session.question_ids) if session else 0

    # En modo práctica, obtener notas vinculadas vía linking-service
    linked_notes = []
    if session and session.mode == "practice":
        linked_notes = linking_client.get_links_by_question(question_id)

    return templates.TemplateResponse(
        request,
        "partials/answer_feedback.html",
        {
            "result": result,
            "question": question,
            "session": session,
            "n": n,
            "next_n": n + 1,
            "total": total,
            "linked_notes": linked_notes,
            "study_assistant_url": STUDY_ASSISTANT_URL,
        },
        headers=NO_CACHE,
    )


# ---------------------------------------------------------------------------
# Resultados
# ---------------------------------------------------------------------------

@router.get("/{session_id}/result", response_class=HTMLResponse)
def show_result(
    request: Request,
    session_id: str,
    svc: SessionServiceDep,
    q_repo: QuestionRepoDep,
    linking_client: LinkingClientDep,
):
    """Hoja de resultados. Cierra la sesión si aún estaba abierta (lazy close)."""
    result = svc.get_result(session_id)

    question_ids = [qr.question_id for qr in result.questions]
    questions_map = q_repo.get_by_ids(question_ids)
    linked_notes_map = linking_client.get_links_by_questions(question_ids)

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "result": result,
            "questions_map": questions_map,
            "linked_notes_map": linked_notes_map,
            "study_assistant_url": STUDY_ASSISTANT_URL,
        },
        headers=NO_CACHE,
    )
