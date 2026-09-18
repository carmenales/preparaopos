import os
import sys
import tempfile
import unittest
from pathlib import Path

import fitz

# Añadir paths del repo
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "services" / "knowledge"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from config import settings
from ingest_service import (
    IngestService,
    detect_note_title,
    sanitize_filename,
    strip_frontmatter,
)
from schemas import PublishNoteRequest


def _create_sample_pdf_bytes() -> bytes:
    """Crea un documento PDF mínimo en memoria con fitz para pruebas."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    # Título con tamaño grande (20pt)
    page.insert_text((50, 100), "TEMA 12. REDES DE AREA LOCAL Y PROTOCOLOS", fontsize=20)
    # Subtítulo (14pt)
    page.insert_text((50, 150), "1. Arquitectura de Red", fontsize=14)
    # Cuerpo (10pt)
    page.insert_text((50, 180), "Las redes de area local (LAN) permiten interconectar equipos.", fontsize=10)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


class TestIngestService(unittest.TestCase):

    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename("Tema: 01 / Redes? *"), "Tema-01-Redes.md")
        self.assertEqual(sanitize_filename("apunte_final.md"), "apunte_final.md")
        self.assertEqual(sanitize_filename("archivo sin extension"), "archivo sin extension.md")

    def test_detect_note_title_from_tema_header(self):
        text = "# TEMA IV.17. SEGURIDAD Y PROTECCIÓN DE DATOS\n\nContenido introductorio..."
        title, topic = detect_note_title(text, "test.pdf")
        self.assertEqual(title, "Tema IV.17 SEGURIDAD Y PROTECCIÓN DE DATOS")
        self.assertEqual(topic, "IV.17 SEGURIDAD Y PROTECCIÓN DE DATOS")

    def test_detect_note_title_fallback_filename(self):
        text = "Solo un párrafo sin headings.\nSegunda línea."
        title, topic = detect_note_title(text, "A2_Tema_05_BBDD.pdf")
        self.assertIn("Tema 05 BBDD", title)

    def test_strip_frontmatter(self):
        content_with_fm = "---\nid: test\ntitle: Titulo\n---\n# Encabezado\nTexto real"
        cleaned = strip_frontmatter(content_with_fm)
        self.assertEqual(cleaned, "# Encabezado\nTexto real")

        content_without_fm = "# Encabezado\nTexto directo"
        self.assertEqual(strip_frontmatter(content_without_fm), "# Encabezado\nTexto directo")

    def test_extract_from_pdf_bytes(self):
        pdf_bytes = _create_sample_pdf_bytes()
        service = IngestService()
        result = service.extract_from_pdf_bytes(pdf_bytes, filename="test_tema12.pdf", normalize=True)

        self.assertEqual(result["page_count"], 1)
        self.assertIn("REDES DE AREA LOCAL", result["detected_title"])
        self.assertTrue(result["stats"]["char_count"] > 0)
        self.assertTrue(len(result["markdown"]) > 0)

    def test_publish_note_creates_file_and_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir).resolve()
            knowledge_dir = tmp_root / "knowledge"
            index_path = tmp_root / "apps" / "studyassistant" / "data" / "knowledge_index.json"

            # Reconfigurar settings temporalmente
            object.__setattr__(settings, "knowledge_dir", knowledge_dir)
            object.__setattr__(settings, "index_output_path", index_path)

            service = IngestService()
            request = PublishNoteRequest(
                process_slug="age/a2-gsi",
                title="Tema IV.17 Nuevas Tecnologías en la AGE",
                official_topic="IV.17 Nuevas Tecnologías",
                markdown_body="## 1. Introducción\n\nTexto de prueba para el nuevo apunte.",
                tags=["nuevas-tecnologias", "innovacion"],
                status="revisado",
                source="cetic",
            )

            resp = service.publish_note(request)
            self.assertTrue(resp.success)
            self.assertEqual(resp.note_id, "tema-iv-17-nuevas-tecnologias-en-la-age")

            # Verificar que el fichero existe físicamente
            expected_file = (knowledge_dir.parent / resp.file_path).resolve()
            self.assertTrue(expected_file.exists())

            # Verificar contenido del frontmatter
            content = expected_file.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---\n"))
            self.assertIn('title: "Tema IV.17 Nuevas Tecnologías en la AGE"', content)
            self.assertIn('id: "tema-iv-17-nuevas-tecnologias-en-la-age"', content)
            self.assertIn('- "nuevas-tecnologias"', content)
            self.assertIn("## 1. Introducción", content)


if __name__ == "__main__":
    unittest.main()
