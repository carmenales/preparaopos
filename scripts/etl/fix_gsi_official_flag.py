#!/usr/bin/env python3
"""Marca las preguntas de GSI 2024 como de examen oficial del año 2024.

El importador las guardaba con ``is_official_exam = 0`` y sin año, así que no salían en
«solo preguntas de examen oficial» (generador), «Mostrar exclusivamente» (Filtrar) ni en las
estadísticas de oficiales. Solo toca ``questions.year`` e ``is_official_exam`` de las preguntas
con ``source = 'age-gsi-2024'``; no cambia ids, opciones ni intentos. El importador ya las crea así.

Por defecto es una simulación. Con --apply hace una copia verificada. Idempotente.

    docker compose stop test-engine
    python scripts/etl/fix_gsi_official_flag.py            # simulación
    python scripts/etl/fix_gsi_official_flag.py --apply
    docker compose start test-engine
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from import_age_gsi_2024 import EXAM_YEAR, SOURCE_NAME  # noqa: E402
from backup_test_engine import DEFAULT_DB, DEFAULT_DIR, backup_database  # noqa: E402


def pending(conn: sqlite3.Connection) -> list[int]:
    """Ids de las preguntas de GSI 2024 que aún no tienen el año o la marca de examen oficial."""
    rows = conn.execute(
        "SELECT id FROM questions WHERE source = ? AND (year IS NOT ? OR is_official_exam IS NOT 1) ORDER BY id",
        (SOURCE_NAME, EXAM_YEAR)).fetchall()
    return [r[0] for r in rows]


def main() -> int:
    parser = argparse.ArgumentParser(description="Marca GSI 2024 como examen oficial de 2024.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--apply", action="store_true", help="Escribir en la BD (por defecto, simulación)")
    args = parser.parse_args()
    if not args.db.exists():
        print(f"ERROR: no existe {args.db}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(args.db, timeout=5)
    try:
        ids = pending(conn)
    finally:
        conn.close()
    print(f"Preguntas de GSI 2024 sin año {EXAM_YEAR} o sin marca de examen oficial: {len(ids)}")
    if not args.apply:
        print("Simulación: no se ha escrito nada. Repite con --apply.")
        return 0
    if not ids:
        print("Nada que hacer.")
        return 0

    try:
        backup = backup_database(args.db, args.backup_dir, label="antes-de-marcar-gsi-oficial")
    except Exception as exc:
        print(f"ERROR: no se pudo hacer la copia previa; no se escribe nada ({exc})", file=sys.stderr)
        return 1
    print(f"[ok] Copia previa: {backup}")
    conn = sqlite3.connect(args.db, timeout=5)
    try:
        try:
            conn.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as exc:
            print(f"ERROR: la BD está en uso ({exc}). Ejecuta: docker compose stop test-engine", file=sys.stderr)
            return 1
        conn.execute("UPDATE questions SET year = ?, is_official_exam = 1 WHERE source = ?", (EXAM_YEAR, SOURCE_NAME))
        conn.commit()
        left = pending(conn)
    finally:
        conn.close()
    if left:
        print(f"ERROR: quedan {len(left)} preguntas sin marcar.", file=sys.stderr)
        return 1
    print(f"[ok] Marcadas {len(ids)} preguntas como examen oficial de {EXAM_YEAR}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
