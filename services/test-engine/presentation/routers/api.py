"""Router de API REST para integración entre servicios (linking-service, etc.)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from infrastructure.db import orm_models as orm
from presentation.dependencies import DbDep

router = APIRouter(prefix="/api")


@router.get("/syllabus-tags")
def list_syllabus_tags(
    db: DbDep,
    syllabus_id: str = Query(..., description="Identificador del temario (ej: age-gsi-official)"),
):
    """Devuelve las etiquetas de temario asociadas a preguntas para un temario dado."""
    stmt = (
        select(orm.QuestionSyllabusTag)
        .where(orm.QuestionSyllabusTag.syllabus_id == syllabus_id)
        .order_by(orm.QuestionSyllabusTag.question_id)
    )
    rows = db.scalars(stmt).all()
    return [
        {
            "question_id": r.question_id,
            "syllabus_id": r.syllabus_id,
            "block": r.block,
            "topic": r.topic,
        }
        for r in rows
    ]


@router.get("/questions/{question_id}")
def get_question(
    question_id: int,
    db: DbDep,
):
    """Devuelve los datos básicos y extracto de una pregunta junto al nombre de su examen."""
    q = db.get(orm.Question, question_id)
    if not q:
        raise HTTPException(status_code=404, detail=f"Pregunta {question_id} no encontrada")

    # Obtener el nombre del examen si está asociada a uno
    exam_name = None
    eq = db.scalar(
        select(orm.ExamQuestion).where(orm.ExamQuestion.question_id == question_id)
    )
    if eq:
        exam = db.get(orm.Exam, eq.exam_id)
        if exam:
            exam_name = exam.name

    statement = q.statement or ""
    excerpt = (statement[:120] + "...") if len(statement) > 120 else statement

    return {
        "id": q.id,
        "statement": statement,
        "excerpt": excerpt,
        "exam_name": exam_name,
    }
