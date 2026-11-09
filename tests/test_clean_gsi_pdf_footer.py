"""Limpieza del pie de página del PDF en opciones de GSI 2024."""

import contextlib
import io
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "etl"))

import clean_gsi_pdf_footer as cleaner  # noqa: E402
from import_age_gsi_2024 import strip_pdf_footer  # noqa: E402


class TestStripPdfFooter(unittest.TestCase):
    def test_strip(self):
        self.assertEqual(strip_pdf_footer("Round Robin. 2024 - GSI-L  Página 7 de 10"), "Round Robin.")
        self.assertEqual(strip_pdf_footer("X.509 Certificate Token. 2024 - GSI-L  Pagina 10 de 10"),
                         "X.509 Certificate Token.")
        self.assertEqual(strip_pdf_footer("Página 7 del manual"), "Página 7 del manual")
        self.assertEqual(strip_pdf_footer("Sin pie."), "Sin pie.")


class TestCleanScript(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.db, self.backups = tmp / "te.sqlite", tmp / "backups"
        conn = sqlite3.connect(self.db)
        conn.executescript("""
            CREATE TABLE questions (id INTEGER PRIMARY KEY, source TEXT);
            CREATE TABLE question_options (id INTEGER PRIMARY KEY, question_id INTEGER, option_text TEXT);
            INSERT INTO questions VALUES (1, 'age-gsi-2024'), (2, 'tai-mariadb-legacy');
            INSERT INTO question_options VALUES (10, 1, 'Round Robin. 2024 - GSI-L  Página 7 de 10'),
                (11, 1, 'FCFS.'), (12, 2, 'Otra fuente. 2024 - GSI-L  Página 7 de 10');
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, *extra):
        argv = ["clean", "--db", str(self.db), "--backup-dir", str(self.backups), *extra]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
            return cleaner.main()

    def _texts(self):
        conn = sqlite3.connect(self.db)
        try:
            return dict(conn.execute("SELECT id, option_text FROM question_options"))
        finally:
            conn.close()

    def test_dry_run_then_apply_only_gsi_and_idempotent(self):
        self.assertEqual(self._run(), 0)
        self.assertTrue(self._texts()[10].endswith("de 10"))
        self.assertEqual(self._run("--apply"), 0)
        texts = self._texts()
        self.assertEqual(texts[10], "Round Robin.")
        self.assertEqual(texts[11], "FCFS.")
        self.assertTrue(texts[12].endswith("de 10"))  # otras fuentes no se tocan
        self.assertEqual(self._run("--apply"), 0)
        self.assertEqual(len(list(self.backups.glob("*.sqlite"))), 1)


if __name__ == "__main__":
    unittest.main()
