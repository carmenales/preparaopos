#!/usr/bin/env python3
"""
Normaliza Markdown extraído de PDFs/PPTX con reglas conservadoras.

Objetivo:
- limpiar ruido obvio,
- compactar espacios,
- eliminar páginas/títulos de página,
- convertir bloques de siglas muy claros en tabla,
- deduplicar líneas repetidas.

No intenta reconstruir párrafos ni reordenar contenido.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
import string


from collections import Counter

SIGLAS_INTRO_RE = re.compile(r"^\s*Las siglas empleadas en este documento son las siguientes\s*:??\s*$", re.IGNORECASE)
PAGE_MARKER_RE = re.compile(
    r"^\s*#{0,6}\s*(?:P[áa]g(?:ina)?\.?|Diapositiva)\s*\d+\s*(?:(?:\||/|de|-)\s*\d+)?\s*$",
    re.IGNORECASE,
)
LONE_PAGE_NUMBER_RE = re.compile(
    r"^\s*#{0,6}\s*\d+\s*(?:(?:\||/|de)\s*\d+)\s*$",
    re.IGNORECASE,
)
LEGAL_BOILERPLATE_RE = re.compile(
    r"^\s*(?:Actualizado\s+(?:a|en|el|de)?\s*:?\s*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}"
    r"|Actualizado\s+(?:a|en|el|de)?\s*:?\s*[a-záéíóú]+\s+de\s+\d{4}"
    r"|Fecha\s*:?\s*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}"
    r"|Edici[óo]n\s+\d{4}"
    r"|Convocatoria\s+\d{4}"
    r"|https?://\S+"
    r"|www\.[a-z0-9\-\.]+\.[a-z]{2,}"
    r"|Dep[óo]sito\s+legal[^\n]*"
    r"|Copyright\s+[^\n]*"
    r"|©[^\n]*"
    r"|Todos\s+los\s+derechos\s+reservados"
    r"|Prohibida\s+(?:su\s+)?reproducci[óo]n.*)\s*$",
    re.IGNORECASE,
)
SIGLA_RE = re.compile(r"^[A-ZÁÉÍÓÚÜÑ0-9]{2,15}[a-z]?$")

HEADER_FOOTER_EDGE_LINES = 2
HEADER_FOOTER_MIN_FRACTION = 0.5
HEADER_FOOTER_MIN_OCCURRENCES = 2


def _normalize_for_comparison(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip().lower())


def _split_into_pages(text: str) -> list[list[str]]:
    lines = text.splitlines()
    pages: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        if PAGE_MARKER_RE.match(line.strip()):
            if current:
                pages.append(current)
            current = [line]
        else:
            current.append(line)

    if current:
        pages.append(current)

    return pages if len(pages) > 1 else [lines]


def _detect_repeated_header_footer_lines(pages: list[list[str]]) -> set[str]:
    if len(pages) < 2:
        return set()

    counter: Counter[str] = Counter()

    for page_lines in pages:
        non_empty = [line.strip() for line in page_lines if line.strip()]
        candidates = non_empty[:HEADER_FOOTER_EDGE_LINES] + non_empty[-HEADER_FOOTER_EDGE_LINES:]
        seen_this_page: set[str] = set()
        for candidate in candidates:
            normalized = _normalize_for_comparison(candidate)
            if normalized and normalized not in seen_this_page:
                counter[normalized] += 1
                seen_this_page.add(normalized)

    threshold = max(HEADER_FOOTER_MIN_OCCURRENCES, int(len(pages) * HEADER_FOOTER_MIN_FRACTION))
    return {text for text, count in counter.items() if count >= threshold}


def remove_repeated_headers_footers(text: str) -> str:
    pages = _split_into_pages(text)
    repeated = _detect_repeated_header_footer_lines(pages)

    if not repeated:
        return text

    lines = text.splitlines()
    cleaned = [line for line in lines if _normalize_for_comparison(line) not in repeated]
    return "\n".join(cleaned)


_HEADING_RE = re.compile(r"^(#{1,6}\s+|\d+(\.\d+)*\.?\s)")
_LIST_RE = re.compile(r"^(\s*[-*+•·●○▪▫⁃–—\uf0b7\uf0a7\uf0d8]\s+|\s*\d+\.\s+)")
_TABLE_RE = re.compile(r"^\|.*\|$")


def _is_joinable(a: str, b: str) -> bool:
    a = a.rstrip()
    b = b.lstrip()

    if not a or not b:
        return False

    if _HEADING_RE.match(a) or _HEADING_RE.match(b):
        return False

    if _LIST_RE.match(a) or _LIST_RE.match(b):
        return False

    if _TABLE_RE.match(a) or _TABLE_RE.match(b):
        return False

    if a.endswith((":", ";", ".", "?", "!", "|")):
        return False

    if b.startswith(("#", "-", "*", "•", "·", "●", "|", ">")):
        return False

    return True


def join_broken_paragraphs(text: str) -> str:
    lines = text.splitlines()

    out = []
    i = 0

    while i < len(lines):
        current = lines[i].rstrip()

        if not current.strip():
            out.append("")
            i += 1
            continue

        while i + 1 < len(lines):
            nxt = lines[i + 1].strip()

            if not _is_joinable(current, nxt):
                break

            current += " " + nxt
            i += 1

        out.append(current)
        i += 1

    return "\n".join(out)


def fix_broken_lists(text: str) -> str:
    lines = text.splitlines()

    out = []

    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        if line.strip() in {"-", "*", "•"} and i + 1 < len(lines):
            out.append("- " + lines[i + 1].strip())
            i += 2
            continue

        if line.strip().startswith("•"):
            out.append("- " + line.strip()[1:].strip())
            i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


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


def clean_inline_noise(text: str) -> str:
    """Limpia ruido incrustado como fechas de actualización, números de página y academias."""
    text = text.replace("\u200b", "").replace("\u00a0", " ")

    # 1. Fechas de actualización y convocatorias
    text = re.sub(r"\bactualizado\s+(?:a|en|el|de)?\s*:?\s*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b", "", text, flags=re.I)
    text = re.sub(r"\bactualizado\s+(?:a|en|el|de)?\s*:?\s*[a-záéíóú]+\s+de\s+\d{4}\b", "", text, flags=re.I)
    text = re.sub(r"\bactualizado\s*:?\s*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b", "", text, flags=re.I)
    text = re.sub(r"\bfecha\s*:?\s*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b", "", text, flags=re.I)
    text = re.sub(r"\bconvocatoria\s+\d{4}\b", "", text, flags=re.I)
    text = re.sub(r"\bedici[óo]n\s+\d{4}\b", "", text, flags=re.I)

    # 2. URLs y enlaces web genéricos
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\bwww\.[a-z0-9\-\.]+\.[a-z]{2,}\b", "", text, flags=re.I)

    # 3. Marcadores de paginación explícitos ('Página 1 | 12', 'Pág. 3 / 10', 'Página1 | 12', 'Página1')
    text = re.sub(r"\bp[áa]g(?:ina)?\.?\s*\d+\s*(?:\||/|de)\s*\d+\b", "", text, flags=re.I)
    text = re.sub(r"\bp[áa]g\.\s*\d+\b", "", text, flags=re.I)
    text = re.sub(r"\bp[áa]gina\d+\b", "", text, flags=re.I)

    # Marcador de página prefijado al inicio de línea o heading (ej. '^Página1 | 12 ## ...')
    text = re.sub(r"^\s*p[áa]g(?:ina)?\.?\s*\d+\s*(?:(?:\||/|de|-)\s*\d+)?\s*", "", text, flags=re.I)

    # 4. Fracciones de página sueltas con barras o pipes ('1 | 12')
    text = re.sub(r"\b\d{1,3}\s*\|\s*\d{1,3}\b", "", text)

    # 5. Símbolos residuales de bordes
    text = re.sub(r"\s*\|\s*\d+\s*$", "", text)
    text = re.sub(r"\|\s*\d+\b", "", text)
    text = re.sub(r"\s*\|\s*$", "", text)
    text = re.sub(r"^\s*\|\s*", "", text)
    text = re.sub(r"\s*-\s*$", "", text)
    if re.match(r"^[\s\-\|]+$", text):
        return ""

    # 6. Normalizar headings con ruido al inicio (ej. 'Página1 | 12 ## Título' -> '## Título')
    if not text.strip().startswith("#") and re.search(r"\s(#{1,6}\s+)", text):
        m = re.search(r"(#{1,6}\s+.*)", text)
        if m:
            text = m.group(1).strip()

    # Si solo quedan almohadillas (como '###' derivado de '### Página2 | 12')
    if re.match(r"^#{1,6}\s*$", text.strip()):
        return ""

    text = re.sub(r"[ \t]+", " ", text).strip()
    return text


def is_pure_page_or_header_noise(text: str) -> bool:
    """Detecta si una línea o bloque es únicamente un marcador de página o cabecera/pie residual."""
    s = text.strip()
    if not s:
        return True
    if re.match(r"^\s*#{0,6}\s*(?:p[áa]g(?:ina)?\.?\s*\d+|\d+)\s*(?:(?:\||/|de|-)\s*\d+)?\s*$", s, re.I):
        return True
    if re.match(r"^\s*#{0,6}\s*\d+\s*$", s):
        return True
    if LEGAL_BOILERPLATE_RE.match(s):
        return True
    if re.match(r"^\s*actualizado\s+[^\n]+$", s, re.I):
        return True
    return False


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

        if LONE_PAGE_NUMBER_RE.match(stripped):
            continue

        if LEGAL_BOILERPLATE_RE.match(stripped):
            continue

        if is_pure_page_or_header_noise(stripped):
            continue

        if stripped.lower() in {"mostrar menos", "mostrar más"}:
            continue

        cleaned_line = clean_inline_noise(line)
        if not cleaned_line.strip() or is_pure_page_or_header_noise(cleaned_line):
            continue

        cleaned.append(cleaned_line)

    return "\n".join(cleaned)


def looks_like_sigla_definition_row(line: str) -> bool:
    s = line.strip()
    return bool(s and len(s) <= 20 and " " not in s and SIGLA_RE.match(s))


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
            while i < len(lines):
                current = lines[i].strip()
                if not current:
                    i += 1
                    continue
                if current.startswith("#"):
                    break
                if current.startswith("|"):
                    break
                if not looks_like_sigla_definition_row(current):
                    break

                sigla = current
                i += 1
                if i >= len(lines):
                    entries.append((sigla, ""))
                    break

                definition = lines[i].strip()
                if definition and not looks_like_sigla_definition_row(definition) and not definition.startswith("#"):
                    entries.append((sigla, definition))
                    i += 1
                else:
                    entries.append((sigla, ""))

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
    content = remove_repeated_headers_footers(content)
    content = remove_obvious_extraction_noise(content)
    content = join_broken_paragraphs(content)
    content = fix_broken_lists(content)
    content = convert_acronym_blocks_to_table(content)
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
