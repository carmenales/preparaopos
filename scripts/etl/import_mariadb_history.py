#!/usr/bin/env python3
"""Migra a test-engine tu historial de práctica de preparadortai (MariaDB).

Entrada: los volcados exportados del contenedor de MariaDB (ver docs/MIGRACION.md):
- ``backups/mariadb/attempts.tsv``: test_attempts + enunciado de ptype.
- ``backups/mariadb/sessions.tsv``: test_sessions (solo conserva 3 de las 11 sesiones).

Cada intento se casa con su pregunta y su opción en test-engine:
- TAI: por el id de ``ptype`` (= ``questions.source_id`` de ``tai-mariadb-legacy``).
- Exámenes locales (Ayto. Madrid, Majadahonda, CM, UC3M): por el enunciado, dentro
  de esas fuentes.
- Opción: por el texto de la respuesta elegida. Además se comprueba que el
  acierto/fallo guardado coincide con la corrección de test-engine.
Si cualquier intento no casa de forma exacta y única, no se escribe nada.

Cada sesión de MariaDB se crea como sesión cerrada (``source = 'legacy'``,
modo práctica) con su mismo id, sus preguntas en el orden en que se respondieron,
inicio y fin según las fechas de los intentos, y la nota calculada con la regla del
examen (o la común de sus preguntas). Si la sesión era de un único cuestionario,
queda vinculada a su examen. Solo constan las preguntas respondidas: las que se
dejaron sin responder en preparadortai no se guardaban.

Por defecto es una simulación. Con --apply hace una copia verificada e inserta en
una transacción. Es idempotente: las sesiones ya migradas (mismo id) se omiten.

    docker compose stop test-engine
    python scripts/etl/import_mariadb_history.py            # simulación
    python scripts/etl/import_mariadb_history.py --apply
    docker compose start test-engine
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "services" / "test-engine"))

from backup_test_engine import DEFAULT_DB, DEFAULT_DIR, backup_database  # noqa: E402
from domain.scoring.models import ScoringRule  # noqa: E402
from domain.scoring.service import ScoringService  # noqa: E402

DEFAULT_ATTEMPTS = REPO_ROOT / "backups" / "mariadb" / "attempts.tsv"
DEFAULT_SESSIONS = REPO_ROOT / "backups" / "mariadb" / "sessions.tsv"
TAI_SOURCE = "tai-mariadb-legacy"
LOCAL_SOURCES = ("ayto-madrid-aux-tic", "ayto-majadahonda", "cm-madrid-digital", "uc3m-a2-gsi")
LOCAL_PREFIXES = ("AYTO MADRID", "AYTO MAJADAHONDA", "CM MADRID DIGITAL", "UC3M")
LEGACY_SOURCE = "legacy"

csv.field_size_limit(10**8)


def _unescape(value: str) -> str | None:
    """Valores de ``mariadb -B``: NULL literal y escapes \\n, \\t, \\0 y \\\\."""
    if value == "NULL":
        return None
    out, i = [], 0
    while i < len(value):
        ch = value[i]
        if ch == "\\" and i + 1 < len(value):
            out.append({"n": "\n", "t": "\t", "0": "\0", "\\": "\\"}.get(value[i + 1], value[i + 1]))
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _norm(text: str | None) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text or "")).strip().lower()


def read_tsv(path: Path) -> list[dict[str, str | None]]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [{k: _unescape(v) for k, v in row.items()}
                for row in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)]


@dataclass
class MappedAttempt:
    legacy_id: int
    session_id: str
    question_id: int
    option_id: int
    is_correct: bool
    answered_at: str
    categoria: str


@dataclass
class LegacySession:
    id: str
    title: str | None
    attempts: list[MappedAttempt] = field(default_factory=list)


def map_attempts(conn: sqlite3.Connection, attempts: list[dict]) -> tuple[list[MappedAttempt], list[str]]:
    tai = {sid: qid for qid, sid in conn.execute(
        "SELECT id, source_id FROM questions WHERE source = ?", (TAI_SOURCE,))}
    by_statement: dict[str, list[int]] = defaultdict(list)
    marks = ",".join("?" * len(LOCAL_SOURCES))
    for qid, statement in conn.execute(
            f"SELECT id, statement FROM questions WHERE source IN ({marks})", LOCAL_SOURCES):
        by_statement[_norm(statement)].append(qid)
    options: dict[int, dict[str, tuple[int, bool]]] = defaultdict(dict)
    for qid, oid, text, ok in conn.execute("SELECT question_id, id, option_text, is_correct FROM question_options"):
        options[qid][_norm(text)] = (oid, bool(ok))

    mapped, errors = [], []
    for a in attempts:
        ctx = f"intento {a['id']} ({a['categoria']})"
        if (a["categoria"] or "").upper().startswith(LOCAL_PREFIXES):
            candidates = by_statement.get(_norm(a["pregunta"]), [])
            if len(candidates) != 1:
                errors.append(f"{ctx}: enunciado {'ambiguo' if candidates else 'no encontrado'}")
                continue
            qid = candidates[0]
        else:
            qid = tai.get(str(a["question_id"]))
            if qid is None:
                errors.append(f"{ctx}: ptype {a['question_id']} no está en test-engine")
                continue
        option = options[qid].get(_norm(a["selected_answer"]))
        if option is None:
            errors.append(f"{ctx}: la respuesta elegida no es ninguna opción de la pregunta {qid}")
            continue
        if option[1] != (a["is_correct"] == "1"):
            errors.append(f"{ctx}: el acierto guardado no coincide con la corrección de test-engine")
            continue
        mapped.append(MappedAttempt(int(a["id"]), a["test_session_id"], qid, option[0], option[1],
                                    a["created_at"], a["categoria"]))
    return mapped, errors


def group_sessions(mapped: list[MappedAttempt], sessions: list[dict]) -> list[LegacySession]:
    titles = {s["id"]: s["title"] for s in sessions}
    grouped: dict[str, LegacySession] = {}
    for a in sorted(mapped, key=lambda a: a.legacy_id):
        grouped.setdefault(a.session_id, LegacySession(a.session_id, titles.get(a.session_id))).attempts.append(a)
    return list(grouped.values())


def _rules(conn: sqlite3.Connection) -> dict[int, ScoringRule]:
    return {
        rid: ScoringRule(id=rid, code=code, name=name, correct_score=Decimal(str(c)),
                         wrong_penalty=Decimal(str(w)), blank_score=Decimal(str(b)),
                         score_scale=Decimal(str(s)), min_score_zero=bool(z),
                         round_decimals=2, rounding_mode=ROUND_HALF_UP)
        for rid, code, name, c, w, b, s, z in conn.execute(
            "SELECT id, code, name, correct_score, wrong_penalty, blank_score, score_scale, min_score_zero "
            "FROM scoring_rules")
    }


def plan_session_rows(conn: sqlite3.Connection, sessions: list[LegacySession]) -> list[dict]:
    rules = _rules(conn)
    default_rule = next((rid for rid, r in rules.items() if r.code == "age-oficial-tercio"), None)
    scoring = ScoringService()
    rows = []
    for s in sessions:
        qids = [a.question_id for a in s.attempts]
        marks = ",".join("?" * len(qids))
        exams = conn.execute(
            f"SELECT DISTINCT e.id, e.scoring_rule_id FROM exam_questions eq JOIN exams e ON e.id = eq.exam_id "
            f"WHERE eq.question_id IN ({marks})", qids).fetchall()
        exam_id = exams[0][0] if len(exams) == 1 else None
        rule_ids = {r for _, r in exams if r is not None}
        rule_id = rule_ids.pop() if len(rule_ids) == 1 else default_rule
        correct = sum(a.is_correct for a in s.attempts)
        score = scoring.score_scaled(correct=correct, wrong=len(qids) - correct, blank=0,
                                     total_questions=len(qids), rule=rules[rule_id]) if rule_id else None
        categorias = Counter(a.categoria for a in s.attempts)
        label = s.title or categorias.most_common(1)[0][0]
        rows.append({
            "id": s.id,
            "source_ref": f"preparadortai: {label}"[:128],
            "question_ids": json.dumps(qids),
            "started_at": min(a.answered_at for a in s.attempts),
            "closed_at": max(a.answered_at for a in s.attempts),
            "scoring_rule_id": rule_id,
            "exam_id": exam_id,
            "final_score": str(score) if score is not None else None,
            "attempts": s.attempts,
            "correct": correct,
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Migra el historial de preparadortai a test-engine.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--attempts", type=Path, default=DEFAULT_ATTEMPTS)
    parser.add_argument("--sessions", type=Path, default=DEFAULT_SESSIONS)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--apply", action="store_true", help="Escribir en la BD (por defecto, simulación)")
    args = parser.parse_args()

    for path in (args.db, args.attempts, args.sessions):
        if not path.exists():
            print(f"ERROR: no existe {path}", file=sys.stderr)
            return 1

    attempts = read_tsv(args.attempts)
    conn = sqlite3.connect(args.db, timeout=5)
    try:
        mapped, errors = map_attempts(conn, attempts)
        sessions = group_sessions(mapped, read_tsv(args.sessions))
        existing = {r[0] for r in conn.execute("SELECT id FROM test_sessions WHERE source = ?", (LEGACY_SOURCE,))}
        rows = [r for r in plan_session_rows(conn, sessions) if r["id"] not in existing]
    finally:
        conn.close()

    print(f"Intentos leídos: {len(attempts)} · casados: {len(mapped)} · sin casar: {len(errors)}")
    for r in sorted(rows, key=lambda r: r["started_at"]):
        print(f"  {r['started_at'][:16]}  {len(r['attempts']):>3} preguntas  {r['correct']:>3} aciertos  "
              f"nota {r['final_score']}  {r['source_ref']}")
    if existing:
        print(f"Sesiones ya migradas (se omiten): {len(existing)}")
    if errors:
        print("ERROR: no se escribe nada:\n  " + "\n  ".join(errors[:20]), file=sys.stderr)
        return 1
    if not args.apply:
        print("\nSimulación: no se ha escrito nada. Repite con --apply.")
        return 0
    if not rows:
        print("Nada que migrar.")
        return 0

    try:
        backup = backup_database(args.db, args.backup_dir, label="antes-de-historial-mariadb")
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
        for r in rows:
            conn.execute(
                "INSERT INTO test_sessions (id, started_at, duration_seconds, finished_at, mode, status, "
                "scoring_rule_id, exam_id, source, source_ref, question_ids, closed_at, final_score) "
                "VALUES (?, ?, NULL, ?, 'practice', 'closed', ?, ?, ?, ?, ?, ?, ?)",
                (r["id"], r["started_at"], r["closed_at"], r["scoring_rule_id"], r["exam_id"], LEGACY_SOURCE,
                 r["source_ref"], r["question_ids"], r["closed_at"], r["final_score"]),
            )
            conn.executemany(
                "INSERT INTO test_attempts (test_session_id, question_id, selected_option_id, is_correct, answered_at) "
                "VALUES (?, ?, ?, ?, ?)",
                [(r["id"], a.question_id, a.option_id, int(a.is_correct), a.answered_at) for a in r["attempts"]],
            )
        conn.commit()
        n_sessions, n_attempts = conn.execute(
            "SELECT COUNT(DISTINCT s.id), COUNT(a.id) FROM test_sessions s "
            "JOIN test_attempts a ON a.test_session_id = s.id WHERE s.source = ?", (LEGACY_SOURCE,)).fetchone()
    finally:
        conn.close()
    print(f"[ok] Historial migrado: {n_sessions} sesiones y {n_attempts} intentos con source = '{LEGACY_SOURCE}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
