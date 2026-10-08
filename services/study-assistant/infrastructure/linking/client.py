"""Cliente HTTP hacia linking-service para Study Assistant."""

from __future__ import annotations

from typing import Any
import httpx

from config import LINKING_SERVICE_URL


class LinkingClient:
    """Cliente HTTP hacia linking-service para resolver preguntas asociadas a un apunte."""

    def __init__(self, base_url: str = LINKING_SERVICE_URL, timeout: float = 1.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_links_by_note(self, note_id: str) -> list[dict[str, Any]]:
        """Devuelve la lista de preguntas vinculadas a un apunte."""
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                resp = client.get(f"/links/by-note/{note_id}")
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return []
