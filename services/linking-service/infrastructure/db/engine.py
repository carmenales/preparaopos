"""Conexión SQLite y creación de esquema propio de linking-service."""

from __future__ import annotations

import sqlite3
from pathlib import Path


def init_db(db_path: Path) -> None:
    """Crea el directorio y las tablas de linking.sqlite si no existen."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS question_note_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                note_id TEXT NOT NULL,
                syllabus_id TEXT NOT NULL,
                confidence REAL,
                source TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(question_id, note_id)
            );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_qnl_question_id ON question_note_links(question_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_qnl_note_id ON question_note_links(note_id);")
        conn.commit()
    finally:
        conn.close()


def get_connection(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
