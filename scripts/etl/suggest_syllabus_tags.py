#!/usr/bin/env python3
"""
Sugiere y aplica etiquetas de temario (bloque/tema) para preguntas pendientes
en test_engine.sqlite usando búsqueda semántica sobre los apuntes de knowledge/.

Piloto inicial: acotado estrictamente a preguntas de 'age-gsi-official' (101 preguntas
del examen AGE A2 GSI Libre 2024) cruzadas contra los apuntes de 'age/a2-gsi'.

Modo 1: Generar sugerencias (por defecto)
    python scripts/etl/suggest_syllabus_tags.py suggest [sugerencias.csv]

Modo 2: Aplicar lo confirmado
    python scripts/etl/suggest_syllabus_tags.py apply [sugerencias.csv]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

import requests

DEFAULT_DB_PATH = Path("services/test-engine/data/test_engine.sqlite")
DEFAULT_KNOWLEDGE_INDEX = Path("apps/studyassistant/data/knowledge_index.json")
DEFAULT_CHUNKS_PATH = Path("apps/studyassistant/data/semantic_chunks.json")
DEFAULT_EMBEDDINGS_PATH = Path("apps/studyassistant/data/semantic_embeddings.npy")
DEFAULT_OUTPUT_CSV = Path("scripts/etl/suggested_tags_age_gsi_2024.csv")
DEFAULT_EMBEDDINGS_URL = "http://localhost:8091"
DEFAULT_SCORE_THRESHOLD = 0.45
DEFAULT_TOP_K = 15
TARGET_SYLLABUS = "age-gsi-official"
TARGET_PROCESS_PREFIX = "age/a2-gsi"

CSV_FIELDS = [
    "question_id",
    "question_text",
    "suggested_note_id",
    "suggested_official_topic",
    "suggested_heading",
    "score",
    "confirmar",
]


def load_a2_notes_catalog(knowledge_index_path: Path) -> dict[str, dict[str, Any]]:
    """Carga el catálogo de notas que pertenecen a age/a2-gsi desde knowledge_index.json."""
    if not knowledge_index_path.exists():
        raise FileNotFoundError(f"No existe el índice de conocimiento: {knowledge_index_path}")

    with knowledge_index_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    notes = data.get("notes", [])
    a2_notes: dict[str, dict[str, Any]] = {}
    for n in notes:
        procs = n.get("processes", [])
        path = n.get("path", "").replace("\\", "/")
        if TARGET_PROCESS_PREFIX in procs or "knowledge/processes/age/a2-gsi/" in path:
            a2_notes[n["id"]] = n

    return a2_notes


class SemanticSearcher:
    """Realiza búsquedas semánticas intentando primero el servicio HTTP y
    haciendo fallback directo en memoria si el servicio no está corriendo."""

    def __init__(self, embeddings_url: str):
        self.embeddings_url = embeddings_url
        self._local_loaded = False
        self._model = None
        self._chunks: list[dict] = []
        self._embeddings = None
        self.use_http = True
        try:
            resp = requests.get(f"{self.embeddings_url}/health", timeout=1)
            if resp.status_code != 200:
                self.use_http = False
        except Exception:
            self.use_http = False

    def search(self, query: str, top_k: int) -> list[dict]:
        if self.use_http:
            try:
                resp = requests.get(
                    f"{self.embeddings_url}/search",
                    params={"q": query, "top_k": top_k},
                    timeout=3,
                )
                if resp.status_code == 200:
                    return resp.json().get("results", [])
            except Exception:
                self.use_http = False

        return self._search_local(query, top_k)

    def _init_local(self) -> None:
        if self._local_loaded:
            return
        import numpy as np
        from sentence_transformers import SentenceTransformer

        model_name = "paraphrase-multilingual-MiniLM-L12-v2"
        self._model = SentenceTransformer(model_name)

        if DEFAULT_CHUNKS_PATH.exists() and DEFAULT_EMBEDDINGS_PATH.exists():
            self._chunks = json.loads(DEFAULT_CHUNKS_PATH.read_text(encoding="utf-8"))
            vectors = np.load(DEFAULT_EMBEDDINGS_PATH).astype(np.float32)
            norms = np.linalg.norm(vectors, axis=1, keepdims=True)
            norms[norms == 0] = 1e-8
            self._embeddings = vectors / norms
        else:
            self._chunks = []
            self._embeddings = np.zeros((0, 384), dtype=np.float32)
        self._local_loaded = True

    def _search_local(self, query: str, top_k: int) -> list[dict]:
        self._init_local()
        import numpy as np

        if not self._chunks or self._embeddings is None or len(self._embeddings) == 0:
            return []

        query_vector = self._model.encode([query], normalize_embeddings=True)[0].astype(np.float32)
        scores = self._embeddings @ query_vector

        k = min(top_k, len(self._chunks))
        top_indices = np.argsort(-scores)[:k]

        results = []
        for idx in top_indices:
            idx = int(idx)
            chunk = self._chunks[idx]
            results.append({
                "note_id": chunk["note_id"],
                "note_title": chunk.get("note_title", ""),
                "heading": chunk.get("heading") or "",
                "score": round(float(scores[idx]), 4),
            })
        return results


def extract_block_and_topic(official_topic: str | None, note_id: str | None = None) -> tuple[str | None, str | None]:
    """Extrae bloque y número de tema de cadenas como:
    - 'TEMA III.12 APLICACIONES WEB...' -> ('III', '12')
    - 'III.12. APLICACIONES WEB...'     -> ('III', '12')
    - 'Tema I.02 Derecho Constitucional' -> ('I', '2')
    - 'I.01_DerechoConstitucional'      -> ('I', '1')
    - 'TEMA III.3 ESTRATEGIAS...'       -> ('III', '3')
    Si official_topic está vacío, prueba con note_id (ej. 'Tema III.08_Mantenimiento-SW_gem' -> ('III', '8')).
    Si no tiene formato numérico limpio (ej. 'ESQUEMA NACIONAL DE SEGURIDAD', 'ens'), retorna (None, None).
    """
    for candidate in [official_topic, note_id]:
        if not candidate:
            continue
        match = re.search(r"(?:TEMA\s+)?([IVX]+)[._\s]+(\d+)", candidate, re.IGNORECASE)
        if match:
            block = match.group(1).upper()
            topic_num = str(int(match.group(2)))
            return block, topic_num

    return None, None


def cmd_suggest(args: argparse.Namespace) -> None:
    db_path = Path(args.db_path)
    if not db_path.exists():
        raise FileNotFoundError(f"No existe la base de datos: {db_path}")

    a2_notes = load_a2_notes_catalog(Path(args.knowledge_index))
    print(f"Catálogo A2-GSI cargado: {len(a2_notes)} notas válidas de referencia.", flush=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT q.id, q.statement
        FROM questions q
        JOIN question_syllabus_tags t ON q.id = t.question_id
        WHERE t.syllabus_id = ?
          AND q.pending_classification = 1
        ORDER BY q.id
    """, (TARGET_SYLLABUS,))
    questions = cursor.fetchall()
    conn.close()

    total_questions = len(questions)
    print(f"Total preguntas leídas ({TARGET_SYLLABUS}, pendientes): {total_questions}", flush=True)

    if args.sample and args.sample > 0:
        questions = questions[:args.sample]
        print(f"Modo muestra activo: procesando {len(questions)} preguntas.", flush=True)

    searcher = SemanticSearcher(args.embeddings_url)

    rows_to_write: list[dict[str, Any]] = []
    scores_with_candidate: list[float] = []
    count_with_candidate = 0
    count_without_candidate = 0

    for i, q in enumerate(questions, 1):
        q_id = q["id"]
        q_text = (q["statement"] or "").strip()
        preview_text = (q_text[:147] + "...") if len(q_text) > 150 else q_text

        raw_results = searcher.search(q_text, top_k=args.top_k)

        valid_candidates = []
        for r in raw_results:
            note_id = r.get("note_id")
            if note_id in a2_notes:
                r["official_topic"] = a2_notes[note_id].get("official_topic") or ""
                valid_candidates.append(r)

        best_candidate = None
        if valid_candidates:
            top_cand = valid_candidates[0]
            if top_cand["score"] >= args.threshold:
                best_candidate = top_cand

        if best_candidate:
            count_with_candidate += 1
            scores_with_candidate.append(best_candidate["score"])
            rows_to_write.append({
                "question_id": q_id,
                "question_text": preview_text.replace("\n", " "),
                "suggested_note_id": best_candidate["note_id"],
                "suggested_official_topic": best_candidate["official_topic"],
                "suggested_heading": best_candidate["heading"],
                "score": f"{best_candidate['score']:.4f}",
                "confirmar": "",
            })
        else:
            count_without_candidate += 1
            rows_to_write.append({
                "question_id": q_id,
                "question_text": preview_text.replace("\n", " "),
                "suggested_note_id": "",
                "suggested_official_topic": "",
                "suggested_heading": "",
                "score": "",
                "confirmar": "",
            })

        if i % 25 == 0 or i == len(questions):
            print(f"Progreso: {i}/{len(questions)} procesadas...", flush=True)

    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows_to_write)

    print("\n" + "=" * 55, flush=True)
    print("RESUMEN DE SUGERENCIAS (PILOTO AGE GSI 2024)", flush=True)
    print("=" * 55, flush=True)
    print(f"Preguntas procesadas: {len(questions)} (100% de {TARGET_SYLLABUS})", flush=True)
    print(f"Con candidato válido (score >= {args.threshold}): {count_with_candidate}", flush=True)
    print(f"Sin candidato válido: {count_without_candidate}", flush=True)

    if scores_with_candidate:
        score_max = max(scores_with_candidate)
        score_min = min(scores_with_candidate)
        score_avg = sum(scores_with_candidate) / len(scores_with_candidate)
        print("Distribución de scores (con candidato):", flush=True)
        print(f"  - Máximo: {score_max:.4f}", flush=True)
        print(f"  - Mínimo: {score_min:.4f}", flush=True)
        print(f"  - Media:  {score_avg:.4f}", flush=True)
    print(f"Fichero generado: {output_path}", flush=True)
    print("=" * 55, flush=True)
    print("Instrucciones de revisión:", flush=True)
    print('1. Abre el CSV y escribe "si" en la columna "confirmar" para las que aceptes.', flush=True)
    print(f"2. Para aplicar: python scripts/etl/suggest_syllabus_tags.py apply {output_path}", flush=True)


def cmd_apply(args: argparse.Namespace) -> None:
    csv_path = Path(args.output_csv)
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe el fichero CSV: {csv_path}")

    db_path = Path(args.db_path)
    if not db_path.exists():
        raise FileNotFoundError(f"No existe la base de datos: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    applied_count = 0
    skipped_count = 0
    no_clean_topic_count = 0
    unclean_topics_list: list[tuple[int, str]] = []

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            conf = (row.get("confirmar") or "").strip().lower()
            if conf not in {"si", "sí", "yes", "y"}:
                skipped_count += 1
                continue

            q_id = int(row["question_id"])
            official_topic = row.get("suggested_official_topic") or ""
            note_id = row.get("suggested_note_id") or ""

            block, topic_num = extract_block_and_topic(official_topic, note_id)

            if topic_num is None:
                no_clean_topic_count += 1
                unclean_topics_list.append((q_id, official_topic or note_id))
                cursor.execute("""
                    UPDATE question_syllabus_tags
                    SET block = ?, topic = NULL
                    WHERE question_id = ? AND syllabus_id = ?
                """, (block, q_id, TARGET_SYLLABUS))
            else:
                cursor.execute("""
                    UPDATE question_syllabus_tags
                    SET block = ?, topic = ?
                    WHERE question_id = ? AND syllabus_id = ?
                """, (block, topic_num, q_id, TARGET_SYLLABUS))

            cursor.execute("""
                UPDATE questions
                SET pending_classification = 0
                WHERE id = ?
            """, (q_id,))
            applied_count += 1

    conn.commit()
    conn.close()

    print("\n" + "=" * 55, flush=True)
    print("RESUMEN DE APLICACIÓN", flush=True)
    print("=" * 55, flush=True)
    print(f"Total confirmadas y aplicadas: {applied_count}", flush=True)
    print(f"Omitidas (sin confirmación):   {skipped_count}", flush=True)
    if no_clean_topic_count > 0:
        print(f"Aviso: {no_clean_topic_count} preguntas tenían official_topic sin número de tema limpio:", flush=True)
        for q_id, ot in unclean_topics_list:
            print(f"  - Pregunta ID {q_id}: '{ot}' (se dejó topic=NULL)", flush=True)
    print("=" * 55, flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sugiere y aplica clasificación de temario para AGE GSI 2024."
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["suggest", "apply"],
        default="suggest",
        help="Modo de ejecución: 'suggest' genera el CSV; 'apply' aplica las confirmadas.",
    )
    parser.add_argument(
        "output_csv",
        nargs="?",
        default=str(DEFAULT_OUTPUT_CSV),
        help=f"Ruta del CSV (por defecto: {DEFAULT_OUTPUT_CSV})",
    )
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--knowledge-index", default=str(DEFAULT_KNOWLEDGE_INDEX))
    parser.add_argument("--embeddings-url", default=DEFAULT_EMBEDDINGS_URL)
    parser.add_argument("--threshold", type=float, default=DEFAULT_SCORE_THRESHOLD)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--sample", type=int, default=None, help="Limitar a N preguntas de prueba")

    args = parser.parse_args()

    if args.mode == "apply":
        cmd_apply(args)
    else:
        cmd_suggest(args)


if __name__ == "__main__":
    main()
