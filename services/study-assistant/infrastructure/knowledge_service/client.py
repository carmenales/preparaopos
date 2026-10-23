"""Cliente HTTP hacia knowledge-service (ingesta de PDF, refinado con Ollama y publicación)."""

from __future__ import annotations

from typing import Any

import httpx

from config import KNOWLEDGE_SERVICE_INTERNAL_URL, KNOWLEDGE_SERVICE_REFINE_TIMEOUT


class KnowledgeServiceError(RuntimeError):
    """Error comprensible para mostrar en la interfaz."""


class KnowledgeServiceClient:
    def __init__(self, base_url: str = KNOWLEDGE_SERVICE_INTERNAL_URL,
                 refine_timeout: float = KNOWLEDGE_SERVICE_REFINE_TIMEOUT) -> None:
        self.base_url = base_url.rstrip("/")
        self.refine_timeout = refine_timeout

    def _post(self, path: str, *, timeout: float, **kwargs) -> dict[str, Any]:
        try:
            resp = httpx.post(f"{self.base_url}{path}", timeout=timeout, **kwargs)
        except httpx.TimeoutException as exc:
            raise KnowledgeServiceError(
                "El servicio de ingesta ha tardado demasiado en responder. "
                "Si estabas refinando con Ollama, prueba con un texto más corto."
            ) from exc
        except httpx.HTTPError as exc:
            raise KnowledgeServiceError(
                "No se puede contactar con el servicio de ingesta (knowledge-service). "
                "¿Está levantado? → docker compose up -d knowledge-service"
            ) from exc
        if resp.status_code >= 400:
            try:
                detail = resp.json().get("detail")
            except ValueError:
                detail = resp.text[:300]
            raise KnowledgeServiceError(f"El servicio de ingesta ha devuelto un error ({resp.status_code}): {detail}")
        return resp.json()

    def extract_pdf(self, pdf_bytes: bytes, filename: str, normalize: bool = True) -> dict[str, Any]:
        return self._post(
            "/ingest/extract-pdf", timeout=120,
            files={"file": (filename, pdf_bytes, "application/pdf")},
            data={"normalize": "true" if normalize else "false"},
        )

    def refine(self, markdown: str, instructions: str = "") -> dict[str, Any]:
        return self._post("/ingest/refine", timeout=self.refine_timeout,
                          json={"markdown": markdown, "instructions": instructions})

    def publish(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._post("/ingest/publish", timeout=120, json=payload)

    def delete_note(self, path: str) -> dict[str, Any]:
        """Borra definitivamente el fichero del apunte (ruta del índice) y regenera el índice."""
        return self._post("/notes/delete", timeout=120, json={"path": path})
