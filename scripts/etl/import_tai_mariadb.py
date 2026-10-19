"""
Script ETL para importar las preguntas de Preparador TAI (MariaDB / dump SQL)
a la base de datos unificada test_engine.sqlite.

Origen:
  - db/local/001_preparadortai_dump.sql (ptype + incorrectas)
  - apps/preparadortai/assets/img/ (11 imágenes asociadas)

Destino:
  - services/test-engine/data/test_engine.sqlite
  - services/test-engine/presentation/static/img/questions/

Tablas pobladas:
  - syllabi (tai-legacy -> age/c1-tai)
  - exams (52 exámenes/cuestionarios derivados de categoria)
  - exam_questions (vinculación examen-pregunta con orden)
  - questions (source = 'tai-mariadb-legacy')
  - question_options (opción correcta de ptype + incorrectas con justificaciones)
  - question_syllabus_tags (para preguntas con bloque y tema válidos)

Ejecución:
  python scripts/etl/import_tai_mariadb.py
"""

from __future__ import annotations

import logging
import re
import shutil
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from option_order import letter_hint, stable_positions  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("import_tai")

SOURCE_NAME = "tai-mariadb-legacy"
SYLLABUS_ID = "tai-legacy"
SYLLABUS_CODE = "age/c1-tai"
SYLLABUS_NAME = "TAI AGE"
ORGANISM = "AGE"


# Exámenes de otros organismos que también acabaron en ptype de MariaDB. Tienen su
# propio importador (import_local_exams.py, desde imports/*/generated/*.sql); si
# entraran aquí se duplicarían como preguntas de TAI.
LOCAL_EXAM_CATEGORY_PREFIXES = ("AYTO MADRID", "AYTO MAJADAHONDA", "CM MADRID DIGITAL", "UC3M")


def is_local_exam_category(categoria: str | None) -> bool:
    return bool(categoria) and categoria.strip().upper().startswith(LOCAL_EXAM_CATEGORY_PREFIXES)


def get_db_connection(db_path: Path) -> sqlite3.Connection:
    """Abre conexión SQLite configurando pragmas para WAL y claves foráneas."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def ensure_syllabus(conn: sqlite3.Connection) -> None:
    """Garantiza que la fila del temario TAI exista en la tabla syllabi."""
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


def parse_mysql_dump(dump_path: Path) -> tuple[list[dict], dict[int, list[dict]]]:
    """Extrae las filas de ptype e incorrectas desde el dump SQL de MariaDB."""
    logger.info("Parseando dump SQL: %s...", dump_path.name)
    lines = dump_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    mem_db = sqlite3.connect(":memory:")
    mem_cursor = mem_db.cursor()

    mem_cursor.execute("""
    CREATE TABLE ptype (
      id int,
      pregunta text,
      respuesta text,
      justif text,
      img_path text,
      categoria text,
      bloque int,
      tema int
    )
    """)
    mem_cursor.execute("""
    CREATE TABLE incorrectas (
      id int,
      id_pregunta int,
      respuesta text,
      justif text
    )
    """)

    for line in lines:
        line_s = line.strip()
        if not line_s.startswith("INSERT INTO"):
            continue

        m = re.match(r"INSERT INTO `?(ptype|incorrectas)`? VALUES\s*(.+);$", line_s)
        if not m:
            continue

        table, values_str = m.group(1), m.group(2)
        cleaned = values_str.replace(r"\'", "''").replace(r'\"', '"').replace(r"\r\n", "\n").replace(r"\n", "\n")
        sql = f"INSERT INTO {table} VALUES {cleaned}"
        try:
            mem_cursor.execute(sql)
        except Exception as e:
            logger.warning("Error insertando en tabla temporal %s: %s", table, e)

    mem_db.commit()

    # Cargar ptype en lista de dicts
    ptype_rows = mem_cursor.execute(
        "SELECT id, pregunta, respuesta, justif, img_path, categoria, bloque, tema FROM ptype ORDER BY id"
    ).fetchall()
    questions = []
    skipped_local = 0
    for r in ptype_rows:
        if is_local_exam_category(r[5]):
            skipped_local += 1
            continue
        questions.append({
            "id": r[0],
            "pregunta": r[1],
            "respuesta": r[2],
            "justif": r[3],
            "img_path": r[4].strip() if r[4] else None,
            "categoria": r[5].strip() if r[5] else "General TAI",
            "bloque": r[6],
            "tema": r[7],
        })

    # Cargar incorrectas agrupadas por id_pregunta
    inc_rows = mem_cursor.execute(
        "SELECT id_pregunta, respuesta, justif FROM incorrectas ORDER BY id"
    ).fetchall()
    incorrectas_by_q: dict[int, list[dict]] = {}
    for r in inc_rows:
        qid = r[0]
        incorrectas_by_q.setdefault(qid, []).append({
            "respuesta": r[1],
            "justif": r[2],
        })

    mem_db.close()
    if skipped_local:
        logger.info(
            "Omitidas %d preguntas de exámenes locales (las importa scripts/etl/import_local_exams.py).",
            skipped_local,
        )
    logger.info("Dump parseado con éxito: %d preguntas en ptype y %d opciones incorrectas.", len(questions), len(inc_rows))
    return questions, incorrectas_by_q


def copy_question_images(repo_root: Path) -> int:
    """Copia las imágenes de preguntas de preparadortai a static/img/questions/ de test-engine."""
    src_dir = repo_root / "apps" / "preparadortai" / "assets" / "img"
    dest_dir = repo_root / "services" / "test-engine" / "presentation" / "static" / "img" / "questions"
    dest_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    if src_dir.is_dir():
        for img_file in src_dir.glob("*.png"):
            # Omitir iconos de interfaz
            if img_file.name in ("add-icon.png", "remove-icon.png"):
                continue
            dest_file = dest_dir / img_file.name
            shutil.copy2(img_file, dest_file)
            copied += 1
        logger.info("Copiadas %d imágenes de preguntas a %s.", copied, dest_dir.relative_to(repo_root))
    else:
        logger.warning("No se encontró el directorio de imágenes en %s.", src_dir)

    return copied


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    dump_path = repo_root / "db" / "local" / "001_preparadortai_dump.sql"
    db_path = repo_root / "services" / "test-engine" / "data" / "test_engine.sqlite"

    if not dump_path.is_file():
        logger.error("No se encontró el dump SQL en: %s", dump_path)
        sys.exit(1)

    if not db_path.is_file():
        logger.error("La base de datos SQLite no existe en: %s. Ejecuta create_schema primero.", db_path)
        sys.exit(1)

    t0 = time.time()
    questions, incorrectas_by_q = parse_mysql_dump(dump_path)

    # 1. Copiar assets/imágenes
    copy_question_images(repo_root)

    # 2. Conectar a SQLite y asegurar temario
    conn = get_db_connection(db_path)
    ensure_syllabus(conn)
    cursor = conn.cursor()

    # 3. Obtener regla de puntuación oficial por defecto
    cursor.execute("SELECT id FROM scoring_rules WHERE code = 'age-oficial-tercio'")
    sr_row = cursor.fetchone()
    scoring_rule_id = sr_row[0] if sr_row else None

    # 4. Crear o resolver exámenes basados en categoria (Decisión a)
    distinct_categories = sorted(list({q["categoria"] for q in questions}))
    logger.info("Registrando %d exámenes/cuestionarios derivados de 'categoria'...", len(distinct_categories))

    exam_id_map: dict[str, int] = {}
    for cat in distinct_categories:
        # Extraer año si está en el texto (ej: "TAI 2024", "CUESTIONARIO 16/TAI")
        year_match = re.search(r"\b(20\d\d)\b", cat)
        if year_match:
            year_val = int(year_match.group(1))
        else:
            short_year = re.search(r"\b(1[4-9]|2[0-4])/TAI", cat)
            year_val = 2000 + int(short_year.group(1)) if short_year else None

        convocatoria_val = None
        if "PI" in cat or "Promoción Interna" in cat:
            convocatoria_val = "Promoción Interna"
        elif "LI" in cat or "Libre" in cat:
            convocatoria_val = "Turno Libre"

        # Buscar o insertar examen
        cursor.execute("SELECT id FROM exams WHERE name = ? AND syllabus_id = ?", (cat, SYLLABUS_ID))
        existing_exam = cursor.fetchone()
        if existing_exam:
            exam_id_map[cat] = existing_exam[0]
        else:
            cursor.execute(
                """
                INSERT INTO exams (name, year, convocatoria, syllabus_id, scoring_rule_id, duration_seconds)
                VALUES (?, ?, ?, ?, ?, NULL)
                """,
                (cat, year_val, convocatoria_val, SYLLABUS_ID, scoring_rule_id),
            )
            exam_id_map[cat] = cursor.lastrowid

    # 5. Pre-cargar preguntas existentes para idempotencia
    cursor.execute("SELECT source_id, id FROM questions WHERE source = ?", (SOURCE_NAME,))
    existing_q_map = {row[0]: row[1] for row in cursor.fetchall()}

    # 6. Inserción de preguntas, opciones, etiquetas de examen y temario
    logger.info("Iniciando inserción transaccional de preguntas TAI en SQLite...")
    conn.commit()  # Asegurar que pasos previos están consolidados

    inserted_questions = 0
    skipped_existing = 0
    inserted_options = 0
    inserted_exam_questions = 0
    inserted_tags = 0
    warnings: list[dict] = []

    # Contador de posición por examen
    exam_position_counter: dict[int, int] = {}

    options_count_distribution: dict[int, int] = {}

    for q in questions:
        q_id_str = str(q["id"])
        incorrect_list = incorrectas_by_q.get(q["id"], [])
        total_options_for_q = len(incorrect_list) + 1  # 1 correcta + N incorrectas
        options_count_distribution[total_options_for_q] = options_count_distribution.get(total_options_for_q, 0) + 1

        if len(incorrect_list) == 0:
            warnings.append({
                "id": q_id_str,
                "reason": "La pregunta no tiene ninguna opción incorrecta en la tabla incorrectas.",
                "question": q,
            })
            continue

        statement = q["pregunta"].strip()
        justification = q["justif"].strip() if q["justif"] else None
        img_path = q["img_path"].strip() if q["img_path"] else None

        has_bloque = q["bloque"] is not None and q["bloque"] > 0
        has_tema = q["tema"] is not None and q["tema"] > 0
        pending_class = 0 if (has_bloque and has_tema) else 1

        if q_id_str in existing_q_map:
            skipped_existing += 1
            db_question_id = existing_q_map[q_id_str]
        else:
            cursor.execute(
                """
                INSERT INTO questions (
                    statement, justification, img_path, source, source_id,
                    is_annulled, annulment_reason, pending_classification
                ) VALUES (?, ?, ?, ?, ?, 0, NULL, ?)
                """,
                (statement, justification, img_path, SOURCE_NAME, q_id_str, pending_class),
            )
            db_question_id = cursor.lastrowid
            existing_q_map[q_id_str] = db_question_id
            inserted_questions += 1

            # MariaDB no guarda el orden A-D original: se baraja de forma determinista
            # por pregunta (mismo orden que aplica scripts/etl/fix_option_order.py).
            n_options = 1 + len(incorrect_list)
            positions = stable_positions(
                f"{SOURCE_NAME}:{q_id_str}", n_options, letter_hint(justification, n_options)
            )
            cursor.execute(
                """
                INSERT INTO question_options (
                    question_id, option_text, is_correct, display_order, justification
                ) VALUES (?, ?, 1, ?, NULL)
                """,
                (db_question_id, q["respuesta"].strip(), positions[0]),
            )
            inserted_options += 1

            for idx, inc in zip(positions[1:], incorrect_list):
                inc_text = inc["respuesta"].strip()
                inc_justif = inc["justif"].strip() if inc["justif"] else None
                cursor.execute(
                    """
                    INSERT INTO question_options (
                        question_id, option_text, is_correct, display_order, justification
                    ) VALUES (?, ?, 0, ?, ?)
                    """,
                    (db_question_id, inc_text, idx, inc_justif),
                )
                inserted_options += 1

        # Vincular a su examen correspondiente (exam_questions)
        exam_id = exam_id_map[q["categoria"]]
        curr_pos = exam_position_counter.get(exam_id, 0) + 1
        exam_position_counter[exam_id] = curr_pos

        cursor.execute(
            """
            INSERT OR IGNORE INTO exam_questions (exam_id, question_id, position)
            VALUES (?, ?, ?)
            """,
            (exam_id, db_question_id, curr_pos),
        )
        if cursor.rowcount > 0:
            inserted_exam_questions += 1

        # Si tiene bloque y tema válidos, insertar etiqueta de temario
        if has_bloque or has_tema:
            block_str = f"B{q['bloque']}" if has_bloque else None
            topic_str = str(q["tema"]) if has_tema else None
            cursor.execute(
                "SELECT id FROM question_syllabus_tags WHERE question_id = ? AND syllabus_id = ?",
                (db_question_id, SYLLABUS_ID),
            )
            if not cursor.fetchone():
                cursor.execute(
                    """
                    INSERT INTO question_syllabus_tags (
                        question_id, syllabus_id, block, topic
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (db_question_id, SYLLABUS_ID, block_str, topic_str),
                )
                inserted_tags += 1

    conn.commit()

    # Guardar advertencias si las hubo
    warnings_file = repo_root / "scripts" / "etl" / "tai_import_warnings.json"
    if warnings:
        with open(warnings_file, "w", encoding="utf-8") as f:
            import json
            json.dump(warnings, f, ensure_ascii=False, indent=2)
        logger.warning("Generado fichero de avisos con %d preguntas: %s", len(warnings), warnings_file.name)
    else:
        logger.info("Cero preguntas descartadas en TAI.")

    # Verificación final
    total_tai_questions = cursor.execute("SELECT COUNT(*) FROM questions WHERE source = ?", (SOURCE_NAME,)).fetchone()[0]
    total_tai_options = cursor.execute(
        "SELECT COUNT(*) FROM question_options WHERE question_id IN (SELECT id FROM questions WHERE source = ?)",
        (SOURCE_NAME,),
    ).fetchone()[0]
    total_img_questions = cursor.execute(
        "SELECT COUNT(*) FROM questions WHERE source = ? AND img_path IS NOT NULL AND TRIM(img_path) != ''",
        (SOURCE_NAME,),
    ).fetchone()[0]
    total_justif_options = cursor.execute(
        "SELECT COUNT(*) FROM question_options WHERE justification IS NOT NULL AND question_id IN (SELECT id FROM questions WHERE source = ?)",
        (SOURCE_NAME,),
    ).fetchone()[0]

    elapsed = time.time() - t0
    logger.info("=" * 65)
    logger.info("RESUMEN DE IMPORTACIÓN DE TAI LEGACY (test_engine.sqlite)")
    logger.info("=" * 65)
    logger.info("Total preguntas leídas en ptype      : %d", len(questions))
    logger.info("Preguntas nuevas insertadas en BD    : %d", inserted_questions)
    logger.info("Preguntas existentes omitidas (dedup): %d", skipped_existing)
    logger.info("Total preguntas TAI en BD            : %d", total_tai_questions)
    logger.info("Total opciones insertadas            : %d", total_tai_options)
    logger.info("Opciones con justificación guardadas : %d", total_justif_options)
    logger.info("Preguntas con imagen (img_path)      : %d", total_img_questions)
    logger.info("Exámenes/Cuestionarios creados       : %d", len(distinct_categories))
    logger.info("Vinculaciones exam_questions         : %d", inserted_exam_questions)
    logger.info("Etiquetas de temario asignadas       : %d", inserted_tags)
    logger.info("Tiempo de importación                : %.2f segundos", elapsed)
    logger.info("=" * 65)
    logger.info("Distribución real de opciones por pregunta:")
    for opt_c, q_c in sorted(options_count_distribution.items()):
        logger.info("  %d opciones en total: %d preguntas", opt_c, q_c)

    # Muestras aleatorias incluyendo una con imagen y otra con justificación
    logger.info("=" * 65)
    logger.info("Muestras aleatorias desde SQLite:")

    # 1. Pregunta con imagen
    img_sample = cursor.execute(
        "SELECT id, statement, source_id, img_path, justification FROM questions WHERE source = ? AND img_path IS NOT NULL LIMIT 1",
        (SOURCE_NAME,),
    ).fetchone()
    if img_sample:
        _print_sample(cursor, img_sample, "Muestra con Imagen")

    # 2. Pregunta con justificación en opciones
    justif_sample = cursor.execute(
        """
        SELECT q.id, q.statement, q.source_id, q.img_path, q.justification
        FROM questions q
        JOIN question_options o ON q.id = o.question_id
        WHERE q.source = ? AND o.justification IS NOT NULL
        LIMIT 1
        """,
        (SOURCE_NAME,),
    ).fetchone()
    if justif_sample:
        _print_sample(cursor, justif_sample, "Muestra con Justificación en opciones")

    # 3. Pregunta aleatoria
    rnd_sample = cursor.execute(
        "SELECT id, statement, source_id, img_path, justification FROM questions WHERE source = ? ORDER BY RANDOM() LIMIT 1",
        (SOURCE_NAME,),
    ).fetchone()
    if rnd_sample:
        _print_sample(cursor, rnd_sample, "Muestra Aleatoria")

    conn.close()
    logger.info("¡Importación de TAI legacy finalizada y verificada con éxito!")


def _print_sample(cursor: sqlite3.Cursor, q_row: tuple, label: str) -> None:
    q_id = q_row[0]
    opt_rows = cursor.execute(
        "SELECT option_text, is_correct, display_order, justification FROM question_options WHERE question_id = ? ORDER BY display_order",
        (q_id,),
    ).fetchall()
    exam_rows = cursor.execute(
        "SELECT e.name, eq.position FROM exams e JOIN exam_questions eq ON e.id = eq.exam_id WHERE eq.question_id = ?",
        (q_id,),
    ).fetchall()
    tag_rows = cursor.execute(
        "SELECT block, topic FROM question_syllabus_tags WHERE question_id = ?",
        (q_id,),
    ).fetchall()

    exam_str = f"Examen: {exam_rows[0][0]} (Posición #{exam_rows[0][1]})" if exam_rows else "Sin examen"
    tag_str = ", ".join(f"Bloque {b} / Tema {t}" for b, t in tag_rows) if tag_rows else "Pendiente de clasificar temario"
    img_str = f" [Imagen: {q_row[3]}]" if q_row[3] else ""

    logger.info("--- %s (ID BD: %d | Source ID: %s | %s | %s)%s ---", label, q_id, q_row[2], exam_str, tag_str, img_str)
    logger.info("Enunciado: %s", q_row[1][:120] + ("..." if len(q_row[1]) > 120 else ""))
    for opt in opt_rows:
        mark = "[CORRECTA]" if opt[1] == 1 else "          "
        just_str = f" (Justif: {opt[3][:60]}...)" if opt[3] else ""
        logger.info("  %s: %s%s", mark, opt[0][:80] + ("..." if len(opt[0]) > 80 else ""), just_str)


if __name__ == "__main__":
    main()
