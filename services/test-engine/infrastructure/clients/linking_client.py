"""Cliente HTTP hacia linking-service para Test Engine."""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import quote

import httpx

from config import LINKING_SERVICE_URL

# Las lecturas degradan a «sin enlaces» para no romper el test, pero el fallo queda en el log:
# si no, un linking-service caído es indistinguible de una pregunta sin apuntes.
log = logging.getLogger("test-engine.linking")


class LinkingClient:
    """Cliente HTTP hacia linking-service con degradación elegante."""

    def __init__(self, base_url: str = LINKING_SERVICE_URL, timeout: float = 3.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(base_url=self.base_url, timeout=self.timeout)

    def get_links_by_question(self, question_id: int) -> list[dict[str, Any]]:
        """Obtiene las notas enlazadas para una pregunta."""
        try:
            resp = self._client.get(f"/links/by-question/{question_id}")
            if resp.status_code == 200:
                return resp.json()
            log.warning("linking-service respondió %s", resp.status_code)
        except Exception as exc:
            log.warning("linking-service no responde: %s", exc)
        return []

    def get_links_by_questions(self, question_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
        """Obtiene las notas enlazadas para un listado de preguntas (batch)."""
        if not question_ids:
            return {}
        try:
            resp = self._client.post("/links/by-questions", json={"question_ids": question_ids})
            if resp.status_code == 200:
                data = resp.json()
                # Normalizar claves a enteros
                return {int(k): v for k, v in data.items()}
            log.warning("linking-service respondió %s", resp.status_code)
        except Exception as exc:
            log.warning("linking-service no responde: %s", exc)
        return {qid: [] for qid in question_ids}

    def get_links_by_note(self, note_id: str) -> list[dict[str, Any]]:
        """Obtiene las preguntas enlazadas para un apunte."""
        try:
            resp = self._client.get(f"/links/by-note/{note_id}")
            if resp.status_code == 200:
                return resp.json()
            log.warning("linking-service respondió %s", resp.status_code)
        except Exception as exc:
            log.warning("linking-service no responde: %s", exc)
        return []

    def get_question_ids_by_note(self, note_id: str) -> list[int]:
        """Obtiene los IDs de preguntas enlazadas para un apunte sin sobrecarga ni llamadas circulares."""
        try:
            resp = self._client.get(f"/links/by-note/{note_id}/question-ids")
            if resp.status_code == 200:
                return [int(x) for x in resp.json()]
            log.warning("linking-service respondió %s", resp.status_code)
        except Exception as exc:
            log.warning("linking-service no responde: %s", exc)
        return []


    # --- Edición manual de enlaces (gestión de preguntas) -------------------
    # A diferencia de las lecturas de arriba, aquí hay que distinguir «sin enlaces»
    # de «linking-service no responde», así que se devuelve None o un mensaje de error.

    def links_for_question(self, question_id: int) -> list[dict[str, Any]] | None:
        """Enlaces activos de la pregunta, o None si linking-service no responde."""
        try:
            resp = self._client.get(f"/links/by-question/{question_id}")
            if resp.status_code == 200:
                return resp.json()
            log.warning("linking-service respondió %s", resp.status_code)
        except Exception as exc:
            log.warning("linking-service no responde: %s", exc)
        return None

    def add_link(self, question_id: int, note_id: str, syllabus_id: str) -> str | None:
        """Enlaza a mano pregunta y apunte. Devuelve None si va bien o el motivo del fallo."""
        try:
            resp = self._client.post("/links", json={
                "question_id": question_id, "note_id": note_id, "syllabus_id": syllabus_id})
        except Exception:
            return "linking-service no responde."
        if resp.status_code in (200, 201):
            return None
        return _detail(resp)

    def remove_link(self, question_id: int, note_id: str) -> str | None:
        """Quita un enlace. Devuelve None si va bien o el motivo del fallo."""
        try:
            resp = self._client.delete(f"/links/{question_id}/{quote(note_id, safe='')}")
        except Exception:
            return "linking-service no responde."
        if resp.status_code in (200, 204):
            return None
        return _detail(resp)


def _detail(resp: httpx.Response) -> str:
    try:
        detail = resp.json().get("detail")
    except Exception:
        detail = None
    return detail if isinstance(detail, str) and detail else f"linking-service respondió {resp.status_code}."
