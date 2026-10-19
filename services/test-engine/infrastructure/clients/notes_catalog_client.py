"""Catálogo de apuntes de study-assistant (GET /api/notes) para elegir a qué apunte enlazar."""

from __future__ import annotations

from typing import Any

import httpx

from config import STUDY_ASSISTANT_INTERNAL_URL


class NotesCatalogClient:
    def __init__(self, base_url: str = STUDY_ASSISTANT_INTERNAL_URL, timeout: float = 5.0) -> None:
        self._client = httpx.Client(base_url=base_url.rstrip("/"), timeout=timeout)

    def list_notes(self) -> list[dict[str, Any]] | None:
        """Todas las notas, o None si study-assistant no responde."""
        try:
            resp = self._client.get("/api/notes")
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return None
