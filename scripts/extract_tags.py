#!/usr/bin/env python3
"""
Extrae tags automáticos para apuntes Markdown usando spaCy (es_core_news_sm).

- Lee .md con frontmatter YAML (--- ... ---).
- Usa noun chunks y entidades para detectar conceptos clave.
- Genera hasta N tags tipo 'constitucion-espanola'.
- Sustituye el bloque 'tags:' del frontmatter o lo añade si no existe.
"""

from __future__ import annotations

import argparse
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Tuple, List

import spacy

# Cargamos el modelo español una sola vez
NLP = spacy.load("es_core_news_sm")

FRONTMATTER_DELIM_RE = re.compile(r"^---\s*$", re.MULTILINE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def split_frontmatter(content: str) -> Tuple[str, str]:
    """
    Devuelve (frontmatter, body). Si no hay frontmatter, frontmatter es "".
    """
    matches = list(FRONTMATTER_DELIM_RE.finditer(content))
    if len(matches) < 2:
        return "", content

    start = matches[0].start()
    end = matches[1].end()
    frontmatter = content[start:end]
    body = content[end:]
    return frontmatter, body


def clean_markdown_body(body: str) -> str:
    """
    Limpia el cuerpo para extracción de términos:
    - quita cabeceras Markdown y líneas de tablas/citas
    - deja texto plano para NLP
    """
    lines: List[str] = []
    for raw in body.splitlines():
        s = raw.strip()
        if not s:
            continue
        if s.startswith("#"):
            # headings fuera
            continue
        if s.startswith("|") or s.startswith(">"):
            # tablas y citas fuera
            continue
        # bullets: nos quedamos con el texto
        if s.startswith("- "):
            s = s[2:].strip()
        lines.append(s)
    text = " ".join(lines)
    return text


def slugify(text: str) -> str:
    """
    Convierte 'Constitución Española' -> 'constitucion-espanola'.
    """
    text = text.strip().lower()
    # normalizar acentos
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    # reemplazar cualquier cosa no alfanumérica por espacio
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = text.strip()
    if not text:
        return ""
    return re.sub(r"\s+", "-", text)


def extract_candidates(doc: spacy.tokens.Doc) -> List[str]:
    """
    Extrae frases candidatas (noun chunks + entidades).
    """
    candidates: List[str] = []

    # noun chunks
    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        if phrase:
            candidates.append(phrase)

    # entidades
    for ent in doc.ents:
        phrase = ent.text.strip()
        if phrase:
            candidates.append(phrase)

    return candidates


def select_tags(candidates: List[str], max_tags: int = 10) -> List[str]:
    """
    Normaliza candidatos a slugs y selecciona los mejores por frecuencia y longitud.
    """
    counts: Counter[str] = Counter()

    for phrase in candidates:
        slug = slugify(phrase)
        if not slug:
            continue
        # descartamos slugs demasiado cortos
        if len(slug) < 3:
            continue
        # descartamos slugs tipo 'tema', 'introduccion', etc.
        if slug in {
            "tema", "introduccion", "conclusion", "resumen",
            "bloque", "apartado", "punto", "seccion"
        }:
            continue
        counts[slug] += 1

    if not counts:
        return []

    # ordenar por frecuencia desc y longitud desc (preferimos conceptos algo más largos)
    sorted_slugs = sorted(counts.items(), key=lambda kv: (-kv[1], -len(kv[0])))
    tags = [slug for slug, _ in sorted_slugs[:max_tags]]
    return tags


def update_frontmatter_tags(frontmatter: str, tags: List[str]) -> str:
    """
    Sustituye/añade bloque 'tags:' en el frontmatter con la lista dada.
    """
    lines = frontmatter.splitlines()
    out: List[str] = []
    in_tags_block = False
    has_tags = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("tags:"):
            has_tags = True
            out.append("tags:")
            for tag in tags:
                out.append(f'  - "{tag}"')
            in_tags_block = True
            continue

        if in_tags_block:
            # saltamos líneas anteriores del bloque tags hasta encontrar otra clave o cierre ---
            if stripped.startswith(("id:", "title:", "type:", "status:", "processes:",
                                    "official_topic:", "source_ids:", "created_at:",
                                    "last_reviewed:", "origin:", "academy:",
                                    "ai_generated:", "ai_cleaned:", "ai_sources:",
                                    "needs_human_review:", "---")):
                in_tags_block = False
                out.append(line)
            # si no, ignoramos (eran los tags antiguos)
            continue

        out.append(line)

    if not has_tags:
        # insertar tags antes del segundo '---' si existe
        inserted = False
        for i, line in enumerate(out):
            if line.strip() == "---" and i != 0:  # cierre del frontmatter
                out.insert(i, "tags:")
                for tag in tags:
                    out.insert(i + 1, f'  - "{tag}"')
                inserted = True
                break
        if not inserted:
            # frontmatter raro; añadimos al final
            out.append("tags:")
            for tag in tags:
                out.append(f'  - "{tag}"')

    return "\n".join(out)


def process_file(input_path: Path, output_path: Path, overwrite: bool, max_tags: int) -> None:
    content = read_text(input_path)
    frontmatter, body = split_frontmatter(content)

    if not frontmatter or not body.strip():
        print(f"[sin-frontmatter/body] {input_path}")
        return

    text = clean_markdown_body(body)
    if not text.strip():
        print(f"[sin-texto] {input_path}")
        return

    doc = NLP(text)
    candidates = extract_candidates(doc)
    tags = select_tags(candidates, max_tags=max_tags)

    if not tags:
        print(f"[sin-tags] {input_path}")
        return

    new_frontmatter = update_frontmatter_tags(frontmatter, tags)
    new_content = new_frontmatter + body

    if overwrite:
        target = output_path
    else:
        # escribe junto al input, con sufijo .tagged.md
        target = output_path.with_suffix(".tagged.md")

    write_text(target, new_content)
    print(f"[tags] {input_path} -> {', '.join(tags)}")


def iter_markdown_files(root: Path) -> List[Path]:
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extrae tags automáticos para apuntes Markdown usando spaCy."
    )
    parser.add_argument("input", help="Archivo .md o carpeta de entrada")
    parser.add_argument("output", help="Archivo .md o carpeta de salida")
    parser.add_argument(
        "--max-tags",
        type=int,
        default=10,
        help="Número máximo de tags por apunte (default: 10)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescribir archivos existentes en la carpeta de salida",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if input_path.is_file():
        # caso fichero único
        target = output_path
        if output_path.exists() and output_path.is_dir():
            target = output_path / input_path.name
        if target.exists() and not args.overwrite:
            raise FileExistsError(f"Ya existe: {target}. Usa --overwrite para sobrescribir.")
        process_file(input_path, target, overwrite=True, max_tags=args.max_tags)
        return

    if not input_path.exists() or not input_path.is_dir():
        raise FileNotFoundError(f"No existe la carpeta de entrada: {input_path}")

    md_files = iter_markdown_files(input_path)
    if not md_files:
        print(f"No se han encontrado .md en {input_path}")
        return

    for source in md_files:
        rel = source.relative_to(input_path)
        target = output_path / rel
        if target.exists() and not args.overwrite:
            print(f"[omitido] {rel}")
            continue
        process_file(source, target, overwrite=True, max_tags=args.max_tags)


if __name__ == "__main__":
    main()