"""Router de enlaces pregunta-apunte."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, Field

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


@router.get("/by-note/{note_id}/question-ids")
async def get_question_ids_by_note(request: Request, note_id: str):
    """Devuelve únicamente los IDs de preguntas enlazadas a un apunte dado."""
    linking_service = request.app.state.linking_service
    return linking_service.get_question_ids_by_note(note_id)



class ManualLinkIn(BaseModel):
    question_id: int
    note_id: str = Field(..., min_length=1)
    syllabus_id: str = Field(..., min_length=1)


# Handlers síncronos: consultan study-assistant con un cliente HTTP síncrono y no deben
# bloquear el bucle de eventos (ver docs/ESTADO.md, bloqueo con async def).
@router.post("", status_code=201)
def add_manual_link(request: Request, body: ManualLinkIn):
    """Añade a mano un enlace pregunta-apunte (o restaura uno retirado)."""
    try:
        return request.app.state.linking_service.add_manual_link(body.question_id, body.note_id, body.syllabus_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


# Va antes de DELETE /{question_id}/{note_id}: si no, «by-note» se tomaría como question_id (422).
@router.delete("/by-note/{note_id}")
def delete_links_by_note(request: Request, note_id: str):
    """Borra todos los enlaces de un apunte que se ha borrado."""
    return {"deleted": request.app.state.linking_service.delete_links_by_note(note_id)}


@router.delete("/{question_id}/{note_id}", status_code=204)
def remove_link(request: Request, question_id: int, note_id: str):
    """Retira un enlace; queda como lápida para que la resolución automática no lo recree."""
    if not request.app.state.linking_service.remove_link(question_id, note_id):
        raise HTTPException(status_code=404, detail="Ese enlace no existe")
    return Response(status_code=204)
