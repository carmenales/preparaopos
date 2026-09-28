"""Configuración del servicio Study Assistant."""

import os
from pathlib import Path


# --- Rutas ---

# Raíz del servicio
SERVICE_ROOT = Path(__file__).resolve().parent

# Raíz del repositorio (2 niveles arriba: services/study-assistant/ → repo root)
REPO_ROOT = SERVICE_ROOT.parent.parent

# Base de conocimiento (ficheros Markdown)
KNOWLEDGE_BASE_PATH = Path(
    os.getenv("KNOWLEDGE_BASE_PATH", str(REPO_ROOT / "knowledge"))
)

# Índice pregenerado de notas (reutiliza el generado por scripts/build_knowledge_index.py)
KNOWLEDGE_INDEX_PATH = Path(
    os.getenv(
        "KNOWLEDGE_INDEX_PATH",
        str(REPO_ROOT / "apps" / "studyassistant" / "data" / "knowledge_index.json"),
    )
)

# --- Servicios externos ---

# URL del microservicio de embeddings (para búsqueda semántica)
EMBEDDINGS_SERVICE_URL = os.getenv("EMBEDDINGS_SERVICE_URL", "http://localhost:8091")

# URL base de Preparador TAI (para enlaces de práctica)
PREPARADORTAI_BASE_URL = os.getenv("PREPARADORTAI_BASE_URL", "http://localhost:8080")

# --- Servidor ---

HOST = os.getenv("SA_HOST", "0.0.0.0")
PORT = int(os.getenv("SA_PORT", "8095"))

# --- Templates ---

TEMPLATES_DIR = SERVICE_ROOT / "presentation" / "templates"
STATIC_DIR = SERVICE_ROOT / "presentation" / "static"
