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

from fastapi import FastAPI, HTTPException

from config import settings
from frontmatter_generator import build_frontmatter
from note_generator import NoteGenerator, NoteGeneratorError
from ollama_client import OllamaClient, OllamaClientError
from schemas import GenerateNotePreview, GenerateNoteRequest
from search_client import SearchClient, SearchClientError
from topic_retriever import TopicRetriever

app = FastAPI(
    title="preparaopos-knowledge-service",
    description=(
        "Servicio de explotación de la base de conocimiento: generación "
        "de apuntes en este milestone, y en el futuro, de tests."
    ),
    version="0.1.0",
)

_search_client = SearchClient()
_ollama_client = OllamaClient()
_topic_retriever = TopicRetriever(_search_client)
_note_generator = NoteGenerator(_ollama_client, settings.prompts_dir)


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
