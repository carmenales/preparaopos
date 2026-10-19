"""La BD existente recibe las columnas nuevas sin perder datos."""

from __future__ import annotations

import sqlite3

from infrastructure.db.engine import create_sqlite_engine, ensure_additive_columns, init_schema


def _legacy_db(path):
    conn = sqlite3.connect(path)
    conn.execute(
        """CREATE TABLE questions (
            id INTEGER PRIMARY KEY, statement TEXT NOT NULL, justification TEXT,
            img_path VARCHAR(255), source VARCHAR(32) NOT NULL, source_id VARCHAR(64) NOT NULL,
            is_annulled BOOLEAN NOT NULL, annulment_reason TEXT,
            pending_classification BOOLEAN NOT NULL)"""
    )
    conn.execute(
        "INSERT INTO questions VALUES (7, '¿Pregunta?', NULL, NULL, 'preparatic-bundle-2026', '16628', 0, NULL, 0)"
    )
    conn.commit()
    conn.close()


def test_init_schema_adds_missing_columns_and_keeps_rows(tmp_path):
    db = tmp_path / "legacy.sqlite"
    _legacy_db(db)

    engine = create_sqlite_engine(db, journal_mode="DELETE")
    init_schema(engine)
    engine.dispose()

    conn = sqlite3.connect(db)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(questions)")}
    row = conn.execute("SELECT id, statement, year, is_official_exam FROM questions").fetchone()
    conn.close()

    assert {"year", "is_official_exam"} <= columns
    assert row == (7, "¿Pregunta?", None, 0)


def test_ensure_additive_columns_is_idempotent(tmp_path):
    db = tmp_path / "legacy.sqlite"
    _legacy_db(db)
    engine = create_sqlite_engine(db, journal_mode="DELETE")

    assert sorted(ensure_additive_columns(engine)) == ["questions.is_official_exam", "questions.year"]
    assert ensure_additive_columns(engine) == []
    engine.dispose()
