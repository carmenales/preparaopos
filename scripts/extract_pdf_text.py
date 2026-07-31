#!/usr/bin/env python3
"""
Extrae texto e imágenes de PDFs a Markdown usando PyMuPDF.

Incluye soporte básico para tablas detectadas por layout cuando la librería lo
permite. Las tablas simples se exportan como Markdown; los casos complejos se
mantienen como texto lineal para no perder contenido.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF


@dataclass(frozen=True)
class LineText:
    page_number: int
    text: str
    bbox: tuple[float, float, float, float]
    font_size: float


@dataclass(frozen=True)
class TableRegion:
    bbox: tuple[float, float, float, float]
    markdown: str


def _sanitize_filename(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-")
    return name or "img"


def _normalize_text(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _line_signature(text: str) -> str:
    text = _normalize_text(text).lower()
    text = re.sub(r"\b\d+\b", "#", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _looks_like_toc_page(lines: list[str]) -> bool:
    if len(lines) < 8:
        return False

    toc_like = 0
    for line in lines[:30]:
        if re.match(r"^\s*(\d+(\.\d+)*)\s+.+?\s+\d+\s*$", line):
            toc_like += 1
        elif re.search(r"\.\.\.\.+\s*\d+\s*$", line):
            toc_like += 1
        elif re.match(r"^\s*\d+(\.\d+)*\.?\s*[A-ZÁÉÍÓÚÑ].+\s+\d+\s*$", line):
            toc_like += 1

    return toc_like >= 5


def _extract_lines(page: fitz.Page) -> list[LineText]:
    data = page.get_text("dict")
    lines: list[LineText] = []

    for block in data.get("blocks", []):
        if block.get("type", 0) != 0:
            continue

        for line in block.get("lines", []):
            spans = line.get("spans", [])
            parts = []
            sizes = []
            for span in spans:
                span_text = span.get("text", "")
                if span_text:
                    parts.append(span_text)
                    try:
                        sizes.append(float(span.get("size", 0.0)))
                    except Exception:
                        pass

            text = _normalize_text("".join(parts))
            if not text:
                continue

            bbox = tuple(float(v) for v in line.get("bbox", (0, 0, 0, 0)))
            font_size = max(sizes) if sizes else 0.0
            lines.append(LineText(page.number + 1, text, bbox, font_size))

    return lines


def _extract_tables(page: fitz.Page) -> list[TableRegion]:
    tables: list[TableRegion] = []
    try:
        finder = page.find_tables()
    except Exception:
        return tables

    for table in getattr(finder, "tables", []) or []:
        try:
            matrix = table.extract()
        except Exception:
            matrix = []

        if not matrix:
            try:
                matrix = table.to_list()
            except Exception:
                matrix = []

        rows = []
        for row in matrix:
            clean_row = [_normalize_text(str(cell)) for cell in row]
            clean_row = [cell for cell in clean_row if cell]
            if clean_row:
                rows.append(clean_row)

        if not rows:
            continue

        max_cols = max(len(r) for r in rows)
        if max_cols < 2:
            continue

        normalized_rows = [r + [""] * (max_cols - len(r)) for r in rows]
        header = normalized_rows[0]
        body = normalized_rows[1:] if len(normalized_rows) > 1 else []

        md_lines = []
        md_lines.append("| " + " | ".join(header) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        for row in body:
            md_lines.append("| " + " | ".join(row) + " |")

        bbox = getattr(table, "bbox", None)
        if bbox:
            bbox_tuple = tuple(float(v) for v in bbox)
        else:
            bbox_tuple = (0.0, 0.0, 0.0, 0.0)

        tables.append(TableRegion(bbox=bbox_tuple, markdown="\n".join(md_lines)))

    return tables


def _collect_repeated_header_footer_signatures(doc: fitz.Document) -> set[str]:
    counter: Counter[str] = Counter()
    total_pages = len(doc)

    for page in doc:
        page_h = float(page.rect.height)
        page_lines = _extract_lines(page)
        for line in page_lines:
            y0, y1 = float(line.bbox[1]), float(line.bbox[3])
            if y1 <= page_h * 0.12 or y0 >= page_h * 0.88:
                sig = _line_signature(line.text)
                if sig:
                    counter[sig] += 1

    threshold = max(3, int(total_pages * 0.6))
    return {sig for sig, count in counter.items() if count >= threshold}


def _infer_heading_level(font_size: float, body_size: float) -> int:
    if body_size <= 0:
        return 0
    delta = font_size - body_size
    if delta >= 5:
        return 2
    if delta >= 3:
        return 3
    if delta >= 1.5:
        return 4
    return 0


def _convert_pixmap_to_png(pix: fitz.Pixmap, target: Path) -> None:
    if pix.alpha:
        pix = fitz.Pixmap(pix, 0)
    pix.save(str(target.with_suffix(".png")))


def _extract_images_from_page(page: fitz.Page, page_number: int, images_dir: Path, images_dir_relative: str) -> list[str]:
    markdown_lines: list[str] = []
    seen_xrefs: set[int] = set()

    for img_index, img in enumerate(page.get_images(full=True), start=1):
        xref = int(img[0])
        if xref in seen_xrefs:
            continue
        seen_xrefs.add(xref)

        try:
            pix = fitz.Pixmap(page.parent, xref)
            filename = _sanitize_filename(f"pagina-{page_number}-img-{img_index}.png")
            images_dir.mkdir(parents=True, exist_ok=True)
            out_path = images_dir / filename
            _convert_pixmap_to_png(pix, out_path)
            markdown_lines.append(f"![Imagen de la página {page_number}]({images_dir_relative}/{filename})")
            markdown_lines.append("")
        except Exception:
            try:
                base = page.parent.extract_image(xref)
                image_bytes = base.get("image", b"")
                if not image_bytes:
                    continue
                ext = (base.get("ext") or "bin").lower()
                filename = _sanitize_filename(f"pagina-{page_number}-img-{img_index}.{ext}")
                images_dir.mkdir(parents=True, exist_ok=True)
                (images_dir / filename).write_bytes(image_bytes)
                markdown_lines.append(f"![Imagen de la página {page_number}]({images_dir_relative}/{filename})")
                markdown_lines.append("")
            except Exception:
                continue

    return markdown_lines


def _remove_table_regions(lines: list[LineText], tables: list[TableRegion]) -> list[LineText]:
    if not tables:
        return lines

    filtered: list[LineText] = []
    for line in lines:
        x0, y0, x1, y1 = line.bbox
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2
        inside_table = False
        for table in tables:
            tx0, ty0, tx1, ty1 = table.bbox
            if tx0 <= center_x <= tx1 and ty0 <= center_y <= ty1:
                inside_table = True
                break
        if not inside_table:
            filtered.append(line)
    return filtered


def extract_pdf_to_markdown(input_pdf: Path, output_md: Path, extract_images: bool = True) -> None:
    if not input_pdf.exists():
        raise FileNotFoundError(f"No existe el PDF: {input_pdf}")

    output_md.parent.mkdir(parents=True, exist_ok=True)
    images_dir = output_md.parent / output_md.stem / "images"
    images_dir_relative = f"{output_md.stem}/images"

    doc = fitz.open(str(input_pdf))
    repeated_headers_footers = _collect_repeated_header_footer_signatures(doc)

    page_lines_map: dict[int, list[LineText]] = {}
    page_tables_map: dict[int, list[TableRegion]] = {}
    body_sizes: list[float] = []

    for page in doc:
        lines = _extract_lines(page)
        tables = _extract_tables(page)
        lines = _remove_table_regions(lines, tables)
        page_lines_map[page.number + 1] = lines
        page_tables_map[page.number + 1] = tables
        for line in lines:
            if line.font_size > 0:
                body_sizes.append(line.font_size)

    body_size = sorted(body_sizes)[len(body_sizes) // 2] if body_sizes else 0.0

    output_lines = [
        f"# Texto extraído: {input_pdf.name}",
        "",
        "> Texto extraído automáticamente desde PDF. Puede contener errores de formato, pero se han eliminado cabeceras/pies repetidos y páginas de índice cuando han podido detectarse.",
        "",
        f"- Archivo origen: `{input_pdf.as_posix()}`",
        f"- Número de páginas: {len(doc)}",
        "",
    ]

    total_images = 0

    for page_number in range(1, len(doc) + 1):
        page = doc[page_number - 1]
        lines = page_lines_map.get(page_number, [])
        tables = page_tables_map.get(page_number, [])

        visible_lines = []
        for line in lines:
            sig = _line_signature(line.text)
            if sig in repeated_headers_footers:
                continue
            visible_lines.append(line)

        if not visible_lines and not tables:
            continue

        visible_texts = [line.text for line in visible_lines]
        if visible_texts and _looks_like_toc_page(visible_texts):
            continue

        if visible_lines:
            for i, line in enumerate(visible_lines):
                heading_level = _infer_heading_level(line.font_size, body_size)
                text = line.text

                if heading_level and len(text) <= 180:
                    prev_line = visible_lines[i - 1].text if i > 0 else ""
                    next_line = visible_lines[i + 1].text if i + 1 < len(visible_lines) else ""
                    if prev_line and len(prev_line) < 120 and not prev_line.endswith((".", ":", ";")):
                        pass
                    elif next_line and len(next_line) > 120 and not re.match(r"^\d+(\.\d+)*\s", text):
                        pass
                    else:
                        output_lines.append(f"{'#' * heading_level} {text}")
                        output_lines.append("")
                        continue

                output_lines.append(text)

            output_lines.append("")

        for table in tables:
            output_lines.append(table.markdown)
            output_lines.append("")

        if extract_images:
            image_lines = _extract_images_from_page(page, page_number, images_dir, images_dir_relative)
            if image_lines:
                output_lines.extend(image_lines)
                total_images += sum(1 for line in image_lines if line.startswith("!["))

    output_md.write_text("\n".join(output_lines).rstrip() + "\n", encoding="utf-8")

    if total_images:
        print(f"Extraídas {total_images} imágenes en: {images_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrae texto e imágenes de un PDF a Markdown.")
    parser.add_argument("input_pdf", help="Ruta del PDF de origen")
    parser.add_argument("output_md", help="Ruta del Markdown de salida")
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="No extraer imágenes incrustadas, solo texto.",
    )
    args = parser.parse_args()

    extract_pdf_to_markdown(
        input_pdf=Path(args.input_pdf),
        output_md=Path(args.output_md),
        extract_images=not args.no_images,
    )


if __name__ == "__main__":
    main()
