#!/usr/bin/env python3
"""Elimina sesiones de test (y sus intentos) de la BD de test-engine.

No toca preguntas, opciones, exámenes, temarios ni reglas de puntuación.
Por defecto solo muestra lo que borraría; con --apply hace antes una copia de
seguridad verificada (scripts/backup_test_engine.py) y borra en una transacción.

Para el uso normal, detén antes el contenedor para que no haya escrituras a la vez:
    docker compose stop test-engine

Uso:
    python scripts/purge_test_sessions.py                         # simulación, todas
    python scripts/purge_test_sessions.py --before 2026-10-20     # simulación, anteriores a esa fecha
    python scripts/purge_test_sessions.py --apply
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_test_engine import DEFAULT_DB, DEFAULT_DIR, backup_database  # noqa: E402


def build_filter(before: str | None) -> tuple[str, tuple]:
    if before:
        return "WHERE started_at < ?", (before,)
    return "", ()


def summarize(conn: sqlite3.Connection, where: str, params: tuple) -> tuple[int, int]:
    sessions = conn.execute(f"SELECT COUNT(*) FROM test_sessions {where}", params).fetchone()[0]
    attempts = conn.execute(
        f"SELECT COUNT(*) FROM test_attempts WHERE test_session_id IN (SELECT id FROM test_sessions {where})",
        params,
    ).fetchone()[0]
    print(f"Sesiones a borrar: {sessions} · intentos a borrar: {attempts}")
    for day, source, n in conn.execute(
        f"SELECT substr(started_at, 1, 10), source, COUNT(*) FROM test_sessions {where} "
        "GROUP BY 1, 2 ORDER BY 1, 2",
        params,
    ):
        print(f"  {day}  {source:<10} {n}")
    return sessions, attempts


def main() -> int:
    parser = argparse.ArgumentParser(description="Purga sesiones de test de test-engine.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--before", help="Solo sesiones iniciadas antes de esta fecha (AAAA-MM-DD)")
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_DIR, help="Carpeta de la copia previa")
    parser.add_argument("--apply", action="store_true", help="Borrar de verdad (por defecto, simulación)")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"ERROR: no existe la BD: {args.db}", file=sys.stderr)
        return 1

    where, params = build_filter(args.before)
    conn = sqlite3.connect(args.db, timeout=5)
    try:
        sessions, _ = summarize(conn, where, params)
        if not args.apply:
            print("\nSimulación: no se ha borrado nada. Repite con --apply para borrar.")
            return 0
        if sessions == 0:
            print("Nada que borrar.")
            return 0

        conn.close()
        try:
            backup = backup_database(args.db, args.backup_dir, label="antes-de-purga")
        except Exception as exc:
            print(f"ERROR: no se pudo hacer la copia previa; no se borra nada ({exc})", file=sys.stderr)
            return 1
        print(f"[ok] Copia previa: {backup}")

        conn = sqlite3.connect(args.db, timeout=5)
        try:
            conn.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as exc:
            print(f"ERROR: la BD está en uso ({exc}). Ejecuta: docker compose stop test-engine", file=sys.stderr)
            return 1
        conn.execute(
            f"DELETE FROM test_attempts WHERE test_session_id IN (SELECT id FROM test_sessions {where})",
            params,
        )
        conn.execute(f"DELETE FROM test_sessions {where}", params)
        conn.commit()
        conn.execute("VACUUM")

        left_s = conn.execute("SELECT COUNT(*) FROM test_sessions").fetchone()[0]
        left_a = conn.execute("SELECT COUNT(*) FROM test_attempts").fetchone()[0]
        questions = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        print(f"[ok] Purga hecha. Quedan {left_s} sesiones, {left_a} intentos y {questions} preguntas.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
