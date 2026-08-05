#!/usr/bin/env python3
"""
Construye un índice JSON de la base de conocimiento Markdown.

Entrada:
    knowledge/**/*.md

Salida:
    apps/studyassistant/data/knowledge_index.json

No usa dependencias externas.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXCLUDED_PARTS = {"_template", "sources"}
DEFAULT_OUTPUT = Path("apps/studyassistant/data/knowledge_index.json")


def slugify(text: str) -> str:
    """Genera un slug seguro para URLs y anclas."""
    text = str(text).lower()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def normalize_array(value: Any) -> list[str]:
    """Asegura que el valor sea una lista plana de strings limpia."""
    if not value:
        return []
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return []


def parse_frontmatter(file_path: Path) -> tuple[dict[str, Any], str]:
    """Lee YAML frontmatter, normaliza arrays y deriva ID si falta."""
    raw = file_path.read_text(encoding="utf-8")
    markdown = raw.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")

    # Derivamos ID base por defecto
    default_id = file_path.stem

    if not markdown.startswith("---\n"):
        return {"id": default_id}, markdown

    end = markdown.find("\n---", 4)
    if end == -1:
        return {"id": default_id}, markdown

    raw_meta = markdown[4:end].strip("\n")
    body = markdown[end + 4 :].lstrip("\n")
    metadata: dict[str, Any] = {}
    current_key: str | None = None

    for line in raw_meta.splitlines():
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#"):
            continue

        if stripped.startswith("- ") and current_key:
            metadata.setdefault(current_key, [])
            if isinstance(metadata[current_key], list):
                metadata[current_key].append(parse_scalar(stripped[2:]))
            continue

        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key

            if value == "":
                metadata[key] = []
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                metadata[key] = [] if inner == "" else [parse_scalar(item.strip()) for item in inner.split(",") if item.strip()]
            else:
                metadata[key] = parse_scalar(value)

    for array_field in ["processes", "profiles", "shared_with", "tags", "topics"]:
        metadata[array_field] = normalize_array(metadata.get(array_field))

    # Derivar ID si falta
    if not metadata.get("id"):
        metadata["id"] = default_id

    return metadata, body


def extract_headings(body: str) -> list[dict[str, Any]]:
    """Extrae ##, ###, #### y genera anchors estables tipo slug."""
    headings: list[dict[str, Any]] = []
    
    for line in body.splitlines():
        match = re.match(r"^(#{2,4})\s+(.+?)\s*$", line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            clean_text = re.sub(r'[*_`]', '', text)
            anchor = slugify(clean_text)
            headings.append({"level": level, "text": clean_text, "anchor": anchor})
            
    return headings


def strip_markdown_to_text(body: str) -> str:
    """Convierte Markdown a texto plano aproximado: fuera bloques de código,
    enlaces (se queda con el texto visible), énfasis, marcas de heading/lista
    y tablas. No es un parser completo, es suficiente para excerpt y
    búsqueda por substring."""
    text = body

    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_~]{1,3}", "", text)
    text = re.sub(r"^\s*[-*+>]\s+", "", text, flags=re.MULTILINE)
    text = text.replace("|", " ")
    text = re.sub(r"\s+", " ", text).strip()

    return text


def build_excerpt(plain_text: str, max_chars: int = 220) -> str:
    if len(plain_text) <= max_chars:
        return plain_text

    excerpt = plain_text[:max_chars]
    cut = excerpt.rfind(" ")
    if cut > max_chars // 2:
        excerpt = excerpt[:cut]

    return excerpt + "…"


# Tope defensivo: content_text se carga entero en memoria en cada petición
# PHP (sa_load_index -> sa_filter_notes).
CONTENT_TEXT_MAX_CHARS = 4000


def should_include(path: Path, knowledge_root: Path) -> bool:
    if path.suffix.lower() != ".md":
        return False

    relative_parts = path.relative_to(knowledge_root).parts
    relative_parts_set = set(relative_parts)

    if relative_parts_set & EXCLUDED_PARTS:
        return False

    if path.name.lower() == "readme.md":
        return False

    if "apuntes" not in relative_parts:
        return False

    return True


def build_index(knowledge_root: Path, output_path: Path) -> list[dict[str, Any]]:
    """Recorre la base de conocimiento y produce el JSON de metadatos ordenado."""
    notes: list[dict[str, Any]] = []

    for path in sorted(knowledge_root.rglob("*.md")):
        if not should_include(path, knowledge_root):
            continue

        metadata, body = parse_frontmatter(path)

        title = metadata.get("title") or path.stem.replace("-", " ").title()
        note_id = metadata["id"]

        practice_obj = {}
        if metadata.get("topics"):
            practice_obj = {
                "mode": metadata.get("mode", "thematic"),
                "topics": metadata.get("topics")
            }

        plain_text = strip_markdown_to_text(body)

        notes.append({
            "id": note_id,
            "title": title,
            "official_topic": metadata.get("official_topic", ""),
            "slug": slugify(title),
            "path": path.as_posix(),
            "processes": metadata.get("processes", []),
            "profiles": metadata.get("profiles", []),
            "origin": metadata.get("origin", ""),
            "shared_with": metadata.get("shared_with", []),
            "tags": metadata.get("tags", []),
            "practice": practice_obj,
            "status": metadata.get("status", ""),
            "headings": extract_headings(body),
            "excerpt": build_excerpt(plain_text),
            "content_text": plain_text[:CONTENT_TEXT_MAX_CHARS],
        })

    notes.sort(key=lambda x: x["title"])

    output_data = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "notes": notes
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return notes


def main() -> None:
    parser = argparse.ArgumentParser(description="Construye el índice de apuntes Markdown.")
    parser.add_argument("--knowledge-root", default="knowledge", help="Carpeta raíz de la base de conocimiento.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Fichero JSON de salida.")
    args = parser.parse_args()

    knowledge_root = Path(args.knowledge_root)
    output_path = Path(args.output)

    if not knowledge_root.exists():
        raise FileNotFoundError(f"No existe la carpeta de conocimiento: {knowledge_root}")

    notes = build_index(knowledge_root, output_path)
    print(f"Índice generado con éxito en: {output_path}")
    print(f"Total de apuntes indexados: {len(notes)}")


if __name__ == "__main__":
    main()