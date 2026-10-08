"""Cliente HTTP hacia linking-service para Test Engine."""

from __future__ import annotations

from typing import Any
import httpx

from config import LINKING_SERVICE_URL


class LinkingClient:
    """Cliente HTTP hacia linking-service con degradación elegante."""

    def __init__(self, base_url: str = LINKING_SERVICE_URL, timeout: float = 1.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_links_by_question(self, question_id: int) -> list[dict[str, Any]]:
        """Obtiene las notas enlazadas para una pregunta."""
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                resp = client.get(f"/links/by-question/{question_id}")
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return []

    def get_links_by_questions(self, question_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
        """Obtiene las notas enlazadas para un listado de preguntas (batch)."""
        if not question_ids:
            return {}
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                resp = client.post("/links/by-questions", json={"question_ids": question_ids})
                if resp.status_code == 200:
                    data = resp.json()
                    # Normalizar claves a enteros
                    return {int(k): v for k, v in data.items()}
        except Exception:
            pass
        return {qid: [] for qid in question_ids}

    def get_links_by_note(self, note_id: str) -> list[dict[str, Any]]:
        """Obtiene las preguntas enlazadas para un apunte."""
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                resp = client.get(f"/links/by-note/{note_id}")
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return []
