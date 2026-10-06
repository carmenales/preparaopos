#!/usr/bin/env python3
"""Sugerencia semántica de enlaces pregunta-apunte (Vía b).

Se ejecuta únicamente para aquellas preguntas que la resolución por tema (Vía a)
no haya resuelto (0 coincidencias).
Sigue el patrón de revisión manual en CSV con columna 'confirmar' vacía.

Uso:
    python suggest_semantic_links.py suggest [output.csv]
    python suggest_semantic_links.py apply [output.csv]
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

# Asegurar importación de linking-service
SERVICE_ROOT = Path(__file__).resolve().parent.parent
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from config import APUNTES_SERVICE_URL, SQLITE_PATH, TEST_ENGINE_URL
from infrastructure.clients.apuntes_client import ApuntesClient
from infrastructure.clients.test_engine_client import TestEngineClient
from infrastructure.db.engine import get_connection, init_db
from infrastructure.db.repository import QuestionNoteLinkRepository

DEFAULT_CSV_PATH = SERVICE_ROOT / "data" / "semantic_link_suggestions.csv"
DEFAULT_EMBEDDINGS_URL = "http://localhost:8091"

CSV_FIELDS = [
    "question_id",
    "question_excerpt",
    "suggested_note_id",
    "suggested_note_title",
    "score",
    "confirmar",
]


def cmd_suggest(
    syllabus_id: str,
    output_csv: Path,
    embeddings_url: str,
    db_path: Path,
    apuntes_url: str,
    test_engine_url: str,
    threshold: float = 0.45,
    top_k: int = 5,
) -> None:
    import requests

    init_db(db_path)
    conn = get_connection(db_path)
    repo = QuestionNoteLinkRepository(conn)
    te_client = TestEngineClient(test_engine_url)
    ap_client = ApuntesClient(apuntes_url)

    # 1. Obtener todas las preguntas del temario
    tags = te_client.get_syllabus_tags(syllabus_id)

    # 2. Identificar preguntas que aún NO tienen ningún enlace en la BD
    unlinked_qids = []
    for t in tags:
        qid = t["question_id"]
        existing = repo.get_by_question_id(qid)
        if not existing:
            unlinked_qids.append(qid)

    print(f"Preguntas del temario '{syllabus_id}' sin enlace: {len(unlinked_qids)}")
    if not unlinked_qids:
        print("Todas las preguntas ya tienen enlaces resueltos. No hay nada pendiente.")
        conn.close()
        return

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    rows_to_write = []

    for qid in unlinked_qids:
        q_data = te_client.get_question(qid)
        statement = q_data.get("statement", "") if q_data else ""
        excerpt = q_data.get("excerpt", "") if q_data else ""

        try:
            resp = requests.get(
                f"{embeddings_url}/search",
                params={"q": statement, "top_k": top_k},
                timeout=5,
            )
            candidates = resp.json().get("results", []) if resp.status_code == 200 else []
        except Exception:
            candidates = []

        best = candidates[0] if (candidates and candidates[0].get("score", 0) >= threshold) else None
        if best:
            note_info = ap_client.get_note(best["note_id"])
            note_title = note_info.get("title", "") if note_info else ""
            rows_to_write.append({
                "question_id": qid,
                "question_excerpt": excerpt.replace("\n", " "),
                "suggested_note_id": best["note_id"],
                "suggested_note_title": note_title,
                "score": f"{best['score']:.4f}",
                "confirmar": "",
            })
        else:
            rows_to_write.append({
                "question_id": qid,
                "question_excerpt": excerpt.replace("\n", " "),
                "suggested_note_id": "",
                "suggested_note_title": "",
                "score": "",
                "confirmar": "",
            })

    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows_to_write)

    conn.close()
    print(f"Generado CSV con {len(rows_to_write)} sugerencias: {output_csv}")
    print("Revisa el CSV, pon 'si' en la columna 'confirmar' y ejecuta el modo 'apply'.")


def cmd_apply(csv_path: Path, db_path: Path, syllabus_id: str) -> None:
    if not csv_path.exists():
        print(f"Error: no existe el fichero {csv_path}", file=sys.stderr)
        sys.exit(1)

    init_db(db_path)
    conn = get_connection(db_path)
    repo = QuestionNoteLinkRepository(conn)

    applied = 0
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            conf = (row.get("confirmar") or "").strip().lower()
            if conf in {"si", "sí", "yes", "y"} and row.get("suggested_note_id"):
                qid = int(row["question_id"])
                note_id = row["suggested_note_id"]
                score = float(row["score"]) if row.get("score") else 0.7
                repo.upsert_link(
                    question_id=qid,
                    note_id=note_id,
                    syllabus_id=syllabus_id,
                    confidence=score,
                    source="semantic-suggestion",
                )
                applied += 1

    conn.close()
    print(f"Aplicados {applied} enlaces confirmados manualmente en linking.sqlite.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sugerencias semánticas de enlaces.")
    parser.add_argument("mode", choices=["suggest", "apply"], default="suggest", nargs="?")
    parser.add_argument("output_csv", nargs="?", default=str(DEFAULT_CSV_PATH))
    parser.add_argument("--syllabus-id", default="age-gsi-official")
    parser.add_argument("--embeddings-url", default=DEFAULT_EMBEDDINGS_URL)
    parser.add_argument("--db-path", default=str(SQLITE_PATH))
    parser.add_argument("--apuntes-url", default=APUNTES_SERVICE_URL)
    parser.add_argument("--test-engine-url", default=TEST_ENGINE_URL)

    args = parser.parse_args()

    if args.mode == "apply":
        cmd_apply(Path(args.output_csv), Path(args.db_path), args.syllabus_id)
    else:
        cmd_suggest(
            syllabus_id=args.syllabus_id,
            output_csv=Path(args.output_csv),
            embeddings_url=args.embeddings_url,
            db_path=Path(args.db_path),
            apuntes_url=args.apuntes_url,
            test_engine_url=args.test_engine_url,
        )


if __name__ == "__main__":
    main()
