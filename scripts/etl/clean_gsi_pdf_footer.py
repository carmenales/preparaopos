#!/usr/bin/env python3
"""Quita el pie de página del PDF («2024 - GSI-L  Página N de 10») de las opciones de GSI 2024.

La extracción del PDF oficial dejó ese pie pegado al final de la última opción de
cada página (9 opciones). Solo modifica ``question_options.option_text`` de las
preguntas con ``source = 'age-gsi-2024'``; no toca ids, correctas ni intentos.
Los ficheros originales de imports/ no se modifican: el importador ya limpia el
texto al importar.

Por defecto es una simulación. Con --apply hace una copia verificada. Idempotente.

    docker compose stop test-engine
    python scripts/etl/clean_gsi_pdf_footer.py            # simulación
    python scripts/etl/clean_gsi_pdf_footer.py --apply
    docker compose start test-engine
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from import_age_gsi_2024 import PDF_FOOTER_RE, SOURCE_NAME, strip_pdf_footer  # noqa: E402
from backup_test_engine import DEFAULT_DB, DEFAULT_DIR, backup_database  # noqa: E402


def affected(conn: sqlite3.Connection) -> list[tuple[int, str, str]]:
    rows = conn.execute(
        "SELECT o.id, o.option_text FROM question_options o JOIN questions q ON q.id = o.question_id "
        "WHERE q.source = ?", (SOURCE_NAME,)).fetchall()
    return [(oid, text, strip_pdf_footer(text)) for oid, text in rows if PDF_FOOTER_RE.search(text or "")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Limpia el pie de página del PDF en opciones de GSI 2024.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--apply", action="store_true", help="Escribir en la BD (por defecto, simulación)")
    args = parser.parse_args()
    if not args.db.exists():
        print(f"ERROR: no existe {args.db}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(args.db, timeout=5)
    try:
        rows = affected(conn)
    finally:
        conn.close()
    print(f"Opciones con pie de página: {len(rows)}")
    for oid, before, after in rows:
        print(f"  {oid}: …{before[-55:]!r} → …{after[-35:]!r}")
    if not args.apply:
        print("Simulación: no se ha escrito nada. Repite con --apply.")
        return 0
    if not rows:
        print("Nada que hacer.")
        return 0

    try:
        backup = backup_database(args.db, args.backup_dir, label="antes-de-limpiar-pie-gsi")
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
        conn.executemany("UPDATE question_options SET option_text = ? WHERE id = ?",
                         [(after, oid) for oid, _, after in rows])
        conn.commit()
        left = affected(conn)
    finally:
        conn.close()
    if left:
        print(f"ERROR: quedan {len(left)} opciones con pie de página.", file=sys.stderr)
        return 1
    print(f"[ok] Limpiadas {len(rows)} opciones.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
