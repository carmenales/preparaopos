#!/usr/bin/env python3
"""
Refina Markdown extraído para acercarlo más a una nota curada.

Entrada típica:
- Markdown bruto o normalizado generado por extract_pdf_text.py / normalize_markdown.py

Salida:
- Markdown más limpio, con menos falsos encabezados, mejores párrafos y
  tablas simples de siglas convertidas a Markdown.

Este script no inventa contenido ni resume.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

HEADER_CANDIDATE_RE = re.compile(r"^#{2,6}\s+(.+)$")
LONG_SENTENCE_RE = re.compile(r"[.!?;:]\s")
SECTION_RE = re.compile(r"^\d+(\.\d+)*\s+[A-ZÁÉÍÓÚÑ].+$")
SIGLAS_INTRO_RE = re.compile(r"^\s*Las siglas empleadas en este documento son las siguientes\s*:??\s*$", re.IGNORECASE)
PAGE_HEADER_RE = re.compile(r"^#{1,6}\s*Página\s+\d+\s*$", re.IGNORECASE)
NOISE_HEADER_RE = re.compile(r"^#{1,6}\s*(Centro de Estudios TIC|CentrodeEstudiosTIC|Centro de Estudios|Cuerpo de Gestión de Sistemas e Informática de la Administración del Estado)\b", re.IGNORECASE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def normalize_spaces(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def title_score(text: str) -> int:
    s = text.strip()
    if not s:
        return -100
    score = 0
    if len(s) <= 90:
        score += 2
    elif len(s) <= 140:
        score += 1
    else:
        score -= 3
    if SECTION_RE.match(s):
        score += 3
    if s.isupper():
        score += 1
    if LONG_SENTENCE_RE.search(s):
        score -= 4
    if len(s.split()) > 14:
        score -= 2
    if re.search(r"\b(en este|como|que|para|cuando|si bien|además|por tanto)\b", s, re.IGNORECASE):
        score -= 2
    return score


def is_probable_heading(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if PAGE_HEADER_RE.match(s):
        return False
    if NOISE_HEADER_RE.match(s):
        return False
    if s.startswith(">"):
        return False
    if s.startswith("|"):
        return False
    if SIGLAS_INTRO_RE.match(s):
        return False
    return title_score(s) >= 2


def collapse_broken_paragraphs(lines: list[str]) -> list[str]:
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
            if out and out[-1] != "":
                out.append("")
            continue

        if stripped.startswith("#") or stripped.startswith("-") or stripped.startswith(">") or stripped.startswith("|"):
            flush_buffer()
            out.append(line)
            continue

        if is_probable_heading(stripped):
            flush_buffer()
            out.append(f"### {stripped.lstrip('# ').strip()}")
            continue

        buffer.append(stripped)

    flush_buffer()
    return out


def convert_sigla_block(lines: list[str]) -> list[str]:
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
            current_sigla: str | None = None

            while i < len(lines):
                s = lines[i].strip()
                if not s:
                    i += 1
                    continue
                if s.startswith("#"):
                    break
                if re.match(r"^[A-ZÁÉÍÓÚÜÑ0-9]{2,15}[a-z]?$", s) and len(s) <= 16:
                    current_sigla = s
                    i += 1
                    continue
                if current_sigla is not None:
                    entries.append((current_sigla, s))
                    current_sigla = None
                i += 1

            if entries:
                out.append("| Sigla | Significado |")
                out.append("| --- | --- |")
                for sigla, meaning in entries:
                    out.append(f"| {sigla} | {meaning} |")
                out.append("")
            continue

        out.append(line)
        i += 1

    return out


def remove_repeated_noise(lines: list[str]) -> list[str]:
    out: list[str] = []
    prev = None
    for line in lines:
        s = line.strip()
        if s and prev == s:
            continue
        out.append(line)
        if s:
            prev = s
    return out


def refine_markdown(text: str) -> str:
    text = normalize_spaces(text)
    lines = text.splitlines()
    lines = [line for line in lines if not PAGE_HEADER_RE.match(line.strip())]
    lines = [line for line in lines if not NOISE_HEADER_RE.match(line.strip())]
    lines = convert_sigla_block(lines)
    lines = collapse_broken_paragraphs(lines)
    lines = remove_repeated_noise(lines)
    return normalize_spaces("\n".join(lines))


def process_file(input_path: Path, output_path: Path) -> None:
    write_text(output_path, refine_markdown(read_text(input_path)))


def iter_md_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def main() -> None:
    parser = argparse.ArgumentParser(description="Refina Markdown extraído para aproximarlo a una nota curada.")
    parser.add_argument("input", help="Archivo .md o carpeta de entrada")
    parser.add_argument("output", help="Archivo .md o carpeta de salida")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescribir archivos existentes")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if input_path.is_file():
        target = output_path
        if output_path.exists() and output_path.is_dir():
            target = output_path / input_path.name
        if target.exists() and not args.overwrite:
            raise FileExistsError(f"Ya existe: {target}. Usa --overwrite para sobrescribir.")
        process_file(input_path, target)
        return

    if not input_path.exists() or not input_path.is_dir():
        raise FileNotFoundError(f"No existe la carpeta de entrada: {input_path}")

    files = iter_md_files(input_path)
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
