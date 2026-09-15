import unittest
import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

# Graceful mock for spacy if not installed in local environment
if "spacy" not in sys.modules:
    try:
        import spacy
    except ImportError:
        mock_spacy = MagicMock()
        sys.modules["spacy"] = mock_spacy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from extract_tags import (
    slugify,
    split_frontmatter,
    clean_markdown_body,
    select_tags,
    update_frontmatter_tags,
    extract_candidates,
    process_file,
)


class TestExtractTags(unittest.TestCase):

    def test_slugify_converts_accents_and_spaces_to_hyphens(self):
        self.assertEqual(slugify("Constitución Española"), "constitucion-espanola")
        self.assertEqual(slugify("  Inteligencia   Artificial  "), "inteligencia-artificial")
        self.assertEqual(slugify("C++ & Python / Shell"), "c-python-shell")
        self.assertEqual(slugify("---"), "")

    def test_split_frontmatter_with_valid_frontmatter(self):
        content = "---\ntitle: Test\ntags: []\n---\n# Encabezado\nCuerpo del apunte."
        fm, body = split_frontmatter(content)
        self.assertEqual(fm, "---\ntitle: Test\ntags: []\n---")
        self.assertEqual(body, "\n# Encabezado\nCuerpo del apunte.")

    def test_split_frontmatter_without_frontmatter(self):
        content = "# Solo encabezado\nCuerpo sin frontmatter."
        fm, body = split_frontmatter(content)
        self.assertEqual(fm, "")
        self.assertEqual(body, content)

    def test_clean_markdown_body_strips_headings_tables_quotes_and_formats_bullets(self):
        body = (
            "# Título Principal\n"
            "Texto normal de introducción.\n"
            "## Subtítulo\n"
            "| Columna 1 | Columna 2 |\n"
            "| --- | --- |\n"
            "| Dato A | Dato B |\n"
            "> Cita célebre\n"
            "- Elemento de lista uno\n"
            "- Elemento de lista dos\n"
        )
        cleaned = clean_markdown_body(body)
        self.assertNotIn("# Título Principal", cleaned)
        self.assertNotIn("## Subtítulo", cleaned)
        self.assertNotIn("Columna 1", cleaned)
        self.assertNotIn("Cita célebre", cleaned)
        self.assertIn("Texto normal de introducción.", cleaned)
        self.assertIn("Elemento de lista uno", cleaned)
        self.assertIn("Elemento de lista dos", cleaned)

    def test_select_tags_filters_short_slugs_and_stopwords(self):
        candidates = [
            "tema", "introduccion", "resumen", "bloque", "apartado", "punto", "seccion",  # stopwords
            "ia", "el", "de",  # < 3 chars
            "ciberseguridad", "ciberseguridad",  # freq 2
            "esquema nacional de seguridad",  # freq 1, longer
            "criptografia",  # freq 1
        ]
        tags = select_tags(candidates, max_tags=5)
        # Should exclude stopwords and short slugs
        self.assertNotIn("tema", tags)
        self.assertNotIn("introduccion", tags)
        self.assertNotIn("ia", tags)

        # Most frequent first
        self.assertEqual(tags[0], "ciberseguridad")
        self.assertIn("esquema-nacional-de-seguridad", tags)
        self.assertIn("criptografia", tags)

    def test_select_tags_respects_max_tags(self):
        candidates = [f"concepto {i}" for i in range(20)]
        tags = select_tags(candidates, max_tags=3)
        self.assertEqual(len(tags), 3)

    def test_update_frontmatter_tags_replaces_existing_block(self):
        existing_fm = (
            "---\n"
            "id: \"apunte-01\"\n"
            "title: \"Prueba\"\n"
            "tags:\n"
            "  - \"viejo-tag-1\"\n"
            "  - \"viejo-tag-2\"\n"
            "status: \"draft\"\n"
            "---"
        )
        new_tags = ["ciberseguridad", "ens"]
        updated = update_frontmatter_tags(existing_fm, new_tags)

        self.assertNotIn("viejo-tag-1", updated)
        self.assertIn('  - "ciberseguridad"', updated)
        self.assertIn('  - "ens"', updated)
        self.assertIn('status: "draft"', updated)

    def test_update_frontmatter_tags_inserts_tags_when_not_present(self):
        existing_fm = (
            "---\n"
            "id: \"apunte-02\"\n"
            "title: \"Sin tags previos\"\n"
            "status: \"draft\"\n"
            "---"
        )
        new_tags = ["redes", "protocolos"]
        updated = update_frontmatter_tags(existing_fm, new_tags)

        self.assertIn("tags:", updated)
        self.assertIn('  - "redes"', updated)
        self.assertIn('  - "protocolos"', updated)
        self.assertTrue(updated.endswith("---"))

    def test_extract_candidates_from_doc_chunks_and_ents(self):
        mock_chunk1 = MagicMock()
        mock_chunk1.text = "redes neuronales"
        mock_chunk2 = MagicMock()
        mock_chunk2.text = "   "

        mock_ent1 = MagicMock()
        mock_ent1.text = "Comunidad de Madrid"
        mock_ent2 = MagicMock()
        mock_ent2.text = ""

        mock_doc = MagicMock()
        mock_doc.noun_chunks = [mock_chunk1, mock_chunk2]
        mock_doc.ents = [mock_ent1, mock_ent2]

        candidates = extract_candidates(mock_doc)
        self.assertEqual(candidates, ["redes neuronales", "Comunidad de Madrid"])

    def test_process_file_end_to_end_with_mock_nlp(self):
        import extract_tags

        with tempfile.TemporaryDirectory() as tmpdir:
            in_file = Path(tmpdir) / "test_note.md"
            out_file = Path(tmpdir) / "out_note.md"

            content = (
                "---\n"
                "id: \"test-nlp\"\n"
                "title: \"Nota NLP\"\n"
                "status: \"draft\"\n"
                "---\n"
                "# Título\n"
                "El aprendizaje profundo y el procesamiento de lenguaje natural son ramas de la inteligencia artificial."
            )
            in_file.write_text(content, encoding="utf-8")

            # Mock NLP call for process_file
            mock_chunk1 = MagicMock()
            mock_chunk1.text = "aprendizaje profundo"
            mock_chunk2 = MagicMock()
            mock_chunk2.text = "inteligencia artificial"
            mock_doc = MagicMock()
            mock_doc.noun_chunks = [mock_chunk1, mock_chunk2]
            mock_doc.ents = []

            original_nlp = extract_tags.NLP
            try:
                extract_tags.NLP = MagicMock(return_value=mock_doc)
                process_file(in_file, out_file, overwrite=True, max_tags=5)

                self.assertTrue(out_file.exists())
                result_text = out_file.read_text(encoding="utf-8")
                self.assertIn('  - "aprendizaje-profundo"', result_text)
                self.assertIn('  - "inteligencia-artificial"', result_text)
            finally:
                extract_tags.NLP = original_nlp


if __name__ == "__main__":
    unittest.main()

