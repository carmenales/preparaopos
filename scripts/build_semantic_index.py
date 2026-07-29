#!/usr/bin/env python3
"""
Construye el índice semántico de los apuntes, troceados por sección/heading,
para que el servicio de embeddings pueda hacer búsqueda por similitud.

Reutiliza el parseo de frontmatter y el filtrado de ficheros de
build_knowledge_index.py, para no duplicar esa lógica ni desincronizarla.

Entrada:
    knowledge/**/*.md

Salida:
    apps/studyassistant/data/semantic_chunks.json      (metadatos por fragmento)
    apps/studyassistant/data/semantic_embeddings.npy   (vectores, mismo orden)

Se ejecuta DENTRO del contenedor `embeddings` (es el que tiene
sentence-transformers instalado):

    docker compose exec embeddings python scripts/build_semantic_index.py

Tras reindexar, reinicia el servicio para que cargue el índice nuevo:

    docker compose restart embeddings

Vuelve a ejecutarse cada vez que añadas o cambies apuntes (por ejemplo,
al meter los de la academia). No hay reindexado incremental en esta
primera versión: siempre regenera el índice completo.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from build_knowledge_index import parse_frontmatter, should_include, slugify

DEFAULT_CHUNKS_OUTPUT = Path("apps/studyassistant/data/semantic_chunks.json")
DEFAULT_EMBEDDINGS_OUTPUT = Path("apps/studyassistant/data/semantic_embeddings.npy")
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# El modelo trunca igualmente a su longitud máxima de tokens (~128 palabras);
# este límite es solo para no mandarle texto absurdamente largo a encode().
MAX_CHUNK_CHARS = 2000

HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$")


def split_into_heading_chunks(body: str) -> list[dict[str, Any]]:
    """
    Trocea el cuerpo Markdown en un fragmento por cada heading ##/###/####,
    más un fragmento "preámbulo" si hay contenido antes del primer heading.
    Cada fragmento se queda con el texto hasta el siguiente heading (de
    cualquier nivel) — trocear por heading, no por sección anidada, para
    resultados de búsqueda más finos.
    """
    lines = body.splitlines()

    boundaries: list[tuple[int, int, str]] = []
    for i, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            text = re.sub(r"[*_`]", "", match.group(2).strip())
            boundaries.append((i, level, text))

    chunks: list[dict[str, Any]] = []

    first_boundary_line = boundaries[0][0] if boundaries else len(lines)
    preamble = "\n".join(lines[:first_boundary_line]).strip()
    if preamble:
        chunks.append({"level": 0, "heading": None, "anchor": None, "text": preamble})

    for idx, (line_idx, level, text) in enumerate(boundaries):
        end_line = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(lines)
        chunk_text = "\n".join(lines[line_idx + 1 : end_line]).strip()
        if not chunk_text:
            continue
        chunks.append({
            "level": level,
            "heading": text,
            "anchor": slugify(text),
            "text": chunk_text[:MAX_CHUNK_CHARS],
        })

    return chunks


def build_semantic_index(
    knowledge_root: Path,
    chunks_output: Path,
    embeddings_output: Path,
) -> int:
    # Import perezoso: así `--help` no tarda en cargar torch si solo
    # quieres ver las opciones del script.
    import numpy as np
    from sentence_transformers import SentenceTransformer

    all_chunks: list[dict[str, Any]] = []
    texts_to_encode: list[str] = []

    for path in sorted(knowledge_root.rglob("*.md")):
        if not should_include(path, knowledge_root):
            continue

        metadata, body = parse_frontmatter(path)
        title = metadata.get("title") or path.stem.replace("-", " ").title()
        note_id = metadata["id"]

        for chunk in split_into_heading_chunks(body):
            heading_label = chunk["heading"] or "(introducción)"
            # Anteponer título + heading ayuda al modelo a situar el
            # fragmento aunque el texto en sí no repita esas palabras.
            embed_text = f"{title} — {heading_label}\n{chunk['text']}"

            all_chunks.append({
                "note_id": note_id,
                "note_title": title,
                "heading": chunk["heading"],
                "anchor": chunk["anchor"],
                "level": chunk["level"],
                "text_preview": chunk["text"][:280],
            })
            texts_to_encode.append(embed_text)

    if not texts_to_encode:
        raise RuntimeError("No se ha encontrado ningún fragmento que indexar en knowledge/.")

    print(f"Troceando y codificando {len(texts_to_encode)} fragmentos con {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts_to_encode, show_progress_bar=True, convert_to_numpy=True)

    chunks_output.parent.mkdir(parents=True, exist_ok=True)
    chunks_output.write_text(json.dumps(all_chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    np.save(embeddings_output, embeddings.astype(np.float32))

    return len(all_chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Construye el índice semántico de los apuntes.")
    parser.add_argument("--knowledge-root", default="knowledge")
    parser.add_argument("--chunks-output", default=str(DEFAULT_CHUNKS_OUTPUT))
    parser.add_argument("--embeddings-output", default=str(DEFAULT_EMBEDDINGS_OUTPUT))
    args = parser.parse_args()

    knowledge_root = Path(args.knowledge_root)
    if not knowledge_root.exists():
        raise FileNotFoundError(f"No existe la carpeta de conocimiento: {knowledge_root}")

    total = build_semantic_index(knowledge_root, Path(args.chunks_output), Path(args.embeddings_output))
    print(f"Índice semántico generado con éxito: {total} fragmentos.")


if __name__ == "__main__":
    main()
