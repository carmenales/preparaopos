#!/usr/bin/env python3
"""Añade la etiqueta de temario que les falta a las preguntas de TAI sin bloque ni tema.

``import_tai_mariadb.py`` solo etiquetaba las preguntas con bloque o tema, y el
generador de test-engine busca las preguntas de un temario por su etiqueta: las
1.147 restantes no aparecían ni en «todo el temario» ni en el refuerzo. Este script
les añade la etiqueta ``tai-legacy`` con bloque y tema vacíos, como hacen ya el
importador corregido y el resto de fuentes. No modifica ninguna etiqueta existente.

Por defecto es una simulación. Con --apply hace una copia verificada. Idempotente.

    docker compose stop test-engine
    python scripts/etl/fix_tai_syllabus_tags.py            # simulación
    python scripts/etl/fix_tai_syllabus_tags.py --apply
    docker compose start test-engine
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from backup_test_engine import DEFAULT_DB, DEFAULT_DIR, backup_database  # noqa: E402

SOURCE = "tai-mariadb-legacy"
SYLLABUS_ID = "tai-legacy"
UNTAGGED_SQL = (
    "SELECT q.id FROM questions q WHERE q.source = ? AND NOT EXISTS "
    "(SELECT 1 FROM question_syllabus_tags t WHERE t.question_id = q.id AND t.syllabus_id = ?) ORDER BY q.id"
)


def untagged(conn: sqlite3.Connection) -> list[int]:
    return [r[0] for r in conn.execute(UNTAGGED_SQL, (SOURCE, SYLLABUS_ID))]


def main() -> int:
    parser = argparse.ArgumentParser(description="Etiqueta de temario para las preguntas de TAI sin bloque ni tema.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--apply", action="store_true", help="Escribir en la BD (por defecto, simulación)")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"ERROR: no existe {args.db}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(args.db, timeout=5)
    try:
        missing = untagged(conn)
        total = conn.execute("SELECT COUNT(*) FROM questions WHERE source = ?", (SOURCE,)).fetchone()[0]
    finally:
        conn.close()
    print(f"Preguntas de TAI: {total} · sin etiqueta de temario: {len(missing)}")

    if not args.apply:
        print("Simulación: no se ha escrito nada. Repite con --apply.")
        return 0
    if not missing:
        print("Nada que hacer.")
        return 0

    try:
        backup = backup_database(args.db, args.backup_dir, label="antes-de-fix-tai-tags")
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
        conn.executemany(
            "INSERT INTO question_syllabus_tags (question_id, syllabus_id, block, topic) VALUES (?, ?, NULL, NULL)",
            [(qid, SYLLABUS_ID) for qid in missing],
        )
        conn.commit()
        left = untagged(conn)
    finally:
        conn.close()
    if left:
        print(f"ERROR: quedan {len(left)} preguntas sin etiqueta.", file=sys.stderr)
        return 1
    print(f"[ok] Etiquetadas {len(missing)} preguntas; todas las de TAI tienen ya etiqueta de temario.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
