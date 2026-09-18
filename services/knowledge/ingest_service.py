"""
services/knowledge/ingest_service.py

Servicio para la ingestión y publicación de nuevas fuentes de conocimiento.
Coordina:
- Extracción de texto y estructura desde PDFs con PyMuPDF.
- Normalización mediante scripts/normalize_markdown.py.
- Detección automática de títulos y temas oficiales.
- Refinado opcional asistido por LLM (Ollama).
- Publicación física en knowledge/processes/{process_slug}/apuntes/ con YAML frontmatter.
- Sincronización automática de knowledge_index.json vía scripts/build_knowledge_index.py.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF

from config import settings
from ollama_client import OllamaClient, OllamaClientError
from schemas import PublishNoteRequest, PublishNoteResponse
from text_utils import slugify

# Asegurar que scripts/ esté en sys.path para reutilizar extractores e indexador
_scripts_dir = str(settings.scripts_dir)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

try:
    from normalize_markdown import normalize_markdown
except ImportError:
    def normalize_markdown(content: str) -> str:
        return content

try:
    from build_knowledge_index import build_index
except ImportError:
    build_index = None

try:
    from extract_pdf_text import (
        _collect_repeated_header_footer_blocks,
        _extract_blocks,
        _infer_heading_level,
        _looks_like_toc_page,
        _normalize_text,
    )
except ImportError:
    # Fallback directo si no se puede importar
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
        toc_like = sum(1 for line in lines[:25] if re.search(r"\b\d+\s*$", line) or re.search(r"\.{3,}", line))
        return toc_like >= max(4, len(lines[:25]) // 2)

    def _collect_repeated_header_footer_blocks(doc: fitz.Document) -> set:
        return set()

    def _infer_heading_level(font_size: float, body_size: float) -> int:
        delta = font_size - body_size
        if delta >= 5:
            return 2
        if delta >= 3:
            return 3
        if delta >= 1.5:
            return 4
        return 0

    def _extract_blocks(page: fitz.Page) -> list:
        return []


def sanitize_filename(filename: str) -> str:
    """Limpia caracteres inválidos en nombres de fichero y asegura extensión .md."""
    has_md = filename.lower().endswith(".md")
    base = filename[:-3] if has_md else filename
    cleaned = re.sub(r'[\\/*?:"<>|]', "-", base)
    cleaned = re.sub(r"\s*-\s*", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned).strip(" -.")
    return f"{cleaned}.md" if cleaned else "apunte.md"


def detect_note_title(extracted_text: str, filename: str = "") -> tuple[str, str]:
    """
    Detecta automáticamente el título de la nota y el tema oficial a partir
    del texto extraído o del nombre de archivo.
    Retorna (title, official_topic).
    """
    # 1. Buscar patrón tipo "TEMA X. TITULO..." en los primeros párrafos
    first_lines = extracted_text[:3000].splitlines()
    for line in first_lines:
        line_clean = line.strip().lstrip("#").strip()
        tema_match = re.match(r"^(TEMA\s+([A-Z0-9IVXLCDM\.\-_]+)[\.\:\s\-]+(.+))$", line_clean, re.IGNORECASE)
        if tema_match:
            topic_num = tema_match.group(2).strip().rstrip(".:-")
            topic_name = tema_match.group(3).strip()
            title = f"Tema {topic_num} {topic_name}".strip()
            official_topic = f"{topic_num} {topic_name}".strip()
            return title, official_topic

    # 2. Buscar primer heading de nivel 1 o 2 (# o ##)
    for line in first_lines:
        match = re.match(r"^#{1,2}\s+(.+)$", line.strip())
        if match:
            heading = match.group(1).strip()
            if not heading.lower().startswith("página"):
                return heading, heading

    # 3. Fallback a limpiar el nombre de archivo
    if filename:
        stem = Path(filename).stem
        cleaned = re.sub(r"^[A-Z0-9]+[_\-]", "", stem)  # Quitar prefijos tipo A2_
        cleaned = cleaned.replace("_", " ").replace("-", " ")
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned, cleaned

    return "Nuevo Apunte", ""


def strip_frontmatter(content: str) -> str:
    """Elimina frontmatter YAML existente del contenido si lo hay."""
    content = content.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    if content.startswith("---\n"):
        end = content.find("\n---", 4)
        if end != -1:
            return content[end + 4 :].lstrip("\n")
    return content


class IngestService:
    def __init__(self, ollama_client: OllamaClient | None = None) -> None:
        self._ollama_client = ollama_client or OllamaClient()

    def extract_from_pdf_bytes(
        self,
        pdf_bytes: bytes,
        filename: str = "",
        normalize: bool = True,
    ) -> dict[str, Any]:
        """
        Extrae texto estructurado desde un archivo PDF en memoria.
        Aplica heurísticas de descarte de cabeceras/pies repetidos y detección de headings.
        """
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = len(doc)
        warnings: list[str] = []

        if page_count == 0:
            return {
                "markdown": "",
                "raw_markdown": "",
                "detected_title": Path(filename).stem if filename else "Documento vacío",
                "official_topic": "",
                "page_count": 0,
                "headings": [],
                "stats": {"char_count": 0, "word_count": 0, "line_count": 0},
                "images": [],
                "warnings": ["El PDF no contiene páginas."],
            }

        repeated_headers_footers = _collect_repeated_header_footer_blocks(doc)
        page_texts: dict[int, str] = {}
        all_headings: list[str] = []

        for page in doc:
            blocks = _extract_blocks(page)
            body_candidates = [b.font_size for b in blocks if getattr(b, "font_size", 0) > 0]
            body_size = (
                sorted(body_candidates)[len(body_candidates) // 2]
                if body_candidates
                else 0.0
            )

            page_lines: list[str] = []
            for block in blocks:
                text = getattr(block, "text", "")
                sig_text = re.sub(r"\b\d+\b", "#", text).lower()
                if (sig_text, len(text.splitlines())) in repeated_headers_footers:
                    continue

                if _looks_like_toc_page(text):
                    continue

                heading_level = _infer_heading_level(getattr(block, "font_size", 0.0), body_size)
                if heading_level == 2:
                    page_lines.append(f"## {text}")
                    all_headings.append(text)
                elif heading_level == 3:
                    page_lines.append(f"### {text}")
                    all_headings.append(text)
                elif heading_level == 4:
                    page_lines.append(f"#### {text}")
                else:
                    page_lines.append(text)

            page_texts[page.number + 1] = _normalize_text("\n\n".join(page_lines))

        raw_lines = [
            f"> Documento extraído automáticamente desde `{filename or 'archivo PDF'}`.",
            f"> Páginas analizadas: {page_count}.",
            "",
        ]

        for page_number in range(1, page_count + 1):
            p_text = page_texts.get(page_number, "")
            if p_text:
                raw_lines.append(f"## Página {page_number}")
                raw_lines.append("")
                raw_lines.append(p_text)
                raw_lines.append("")

        raw_markdown = "\n".join(raw_lines).strip()

        if normalize:
            try:
                processed_markdown = normalize_markdown(raw_markdown)
            except Exception as exc:
                warnings.append(f"Error durante normalización: {exc}")
                processed_markdown = raw_markdown
        else:
            processed_markdown = raw_markdown

        detected_title, detected_topic = detect_note_title(processed_markdown, filename)

        # Extraer lista de títulos principales para el índice
        headings_clean: list[str] = []
        for line in processed_markdown.splitlines():
            m = re.match(r"^#{1,3}\s+(.+)$", line.strip())
            if m:
                h_text = m.group(1).strip()
                if not h_text.lower().startswith("página") and h_text not in headings_clean:
                    headings_clean.append(h_text)

        stats = {
            "char_count": len(processed_markdown),
            "word_count": len(processed_markdown.split()),
            "line_count": len(processed_markdown.splitlines()),
            "page_count": page_count,
        }

        return {
            "markdown": processed_markdown,
            "raw_markdown": raw_markdown,
            "detected_title": detected_title,
            "official_topic": detected_topic,
            "page_count": page_count,
            "headings": headings_clean[:20],
            "stats": stats,
            "images": [],
            "warnings": warnings,
        }

    def refine_markdown(self, markdown: str, instructions: str = "") -> dict[str, Any]:
        """
        Refina un documento Markdown usando Ollama, dividiéndolo en secciones
        manejables para conservar precisión sin exceder el context window.
        """
        prompt_instructions = (
            "Eres un editor de Markdown técnico para oposiciones TIC.\n"
            "Tu tarea es limpiar y estructurar el texto recibido sin resumir ni inventar información.\n"
            "- Une líneas o párrafos cortados a mitad de frase.\n"
            "- Convierte listas rotas en listas Markdown limpias (- o 1.).\n"
            "- Convierte tablas de texto en tablas Markdown si aplica.\n"
            "- Corrige erratas evidentes de OCR.\n"
            "- Conserva todos los términos técnicos, artículos legales y acrónimos.\n"
            "- No añadas explicaciones ni saludos: devuelve ÚNICAMENTE el Markdown refinado.\n"
        )
        if instructions.strip():
            prompt_instructions += f"\nInstrucciones adicionales del usuario: {instructions.strip()}\n"

        prompt = (
            f"{prompt_instructions}\n"
            f"=== CONTENIDO ORIGINAL ===\n\n"
            f"{markdown}\n\n"
            f"=== FIN CONTENIDO ORIGINAL ===\n\n"
            f"Markdown refinado:"
        )

        try:
            refined = self._ollama_client.generate(prompt)
            return {"refined_markdown": refined.strip(), "warnings": []}
        except OllamaClientError as exc:
            raise exc

    def publish_note(self, request: PublishNoteRequest) -> PublishNoteResponse:
        """
        Publica una nota en la base de conocimiento:
        1. Valida y crea la estructura de directorios en knowledge/processes/{process_slug}/apuntes/.
        2. Construye el frontmatter YAML estandarizado.
        3. Guarda físicamente el archivo .md.
        4. Invoca build_index para regenerar knowledge_index.json.
        """
        knowledge_root = Path(settings.knowledge_dir).resolve()
        slug_clean = request.process_slug.strip().strip("/")
        target_dir = knowledge_root / "processes" / slug_clean / "apuntes"
        target_dir.mkdir(parents=True, exist_ok=True)

        # Nombre de archivo
        if request.custom_filename and request.custom_filename.strip():
            filename = sanitize_filename(request.custom_filename)
        else:
            filename = sanitize_filename(f"{request.title}.md")

        target_file = target_dir / filename

        # ID de la nota: slug URL-friendly
        note_id = slugify(request.title) or slugify(target_file.stem) or "nota"

        # Limpiar cualquier frontmatter preexistente en el cuerpo
        clean_body = strip_frontmatter(request.markdown_body).strip()

        # Construir frontmatter YAML estándar
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        official_topic = request.official_topic.strip() or request.title.strip()

        tags_lines = []
        if request.tags:
            tags_lines = [f'  - "{t.strip()}"' for t in request.tags if t.strip()]

        frontmatter_lines = [
            "---",
            f'id: "{note_id}"',
            f'title: "{request.title.strip()}"',
            'type: "apunte"',
            f'status: "{request.status.strip()}"',
            f'source: "{request.source.strip()}"',
            "processes:",
            f'  - "{slug_clean}"',
            f'official_topic: "{official_topic}"',
            "source_ids: []",
        ]

        if tags_lines:
            frontmatter_lines.append("tags:")
            frontmatter_lines.extend(tags_lines)
        else:
            frontmatter_lines.append("tags: []")

        frontmatter_lines.extend([
            f'created_at: "{today}"',
            f'last_reviewed: "{today}"',
            "ai_generated: false",
            "ai_cleaned: true",
            "ai_sources: []",
            "needs_human_review: false",
            "---",
        ])

        full_content = "\n".join(frontmatter_lines) + "\n\n" + clean_body + "\n"
        target_file.write_text(full_content, encoding="utf-8")

        # Reconstruir índice si el indexador está disponible
        index_rebuilt = False
        warnings: list[str] = []

        if build_index is not None:
            try:
                index_output = Path(settings.index_output_path).resolve()
                build_index(knowledge_root, index_output)
                index_rebuilt = True
            except Exception as exc:
                warnings.append(f"No se pudo regenerar el índice automáticamente: {exc}")
        else:
            warnings.append("build_index no disponible para regenerar knowledge_index.json.")

        # Ruta relativa al repo
        repo_root = knowledge_root.parent
        try:
            rel_path = str(target_file.relative_to(repo_root)).replace("\\", "/")
        except ValueError:
            rel_path = str(target_file).replace("\\", "/")

        note_url = f"note.php?id={note_id}&process={slug_clean}"

        return PublishNoteResponse(
            success=True,
            note_id=note_id,
            slug=slugify(request.title),
            file_path=rel_path,
            index_rebuilt=index_rebuilt,
            note_url=note_url,
            warnings=warnings,
        )
