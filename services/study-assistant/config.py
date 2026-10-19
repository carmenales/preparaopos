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

# Microservicio de linking (comunicación interna)
LINKING_SERVICE_INTERNAL_URL = os.getenv("LINKING_SERVICE_INTERNAL_URL", os.getenv("LINKING_SERVICE_URL", "http://localhost:8097"))
LINKING_SERVICE_URL = LINKING_SERVICE_INTERNAL_URL

# Motor de tests (separación entre URL interna y URL pública vista por el navegador)
TEST_ENGINE_INTERNAL_URL = os.getenv("TEST_ENGINE_INTERNAL_URL", os.getenv("TEST_ENGINE_URL", "http://localhost:8096"))
TEST_ENGINE_PUBLIC_URL = os.getenv("TEST_ENGINE_PUBLIC_URL", os.getenv("TEST_ENGINE_URL", "http://localhost:8096"))
TEST_ENGINE_URL = TEST_ENGINE_PUBLIC_URL

# Servicio de ingesta (PDF → Markdown, refinado con Ollama y publicación en knowledge/)
KNOWLEDGE_SERVICE_INTERNAL_URL = os.getenv("KNOWLEDGE_SERVICE_INTERNAL_URL", "http://localhost:8100")
# El refinado con Ollama en CPU puede tardar minutos (knowledge-service usa 900 s de lectura)
KNOWLEDGE_SERVICE_REFINE_TIMEOUT = float(os.getenv("KNOWLEDGE_SERVICE_REFINE_TIMEOUT", "960"))

# --- Servidor ---

HOST = os.getenv("SA_HOST", "0.0.0.0")
PORT = int(os.getenv("SA_PORT", "8095"))

# --- Templates ---

TEMPLATES_DIR = SERVICE_ROOT / "presentation" / "templates"
STATIC_DIR = SERVICE_ROOT / "presentation" / "static"
