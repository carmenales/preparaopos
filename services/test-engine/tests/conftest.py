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


# Sin la BD real (no está en git: CI o un clon limpio) se saltan los tests que la usan: los que
# piden alguno de estos fixtures (también de forma indirecta) o llevan @pytest.mark.real_db.
# Los demás se ejecutan igual.
DB_FIXTURES = {"client", "db", "db_session", "session_service", "svc"}
NO_REAL_DB = "Necesita la BD real de test-engine (data/test_engine.sqlite, no versionada)"


def pytest_configure(config):
    config.addinivalue_line("markers", "real_db: el test necesita la BD real de test-engine")


def pytest_collection_modifyitems(config, items):
    if REAL_DB.exists():
        return
    skip = pytest.mark.skip(reason=NO_REAL_DB)
    for item in items:
        if DB_FIXTURES & set(getattr(item, "fixturenames", ())) or item.get_closest_marker("real_db"):
            item.add_marker(skip)


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree(_TMP_DIR, ignore_errors=True)
