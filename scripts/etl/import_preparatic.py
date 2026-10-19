"""
Script ETL para importar las preguntas y catálogo de PreparaTIC en test_engine.sqlite.

Origen:
  - scripts/etl/preparatic_bundle_extracted.json (16.680 preguntas)
  - scripts/etl/preparatic_catalog.json (8 bloques, 133 temas)

Destino:
  - services/test-engine/data/test_engine.sqlite

Tablas pobladas:
  - syllabi (maestro A1 TIC)
  - questions
  - question_options
  - question_syllabus_tags

Ejecución:
  python scripts/etl/import_preparatic.py
"""

from __future__ import annotations

import json
import logging
import random
import sqlite3
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("import_preparatic")

SOURCE_NAME = "preparatic-bundle-2026"
SYLLABUS_ID = "preparatic-a1"
SYLLABUS_CODE = "age/a1-sti"
SYLLABUS_NAME = "A1 TIC AGE"
ORGANISM = "AGE"


def parse_question_metadata(q: dict) -> tuple[int | None, bool]:
    """Año de convocatoria y marca de examen oficial de una pregunta del bundle.

    El bundle trae ``year`` como texto de 4 cifras y ``exam`` como ``True`` o ausente.
    """
    raw_year = str(q.get("year") or "").strip()
    year = int(raw_year) if raw_year.isdigit() and len(raw_year) == 4 else None
    return year, q.get("exam") is True


def get_db_connection(db_path: Path) -> sqlite3.Connection:
    """Abre conexión SQLite configurando pragmas para WAL y claves foráneas."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def ensure_syllabus(conn: sqlite3.Connection) -> None:
    """Garantiza que la fila del temario oficial exista en la tabla syllabi."""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO syllabi (id, code, name, organism)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            code=excluded.code,
            name=excluded.name,
            organism=excluded.organism
        """,
        (SYLLABUS_ID, SYLLABUS_CODE, SYLLABUS_NAME, ORGANISM),
    )
    conn.commit()
    logger.info("Temario verificado en syllabi: id='%s', code='%s', name='%s'.", SYLLABUS_ID, SYLLABUS_CODE, SYLLABUS_NAME)


def validate_question(q: dict, valid_blocks: set[str], valid_topics: set[str]) -> str | None:
    """Valida la integridad de una pregunta antes de insertarla.

    Returns:
        None si es válida, o un string describiendo el motivo de descarte.
    """
    answers = q.get("answers", [])
    if not answers:
        return "Pregunta sin lista de opciones ('answers' vacío)."

    correct_count = sum(1 for a in answers if a.get("right") is True)
    if correct_count != 1:
        return f"Se esperaba exactamente 1 respuesta correcta, se encontraron {correct_count}."

    block = q.get("block")
    if not block or block not in valid_blocks:
        return f"Bloque '{block}' no reconocido en el catálogo oficial."

    topic = str(q.get("topic", ""))
    if not topic or topic not in valid_topics:
        return f"Tema '{topic}' no reconocido en el catálogo oficial."

    statement = q.get("text", "").strip()
    if not statement:
        return "Enunciado de la pregunta vacío."

    return None


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    questions_file = repo_root / "scripts" / "etl" / "preparatic_bundle_extracted.json"
    catalog_file = repo_root / "scripts" / "etl" / "preparatic_catalog.json"
    warnings_file = repo_root / "scripts" / "etl" / "preparatic_import_warnings.json"
    db_path = repo_root / "services" / "test-engine" / "data" / "test_engine.sqlite"

    if not questions_file.is_file():
        logger.error("No se encontró el fichero de preguntas en: %s", questions_file)
        sys.exit(1)

    if not catalog_file.is_file():
        logger.error("No se encontró el fichero de catálogo en: %s", catalog_file)
        sys.exit(1)

    if not db_path.is_file():
        logger.error("La base de datos SQLite no existe en: %s. Ejecuta create_schema primero.", db_path)
        sys.exit(1)

    t0 = time.time()
    logger.info("Cargando catálogo desde: %s...", catalog_file.name)
    with open(catalog_file, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    valid_blocks = {b["name"] for b in catalog.get("blocks", [])}
    valid_topics = {str(t["id"]) for t in catalog.get("topics", [])}
    logger.info("Catálogo validado: %d bloques y %d temas.", len(valid_blocks), len(valid_topics))

    if len(valid_blocks) != 8 or len(valid_topics) != 133:
        logger.error("Error crítico: el catálogo debe contener exactamente 8 bloques y 133 temas.")
        sys.exit(1)

    logger.info("Cargando preguntas extraídas desde: %s...", questions_file.name)
    with open(questions_file, "r", encoding="utf-8") as f:
        questions = json.load(f)
    logger.info("Cargadas %d preguntas en memoria.", len(questions))

    conn = get_db_connection(db_path)
    ensure_syllabus(conn)

    warnings: list[dict] = []
    inserted_questions = 0
    skipped_existing = 0
    inserted_options = 0
    inserted_tags = 0

    letter_to_order = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}

    logger.info("Iniciando validación e inserción en base de datos...")
    cursor = conn.cursor()

    # Pre-cargar IDs de preguntas ya existentes con este source para máxima velocidad e idempotencia
    cursor.execute("SELECT source_id, id FROM questions WHERE source = ?", (SOURCE_NAME,))
    existing_map = {row[0]: row[1] for row in cursor.fetchall()}
    if existing_map:
        logger.info("Preguntas ya registradas previamente en BD con source '%s': %d.", SOURCE_NAME, len(existing_map))

    # Transacción por lotes para máximo rendimiento
    cursor.execute("BEGIN TRANSACTION;")

    for q in questions:
        q_id = str(q.get("id", "")).strip()
        validation_error = validate_question(q, valid_blocks, valid_topics)
        if validation_error:
            warnings.append({
                "id": q_id,
                "reason": validation_error,
                "question": q,
            })
            continue

        statement = q.get("text", "").strip()
        comments = q.get("comments")
        justification = str(comments).strip() if comments else None

        # Si ya existe por source + source_id, saltar o reutilizar ID
        if q_id in existing_map:
            skipped_existing += 1
            db_question_id = existing_map[q_id]
        else:
            year, is_official_exam = parse_question_metadata(q)
            cursor.execute(
                """
                INSERT INTO questions (
                    statement, justification, img_path, source, source_id,
                    is_annulled, annulment_reason, pending_classification,
                    year, is_official_exam
                ) VALUES (?, ?, NULL, ?, ?, 0, NULL, 0, ?, ?)
                """,
                (statement, justification, SOURCE_NAME, q_id, year, int(is_official_exam)),
            )
            db_question_id = cursor.lastrowid
            existing_map[q_id] = db_question_id
            inserted_questions += 1

            # Insertar opciones
            answers = q.get("answers", [])
            for opt_idx, ans in enumerate(answers):
                letter = str(ans.get("letter", "")).strip().lower()
                display_order = letter_to_order.get(letter, opt_idx)
                opt_text = str(ans.get("answer", "")).strip()
                is_correct = 1 if ans.get("right") is True else 0

                cursor.execute(
                    """
                    INSERT INTO question_options (
                        question_id, option_text, is_correct, display_order, justification
                    ) VALUES (?, ?, ?, ?, NULL)
                    """,
                    (db_question_id, opt_text, is_correct, display_order),
                )
                inserted_options += 1

        # Insertar etiqueta de temario (idempotente con INSERT OR IGNORE)
        block = str(q.get("block"))
        topic = str(q.get("topic"))
        cursor.execute(
            """
            INSERT OR IGNORE INTO question_syllabus_tags (
                question_id, syllabus_id, block, topic
            ) VALUES (?, ?, ?, ?)
            """,
            (db_question_id, SYLLABUS_ID, block, topic),
        )
        if cursor.rowcount > 0:
            inserted_tags += 1

    conn.commit()

    # Guardar fichero de avisos si hubo alguna incidencia
    if warnings:
        logger.warning("Generando fichero de advertencias con %d preguntas descartadas...", len(warnings))
        with open(warnings_file, "w", encoding="utf-8") as f:
            json.dump(warnings, f, ensure_ascii=False, indent=2)
    else:
        logger.info("¡Cero advertencias! Todas las preguntas pasaron la validación de integridad al 100%%.")
        if warnings_file.exists():
            warnings_file.unlink()

    # Verificación final contra SQLite
    total_db_questions = cursor.execute("SELECT COUNT(*) FROM questions WHERE source = ?", (SOURCE_NAME,)).fetchone()[0]
    total_db_options = cursor.execute(
        """
        SELECT COUNT(*) FROM question_options
        WHERE question_id IN (SELECT id FROM questions WHERE source = ?)
        """,
        (SOURCE_NAME,),
    ).fetchone()[0]
    total_db_tags = cursor.execute(
        """
        SELECT COUNT(*) FROM question_syllabus_tags
        WHERE question_id IN (SELECT id FROM questions WHERE source = ?)
        """,
        (SOURCE_NAME,),
    ).fetchone()[0]

    elapsed = time.time() - t0
    logger.info("=" * 65)
    logger.info("RESUMEN DE IMPORTACIÓN A SQLITE (test_engine.sqlite)")
    logger.info("=" * 65)
    logger.info("Total preguntas leídas del JSON      : %d", len(questions))
    logger.info("Preguntas con inconsistencias/avisos : %d", len(warnings))
    logger.info("Preguntas nuevas insertadas en BD    : %d", inserted_questions)
    logger.info("Preguntas existentes omitidas (dedup): %d", skipped_existing)
    logger.info("Total preguntas PreparaTIC en BD     : %d", total_db_questions)
    logger.info("Total opciones insertadas en BD      : %d", total_db_options)
    logger.info("Total etiquetas de temario asociadas : %d", total_db_tags)
    logger.info("Promedio de opciones por pregunta    : %.2f", total_db_options / total_db_questions if total_db_questions else 0)
    logger.info("Tiempo de importación                : %.2f segundos", elapsed)
    logger.info("=" * 65)

    # Inspección de 3 preguntas al azar extraídas directamente de SQLite
    logger.info("Verificación de muestra aleatoria desde SQLite:")
    sample_ids = cursor.execute(
        "SELECT id FROM questions WHERE source = ? ORDER BY RANDOM() LIMIT 3",
        (SOURCE_NAME,),
    ).fetchall()

    for idx, (q_db_id,) in enumerate(sample_ids, 1):
        q_row = cursor.execute(
            "SELECT statement, source_id, justification FROM questions WHERE id = ?",
            (q_db_id,),
        ).fetchone()
        opt_rows = cursor.execute(
            "SELECT option_text, is_correct, display_order FROM question_options WHERE question_id = ? ORDER BY display_order",
            (q_db_id,),
        ).fetchall()
        tag_rows = cursor.execute(
            "SELECT block, topic FROM question_syllabus_tags WHERE question_id = ?",
            (q_db_id,),
        ).fetchall()

        tag_str = ", ".join(f"Bloque {b} / Tema {t}" for b, t in tag_rows)
        logger.info("--- Muestra #%d (ID BD: %d | Source ID: %s | %s) ---", idx, q_db_id, q_row[1], tag_str)
        logger.info("Enunciado: %s", q_row[0][:120] + ("..." if len(q_row[0]) > 120 else ""))
        for opt in opt_rows:
            mark = "[CORRECTA]" if opt[1] == 1 else "          "
            logger.info("  %s %s: %s", mark, chr(65 + opt[2]), opt[0][:80] + ("..." if len(opt[0]) > 80 else ""))

    conn.close()
    logger.info("¡Importación de PreparaTIC finalizada y verificada con éxito!")


if __name__ == "__main__":
    main()
