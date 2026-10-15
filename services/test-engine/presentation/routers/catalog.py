"""Router de catálogo: lista exámenes y bloques disponibles para iniciar sesión."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from config import TEMPLATES_DIR, prefix_url
from presentation.dependencies import DbDep
from presentation.templating import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def catalog(request: Request, db: DbDep):
    """Pantalla principal: lista exámenes oficiales disponibles."""
    rows = db.execute(
        text("SELECT id, name, year, convocatoria, duration_seconds FROM exams ORDER BY year DESC, id DESC")
    ).fetchall()

    exams = [
        {
            "id": r.id,
            "name": r.name,
            "year": r.year,
            "convocatoria": r.convocatoria,
            "duration_min": (r.duration_seconds // 60) if r.duration_seconds else None,
        }
        for r in rows
    ]

    return templates.TemplateResponse(
        request,
        "catalog.html",
        {"exams": exams},
    )


@router.post("/practice/by-note/{note_id}")
async def practice_by_note_redirect(note_id: str):
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=prefix_url(f"/sessions/practice/by-note/{note_id}"), status_code=307)


