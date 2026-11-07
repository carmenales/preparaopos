"""Marca de examen oficial y año en las preguntas de GSI 2024."""

import contextlib
import io
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "etl"))

import fix_gsi_official_flag as fixer  # noqa: E402


class TestFixGsiOfficialFlag(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.db, self.backups = tmp / "te.sqlite", tmp / "backups"
        conn = sqlite3.connect(self.db)
        conn.executescript("""
            CREATE TABLE questions (id INTEGER PRIMARY KEY, source TEXT, year INTEGER, is_official_exam INTEGER);
            INSERT INTO questions VALUES (1, 'age-gsi-2024', NULL, 0), (2, 'age-gsi-2024', NULL, 0),
                (3, 'tai-mariadb-legacy', NULL, 0), (4, 'preparatic-bundle-2026', 2019, 1);
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, *extra):
        argv = ["fix", "--db", str(self.db), "--backup-dir", str(self.backups), *extra]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
            return fixer.main()

    def _rows(self):
        conn = sqlite3.connect(self.db)
        try:
            return {r[0]: (r[1], r[2]) for r in conn.execute("SELECT id, year, is_official_exam FROM questions")}
        finally:
            conn.close()

    def test_dry_run_then_apply_only_gsi_and_idempotent(self):
        before = self._rows()
        self.assertEqual(self._run(), 0)
        self.assertEqual(self._rows(), before)                     # simulación: no escribe
        self.assertFalse(self.backups.exists())

        self.assertEqual(self._run("--apply"), 0)
        rows = self._rows()
        self.assertEqual(rows[1], (2024, 1))
        self.assertEqual(rows[2], (2024, 1))
        self.assertEqual(rows[3], (None, 0))                       # otras fuentes, intactas
        self.assertEqual(rows[4], (2019, 1))
        self.assertEqual(len(list(self.backups.iterdir())), 1)

        self.assertEqual(self._run("--apply"), 0)                  # idempotente: ni copia nueva
        self.assertEqual(len(list(self.backups.iterdir())), 1)


if __name__ == "__main__":
    unittest.main()
