import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from extract_pdf_text import (
    _sanitize_filename,
    _normalize_text,
    _looks_like_toc_page,
    _infer_heading_level,
)


class TestSanitizeFilename(unittest.TestCase):

    def test_replaces_disallowed_characters_with_hyphen(self):
        # _sanitize_filename no translitera acentos, solo permite
        # [a-zA-Z0-9._-]; cualquier otra cosa (incluidos acentos) se
        # sustituye por guion.
        self.assertEqual(_sanitize_filename("página 1: imagen/raro?.png"), "p-gina-1-imagen-raro-.png")

    def test_strips_leading_and_trailing_hyphens(self):
        self.assertEqual(_sanitize_filename("---nombre---"), "nombre")

    def test_empty_input_falls_back_to_img(self):
        self.assertEqual(_sanitize_filename(""), "img")

    def test_only_disallowed_characters_falls_back_to_img(self):
        self.assertEqual(_sanitize_filename("???"), "img")


class TestNormalizeText(unittest.TestCase):

    def test_removes_soft_hyphen(self):
        self.assertNotIn("\u00ad", _normalize_text("pala\u00adbra"))

    def test_joins_hyphenated_word_split_across_line(self):
        result = _normalize_text("informa-\nción")
        self.assertEqual(result, "información")

    def test_joins_word_wrapped_without_hyphen(self):
        # Esto es justo el bug que arreglamos cambiando de pypdf a PyMuPDF:
        # una palabra cortada por salto de línea sin guion se une con un
        # espacio, no se queda pegada ("informacion" + "extra" -> con espacio).
        result = _normalize_text("informacion\nextra")
        self.assertEqual(result, "informacion extra")

    def test_collapses_any_run_of_blank_lines_to_a_single_space(self):
        """_normalize_text normaliza DENTRO de un bloque de texto de
        PyMuPDF, no entre bloques — por eso cualquier racha de saltos de
        línea, sea uno o varios, acaba colapsada a un solo espacio. La
        separación real entre párrafos/páginas la pone el código que
        reensambla bloques más arriba (con "\\n\\n".join), no esta función."""
        result = _normalize_text("A\n\n\n\nB")
        self.assertEqual(result, "A B")

    def test_collapses_repeated_spaces_and_tabs(self):
        result = _normalize_text("palabra\t\tcon   espacios")
        self.assertEqual(result, "palabra con espacios")


class TestLooksLikeTocPage(unittest.TestCase):

    def test_recognizes_toc_with_dot_leaders_and_page_numbers(self):
        toc_text = "\n".join([
            "ÍNDICE",
            "1. Introducción .......................... 3",
            "2. La Constitución Española .............. 5",
            "2.1. Características ..................... 5",
            "2.2. Estructura ........................... 7",
            "3. La Corona .............................. 21",
            "4. Conclusión .............................. 25",
        ])
        self.assertTrue(_looks_like_toc_page(toc_text))

    def test_does_not_flag_normal_prose_as_toc(self):
        prose = "\n".join([
            "La Constitución española es la norma suprema del ordenamiento jurídico.",
            "Recoge los fundamentos y principios básicos sobre los que se asienta el Estado.",
            "A lo largo de este tema se analizan los principios constitucionales, los derechos",
            "fundamentales y sus mecanismos de protección, así como la Corona.",
            "El contenido de este tema es uno de los más extensos del temario completo.",
            "Como ventaja, puede afirmarse que no se trata de un tema de difícil comprensión.",
        ])
        self.assertFalse(_looks_like_toc_page(prose))

    def test_short_page_is_never_flagged_as_toc(self):
        self.assertFalse(_looks_like_toc_page("Solo\ndos\nlíneas"))


class TestInferHeadingLevel(unittest.TestCase):

    def test_no_size_difference_is_not_a_heading(self):
        self.assertEqual(_infer_heading_level(11.0, 11.0), 0)

    def test_small_size_difference_is_level_4(self):
        self.assertEqual(_infer_heading_level(12.5, 11.0), 4)

    def test_medium_size_difference_is_level_3(self):
        self.assertEqual(_infer_heading_level(14.0, 11.0), 3)

    def test_large_size_difference_is_level_2(self):
        self.assertEqual(_infer_heading_level(17.0, 11.0), 2)

    def test_zero_body_size_never_infers_heading(self):
        """Evita división por cero / falsos positivos cuando no se ha
        podido calcular un tamaño de cuerpo de referencia para la página."""
        self.assertEqual(_infer_heading_level(20.0, 0.0), 0)


if __name__ == '__main__':
    unittest.main()
