import unittest
import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

if "pymysql" not in sys.modules:
    try:
        import pymysql
    except ImportError:
        mock_pymysql = MagicMock()
        sys.modules["pymysql"] = mock_pymysql

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from suggest_topic_links import (
    fetch_existing_links,
    fetch_unlinked_topics,
    fetch_sample_questions,
    search_semantic,
    cmd_suggest,
    cmd_apply,
    CSV_FIELDS,
)


class TestSuggestTopicLinks(unittest.TestCase):

    def test_fetch_existing_links(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"categoria": "tai", "bloque": 1, "tema": 2},
            {"categoria": "tai", "bloque": 2, "tema": None},
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        links = fetch_existing_links(mock_conn)
        self.assertEqual(len(links), 2)
        self.assertIn(("tai", 1, 2), links)
        self.assertIn(("tai", 2, None), links)

    def test_fetch_unlinked_topics(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"categoria": "tai", "bloque": 1, "tema": 3, "attempts_count": 15},
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        unlinked = fetch_unlinked_topics(mock_conn)
        self.assertEqual(len(unlinked), 1)
        self.assertEqual(unlinked[0]["attempts_count"], 15)

    def test_fetch_sample_questions(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"pregunta": "¿Qué es la memoria caché?"},
            {"pregunta": "¿Qué nivel de RAID ofrece redundancia?"},
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        samples = fetch_sample_questions(mock_conn, "tai", 1, 1, 2)
        self.assertEqual(len(samples), 2)
        self.assertEqual(samples[0], "¿Qué es la memoria caché?")

    @patch("requests.get")
    def test_search_semantic(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "results": [
                {"note_id": "nota-01", "score": 0.85, "note_title": "Arquitectura de Computadores"}
            ]
        }
        mock_get.return_value = mock_resp

        results = search_semantic("http://localhost:8091", "memoria cache", 5)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["note_id"], "nota-01")
        self.assertEqual(results[0]["score"], 0.85)

    @patch("suggest_topic_links.connect_db")
    @patch("suggest_topic_links.search_semantic")
    def test_cmd_suggest_generates_csv(self, mock_search, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        # 1: fetch_existing_links -> empty
        # 2: fetch_unlinked_topics -> 1 topic
        # 3: fetch_sample_questions -> 1 question
        mock_cursor.fetchall.side_effect = [
            [],
            [{"categoria": "madrid", "bloque": 1, "tema": 1, "attempts_count": 5}],
            [{"pregunta": "¿En qué año se aprobó la Constitución?"}],
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        mock_search.return_value = [
            {
                "note_id": "constitucion-1978",
                "note_title": "Constitución Española",
                "heading": "Título Preliminar",
                "score": 0.92,
            }
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "sugerencias.csv"

            args = MagicMock()
            args.db_host = "127.0.0.1"
            args.db_port = 3307
            args.db_user = "user"
            args.db_password = "pw"
            args.db_name = "db"
            args.output_csv = str(csv_path)
            args.embeddings_url = "http://localhost:8091"
            args.threshold = 0.45
            args.top_k = 5

            cmd_suggest(args)

            self.assertTrue(csv_path.exists())
            content = csv_path.read_text(encoding="utf-8")
            self.assertIn("constitucion-1978", content)
            self.assertIn("0.92", content)


if __name__ == "__main__":
    unittest.main()

