import unittest
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from pptx import Presentation
from pptx.util import Inches

from extract_pptx_text import (
    _sanitize_filename,
    _shape_text,
    extract_pptx_to_markdown,
)


class DummyShapeNoText:
    has_text_frame = False
    has_table = False


class DummyTableShape:
    has_text_frame = False
    has_table = True

    class Table:
        class Row:
            class Cell:
                def __init__(self, text):
                    self.text = text

            def __init__(self, cell_texts):
                self.cells = [self.Cell(t) for t in cell_texts]

        def __init__(self, rows_data):
            self.rows = [self.Row(r) for r in rows_data]

    def __init__(self, rows_data):
        self.table = self.Table(rows_data)


class TestExtractPptxText(unittest.TestCase):

    def test_sanitize_filename_replaces_disallowed_characters(self):
        self.assertEqual(_sanitize_filename("foto/con*espacios?.png"), "foto-con-espacios-.png")
        self.assertEqual(_sanitize_filename("diapositiva#1!"), "diapositiva-1")

    def test_sanitize_filename_fallback_when_empty_or_only_symbols(self):
        self.assertEqual(_sanitize_filename(""), "img")
        self.assertEqual(_sanitize_filename("***///???"), "img")

    def test_shape_text_returns_empty_when_no_text_or_table(self):
        shape = DummyShapeNoText()
        self.assertEqual(_shape_text(shape), "")

    def test_shape_text_formats_table_rows_with_pipe(self):
        shape = DummyTableShape([
            ["Encabezado 1", "Encabezado 2"],
            ["Valor A", "Valor B"],
        ])
        result = _shape_text(shape)
        self.assertEqual(result, "Encabezado 1 | Encabezado 2\nValor A | Valor B")

    def test_extract_pptx_to_markdown_raises_when_file_not_found(self):
        non_existent = Path("unlikely_to_exist_presentation_12345.pptx")
        out_md = Path("output.md")
        with self.assertRaises(FileNotFoundError):
            extract_pptx_to_markdown(non_existent, out_md)

    def test_extract_pptx_to_markdown_generates_markdown_from_presentation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            pptx_path = tmp_path / "sample.pptx"
            md_path = tmp_path / "sample.md"

            prs = Presentation()
            # Slide 1: Title and content
            slide_layout = prs.slide_layouts[0]
            slide1 = prs.slides.add_slide(slide_layout)
            slide1.shapes.title.text = "Título de prueba"
            slide1.placeholders[1].text = "Subtítulo o contenido de diapositiva"

            # Add speaker notes to slide 1
            slide1.notes_slide.notes_text_frame.text = "Nota importante del orador."

            # Slide 2: Blank slide
            blank_layout = prs.slide_layouts[6]
            prs.slides.add_slide(blank_layout)

            prs.save(str(pptx_path))

            extract_pptx_to_markdown(pptx_path, md_path, extract_images=False)

            self.assertTrue(md_path.exists())
            content = md_path.read_text(encoding="utf-8")

            self.assertIn("## Diapositiva 1", content)
            self.assertIn("Título de prueba", content)
            self.assertIn("Subtítulo o contenido de diapositiva", content)
            self.assertIn("**Notas del orador:**", content)
            self.assertIn("Nota importante del orador.", content)
            self.assertIn("## Diapositiva 2", content)
            self.assertIn("_Diapositiva sin texto ni imágenes reconocidas._", content)


if __name__ == "__main__":
    unittest.main()

