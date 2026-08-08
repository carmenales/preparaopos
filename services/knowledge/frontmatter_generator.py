"""
services/knowledge/frontmatter_generator.py

Construye el frontmatter del apunte generado de forma enteramente
determinista — el LLM nunca decide id, processes, tags ni source_ids.
Solo Python, sin llamadas externas.

source_ids se deriva EXCLUSIVAMENTE de los fragmentos recuperados por
SearchClient (los mismos que se le pasaron a note_generator.py): así
es imposible que el frontmatter declare una fuente que no haya
alimentado realmente la generación, y el LLM no tiene ninguna vía para
"colar" una fuente inventada en este campo, porque no lo toca.
"""

from __future__ import annotations

from datetime import date

from config import settings
from schemas import GenerateNoteRequest, NoteFrontmatter, RetrievedFragment
from text_utils import slugify

# Límite de tags propagados al frontmatter generado: evita que un
# apunte con fragmentos de fuentes distintas termine con decenas de
# tags poco selectivos. Se conservan los más frecuentes.
MAX_TAGS = 10


def _collect_tags(fragments: list[RetrievedFragment]) -> list[str]:
    counts: dict[str, int] = {}

    for fragment in fragments:
        for tag in fragment.tags:
            normalized = tag.strip().lower()
            if not normalized:
                continue
            counts[normalized] = counts.get(normalized, 0) + 1

    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [tag for tag, _ in ordered[:MAX_TAGS]]


def _collect_source_ids(fragments: list[RetrievedFragment]) -> list[str]:
    seen: dict[str, None] = {}
    for fragment in fragments:
        seen.setdefault(fragment.source_id, None)
    return list(seen.keys())


def build_frontmatter(
    request: GenerateNoteRequest,
    fragments: list[RetrievedFragment],
) -> NoteFrontmatter:
    note_slug = slugify(f"{request.process_slug}-{request.topic}")

    return NoteFrontmatter(
        id=note_slug,
        title=request.topic.strip(),
        official_topic=request.topic.strip(),
        processes=[request.process_slug],
        profiles=[],
        shared_with=[],
        tags=_collect_tags(fragments),
        status="draft",
        created_at=date.today().isoformat(),
        ai_generated=True,
        needs_human_review=True,
        source_ids=_collect_source_ids(fragments),
        generator_model=settings.ollama_model,
        fragment_count=len(fragments),
    )
