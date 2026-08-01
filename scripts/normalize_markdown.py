#!/usr/bin/env python3
"""
Normaliza Markdown extraído de PDFs/PPTX para que quede más legible antes de la revisión manual.

Hace tareas seguras y reversibles:
- elimina residuos típicos de extracción (páginas, cabeceras obvias, marcadores vacíos)
- compacta espacios y líneas en blanco
- reconstruye listas de siglas en tablas Markdown de 2 columnas
- convierte bloques muy repetitivos de texto en párrafos más legibles

No resume ni inventa contenido.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SIGLAS_INTRO_RE = re.compile(r"^\s*Las siglas empleadas en este documento son las siguientes\s*:??\s*$", re.IGNORECASE)
PAGE_MARKER_RE = re.compile(r"^\s*#{1,6}\s*Página\s+\d+\s*$", re.IGNORECASE)
SIMPLE_HEADER_RE = re.compile(r"^\s*#{2,6}\s*(Centro de Estudios TIC|CentrodeEstudiosTIC|Centro de Estudios|Página\s+\d+)\b", re.IGNORECASE)
TOC_LINE_RE = re.compile(r"^\s*(\d+(\.\d+)*)\s+(.+?)\s+\d+\s*$")
SIGLA_RE = re.compile(r"^[A-ZÁÉÍÓÚÜÑ0-9]{2,15}[a-z]?$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\t\f\v]+", " ", text)
    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def remove_obvious_extraction_noise(text: str) -> str:
    lines = text.splitlines()
    cleaned: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned.append("")
            continue

        if PAGE_MARKER_RE.match(stripped):
            continue

        if SIMPLE_HEADER_RE.match(stripped):
            continue

        if stripped.lower() in {"mostrar menos", "mostrar más"}:
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def looks_like_sigla_definition_row(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if len(s) > 40:
        return False
    if " " in s:
        return False
    return bool(SIGLA_RE.match(s))


def maybe_clean_signatures(sigla: str) -> str:
    sigla = sigla.strip()
    sigla = re.sub(r"\s+", "", sigla)
    return sigla


def convert_acronym_blocks_to_table(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if SIGLAS_INTRO_RE.match(stripped):
            out.append("## Siglas")
            out.append("")
            i += 1

            entries: list[tuple[str, str]] = []
            pending_sigla: str | None = None

            while i < len(lines):
                current = lines[i].strip()
                if not current:
                    if pending_sigla is not None:
                        pending_sigla = pending_sigla
                    i += 1
                    continue

                if current.startswith("#"):
                    break

                if looks_like_sigla_definition_row(current):
                    pending_sigla = maybe_clean_signatures(current)
                    i += 1
                    if i < len(lines):
                        definition = lines[i].strip()
                        if definition and not looks_like_sigla_definition_row(definition) and not definition.startswith("#"):
                            entries.append((pending_sigla, definition))
                            pending_sigla = None
                            i += 1
                            continue
                    if pending_sigla is not None:
                        entries.append((pending_sigla, ""))
                        pending_sigla = None
                    continue

                if pending_sigla is not None:
                    entries.append((pending_sigla, current))
                    pending_sigla = None
                    i += 1
                    continue

                break

            if entries:
                out.append("| Sigla | Significado |")
                out.append("| --- | --- |")
                for sigla, definition in entries:
                    definition = re.sub(r"\s+", " ", definition).strip()
                    out.append(f"| {sigla} | {definition} |")
                out.append("")
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def collapse_broken_paragraphs(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    buffer: list[str] = []

    def flush_buffer() -> None:
        if not buffer:
            return
        paragraph = " ".join(part.strip() for part in buffer if part.strip())
        paragraph = re.sub(r"\s+", " ", paragraph).strip()
        if paragraph:
            out.append(paragraph)
        buffer.clear()

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_buffer()
            out.append("")
            continue

        if stripped.startswith("#") or stripped.startswith("|") or stripped.startswith("-") or stripped.startswith(">"):
            flush_buffer()
            out.append(line)
            continue

        if TOC_LINE_RE.match(stripped):
            flush_buffer()
            out.append(line)
            continue

        buffer.append(stripped)

    flush_buffer()
    return "\n".join(out)


def dedupe_repeated_lines(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    prev = None
    for line in lines:
        stripped = line.strip()
        if stripped and prev is not None and stripped == prev:
            continue
        out.append(line)
        if stripped:
            prev = stripped
    return "\n".join(out)


def normalize_markdown(content: str) -> str:
    content = normalize_whitespace(content)
    content = remove_obvious_extraction_noise(content)
    content = convert_acronym_blocks_to_table(content)
    content = collapse_broken_paragraphs(content)
    content = dedupe_repeated_lines(content)
    content = normalize_whitespace(content)
    return content


def process_file(input_path: Path, output_path: Path) -> None:
    content = read_text(input_path)
    normalized = normalize_markdown(content)
    write_text(output_path, normalized)


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def main() -> None:
    parser = argparse.ArgumentParser(description="Normaliza Markdown extraído de PDFs/PPTX.")
    parser.add_argument("input", help="Archivo .md o carpeta de entrada")
    parser.add_argument("output", help="Archivo .md o carpeta de salida")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescribir archivos existentes")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if input_path.is_file():
        if output_path.exists() and output_path.is_dir():
            target = output_path / input_path.name
        else:
            target = output_path
        if target.exists() and not args.overwrite:
            raise FileExistsError(f"Ya existe: {target}. Usa --overwrite para sobrescribir.")
        process_file(input_path, target)
        return

    if not input_path.exists() or not input_path.is_dir():
        raise FileNotFoundError(f"No existe la carpeta de entrada: {input_path}")

    files = iter_markdown_files(input_path)
    if not files:
        print(f"No se han encontrado .md en {input_path}")
        return

    for source in files:
        rel = source.relative_to(input_path)
        target = output_path / rel
        if target.exists() and not args.overwrite:
            print(f"[omitido] {rel}")
            continue
        process_file(source, target)
        print(f"[ok] {rel}")


if __name__ == "__main__":
    main()
