"""Cliente HTTP para interactuar con apuntes-service (study-assistant)."""

from __future__ import annotations

import httpx
from typing import Any


class ApuntesClient:
    def __init__(self, base_url: str, client: httpx.Client | None = None) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = client or httpx.Client(timeout=10.0)

    def _get(self, path: str, params: dict | None = None) -> httpx.Response:
        url = f"{self._base_url}{path}"
        return self._client.get(url, params=params)

    def get_notes_by_process(self, process: str = "") -> list[dict[str, Any]]:
        """Consulta el catálogo de notas por proceso."""
        resp = self._get("/api/notes", params={"process": process} if process else None)
        if resp.status_code != 200:
            raise RuntimeError(f"Error al obtener notas ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_note(self, note_id: str) -> dict[str, Any] | None:
        """Consulta los metadatos de una nota específica."""
        resp = self._get(f"/api/notes/{note_id}")
        if resp.status_code == 404:
            return None
        if resp.status_code != 200:
            raise RuntimeError(f"Error al obtener nota {note_id} ({resp.status_code}): {resp.text}")
        return resp.json()
