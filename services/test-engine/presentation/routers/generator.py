"""Router del generador de tests: filtros por temario, bloque/tema, año, examen oficial y falladas."""

from __future__ import annotations

from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from config import prefix_url
from domain.sessions.generator import DEFAULT_COUNT, GeneratorFilters, NoQuestionsForFilters
from presentation.dependencies import QuestionRepoDep, SessionServiceDep
from presentation.templating import templates

router = APIRouter(prefix="/generator")

COUNT_CHOICES = [10, 20, 30, 50, 100]


def _split_scope(scope: str | None) -> tuple[str | None, str | None]:
    """'I' → bloque I; 'I|9' → bloque I, tema 9; '' → todo el temario."""
    if not scope:
        return None, None
    block, _, topic = scope.partition("|")
    return block or None, topic or None


def _build_filters(syllabus_id, scope, year, official, failed, count) -> GeneratorFilters:
    block, topic = _split_scope(scope)
    return GeneratorFilters(
        syllabus_id=syllabus_id or "",
        block=block,
        topic=topic,
        year=int(year) if year else None,
        official_only=bool(official),
        failed_only=bool(failed),
        count=int(count) if count else DEFAULT_COUNT,
    )


def _back_to_form(syllabus_id: str | None, error: str) -> RedirectResponse:
    query = urlencode({k: v for k, v in {"syllabus_id": syllabus_id, "error": error}.items() if v})
    return RedirectResponse(url=prefix_url(f"/generator/?{query}"), status_code=303)


@router.get("/", response_class=HTMLResponse)
def generator_form(
    request: Request,
    repo: QuestionRepoDep,
    syllabus_id: str | None = None,
    error: str | None = None,
):
    syllabi = repo.list_syllabi_with_counts()
    ids = {s["id"] for s in syllabi}
    selected = syllabus_id if syllabus_id in ids else (syllabi[0]["id"] if syllabi else None)
    facets = repo.generator_facets(selected) if selected else None
    return templates.TemplateResponse(
        request,
        "generator.html",
        {
            "syllabi": syllabi,
            "selected": selected,
            "facets": facets,
            "count_choices": COUNT_CHOICES,
            "default_count": DEFAULT_COUNT,
            "error": error,
        },
        headers={"Cache-Control": "no-store"},
    )


@router.get("/count", response_class=HTMLResponse)
def available_count(
    request: Request,
    repo: QuestionRepoDep,
    syllabus_id: Annotated[str | None, Query()] = None,
    scope: Annotated[str | None, Query()] = None,
    year: Annotated[str | None, Query()] = None,
    official: Annotated[str | None, Query()] = None,
    failed: Annotated[str | None, Query()] = None,
):
    """Fragmento htmx: cuántas preguntas cumplen los filtros actuales."""
    try:
        n = repo.count_for_generator(_build_filters(syllabus_id, scope, year, official, failed, None))
    except ValueError:
        n = 0
    return HTMLResponse(
        f'<strong>{n}</strong> pregunta{"s" if n != 1 else ""} disponible{"s" if n != 1 else ""}',
        headers={"Cache-Control": "no-store"},
    )


@router.post("/", response_class=HTMLResponse)
def generate(
    svc: SessionServiceDep,
    syllabus_id: Annotated[str, Form()],
    mode: Annotated[str, Form()] = "practice",
    scope: Annotated[str | None, Form()] = None,
    year: Annotated[str | None, Form()] = None,
    official: Annotated[str | None, Form()] = None,
    failed: Annotated[str | None, Form()] = None,
    count: Annotated[str | None, Form()] = None,
):
    if mode not in ("practice", "exam"):
        return _back_to_form(syllabus_id, "Modo no válido.")
    try:
        filters = _build_filters(syllabus_id, scope, year, official, failed, count)
    except ValueError as exc:
        return _back_to_form(syllabus_id, str(exc))
    try:
        session = svc.start_session(mode=mode, source="generated", source_ref=filters.to_source_ref())  # type: ignore[arg-type]
    except NoQuestionsForFilters:
        return _back_to_form(syllabus_id, "Ninguna pregunta cumple esos filtros. Prueba a ampliarlos.")
    return RedirectResponse(url=prefix_url(f"/sessions/{session.id}/question/1"), status_code=303)

