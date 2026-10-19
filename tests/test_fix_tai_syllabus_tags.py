"""Etiqueta de temario para las preguntas de TAI sin bloque ni tema."""

import contextlib
import io
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "etl"))

import fix_tai_syllabus_tags as fixer  # noqa: E402


class TestFixTaiSyllabusTags(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.db, self.backups = tmp / "te.sqlite", tmp / "backups"
        conn = sqlite3.connect(self.db)
        conn.executescript("""
            CREATE TABLE questions (id INTEGER PRIMARY KEY, source TEXT);
            CREATE TABLE question_syllabus_tags (id INTEGER PRIMARY KEY, question_id INTEGER, syllabus_id TEXT,
                block TEXT, topic TEXT);
            INSERT INTO questions VALUES (1, 'tai-mariadb-legacy'), (2, 'tai-mariadb-legacy'), (3, 'uc3m-a2-gsi');
            INSERT INTO question_syllabus_tags (question_id, syllabus_id, block, topic) VALUES (1, 'tai-legacy', 'B2', '7');
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, *extra):
        argv = ["fix", "--db", str(self.db), "--backup-dir", str(self.backups), *extra]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
            return fixer.main()

    def _tags(self):
        conn = sqlite3.connect(self.db)
        try:
            return conn.execute("SELECT question_id, syllabus_id, block, topic FROM question_syllabus_tags "
                                "ORDER BY question_id").fetchall()
        finally:
            conn.close()

    def test_dry_run_writes_nothing(self):
        self.assertEqual(self._run(), 0)
        self.assertEqual(len(self._tags()), 1)

    def test_apply_tags_only_untagged_tai_questions_and_is_idempotent(self):
        self.assertEqual(self._run("--apply"), 0)
        self.assertEqual(self._tags(), [(1, "tai-legacy", "B2", "7"), (2, "tai-legacy", None, None)])
        self.assertEqual(self._run("--apply"), 0)
        self.assertEqual(len(self._tags()), 2)


if __name__ == "__main__":
    unittest.main()
