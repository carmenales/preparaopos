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
    clean_inline_noise,
    detect_note_title,
    is_pure_page_or_header_noise,
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

    def test_detect_note_title_from_noisy_header(self):
        noisy_line = "Página1 | 12 ## ESQUEMA NACIONAL DE SEGURIDAD Actualizado a 06/11/2023"
        title, topic = detect_note_title(noisy_line, "A2_Tema_I.09.II_ENS-ENI.pdf")
        self.assertEqual(title, "ESQUEMA NACIONAL DE SEGURIDAD")
        self.assertEqual(topic, "ESQUEMA NACIONAL DE SEGURIDAD")

    def test_clean_inline_noise_removes_page_markers_and_dates(self):
        noisy_heading = "Página1 | 12 ## ESQUEMA NACIONAL DE SEGURIDAD Actualizado a 06/11/2023"
        self.assertEqual(clean_inline_noise(noisy_heading), "## ESQUEMA NACIONAL DE SEGURIDAD")

        pure_noise_page = "### Página2 | 12"
        self.assertEqual(clean_inline_noise(pure_noise_page), "")

        footer_noise = "Convocatoria 2024 - Pág. 3 / 10 - Actualizado a 01/02/2024"
        self.assertEqual(clean_inline_noise(footer_noise), "")

    def test_is_pure_page_or_header_noise(self):
        self.assertTrue(is_pure_page_or_header_noise("### Página2 | 12"))
        self.assertTrue(is_pure_page_or_header_noise("Página1 | 12"))
        self.assertTrue(is_pure_page_or_header_noise("1 | 12"))
        self.assertTrue(is_pure_page_or_header_noise("Actualizado a 06/11/2023"))
        self.assertTrue(is_pure_page_or_header_noise("Todos los derechos reservados"))
        self.assertTrue(is_pure_page_or_header_noise("www.ejemplo-academia.com"))
        self.assertFalse(is_pure_page_or_header_noise("ESQUEMA NACIONAL DE SEGURIDAD"))
        self.assertFalse(is_pure_page_or_header_noise("## Principios Básicos del ENS"))

    def test_natural_prose_with_page_word_is_preserved(self):
        prose = "En la página 10 del Esquema Nacional de Seguridad se definen las dimensiones."
        self.assertFalse(is_pure_page_or_header_noise(prose))
        self.assertEqual(clean_inline_noise(prose), prose)

    def test_line_level_heading_and_callout_separation(self):
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        # Heading: 14pt
        page.insert_text((50, 100), "1. INTRODUCCIÓN", fontsize=14)
        # Paragraph: 10pt
        page.insert_text((50, 130), "El Esquema Nacional de Seguridad se ha actualizado con el RD 311/2022.", fontsize=10)
        page.insert_text((50, 150), "El supuesto práctico suele incorporar una pregunta relativa al ENS.", fontsize=10)
        # Callout: 10pt (starts with 'Consejo...')
        page.insert_text((50, 190), "Consejo de Preparatic", fontsize=10)
        # Callout body: 10pt
        page.insert_text((50, 210), "Aunque en el examen no nos pidan categorizar el sistema...", fontsize=10)
        # Label with colon
        page.insert_text((50, 250), "Ejemplos a evitar:", fontsize=10)
        page.insert_text((50, 270), "Indicar que el sistema es de categoría básica.", fontsize=10)

        pdf_bytes = doc.tobytes()
        doc.close()

        service = IngestService()
        result = service.extract_from_pdf_bytes(pdf_bytes, filename="test_intro.pdf", normalize=True)
        md = result["markdown"]

        # 1. El heading debe estar en su propia línea
        self.assertIn("### 1. INTRODUCCIÓN", md)
        # 2. El párrafo NO debe estar pegado al heading como ####
        self.assertNotIn("#### 1. INTRODUCCIÓN El Esquema", md)
        self.assertNotIn("### 1. INTRODUCCIÓN El Esquema", md)
        self.assertIn("El Esquema Nacional de Seguridad se ha actualizado con el RD 311/2022.", md)
        # 3. Consejo debe ser un callout destacado
        self.assertIn("**Consejo de Preparatic**", md)
        # 4. Ejemplos a evitar debe ser un bloque destacado
        self.assertIn("**Ejemplos a evitar:**", md)

    def test_bullet_point_continuation_without_blank_lines(self):
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        # Línea 1 de viñeta
        page.insert_text((50, 100), "• Un nivel Alto suele estar vinculado con: riesgo de muerte para las personas, perjuicio muy alto", fontsize=10)
        # Línea 2 continuación
        page.insert_text((50, 120), "para el país, etc. Si se pone hay que tenerlo muy justificado y asumir que se pueden implantar", fontsize=10)
        # Línea 3 continuación
        page.insert_text((50, 140), "las medidas que este nivel requiere.", fontsize=10)

        pdf_bytes = doc.tobytes()
        doc.close()

        service = IngestService()
        result = service.extract_from_pdf_bytes(pdf_bytes, filename="test_bullets.pdf", normalize=True)
        md = result["markdown"]

        # Debe unirse en un solo ítem de viñeta sin líneas en blanco intermedias
        self.assertIn("- Un nivel Alto suele estar vinculado con: riesgo de muerte para las personas, perjuicio muy alto para el país, etc.", md)
        self.assertIn("asumir que se pueden implantar las medidas que este nivel requiere.", md)
        self.assertNotIn("perjuicio muy alto\n\npara el país", md)
        self.assertNotIn("implantar\n\nlas medidas", md)

    def test_unclosed_parenthesis_and_abbreviation_continuation(self):
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        page.insert_text((50, 100), "• Régimen jurídico del sector público: Ley 40/2015 del Régimen Jurídico del Sector Público (art.", fontsize=10)
        page.insert_text((50, 120), "156) o RD 203/2021 Reglamento de actuación y funcionamiento del Sector Público por medios electrónicos.", fontsize=10)
        pdf_bytes = doc.tobytes()
        doc.close()

        service = IngestService()
        result = service.extract_from_pdf_bytes(pdf_bytes, filename="test_art.pdf", normalize=True)
        md = result["markdown"]
        self.assertIn("- Régimen jurídico del sector público: Ley 40/2015 del Régimen Jurídico del Sector Público (art. 156) o RD 203/2021", md)
        self.assertNotIn("(art.\n\n156)", md)

    def test_dangling_connective_continuation(self):
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        page.insert_text((50, 100), "• Ley Orgánica 7/2021, de 26 de mayo, de protección de datos personales tratados para fines de", fontsize=10)
        page.insert_text((50, 120), "prevención, detección, investigación y enjuiciamiento de infracciones penales y de ejecución de sanciones penales (art.37)", fontsize=10)
        pdf_bytes = doc.tobytes()
        doc.close()

        service = IngestService()
        result = service.extract_from_pdf_bytes(pdf_bytes, filename="test_fines_de.pdf", normalize=True)
        md = result["markdown"]
        self.assertIn("- Ley Orgánica 7/2021, de 26 de mayo, de protección de datos personales tratados para fines de prevención, detección", md)
        self.assertNotIn("fines de\n\nprevención", md)

    def test_lone_bullet_and_subbullets(self):
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        page.insert_text((50, 100), "•", fontsize=10)
        page.insert_text((50, 120), "Marco estratégico de ciberseguridad:", fontsize=10)
        page.insert_text((50, 140), "o RD 1150/2021 de Estrategia de Seguridad Nacional 2021", fontsize=10)
        page.insert_text((50, 160), "o Plan Nacional de Ciberseguridad aprobado en Consejo de Ministros el 29/03/2022", fontsize=10)
        pdf_bytes = doc.tobytes()
        doc.close()

        service = IngestService()
        result = service.extract_from_pdf_bytes(pdf_bytes, filename="test_subbullets.pdf", normalize=True)
        md = result["markdown"]
        self.assertIn("- **Marco estratégico de ciberseguridad:**", md)
        self.assertIn("- RD 1150/2021 de Estrategia de Seguridad Nacional 2021", md)
        self.assertNotIn("•\n\n**Marco", md)

    def test_colon_in_continuous_sentence_is_not_split_as_callout(self):
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        page.insert_text((50, 100), "Para asignar un nivel de seguridad u otro a cada dimensión se tendrá que valorar el impacto de un", fontsize=10)
        page.insert_text((50, 120), "incidente sobre:", fontsize=10)
        pdf_bytes = doc.tobytes()
        doc.close()

        service = IngestService()
        result = service.extract_from_pdf_bytes(pdf_bytes, filename="test_colon.pdf", normalize=True)
        md = result["markdown"]
        self.assertIn("Para asignar un nivel de seguridad u otro a cada dimensión se tendrá que valorar el impacto de un incidente sobre:", md)
        self.assertNotIn("un\n\n**incidente sobre:**", md)

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
