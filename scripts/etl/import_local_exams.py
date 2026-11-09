#!/usr/bin/env python3
"""Importa a test-engine los exámenes de imports/ que solo existían como SQL para MariaDB.

Fuentes (lista explícita; ver docs/MIGRACION.md, paso 2):
- Ayto. Madrid Técnico Auxiliar TIC 2021/2024 (6 cuestionarios, 294 preguntas)
- Ayto. Majadahonda Técnico de Informática (44)
- Comunidad de Madrid · Madrid Digital IA P01 y P02 2026 (100)
- UC3M A2 GSI 2021 y 2024 (3 exámenes, 270)

Excluido a propósito:
- ``old_ayto_madrid_aux_tic_import.sql``: versión anterior del fichero ``_fixed``.
- ``import_cm_tic_p01_analista_aplicaciones_template.sql``: sin plantilla oficial
  ("[PENDIENTE DE PLANTILLA OFICIAL]").
- Los tres SQL sueltos de UC3M: mismo contenido que ``import_uc3m_a2_gsi_examenes.sql``.

Cada pregunta conserva el orden original de sus opciones (A, B, C...):
- Ayto. Madrid: desde ``review_questions.csv`` (opcion_A..C y letra correcta).
- Resto: desde las justificaciones ("Respuesta correcta: opción C", "Opción A incorrecta...").

Las preguntas entran con ``pending_classification = 1`` y etiqueta de temario sin
bloque/tema, igual que las de TAI. Año y marca de examen oficial salen de question_sets.

Por defecto solo valida y muestra el resumen. Con --apply hace una copia verificada,
inserta en una transacción (todo o nada) y verifica. Es idempotente: las preguntas ya
importadas (mismo source + source_id) no se tocan.

    docker compose stop test-engine
    python scripts/etl/import_local_exams.py            # validación y resumen
    python scripts/etl/import_local_exams.py --apply
    docker compose start test-engine
"""

from __future__ import annotations

import argparse
import csv
import re
import sqlite3
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
IMPORTS = REPO_ROOT / "imports"
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from mysql_dump_parser import LAST_INSERT_ID, parse_dump  # noqa: E402
from backfill_preparatic_metadata import ensure_columns, missing_columns  # noqa: E402
from backup_test_engine import DEFAULT_DB, DEFAULT_DIR, backup_database  # noqa: E402

LETTERS = "ABCDE"

SCORING_RULES = {
    "age-oficial-tercio": {
        "name": "AGE oficial A − F/3", "correct_score": Decimal(1), "wrong_penalty": Decimal(1) / Decimal(3),
        "blank_score": Decimal(0), "score_scale": Decimal(10), "min_score_zero": True,
    },
    "oficial-cuarto": {
        "name": "Oficial A − F/4", "correct_score": Decimal(1), "wrong_penalty": Decimal(1) / Decimal(4),
        "blank_score": Decimal(0), "score_scale": Decimal(10), "min_score_zero": True,
    },
}


@dataclass(frozen=True)
class Syllabus:
    id: str
    code: str
    name: str
    organism: str


@dataclass(frozen=True)
class Source:
    name: str            # questions.source (≤ 32)
    sql: Path
    syllabus: Syllabus
    scoring_rule: str | None   # code; None = no consta en las bases revisadas
    order_csv: Path | None = None


SOURCES = [
    Source(
        name="ayto-madrid-aux-tic",
        sql=IMPORTS / "ayto_madrid_aux_tic/generated/ayto_madrid_aux_tic_import_fixed.sql",
        syllabus=Syllabus("ayto-madrid-aux-tic", "ayuntamiento-madrid/aux-tic",
                          "Ayto. Madrid Técnico Auxiliar TIC", "Ayuntamiento de Madrid"),
        scoring_rule="age-oficial-tercio",
        order_csv=IMPORTS / "ayto_madrid_aux_tic/generated/review_questions.csv",
    ),
    Source(
        name="ayto-majadahonda",
        sql=IMPORTS / "ayto_majadahonda/generated/import_tecnicoinformatico.sql",
        syllabus=Syllabus("majadahonda-tecnico-informatica", "ayuntamiento-majadahonda/tecnico-informatica",
                          "Ayto. Majadahonda Técnico de Informática", "Ayuntamiento de Majadahonda"),
        scoring_rule=None,
    ),
    Source(
        name="cm-madrid-digital",
        sql=IMPORTS / "cm_madrid_digital/generated/import_cm_ia_p01_consultor_software.sql",
        syllabus=Syllabus("cm-madrid-digital-ia", "comunidad-madrid/administracion-digital/ia",
                          "Comunidad de Madrid · Madrid Digital IA", "Comunidad de Madrid"),
        scoring_rule="age-oficial-tercio",
    ),
    Source(
        name="cm-madrid-digital",
        sql=IMPORTS / "cm_madrid_digital/generated/import_cm_ia_p02_consultor_gobierno.sql",
        syllabus=Syllabus("cm-madrid-digital-ia", "comunidad-madrid/administracion-digital/ia",
                          "Comunidad de Madrid · Madrid Digital IA", "Comunidad de Madrid"),
        scoring_rule="age-oficial-tercio",
    ),
    Source(
        name="uc3m-a2-gsi",
        sql=IMPORTS / "uc3m_gsi/generated/import_uc3m_a2_gsi_examenes.sql",
        syllabus=Syllabus("uc3m-a2-gsi", "uc3m/a2-gsi", "UC3M A2 Gestión de Sistemas e Informática", "UC3M"),
        scoring_rule="oficial-cuarto",
    ),
]

_CORRECT_LETTER_RE = re.compile(r"[Rr]espuesta correcta:\s*opci[oó]n\s+([A-E])\b")
_WRONG_LETTER_RE = re.compile(r"^\s*Opci[oó]n\s+([A-E])\s+incorrecta\b")
_BOILERPLATE_RE = re.compile(r"^\s*Opci[oó]n\s+[A-E]\s+incorrecta\s+según plantilla oficial[^.]*\.?\s*$")


@dataclass
class Option:
    letter: str
    text: str
    is_correct: bool
    justification: str | None


@dataclass
class ImportedQuestion:
    source: str
    source_id: str
    exam_name: str
    position: int
    statement: str
    justification: str | None
    img_path: str | None
    year: int | None
    is_official_exam: bool
    options: list[Option]


@dataclass
class ImportedExam:
    name: str
    year: int | None
    convocatoria: str | None
    source: Source
    questions: list[ImportedQuestion] = field(default_factory=list)


def slugify(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def _clean(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _to_year(value: object) -> int | None:
    text = str(value).strip() if value is not None else ""
    return int(text) if text.isdigit() and len(text) == 4 else None


def _load_order_csv(path: Path) -> dict[str, list[dict[str, str]]]:
    by_exam: dict[str, list[dict[str, str]]] = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            by_exam.setdefault(row["categoria"].strip(), []).append(row)
    return by_exam


WARNINGS: list[str] = []


def _order_from_csv(row: dict[str, str], correct: str, wrongs: list[str], ctx: str) -> list[tuple[str, str]]:
    """Devuelve [(letra, texto)] con el texto del SQL y el orden del CSV.

    El SQL ``_fixed`` es la fuente del texto (versión corregida). Del CSV se toma la
    letra de la correcta; las incorrectas ocupan las letras restantes en el orden del
    SQL. Si alguna incorrecta difiere en texto del CSV se avisa, y si el orden del SQL
    contradice al CSV (un texto idéntico en otra letra) se rechaza.
    """
    letters = [l for l in LETTERS if row.get(f"opcion_{l}", "").strip()]
    by_letter = {l: row[f"opcion_{l}"].strip() for l in letters}
    correct_letter = row["respuesta_correcta_letra"].strip()
    if len(letters) != 1 + len(wrongs):
        raise ValueError(f"{ctx}: el CSV tiene {len(letters)} opciones y el SQL {1 + len(wrongs)}")
    if correct_letter not in by_letter:
        raise ValueError(f"{ctx}: letra correcta {correct_letter!r} sin opción en el CSV")
    if by_letter[correct_letter] != correct:
        if correct in by_letter.values():
            raise ValueError(f"{ctx}: la respuesta correcta del SQL está en otra letra del CSV")
        WARNINGS.append(
            f"{ctx} opción {correct_letter} (correcta): SQL {correct!r} / CSV {by_letter[correct_letter]!r} (se usa el SQL)"
        )

    wrong_letters = [l for l in letters if l != correct_letter]
    for letter, text in zip(wrong_letters, wrongs):
        if by_letter[letter] != text:
            if text in by_letter.values():
                raise ValueError(f"{ctx}: el orden de las incorrectas del SQL contradice al CSV")
            WARNINGS.append(f"{ctx} opción {letter}: SQL {text!r} / CSV {by_letter[letter]!r} (se usa el SQL)")
    ordered = dict(zip(wrong_letters, wrongs))
    ordered[correct_letter] = correct
    return [(l, ordered[l]) for l in letters]


def load_source(source: Source) -> list[ImportedExam]:
    parsed = parse_dump(source.sql.read_text(encoding="utf-8"))
    sets = {r.values["categoria"]: r.values for r in parsed.rows if r.table == "question_sets"}

    # Agrupa cada ptype con sus incorrectas (vinculadas por LAST_INSERT_ID).
    raw: list[tuple[dict, list[dict]]] = []
    for row in parsed.rows:
        if row.table == "ptype":
            raw.append((row.values, []))
        elif row.table == "incorrectas":
            if row.values.get("id_pregunta") is not LAST_INSERT_ID or not raw:
                raise ValueError(f"{source.sql.name}: incorrecta sin pregunta previa")
            raw[-1][1].append(row.values)

    csv_rows = _load_order_csv(source.order_csv) if source.order_csv else {}
    exams: dict[str, ImportedExam] = {}
    seen_in_exam: Counter = Counter()

    for ptype, wrongs in raw:
        cat = str(ptype["categoria"]).strip()
        qset = sets.get(cat)
        if qset is None:
            raise ValueError(f"{source.sql.name}: categoría sin question_sets: {cat}")
        exam = exams.setdefault(cat, ImportedExam(
            name=cat, year=_to_year(qset.get("convocatoria_year")),
            convocatoria=_clean(qset.get("turno")), source=source,
        ))
        seen_in_exam[cat] += 1
        index = seen_in_exam[cat]
        ctx = f"{cat} #{index}"

        correct_text = str(ptype["respuesta"]).strip()
        wrong_texts = [str(w["respuesta"]).strip() for w in wrongs]
        justif_q = _clean(ptype.get("justif"))

        if source.order_csv:
            rows = csv_rows.get(cat, [])
            if index > len(rows):
                raise ValueError(f"{ctx}: no está en {source.order_csv.name}")
            csv_row = rows[index - 1]
            if csv_row["pregunta"].strip() != str(ptype["pregunta"]).strip():
                raise ValueError(f"{ctx}: el enunciado no coincide con la fila del CSV")
            position = int(csv_row["pregunta_num"])
            ordered = _order_from_csv(csv_row, correct_text, wrong_texts, ctx)
            options = [Option(l, t, t == correct_text, None) for l, t in ordered]
        else:
            position = index
            m = _CORRECT_LETTER_RE.search(justif_q or "")
            if not m:
                raise ValueError(f"{ctx}: la justificación no indica la letra correcta")
            options = [Option(m.group(1), correct_text, True, None)]
            for w in wrongs:
                wm = _WRONG_LETTER_RE.match(str(w.get("justif") or ""))
                if not wm:
                    raise ValueError(f"{ctx}: incorrecta sin letra en la justificación")
                wj = _clean(w.get("justif"))
                if wj and _BOILERPLATE_RE.match(wj):
                    wj = None
                options.append(Option(wm.group(1), str(w["respuesta"]).strip(), False, wj))

        letters = sorted(o.letter for o in options)
        if letters != list(LETTERS[: len(options)]):
            raise ValueError(f"{ctx}: letras de opciones no consecutivas: {letters}")
        if sum(o.is_correct for o in options) != 1:
            raise ValueError(f"{ctx}: debe haber exactamente una opción correcta")
        if not 3 <= len(options) <= 5:
            raise ValueError(f"{ctx}: número de opciones inesperado ({len(options)})")
        options.sort(key=lambda o: o.letter)

        source_id = f"{slugify(cat)}-{position:03d}"
        if len(source_id) > 64:
            raise ValueError(f"{ctx}: source_id demasiado largo ({source_id})")

        exam.questions.append(ImportedQuestion(
            source=source.name, source_id=source_id, exam_name=cat, position=position,
            statement=str(ptype["pregunta"]).strip(), justification=justif_q,
            img_path=_clean(ptype.get("img_path")), year=exam.year,
            is_official_exam=str(qset.get("tipo") or "").strip().lower() == "examen oficial",
            options=options,
        ))

    for exam in exams.values():
        positions = [q.position for q in exam.questions]
        if len(set(positions)) != len(positions):
            raise ValueError(f"{exam.name}: posiciones repetidas")
    return list(exams.values())


def load_all() -> list[ImportedExam]:
    exams: list[ImportedExam] = []
    for source in SOURCES:
        exams.extend(load_source(source))
    ids = Counter((q.source, q.source_id) for e in exams for q in e.questions)
    dup = [k for k, n in ids.items() if n > 1]
    if dup:
        raise ValueError(f"source_id duplicados: {dup[:5]}")
    return exams


def print_summary(exams: list[ImportedExam]) -> None:
    total = 0
    for e in exams:
        correct = Counter(o.letter for q in e.questions for o in q.options if o.is_correct)
        n_opts = Counter(len(q.options) for q in e.questions)
        print(f"- {e.name}: {len(e.questions)} preguntas · año {e.year} · {e.convocatoria or '—'} · "
              f"baremo {e.source.scoring_rule or 'sin regla (no consta)'} · opciones {dict(n_opts)} · "
              f"correctas {dict(sorted(correct.items()))}")
        total += len(e.questions)
    print(f"Total: {total} preguntas en {len(exams)} exámenes.")
    if WARNINGS:
        print(f"\nAvisos ({len(WARNINGS)}):")
        for w in WARNINGS:
            print(f"  - {w}")


def _ensure_scoring_rule(conn: sqlite3.Connection, code: str) -> int:
    row = conn.execute("SELECT id FROM scoring_rules WHERE code = ?", (code,)).fetchone()
    if row:
        return row[0]
    r = SCORING_RULES[code]
    cur = conn.execute(
        "INSERT INTO scoring_rules (code, name, correct_score, wrong_penalty, blank_score, score_scale, min_score_zero) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (code, r["name"], str(r["correct_score"]), str(r["wrong_penalty"]), str(r["blank_score"]),
         str(r["score_scale"]), int(r["min_score_zero"])),
    )
    return cur.lastrowid


def apply_import(conn: sqlite3.Connection, exams: list[ImportedExam]) -> dict[str, int]:
    stats = Counter()
    for e in exams:
        s = e.source.syllabus
        if conn.execute("SELECT 1 FROM syllabi WHERE id = ?", (s.id,)).fetchone() is None:
            conn.execute("INSERT INTO syllabi (id, code, name, organism) VALUES (?, ?, ?, ?)",
                         (s.id, s.code, s.name, s.organism))
            stats["syllabi"] += 1
        rule_id = _ensure_scoring_rule(conn, e.source.scoring_rule) if e.source.scoring_rule else None

        row = conn.execute("SELECT id FROM exams WHERE name = ? AND syllabus_id = ?", (e.name, s.id)).fetchone()
        if row:
            exam_id = row[0]
        else:
            exam_id = conn.execute(
                "INSERT INTO exams (name, year, convocatoria, syllabus_id, scoring_rule_id, duration_seconds) "
                "VALUES (?, ?, ?, ?, ?, NULL)",
                (e.name, e.year, e.convocatoria, s.id, rule_id),
            ).lastrowid
            stats["exams"] += 1

        for q in e.questions:
            if conn.execute("SELECT 1 FROM questions WHERE source = ? AND source_id = ?",
                            (q.source, q.source_id)).fetchone():
                stats["skipped"] += 1
                continue
            qid = conn.execute(
                "INSERT INTO questions (statement, justification, img_path, source, source_id, is_annulled, "
                "annulment_reason, pending_classification, year, is_official_exam) "
                "VALUES (?, ?, ?, ?, ?, 0, NULL, 1, ?, ?)",
                (q.statement, q.justification, q.img_path, q.source, q.source_id, q.year, int(q.is_official_exam)),
            ).lastrowid
            for order, opt in enumerate(q.options):
                conn.execute(
                    "INSERT INTO question_options (question_id, option_text, is_correct, display_order, justification) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (qid, opt.text, int(opt.is_correct), order, opt.justification),
                )
            conn.execute(
                "INSERT INTO question_syllabus_tags (question_id, syllabus_id, block, topic) VALUES (?, ?, NULL, NULL)",
                (qid, s.id),
            )
            conn.execute(
                "INSERT INTO exam_questions (exam_id, question_id, position, is_reserve) VALUES (?, ?, ?, 0)",
                (exam_id, qid, q.position),
            )
            stats["questions"] += 1
    return dict(stats)


def verify(conn: sqlite3.Connection, exams: list[ImportedExam]) -> list[str]:
    problems = []
    for e in exams:
        n = conn.execute(
            "SELECT COUNT(*) FROM exam_questions eq JOIN exams x ON x.id = eq.exam_id "
            "WHERE x.name = ? AND x.syllabus_id = ?", (e.name, e.source.syllabus.id),
        ).fetchone()[0]
        if n != len(e.questions):
            problems.append(f"{e.name}: {n} en BD, {len(e.questions)} esperadas")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Importa los exámenes locales de imports/ a test-engine.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--backup-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--apply", action="store_true", help="Escribir en la BD (por defecto, solo validar)")
    args = parser.parse_args()

    try:
        exams = load_all()
    except ValueError as exc:
        print(f"ERROR de validación: {exc}. No se escribe nada.", file=sys.stderr)
        return 1
    print_summary(exams)

    if not args.apply:
        print("\nValidación correcta. No se ha escrito nada. Repite con --apply.")
        return 0
    if not args.db.exists():
        print(f"ERROR: no existe {args.db}", file=sys.stderr)
        return 1

    try:
        backup = backup_database(args.db, args.backup_dir, label="antes-de-import-local-exams")
    except Exception as exc:
        print(f"ERROR: no se pudo hacer la copia previa; no se escribe nada ({exc})", file=sys.stderr)
        return 1
    print(f"[ok] Copia previa: {backup}")

    conn = sqlite3.connect(args.db, timeout=5)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        if missing_columns(conn):
            ensure_columns(conn)
        try:
            conn.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as exc:
            print(f"ERROR: la BD está en uso ({exc}). Ejecuta: docker compose stop test-engine", file=sys.stderr)
            return 1
        try:
            stats = apply_import(conn, exams)
        except Exception:
            conn.rollback()
            raise
        conn.commit()
        problems = verify(conn, exams)
    finally:
        conn.close()

    print(f"[ok] Insertado: {stats}")
    if problems:
        print("ERROR en la verificación:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    print("[ok] Verificación: cada examen tiene en BD todas sus preguntas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
