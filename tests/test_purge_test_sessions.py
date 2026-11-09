"""Purga de sesiones: por defecto solo las que dejó el smoke test, nunca el historial real."""

import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "purge_test_sessions.py"


def _make_db(path: Path) -> None:
    conn = sqlite3.connect(path)
    conn.executescript("""
        CREATE TABLE questions (id INTEGER PRIMARY KEY);
        CREATE TABLE test_sessions (id TEXT PRIMARY KEY, started_at TEXT, mode TEXT, source TEXT, source_ref TEXT);
        CREATE TABLE test_attempts (id INTEGER PRIMARY KEY, test_session_id TEXT, question_id INTEGER);
        INSERT INTO questions VALUES (18012);
    """)
    sessions = [
        # Pares del smoke test (simulacro 53 + práctica del apunte en menos de 10 s)
        ("smoke-exam-1", "2026-10-19 11:07:06.05", "exam", "exam", "53"),
        ("smoke-note-1", "2026-10-19 11:07:07.45", "practice", "note", "tema-i-01-derecho-constitucional"),
        ("smoke-exam-2", "2026-10-23 17:11:29.27", "exam", "exam", "53"),
        ("smoke-note-2", "2026-10-23 17:11:31.07", "practice", "note", "tema-i-01-derecho-constitucional"),
        # Uso real: no deben tocarse
        ("legacy-1", "2026-06-17 10:00:00", "practice", "legacy", "preparadortai: CUESTIONARIO TAI 2024"),
        ("generated-1", "2026-10-19 12:40:35", "practice", "generated", "syllabus=age-gsi-official&n=10"),
        ("real-exam-53", "2026-10-20 09:00:00", "exam", "exam", "53"),           # simulacro real, con respuestas
        ("real-note", "2026-10-21 09:00:00", "practice", "note", "tema-i-01-derecho-constitucional"),  # práctica sola
    ]
    conn.executemany("INSERT INTO test_sessions VALUES (?, ?, ?, ?, ?)", sessions)
    attempts = [("smoke-exam-1", 18012), ("smoke-exam-2", 18012), ("legacy-1", 1), ("legacy-1", 2),
                ("generated-1", 3), ("real-exam-53", 18012), ("real-exam-53", 18013)]
    conn.executemany("INSERT INTO test_attempts (test_session_id, question_id) VALUES (?, ?)", attempts)
    conn.commit()
    conn.close()


class PurgeTestSessionsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / "te.sqlite"
        _make_db(self.db)

    def _run(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), "--db", str(self.db),
                               "--backup-dir", str(Path(self.tmp.name) / "bk"), *args],
                              capture_output=True, text=True, encoding="utf-8")

    def _sessions(self):
        conn = sqlite3.connect(self.db)
        try:
            return sorted(r[0] for r in conn.execute("SELECT id FROM test_sessions"))
        finally:
            conn.close()

    def test_dry_run_selects_only_smoke_pairs(self):
        out = self._run()
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("Sesiones a borrar: 4 · intentos a borrar: 2", out.stdout)
        self.assertEqual(len(self._sessions()), 8)

    def test_apply_deletes_smoke_sessions_and_keeps_real_history(self):
        out = self._run("--apply")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(self._sessions(), ["generated-1", "legacy-1", "real-exam-53", "real-note"])
        conn = sqlite3.connect(self.db)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM test_attempts").fetchone()[0], 5)
        conn.close()
        self.assertTrue(any((Path(self.tmp.name) / "bk").iterdir()))
        self.assertIn("Sesiones a borrar: 0", self._run().stdout)

    def test_all_includes_everything_before_a_date(self):
        out = self._run("--all", "--before", "2026-10-20")
        self.assertIn("Selección: TODAS las sesiones", out.stdout)
        self.assertIn("Sesiones a borrar: 4 · intentos a borrar: 4", out.stdout)  # legacy, par del smoke, generado


if __name__ == "__main__":
    unittest.main()
