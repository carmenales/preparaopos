"""Inicio: qué es PreparaOpos, cómo se usa y los tests que tienes a medias."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import text

from presentation.dependencies import DbDep, QuestionRepoDep, StatsRepoDep
from presentation.templating import templates

router = APIRouter()


@router.get("/home", response_class=HTMLResponse)
def home(request: Request, db: DbDep, repo: QuestionRepoDep, stats: StatsRepoDep):
    unfinished = [s for s in stats.list_sessions(limit=300) if not s["is_closed"]][:5]
    totals = {
        "questions": db.execute(text("SELECT COUNT(*) FROM questions WHERE is_annulled = 0")).scalar() or 0,
        "exams": db.execute(text("SELECT COUNT(*) FROM exams")).scalar() or 0,
        "done": db.execute(text("SELECT COUNT(*) FROM test_sessions WHERE closed_at IS NOT NULL")).scalar() or 0,
        "doubtful": db.execute(text("SELECT COUNT(*) FROM question_marks WHERE doubtful = 1")).scalar() or 0,
    }
    return templates.TemplateResponse(
        request, "home.html",
        {"unfinished": unfinished, "totals": totals, "syllabi": repo.list_syllabi_with_counts()},
        headers={"Cache-Control": "no-store"},
    )
