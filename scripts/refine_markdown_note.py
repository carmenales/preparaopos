#!/usr/bin/env python3
"""Refina Markdown extraído de forma conservadora.

Reglas:
- elimina ruido de OCR repetido o marcadores de página,
- normaliza viñetas raras a '- ',
- une líneas partidas por salto de renglón,
- añade una línea en blanco antes de listas cuando el párrafo anterior termina en ':',
- no inventa títulos ni reestructura el documento.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PAGE_MARKER_RE = re.compile(r"^\s*#{1,6}\s*Página\s+\d+\s*$", re.IGNORECASE)
NOISE_RE = re.compile(
    r"^\s*#{1,6}\s*(Centro de Estudios TIC|CentrodeEstudiosTIC|Centro de Estudios|Cuerpo de Gestión de Sistemas e Informática de la Administración del Estado|Página\s+\d+)\b",
    re.IGNORECASE,
)
BULLET_RE = re.compile(r"^\s*[●•◦▪▫‣*]\s*(.+?)\s*$")
HEADING_RE = re.compile(r"^\s*(#{1,6}\s+)?(\d+(?:\.\d+)*\.?\s+.+|[IVXLCDM]+(?:\.[IVXLCDM]+)*\.?\s+.+)$")
ENUM_START_RE = re.compile(r"^\s*(?:[a-zA-ZÁÉÍÓÚÜÑ]\.|[a-zA-ZÁÉÍÓÚÜÑ]\)|\d+\.|\d+\))\s+")
PUNCT_END = (".", ":", ";", "?", "!", "…")
CLOSE_END = ("),", ")]", "}", "»", "”", ")", "]")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00ad", "")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip("\n") + "\n"


def is_noise(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if PAGE_MARKER_RE.match(s):
        return True
    if NOISE_RE.match(s):
        return True
    if s.lower() in {"mostrar menos", "mostrar más"}:
        return True
    return False


def is_heading(line: str) -> bool:
    s = line.strip()
    return s.startswith("#") or bool(HEADING_RE.match(s))


def normalize_bullet(line: str) -> str:
    m = BULLET_RE.match(line)
    if m:
        return f"- {m.group(1).strip()}"
    s = line.strip()
    if s.startswith("-"):
        return "- " + s[1:].strip()
    return line.rstrip()


def should_join(prev: str, curr: str) -> bool:
    p = prev.rstrip()
    c = curr.lstrip()
    if not p or not c:
        return False
    if is_heading(c) or BULLET_RE.match(c) or c.startswith("-") or c.startswith("|") or c.startswith(">"):
        return False
    if p.endswith(PUNCT_END) or p.endswith(CLOSE_END):
        return False
    if p.endswith("-"):
        return True
    if p[-1].islower() or p[-1].isdigit() or p[-1] in (")", "]", "}", "º", "ª"):
        return True
    if c[0].islower() or c[0].isdigit():
        return True
    if re.search(r"[a-záéíóúñü]$", p) and re.search(r"^[A-ZÁÉÍÓÚÑÜ]", c):
        return True
    return False


def join_wrapped_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    buffer: list[str] = []

    def flush_buffer() -> None:
        nonlocal buffer
        if not buffer:
            return
        paragraph = " ".join(x.strip() for x in buffer if x.strip())
        paragraph = re.sub(r"\s+", " ", paragraph).strip()
        if paragraph:
            out.append(paragraph)
        buffer = []

    for raw in lines:
        line = raw.rstrip()
        s = line.strip()

        if not s:
            flush_buffer()
            if out and out[-1] != "":
                out.append("")
            continue

        if is_noise(line):
            continue

        if is_heading(line):
            flush_buffer()
            if out and out[-1] != "":
                out.append("")
            out.append(line.strip())
            continue

        if BULLET_RE.match(line) or s.startswith("-"):
            flush_buffer()
            out.append(normalize_bullet(line))
            continue

        if s.startswith("|") or s.startswith(">"):
            flush_buffer()
            out.append(line)
            continue

        if not buffer:
            buffer.append(s)
            continue

        if should_join(buffer[-1], s):
            buffer.append(s)
        else:
            flush_buffer()
            buffer.append(s)

    flush_buffer()
    return out


def add_blank_line_before_lists(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        s = line.strip()
        if s.startswith("-") and out:
            prev = out[-1].strip()
            if prev and prev.endswith(":") and prev != "":
                if out[-1] != "":
                    out.append("")
        out.append(line)
    return out


def refine_markdown(text: str) -> str:
    text = normalize_text(text)
    lines = text.splitlines()
    lines = join_wrapped_lines(lines)
    lines = add_blank_line_before_lists(lines)
    result = "\n".join(lines)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip() + "\n"


def process_file(input_path: Path, output_path: Path) -> None:
    write_text(output_path, refine_markdown(read_text(input_path)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Refina Markdown extraído de forma conservadora.")
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

    md_files = sorted(p for p in input_path.rglob("*.md") if p.is_file())
    if not md_files:
        print(f"No se han encontrado .md en {input_path}")
        return

    for source in md_files:
        rel = source.relative_to(input_path)
        target = output_path / rel
        if target.exists() and not args.overwrite:
            print(f"[omitido] {rel}")
            continue
        process_file(source, target)
        print(f"[ok] {rel}")


if __name__ == "__main__":
    main()
