"""Configuración del servicio Linking Service."""

import os
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_ROOT.parent.parent

SQLITE_PATH = Path(
    os.getenv(
        "LINKING_SQLITE_PATH",
        str(SERVICE_ROOT / "data" / "linking.sqlite"),
    )
)

APUNTES_SERVICE_INTERNAL_URL = os.getenv("APUNTES_SERVICE_INTERNAL_URL", os.getenv("APUNTES_SERVICE_URL", "http://127.0.0.1:8095"))
APUNTES_SERVICE_URL = APUNTES_SERVICE_INTERNAL_URL

TEST_ENGINE_INTERNAL_URL = os.getenv("TEST_ENGINE_INTERNAL_URL", os.getenv("TEST_ENGINE_URL", "http://127.0.0.1:8096"))
TEST_ENGINE_URL = TEST_ENGINE_INTERNAL_URL

HOST = os.getenv("LS_HOST", "0.0.0.0")
PORT = int(os.getenv("LS_PORT", "8097"))

# Mapeo oficial de temarios a slugs de proceso de apuntes
SYLLABUS_TO_PROCESS_MAP = {
    "age-gsi-official": "age/a2-gsi",
}
