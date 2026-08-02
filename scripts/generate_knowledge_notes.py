#!/usr/bin/env python3
"""Genera apuntes Markdown consumibles a partir de ficheros fuente o Markdown previo.

Casos de uso:
- aplicar una plantilla de frontmatter a apuntes ya preparados,
- inferir metadatos mínimos por ruta,
- generar salidas por lotes manteniendo estructura de carpetas.

Diseño conservador:
- no reescribe el cuerpo salvo insertar el texto fuente bajo la plantilla,
- no intenta normalizar ni refinar Markdown,
- deja los metadatos explícitos para que StudyAssistant y el indexador los consuman.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

TEMPLATE_DEFAULT = Path("knowledge/_template/apunte.md")
SUPPORTED_EXTENSIONS = {".md", ".txt"}


@dataclass(frozen=True)
class NoteMetadata:
    id: str
    title: str
    type: str
    status: str
    processes: list[str]
    official_topic: str
    source_ids: list[str]
    tags: list[str]
    created_at: str
    last_reviewed: str | None
    origin: str
    academy: str
    ai_generated: bool
    ai_cleaned: bool
    ai_sources: list[str]
    needs_human_review: bool


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("/", "-")
    value = re.sub(r"[^a-z0-9áéíóúüñ\-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def split_frontmatter(text: str) -> tuple[list[str], str]:
    if not text.startswith("---\n"):
        return [], text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return [], text
    return parts[1].splitlines(), parts[2].lstrip("\n")


def parse_scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def load_template(path: Path) -> list[str]:
    frontmatter_lines, _ = split_frontmatter(read_text(path))
    if not frontmatter_lines:
        raise ValueError(f"La plantilla {path} no contiene frontmatter YAML válido.")
    return frontmatter_lines


def default_title_from_path(source_path: Path) -> str:
    title = source_path.stem.replace("_", " ").replace("-", " ").strip()
    title = re.sub(r"\s+", " ", title)
    return title or source_path.stem


def infer_process(relative_parts: tuple[str, ...], fallback: str) -> str:
    if relative_parts:
        return relative_parts[0]
    return fallback


def infer_academy(relative_parts: tuple[str, ...]) -> str:
    if len(relative_parts) >= 2:
        return relative_parts[1]
    return ""


def infer_official_topic(source_path: Path, explicit_topic: str | None) -> str:
    if explicit_topic is not None:
        return explicit_topic
    match = re.search(r"(?:tema|topic)\s*([\w.-]+)", source_path.stem, re.IGNORECASE)
    if match:
        return match.group(1)
    return ""


def parse_list_arg(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def build_metadata(
    source_path: Path,
    input_root: Path,
    title: str | None,
    process: str | None,
    academy: str | None,
    official_topic: str | None,
    origin: str,
    status: str,
    ai_generated: bool,
    ai_cleaned: bool,
    needs_human_review: bool,
    tags: list[str],
    source_ids: list[str],
    ai_sources: list[str],
) -> NoteMetadata:
    relative = source_path.relative_to(input_root)
    parts = relative.parts[:-1] if source_path.is_file() and source_path.suffix.lower() in SUPPORTED_EXTENSIONS else relative.parts
    note_title = title or default_title_from_path(source_path)
    process_value = process or infer_process(parts, "age")
    academy_value = academy or infer_academy(parts)
    official_topic_value = infer_official_topic(source_path, official_topic)
    return NoteMetadata(
        id=slugify(source_path.stem),
        title=note_title,
        type="apunte",
        status=status,
        processes=[process_value],
        official_topic=official_topic_value,
        source_ids=source_ids,
        tags=tags,
        created_at=date.today().isoformat(),
        last_reviewed=None,
        origin=origin,
        academy=academy_value,
        ai_generated=ai_generated,
        ai_cleaned=ai_cleaned,
        ai_sources=ai_sources,
        needs_human_review=needs_human_review,
    )


def render_scalar(value: str | None) -> str:
    if value is None:
        return "null"
    return f'"{value}"'


def render_list(values: Iterable[str]) -> list[str]:
    values = list(values)
    if not values:
        return ["[]"]
    return ["", *[f'  - "{item}"' for item in values]]


def render_frontmatter(template_lines: list[str], metadata: NoteMetadata) -> list[str]:
    output: list[str] = []
    for line in template_lines:
        key = line.split(":", 1)[0].strip()
        if key == "id":
            output.append(f'id: "{metadata.id}"')
        elif key == "title":
            output.append(f'title: "{metadata.title}"')
        elif key == "type":
            output.append(f'type: "{metadata.type}"')
        elif key == "status":
            output.append(f'status: "{metadata.status}"')
        elif key == "processes":
            output.append("processes:")
            output.extend(render_list(metadata.processes)[1:])
        elif key == "official_topic":
            output.append(f'official_topic: {render_scalar(metadata.official_topic)}')
        elif key == "source_ids":
            output.append("source_ids: []")
        elif key == "tags":
            output.append("tags: []" if not metadata.tags else "tags:")
            if metadata.tags:
                output.extend([f'  - "{tag}"' for tag in metadata.tags])
        elif key == "created_at":
            output.append(f'created_at: "{metadata.created_at}"')
        elif key == "last_reviewed":
            output.append("last_reviewed: null")
        elif key == "origin":
            output.append(f'origin: "{metadata.origin}"')
        elif key == "academy":
            output.append(f'academy: "{metadata.academy}"')
        elif key == "ai_generated":
            output.append(f'ai_generated: {str(metadata.ai_generated).lower()}')
        elif key == "ai_cleaned":
            output.append(f'ai_cleaned: {str(metadata.ai_cleaned).lower()}')
        elif key == "ai_sources":
            output.append("ai_sources: []" if not metadata.ai_sources else "ai_sources:")
            if metadata.ai_sources:
                output.extend([f'  - "{src}"' for src in metadata.ai_sources])
        elif key == "needs_human_review":
            output.append(f'needs_human_review: {str(metadata.needs_human_review).lower()}')
        else:
            output.append(line)
    return output


def build_note(template_path: Path, metadata: NoteMetadata, body: str) -> str:
    template_lines = load_template(template_path)
    rendered_frontmatter = render_frontmatter(template_lines, metadata)
    body = body.lstrip("\n")
    return "---\n" + "\n".join(rendered_frontmatter) + "\n---\n\n" + f"# {metadata.title}\n\n" + body.rstrip() + "\n"


def collect_inputs(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    return sorted(p for p in input_path.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS)


def process_file(
    source_path: Path,
    input_root: Path,
    output_root: Path,
    template_path: Path,
    origin: str,
    status: str,
    process: str | None,
    academy: str | None,
    official_topic: str | None,
    ai_generated: bool,
    ai_cleaned: bool,
    needs_human_review: bool,
    tags: list[str],
    source_ids: list[str],
    ai_sources: list[str],
    title: str | None,
    overwrite: bool,
) -> Path:
    metadata = build_metadata(
        source_path=source_path,
        input_root=input_root,
        title=title,
        process=process,
        academy=academy,
        official_topic=official_topic,
        origin=origin,
        status=status,
        ai_generated=ai_generated,
        ai_cleaned=ai_cleaned,
        needs_human_review=needs_human_review,
        tags=tags,
        source_ids=source_ids,
        ai_sources=ai_sources,
    )
    relative = source_path.relative_to(input_root).with_suffix(".md")
    output_path = output_root / relative
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Ya existe: {output_path}. Usa --overwrite para reemplazarlo.")
    body = read_text(source_path)
    write_text(output_path, build_note(template_path, metadata, body))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera apuntes Markdown consumibles con frontmatter.")
    parser.add_argument("input_path", help="Archivo o carpeta de entrada")
    parser.add_argument("output_root", help="Carpeta raíz de salida")
    parser.add_argument("--template", default=str(TEMPLATE_DEFAULT), help="Ruta de la plantilla de apunte.")
    parser.add_argument("--origin", default="academia", choices=["academia", "community", "ai-generated"], help="Procedencia del apunte.")
    parser.add_argument("--academy", default=None, help="Academia o fuente de procedencia.")
    parser.add_argument("--process", default=None, help="Proceso destino, por ejemplo age.")
    parser.add_argument("--official-topic", default=None, help="Tema oficial o identificador equivalente.")
    parser.add_argument("--status", default="borrador", help="Estado del apunte.")
    parser.add_argument("--title", default=None, help="Título explícito del apunte.")
    parser.add_argument("--tags", default="", help="Lista de tags separada por comas.")
    parser.add_argument("--source-ids", default="", help="IDs de fuentes separadas por comas.")
    parser.add_argument("--ai-sources", default="", help="Fuentes IA separadas por comas.")
    parser.add_argument("--ai-generated", action="store_true", help="Marca el apunte como generado por IA.")
    parser.add_argument("--ai-cleaned", action="store_true", default=True, help="Marca el apunte como limpiado con IA.")
    parser.add_argument("--not-ai-cleaned", dest="ai_cleaned", action="store_false", help="Marca el apunte como no limpiado con IA.")
    parser.add_argument("--needs-human-review", action="store_true", default=True, help="Marca el apunte como pendiente de revisión humana.")
    parser.add_argument("--no-human-review", dest="needs_human_review", action="store_false", help="Marca el apunte como revisado.")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescribe si el destino ya existe.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_path)
    output_root = Path(args.output_root)
    template_path = Path(args.template)

    if not input_path.exists():
        raise FileNotFoundError(f"No existe la ruta de entrada: {input_path}")
    if not template_path.exists():
        raise FileNotFoundError(f"No existe la plantilla: {template_path}")

    inputs = collect_inputs(input_path)
    if not inputs:
        print("No se han encontrado ficheros compatibles.")
        return

    input_root = input_path if input_path.is_dir() else input_path.parent
    tags = parse_list_arg(args.tags)
    source_ids = parse_list_arg(args.source_ids)
    ai_sources = parse_list_arg(args.ai_sources)

    for source in inputs:
        out = process_file(
            source_path=source,
            input_root=input_root,
            output_root=output_root,
            template_path=template_path,
            origin=args.origin,
            status=args.status,
            process=args.process,
            academy=args.academy,
            official_topic=args.official_topic,
            ai_generated=args.ai_generated,
            ai_cleaned=args.ai_cleaned,
            needs_human_review=args.needs_human_review,
            tags=tags,
            source_ids=source_ids,
            ai_sources=ai_sources,
            title=args.title,
            overwrite=args.overwrite,
        )
        print(f"[ok] {source} -> {out}")


if __name__ == "__main__":
    main()
