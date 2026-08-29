import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from build_semantic_index import split_into_heading_chunks


class TestSplitIntoHeadingChunks(unittest.TestCase):

    def test_preamble_before_first_heading_becomes_its_own_chunk(self):
        body = "Texto introductorio sin heading.\n\n## Primer tema\n\nContenido del tema."
        chunks = split_into_heading_chunks(body)

        self.assertEqual(chunks[0]["level"], 0)
        self.assertIsNone(chunks[0]["heading"])
        self.assertIsNone(chunks[0]["anchor"])
        self.assertEqual(chunks[0]["text"], "Texto introductorio sin heading.")

    def test_no_preamble_when_document_starts_with_heading(self):
        body = "## Primer tema\n\nContenido."
        chunks = split_into_heading_chunks(body)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["heading"], "Primer tema")

    def test_each_heading_level_becomes_a_separate_chunk(self):
        body = "## Nivel 2\nTexto A.\n### Nivel 3\nTexto B.\n#### Nivel 4\nTexto C."
        chunks = split_into_heading_chunks(body)

        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0]["level"], 2)
        self.assertEqual(chunks[0]["heading"], "Nivel 2")
        self.assertEqual(chunks[0]["text"], "Texto A.")
        self.assertEqual(chunks[1]["level"], 3)
        self.assertEqual(chunks[1]["text"], "Texto B.")
        self.assertEqual(chunks[2]["level"], 4)
        self.assertEqual(chunks[2]["text"], "Texto C.")

    def test_h1_is_not_a_chunk_boundary(self):
        """El regex de heading solo reconoce ## a #### — un # (H1, título
        del documento) se queda como texto normal dentro del chunk, no
        genera un chunk propio. Es el comportamiento actual real, no
        necesariamente el ideal — este test documenta qué pasa hoy."""
        body = "# Título del documento\nTexto bajo el título.\n## Primer tema\nContenido."
        chunks = split_into_heading_chunks(body)

        self.assertEqual(len(chunks), 2)
        self.assertIsNone(chunks[0]["heading"])
        self.assertIn("Título del documento", chunks[0]["text"])

    def test_heading_markers_asterisk_underscore_backtick_are_stripped(self):
        body = "## **Negrita** y `código`\nContenido."
        chunks = split_into_heading_chunks(body)

        self.assertEqual(chunks[0]["heading"], "Negrita y código")

    def test_anchor_matches_slugify_from_build_knowledge_index(self):
        from build_knowledge_index import slugify

        body = "## Tema con Ácentos y Ñ\nContenido del tema."
        chunks = split_into_heading_chunks(body)

        self.assertEqual(chunks[0]["anchor"], slugify("Tema con Ácentos y Ñ"))

    def test_heading_with_no_following_content_produces_no_chunk(self):
        """Caso límite real, encontrado escribiendo este test: un heading
        sin texto debajo (el último del documento, o seguido directamente
        de otro heading) no genera ningún chunk — su `chunk_text` queda
        vacío tras strip() y se descarta con `if not chunk_text: continue`.
        Efecto práctico: un apunte cuyo último heading no tiene contenido
        propio (todo el texto real quedó en un heading anterior) deja esa
        sección sin indexar para búsqueda semántica, en silencio."""
        body = "## Tema con Ácentos y Ñ"
        chunks = split_into_heading_chunks(body)

        self.assertEqual(chunks, [])

    def test_heading_immediately_followed_by_another_heading_produces_no_empty_chunk(self):
        body = "## Vacío\n## Con contenido\nTexto."
        chunks = split_into_heading_chunks(body)

        # El heading "Vacío" no genera chunk propio porque su texto
        # asociado queda vacío tras strip().
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["heading"], "Con contenido")

    def test_chunk_text_is_truncated_to_max_chunk_chars(self):
        import build_semantic_index as bsi

        long_text = "palabra " * 2000  # muy por encima de MAX_CHUNK_CHARS
        body = f"## Tema largo\n{long_text}"
        chunks = split_into_heading_chunks(body)

        self.assertLessEqual(len(chunks[0]["text"]), bsi.MAX_CHUNK_CHARS)


if __name__ == '__main__':
    unittest.main()
