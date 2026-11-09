"""
services/knowledge/ingest_service.py

Servicio para la ingestión y publicación de nuevas fuentes de conocimiento.
Coordina:
- Extracción estructurada de texto y headings desde PDFs mediante PdfExtractor.
- Normalización determinista mediante MarkdownNormalizer.
- Refinado opcional asistido por LLM (Ollama).
- Publicación física en knowledge/processes/{process_slug}/apuntes/ con YAML frontmatter.
- Sincronización automática de knowledge_index.json.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import settings
from markdown_normalizer import (
    MarkdownNormalizer,
    clean_inline_noise,
    is_pure_page_or_header_noise,
    normalize_markdown,
)
from ollama_client import OllamaClient, OllamaClientError
from pdf_extractor import ExtractedDocument, PdfExtractor
from schemas import DeleteNoteResponse, PublishNoteRequest, PublishNoteResponse
from text_utils import slugify

try:
    from build_knowledge_index import build_index
except ImportError:
    build_index = None


def sanitize_filename(filename: str) -> str:
    """Limpia caracteres inválidos en nombres de fichero y asegura extensión .md."""
    has_md = filename.lower().endswith(".md")
    base = filename[:-3] if has_md else filename
    cleaned = re.sub(r'[\\/*?:"<>|]', "-", base)
    cleaned = re.sub(r"\s*-\s*", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned).strip(" -.")
    return f"{cleaned}.md" if cleaned else "apunte.md"


def strip_frontmatter(content: str) -> str:
    """Elimina frontmatter YAML existente del contenido si lo hay."""
    content = content.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    if content.startswith("---\n"):
        end = content.find("\n---", 4)
        if end != -1:
            return content[end + 4 :].lstrip("\n")
    return content


def detect_note_title(extracted_text: str, filename: str = "") -> tuple[str, str]:
    """Función de conveniencia para compatibilidad con código existente."""
    return PdfExtractor().detect_note_title(extracted_text, filename=filename)


class IngestService:
    def __init__(
        self,
        ollama_client: OllamaClient | None = None,
        pdf_extractor: PdfExtractor | None = None,
        markdown_normalizer: type[MarkdownNormalizer] = MarkdownNormalizer,
    ) -> None:
        self._ollama_client = ollama_client or OllamaClient()
        self._pdf_extractor = pdf_extractor or PdfExtractor(normalizer=markdown_normalizer)
        self._markdown_normalizer = markdown_normalizer

    def extract_from_pdf_bytes(
        self,
        pdf_bytes: bytes,
        filename: str = "",
        normalize: bool = True,
    ) -> dict[str, Any]:
        """
        Extrae texto estructurado desde un archivo PDF en memoria.
        Aplica heurísticas de segmentación por línea, descarte de cabeceras/pies repetidos
        y detección de títulos limpios.
        """
        doc_result: ExtractedDocument = self._pdf_extractor.extract_from_bytes(
            pdf_bytes=pdf_bytes,
            filename=filename,
            normalize=normalize,
        )

        return {
            "markdown": doc_result.markdown,
            "raw_markdown": doc_result.raw_markdown,
            "detected_title": doc_result.detected_title,
            "official_topic": doc_result.official_topic,
            "page_count": doc_result.page_count,
            "headings": doc_result.headings,
            "stats": doc_result.stats,
            "images": doc_result.images,
            "warnings": doc_result.warnings,
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
            f"ai_cleaned: {str(request.ai_cleaned).lower()}",
            "ai_sources: []",
            f"needs_human_review: {str(request.needs_human_review).lower()}",
            "---",
        ])

        full_content = "\n".join(frontmatter_lines) + "\n\n" + clean_body + "\n"
        target_file.write_text(full_content, encoding="utf-8")

        warnings: list[str] = []
        index_rebuilt = _rebuild_index(knowledge_root, warnings)

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

    def delete_note(self, note_path: str) -> DeleteNoteResponse:
        """Borra definitivamente el fichero .md de un apunte y regenera knowledge_index.json.

        note_path es la ruta del índice, relativa a la raíz del repo («knowledge/processes/…/x.md»).
        Se borra por ruta y no por id porque hay ids repetidos en el índice. No toca las imágenes:
        pueden estar compartidas con otros apuntes de la misma carpeta.
        """
        knowledge_root = Path(settings.knowledge_dir).resolve()
        target = (knowledge_root.parent / note_path.strip().lstrip("/\\")).resolve()
        try:
            rel_to_knowledge = target.relative_to(knowledge_root)
        except ValueError as exc:
            raise ValueError("La ruta no está dentro de la base de conocimiento.") from exc
        if target.suffix.lower() != ".md" or not rel_to_knowledge.parts:
            raise ValueError("Solo se pueden borrar ficheros .md de apuntes.")
        if not target.is_file():
            raise FileNotFoundError(f"No existe el apunte {note_path}")

        target.unlink()
        warnings: list[str] = []
        index_rebuilt = _rebuild_index(knowledge_root, warnings)
        rel_path = str(target.relative_to(knowledge_root.parent)).replace("\\", "/")
        return DeleteNoteResponse(success=True, file_path=rel_path, index_rebuilt=index_rebuilt, warnings=warnings)


def _rebuild_index(knowledge_root: Path, warnings: list[str]) -> bool:
    """Regenera knowledge_index.json si el indexador está disponible; anota el fallo en warnings."""
    if build_index is None:
        warnings.append("build_index no disponible para regenerar knowledge_index.json.")
        return False
    try:
        build_index(knowledge_root, Path(settings.index_output_path).resolve())
        return True
    except Exception as exc:
        warnings.append(f"No se pudo regenerar el índice automáticamente: {exc}")
        return False
