#!/usr/bin/env python3
"""
Sugiere enlaces entre (categoria, bloque, tema) de preparadortai y apuntes
de knowledge/, usando el servicio de búsqueda semántica que ya existe
(services/embeddings). No escribe en question_topic_links directamente —
saca un CSV para que lo revises, y solo inserta lo que confirmes ahí.

Modo 1: generar sugerencias
    python3 scripts/suggest_topic_links.py suggest sugerencias.csv

Revisa el CSV, añade "si"/"no" en la columna `confirmar` de las filas que
quieras aceptar (todo lo demás se ignora).

Modo 2: aplicar lo confirmado
    python3 scripts/suggest_topic_links.py apply sugerencias.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import pymysql
import requests

DEFAULT_DB_HOST = "127.0.0.1"
DEFAULT_DB_PORT = 3307  # puerto expuesto en docker-compose.yml para el servicio "db"
DEFAULT_DB_USER = "preparaopos"
DEFAULT_DB_PASSWORD = "preparaopos"
DEFAULT_DB_NAME = "preparadortai"
DEFAULT_EMBEDDINGS_URL = "http://localhost:8091"
DEFAULT_SCORE_THRESHOLD = 0.45
DEFAULT_TOP_K = 5
SAMPLE_QUESTIONS_PER_TOPIC = 3

CSV_FIELDS = [
    "categoria", "bloque", "tema", "attempts_count", "sample_question",
    "suggested_note_id", "suggested_note_title", "suggested_heading",
    "score", "confirmar",
]


def connect_db(host: str, port: int, user: str, password: str, database: str):
    return pymysql.connect(
        host=host, port=port, user=user, password=password,
        database=database, charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
    )


def fetch_existing_links(conn) -> set[tuple[str, int | None, int | None]]:
    with conn.cursor() as cursor:
        cursor.execute("SELECT categoria, bloque, tema FROM question_topic_links")
        rows = cursor.fetchall()
    return {(row["categoria"], row["bloque"], row["tema"]) for row in rows}


def fetch_unlinked_topics(conn) -> list[dict]:
    """Combinaciones (categoria, bloque, tema) con al menos un intento,
    junto con el número de intentos — para poder priorizar por relevancia
    (más intentos = más vale la pena tener el enlace bien puesto)."""
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT categoria, bloque, tema, COUNT(*) AS attempts_count
            FROM test_attempts
            WHERE categoria IS NOT NULL AND categoria <> ''
            GROUP BY categoria, bloque, tema
            ORDER BY attempts_count DESC
        """)
        return cursor.fetchall()


def fetch_sample_questions(conn, categoria: str, bloque: int | None, tema: int | None, limit: int) -> list[str]:
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT ptype.pregunta
            FROM test_attempts ta
            JOIN ptype ON ptype.id = ta.question_id
            WHERE ta.categoria = %s
              AND (ta.bloque <=> %s)
              AND (ta.tema <=> %s)
              AND ptype.pregunta IS NOT NULL
              AND ptype.pregunta <> ''
            LIMIT %s
        """, (categoria, bloque, tema, limit))
        rows = cursor.fetchall()
    return [row["pregunta"] for row in rows]


def search_semantic(embeddings_url: str, query: str, top_k: int) -> list[dict]:
    response = requests.get(
        f"{embeddings_url}/search",
        params={"q": query, "top_k": top_k},
        timeout=15,
    )
    response.raise_for_status()
    return response.json().get("results", [])


def cmd_suggest(args: argparse.Namespace) -> None:
    conn = connect_db(args.db_host, args.db_port, args.db_user, args.db_password, args.db_name)

    existing_links = fetch_existing_links(conn)
    topics = fetch_unlinked_topics(conn)

    rows_to_write = []
    skipped_no_questions = 0
    skipped_already_linked = 0

    for topic in topics:
        key = (topic["categoria"], topic["bloque"], topic["tema"])
        if key in existing_links:
            skipped_already_linked += 1
            continue

        sample_questions = fetch_sample_questions(
            conn, topic["categoria"], topic["bloque"], topic["tema"], SAMPLE_QUESTIONS_PER_TOPIC
        )
        if not sample_questions:
            skipped_no_questions += 1
            continue

        query_text = " ".join(sample_questions)[:1000]

        try:
            results = search_semantic(args.embeddings_url, query_text, args.top_k)
        except requests.RequestException as error:
            print(f"[error] No se pudo consultar el servicio de embeddings para "
                  f"{topic['categoria']}/{topic['bloque']}/{topic['tema']}: {error}", file=sys.stderr)
            continue

        if not results:
            continue

        best = results[0]
        if best["score"] < args.threshold:
            continue

        rows_to_write.append({
            "categoria": topic["categoria"],
            "bloque": topic["bloque"] if topic["bloque"] is not None else "",
            "tema": topic["tema"] if topic["tema"] is not None else "",
            "attempts_count": topic["attempts_count"],
            "sample_question": sample_questions[0][:200],
            "suggested_note_id": best["note_id"],
            "suggested_note_title": best["note_title"],
            "suggested_heading": best.get("heading") or "",
            "score": best["score"],
            "confirmar": "",
        })

    conn.close()

    output_path = Path(args.output_csv)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows_to_write)

    print(f"Sugerencias escritas en: {output_path}")
    print(f"Total: {len(rows_to_write)} sugerencias · "
          f"{skipped_already_linked} ya enlazados · "
          f"{skipped_no_questions} sin preguntas de muestra")
    print(f'Revisa el CSV y escribe "si" en la columna "confirmar" de las filas que quieras aplicar, '
          f'luego ejecuta: python3 scripts/suggest_topic_links.py apply {output_path}')


def cmd_apply(args: argparse.Namespace) -> None:
    input_path = Path(args.output_csv)
    if not input_path.exists():
        raise FileNotFoundError(f"No existe el fichero: {input_path}")

    conn = connect_db(args.db_host, args.db_port, args.db_user, args.db_password, args.db_name)
    applied = 0
    skipped = 0

    with input_path.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        with conn.cursor() as cursor:
            for row in reader:
                if row.get("confirmar", "").strip().lower() not in {"si", "sí", "yes", "y"}:
                    skipped += 1
                    continue

                bloque = int(row["bloque"]) if row["bloque"] else None
                tema = int(row["tema"]) if row["tema"] else None

                cursor.execute("""
                    INSERT IGNORE INTO question_topic_links (categoria, bloque, tema, knowledge_note_id)
                    VALUES (%s, %s, %s, %s)
                """, (row["categoria"], bloque, tema, row["suggested_note_id"]))
                applied += 1

    conn.commit()
    conn.close()

    print(f"Aplicados: {applied} · Omitidos (sin confirmar): {skipped}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sugiere y aplica enlaces pregunta-apunte vía búsqueda semántica.")
    parser.add_argument("mode", choices=["suggest", "apply"])
    parser.add_argument("output_csv", help="Ruta del CSV de sugerencias (se lee o se escribe según el modo)")
    parser.add_argument("--db-host", default=DEFAULT_DB_HOST)
    parser.add_argument("--db-port", type=int, default=DEFAULT_DB_PORT)
    parser.add_argument("--db-user", default=DEFAULT_DB_USER)
    parser.add_argument("--db-password", default=DEFAULT_DB_PASSWORD)
    parser.add_argument("--db-name", default=DEFAULT_DB_NAME)
    parser.add_argument("--embeddings-url", default=DEFAULT_EMBEDDINGS_URL)
    parser.add_argument("--threshold", type=float, default=DEFAULT_SCORE_THRESHOLD)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)

    args = parser.parse_args()

    if args.mode == "suggest":
        cmd_suggest(args)
    else:
        cmd_apply(args)


if __name__ == "__main__":
    main()