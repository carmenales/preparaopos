import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from normalize_markdown import (
    remove_obvious_extraction_noise,
    convert_acronym_blocks_to_table,
    dedupe_repeated_lines,
    join_broken_paragraphs,
    fix_broken_lists,
    normalize_whitespace,
)


class TestRemoveObviousExtractionNoise(unittest.TestCase):

    def test_removes_page_marker(self):
        text = "## Página 3\nContenido real."
        result = remove_obvious_extraction_noise(text)
        self.assertNotIn("Página 3", result)
        self.assertIn("Contenido real.", result)

    def test_removes_known_hardcoded_header(self):
        text = "## Centro de Estudios TIC\nContenido real."
        result = remove_obvious_extraction_noise(text)
        self.assertNotIn("Centro de Estudios TIC", result)

    def test_KNOWN_LIMITATION_does_not_remove_unlisted_academy_headers(self):
        """Documenta una limitación real, no un comportamiento deseado:
        SIMPLE_HEADER_RE tiene la cabecera de una academia concreta
        hardcodeada como texto literal. Cualquier otra fuente (otra
        academia, PreparaTIC) con su propia cabecera repetida NO se
        detecta ni se limpia aquí. Si este test empieza a fallar porque
        alguien generalizó la detección (por posición/frecuencia en vez
        de texto literal), es una buena noticia — hay que actualizarlo,
        no dejarlo en rojo."""
        text = "## ForjaTIC — Apuntes oficiales\nContenido real."
        result = remove_obvious_extraction_noise(text)
        self.assertIn("ForjaTIC", result)

    def test_preserves_blank_lines(self):
        text = "Párrafo uno.\n\nPárrafo dos."
        result = remove_obvious_extraction_noise(text)
        self.assertEqual(result, text)


class TestConvertAcronymBlocksToTable(unittest.TestCase):

    def test_converts_recognized_acronym_block_to_table(self):
        text = (
            "Las siglas empleadas en este documento son las siguientes:\n"
            "ENS\n"
            "Esquema Nacional de Seguridad\n"
            "RGPD\n"
            "Reglamento General de Protección de Datos\n"
        )
        result = convert_acronym_blocks_to_table(text)

        self.assertIn("## Siglas", result)
        self.assertIn("| Sigla | Significado |", result)
        self.assertIn("| ENS | Esquema Nacional de Seguridad |", result)
        self.assertIn("| RGPD | Reglamento General de Protección de Datos |", result)

    def test_leaves_text_without_intro_phrase_untouched(self):
        text = "ENS\nEsquema Nacional de Seguridad\n"
        result = convert_acronym_blocks_to_table(text)
        self.assertNotIn("| Sigla |", result)


class TestDedupeRepeatedLines(unittest.TestCase):

    def test_removes_consecutive_duplicate_lines(self):
        text = "Línea A\nLínea A\nLínea B"
        result = dedupe_repeated_lines(text)
        self.assertEqual(result, "Línea A\nLínea B")

    def test_keeps_non_consecutive_duplicates(self):
        text = "Línea A\nLínea B\nLínea A"
        result = dedupe_repeated_lines(text)
        self.assertEqual(result.count("Línea A"), 2)


class TestJoinBrokenParagraphs(unittest.TestCase):

    def test_joins_lines_split_mid_sentence(self):
        text = "Esta frase se ha\ncortado a mitad."
        result = join_broken_paragraphs(text)
        self.assertEqual(result, "Esta frase se ha cortado a mitad.")

    def test_does_not_join_across_heading(self):
        text = "Texto antes.\n## Un heading\nTexto después."
        result = join_broken_paragraphs(text)
        self.assertIn("## Un heading", result)

    def test_does_not_join_list_items(self):
        text = "- primer punto\n- segundo punto"
        result = join_broken_paragraphs(text)
        self.assertEqual(result, text)

    def test_does_not_join_after_sentence_ending_punctuation(self):
        text = "Frase completa.\nOtra frase distinta."
        result = join_broken_paragraphs(text)
        self.assertIn("Frase completa.\nOtra frase distinta.", result)


class TestFixBrokenLists(unittest.TestCase):

    def test_joins_lone_bullet_marker_with_next_line(self):
        text = "-\nprimer punto"
        result = fix_broken_lists(text)
        self.assertEqual(result, "- primer punto")

    def test_normalizes_bullet_character(self):
        text = "• un punto con viñeta rara"
        result = fix_broken_lists(text)
        self.assertEqual(result, "- un punto con viñeta rara")


class TestNormalizeWhitespace(unittest.TestCase):

    def test_collapses_three_or_more_blank_lines_to_two(self):
        text = "A\n\n\n\nB"
        result = normalize_whitespace(text)
        self.assertEqual(result, "A\n\nB\n")

    def test_collapses_repeated_spaces(self):
        text = "palabra    con    espacios"
        result = normalize_whitespace(text)
        self.assertEqual(result, "palabra con espacios\n")


if __name__ == '__main__':
    unittest.main()
