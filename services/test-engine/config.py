"""Configuración del servicio Test Engine."""

import os
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_ROOT.parent.parent

SQLITE_PATH = Path(
    os.getenv(
        "TEST_ENGINE_SQLITE_PATH",
        str(SERVICE_ROOT / "data" / "test_engine.sqlite"),
    )
)

HOST = os.getenv("TE_HOST", "0.0.0.0")
PORT = int(os.getenv("TE_PORT", "8096"))

TEMPLATES_DIR = SERVICE_ROOT / "presentation" / "templates"
STATIC_DIR = SERVICE_ROOT / "presentation" / "static"

ROOT_PATH = os.getenv("ROOT_PATH", "").rstrip("/")


def prefix_url(path: str) -> str:
    """Antepone ROOT_PATH a una ruta interna relativa a la aplicación si está configurado."""
    if not path.startswith("/"):
        path = f"/{path}"
    root = os.getenv("ROOT_PATH", ROOT_PATH).rstrip("/")
    if not root:
        return path
    if path == "/":
        return f"{root}/"
    return f"{root}{path}"


LINKING_SERVICE_INTERNAL_URL = os.getenv("LINKING_SERVICE_INTERNAL_URL", os.getenv("LINKING_SERVICE_URL", "http://localhost:8097"))
LINKING_SERVICE_URL = LINKING_SERVICE_INTERNAL_URL

STUDY_ASSISTANT_INTERNAL_URL = os.getenv("STUDY_ASSISTANT_INTERNAL_URL", os.getenv("STUDY_ASSISTANT_URL", "http://localhost:8095"))
STUDY_ASSISTANT_PUBLIC_URL = os.getenv("STUDY_ASSISTANT_PUBLIC_URL", os.getenv("STUDY_ASSISTANT_URL", "http://localhost:8095"))
STUDY_ASSISTANT_URL = STUDY_ASSISTANT_PUBLIC_URL

