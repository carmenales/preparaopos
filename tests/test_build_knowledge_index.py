import unittest
import sys
import os
from pathlib import Path
import json
import subprocess
import tempfile
import textwrap

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

class TestBuildIndexEndToEnd(unittest.TestCase):

    def run_builder(self, note_content: str, relative_note_path: str):
        repo_root = Path(__file__).resolve().parents[1]
        script_path = repo_root / "scripts" / "build_knowledge_index.py"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            knowledge_dir = tmpdir_path / "knowledge"
            note_path = knowledge_dir / relative_note_path
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(textwrap.dedent(note_content).strip() + "\n", encoding="utf-8")

            output_dir = tmpdir_path / "apps" / "studyassistant" / "data"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / "knowledge_index.json"

            subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "--knowledge-root",
                    str(knowledge_dir),
                    "--output",
                    str(output_file),
                ],
                check=True,
                cwd=repo_root,
            )

            self.assertTrue(output_file.exists(), "No se ha generado knowledge_index.json")

            return json.loads(output_file.read_text(encoding="utf-8"))

    def test_generates_index_with_metadata_and_headings(self):
        data = self.run_builder(
            """
            ---
            id: tema-007-tipos-encriptacion
            title: Tipos de encriptación
            official_topic: Tema 7. Tipos de encriptación
            processes:
              - ayuntamiento-majadahonda
            profiles:
              - operador-sistemas-informaticos
            shared_with:
              - otro-perfil
            tags:
              - rsa
              - hash
            status: draft
            ---

            # Tipos de encriptación

            ## RSA

            Contenido.

            ### Hash

            Más contenido.
            """,
            "processes/ayuntamiento-majadahonda/profiles/operador-sistemas-informaticos/apuntes/tema-007-tipos-encriptacion.md",
        )

        self.assertIn("notes", data)
        self.assertEqual(len(data["notes"]), 1)

        note = data["notes"][0]

        self.assertEqual(note["id"], "tema-007-tipos-encriptacion")
        self.assertEqual(note["title"], "Tipos de encriptación")
        self.assertEqual(note["official_topic"], "Tema 7. Tipos de encriptación")
        self.assertEqual(note["status"], "draft")
        self.assertEqual(note["tags"], ["rsa", "hash"])
        self.assertEqual(note["processes"], ["ayuntamiento-majadahonda"])
        self.assertEqual(note["profiles"], ["operador-sistemas-informaticos"])
        self.assertEqual(note["shared_with"], ["otro-perfil"])

        self.assertIn("path", note)
        self.assertTrue(note["path"].endswith("tema-007-tipos-encriptacion.md"))

        self.assertIn("headings", note)
        self.assertEqual(len(note["headings"]), 2)
        self.assertEqual(note["headings"][0]["level"], 2)
        self.assertEqual(note["headings"][0]["text"], "RSA")
        self.assertEqual(note["headings"][0]["anchor"], "rsa")
        self.assertEqual(note["headings"][1]["level"], 3)
        self.assertEqual(note["headings"][1]["text"], "Hash")
        self.assertEqual(note["headings"][1]["anchor"], "hash")

    def test_note_without_practice_topics_is_still_indexed(self):
        data = self.run_builder(
            """
            ---
            id: p01-tema-006-arquitectura
            title: Arquitectura
            official_topic: Tema 6. Arquitectura
            tags:
              - arquitectura
              - patrones
            ---

            # Arquitectura

            ## Patrones

            Contenido.
            """,
            "processes/comunidad-madrid/administracion-digital/ia/profiles/p01-consultor-sistemas-informacion-ia/apuntes/p01-tema-006-arquitectura.md",
        )

        self.assertIn("notes", data)
        self.assertEqual(len(data["notes"]), 1)

        note = data["notes"][0]

        self.assertEqual(note["id"], "p01-tema-006-arquitectura")
        self.assertEqual(note["tags"], ["arquitectura", "patrones"])
        self.assertIn("headings", note)
        self.assertEqual(note["headings"][0]["text"], "Patrones")

if __name__ == '__main__':
    unittest.main()