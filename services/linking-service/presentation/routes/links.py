"""Router de enlaces pregunta-apunte."""

from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter(prefix="/links")


@router.get("/by-question/{question_id}")
async def get_links_by_question(request: Request, question_id: int):
    """Devuelve las notas enlazadas a una pregunta dada."""
    linking_service = request.app.state.linking_service
    return linking_service.get_links_by_question(question_id)


@router.post("/by-questions")
async def get_links_by_questions(request: Request, body: dict):
    """Devuelve las notas enlazadas para un listado de IDs de preguntas."""
    linking_service = request.app.state.linking_service
    question_ids = body.get("question_ids", [])
    return linking_service.get_links_by_question_ids(question_ids)


@router.get("/by-note/{note_id}")
async def get_links_by_note(request: Request, note_id: str):
    """Devuelve las preguntas enlazadas a un apunte dado."""
    linking_service = request.app.state.linking_service
    return linking_service.get_links_by_note(note_id)
