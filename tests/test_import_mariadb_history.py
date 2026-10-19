"""Lectura de los volcados de MariaDB para migrar el historial."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "etl"))

try:
    from import_mariadb_history import _norm, _unescape, read_tsv  # noqa: E402
except ImportError as exc:  # el script importa el dominio de test-engine
    raise unittest.SkipTest(f"dependencias no disponibles: {exc}")


class TestTsvReading(unittest.TestCase):
    def test_unescape_mariadb_batch_values(self):
        self.assertIsNone(_unescape("NULL"))
        self.assertEqual(_unescape(r"línea 1\nlínea 2\tfin \\ barra"), "línea 1\nlínea 2\tfin \\ barra")

    def test_read_tsv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.tsv"
            path.write_text("id\tpregunta\tsesion\n1\t¿Qué es\\tX?\tNULL\n", encoding="utf-8")
            self.assertEqual(read_tsv(path), [{"id": "1", "pregunta": "¿Qué es\tX?", "sesion": None}])

    def test_norm_ignores_spacing_and_case(self):
        self.assertEqual(_norm("  Hola\n  MUNDO "), "hola mundo")


if __name__ == "__main__":
    unittest.main()
