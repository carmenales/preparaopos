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
