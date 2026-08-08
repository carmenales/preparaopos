"""
Servicio de búsqueda semántica sobre los apuntes de knowledge/.

No llama a ninguna API externa ni tiene coste por uso: el modelo de
embeddings se descarga una vez desde Hugging Face (sentence-transformers)
la primera vez que arranca el contenedor, y a partir de ahí corre
enteramente en local, en CPU.

Endpoints:
    GET /health
    GET /search?q=...&top_k=8

El índice (fragmentos + vectores) lo genera aparte
scripts/build_semantic_index.py — este servicio solo lo carga y sirve
búsquedas contra él.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException, Query
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
DATA_DIR = Path("/workspace/apps/studyassistant/data")
CHUNKS_PATH = DATA_DIR / "semantic_chunks.json"
EMBEDDINGS_PATH = DATA_DIR / "semantic_embeddings.npy"

app = FastAPI(title="preparaopos-embeddings")

_model: SentenceTransformer | None = None
_chunks: list[dict] = []
_embeddings: np.ndarray | None = None


def _normalize_rows(vectors: np.ndarray) -> np.ndarray:
    """Normaliza cada fila a norma 1, para que el producto escalar sea coseno."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1e-8
    return vectors / norms


@app.on_event("startup")
def load_resources() -> None:
    global _model, _chunks, _embeddings

    _model = SentenceTransformer(MODEL_NAME)

    if CHUNKS_PATH.exists() and EMBEDDINGS_PATH.exists():
        _chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
        _embeddings = _normalize_rows(np.load(EMBEDDINGS_PATH).astype(np.float32))
    else:
        # Todavía no se ha ejecutado build_semantic_index.py.
        _chunks = []
        _embeddings = np.zeros((0, 384), dtype=np.float32)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "indexed_chunks": len(_chunks),
    }


@app.get("/search")
def search(
    q: str = Query(..., min_length=1),
    top_k: int = Query(8, ge=1, le=50),
) -> dict:
    if _model is None or _embeddings is None:
        raise HTTPException(status_code=503, detail="El modelo todavía no ha terminado de cargar.")

    if len(_chunks) == 0:
        return {
            "query": q,
            "results": [],
            "warning": "El índice semántico está vacío. Ejecuta scripts/build_semantic_index.py.",
        }

    query_vector = _model.encode([q], normalize_embeddings=True)[0].astype(np.float32)
    scores = _embeddings @ query_vector  # ya normalizados -> producto escalar = coseno

    k = min(top_k, len(_chunks))
    top_indices = np.argsort(-scores)[:k]

    results = []
    for idx in top_indices:
        idx = int(idx)
        chunk = _chunks[idx]
        results.append({
            "note_id": chunk["note_id"],
            "note_title": chunk["note_title"],
            "heading": chunk["heading"],
            "anchor": chunk["anchor"],
            "text_preview": chunk["text_preview"],
            "score": round(float(scores[idx]), 4),
            "chunk_id": chunk.get("chunk_id"),
            "source_id": chunk.get("source_id"),
            "content": chunk.get("content"),
            "tags": chunk.get("tags", []),
        })

    return {"query": q, "results": results}
