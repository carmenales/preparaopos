import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from normalize_markdown import (
    remove_obvious_extraction_noise,
    remove_repeated_headers_footers,
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

    def test_removes_any_repeated_header_regardless_of_text(self):
        text = "\n".join([
            "## Página 1",
            "ForjaTIC — Apuntes oficiales",
            "Contenido de la página 1.",
            "## Página 2",
            "ForjaTIC — Apuntes oficiales",
            "Contenido de la página 2.",
        ])
        result = remove_obvious_extraction_noise(remove_repeated_headers_footers(text))
        self.assertNotIn("ForjaTIC", result)
        self.assertIn("Contenido de la página 1.", result)
        self.assertIn("Contenido de la página 2.", result)

    def test_single_page_repeated_line_is_not_removed(self):
        text = "## Página 1\nForjaTIC — Apuntes oficiales\nContenido único."
        result = remove_repeated_headers_footers(text)
        self.assertIn("ForjaTIC", result)

    def test_body_text_that_happens_to_repeat_in_the_middle_is_not_touched(self):
        text = "\n".join([
            "## Página 1",
            "Cabecera real",
            "Primera línea de contenido de la página 1.",
            "Un concepto importante se repite aquí para énfasis.",
            "Última línea de contenido de la página 1.",
            "Pie real",
            "## Página 2",
            "Cabecera real",
            "Primera línea de contenido de la página 2.",
            "Un concepto importante se repite aquí para énfasis.",
            "Última línea de contenido de la página 2.",
            "Pie real",
        ])
        result = remove_repeated_headers_footers(text)
        self.assertEqual(result.count("Un concepto importante se repite aquí para énfasis."), 2)
        self.assertNotIn("Cabecera real", result)
        self.assertNotIn("Pie real", result)

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

    def test_joins_continuation_starting_with_capitalized_proper_noun(self):
        """Regresión: _is_joinable exigía que la línea siguiente empezara
        en minúscula, lo que rompía frases que continúan con un sustantivo
        propio en mayúscula (Ley Orgánica, España, Estado...) — muy común
        en texto legal/administrativo."""
        text = "El artículo 53.2 remite a la Ley Orgánica que regula\nEspaña y su ordenamiento territorial."
        result = join_broken_paragraphs(text)
        self.assertEqual(
            result,
            "El artículo 53.2 remite a la Ley Orgánica que regula España y su ordenamiento territorial."
        )

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
