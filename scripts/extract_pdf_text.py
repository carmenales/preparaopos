#!/usr/bin/env python3
"""
Extrae texto e imágenes de PDFs a Markdown usando PyMuPDF.

Características:
- Detecta cabeceras/pies repetidos por posición y frecuencia.
- Descarta páginas tipo índice/TOC en bruto.
- Convierte imágenes incrustadas a PNG/JPG estándar cuando es posible.
- Genera un Markdown más limpio, con headings inferidos por tamaño de fuente.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF


@dataclass(frozen=True)
class TextBlock:
    page_number: int
    text: str
    bbox: tuple[float, float, float, float]
    font_size: float


def _sanitize_filename(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-")
    return name or "img"


def _normalize_text(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"(?<=\w)\n(?=\w)", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def _looks_like_toc_page(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 6:
        return False
    toc_like = 0
    for line in lines[:25]:
        if re.search(r"\b\d+\s*$", line) and len(line) < 120:
            toc_like += 1
        elif re.search(r"\.\.\.\.\.|\.{3,}", line):
            toc_like += 1
        elif re.match(r"^\d+(\.\d+)*\.?\s+", line):
            toc_like += 1
    return toc_like >= max(4, len(lines[:25]) // 2)


def _page_block_signature(block: dict[str, Any]) -> tuple[str, int]:
    lines = []
    for line in block.get("lines", []):
        spans = line.get("spans", [])
        line_text = "".join(span.get("text", "") for span in spans)
        line_text = _normalize_text(line_text)
        if line_text:
            lines.append(line_text)
    text = " ".join(lines)
    text = re.sub(r"\b\d+\b", "#", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text, len(lines)


def _is_header_footer_candidate(block: dict[str, Any], page_height: float) -> bool:
    bbox = block.get("bbox", [0, 0, 0, 0])
    y0 = float(bbox[1])
    y1 = float(bbox[3])
    top_band = page_height * 0.12
    bottom_band = page_height * 0.88
    return y1 <= top_band or y0 >= bottom_band


def _extract_blocks(page: fitz.Page) -> list[TextBlock]:
    data = page.get_text("dict")
    blocks: list[TextBlock] = []
    page_height = float(page.rect.height)

    for block in data.get("blocks", []):
        if block.get("type", 0) != 0:
            continue

        text_parts = []
        font_sizes = []
        for line in block.get("lines", []):
            line_parts = []
            for span in line.get("spans", []):
                span_text = span.get("text", "")
                if span_text:
                    line_parts.append(span_text)
                    try:
                        font_sizes.append(float(span.get("size", 0.0)))
                    except Exception:
                        pass
            if line_parts:
                text_parts.append("".join(line_parts))

        text = _normalize_text("\n".join(text_parts))
        if not text:
            continue

        bbox = tuple(float(v) for v in block.get("bbox", (0, 0, 0, 0)))
        font_size = max(font_sizes) if font_sizes else 0.0
        blocks.append(TextBlock(page.number + 1, text, bbox, font_size))

    return blocks


def _collect_repeated_header_footer_blocks(doc: fitz.Document) -> set[tuple[str, int]]:
    signature_counter: Counter[tuple[str, int]] = Counter()
    signatures_by_page: dict[int, list[tuple[str, int]]] = defaultdict(list)

    for page in doc:
        page_height = float(page.rect.height)
        for block in page.get_text("dict").get("blocks", []):
            if block.get("type", 0) != 0:
                continue
            if not _is_header_footer_candidate(block, page_height):
                continue
            sig = _page_block_signature(block)
            if sig[0]:
                signature_counter[sig] += 1
                signatures_by_page[page.number].append(sig)

    threshold = max(3, int(len(doc) * 0.6))
    return {sig for sig, count in signature_counter.items() if count >= threshold}


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
            base = page.parent.extract_image(xref)
            ext = (base.get("ext") or "png").lower()
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
                filename = _sanitize_filename(f"pagina-{page_number}-img-{img_index}.{base.get('ext', 'bin')}")
                images_dir.mkdir(parents=True, exist_ok=True)
                (images_dir / filename).write_bytes(image_bytes)
                markdown_lines.append(f"![Imagen de la página {page_number}]({images_dir_relative}/{filename})")
                markdown_lines.append("")
            except Exception:
                continue

    return markdown_lines


def extract_pdf_to_markdown(input_pdf: Path, output_md: Path, extract_images: bool = True) -> None:
    if not input_pdf.exists():
        raise FileNotFoundError(f"No existe el PDF: {input_pdf}")

    output_md.parent.mkdir(parents=True, exist_ok=True)
    images_dir = output_md.parent / output_md.stem / "images"
    images_dir_relative = f"{output_md.stem}/images"

    doc = fitz.open(str(input_pdf))
    repeated_headers_footers = _collect_repeated_header_footer_blocks(doc)

    all_blocks: list[TextBlock] = []
    page_texts: dict[int, str] = {}

    for page in doc:
        blocks = _extract_blocks(page)
        body_candidates = [b.font_size for b in blocks if b.font_size > 0]
        body_size = sorted(body_candidates)[len(body_candidates) // 2] if body_candidates else 0.0

        page_lines: list[str] = []
        for block in blocks:
            sig_text = re.sub(r"\b\d+\b", "#", block.text).lower()
            if (sig_text, len(block.text.splitlines())) in repeated_headers_footers:
                continue

            if _looks_like_toc_page(block.text):
                continue

            heading_level = _infer_heading_level(block.font_size, body_size)
            text = block.text
            if heading_level == 2:
                page_lines.append(f"## {text}")
            elif heading_level == 3:
                page_lines.append(f"### {text}")
            elif heading_level == 4:
                page_lines.append(f"#### {text}")
            else:
                page_lines.append(text)

        page_texts[page.number + 1] = _normalize_text("\n\n".join(page_lines))

    lines = [
        "> Texto extraído automáticamente desde PDF. Puede contener errores de formato.",
        "",
        f"- Archivo origen: `{input_pdf.as_posix()}`",
        f"- Número de páginas: {len(doc)}",
        "",
    ]

    total_images = 0
    for page_number in range(1, len(doc) + 1):
        page_text = page_texts.get(page_number, "")
        if page_text:
            lines.append(f"## Página {page_number}")
            lines.append("")
            lines.append(page_text)
            lines.append("")
        if extract_images:
            page = doc[page_number - 1]
            image_lines = _extract_images_from_page(page, page_number, images_dir, images_dir_relative)
            total_images += sum(1 for line in image_lines if line.startswith("![]") or line.startswith("![") )
            lines.extend(image_lines)

    output_md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

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
