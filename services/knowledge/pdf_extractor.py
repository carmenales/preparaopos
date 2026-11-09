"""
services/knowledge/pdf_extractor.py

Extractor de texto y estructura desde PDFs con PyMuPDF (fitz).
Diseñado bajo principios de ingeniería de software profesional:
- Segmentación precisa a nivel de línea/span (evita convertir párrafos enteros en encabezados).
- Detección de encabezados reales basada en tipografía (tamaño de fuente, peso bold, brevedad).
- Detección y formato de notas destacadas y callouts (ej. 'Consejo de...', 'Ejemplos a evitar:').
- Eliminación geométrica de cabeceras/pies repetidos por bandas y frecuencia (sin nombres hardcodeados).
- Cero acoplamiento a nombres de academias o procesos selectivos.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF

from markdown_normalizer import MarkdownNormalizer

BULLET_CHARS = r"-*+•·●○▪▫⁃–—\uf0b7\uf0a7\uf0d8"
LONE_BULLET_RE = re.compile(rf"^\s*([{BULLET_CHARS}])\s*$")
BULLET_START_RE = re.compile(rf"^\s*([{BULLET_CHARS}])\s*(.*)$")
SUB_BULLET_RE = re.compile(r"^\s*([oO○\u25cb\u25ef\u25e6]|\([a-z]\)|[a-z]\))\s+([A-ZÁÉÍÓÚ0-9\"'¿¡].*)$")

ABBREVIATIONS_RE = re.compile(r"\b(art|arts|p[áa]g|p[áa]gs|n[úu]m|n[úu]ms|vol|ej|apdo|disp|letra|etc)\.\s*$", re.IGNORECASE)
DANGLING_CONNECTIVE_RE = re.compile(
    r"\b(de|del|en|con|por|para|sobre|tras|y|o|u|e|que|a|al|el|la|los|las|un|una|unos|unas|su|sus|este|esta|estos|estas|como|seg[úu]n|sin|ni|si)\s*$",
    re.IGNORECASE,
)


def _is_sentence_open(text: str) -> bool:
    """Determina si un fragmento de texto ha quedado a mitad de frase o expresión."""
    s = text.rstrip()
    if not s:
        return False
    if s.count("(") > s.count(")"):
        return True
    if ABBREVIATIONS_RE.search(s):
        return True
    if DANGLING_CONNECTIVE_RE.search(s):
        return True
    if not s.endswith((".", ":", ";", "!", "?", "|")):
        return True
    return False


@dataclass
class ExtractedDocument:
    markdown: str
    raw_markdown: str
    detected_title: str
    official_topic: str
    page_count: int
    headings: list[str] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=dict)
    images: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class PdfExtractor:
    """Extrae y estructura documentos PDF a Markdown limpio."""

    def __init__(self, normalizer: type[MarkdownNormalizer] = MarkdownNormalizer) -> None:
        self.normalizer = normalizer

    def extract_from_bytes(
        self,
        pdf_bytes: bytes,
        filename: str = "",
        normalize: bool = True,
    ) -> ExtractedDocument:
        """Punto de entrada principal para extraer un PDF en memoria."""
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        return self._process_fitz_document(doc, filename=filename, normalize=normalize)

    def extract_from_file(
        self,
        file_path: Path | str,
        normalize: bool = True,
    ) -> ExtractedDocument:
        """Punto de entrada para extraer un PDF desde disco."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"No existe el archivo PDF: {path}")
        doc = fitz.open(str(path))
        return self._process_fitz_document(doc, filename=path.name, normalize=normalize)

    def _process_fitz_document(
        self,
        doc: fitz.Document,
        filename: str = "",
        normalize: bool = True,
    ) -> ExtractedDocument:
        page_count = len(doc)
        warnings: list[str] = []

        if page_count == 0:
            doc.close()
            return ExtractedDocument(
                markdown="",
                raw_markdown="",
                detected_title=Path(filename).stem if filename else "Documento vacío",
                official_topic="",
                page_count=0,
                headings=[],
                stats={"char_count": 0, "word_count": 0, "line_count": 0, "page_count": 0},
                images=[],
                warnings=["El PDF no contiene páginas."],
            )

        # 1. Recolección de cabeceras y pies repetidos por geometría y frecuencia
        repeated_headers_footers = self._collect_repeated_header_footer_blocks(doc)

        # 2. Cálculo del tamaño de fuente base (cuerpo del texto) en el documento
        doc_body_font_size = self._calculate_doc_body_font_size(doc)

        page_texts: list[str] = []
        headings_collected: list[str] = []

        for page in doc:
            page_text, page_headings = self._process_page(
                page=page,
                repeated_headers_footers=repeated_headers_footers,
                doc_body_font_size=doc_body_font_size,
            )
            if page_text:
                page_texts.append(page_text)
                headings_collected.extend(page_headings)

        doc.close()

        # 3. Ensamblar documento crudo
        raw_markdown = "\n\n".join(page_texts).strip()

        # 4. Normalización final
        if normalize:
            try:
                processed_markdown = self.normalizer.normalize(raw_markdown)
            except Exception as exc:
                warnings.append(f"Error durante normalización: {exc}")
                processed_markdown = raw_markdown
        else:
            processed_markdown = raw_markdown

        # 5. Detección automática del título y tema oficial
        detected_title, official_topic = self.detect_note_title(processed_markdown, filename=filename)

        # 6. Filtrar headings únicos
        clean_headings: list[str] = []
        for h in headings_collected:
            h_clean = self.normalizer.clean_inline_noise(h)
            if h_clean and h_clean not in clean_headings and not self.normalizer.is_pure_page_or_header_noise(h_clean):
                clean_headings.append(h_clean)

        stats = {
            "char_count": len(processed_markdown),
            "word_count": len(processed_markdown.split()),
            "line_count": len(processed_markdown.splitlines()),
            "page_count": page_count,
        }

        return ExtractedDocument(
            markdown=processed_markdown,
            raw_markdown=raw_markdown,
            detected_title=detected_title,
            official_topic=official_topic,
            page_count=page_count,
            headings=clean_headings,
            stats=stats,
            images=[],
            warnings=warnings,
        )

    # -------------------------------------------------------------------------
    # Heurísticas de Layout y Geometría (100% genéricas, sin nombres hardcodeados)
    # -------------------------------------------------------------------------

    def _is_header_footer_candidate(self, block: dict[str, Any], page_height: float) -> bool:
        """Determina si un bloque se encuentra en la franja superior (16%) o inferior (16%)."""
        bbox = block.get("bbox", [0, 0, 0, 0])
        y0 = float(bbox[1])
        y1 = float(bbox[3])
        top_band = page_height * 0.16
        bottom_band = page_height * 0.84
        return y1 <= top_band or y0 >= bottom_band

    def _page_block_signature(self, block: dict[str, Any]) -> tuple[str, int]:
        """Genera una firma estructural del bloque sustituyendo números por '#'."""
        lines = []
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            line_text = "".join(span.get("text", "") for span in spans).strip()
            if line_text:
                lines.append(line_text)
        text = " ".join(lines).replace("\u200b", "").replace("\u00a0", " ")
        text = re.sub(r"\d+", "#", text)
        text = re.sub(r"\s+", " ", text).strip().lower()
        return text, len(lines)

    def _collect_repeated_header_footer_blocks(self, doc: fitz.Document) -> set[tuple[str, int]]:
        """Identifica bloques recurrentes en bandas marginales a través de las páginas del documento."""
        signature_counter: Counter[tuple[str, int]] = Counter()
        for page in doc:
            page_height = float(page.rect.height)
            for block in page.get_text("dict").get("blocks", []):
                if block.get("type", 0) != 0:
                    continue
                if not self._is_header_footer_candidate(block, page_height):
                    continue
                sig = self._page_block_signature(block)
                if sig[0]:
                    signature_counter[sig] += 1

        threshold = max(2, int(len(doc) * 0.35))
        return {sig for sig, count in signature_counter.items() if count >= threshold}

    def _calculate_doc_body_font_size(self, doc: fitz.Document) -> float:
        """Calcula estadísticamente el tamaño mediano de fuente del texto de cuerpo."""
        all_sizes: list[float] = []
        for page in doc[:10]:  # Muestrear las primeras 10 páginas
            for block in page.get_text("dict").get("blocks", []):
                if block.get("type", 0) != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        try:
                            sz = float(span.get("size", 0.0))
                            if sz > 4.0:
                                all_sizes.append(sz)
                        except Exception:
                            pass
        if not all_sizes:
            return 10.0
        all_sizes.sort()
        return all_sizes[len(all_sizes) // 2]

    def _looks_like_toc_page(self, text: str) -> bool:
        """Detecta páginas de índice / tabla de contenidos."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if len(lines) < 6:
            return False
        toc_like = sum(1 for line in lines[:25] if re.search(r"\b\d+\s*$", line) or re.search(r"\.{3,}", line))
        return toc_like >= max(4, len(lines[:25]) // 2)

    # -------------------------------------------------------------------------
    # Procesamiento y Segmentación a Nivel de Línea (Heading vs Párrafo vs Nota)
    # -------------------------------------------------------------------------

    def _process_page(
        self,
        page: fitz.Page,
        repeated_headers_footers: set[tuple[str, int]],
        doc_body_font_size: float,
    ) -> tuple[str, list[str]]:
        """
        Procesa una página PDF preservando párrafos y distinguiendo encabezados de cuerpo.
        NUNCA une un encabezado con el párrafo posterior en una sola línea.
        """
        data = page.get_text("dict")
        page_elements: list[str] = []
        page_headings: list[str] = []
        pending_bullet: bool = False

        for block in data.get("blocks", []):
            if block.get("type", 0) != 0:
                continue

            # Descarte de cabeceras/pies repetidos
            sig = self._page_block_signature(block)
            if sig in repeated_headers_footers:
                continue

            # Procesar las líneas de este bloque de forma estructurada
            block_elements, block_headings, pending_bullet = self._process_block_lines(
                block=block,
                body_font_size=doc_body_font_size,
                pending_bullet=pending_bullet,
            )
            if block_elements:
                for el in block_elements:
                    # 1. Fusión de headings consecutivos del mismo nivel
                    if (
                        page_elements
                        and el.startswith("## ")
                        and page_elements[-1].startswith("## ")
                        and not re.match(r"^##\s+\d+(\.\d+)*\.?\s+", el)
                        and not page_elements[-1].endswith((".", ":"))
                    ):
                        page_elements[-1] += " " + el[3:].strip()
                        if page_headings:
                            page_headings[-1] += " " + el[3:].strip()

                    # 2. Fusión de continuación de viñetas entre bloques
                    elif (
                        page_elements
                        and page_elements[-1].startswith(("- ", "  - "))
                        and not el.startswith(("#", "- ", "  - ", "* ", "|", ">", "**"))
                        and not re.match(r"^\d+\.\s+[A-ZÁÉÍÓÚ]", el)
                        and (
                            _is_sentence_open(page_elements[-1])
                            or el[0].islower()
                            or (page_elements[-1].count("(") > page_elements[-1].count(")") and ")" in el)
                        )
                    ):
                        if page_elements[-1].endswith("-"):
                            page_elements[-1] = page_elements[-1][:-1] + el
                        else:
                            page_elements[-1] += " " + el

                    # 3. Fusión de párrafos divididos a mitad de frase entre bloques
                    elif (
                        page_elements
                        and not page_elements[-1].startswith(("#", "- ", "  - ", "* ", "|", ">", "**"))
                        and not el.startswith(("#", "- ", "  - ", "* ", "|", ">", "**"))
                        and not re.match(r"^\d+\.\s+[A-ZÁÉÍÓÚ]", el)
                        and (
                            _is_sentence_open(page_elements[-1])
                            or el[0].islower()
                            or (page_elements[-1].count("(") > page_elements[-1].count(")") and ")" in el)
                        )
                    ):
                        if page_elements[-1].endswith("-"):
                            page_elements[-1] = page_elements[-1][:-1] + el
                        else:
                            page_elements[-1] += " " + el

                    else:
                        page_elements.append(el)
                        if el.startswith("#"):
                            h_text = el.lstrip("#").strip()
                            if h_text and h_text not in page_headings:
                                page_headings.append(h_text)

        # Ensamblar página compactando listas viñeteadas consecutivas
        merged_elements: list[str] = []
        for el in page_elements:
            if not el.strip():
                continue
            if (
                merged_elements
                and merged_elements[-1].strip().startswith(("- ", "* "))
                and el.strip().startswith(("- ", "* "))
            ):
                merged_elements[-1] += "\n" + el
            else:
                merged_elements.append(el)

        page_markdown = "\n\n".join(merged_elements).strip()
        if self._looks_like_toc_page(page_markdown):
            return "", []

        return page_markdown, page_headings

    def _process_block_lines(
        self,
        block: dict[str, Any],
        body_font_size: float,
        pending_bullet: bool = False,
    ) -> tuple[list[str], list[str], bool]:
        """
        Segmenta las líneas de un bloque de texto.
        Diferencia encabezados reales, notas/callouts destacados y texto de párrafo/viñetas.
        """
        elements: list[str] = []
        headings: list[str] = []

        current_paragraph_lines: list[str] = []
        current_bullet_lines: list[str] = []

        def flush_bullet() -> None:
            nonlocal pending_bullet
            if current_bullet_lines:
                b_text = " ".join(current_bullet_lines).strip()
                is_sub = current_bullet_lines[0].startswith("  ")
                indent = "  " if is_sub else ""
                text_no_indent = b_text.lstrip()
                clean_target = text_no_indent[2:] if text_no_indent.startswith("- ") else text_no_indent
                b_clean = self.normalizer.clean_inline_noise(clean_target)
                if b_clean and not self.normalizer.is_pure_page_or_header_noise(b_clean):
                    elements.append(f"{indent}- {b_clean}")
                current_bullet_lines.clear()
                pending_bullet = False

        def flush_paragraph() -> None:
            flush_bullet()
            if current_paragraph_lines:
                p_text = self._join_paragraph_lines(current_paragraph_lines)
                p_clean = self.normalizer.clean_inline_noise(p_text)
                if p_clean and not self.normalizer.is_pure_page_or_header_noise(p_clean):
                    elements.append(p_clean)
                current_paragraph_lines.clear()

        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue

            line_text = "".join(span.get("text", "") for span in spans).strip()
            if not line_text:
                continue

            line_clean = self.normalizer.clean_inline_noise(line_text)
            if not line_clean or self.normalizer.is_pure_page_or_header_noise(line_clean):
                continue

            # Extraer características tipográficas de la línea
            line_font_size = max(float(span.get("size", 0.0)) for span in spans)
            is_bold = any(
                (int(span.get("flags", 0)) & 2 != 0) or ("bold" in str(span.get("font", "")).lower())
                for span in spans
            )
            word_count = len(line_clean.split())

            # Comprobar si el párrafo actual tiene una frase abierta
            prev_open = bool(current_paragraph_lines and _is_sentence_open(current_paragraph_lines[-1]))

            # 1. ¿Es una viñeta suelta (ej. solo '•' o '·')?
            if LONE_BULLET_RE.match(line_clean):
                flush_paragraph()
                pending_bullet = True
                continue

            # 2. ¿Es una sub-viñeta con 'o' / '○' / '(a)' (ej. 'o RD 1150/2021...')?
            m_sub = SUB_BULLET_RE.match(line_clean)
            if m_sub:
                flush_paragraph()
                current_bullet_lines.append(f"  - {m_sub.group(2).strip()}")
                continue

            # 3. ¿Es el inicio de una viñeta con símbolo?
            m_bullet = BULLET_START_RE.match(line_clean)
            if m_bullet:
                flush_paragraph()
                bullet_content = m_bullet.group(2).strip()
                if not bullet_content:
                    pending_bullet = True
                else:
                    current_bullet_lines.append(f"- {bullet_content}")
                continue

            # 4. Si teníamos una viñeta suelta pendiente, esta línea es su contenido
            if pending_bullet:
                pending_bullet = False
                if self._is_callout_or_label(line_clean, is_bold, word_count, prev_is_open=False) or line_clean.endswith(":"):
                    current_bullet_lines.append(f"- **{line_clean}**")
                else:
                    current_bullet_lines.append(f"- {line_clean}")
                continue

            # 5. ¿Es un encabezado real?
            heading_level = self._detect_heading_level(
                text=line_clean,
                font_size=line_font_size,
                body_font_size=body_font_size,
                is_bold=is_bold,
                word_count=word_count,
            )

            if heading_level > 0 and not prev_open:
                flush_paragraph()
                prefix = f"{'#' * heading_level} "
                if (
                    elements
                    and elements[-1].startswith(prefix)
                    and not re.match(r"^\d+(\.\d+)*\.?\s+", line_clean)
                    and not elements[-1].endswith((".", ":"))
                ):
                    elements[-1] += " " + line_clean
                    if headings:
                        headings[-1] += " " + line_clean
                else:
                    heading_md = f"{prefix}{line_clean}"
                    elements.append(heading_md)
                    headings.append(line_clean)
                continue

            # 6. ¿Es un callout, nota o etiqueta destacada (ej. 'Consejo de...', 'Ejemplos a evitar:')?
            if self._is_callout_or_label(line_clean, is_bold, word_count, prev_is_open=prev_open):
                flush_paragraph()
                elements.append(f"**{line_clean}**")
                continue

            # 7. Si ya estamos dentro de una viñeta, las líneas siguientes son su continuación
            if current_bullet_lines:
                if current_bullet_lines[-1].endswith("-"):
                    current_bullet_lines[-1] = current_bullet_lines[-1][:-1] + line_clean
                else:
                    current_bullet_lines.append(line_clean)
                continue

            # 8. Es texto de párrafo continuo
            current_paragraph_lines.append(line_text)

        flush_paragraph()
        return elements, headings, pending_bullet

    def _detect_heading_level(
        self,
        text: str,
        font_size: float,
        body_font_size: float,
        is_bold: bool,
        word_count: int,
    ) -> int:
        """
        Determina si una línea es un encabezado y su nivel Markdown (2, 3 o 4).
        Los encabezados son concisos (<= 15 palabras) y no terminan en punto de oración.
        """
        if word_count > 15:
            return 0
        if text.endswith((".", ";")):
            return 0

        # Patrón numerado explícito: '1. INTRODUCCIÓN', '2.3. ARQUITECTURA'
        has_numbered_prefix = bool(re.match(r"^\d+(\.\d+)*\.?\s+[A-ZÁÉÍÓÚÑ]", text))

        delta = font_size - body_font_size

        if delta >= 4.5:
            return 2
        if delta >= 2.0:
            return 3
        if is_bold and (has_numbered_prefix or delta >= 1.0):
            return 4
        if has_numbered_prefix and text.isupper():
            return 3

        return 0

    def _is_callout_or_label(
        self,
        text: str,
        is_bold: bool,
        word_count: int,
        prev_is_open: bool = False,
    ) -> bool:
        """
        Detecta etiquetas de notas, consejos o avisos (ej. 'Consejo de Preparatic', 'Ejemplos a evitar:').
        NUNCA fragmenta una frase abierta previa.
        """
        if prev_is_open:
            return False

        if word_count > 8:
            return False

        # Empieza con palabras clave de llamada de atención o consejo
        if re.match(
            r"^(consejo|nota|importante|ejemplo[s]?(\s+a\s+evitar)?|atenci[óo]n|advertencia|recordatorio|aviso|caso\s+pr[áa]ctico|definici[óo]n)\b",
            text,
            re.I,
        ):
            return True

        # Es una línea corta en negrita que actúa como título de campo (ej. 'Marco estratégico de ciberseguridad:')
        if is_bold and word_count <= 6 and text.endswith(":") and text[0].isupper():
            return True

        return False

    def _join_paragraph_lines(self, lines: list[str]) -> str:
        """Une líneas dentro de un párrafo resolviendo cortes de palabra con guion."""
        if not lines:
            return ""

        result = lines[0].strip()
        for next_line in lines[1:]:
            next_clean = next_line.strip()
            if not next_clean:
                continue
            if result.endswith("-"):
                # Palabra cortada con guion: unir directamente
                result = result[:-1] + next_clean
            else:
                result = result + " " + next_clean

        return re.sub(r"[ \t]+", " ", result).strip()

    # -------------------------------------------------------------------------
    # Detección Automática de Título y Tema Oficial (Genérica)
    # -------------------------------------------------------------------------

    def detect_note_title(self, markdown_text: str, filename: str = "") -> tuple[str, str]:
        """
        Detecta automáticamente el título del apunte y el tema oficial.
        Prioridades:
        1. Encabezado explícito de temario: 'TEMA X. TITULO...'
        2. Primer heading Markdown (# o ##) no trivial.
        3. Título destacado en mayúsculas (conciso, sin punto final).
        4. Fallback al nombre del archivo limpio.
        """
        first_lines = markdown_text[:4000].splitlines()

        # 1. Buscar patrón tipo "TEMA X. TITULO..."
        for line in first_lines:
            line_clean = self.normalizer.clean_inline_noise(line.strip().lstrip("#").strip())
            if not line_clean or self.normalizer.is_pure_page_or_header_noise(line_clean):
                continue
            tema_match = re.match(r"^(tema\s+([a-z0-9ivxlcdm\.\-_]+)[\.\:\s\-]+(.+))$", line_clean, re.I)
            if tema_match:
                topic_num = tema_match.group(2).strip().rstrip(".:-")
                topic_name = self.normalizer.clean_inline_noise(tema_match.group(3).strip())
                title = f"Tema {topic_num} {topic_name}".strip()
                official_topic = f"{topic_num} {topic_name}".strip()
                return title, official_topic

        # 2. Primer heading Markdown real (# o ##)
        for line in first_lines:
            line_clean = self.normalizer.clean_inline_noise(line.strip())
            match = re.match(r"^#{1,2}\s+(.+)$", line_clean)
            if match:
                heading = self.normalizer.clean_inline_noise(match.group(1).strip())
                if (
                    heading
                    and not heading.lower().startswith("página")
                    and not heading.lower().startswith("índice")
                    and not self.normalizer.is_pure_page_or_header_noise(heading)
                    and len(heading) >= 3
                ):
                    return heading, heading

        # 3. Título en mayúsculas destacado (conciso, no párrafo)
        for line in first_lines[:15]:
            line_clean = self.normalizer.clean_inline_noise(line.strip().lstrip("#").strip())
            if (
                line_clean
                and not self.normalizer.is_pure_page_or_header_noise(line_clean)
                and not line_clean.lower().startswith("página")
                and not line_clean.lower().startswith("índice")
                and len(line_clean) >= 4
                and line_clean.isupper()
                and not line_clean.endswith((".", ";", ":"))
                and len(line_clean.split()) <= 12
                and re.search(r"[A-ZÁÉÍÓÚÑ]", line_clean)
            ):
                return line_clean, line_clean

        # 4. Fallback al nombre de archivo
        if filename:
            stem = Path(filename).stem
            # Limpiar separadores y prefijos alfanuméricos tipo '01_'
            cleaned = re.sub(r"^\d+[_\-]", "", stem)
            cleaned = cleaned.replace("_", " ").replace("-", " ")
            cleaned = self.normalizer.clean_inline_noise(cleaned)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            if cleaned:
                return cleaned, cleaned

        return "Nuevo Apunte", ""
