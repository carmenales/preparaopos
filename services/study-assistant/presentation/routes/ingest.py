"""Asistente de ingesta: PDF → Markdown → revisión (con refinado opcional en Ollama) → apunte publicado.

Sustituye a apps/studyassistant/ingest.php. Toda la extracción, el refinado y la
escritura en knowledge/ los hace knowledge-service; aquí solo está la interfaz y,
tras publicar, la recarga del índice para que el apunte se vea sin reiniciar.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse

from domain.markdown.renderer import render
from infrastructure.knowledge_service.client import KnowledgeServiceClient, KnowledgeServiceError

router = APIRouter(prefix="/ingest")

STATUSES = ["borrador", "revisado"]
NO_CACHE = {"Cache-Control": "no-store"}
MAX_PDF_BYTES = 50 * 1024 * 1024


def get_knowledge_client() -> KnowledgeServiceClient:
    return KnowledgeServiceClient()


ClientDep = Annotated[KnowledgeServiceClient, Depends(get_knowledge_client)]


def _processes(request: Request) -> list[dict]:
    svc = request.app.state.note_service
    return [{"slug": p, "title": svc.format_process_title(p)} for p in svc.collect_unique("processes")]


def _upload_form(request: Request, *, error: str | None = None, values: dict | None = None, status_code: int = 200):
    templates = request.app.state.templates
    return templates.TemplateResponse(request, "ingest_upload.html", {
        "processes": _processes(request), "error": error,
        "v": values or {"process_slug": "", "custom_process": "", "source": "academia", "normalize": True},
    }, status_code=status_code, headers=NO_CACHE)


def _review_form(request: Request, v: dict, *, error: str | None = None, info: dict | None = None,
                 status_code: int = 200):
    templates = request.app.state.templates
    return templates.TemplateResponse(request, "ingest_review.html", {
        "v": v, "error": error, "info": info or {}, "statuses": STATUSES,
        "preview_html": render(v.get("markdown", "")),
    }, status_code=status_code, headers=NO_CACHE)


@router.get("/", response_class=HTMLResponse)
def upload_form(request: Request):
    return _upload_form(request)


@router.post("/extract", response_class=HTMLResponse)
def extract(
    request: Request,
    client: ClientDep,
    pdf_file: Annotated[UploadFile, File()],
    process_slug: Annotated[str, Form()] = "",
    custom_process: Annotated[str, Form()] = "",
    source: Annotated[str, Form()] = "",
    normalize: Annotated[str | None, Form()] = None,
):
    values = {"process_slug": process_slug, "custom_process": custom_process, "source": source,
              "normalize": bool(normalize)}
    process = (custom_process.strip().strip("/") if process_slug == "__otro__" else process_slug.strip())
    if not process:
        return _upload_form(request, error="Elige el proceso al que pertenece el apunte.", values=values,
                            status_code=422)
    if not (pdf_file.filename or "").lower().endswith(".pdf"):
        return _upload_form(request, error="El fichero debe ser un PDF.", values=values, status_code=422)
    content = pdf_file.file.read(MAX_PDF_BYTES + 1)
    if not content:
        return _upload_form(request, error="El PDF está vacío.", values=values, status_code=422)
    if len(content) > MAX_PDF_BYTES:
        return _upload_form(request, error="El PDF pasa de 50 MB.", values=values, status_code=422)

    try:
        data = client.extract_pdf(content, pdf_file.filename, normalize=bool(normalize))
    except KnowledgeServiceError as exc:
        return _upload_form(request, error=str(exc), values=values, status_code=502)

    review = {
        "process_slug": process, "source": source.strip() or "academia",
        "title": data.get("detected_title", ""), "official_topic": data.get("official_topic", ""),
        "tags": "", "status": "borrador", "markdown": data.get("markdown", ""),
        "ai_cleaned": False, "needs_human_review": False,
    }
    info = {"filename": pdf_file.filename, "page_count": data.get("page_count"),
            "headings": len(data.get("headings", [])), "warnings": data.get("warnings", [])}
    return _review_form(request, review, info=info)


@router.post("/preview", response_class=HTMLResponse)
def preview(markdown: Annotated[str, Form()] = ""):
    """Fragmento htmx con el apunte renderizado igual que en el visor."""
    return HTMLResponse(render(markdown) or '<p class="muted">Sin contenido.</p>', headers=NO_CACHE)


@router.post("/refine", response_class=HTMLResponse)
def refine(
    request: Request,
    client: ClientDep,
    markdown: Annotated[str, Form()] = "",
    instructions: Annotated[str, Form()] = "",
):
    """Fragmento htmx: el editor con el texto refinado, o con el original y un aviso si falla."""
    templates = request.app.state.templates
    error = None
    refined = markdown
    if not markdown.strip():
        error = "No hay texto que refinar."
    else:
        try:
            refined = client.refine(markdown, instructions).get("refined_markdown") or markdown
        except KnowledgeServiceError as exc:
            error = f"{exc} Se conserva el texto sin refinar."
    return templates.TemplateResponse(request, "partials/ingest_editor.html",
                                      {"markdown": refined, "refine_error": error,
                                       "refined": error is None}, headers=NO_CACHE)


@router.post("/publish", response_class=HTMLResponse)
def publish(
    request: Request,
    client: ClientDep,
    process_slug: Annotated[str, Form()] = "",
    source: Annotated[str, Form()] = "",
    title: Annotated[str, Form()] = "",
    official_topic: Annotated[str, Form()] = "",
    tags: Annotated[str, Form()] = "",
    status: Annotated[str, Form()] = "borrador",
    markdown: Annotated[str, Form()] = "",
    ai_cleaned: Annotated[str | None, Form()] = None,
    needs_human_review: Annotated[str | None, Form()] = None,
):
    v = {"process_slug": process_slug, "source": source, "title": title, "official_topic": official_topic,
         "tags": tags, "status": status, "markdown": markdown, "ai_cleaned": bool(ai_cleaned),
         "needs_human_review": bool(needs_human_review)}
    errors = [msg for ok, msg in (
        (title.strip(), "El título es obligatorio."),
        (markdown.strip(), "El apunte está vacío."),
        (process_slug.strip(), "Falta el proceso."),
        (status in STATUSES, "Estado no válido."),
    ) if not ok]
    if errors:
        return _review_form(request, v, error=" ".join(errors), status_code=422)

    payload = {
        "process_slug": process_slug.strip(), "title": title.strip(), "official_topic": official_topic.strip(),
        "markdown_body": markdown, "status": status, "source": source.strip() or "academia",
        "tags": [t.strip().lower() for t in tags.split(",") if t.strip()],
        "ai_cleaned": bool(ai_cleaned),
        "needs_human_review": bool(needs_human_review),
    }
    try:
        result = client.publish(payload)
    except KnowledgeServiceError as exc:
        return _review_form(request, v, error=str(exc), status_code=502)

    request.app.state.reload_notes()
    return RedirectResponse(url=f"/notes/{result['note_id']}?published=1", status_code=303)
