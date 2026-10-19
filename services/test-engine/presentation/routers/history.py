"""Historial de sesiones y estadísticas de progreso (sustituyen a historial_sesiones,
detalle_sesion, delete_test_session, estadisticas y progreso_cuestionarios de preparadortai)."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from config import prefix_url
from presentation.dependencies import StatsRepoDep
from presentation.templating import templates

router = APIRouter()

NO_CACHE = {"Cache-Control": "no-store"}


@router.get("/history/", response_class=HTMLResponse)
def history(request: Request, repo: StatsRepoDep, deleted: str | None = None):
    sessions = repo.list_sessions()
    return templates.TemplateResponse(
        request,
        "history.html",
        {"sessions": sessions, "deleted": deleted == "1"},
        headers=NO_CACHE,
    )


@router.post("/history/{session_id}/delete", response_class=HTMLResponse)
def delete_session(session_id: str, repo: StatsRepoDep):
    repo.delete_session(session_id)
    return RedirectResponse(url=prefix_url("/history/?deleted=1"), status_code=303)


@router.get("/stats/", response_class=HTMLResponse)
def stats(request: Request, repo: StatsRepoDep, syllabus_id: str | None = None):
    syllabi = repo.syllabi_with_activity()
    ids = {s["id"] for s in syllabi}
    selected = syllabus_id if syllabus_id in ids else (syllabi[0]["id"] if syllabi else None)
    data = repo.syllabus_stats(selected) if selected else None
    max_score = max((p["score"] for p in data["evolution"]), default=10) if data else 10
    return templates.TemplateResponse(
        request,
        "stats.html",
        {"syllabi": syllabi, "selected": selected, "stats": data, "scale_max": max(10.0, max_score)},
        headers=NO_CACHE,
    )
