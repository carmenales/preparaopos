"""Backfill de año y marca de examen oficial de PreparaTIC."""

import contextlib
import io
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ETL_DIR = Path(__file__).resolve().parent.parent / "scripts" / "etl"
sys.path.insert(0, str(ETL_DIR))

import backfill_preparatic_metadata as backfill  # noqa: E402
from import_preparatic import SOURCE_NAME, parse_question_metadata  # noqa: E402


class TestParseQuestionMetadata(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_question_metadata({"year": "2023", "exam": True}), (2023, True))
        self.assertEqual(parse_question_metadata({"year": "2002"}), (2002, False))
        self.assertEqual(parse_question_metadata({"year": "", "exam": None}), (None, False))
        self.assertEqual(parse_question_metadata({"year": "20xx"}), (None, False))


class TestBackfill(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.db = tmp / "te.sqlite"
        self.bundle = tmp / "bundle.json"
        self.backups = tmp / "backups"

        conn = sqlite3.connect(self.db)
        conn.execute("CREATE TABLE questions (id INTEGER PRIMARY KEY, statement TEXT, source TEXT, source_id TEXT)")
        conn.executemany(
            "INSERT INTO questions VALUES (?, ?, ?, ?)",
            [
                (1, "a", SOURCE_NAME, "100"),
                (2, "b", SOURCE_NAME, "101"),
                (3, "c", "tai-mariadb-legacy", "100"),  # otra fuente con el mismo source_id
            ],
        )
        conn.commit()
        conn.close()
        self._write_bundle([{"id": "100", "year": "2023", "exam": True}, {"id": "101", "year": "2002"}])

    def tearDown(self):
        self._tmp.cleanup()

    def _write_bundle(self, questions):
        self.bundle.write_text(json.dumps(questions), encoding="utf-8")

    def _run(self, *extra):
        argv = ["backfill", "--db", str(self.db), "--bundle", str(self.bundle), "--backup-dir", str(self.backups), *extra]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return backfill.main()

    def _rows(self):
        conn = sqlite3.connect(self.db)
        try:
            return conn.execute("SELECT id, statement, year, is_official_exam FROM questions ORDER BY id").fetchall()
        finally:
            conn.close()

    def _backups(self):
        return list(self.backups.glob("*.sqlite")) if self.backups.exists() else []

    def test_dry_run_writes_nothing(self):
        before = self.db.read_bytes()
        self.assertEqual(self._run(), 0)
        self.assertEqual(self.db.read_bytes(), before)
        self.assertEqual(self._backups(), [])

    def test_apply_backfills_only_preparatic_rows_and_is_idempotent(self):
        self.assertEqual(self._run("--apply"), 0)
        self.assertEqual(self._rows(), [(1, "a", 2023, 1), (2, "b", 2002, 0), (3, "c", None, 0)])
        self.assertEqual(len(self._backups()), 1)

        self.assertEqual(self._run("--apply"), 0)
        self.assertEqual(len(self._backups()), 1)

    def test_aborts_when_db_question_missing_from_bundle(self):
        self._write_bundle([{"id": "100", "year": "2023", "exam": True}])
        before = self.db.read_bytes()
        self.assertEqual(self._run("--apply"), 1)
        self.assertEqual(self.db.read_bytes(), before)
        self.assertEqual(self._backups(), [])


if __name__ == "__main__":
    unittest.main()
