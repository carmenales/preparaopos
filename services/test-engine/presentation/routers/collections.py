"""Tests fijos por colección (menú «Tests»: Aleatorios, Relevancia, Bloques, Temas, Años), como PreparaTIC V3."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from config import prefix_url
from domain.sessions.collections import KINDS, build_collection
from domain.sessions.generator import GeneratorFilters, NoQuestionsForFilters
from infrastructure.syllabus_names import block_title, topic_name
from presentation.dependencies import QuestionRepoDep, SessionServiceDep, StatsRepoDep
from presentation.templating import templates

router = APIRouter()

NO_CACHE = {"Cache-Control": "no-store"}
SYLLABUS_COOKIE = "te_syllabus"


def pick_syllabus(request: Request, syllabi: list[dict], requested: str | None) -> str | None:
    """El temario pedido, si no el último elegido (cookie) y si no el que más preguntas tiene."""
    ids = {s["id"] for s in syllabi}
    for candidate in (requested, request.cookies.get(SYLLABUS_COOKIE)):
        if candidate in ids:
            return candidate
    return max(syllabi, key=lambda s: s["count"])["id"] if syllabi else None


@router.get("/collections/{kind}", response_class=HTMLResponse)
def collection(request: Request, kind: str, repo: QuestionRepoDep, stats: StatsRepoDep,
               syllabus_id: str | None = None):
    if kind not in KINDS:
        raise HTTPException(status_code=404, detail="Colección no encontrada")
    syllabi = repo.list_syllabi_with_counts()
    selected = pick_syllabus(request, syllabi, syllabus_id)
    tests, status = [], {}
    total = 0
    if selected:
        total = repo.count_for_generator(GeneratorFilters(selected))
        tests = build_collection(kind, selected, total, repo.generator_facets(selected))
        status = stats.fixed_test_status([t.source_ref for t in tests])
    rows = [
        {"test": t, "status": status.get(t.source_ref, {"open_id": None, "done": 0, "last_score": None}),
         "block_title": block_title(selected, t.block), "topic_name": topic_name(selected, t.topic)}
        for t in tests
    ]
    done = sum(1 for r in rows if r["status"]["done"])
    response = templates.TemplateResponse(
        request, "collection.html",
        {"kind": KINDS[kind], "syllabi": syllabi, "selected": selected, "rows": rows,
         "total": total, "done": done},
        headers=NO_CACHE,
    )
    if selected and syllabus_id == selected:
        response.set_cookie(SYLLABUS_COOKIE, selected, max_age=365 * 24 * 3600, path=prefix_url("/"),
                            samesite="lax")
    return response


@router.post("/collections/start", response_class=HTMLResponse)
def start_fixed_test(svc: SessionServiceDep, stats: StatsRepoDep, ref: Annotated[str, Form()]):
    """Empieza un test fijo o, si ya tiene uno sin terminar, lo continúa (no se duplican)."""
    try:
        filters = GeneratorFilters.from_source_ref(ref)
    except ValueError:
        raise HTTPException(status_code=400, detail="Test no válido")
    if filters.part is None:
        raise HTTPException(status_code=400, detail="Test no válido")
    ref = filters.to_source_ref()
    open_id = stats.fixed_test_status([ref]).get(ref, {}).get("open_id")
    if open_id:
        return RedirectResponse(url=prefix_url(f"/sessions/{open_id}"), status_code=303)
    try:
        # Como en PreparaTIC: se corrige al final y el cronómetro lo arranca el usuario.
        session = svc.start_session(mode="exam", source="generated", source_ref=ref)
    except NoQuestionsForFilters:
        raise HTTPException(status_code=404, detail="Este test ya no tiene preguntas")
    return RedirectResponse(url=prefix_url(f"/sessions/{session.id}"), status_code=303)
