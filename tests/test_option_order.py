"""Orden de opciones: letras oficiales, barajado determinista y script de corrección."""

import contextlib
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ETL_DIR = Path(__file__).resolve().parent.parent / "scripts" / "etl"
sys.path.insert(0, str(ETL_DIR))

import fix_option_order as fixer  # noqa: E402
from option_order import letter_hint, official_positions, stable_positions  # noqa: E402


class TestOfficialPositions(unittest.TestCase):
    def test_letters_from_justifications(self):
        self.assertEqual(
            official_positions(
                "Pregunta 1. Respuesta correcta: opción D, según plantilla.",
                ["Opción A incorrecta según plantilla.", "Opción B incorrecta.", "Opción C incorrecta."],
            ),
            [3, 0, 1, 2],
        )

    def test_correct_letter_inferred_when_not_stated(self):
        self.assertEqual(
            official_positions(None, ["Opción A incorrecta.", "Opción C incorrecta."]), [1, 0, 2]
        )

    def test_incomplete_or_inconsistent_returns_none(self):
        self.assertIsNone(official_positions("Respuesta correcta: opción B", ["Opción A incorrecta.", None]))
        self.assertIsNone(official_positions("Respuesta correcta: opción A", ["Opción A incorrecta."]))


class TestStablePositions(unittest.TestCase):
    def test_is_a_deterministic_permutation(self):
        first = stable_positions("tai-mariadb-legacy:42", 4)
        self.assertEqual(sorted(first), [0, 1, 2, 3])
        self.assertEqual(first, stable_positions("tai-mariadb-legacy:42", 4))

    def test_correct_is_not_always_first(self):
        firsts = {stable_positions(f"k:{i}", 4)[0] for i in range(50)}
        self.assertEqual(firsts, {0, 1, 2, 3})

    def test_hint_places_correct_option(self):
        for i in range(20):
            positions = stable_positions(f"k:{i}", 4, 2)
            self.assertEqual(positions[0], 2)
            self.assertEqual(sorted(positions), [0, 1, 2, 3])

    def test_letter_hint(self):
        self.assertEqual(letter_hint("La respuesta es la opción C porque...", 4), 2)
        self.assertIsNone(letter_hint("Ni la opción A ni la opción B", 4))
        self.assertIsNone(letter_hint("opción E", 4))
        self.assertIsNone(letter_hint(None, 4))


SCHEMA = """
CREATE TABLE questions (id INTEGER PRIMARY KEY, source TEXT, source_id TEXT, justification TEXT);
CREATE TABLE question_options (id INTEGER PRIMARY KEY, question_id INTEGER, option_text TEXT,
    is_correct BOOLEAN, display_order INTEGER, justification TEXT);
CREATE TABLE exam_questions (exam_id INTEGER, question_id INTEGER, position INTEGER);
"""


class TestFixOptionOrder(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.db, self.json, self.backups = tmp / "te.sqlite", tmp / "gsi.json", tmp / "backups"
        conn = sqlite3.connect(self.db)
        conn.executescript(SCHEMA)
        # GSI: correcta D guardada en primera posición (el bug)
        conn.execute("INSERT INTO questions VALUES (1, 'age-gsi-2024', '1', 'Respuesta correcta: opción D')")
        conn.executemany("INSERT INTO question_options VALUES (?, 1, ?, ?, ?, ?)", [
            (1, "dd", 1, 0, None), (2, "aa", 0, 1, "Opción A incorrecta."),
            (3, "bb", 0, 2, "Opción B incorrecta."), (4, "cc", 0, 3, "Opción C incorrecta."),
        ])
        conn.execute("INSERT INTO exam_questions VALUES (53, 1, 1)")
        # TAI: sin letras
        conn.execute("INSERT INTO questions VALUES (2, 'tai-mariadb-legacy', '7', NULL)")
        conn.executemany("INSERT INTO question_options VALUES (?, 2, ?, ?, ?, NULL)", [
            (5, "ok", 1, 0), (6, "x", 0, 1), (7, "y", 0, 2), (8, "z", 0, 3),
        ])
        conn.commit()
        conn.close()
        self._write_json("D")

    def tearDown(self):
        self._tmp.cleanup()

    def _write_json(self, correct):
        self.json.write_text(json.dumps({"preguntas": [{
            "numero": 1, "respuesta_correcta": correct,
            "opciones": {"a": "aa", "b": "bb", "c": "cc", "d": "dd Página 1 de 10"},
        }]}), encoding="utf-8")

    def _run(self, *extra):
        argv = ["fix", "--db", str(self.db), "--gsi-json", str(self.json), "--backup-dir", str(self.backups), *extra]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return fixer.main()

    def _orders(self):
        conn = sqlite3.connect(self.db)
        try:
            return dict(conn.execute("SELECT option_text, display_order FROM question_options"))
        finally:
            conn.close()

    def test_dry_run_writes_nothing(self):
        before = self.db.read_bytes()
        self.assertEqual(self._run(), 0)
        self.assertEqual(self.db.read_bytes(), before)

    def test_apply_restores_gsi_and_shuffles_tai_idempotently(self):
        self.assertEqual(self._run("--apply"), 0)
        orders = self._orders()
        self.assertEqual([orders[t] for t in ("aa", "bb", "cc", "dd")], [0, 1, 2, 3])
        self.assertEqual([orders[t] for t in ("ok", "x", "y", "z")], stable_positions("tai-mariadb-legacy:7", 4))
        self.assertEqual(len(list(self.backups.glob("*.sqlite"))), 1)

        self.assertEqual(self._run("--apply"), 0)
        self.assertEqual(len(list(self.backups.glob("*.sqlite"))), 1)

    def test_aborts_if_official_json_disagrees(self):
        self._write_json("A")
        before = self.db.read_bytes()
        self.assertEqual(self._run("--apply"), 1)
        self.assertEqual(self.db.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
