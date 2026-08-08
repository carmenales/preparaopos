"""
services/knowledge/ollama_client.py

Cliente contra Ollama, adaptado de scripts/refine_markdown_llm.py (mismo
endpoint /api/generate, mismo patrón de payload con stream=false, mismo
uso de keep_alive para no recargar el modelo entre llamadas), como
cliente reutilizable dentro del servicio en vez de script CLI.

Módulo plano, sin subcarpeta adapters/.
"""

from __future__ import annotations

import httpx

from config import settings


class OllamaClientError(RuntimeError):
    """Error de comunicación con Ollama o respuesta vacía/no válida."""


class OllamaClient:
    def __init__(
        self,
        base_url: str = settings.ollama_url,
        model: str = settings.ollama_model,
        connect_timeout_seconds: float = settings.ollama_connect_timeout_seconds,
        read_timeout_seconds: float = settings.ollama_read_timeout_seconds,
        num_predict: int = settings.ollama_num_predict,
        temperature: float = settings.ollama_temperature,
        keep_alive: str = settings.ollama_keep_alive,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = httpx.Timeout(connect=connect_timeout_seconds, read=read_timeout_seconds)
        self._num_predict = num_predict
        self._temperature = temperature
        self._keep_alive = keep_alive

    def generate(self, prompt: str) -> str:
        """
        Llama a POST /api/generate con stream=false y devuelve el texto
        completo generado. Lanza OllamaClientError si Ollama no responde
        o devuelve una respuesta vacía.
        """
        url = f"{self._base_url}/api/generate"

        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": self._keep_alive,
            "options": {
                "temperature": self._temperature,
                "num_predict": self._num_predict,
            },
        }

        try:
            response = httpx.post(url, json=payload, timeout=self._timeout)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OllamaClientError(
                f"No se ha podido generar contenido con Ollama ({self._model}) en {url}: {exc}"
            ) from exc

        data = response.json()
        text = (data.get("response") or "").strip()

        if not text:
            raise OllamaClientError("Ollama ha devuelto una respuesta vacía.")

        return text
