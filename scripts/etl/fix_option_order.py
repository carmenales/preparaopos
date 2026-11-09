#!/usr/bin/env python3
"""Corrige ``display_order`` en las preguntas con la opción correcta siempre en primera posición.

Afecta solo a dos fuentes, importadas con la correcta en ``display_order = 0``:
- ``age-gsi-2024`` (101): se restaura el orden oficial A-D. La letra sale de las
  justificaciones guardadas y se verifica contra el JSON del examen
  (``imports/age_a2_gsi/data/examen_..._2024.json``); si alguna no coincide, no se escribe nada.
- ``tai-mariadb-legacy`` (1.331): el orden original no existe en ninguna fuente; se
  baraja de forma determinista por pregunta (``option_order.stable_positions``).

Solo cambia ``question_options.display_order``. No toca textos, ids, respuestas
correctas ni intentos: los intentos guardan el id de la opción, no su posición.

Por defecto es una simulación. Con --apply hace una copia verificada y actualiza en
una transacción. Es idempotente.

    docker compose stop test-engine
    python scripts/etl/fix_option_order.py            # simulación
    python scripts/etl/fix_option_order.py --apply
    docker compose start test-engine
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from option_order import LETTERS, letter_hint, official_positions, stable_positions  # noqa: E402
from backup_test_engine import DEFAULT_DB, DEFAULT_DIR, backup_database  # noqa: E402

GSI_SOURCE = "age-gsi-2024"
TAI_SOURCE = "tai-mariadb-legacy"
GSI_JSON = REPO_ROOT / "imports/age_a2_gsi/data/examen_Gestion_de_Sistemas_e_Informatica_Libre_AGE_2024.json"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


def _load_questions(conn: sqlite3.Connection, source: str) -> list[dict]:
    questions = []
    for qid, source_id, justification in conn.execute(
        "SELECT id, source_id, justification FROM questions WHERE source = ? ORDER BY id", (source,)
    ):
        options = conn.execute(
            "SELECT id, option_text, is_correct, display_order, justification FROM question_options "
            "WHERE question_id = ? ORDER BY id",
            (qid,),
        ).fetchall()
        correct = [o for o in options if o[2]]
        if len(correct) != 1:
            raise ValueError(f"{source} {source_id}: {len(correct)} opciones correctas")
        # Orden canónico de las incorrectas: el de importación (id), que no cambia al
        # reordenar; así la permutación es la misma en cada ejecución (idempotente).
        wrongs = [o for o in options if not o[2]]
        questions.append({"id": qid, "source_id": source_id, "justification": justification,
                          "options": [correct[0], *wrongs]})
    return questions


def _gsi_json_letters(conn: sqlite3.Connection, json_path: Path) -> dict[int, dict[str, str]]:
    """{question_id: {texto normalizado: letra}} según el JSON oficial, por posición en el examen."""
    official = {q["numero"]: q for q in json.loads(json_path.read_text(encoding="utf-8"))["preguntas"]}
    result = {}
    for qid, position in conn.execute(
        "SELECT q.id, eq.position FROM questions q JOIN exam_questions eq ON eq.question_id = q.id "
        "WHERE q.source = ?", (GSI_SOURCE,)
    ):
        entry = official.get(position)
        if entry:
            result[qid] = {"options": {_norm(v): k.upper() for k, v in entry["opciones"].items()},
                           "correct": entry["respuesta_correcta"].upper()}
    return result


def _json_letter(option_text: str, mapping: dict[str, str]) -> str | None:
    text = _norm(option_text)
    if text in mapping:
        return mapping[text]
    # El JSON arrastra ruido de pie de página al final de algunas opciones.
    matches = {letter for value, letter in mapping.items() if value.startswith(text) or text.startswith(value)}
    return matches.pop() if len(matches) == 1 else None


def plan(conn: sqlite3.Connection, gsi_json: Path) -> tuple[list[tuple[int, int]], dict]:
    updates: list[tuple[int, int]] = []
    report: dict = {"errors": [], "before": {}, "after": {}, "hints": 0}

    json_letters = _gsi_json_letters(conn, gsi_json)
    for source in (GSI_SOURCE, TAI_SOURCE):
        before, after = Counter(), Counter()
        for q in _load_questions(conn, source):
            options = q["options"]
            before[LETTERS[options[0][3]] if options[0][3] < len(LETTERS) else "?"] += 1
            if source == GSI_SOURCE:
                positions = official_positions(q["justification"], [o[4] for o in options[1:]])
                if positions is None:
                    report["errors"].append(f"{source} {q['source_id']}: justificaciones sin letras completas")
                    continue
                ref = json_letters.get(q["id"])
                json_letters_q = [_json_letter(o[1], ref["options"]) for o in options] if ref else []
                json_pos = [LETTERS.index(letter) if letter else None for letter in json_letters_q]
                if ref is None or json_pos != positions or LETTERS[positions[0]] != ref["correct"]:
                    report["errors"].append(f"{source} {q['source_id']}: el orden no coincide con el JSON oficial")
                    continue
            else:
                hint = letter_hint(q["justification"], len(options))
                report["hints"] += hint is not None
                positions = stable_positions(f"{source}:{q['source_id']}", len(options), hint)
            after[LETTERS[positions[0]]] += 1
            for option, position in zip(options, positions):
                if option[3] != position:
                    updates.append((position, option[0]))
        report["before"][source] = dict(sorted(before.items()))
        report["after"][source] = dict(sorted(after.items()))
    return updates, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Corrige el orden de opciones de GSI 2024 y TAI.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--gsi-json", type=Path, default=GSI_JSON)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--apply", action="store_true", help="Escribir en la BD (por defecto, simulación)")
    args = parser.parse_args()

    for path in (args.db, args.gsi_json):
        if not path.exists():
            print(f"ERROR: no existe {path}", file=sys.stderr)
            return 1

    conn = sqlite3.connect(args.db, timeout=5)
    try:
        updates, report = plan(conn, args.gsi_json)
    finally:
        conn.close()

    for source in (GSI_SOURCE, TAI_SOURCE):
        print(f"{source}: posición de la correcta antes {report['before'][source]} → después {report['after'][source]}")
    print(f"TAI con letra citada en la explicación: {report['hints']}")
    print(f"Opciones a reordenar: {len(updates)}")
    if report["errors"]:
        print("ERROR: no se escribe nada:\n  " + "\n  ".join(report["errors"][:20]), file=sys.stderr)
        return 1
    if not args.apply:
        print("\nSimulación: no se ha escrito nada. Repite con --apply.")
        return 0
    if not updates:
        print("Nada que actualizar.")
        return 0

    try:
        backup = backup_database(args.db, args.backup_dir, label="antes-de-fix-option-order")
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
        conn.executemany("UPDATE question_options SET display_order = ? WHERE id = ?", updates)
        conn.commit()
        remaining, _ = plan(conn, args.gsi_json)
    finally:
        conn.close()
    if remaining:
        print(f"ERROR: quedan {len(remaining)} opciones sin cuadrar.", file=sys.stderr)
        return 1
    print(f"[ok] Reordenadas {len(updates)} opciones; la BD coincide con el orden esperado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
