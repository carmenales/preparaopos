# Ruta: tests/test_build_knowledge_index.py
import unittest
import sys
import os
from pathlib import Path

# Añadimos la carpeta raíz al path para poder importar el script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.build_knowledge_index import slugify, extract_headings, normalize_array

class TestBuildIndex(unittest.TestCase):

    def test_slugify(self):
        """Comprueba que la generación de anclas limpia bien los textos."""
        self.assertEqual(slugify("Tema 1: ¡Hola Mundo!"), "tema-1-hola-mundo")
        self.assertEqual(slugify("Árboles y camión"), "arboles-y-camion")
        self.assertEqual(slugify("**Negritas**"), "negritas")

    def test_normalize_array(self):
        """Comprueba que los arrays del frontmatter se normalizan a listas planas."""
        self.assertEqual(normalize_array("item1, item2"), ["item1", "item2"])
        self.assertEqual(normalize_array([" a ", "b "]), ["a", "b"])
        self.assertEqual(normalize_array(None), [])

    def test_extract_headings(self):
        """Comprueba que se extraen correctamente los encabezados y sus anclas."""
        markdown_body = "## Introducción\nTexto de prueba.\n### Detalles Técnicos\n"
        headings = extract_headings(markdown_body)
        
        self.assertEqual(len(headings), 2)
        self.assertEqual(headings[0]["level"], 2)
        self.assertEqual(headings[0]["text"], "Introducción")
        self.assertEqual(headings[0]["anchor"], "introduccion")
        
        self.assertEqual(headings[1]["level"], 3)
        self.assertEqual(headings[1]["text"], "Detalles Técnicos")
        self.assertEqual(headings[1]["anchor"], "detalles-tecnicos")

if __name__ == '__main__':
    unittest.main()