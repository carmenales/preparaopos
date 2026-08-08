"""
services/knowledge/config.py

Configuración centralizada del Knowledge Service. Un dataclass simple
leyendo variables de entorno, sin pydantic-settings ni ficheros .env
propios — no hace falta más para el número de parámetros de este
milestone.

- SEARCH_SERVICE_URL: nombre de red Docker Compose del contenedor
  `embeddings` (services/embeddings/), el mismo que ya usa
  apps/studyassistant/search.php.
- OLLAMA_URL: Ollama corre en el host, fuera de Docker. Desde un
  contenedor, "host.docker.internal" es el nombre que Docker Desktop
  (Windows/Mac) resuelve al host; requiere `extra_hosts:
  host.docker.internal:host-gateway` en el servicio del docker-compose.
- OLLAMA_MODEL: el default "llama3.1:latest" no es una decisión nueva
  de este servicio — es el modelo ya instalado y confirmado funcionando
  en este repo (el mismo que usa scripts/refine_markdown_llm.py).
  Sigue siendo 100% configurable vía variable de entorno.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _get_int(name: str, default: int) -> int:
    return int(os.environ.get(name, str(default)))


def _get_float(name: str, default: float) -> float:
    return float(os.environ.get(name, str(default)))


@dataclass(frozen=True)
class Settings:
    # --- Servicio de búsqueda semántica (services/embeddings) ---
    search_service_url: str = os.environ.get("SEARCH_SERVICE_URL", "http://embeddings:8000")
    search_timeout_seconds: float = _get_float("SEARCH_TIMEOUT_SECONDS", 10.0)

    # --- Ollama ---
    ollama_url: str = os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434")
    ollama_model: str = os.environ.get("OLLAMA_MODEL", "llama3.1:latest")
    ollama_connect_timeout_seconds: float = _get_float("OLLAMA_CONNECT_TIMEOUT_SECONDS", 10.0)
    ollama_read_timeout_seconds: float = _get_float("OLLAMA_READ_TIMEOUT_SECONDS", 600.0)
    # num_predict alto porque en este milestone el apunte completo se
    # genera en UNA sola llamada al LLM. note_generator.py está separado
    # en una función de "generar para un conjunto de fragmentos" y una
    # de "orquestar la nota completa" precisamente para poder pasar a
    # generación por secciones más adelante sin tocar este cliente.
    ollama_num_predict: int = _get_int("OLLAMA_NUM_PREDICT", 800)
    ollama_temperature: float = _get_float("OLLAMA_TEMPERATURE", 0.0)
    ollama_keep_alive: int = _get_int("OLLAMA_KEEP_ALIVE", -1)

    # --- Recuperación (topic_retriever) ---
    default_top_k: int = _get_int("NOTE_GENERATION_TOP_K", 20)
    default_min_score: float = _get_float("NOTE_GENERATION_MIN_SCORE", 0.35)

    # --- Rutas ---
    prompts_dir: Path = Path(os.environ.get("PROMPTS_DIR", "prompts"))


settings = Settings()
