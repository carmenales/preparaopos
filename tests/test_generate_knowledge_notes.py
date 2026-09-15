import unittest
import sys
import os
import tempfile
from pathlib import Path
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from generate_knowledge_notes import (
    NoteMetadata,
    slugify,
    split_frontmatter,
    build_process_path,
    default_title_from_path,
    infer_process_profile,
    infer_official_topic,
    parse_list_arg,
    bool_from_value,
    merge_config,
    build_metadata,
    render_scalar,
    render_list,
    render_frontmatter,
    load_template_keys,
    load_yaml_config,
    process_file,
)


class TestGenerateKnowledgeNotes(unittest.TestCase):

    def test_slugify(self):
        self.assertEqual(slugify("Tema 1: Redes y Protocolos"), "tema-1-redes-y-protocolos")
        self.assertEqual(slugify("Árbol / Decisión"), "árbol-decisión")
        self.assertEqual(slugify("---test---"), "test")

    def test_split_frontmatter_valid_and_invalid(self):
        text_with_fm = "---\ntitle: Apunte\n---\n# Contenido\nTexto."
        lines, body = split_frontmatter(text_with_fm)
        self.assertEqual(lines, ["title: Apunte"])
        self.assertEqual(body, "# Contenido\nTexto.")

        text_without_fm = "# Solo contenido\nSin frontmatter."
        lines, body = split_frontmatter(text_without_fm)
        self.assertEqual(lines, [])
        self.assertEqual(body, text_without_fm)

        text_unclosed_fm = "---\ntitle: Apunte sin cierre"
        lines, body = split_frontmatter(text_unclosed_fm)
        self.assertEqual(lines, [])
        self.assertEqual(body, text_unclosed_fm)

    def test_build_process_path(self):
        self.assertEqual(build_process_path("age", "tic"), "age/tic")
        self.assertEqual(build_process_path("age", "shared"), "age")
        self.assertEqual(build_process_path("age", ""), "age")

    def test_default_title_from_path(self):
        path = Path("01_introduccion_a_la_ia.md")
        self.assertEqual(default_title_from_path(path), "01 introduccion a la ia")

    def test_infer_process_profile(self):
        self.assertEqual(infer_process_profile(("age", "tai", "sub"), "fallback_proc", "fallback_prof"), ("age", "tai"))
        self.assertEqual(infer_process_profile(("madrid",), "fallback_proc", "fallback_prof"), ("madrid", "fallback_prof"))
        self.assertEqual(infer_process_profile((), "fallback_proc", "fallback_prof"), ("fallback_proc", "fallback_prof"))

    def test_infer_official_topic(self):
        path1 = Path("tema 04 - redes.md")
        self.assertEqual(infer_official_topic(path1, None), "04")

        path2 = Path("Topic 02.md")
        self.assertEqual(infer_official_topic(path2, None), "02")

        path3 = Path("apunte_sin_tema.md")
        self.assertEqual(infer_official_topic(path3, None), "")

        # Explicit topic takes priority
        self.assertEqual(infer_official_topic(path1, "Tema Especial"), "Tema Especial")

    def test_parse_list_arg(self):
        self.assertEqual(parse_list_arg("tag1, tag2,tag3"), ["tag1", "tag2", "tag3"])
        self.assertEqual(parse_list_arg(None), [])
        self.assertEqual(parse_list_arg("  "), [])

    def test_bool_from_value(self):
        self.assertTrue(bool_from_value(True, False))
        self.assertFalse(bool_from_value(False, True))
        self.assertTrue(bool_from_value("true", False))
        self.assertTrue(bool_from_value("sí", False))
        self.assertTrue(bool_from_value("1", False))
        self.assertFalse(bool_from_value("no", True))
        self.assertFalse(bool_from_value("0", True))
        self.assertEqual(bool_from_value(None, True), True)
        self.assertEqual(bool_from_value("desconocido", False), False)

    def test_merge_config(self):
        config = {
            "defaults": {"status": "borrador", "ai_cleaned": True},
            "profiles": {
                "dev": {"status": "revisado", "tags": ["dev"]},
            },
            "shared": {
                "comun": {"shared_with": ["otro_proceso"]},
            }
        }
        # Merging with profile
        merged = merge_config(config, "dev", None, {"title": "CLI Title", "empty": None})
        self.assertEqual(merged["status"], "revisado")
        self.assertEqual(merged["title"], "CLI Title")
        self.assertNotIn("empty", merged)

        # Missing profile raises KeyError
        with self.assertRaises(KeyError):
            merge_config(config, "inexistente", None, {})

        with self.assertRaises(KeyError):
            merge_config(config, None, "inexistente", {})

    def test_build_metadata_and_render_frontmatter(self):
        source_path = Path("fuentes/madrid/ia/tema 02 - modelos.md")
        input_root = Path("fuentes")
        settings = {
            "source": "Manual Oficial",
            "tags": ["ia", "deep-learning"],
            "shared_with": ["tai"],
            "ai_generated": False,
        }
        metadata = build_metadata(source_path, input_root, settings)

        self.assertEqual(metadata.id, "tema-02-modelos")
        self.assertEqual(metadata.official_topic, "02")
        self.assertEqual(metadata.processes, ["madrid/ia"])
        self.assertEqual(metadata.tags, ["ia", "deep-learning"])
        self.assertEqual(metadata.created_at, date.today().isoformat())

        template_keys = [
            "id", "title", "type", "status", "processes", "profile", "source",
            "shared_with", "official_topic", "source_ids", "tags", "created_at",
            "last_reviewed", "ai_generated", "ai_cleaned",
        ]
        rendered = render_frontmatter(template_keys, metadata)
        rendered_text = "\n".join(rendered)

        self.assertIn('id: "tema-02-modelos"', rendered_text)
        self.assertIn('official_topic: "02"', rendered_text)
        self.assertIn('  - "madrid/ia"', rendered_text)
        self.assertIn('  - "ia"', rendered_text)
        self.assertIn('  - "deep-learning"', rendered_text)
        self.assertIn('ai_generated: false', rendered_text)
        self.assertIn('last_reviewed: null', rendered_text)

    def test_render_scalar_and_list(self):
        self.assertEqual(render_scalar("texto"), '"texto"')
        self.assertEqual(render_scalar(None), "null")
        self.assertEqual(render_list([]), ["[]"])
        self.assertEqual(render_list(["a", "b"]), ["", '  - "a"', '  - "b"'])

    def test_load_yaml_config_and_template_keys(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            template_file = tmp_path / "template.md"
            template_file.write_text(
                "---\n"
                "id: \"\"\n"
                "title: \"\"\n"
                "tags: []\n"
                "---\n"
                "Cuerpo de la plantilla\n",
                encoding="utf-8"
            )
            keys = load_template_keys(template_file)
            self.assertEqual(keys, ["id", "title", "tags"])

            config_file = tmp_path / "config.yml"
            config_file.write_text("defaults:\n  status: borrador\n", encoding="utf-8")
            conf = load_yaml_config(config_file)
            self.assertEqual(conf["defaults"]["status"], "borrador")

    def test_process_file_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            source_file = tmp_path / "fuentes" / "tema 01 - intro.md"
            source_file.parent.mkdir(parents=True, exist_ok=True)
            source_file.write_text(
                "---\n"
                "title: \"Antiguo\"\n"
                "---\n"
                "# Introducción a los Sistemas\n"
                "Este es el contenido del tema 01.",
                encoding="utf-8"
            )
            template_file = tmp_path / "template.md"
            template_file.write_text(
                "---\n"
                "id: \"\"\n"
                "title: \"\"\n"
                "official_topic: \"\"\n"
                "tags: []\n"
                "---\n",
                encoding="utf-8"
            )
            output_root = tmp_path / "salida"

            out_file = process_file(
                source_path=source_file,
                input_root=source_file.parent,
                output_root=output_root,
                template_path=template_file,
                settings={"official_topic": "01", "tags": ["intro"]},
                overwrite=True,
            )

            self.assertTrue(out_file.exists())
            result = out_file.read_text(encoding="utf-8")
            self.assertIn('official_topic: "01"', result)
            self.assertIn('  - "intro"', result)
            self.assertIn("# Introducción a los Sistemas", result)


if __name__ == "__main__":
    unittest.main()
