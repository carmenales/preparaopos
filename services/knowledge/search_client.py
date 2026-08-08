"""
services/knowledge/search_client.py

Cliente contra el servicio de búsqueda semántica que ya existe en
services/embeddings/main.py (contenedor `embeddings`, puerto interno
8000 — el mismo que ya usa apps/studyassistant/search.php).

Módulo plano, sin subcarpeta adapters/: una única implementación
concreta, sin interfaz abstracta separada.
"""

from __future__ import annotations

import httpx

from config import settings
from schemas import RetrievedFragment


class SearchClientError(RuntimeError):
    """Error de comunicación con el servicio de búsqueda semántica."""


class SearchClient:
    def __init__(
        self,
        base_url: str = settings.search_service_url,
        timeout_seconds: float = settings.search_timeout_seconds,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def search(self, query: str, top_k: int) -> list[RetrievedFragment]:
        """
        Llama a GET /search?q=...&top_k=... del servicio `embeddings`.

        El servicio ya devuelve, por chunk: note_id, note_title, heading,
        anchor, text_preview, score, chunk_id, source_id, content, tags
        (ver Milestone 0, confirmado con datos reales). Aquí solo
        normalizamos esa respuesta a RetrievedFragment.
        """
        url = f"{self._base_url}/search"

        try:
            response = httpx.get(
                url,
                params={"q": query, "top_k": top_k},
                timeout=self._timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise SearchClientError(
                f"No se ha podido contactar con el servicio de búsqueda semántica en {url}: {exc}"
            ) from exc

        data = response.json()

        if data.get("warning"):
            # Índice vacío u otra advertencia no fatal del servicio.
            return []

        raw_results = data.get("results", [])
        fragments: list[RetrievedFragment] = []

        for raw in raw_results:
            note_id = raw.get("note_id")
            content = raw.get("content")

            if not note_id or not content:
                # Defensivo: si algún chunk no tuviera todavía content
                # (índice sin reconstruir con Milestone 0), lo
                # descartamos en vez de fallar toda la petición.
                continue

            fragments.append(
                RetrievedFragment(
                    chunk_id=raw.get("chunk_id"),
                    note_id=note_id,
                    source_id=raw.get("source_id") or note_id,
                    note_title=raw.get("note_title", ""),
                    heading=raw.get("heading"),
                    anchor=raw.get("anchor"),
                    score=float(raw.get("score", 0.0)),
                    content=content,
                    tags=raw.get("tags") or [],
                )
            )

        return fragments
