"""El importador de TAI no debe absorber los exámenes locales que también están en ptype."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "etl"))

from import_tai_mariadb import is_local_exam_category  # noqa: E402


class TestLocalExamCategories(unittest.TestCase):
    def test_local_exam_categories_are_excluded(self):
        for categoria in (
            "AYTO MADRID AUX TIC 2021 - PRACTICO - LI",
            "AYTO MAJADAHONDA TECNICO INFORMATICA PRIMER EJERCICIO",
            "CM MADRID DIGITAL 2026 IA P01 CONSULTOR SOFTWARE",
            "UC3M A2 GSI 2024 BOLSA EJERCICIO TEORICO-PRACTICO",
        ):
            self.assertTrue(is_local_exam_category(categoria), categoria)

    def test_tai_categories_are_kept(self):
        for categoria in ("CUESTIONARIO TAI 2024 - TAI-LI B2-B4", "Administración Bases de Datos", "ENS", None, ""):
            self.assertFalse(is_local_exam_category(categoria), categoria)


if __name__ == "__main__":
    unittest.main()
