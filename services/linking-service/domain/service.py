"""Servicio de dominio para resolución y consulta de enlaces pregunta-apunte."""

from __future__ import annotations

import re
from typing import Any

from infrastructure.clients.apuntes_client import ApuntesClient
from infrastructure.clients.test_engine_client import TestEngineClient
from infrastructure.db.repository import QuestionNoteLinkRepository


def extract_block_and_topic(
    official_topic: str | None, note_id: str | None = None
) -> tuple[str | None, str | None]:
    """Extrae bloque y número de tema de cadenas de texto.

    Función probada contra datos reales en suggest_syllabus_tags.py.
    Ejemplos:
    - 'TEMA III.12 APLICACIONES WEB...' -> ('III', '12')
    - 'Tema I.02 Derecho Constitucional' -> ('I', '2')
    - 'I.01_DerechoConstitucional'      -> ('I', '1')
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


class LinkingService:
    def __init__(
        self,
        repo: QuestionNoteLinkRepository,
        apuntes_client: ApuntesClient,
        test_engine_client: TestEngineClient,
    ) -> None:
        self._repo = repo
        self._apuntes_client = apuntes_client
        self._test_engine_client = test_engine_client

    def resolve_topic_matches(
        self,
        *,
        syllabus_id: str,
        process_slug: str,
    ) -> dict[str, Any]:
        """Vía (a): Resolución automática por coincidencia de tema (alta confianza).

        1. Pide a test-engine las preguntas y tags de syllabus_id.
        2. Pide a apuntes-service el catálogo de notas de process_slug.
        3. Compara block y topic mediante extract_block_and_topic:
           - 1 match exacto  -> confidence=1.0, source='topic-match'
           - Varios matches  -> vincula a todos, confidence=0.8, source='topic-match'
           - 0 matches       -> registrado para sugerencia semántica
        """
        # 1. Obtener tags de preguntas desde test-engine vía HTTP
        tags = self._test_engine_client.get_syllabus_tags(syllabus_id)

        # 2. Obtener catálogo de notas desde apuntes-service vía HTTP
        notes = self._apuntes_client.get_notes_by_process(process_slug)

        # 3. Indexar notas por (bloque, número_tema)
        notes_by_bt: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for n in notes:
            b, t = extract_block_and_topic(n.get("official_topic"), n.get("id"))
            if b and t:
                notes_by_bt.setdefault((b, t), []).append(n)

        # 4. Procesar preguntas con tema no nulo
        total_evaluated = 0
        exact_matches = 0
        multi_matches = 0
        zero_matches = 0
        zero_questions: list[dict[str, Any]] = []
        links_created = 0

        for row in tags:
            q_id = row["question_id"]
            block = row.get("block")
            topic = row.get("topic")

            if not topic:
                continue

            total_evaluated += 1

            clean_b = block.upper() if block else None
            clean_t = str(int(topic)) if (str(topic).isdigit()) else str(topic)

            candidates = notes_by_bt.get((clean_b, clean_t), [])

            if len(candidates) == 1:
                exact_matches += 1
                c = candidates[0]
                self._repo.upsert_link(
                    question_id=q_id,
                    note_id=c["id"],
                    syllabus_id=syllabus_id,
                    confidence=1.0,
                    source="topic-match",
                )
                links_created += 1
            elif len(candidates) > 1:
                multi_matches += 1
                for c in candidates:
                    self._repo.upsert_link(
                        question_id=q_id,
                        note_id=c["id"],
                        syllabus_id=syllabus_id,
                        confidence=0.8,
                        source="topic-match",
                    )
                    links_created += 1
            else:
                zero_matches += 1
                zero_questions.append({
                    "question_id": q_id,
                    "block": block,
                    "topic": topic,
                })

        return {
            "syllabus_id": syllabus_id,
            "process_slug": process_slug,
            "total_evaluated": total_evaluated,
            "exact_matches": exact_matches,
            "multi_matches": multi_matches,
            "zero_matches": zero_matches,
            "zero_questions": zero_questions,
            "links_created": links_created,
        }

    def get_links_by_question(self, question_id: int) -> list[dict[str, Any]]:
        """Devuelve los enlaces para una pregunta enriquecidos con datos de la nota."""
        links = self._repo.get_by_question_id(question_id)
        results = []
        for l in links:
            note = self._apuntes_client.get_note(l["note_id"])
            title = note.get("title") if note else l["note_id"]
            official_topic = note.get("official_topic") if note else None
            results.append({
                "note_id": l["note_id"],
                "title": title,
                "official_topic": official_topic,
                "confidence": l["confidence"],
            })
        return results

    def get_links_by_note(self, note_id: str) -> list[dict[str, Any]]:
        """Devuelve los enlaces para un apunte enriquecidos con datos de la pregunta."""
        links = self._repo.get_by_note_id(note_id)
        results = []
        for l in links:
            q = self._test_engine_client.get_question(l["question_id"])
            text_excerpt = q.get("excerpt") if q else ""
            exam_name = q.get("exam_name") if q else None
            results.append({
                "question_id": l["question_id"],
                "text_excerpt": text_excerpt,
                "exam_name": exam_name,
                "confidence": l["confidence"],
            })
        return results
