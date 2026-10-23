"""Repositorio de question_note_links sobre SQLite."""

from __future__ import annotations

import sqlite3
from typing import Any


# Un enlace retirado a mano se conserva como «lápida» (source = 'removed') para que
# scripts/resolve_links.py no lo vuelva a crear; las lecturas lo ignoran.
REMOVED = "removed"
MANUAL = "manual"


class QuestionNoteLinkRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._conn.row_factory = sqlite3.Row

    def upsert_link(
        self,
        *,
        question_id: int,
        note_id: str,
        syllabus_id: str,
        confidence: float | None,
        source: str,
    ) -> None:
        """Inserta o actualiza un enlace entre pregunta y apunte."""
        cur = self._conn.cursor()
        cur.execute(
            """
            INSERT INTO question_note_links (
                question_id, note_id, syllabus_id, confidence, source
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(question_id, note_id) DO UPDATE SET
                confidence = excluded.confidence,
                source = excluded.source
            WHERE question_note_links.source NOT IN ('removed', 'manual');
            """,
            (question_id, note_id, syllabus_id, confidence, source),
        )
        self._conn.commit()

    def set_manual_link(self, *, question_id: int, note_id: str, syllabus_id: str) -> None:
        """Enlace añadido a mano: confianza 1.0 y prevalece sobre una lápida o un enlace automático."""
        self._conn.execute(
            """
            INSERT INTO question_note_links (question_id, note_id, syllabus_id, confidence, source)
            VALUES (?, ?, ?, 1.0, 'manual')
            ON CONFLICT(question_id, note_id) DO UPDATE SET
                confidence = 1.0, source = 'manual', syllabus_id = excluded.syllabus_id;
            """,
            (question_id, note_id, syllabus_id),
        )
        self._conn.commit()

    def remove_link(self, question_id: int, note_id: str) -> bool:
        """Retira un enlace activo dejando una lápida. Devuelve si había un enlace activo."""
        cur = self._conn.execute(
            "UPDATE question_note_links SET source = 'removed' "
            "WHERE question_id = ? AND note_id = ? AND source != 'removed'",
            (question_id, note_id),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def get_by_question_id(self, question_id: int) -> list[dict[str, Any]]:
        """Devuelve los enlaces registrados para una pregunta."""
        cur = self._conn.cursor()
        cur.execute(
            """
            SELECT id, question_id, note_id, syllabus_id, confidence, source, created_at
            FROM question_note_links
            WHERE source != 'removed' AND question_id = ?
            ORDER BY confidence DESC, note_id ASC;
            """,
            (question_id,),
        )
        return [dict(row) for row in cur.fetchall()]

    def get_by_question_ids(self, question_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
        """Devuelve los enlaces registrados para una lista de preguntas."""
        if not question_ids:
            return {}
        placeholders = ",".join("?" for _ in question_ids)
        cur = self._conn.cursor()
        cur.execute(
            f"""
            SELECT id, question_id, note_id, syllabus_id, confidence, source, created_at
            FROM question_note_links
            WHERE source != 'removed' AND question_id IN ({placeholders})
            ORDER BY question_id ASC, confidence DESC, note_id ASC;
            """,
            question_ids,
        )
        res: dict[int, list[dict[str, Any]]] = {qid: [] for qid in question_ids}
        for row in cur.fetchall():
            d = dict(row)
            res[d["question_id"]].append(d)
        return res

    def get_by_note_id(self, note_id: str) -> list[dict[str, Any]]:
        """Devuelve los enlaces registrados para un apunte."""
        cur = self._conn.cursor()
        cur.execute(
            """
            SELECT id, question_id, note_id, syllabus_id, confidence, source, created_at
            FROM question_note_links
            WHERE source != 'removed' AND note_id = ?
            ORDER BY confidence DESC, question_id ASC;
            """,
            (note_id,),
        )
        return [dict(row) for row in cur.fetchall()]

    def count(self) -> int:
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM question_note_links WHERE source != 'removed';")
        return cur.fetchone()[0]

    def list_all(self) -> list[dict[str, Any]]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM question_note_links ORDER BY question_id, note_id;")
        return [dict(row) for row in cur.fetchall()]
