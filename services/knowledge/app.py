"""
services/knowledge/app.py

Punto de entrada del Knowledge Service (FastAPI). Módulo único, sin
subcarpeta api/: con dos endpoints no aporta nada separar el router en
otro paquete todavía.

Alcance de este milestone:

    GET  /health
    POST /notes/generate
        → SearchClient → TopicRetriever → NoteGenerator (Ollama)
        → build_frontmatter (Python, determinista)
        → respuesta JSON con trazabilidad (fragments_used)

No hay escritura a disco ni endpoint /notes/save en este milestone.

Arranque en Docker (ver Dockerfile / docker-compose.yml):
    uvicorn app:app --host 0.0.0.0 --port 8000

Arranque en desarrollo, fuera de Docker:
    uvicorn app:app --reload --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from config import settings
from frontmatter_generator import build_frontmatter
from ingest_service import IngestService
from note_generator import NoteGenerator, NoteGeneratorError
from ollama_client import OllamaClient, OllamaClientError
from schemas import (
    ExtractPdfResponse,
    GenerateNotePreview,
    GenerateNoteRequest,
    PublishNoteRequest,
    PublishNoteResponse,
    RefineMarkdownRequest,
    RefineMarkdownResponse,
)
from search_client import SearchClient, SearchClientError
from topic_retriever import TopicRetriever

app = FastAPI(
    title="preparaopos-knowledge-service",
    description=(
        "Servicio de explotación e ingestión de la base de conocimiento: "
        "generación de apuntes, extracción y normalización de PDFs, refinado con LLM "
        "y publicación directa."
    ),
    version="0.2.0",
)

_search_client = SearchClient()
_ollama_client = OllamaClient()
_topic_retriever = TopicRetriever(_search_client)
_note_generator = NoteGenerator(_ollama_client, settings.prompts_dir)
_ingest_service = IngestService(_ollama_client)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "knowledge-service"}


@app.post("/notes/generate", response_model=GenerateNotePreview)
def generate_note(request: GenerateNoteRequest) -> GenerateNotePreview:
    """
    Genera una VISTA PREVIA del apunte. No escribe nada en disco: la
    respuesta incluye frontmatter, markdown_body y la trazabilidad
    completa de fragmentos usados (fragments_used), con chunk_id,
    note_id, source_id, heading, score y content por fragmento.
    """
    query = request.build_query()

    try:
        fragments = _topic_retriever.retrieve(
            query=query,
            top_k=request.top_k,
            min_score=request.min_score,
        )
    except SearchClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    if not fragments:
        raise HTTPException(
            status_code=422,
            detail=(
                "No se ha encontrado evidencia suficiente en la base de conocimiento "
                "para este tema. Amplía la descripción, baja min_score o revisa el "
                "índice semántico (¿se ha ejecutado build_semantic_index.py?)."
            ),
        )

    try:
        markdown_body, warnings = _note_generator.generate_body(
            topic=request.topic,
            description=request.description,
            fragments=fragments,
        )
    except NoteGeneratorError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except OllamaClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    # El frontmatter es SIEMPRE responsabilidad de Python: build_frontmatter()
    # no recibe markdown_body y deriva source_ids solo de `fragments`.
    frontmatter = build_frontmatter(request, fragments)
    full_markdown = f"{frontmatter.to_yaml_block()}\n\n{markdown_body}\n"

    return GenerateNotePreview(
        frontmatter=frontmatter,
        markdown_body=markdown_body,
        full_markdown=full_markdown,
        fragments_used=fragments,
        warnings=warnings,
    )


@app.get("/ingest/processes")
def list_processes() -> dict:
    """
    Devuelve la lista de procesos disponibles leyendo knowledge_index.json
    o escaneando knowledge/processes/ como fallback.
    """
    import json

    index_path = settings.index_output_path
    if index_path.exists():
        try:
            data = json.loads(index_path.read_text(encoding="utf-8"))
            if "processes" in data:
                return {"processes": data["processes"]}
        except Exception:
            pass

    # Fallback escaneando directorios
    proc_root = settings.knowledge_dir / "processes"
    procs = {}
    if proc_root.exists():
        for p in proc_root.iterdir():
            if p.is_dir() and not p.name.startswith("."):
                procs[p.name] = {"id": p.name, "title": p.name.replace("-", " ").title()}
    return {"processes": procs}


@app.post("/ingest/extract-pdf", response_model=ExtractPdfResponse)
async def extract_pdf(
    file: UploadFile = File(...),
    normalize: bool = Form(True),
) -> ExtractPdfResponse:
    """
    Recibe un archivo PDF en formato multipart, extrae su texto estructurado
    aplicando heurísticas de cabeceras/pies repetidos, headings y normalización.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="El archivo proporcionado no es un PDF válido.",
        )

    try:
        content = await file.read()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Error leyendo el archivo: {exc}")

    if not content:
        raise HTTPException(status_code=400, detail="El archivo PDF está vacío.")

    try:
        result = _ingest_service.extract_from_pdf_bytes(
            pdf_bytes=content,
            filename=file.filename,
            normalize=normalize,
        )
        return ExtractPdfResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Error al procesar el PDF: {exc}") from exc


@app.post("/ingest/refine", response_model=RefineMarkdownResponse)
def refine_markdown(request: RefineMarkdownRequest) -> RefineMarkdownResponse:
    """
    Refina un texto Markdown mediante Ollama (Llama 3.1) para arreglar
    párrafos rotos, tablas o erratas de OCR sin resumir ni inventar información.
    """
    try:
        result = _ingest_service.refine_markdown(
            markdown=request.markdown,
            instructions=request.instructions,
        )
        return RefineMarkdownResponse(**result)
    except OllamaClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/ingest/publish", response_model=PublishNoteResponse)
def publish_note(request: PublishNoteRequest) -> PublishNoteResponse:
    """
    Publica formalmente una nota en la base de conocimiento:
    crea el fichero en knowledge/processes/{process_slug}/apuntes/,
    añade el frontmatter YAML estandarizado y reconstruye knowledge_index.json.
    """
    try:
        return _ingest_service.publish_note(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al publicar la nota: {exc}") from exc
