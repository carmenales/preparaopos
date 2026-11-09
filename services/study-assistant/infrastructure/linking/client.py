"""Cliente HTTP hacia linking-service para Study Assistant."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

from config import LINKING_SERVICE_URL


class LinkingClient:
    """Cliente HTTP hacia linking-service para resolver preguntas asociadas a un apunte."""

    def __init__(self, base_url: str = LINKING_SERVICE_URL, timeout: float = 3.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(base_url=self.base_url, timeout=self.timeout)

    def get_links_by_note(self, note_id: str) -> list[dict[str, Any]]:
        """Devuelve la lista de preguntas vinculadas a un apunte."""
        try:
            resp = self._client.get(f"/links/by-note/{note_id}")
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return []

    def count_links_by_note(self, note_id: str) -> int | None:
        """Número de preguntas enlazadas, o None si linking-service no responde."""
        try:
            resp = self._client.get(f"/links/by-note/{quote(note_id, safe='')}/question-ids")
            if resp.status_code == 200:
                return len(resp.json())
        except Exception:
            pass
        return None

    def delete_links_by_note(self, note_id: str) -> bool:
        """Borra los enlaces de un apunte borrado. Devuelve si se ha podido."""
        try:
            resp = self._client.delete(f"/links/by-note/{quote(note_id, safe='')}")
            return resp.status_code == 200
        except Exception:
            return False

