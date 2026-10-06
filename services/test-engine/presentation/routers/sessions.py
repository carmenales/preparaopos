"""Router de sesiones: crear, responder preguntas y ver resultados."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config import TEMPLATES_DIR
from presentation.dependencies import QuestionRepoDep, SessionServiceDep

router = APIRouter(prefix="/sessions")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Cabeceras para rutas GET que pueden producir escritura (cierre perezoso de sesiones)
NO_CACHE = {"Cache-Control": "no-store"}


# ---------------------------------------------------------------------------
# Crear sesión
# ---------------------------------------------------------------------------

@router.post("/", response_class=HTMLResponse)
async def create_session(
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
        url=f"/sessions/{session.id}/question/1",
        status_code=303,
    )


# ---------------------------------------------------------------------------
# Pregunta (práctica y examen comparten plantilla, flag mode)
# ---------------------------------------------------------------------------

@router.get("/{session_id}/question/{n}", response_class=HTMLResponse)
async def show_question(
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
        return RedirectResponse(url="/", status_code=303)

    total = len(session.question_ids)

    if n < 1:
        return RedirectResponse(
            url=f"/sessions/{session_id}/question/1",
            status_code=303,
        )
    if n > total:
        return RedirectResponse(
            url=f"/sessions/{session_id}/result",
            status_code=303,
        )

    # Si la sesión ya está cerrada, saltar directo a resultados
    if session.closed_at is not None:
        return RedirectResponse(
            url=f"/sessions/{session_id}/result",
            status_code=303,
        )

    question_id = session.question_ids[n - 1]
    question = q_repo.get_by_id(question_id)

    if question is None:
        # Pregunta no encontrada — pasar a la siguiente
        return RedirectResponse(
            url=f"/sessions/{session_id}/question/{n + 1}",
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
async def submit_answer(
    request: Request,
    session_id: str,
    svc: SessionServiceDep,
    q_repo: QuestionRepoDep,
    question_id: Annotated[int, Form()],
    selected_option_id: Annotated[int | None, Form()] = None,
    n: Annotated[int, Form()] = 1,
):
    """Registra la respuesta vía htmx y devuelve el fragmento de feedback.

    En modo práctica devuelve corrección inline.
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
        return HTMLResponse(
            content="""<div id="feedback" class="feedback feedback--expired">
                Tiempo agotado. <a href="/sessions/{}/result">Ver resultados →</a>
            </div>""".format(session_id),
            headers=NO_CACHE,
        )

    # En modo examen no se carga ni se pasa el objeto question al contexto (defensa en profundidad)
    question = q_repo.get_by_id(question_id) if (session and session.mode == "practice") else None
    total = len(session.question_ids) if session else 0

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
        },
        headers=NO_CACHE,
    )


# ---------------------------------------------------------------------------
# Resultados
# ---------------------------------------------------------------------------

@router.get("/{session_id}/result", response_class=HTMLResponse)
async def show_result(
    request: Request,
    session_id: str,
    svc: SessionServiceDep,
    q_repo: QuestionRepoDep,
):
    """Hoja de resultados. Cierra la sesión si aún estaba abierta (lazy close)."""
    result = svc.get_result(session_id)

    question_ids = [qr.question_id for qr in result.questions]
    questions_map = q_repo.get_by_ids(question_ids)

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "result": result,
            "questions_map": questions_map,
        },
        headers=NO_CACHE,
    )
