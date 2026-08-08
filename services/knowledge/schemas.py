"""
services/knowledge/schemas.py

Modelos Pydantic del Knowledge Service (ya es dependencia de FastAPI).
Módulo plano, sin subcarpeta models/ — a este nivel de tamaño no aporta
nada la separación en paquete.

RetrievedFragment conserva como mínimo lo exigido para trazabilidad:
chunk_id, note_id, source_id, heading, score, content. Se añaden
note_title, anchor y tags porque ya vienen gratis desde el servicio de
embeddings (Milestone 0) y evitan tener que ampliar este esquema en el
siguiente milestone.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class RetrievedFragment(BaseModel):
    """Un chunk devuelto por services/embeddings, normalizado."""

    chunk_id: str | None = None
    note_id: str
    source_id: str
    note_title: str
    heading: str | None = None
    anchor: str | None = None
    score: float
    content: str
    tags: list[str] = Field(default_factory=list)

    @property
    def heading_label(self) -> str:
        return self.heading or "(introducción)"


class GenerateNoteRequest(BaseModel):
    """Payload de entrada para POST /notes/generate."""

    process_slug: str = Field(..., min_length=1, description="Proceso selectivo, p. ej. 'ayuntamiento-majadahonda'.")
    topic: str = Field(..., min_length=1, description="Tema a generar, p. ej. 'Tipos de cifrado'.")
    description: str = Field(default="", description="Descripción opcional que amplía la consulta de recuperación.")
    top_k: int | None = Field(default=None, ge=1, le=50)
    min_score: float | None = Field(default=None, ge=0.0, le=1.0)

    def build_query(self) -> str:
        """Consulta única de recuperación: tema + descripción (si la hay)."""
        if self.description.strip():
            return f"{self.topic}. {self.description}".strip()
        return self.topic.strip()


class NoteFrontmatter(BaseModel):
    """
    Frontmatter generado de forma determinista (frontmatter_generator.py),
    NUNCA por el LLM. Nombres de campo alineados con el frontmatter
    descrito en las instrucciones del proyecto.
    """

    id: str
    title: str
    official_topic: str
    processes: list[str]
    profiles: list[str] = Field(default_factory=list)
    shared_with: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    status: str = "draft"
    created_at: str
    ai_generated: bool = True
    needs_human_review: bool = True
    source_ids: list[str] = Field(default_factory=list)
    generator_model: str
    fragment_count: int

    def to_yaml_block(self) -> str:
        """
        Serializa a un bloque YAML simple, sin PyYAML (esquema controlado,
        una dependencia menos en la imagen).
        """

        def yaml_list(values: list[str]) -> str:
            if not values:
                return "[]"
            return "\n" + "\n".join(f"  - {value}" for value in values)

        lines = [
            "---",
            f"id: {self.id}",
            f"title: {self.title}",
            f"official_topic: {self.official_topic}",
            f"processes:{yaml_list(self.processes)}",
            f"profiles:{yaml_list(self.profiles)}",
            f"shared_with:{yaml_list(self.shared_with)}",
            f"tags:{yaml_list(self.tags)}",
            f"status: {self.status}",
            f"created_at: {self.created_at}",
            f"ai_generated: {str(self.ai_generated).lower()}",
            f"needs_human_review: {str(self.needs_human_review).lower()}",
            f"source_ids:{yaml_list(self.source_ids)}",
            "generator:",
            "  type: knowledge_service",
            "  milestone: 1",
            f"  model: {self.generator_model}",
            f"  fragment_count: {self.fragment_count}",
            "---",
        ]
        return "\n".join(lines)


class GenerateNotePreview(BaseModel):
    """Respuesta de POST /notes/generate: vista previa, nada guardado."""

    frontmatter: NoteFrontmatter
    markdown_body: str
    full_markdown: str
    fragments_used: list[RetrievedFragment]
    warnings: list[str] = Field(default_factory=list)
