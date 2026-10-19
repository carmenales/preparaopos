"""Lector de SQL de MariaDB e importador de exámenes locales a test-engine."""

import contextlib
import io
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ETL_DIR = Path(__file__).resolve().parent.parent / "scripts" / "etl"
sys.path.insert(0, str(ETL_DIR))

import import_local_exams as importer  # noqa: E402
from mysql_dump_parser import LAST_INSERT_ID, parse_dump, split_statements  # noqa: E402

# Esquema de test-engine para las tablas que toca el importador (igual que la BD real).
SCHEMA = """
CREATE TABLE syllabi (id VARCHAR(64) PRIMARY KEY, code VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL, organism VARCHAR(64) NOT NULL);
CREATE TABLE scoring_rules (id INTEGER PRIMARY KEY, code VARCHAR(64) NOT NULL UNIQUE, name VARCHAR(255) NOT NULL,
    correct_score NUMERIC NOT NULL, wrong_penalty NUMERIC NOT NULL, blank_score NUMERIC NOT NULL,
    score_scale NUMERIC NOT NULL, min_score_zero BOOLEAN NOT NULL);
CREATE TABLE exams (id INTEGER PRIMARY KEY, name VARCHAR(255) NOT NULL, year INTEGER, convocatoria VARCHAR(128),
    syllabus_id VARCHAR(64) REFERENCES syllabi(id), scoring_rule_id INTEGER REFERENCES scoring_rules(id),
    duration_seconds INTEGER);
CREATE TABLE questions (id INTEGER PRIMARY KEY, statement TEXT NOT NULL, justification TEXT, img_path VARCHAR(255),
    source VARCHAR(32) NOT NULL, source_id VARCHAR(64) NOT NULL, is_annulled BOOLEAN NOT NULL, annulment_reason TEXT,
    pending_classification BOOLEAN NOT NULL, year INTEGER, is_official_exam BOOLEAN NOT NULL DEFAULT 0,
    CONSTRAINT uq_questions_source_id UNIQUE (source, source_id));
CREATE TABLE question_options (id INTEGER PRIMARY KEY, question_id INTEGER NOT NULL REFERENCES questions(id)
    ON DELETE CASCADE, option_text TEXT NOT NULL, is_correct BOOLEAN NOT NULL, display_order INTEGER NOT NULL,
    justification TEXT);
CREATE TABLE question_syllabus_tags (id INTEGER PRIMARY KEY, question_id INTEGER NOT NULL REFERENCES questions(id)
    ON DELETE CASCADE, syllabus_id VARCHAR(64) NOT NULL REFERENCES syllabi(id), block VARCHAR(32), topic VARCHAR(32),
    CONSTRAINT uq_question_syllabus_tag UNIQUE (question_id, syllabus_id, block, topic));
CREATE TABLE exam_questions (exam_id INTEGER NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE, position INTEGER NOT NULL,
    is_reserve BOOLEAN NOT NULL DEFAULT 0, PRIMARY KEY (exam_id, question_id));
INSERT INTO scoring_rules VALUES (1, 'age-oficial-tercio', 'AGE oficial A − F/3', 1, 0.3333333333, 0, 10, 1);
"""


class TestMysqlDumpParser(unittest.TestCase):
    def test_split_respects_quotes_and_comments(self):
        sql = "-- comentario; con punto y coma\nSET @a := 'x;y';\nINSERT INTO t (c) VALUES ('it''s -- ok');"
        self.assertEqual(split_statements(sql), ["SET @a := 'x;y'", "INSERT INTO t (c) VALUES ('it''s -- ok')"])

    def test_parse_inserts_variables_and_last_insert_id(self):
        sql = """
        START TRANSACTION;
        SET @categoria := 'EXAMEN 1';
        DELETE FROM ptype WHERE categoria = @categoria;
        INSERT INTO question_sets (categoria, convocatoria_year, created_at) VALUES (@categoria, 2024, NOW())
        ON DUPLICATE KEY UPDATE convocatoria_year = VALUES(convocatoria_year), updated_at = NOW();
        INSERT INTO ptype (pregunta, respuesta, img_path, bloque) VALUES ('¿Qué es ''X''?', 'Una cosa', NULL, 0);
        SET @id_pregunta := LAST_INSERT_ID();
        INSERT INTO incorrectas (id_pregunta, respuesta) VALUES (@id_pregunta, 'Otra'), (@id_pregunta, 'Ninguna');
        COMMIT;
        """
        rows = parse_dump(sql).rows
        self.assertEqual([r.table for r in rows], ["question_sets", "ptype", "incorrectas", "incorrectas"])
        self.assertEqual(rows[0].values, {"categoria": "EXAMEN 1", "convocatoria_year": 2024, "created_at": None})
        self.assertEqual(rows[1].values["pregunta"], "¿Qué es 'X'?")
        self.assertIsNone(rows[1].values["img_path"])
        self.assertIs(rows[2].values["id_pregunta"], LAST_INSERT_ID)
        self.assertEqual(rows[3].values["respuesta"], "Ninguna")

    def test_undefined_variable_fails(self):
        with self.assertRaises(ValueError):
            parse_dump("INSERT INTO ptype (categoria) VALUES (@nope);")


class TestLoadRealSources(unittest.TestCase):
    """Valida los ficheros reales de imports/ (sin tocar ninguna BD)."""

    @classmethod
    def setUpClass(cls):
        cls.exams = importer.load_all()

    def test_counts(self):
        self.assertEqual(len(self.exams), 12)
        self.assertEqual(sum(len(e.questions) for e in self.exams), 708)

    def test_every_question_has_one_correct_and_consecutive_letters(self):
        for e in self.exams:
            for q in e.questions:
                letters = [o.letter for o in q.options]
                self.assertEqual(letters, list("ABCDE"[: len(letters)]), q.source_id)
                self.assertEqual(sum(o.is_correct for o in q.options), 1, q.source_id)

    def test_correct_answer_is_not_always_first(self):
        for e in self.exams:
            letters = {o.letter for q in e.questions for o in q.options if o.is_correct}
            self.assertGreater(len(letters), 1, e.name)

    def test_template_without_official_key_is_excluded(self):
        self.assertFalse(any("ANALISTA APLICACIONES" in e.name for e in self.exams))


class TestApplyImport(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.db = tmp / "te.sqlite"
        self.backups = tmp / "backups"
        conn = sqlite3.connect(self.db)
        conn.executescript(SCHEMA)
        conn.close()

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, *extra):
        argv = ["import", "--db", str(self.db), "--backup-dir", str(self.backups), *extra]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return importer.main()

    def _scalar(self, sql, *params):
        conn = sqlite3.connect(self.db)
        try:
            return conn.execute(sql, params).fetchone()[0]
        finally:
            conn.close()

    def test_dry_run_writes_nothing(self):
        before = self.db.read_bytes()
        self.assertEqual(self._run(), 0)
        self.assertEqual(self.db.read_bytes(), before)

    def test_apply_is_complete_and_idempotent(self):
        self.assertEqual(self._run("--apply"), 0)
        self.assertEqual(self._scalar("SELECT COUNT(*) FROM questions"), 708)
        self.assertEqual(self._scalar("SELECT COUNT(*) FROM exams"), 12)
        self.assertEqual(self._scalar("SELECT COUNT(*) FROM exam_questions"), 708)
        self.assertEqual(self._scalar("SELECT COUNT(*) FROM question_syllabus_tags WHERE block IS NULL"), 708)
        self.assertEqual(self._scalar("SELECT SUM(pending_classification) FROM questions"), 708)
        self.assertEqual(self._scalar("SELECT COUNT(*) FROM questions WHERE source = 'uc3m-a2-gsi'"), 270)
        self.assertEqual(
            self._scalar("SELECT r.code FROM exams e JOIN scoring_rules r ON r.id = e.scoring_rule_id "
                         "WHERE e.syllabus_id = 'uc3m-a2-gsi' LIMIT 1"),
            "oficial-cuarto",
        )
        self.assertIsNone(self._scalar("SELECT scoring_rule_id FROM exams WHERE syllabus_id = "
                                       "'majadahonda-tecnico-informatica'"))
        # La correcta conserva su posición original (WCAG 2.2 es la B en el examen).
        self.assertEqual(
            self._scalar("SELECT o.display_order FROM question_options o JOIN questions q ON q.id = o.question_id "
                         "WHERE q.source_id = 'ayto-madrid-aux-tic-2024-practico-libre-016' AND o.is_correct = 1"),
            1,
        )

        self.assertEqual(self._run("--apply"), 0)
        self.assertEqual(self._scalar("SELECT COUNT(*) FROM questions"), 708)
        self.assertEqual(self._scalar("SELECT COUNT(*) FROM exams"), 12)


if __name__ == "__main__":
    unittest.main()
