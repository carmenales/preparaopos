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

try:
    from normalize_markdown import clean_inline_noise, is_pure_page_or_header_noise
except ImportError:
    def clean_inline_noise(text: str) -> str:
        return text

    def is_pure_page_or_header_noise(text: str) -> bool:
        return False


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
    text = text.replace("\u200b", "").replace("\u00a0", " ")
    text = re.sub(r"\d+", "#", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text, len(lines)


def _is_header_footer_candidate(block: dict[str, Any], page_height: float) -> bool:
    bbox = block.get("bbox", [0, 0, 0, 0])
    y0 = float(bbox[1])
    y1 = float(bbox[3])
    top_band = page_height * 0.16
    bottom_band = page_height * 0.84
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

    threshold = max(2, int(len(doc) * 0.35))
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
        blocks = page.get_text("dict").get("blocks", [])
        body_candidates: list[float] = []
        for b in blocks:
            if b.get("type", 0) != 0:
                continue
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    try:
                        sz = float(span.get("size", 0.0))
                        if sz > 4.0:
                            body_candidates.append(sz)
                    except Exception:
                        pass
        body_candidates.sort()
        body_size = body_candidates[len(body_candidates) // 2] if body_candidates else 10.0

        page_elements: list[str] = []
        for block in blocks:
            if block.get("type", 0) != 0:
                continue
            sig = _page_block_signature(block)
            if sig in repeated_headers_footers:
                continue

            current_paragraph: list[str] = []

            def flush_p() -> None:
                if current_paragraph:
                    p_text = " ".join(current_paragraph).strip()
                    p_clean = clean_inline_noise(p_text)
                    if p_clean and not is_pure_page_or_header_noise(p_clean):
                        page_elements.append(p_clean)
                    current_paragraph.clear()

            for line in block.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue
                line_text = "".join(span.get("text", "") for span in spans).strip()
                line_clean = clean_inline_noise(line_text)
                if not line_clean or is_pure_page_or_header_noise(line_clean):
                    continue

                line_font_size = max(float(span.get("size", 0.0)) for span in spans)
                is_bold = any(
                    (int(span.get("flags", 0)) & 2 != 0) or ("bold" in str(span.get("font", "")).lower())
                    for span in spans
                )
                word_count = len(line_clean.split())

                # Detección de encabezado real (conciso, sin punto final)
                heading_level = 0
                if word_count <= 15 and not line_clean.endswith((".", ";")):
                    delta = line_font_size - body_size
                    if delta >= 4.5:
                        heading_level = 2
                    elif delta >= 2.0:
                        heading_level = 3
                    elif is_bold and (re.match(r"^\d+(\.\d+)*\.?\s+[A-ZÁÉÍÓÚÑ]", line_clean) or delta >= 1.0):
                        heading_level = 4
                    elif re.match(r"^\d+(\.\d+)*\.?\s+[A-ZÁÉÍÓÚÑ]", line_clean) and line_clean.isupper():
                        heading_level = 3

                if heading_level > 0:
                    flush_p()
                    prefix = f"{'#' * heading_level} "
                    if (
                        page_elements
                        and page_elements[-1].startswith(prefix)
                        and not re.match(r"^\d+(\.\d+)*\.?\s+", line_clean)
                        and not page_elements[-1].endswith((".", ":"))
                    ):
                        page_elements[-1] += " " + line_clean
                    else:
                        page_elements.append(f"{prefix}{line_clean}")
                    continue

                # Detección de callout / etiqueta de nota (no dividir frases abiertas)
                is_callout = bool(
                    re.match(r"^(consejo|nota|importante|ejemplo[s]?(\s+a\s+evitar)?|atenci[óo]n|advertencia|recordatorio|aviso|caso\s+pr[áa]ctico|definici[óo]n)\b", line_clean, re.I)
                    or (is_bold and word_count <= 6 and line_clean.endswith(":") and line_clean[0].isupper() and not current_paragraph)
                )
                if is_callout:
                    flush_p()
                    page_elements.append(f"**{line_clean}**")
                    continue

                # Sub-viñetas con 'o' / '○' / '(a)'
                m_sub = re.match(r"^\s*([oO○\u25cb\u25ef\u25e6]|\([a-z]\)|[a-z]\))\s+([A-ZÁÉÍÓÚ0-9\"'¿¡].*)$", line_clean)
                if m_sub:
                    flush_p()
                    page_elements.append(f"  - {m_sub.group(2).strip()}")
                    continue

                if re.match(r"^[-*+•·●○▪▫⁃–—\uf0b7\uf0a7\uf0d8]\s*", line_clean):
                    flush_p()
                    bullet_text = re.sub(r"^[-*+•·●○▪▫⁃–—\uf0b7\uf0a7\uf0d8]\s*", "", line_clean).strip()
                    if bullet_text:
                        page_elements.append(f"- {bullet_text}")
                    continue

                current_paragraph.append(line_text)

            flush_p()

        page_texts[page.number + 1] = "\n\n".join(page_elements)

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
