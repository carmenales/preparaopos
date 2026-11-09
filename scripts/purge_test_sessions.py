#!/usr/bin/env python3
"""Elimina sesiones de test (y sus intentos) de la BD de test-engine.

Por defecto solo selecciona las sesiones que dejó scripts/smoke_gateway.py antes de que
limpiara lo que crea: un simulacro del examen 53 con como mucho una respuesta y, en los
10 s siguientes, una práctica sin respuestas del apunte tema-i-01-derecho-constitucional.
Con --all selecciona todas las sesiones, incluido el historial importado de preparadortai.

No toca preguntas, opciones, exámenes, temarios ni reglas de puntuación.
Por defecto solo muestra lo que borraría; con --apply hace antes una copia de
seguridad verificada (scripts/backup_test_engine.py) y borra en una transacción.

Para el uso normal, detén antes el contenedor para que no haya escrituras a la vez:
    docker compose stop test-engine

Uso:
    python scripts/purge_test_sessions.py                         # simulación, sesiones del smoke test
    python scripts/purge_test_sessions.py --apply                 # borra las sesiones del smoke test
    python scripts/purge_test_sessions.py --all --before 2026-10-20   # simulación, todas las anteriores
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_test_engine import DEFAULT_DB, DEFAULT_DIR, backup_database  # noqa: E402


SMOKE_EXAM_REF = "53"
SMOKE_NOTE_REF = "tema-i-01-derecho-constitucional"
SMOKE_PAIR_SECONDS = 10

# Simulacro del smoke test: examen 53, como mucho una respuesta y su práctica por apunte justo después.
_SMOKE_EXAMS = f"""
    SELECT e.id FROM test_sessions e
    WHERE e.mode = 'exam' AND e.source = 'exam' AND e.source_ref = '{SMOKE_EXAM_REF}'
      AND (SELECT COUNT(*) FROM test_attempts a WHERE a.test_session_id = e.id) <= 1
      AND EXISTS (SELECT 1 FROM test_sessions n
                  WHERE n.mode = 'practice' AND n.source = 'note' AND n.source_ref = '{SMOKE_NOTE_REF}'
                    AND (julianday(n.started_at) - julianday(e.started_at)) * 86400 BETWEEN 0 AND {SMOKE_PAIR_SECONDS})
"""
# Práctica por apunte del smoke test: sin respuestas y justo después de uno de esos simulacros.
_SMOKE_NOTES = f"""
    SELECT n.id FROM test_sessions n
    WHERE n.mode = 'practice' AND n.source = 'note' AND n.source_ref = '{SMOKE_NOTE_REF}'
      AND NOT EXISTS (SELECT 1 FROM test_attempts a WHERE a.test_session_id = n.id)
      AND EXISTS (SELECT 1 FROM test_sessions e WHERE e.id IN ({_SMOKE_EXAMS})
                    AND (julianday(n.started_at) - julianday(e.started_at)) * 86400 BETWEEN 0 AND {SMOKE_PAIR_SECONDS})
"""


def build_filter(before: str | None, all_sessions: bool = False) -> tuple[str, tuple]:
    conditions, params = [], ()
    if not all_sessions:
        conditions.append(f"(id IN ({_SMOKE_EXAMS}) OR id IN ({_SMOKE_NOTES}))")
    if before:
        conditions.append("started_at < ?")
        params = (before,)
    return ("WHERE " + " AND ".join(conditions)) if conditions else "", params


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
    parser.add_argument("--all", action="store_true",
                        help="Todas las sesiones, no solo las del smoke test (incluye el historial importado)")
    parser.add_argument("--before", help="Solo sesiones iniciadas antes de esta fecha (AAAA-MM-DD)")
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_DIR, help="Carpeta de la copia previa")
    parser.add_argument("--apply", action="store_true", help="Borrar de verdad (por defecto, simulación)")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"ERROR: no existe la BD: {args.db}", file=sys.stderr)
        return 1

    where, params = build_filter(args.before, all_sessions=args.all)
    print("Selección:", "TODAS las sesiones" if args.all else "sesiones creadas por el smoke test")
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
        # Fijar los ids antes de borrar: la selección del smoke test empareja simulacro y práctica,
        # y si se evaluara durante el DELETE la práctica dejaría de emparejar al borrarse su simulacro.
        conn.execute(f"CREATE TEMP TABLE purge_ids AS SELECT id FROM test_sessions {where}", params)
        conn.execute("DELETE FROM test_attempts WHERE test_session_id IN (SELECT id FROM purge_ids)")
        conn.execute("DELETE FROM test_sessions WHERE id IN (SELECT id FROM purge_ids)")
        conn.commit()
        conn.execute("DROP TABLE purge_ids")
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
