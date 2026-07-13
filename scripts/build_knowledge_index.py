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
from pathlib import Path
from typing import Any

EXCLUDED_PARTS = {"_templates", "sources"}
DEFAULT_OUTPUT = Path("apps/studyassistant/data/knowledge_index.json")


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


def parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown

    end = markdown.find("\n---", 4)
    if end == -1:
        return {}, markdown

    raw = markdown[4:end].strip("\n")
    body = markdown[end + 4 :].lstrip("\n")
    metadata: dict[str, Any] = {}
    current_key: str | None = None

    for line in raw.splitlines():
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

    return metadata, body


def strip_markdown(markdown: str) -> str:
    text = re.sub(r"```.*?```", " ", markdown, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_>#|-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_headings(body: str) -> list[dict[str, Any]]:
    headings: list[dict[str, Any]] = []
    for line in body.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            headings.append({"level": len(match.group(1)), "text": match.group(2).strip()})
    return headings


def first_non_empty_paragraph(body: str, max_length: int = 260) -> str:
    for paragraph in re.split(r"\n\s*\n", body):
        cleaned = strip_markdown(paragraph)
        if cleaned:
            return cleaned if len(cleaned) <= max_length else cleaned[: max_length - 3].rstrip() + "..."
    return ""


def should_include(path: Path, knowledge_root: Path) -> bool:
    if path.suffix.lower() != ".md":
        return False
    relative_parts = set(path.relative_to(knowledge_root).parts)
    return not bool(relative_parts & EXCLUDED_PARTS)


def build_index(knowledge_root: Path, output_path: Path) -> list[dict[str, Any]]:
    notes: list[dict[str, Any]] = []

    for path in sorted(knowledge_root.rglob("*.md")):
        if not should_include(path, knowledge_root):
            continue

        raw = path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(raw)
        headings = extract_headings(body)
        title = metadata.get("title") or (headings[0]["text"] if headings else path.stem.replace("-", " ").title())
        note_id = metadata.get("id") or path.stem

        notes.append({
            "id": note_id,
            "title": title,
            "path": path.as_posix(),
            "relative_path": path.relative_to(knowledge_root).as_posix(),
            "processes": metadata.get("processes", []),
            "official_topic": metadata.get("official_topic"),
            "source_ids": metadata.get("source_ids", []),
            "tags": metadata.get("tags", []),
            "status": metadata.get("status"),
            "created_at": metadata.get("created_at"),
            "last_reviewed": metadata.get("last_reviewed"),
            "ai_generated": metadata.get("ai_generated"),
            "ai_sources": metadata.get("ai_sources", []),
            "needs_human_review": metadata.get("needs_human_review"),
            "headings": headings,
            "excerpt": first_non_empty_paragraph(body),
            "content_text": strip_markdown(body),
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")
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
    print(f"Índice generado: {output_path}")
    print(f"Apuntes indexados: {len(notes)}")


if __name__ == "__main__":
    main()
