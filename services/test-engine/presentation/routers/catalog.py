"""Router de catálogo: lista exámenes y bloques disponibles para iniciar sesión."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from config import TEMPLATES_DIR
from presentation.dependencies import DbDep

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


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
