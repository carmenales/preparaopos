#!/usr/bin/env python3
"""Rellena ``questions.year`` y ``questions.is_official_exam`` de las preguntas de PreparaTIC.

La importación original (import_preparatic.py) descartó estos dos campos, aunque
el extractor sí los dejó en ``preparatic_bundle_extracted.json``. Este script los
recupera cruzando por ``source`` + ``source_id``.

Solo modifica esas dos columnas y solo en filas con source = PreparaTIC. No toca
ids, enunciados, opciones, etiquetas de temario ni sesiones.

Por defecto es una simulación. Con --apply:
  1. añade las columnas si faltan (igual que hace test-engine al arrancar),
  2. hace una copia verificada en backups/test-engine/,
  3. actualiza en una transacción y verifica el resultado.

Detén antes el servicio para que no haya escrituras a la vez:
    docker compose stop test-engine
    python scripts/etl/backfill_preparatic_metadata.py            # simulación
    python scripts/etl/backfill_preparatic_metadata.py --apply
    docker compose start test-engine
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from import_preparatic import SOURCE_NAME, parse_question_metadata  # noqa: E402
from backup_test_engine import DEFAULT_DB, DEFAULT_DIR, backup_database  # noqa: E402

DEFAULT_BUNDLE = REPO_ROOT / "scripts" / "etl" / "preparatic_bundle_extracted.json"
METADATA_COLUMNS = {"year": "INTEGER", "is_official_exam": "BOOLEAN NOT NULL DEFAULT 0"}


def load_bundle_metadata(bundle_path: Path) -> dict[str, tuple[int | None, bool]]:
    with open(bundle_path, encoding="utf-8") as f:
        questions = json.load(f)
    return {str(q["id"]).strip(): parse_question_metadata(q) for q in questions}


def ensure_columns(conn: sqlite3.Connection) -> list[str]:
    existing = {row[1] for row in conn.execute("PRAGMA table_info(questions)")}
    added = []
    for name, ddl in METADATA_COLUMNS.items():
        if name not in existing:
            conn.execute(f"ALTER TABLE questions ADD COLUMN {name} {ddl}")
            added.append(name)
    conn.commit()
    return added


def missing_columns(conn: sqlite3.Connection) -> list[str]:
    existing = {row[1] for row in conn.execute("PRAGMA table_info(questions)")}
    return [name for name in METADATA_COLUMNS if name not in existing]


def plan_updates(
    conn: sqlite3.Connection, bundle: dict[str, tuple[int | None, bool]], has_columns: bool
) -> dict:
    select_current = "year, is_official_exam" if has_columns else "NULL, 0"
    rows = conn.execute(
        f"SELECT id, source_id, {select_current} FROM questions WHERE source = ?",
        (SOURCE_NAME,),
    ).fetchall()

    updates: list[tuple[int | None, int, int]] = []
    not_in_bundle: list[str] = []
    for qid, source_id, cur_year, cur_exam in rows:
        meta = bundle.get(str(source_id))
        if meta is None:
            not_in_bundle.append(source_id)
            continue
        year, is_exam = meta
        if cur_year != year or bool(cur_exam) != is_exam:
            updates.append((year, int(is_exam), qid))

    db_ids = {str(r[1]) for r in rows}
    return {
        "db_rows": len(rows),
        "updates": updates,
        "not_in_bundle": not_in_bundle,
        "bundle_not_in_db": sorted(set(bundle) - db_ids),
        "years": Counter(m[0] for sid, m in bundle.items() if sid in db_ids),
        "official": sum(1 for sid, m in bundle.items() if sid in db_ids and m[1]),
    }


def print_plan(plan: dict) -> None:
    print(f"Preguntas PreparaTIC en BD: {plan['db_rows']}")
    print(f"Filas a actualizar: {len(plan['updates'])}")
    print(f"Marcadas como examen oficial: {plan['official']}")
    print(f"En BD pero no en el bundle: {len(plan['not_in_bundle'])}")
    print(f"En el bundle pero no en BD: {len(plan['bundle_not_in_db'])}")
    print("Por año:")
    for year, n in sorted(plan["years"].items(), key=lambda kv: (kv[0] is None, kv[0] or 0)):
        print(f"  {year if year is not None else 'sin año'}: {n}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Recupera año y marca de examen oficial de PreparaTIC.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--apply", action="store_true", help="Escribir en la BD (por defecto, simulación)")
    args = parser.parse_args()

    for path in (args.db, args.bundle):
        if not path.exists():
            print(f"ERROR: no existe {path}", file=sys.stderr)
            return 1

    bundle = load_bundle_metadata(args.bundle)
    conn = sqlite3.connect(args.db, timeout=5)
    try:
        has_columns = not missing_columns(conn)
        plan = plan_updates(conn, bundle, has_columns)
        print_plan(plan)

        if plan["not_in_bundle"]:
            print(
                f"ERROR: {len(plan['not_in_bundle'])} preguntas de la BD no están en el bundle "
                f"(p. ej. {plan['not_in_bundle'][:5]}). No se escribe nada.",
                file=sys.stderr,
            )
            return 1
        if not args.apply:
            print("\nSimulación: no se ha escrito nada. Repite con --apply.")
            return 0
        if not plan["updates"] and has_columns:
            print("Nada que actualizar.")
            return 0

        conn.close()
        try:
            backup = backup_database(args.db, args.backup_dir, label="antes-de-backfill-preparatic")
        except Exception as exc:
            print(f"ERROR: no se pudo hacer la copia previa; no se escribe nada ({exc})", file=sys.stderr)
            return 1
        print(f"[ok] Copia previa: {backup}")

        conn = sqlite3.connect(args.db, timeout=5)
        added = ensure_columns(conn)
        if added:
            print(f"[ok] Columnas añadidas: {', '.join(added)}")
        try:
            conn.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as exc:
            print(f"ERROR: la BD está en uso ({exc}). Ejecuta: docker compose stop test-engine", file=sys.stderr)
            return 1
        conn.executemany(
            "UPDATE questions SET year = ?, is_official_exam = ? WHERE id = ? AND source = ?",
            [(year, exam, qid, SOURCE_NAME) for year, exam, qid in plan["updates"]],
        )
        conn.commit()

        after = plan_updates(conn, bundle, has_columns=True)
        if after["updates"]:
            print(f"ERROR: quedan {len(after['updates'])} filas sin cuadrar tras actualizar.", file=sys.stderr)
            return 1
        print(f"[ok] Actualizadas {len(plan['updates'])} preguntas; la BD coincide con el bundle.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
