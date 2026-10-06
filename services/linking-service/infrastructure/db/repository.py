"""Repositorio de question_note_links sobre SQLite."""

from __future__ import annotations

import sqlite3
from typing import Any


class QuestionNoteLinkRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

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
                source = excluded.source;
            """,
            (question_id, note_id, syllabus_id, confidence, source),
        )
        self._conn.commit()

    def get_by_question_id(self, question_id: int) -> list[dict[str, Any]]:
        """Devuelve los enlaces registrados para una pregunta."""
        cur = self._conn.cursor()
        cur.execute(
            """
            SELECT id, question_id, note_id, syllabus_id, confidence, source, created_at
            FROM question_note_links
            WHERE question_id = ?
            ORDER BY confidence DESC, note_id ASC;
            """,
            (question_id,),
        )
        return [dict(row) for row in cur.fetchall()]

    def get_by_note_id(self, note_id: str) -> list[dict[str, Any]]:
        """Devuelve los enlaces registrados para un apunte."""
        cur = self._conn.cursor()
        cur.execute(
            """
            SELECT id, question_id, note_id, syllabus_id, confidence, source, created_at
            FROM question_note_links
            WHERE note_id = ?
            ORDER BY confidence DESC, question_id ASC;
            """,
            (note_id,),
        )
        return [dict(row) for row in cur.fetchall()]

    def count(self) -> int:
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM question_note_links;")
        return cur.fetchone()[0]

    def list_all(self) -> list[dict[str, Any]]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM question_note_links ORDER BY question_id, note_id;")
        return [dict(row) for row in cur.fetchall()]
