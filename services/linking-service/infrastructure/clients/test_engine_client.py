"""Cliente HTTP para interactuar con test-engine."""

from __future__ import annotations

import httpx
from typing import Any


class TestEngineClient:
    def __init__(self, base_url: str, client: httpx.Client | None = None) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = client or httpx.Client(timeout=10.0)

    def _get(self, path: str, params: dict | None = None) -> httpx.Response:
        url = f"{self._base_url}{path}"
        return self._client.get(url, params=params)

    def get_syllabus_tags(self, syllabus_id: str) -> list[dict[str, Any]]:
        """Consulta las etiquetas de temario asociadas a preguntas para un temario dado."""
        resp = self._get("/api/syllabus-tags", params={"syllabus_id": syllabus_id})
        if resp.status_code != 200:
            raise RuntimeError(f"Error al obtener syllabus-tags ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_question(self, question_id: int) -> dict[str, Any] | None:
        """Consulta los datos y extracto de una pregunta."""
        resp = self._get(f"/api/questions/{question_id}")
        if resp.status_code == 404:
            return None
        if resp.status_code != 200:
            raise RuntimeError(f"Error al obtener pregunta {question_id} ({resp.status_code}): {resp.text}")
        return resp.json()
