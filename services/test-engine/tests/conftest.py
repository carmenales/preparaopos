"""Aísla la base de datos de los tests de la BD real del servicio.

``config.SQLITE_PATH`` se resuelve al importar ``config``, y ``presentation.app``
crea su engine al importarse. Por eso la copia y la variable de entorno se
preparan aquí, a nivel de módulo: pytest carga este conftest antes de importar
cualquier módulo de test.
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

SERVICE_ROOT = Path(__file__).resolve().parent.parent
REAL_DB = SERVICE_ROOT / "data" / "test_engine.sqlite"

if "config" in sys.modules:
    raise RuntimeError(
        "config se importó antes de tests/conftest.py: los tests usarían la BD real."
    )

_TMP_DIR = Path(tempfile.mkdtemp(prefix="test_engine_"))
TEST_DB = _TMP_DIR / "test_engine.sqlite"

if REAL_DB.exists():
    # Se copian también los ficheros auxiliares: si hay un journal/WAL pendiente,
    # SQLite lo resuelve sobre la copia y la BD real no se abre nunca.
    for suffix in ("", "-journal", "-wal", "-shm"):
        src = REAL_DB.with_name(REAL_DB.name + suffix)
        if src.exists():
            shutil.copy2(src, TEST_DB.with_name(TEST_DB.name + suffix))

os.environ["TEST_ENGINE_SQLITE_PATH"] = str(TEST_DB)


@pytest.fixture(scope="session", autouse=True)
def _guard_real_database():
    import config

    assert config.SQLITE_PATH.resolve() != REAL_DB.resolve(), (
        "Los tests apuntan a la BD real del servicio."
    )
    yield


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree(_TMP_DIR, ignore_errors=True)
