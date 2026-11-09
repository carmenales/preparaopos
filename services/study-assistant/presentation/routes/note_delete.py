"""Borrar un apunte: confirmación y borrado definitivo (no hay archivado, a propósito).

El fichero lo borra knowledge-service, que es quien escribe en knowledge/ y regenera el índice.
Aquí se pide confirmación, se avisa de las preguntas enlazadas, se recarga el índice en memoria
y se borran los enlaces del apunte en linking-service.

Se identifica el apunte por id y ruta: hay ids repetidos en el índice y borrar solo por id
podría eliminar el fichero equivocado.
"""

from __future__ import annotations

from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from domain.notes.models import Note
from infrastructure.knowledge_service.client import KnowledgeServiceError
from infrastructure.linking.client import LinkingClient
from presentation.routes.ingest import ClientDep

router = APIRouter()
NO_CACHE = {"Cache-Control": "no-store"}


def get_linking_client() -> LinkingClient:
    return LinkingClient()


LinkingDep = Annotated[LinkingClient, Depends(get_linking_client)]


def _find_note(request: Request, note_id: str, path: str) -> Note:
    svc = request.app.state.note_service
    if path:
        note = next((n for n in svc.notes if n.id == note_id and n.path == path), None)
    else:
        note = svc.find_by_id(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Nota no encontrada: {note_id}")
    return note


def _confirm_page(request: Request, note: Note, linking: LinkingClient, *, error: str | None = None,
                  status_code: int = 200):
    svc = request.app.state.note_service
    same_id = [n for n in svc.notes if n.id == note.id and n.path != note.path]
    return request.app.state.templates.TemplateResponse(request, "note_delete.html", {
        "note": note, "linked_count": linking.count_links_by_note(note.id), "same_id": same_id, "error": error,
        "process_titles": {p: svc.format_process_title(p) for p in note.processes},
    }, status_code=status_code, headers=NO_CACHE)


# Handlers síncronos: llaman a otros servicios con clientes HTTP síncronos.

@router.get("/notes/{note_id}/delete", response_class=HTMLResponse)
def confirm_delete(request: Request, note_id: str, linking: LinkingDep, path: str = ""):
    return _confirm_page(request, _find_note(request, note_id, path), linking)


@router.post("/notes/{note_id}/delete", response_class=HTMLResponse)
def delete_note(request: Request, note_id: str, client: ClientDep, linking: LinkingDep,
                path: Annotated[str, Form()] = ""):
    note = _find_note(request, note_id, path)
    try:
        result = client.delete_note(note.path)
    except KnowledgeServiceError as exc:
        return _confirm_page(request, note, linking, error=str(exc), status_code=502)

    request.app.state.reload_notes()
    warnings = list(result.get("warnings") or [])
    # Si queda otro apunte con el mismo id, sus enlaces son también de ese apunte: no se tocan.
    if request.app.state.note_service.find_by_id(note.id) is None and not linking.delete_links_by_note(note.id):
        warnings.append("No se han podido borrar sus enlaces con preguntas (linking-service no responde); "
                        "las preguntas seguirán ofreciendo este apunte hasta que se quiten a mano.")
    params = {"deleted": note.title}
    if note.processes:
        params["process"] = note.processes[0]
    if warnings:
        params["warn"] = " ".join(warnings)
    return RedirectResponse(url="/?" + urlencode(params), status_code=303)
