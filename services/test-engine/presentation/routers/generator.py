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


def _build_filters(syllabus_id, scope, year, official, failed, count, weighted=None, doubtful=None) -> GeneratorFilters:
    block, topic = _split_scope(scope)
    return GeneratorFilters(
        syllabus_id=syllabus_id or "",
        block=block,
        topic=topic,
        year=int(year) if year else None,
        official_only=bool(official),
        failed_only=bool(failed),
        doubtful_only=bool(doubtful),
        weighted=bool(weighted),
        count=int(count) if count else DEFAULT_COUNT,
    )


def _back_to_form(syllabus_id: str | None, error: str) -> RedirectResponse:
    query = urlencode({k: v for k, v in {"syllabus_id": syllabus_id, "error": error}.items() if v})
    return RedirectResponse(url=prefix_url(f"/generator/?{query}"), status_code=303)


def _available_html(n: int, requested: int | None) -> str:
    text = f'<strong>{n}</strong> pregunta{"s" if n != 1 else ""} disponible{"s" if n != 1 else ""}'
    if n == 0:
        text += ' <span class="generator__warning">· ninguna cumple los filtros: amplíalos</span>'
    elif requested and n < requested:
        text += (f' <span class="generator__warning">· has pedido {requested}, pero solo hay {n}: '
                 f'el test tendrá {n} pregunta{"s" if n != 1 else ""}</span>')
    return text


def _fields_context(repo, syllabus_id, scope, year, official, failed, weighted, count, doubtful=None) -> dict:
    """Campos del formulario con los números de cada opción calculados con los demás filtros elegidos."""
    try:
        filters = _build_filters(syllabus_id, scope, year, official, failed, count, weighted, doubtful)
    except ValueError:
        filters = GeneratorFilters(syllabus_id)
        scope = year = official = failed = weighted = doubtful = None
    requested = filters.count
    n = repo.count_for_generator(filters)
    return {
        "facets": repo.generator_facets(syllabus_id, filters),
        "v": {"scope": scope or "", "year": str(filters.year or ""), "official": filters.official_only,
              "failed": filters.failed_only, "doubtful": filters.doubtful_only, "weighted": filters.weighted,
              "count": requested},
        "count_choices": sorted(set(COUNT_CHOICES) | {requested}),
        "available_html": _available_html(n, requested),
    }


@router.get("/", response_class=HTMLResponse)
def generator_form(
    request: Request,
    repo: QuestionRepoDep,
    syllabus_id: str | None = None,
    error: str | None = None,
    scope: str | None = None,
    year: str | None = None,
    official: str | None = None,
    failed: str | None = None,
    weighted: str | None = None,
    count: str | None = None,
    doubtful: str | None = None,
):
    syllabi = repo.list_syllabi_with_counts()
    ids = {s["id"] for s in syllabi}
    selected = syllabus_id if syllabus_id in ids else (syllabi[0]["id"] if syllabi else None)
    context = {"syllabi": syllabi, "selected": selected, "error": error}
    if selected:
        context |= _fields_context(repo, selected, scope, year, official == "1", failed == "1", weighted == "1",
                                   count if count and count.isdigit() else None, doubtful == "1")
    return templates.TemplateResponse(request, "generator.html", context, headers={"Cache-Control": "no-store"})


@router.get("/fields", response_class=HTMLResponse)
def generator_fields(
    request: Request,
    repo: QuestionRepoDep,
    syllabus_id: Annotated[str, Query()],
    scope: Annotated[str | None, Query()] = None,
    year: Annotated[str | None, Query()] = None,
    official: Annotated[str | None, Query()] = None,
    failed: Annotated[str | None, Query()] = None,
    weighted: Annotated[str | None, Query()] = None,
    count: Annotated[str | None, Query()] = None,
    doubtful: Annotated[str | None, Query()] = None,
):
    """Fragmento htmx: los campos del formulario, recalculados al cambiar cualquier filtro."""
    context = _fields_context(repo, syllabus_id, scope, year, official, failed, weighted,
                              count if count and count.isdigit() else None, doubtful)
    return templates.TemplateResponse(request, "partials/generator_fields.html", context,
                                      headers={"Cache-Control": "no-store"})


@router.get("/count", response_class=HTMLResponse)
def available_count(
    request: Request,
    repo: QuestionRepoDep,
    syllabus_id: Annotated[str | None, Query()] = None,
    scope: Annotated[str | None, Query()] = None,
    year: Annotated[str | None, Query()] = None,
    official: Annotated[str | None, Query()] = None,
    failed: Annotated[str | None, Query()] = None,
    count: Annotated[str | None, Query()] = None,
):
    """Fragmento htmx: cuántas preguntas cumplen los filtros actuales y si alcanzan para el test pedido."""
    try:
        n = repo.count_for_generator(_build_filters(syllabus_id, scope, year, official, failed, None))
    except ValueError:
        n = 0
    requested = int(count) if count and count.isdigit() else None
    return HTMLResponse(_available_html(n, requested), headers={"Cache-Control": "no-store"})


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
    weighted: Annotated[str | None, Form()] = None,
    doubtful: Annotated[str | None, Form()] = None,
):
    if mode not in ("practice", "exam"):
        return _back_to_form(syllabus_id, "Modo no válido.")
    try:
        filters = _build_filters(syllabus_id, scope, year, official, failed, count, weighted, doubtful)
    except ValueError as exc:
        return _back_to_form(syllabus_id, str(exc))
    try:
        session = svc.start_session(mode=mode, source="generated", source_ref=filters.to_source_ref())  # type: ignore[arg-type]
    except NoQuestionsForFilters:
        return _back_to_form(syllabus_id, "Ninguna pregunta cumple esos filtros. Prueba a ampliarlos.")
    url = f"/sessions/{session.id}"
    if len(session.question_ids) < filters.count:
        url += f"?requested={filters.count}"
    return RedirectResponse(url=prefix_url(url), status_code=303)

