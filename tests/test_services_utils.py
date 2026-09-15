import unittest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.knowledge.text_utils import slugify as knowledge_slugify


def _normalize_rows(vectors: np.ndarray) -> np.ndarray:
    """Normaliza cada fila a norma 1, para que el producto escalar sea coseno."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1e-8
    return vectors / norms


class TestServicesUtils(unittest.TestCase):

    def test_knowledge_text_utils_slugify(self):
        self.assertEqual(knowledge_slugify("Constitución Española 1978"), "constitucion-espanola-1978")
        self.assertEqual(knowledge_slugify("   Espacios   y   Mayúsculas  "), "espacios-y-mayusculas")
        self.assertEqual(knowledge_slugify("¿Qué es una API RESTful?"), "que-es-una-api-restful")
        self.assertEqual(knowledge_slugify("!@#$%^&*()"), "")
        self.assertEqual(knowledge_slugify(""), "")

    def test_normalize_rows_unit_norm(self):
        vectors = np.array([
            [3.0, 4.0],
            [1.0, 1.0, 1.0, 1.0] if False else [0.0, 5.0],
        ], dtype=np.float32)

        normalized = _normalize_rows(vectors)

        # Vector 1 norm: sqrt(3^2 + 4^2) = 5 -> [3/5, 4/5] = [0.6, 0.8]
        self.assertAlmostEqual(float(np.linalg.norm(normalized[0])), 1.0, places=5)
        self.assertAlmostEqual(float(normalized[0][0]), 0.6, places=5)
        self.assertAlmostEqual(float(normalized[0][1]), 0.8, places=5)

        # Vector 2 norm: sqrt(0^2 + 5^2) = 5 -> [0, 1]
        self.assertAlmostEqual(float(np.linalg.norm(normalized[1])), 1.0, places=5)
        self.assertAlmostEqual(float(normalized[1][1]), 1.0, places=5)

    def test_normalize_rows_handles_zero_vector(self):
        vectors = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
        ], dtype=np.float32)

        normalized = _normalize_rows(vectors)
        # Should not raise division by zero
        self.assertFalse(np.isnan(normalized).any())
        self.assertAlmostEqual(float(np.linalg.norm(normalized[1])), 1.0, places=5)

    def test_cosine_similarity_ranking(self):
        # 3 database vectors
        matrix = np.array([
            [1.0, 0.0],
            [0.7071, 0.7071],
            [0.0, 1.0],
        ], dtype=np.float32)
        norm_matrix = _normalize_rows(matrix)

        # Query vector aligned with second vector
        query = np.array([0.7071, 0.7071], dtype=np.float32)
        query_norm = query / np.linalg.norm(query)

        scores = norm_matrix @ query_norm
        top_idx = int(np.argmax(scores))

        self.assertEqual(top_idx, 1)
        self.assertAlmostEqual(float(scores[1]), 1.0, places=4)


if __name__ == "__main__":
    unittest.main()

