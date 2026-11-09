"""Router de catálogo: lista exámenes y bloques disponibles para iniciar sesión."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import text

from presentation.dependencies import DbDep
from presentation.templating import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def catalog(request: Request, db: DbDep):
    """Pantalla principal: fichas con totales y la tabla de exámenes oficiales con su último resultado."""
    rows = db.execute(
        text(
            """
            SELECT e.id, e.name, e.year, e.convocatoria, e.duration_seconds,
                   (SELECT COUNT(*) FROM exam_questions eq
                     WHERE eq.exam_id = e.id AND eq.is_reserve = 0) AS n_questions,
                   (SELECT COUNT(*) FROM test_sessions s
                     WHERE s.exam_id = e.id AND s.closed_at IS NOT NULL) AS n_done,
                   (SELECT s.final_score FROM test_sessions s
                     WHERE s.exam_id = e.id AND s.closed_at IS NOT NULL
                     ORDER BY s.closed_at DESC LIMIT 1) AS last_score
              FROM exams e
             ORDER BY e.year DESC, e.id DESC
            """
        )
    ).fetchall()

    exams = [
        {
            "id": r.id,
            "name": r.name,
            "year": r.year,
            "convocatoria": r.convocatoria,
            "duration_min": (r.duration_seconds // 60) if r.duration_seconds else None,
            "n_questions": r.n_questions,
            "n_done": r.n_done,
            "last_score": float(r.last_score) if r.last_score is not None else None,
        }
        for r in rows
    ]
    totals = {
        "exams": len(exams),
        "questions": db.execute(text("SELECT COUNT(*) FROM questions")).scalar() or 0,
        "done": db.execute(text("SELECT COUNT(*) FROM test_sessions WHERE closed_at IS NOT NULL")).scalar() or 0,
        "doubtful": db.execute(text("SELECT COUNT(*) FROM question_marks WHERE doubtful = 1")).scalar() or 0,
    }

    return templates.TemplateResponse(
        request,
        "catalog.html",
        {"exams": exams, "totals": totals},
    )
