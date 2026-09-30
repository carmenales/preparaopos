"""Crea (si no existe) el esquema SQLite y las filas maestras de syllabi.

Uso:
    cd services/test-engine
    python -m infrastructure.db.create_schema
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[2]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from config import SQLITE_PATH
from infrastructure.db.engine import create_sqlite_engine, init_schema, wal_mode

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("test-engine.schema")


def main() -> None:
    logger.info("Creando esquema en %s", SQLITE_PATH)
    engine = create_sqlite_engine(SQLITE_PATH)
    init_schema(engine)
    logger.info("journal_mode=%s", wal_mode(engine))
    logger.info("Esquema listo.")


if __name__ == "__main__":
    main()
