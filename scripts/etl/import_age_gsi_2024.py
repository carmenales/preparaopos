"""
Script ETL para importar el Examen Oficial AGE A2 GSI (Turno Libre) 2024
en test_engine.sqlite.

Origen:
  - imports/age_a2_gsi/generated/import_age_gsi_2024.sql

Destino:
  - services/test-engine/data/test_engine.sqlite
  - scripts/etl/age_gsi_2024_anuladas.json (registro de las 4 anuladas)

Tablas pobladas:
  - syllabi (id='age-gsi-official', code='age/a2-gsi')
  - exams (Examen oficial 'AGE A2 GSI LIBRE 2024')
  - exam_questions (con posición oficial exacta 1-105 y bandera is_reserve)
  - questions (source = 'age-gsi-2024', source_id = '1..105', pending_classification = 1)
  - question_options (opción correcta + 3 incorrectas con su justificación)
  - question_syllabus_tags (asociadas a age-gsi-official)

Ejecución:
  python scripts/etl/import_age_gsi_2024.py
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("import_age_gsi_2024")

SOURCE_NAME = "age-gsi-2024"
SYLLABUS_ID = "age-gsi-official"
SYLLABUS_CODE = "age/a2-gsi"
SYLLABUS_NAME = "AGE A2 GSI"
ORGANISM = "AGE"
EXAM_NAME = "AGE A2 GSI LIBRE 2024"


def get_db_connection(db_path: Path) -> sqlite3.Connection:
    """Abre conexión SQLite configurando pragmas para WAL y claves foráneas."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def ensure_syllabus(conn: sqlite3.Connection) -> None:
    """Garantiza que la fila del temario A2 GSI exista en la tabla syllabi."""
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


def extract_single_quoted_strings(text: str) -> list[str]:
    """Extrae todas las cadenas entre comillas simples respetando escapes \' y ''."""
    strings = []
    in_str = False
    current = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if in_str:
            if c == "\\":
                i += 1
                if i < n:
                    current.append(text[i])
            elif c == "'":
                if i + 1 < n and text[i + 1] == "'":
                    current.append("'")
                    i += 1
                else:
                    in_str = False
                    strings.append("".join(current))
                    current = []
            else:
                current.append(c)
        else:
            if c == "'":
                in_str = True
        i += 1
    return strings


def parse_age_gsi_sql(sql_path: Path) -> tuple[list[dict], list[int]]:
    """Parsea el fichero SQL extrayendo preguntas activas y números anulados."""
    logger.info("Leyendo y parseando SQL oficial: %s...", sql_path.name)
    content = sql_path.read_text(encoding="utf-8")

    # Separar por bloques de preguntas: "-- Pregunta (\d+)"
    blocks = re.split(r"(?m)^--\s*Pregunta\s+(\d+)(?:[^\n]*)?$", content)

    parsed_questions: list[dict] = []
    anuladas: list[int] = []

    for i in range(1, len(blocks), 2):
        q_num = int(blocks[i])
        block_text = blocks[i + 1].strip()

        # Si el bloque no contiene INSERT INTO ptype, es una pregunta anulada comentada
        if "INSERT INTO ptype" not in block_text:
            anuladas.append(q_num)
            continue

        parts = block_text.split("SET @id_pregunta := LAST_INSERT_ID();")
        ptype_part = parts[0]
        inc_part = parts[1] if len(parts) > 1 else ""

        ptype_strings = extract_single_quoted_strings(ptype_part)
        inc_strings = extract_single_quoted_strings(inc_part)

        if len(ptype_strings) < 3:
            raise ValueError(f"Pregunta {q_num}: se esperaban >= 3 cadenas en ptype, obtenidas {len(ptype_strings)}")

        statement = ptype_strings[0].strip()
        correct_answer = ptype_strings[1].strip()
        justif = ptype_strings[2].strip()

        # Extraer número oficial de pregunta mediante regex sobre justif (Requisito obligatorio)
        m = re.search(r"Pregunta(?:\s+de\s+reserva)?\s+(\d+)", justif)
        if not m:
            raise ValueError(f"Pregunta {q_num}: no se pudo extraer el número oficial de justif: '{justif}'")

        official_num = int(m.group(1))
        if official_num != q_num:
            raise ValueError(f"Discrepancia en número de pregunta: comentario={q_num} vs justif={official_num}")

        # En incorrectas vienen pares (respuesta, justif)
        if len(inc_strings) % 2 != 0:
            raise ValueError(f"Pregunta {q_num}: número impar de cadenas en incorrectas ({len(inc_strings)})")

        incorrectas = []
        for k in range(0, len(inc_strings), 2):
            incorrectas.append({
                "texto": inc_strings[k].strip(),
                "justif": inc_strings[k + 1].strip() if inc_strings[k + 1].strip() else None,
            })

        is_reserve = official_num > 100
        parsed_questions.append({
            "official_number": official_num,
            "is_reserve": is_reserve,
            "statement": statement,
            "correct_answer": correct_answer,
            "justification": justif,
            "incorrectas": incorrectas,
        })

    logger.info("Parseo completado: %d preguntas activas y %d anuladas.", len(parsed_questions), len(anuladas))
    return parsed_questions, anuladas


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    sql_path = repo_root / "imports" / "age_a2_gsi" / "generated" / "import_age_gsi_2024.sql"
    anuladas_path = repo_root / "scripts" / "etl" / "age_gsi_2024_anuladas.json"
    db_path = repo_root / "services" / "test-engine" / "data" / "test_engine.sqlite"

    if not sql_path.is_file():
        logger.error("No se encontró el fichero SQL en: %s", sql_path)
        sys.exit(1)

    if not db_path.is_file():
        logger.error("La base de datos SQLite no existe en: %s. Ejecuta create_schema primero.", db_path)
        sys.exit(1)

    t0 = time.time()
    questions, anuladas = parse_age_gsi_sql(sql_path)

    # 1. Registrar artefacto de preguntas anuladas
    logger.info("Guardando registro de preguntas anuladas en: %s...", anuladas_path.name)
    anuladas_data = {
        "examen": EXAM_NAME,
        "total_preguntas_cuadernillo": 105,
        "preguntas_ordinarias_totales": 100,
        "preguntas_reserva_totales": 5,
        "preguntas_anuladas": anuladas,
        "motivo": "Anuladas por el tribunal calificador en la plantilla definitiva oficial (sin respuesta válida)",
    }
    with open(anuladas_path, "w", encoding="utf-8") as f:
        json.dump(anuladas_data, f, ensure_ascii=False, indent=2)

    # 2. Conectar a SQLite y asegurar temario y regla de puntuación
    conn = get_db_connection(db_path)
    ensure_syllabus(conn)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM scoring_rules WHERE code = 'age-oficial-tercio'")
    sr_row = cursor.fetchone()
    scoring_rule_id = sr_row[0] if sr_row else None

    # 3. Asegurar examen en tabla exams
    cursor.execute("SELECT id FROM exams WHERE name = ? AND syllabus_id = ?", (EXAM_NAME, SYLLABUS_ID))
    existing_exam = cursor.fetchone()
    if existing_exam:
        exam_id = existing_exam[0]
    else:
        cursor.execute(
            """
            INSERT INTO exams (name, year, convocatoria, syllabus_id, scoring_rule_id, duration_seconds)
            VALUES (?, 2024, 'Turno Libre', ?, ?, 6000)
            """,
            (EXAM_NAME, SYLLABUS_ID, scoring_rule_id),
        )
        exam_id = cursor.lastrowid
    logger.info("Examen verificado en exams: ID=%d, nombre='%s'.", exam_id, EXAM_NAME)

    # 4. Pre-cargar preguntas existentes para idempotencia
    cursor.execute("SELECT source_id, id FROM questions WHERE source = ?", (SOURCE_NAME,))
    existing_q_map = {row[0]: row[1] for row in cursor.fetchall()}

    # 5. Inserción de preguntas, opciones, etiquetas de examen y temario
    logger.info("Iniciando inserción en SQLite...")
    inserted_questions = 0
    skipped_existing = 0
    inserted_options = 0
    inserted_exam_questions = 0
    inserted_tags = 0

    for q in questions:
        q_num = q["official_number"]
        source_id = str(q_num)

        if source_id in existing_q_map:
            skipped_existing += 1
            db_question_id = existing_q_map[source_id]
        else:
            cursor.execute(
                """
                INSERT INTO questions (
                    statement, justification, img_path, source, source_id,
                    is_annulled, annulment_reason, pending_classification
                ) VALUES (?, ?, NULL, ?, ?, 0, NULL, 1)
                """,
                (q["statement"], q["justification"], SOURCE_NAME, source_id),
            )
            db_question_id = cursor.lastrowid
            existing_q_map[source_id] = db_question_id
            inserted_questions += 1

            # Insertar opción correcta (display_order = 0)
            cursor.execute(
                """
                INSERT INTO question_options (
                    question_id, option_text, is_correct, display_order, justification
                ) VALUES (?, ?, 1, 0, NULL)
                """,
                (db_question_id, q["correct_answer"]),
            )
            inserted_options += 1

            # Insertar opciones incorrectas (display_order = 1, 2, 3...)
            for idx, inc in enumerate(q["incorrectas"], 1):
                cursor.execute(
                    """
                    INSERT INTO question_options (
                        question_id, option_text, is_correct, display_order, justification
                    ) VALUES (?, ?, 0, ?, ?)
                    """,
                    (db_question_id, inc["texto"], idx, inc["justif"]),
                )
                inserted_options += 1

        # Vincular a exam_questions respetando posición exacta oficial y bandera is_reserve
        is_reserve_val = 1 if q["is_reserve"] else 0
        cursor.execute(
            """
            INSERT INTO exam_questions (exam_id, question_id, position, is_reserve)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(exam_id, question_id) DO UPDATE SET
                position=excluded.position,
                is_reserve=excluded.is_reserve
            """,
            (exam_id, db_question_id, q_num, is_reserve_val),
        )
        if cursor.rowcount > 0:
            inserted_exam_questions += 1

        # Etiqueta de temario (pendiente de clasificar bloque/tema, idempotente)
        cursor.execute(
            "SELECT id FROM question_syllabus_tags WHERE question_id = ? AND syllabus_id = ?",
            (db_question_id, SYLLABUS_ID),
        )
        if not cursor.fetchone():
            cursor.execute(
                """
                INSERT INTO question_syllabus_tags (
                    question_id, syllabus_id, block, topic
                ) VALUES (?, ?, NULL, NULL)
                """,
                (db_question_id, SYLLABUS_ID),
            )
            inserted_tags += 1

    conn.commit()

    # 6. Verificación exhaustiva
    cursor.execute(
        """
        SELECT eq.position, eq.is_reserve, q.source_id, q.statement
        FROM exam_questions eq
        JOIN questions q ON eq.question_id = q.id
        WHERE eq.exam_id = ?
        ORDER BY eq.position
        """,
        (exam_id,),
    )
    exam_rows = cursor.fetchall()
    positions = [r[0] for r in exam_rows]
    reserve_rows = [r for r in exam_rows if r[1] == 1]
    ordinary_rows = [r for r in exam_rows if r[1] == 0]

    elapsed = time.time() - t0
    logger.info("=" * 65)
    logger.info("RESUMEN DE IMPORTACIÓN AGE GSI 2024 (test_engine.sqlite)")
    logger.info("=" * 65)
    logger.info("Total preguntas parseadas del SQL    : %d", len(questions))
    logger.info("Preguntas anuladas omitidas          : %d (%s)", len(anuladas), ", ".join(map(str, anuladas)))
    logger.info("Preguntas nuevas insertadas en BD    : %d", inserted_questions)
    logger.info("Preguntas existentes omitidas (dedup): %d", skipped_existing)
    logger.info("Total preguntas ordinarias en examen : %d (is_reserve=0)", len(ordinary_rows))
    logger.info("Total preguntas de reserva en examen : %d (is_reserve=1)", len(reserve_rows))
    logger.info("Total filas vinculadas en examen     : %d", len(exam_rows))
    logger.info("Huecos en posiciones 1..100          : %s", sorted(list(set(range(1, 101)) - set(positions))))
    logger.info("Posiciones de reserva                : %s", [r[0] for r in reserve_rows])
    logger.info("Tiempo de importación                : %.2f segundos", elapsed)
    logger.info("=" * 65)

    # Validaciones obligatorias
    assert len(exam_rows) == 101, f"Se esperaban 101 preguntas en el examen, obtenidas {len(exam_rows)}"
    assert len(ordinary_rows) == 96, f"Se esperaban 96 ordinarias, obtenidas {len(ordinary_rows)}"
    assert len(reserve_rows) == 5, f"Se esperaban 5 de reserva, obtenidas {len(reserve_rows)}"
    assert [r[0] for r in reserve_rows] == [101, 102, 103, 104, 105], "Posiciones de reserva no coinciden con 101..105"

    conn.close()
    logger.info("¡Importación de AGE GSI 2024 finalizada y validada con éxito al 100%%!")


if __name__ == "__main__":
    main()

