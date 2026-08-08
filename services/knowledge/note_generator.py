"""
services/knowledge/note_generator.py

Convierte una lista de RetrievedFragment en el cuerpo Markdown de un
apunte, mediante Ollama.

Diseño pensado para evolucionar a generación por secciones sin rehacer
la interfaz pública:

- `_render_fragments_block()` serializa un conjunto de fragmentos a
  texto de prompt. Es la misma función que se reutilizará para generar
  UNA sección con SUS fragmentos, cuando exista outline_builder.
- `_generate_from_fragments()` hace una única llamada al LLM para un
  conjunto de fragmentos y devuelve el Markdown resultante. Es la
  función que, en el siguiente milestone, se llamará una vez POR
  SECCIÓN en lugar de una vez para todo el tema.
- `generate_body()` es la orquestación pública de este milestone: hoy
  llama a `_generate_from_fragments()` una sola vez con todos los
  fragmentos. El día que haya outline_builder, generate_body() pasará
  a iterar secciones y llamar a `_generate_from_fragments()` por cada
  una, concatenando los resultados — sin tocar las dos funciones de
  abajo.

Sin FastAPI ni conocimiento de HTTP: recibe un OllamaClient y una ruta
a prompts/ por constructor.
"""

from __future__ import annotations

from pathlib import Path

from ollama_client import OllamaClient
from schemas import RetrievedFragment

PROMPT_FILENAME = "note_generation.txt"

# Límite defensivo de caracteres de contexto enviados al LLM por
# llamada. Con top_k=20 fragmentos de knowledge/, esto rara vez se
# alcanza en este milestone (una sola llamada, todos los fragmentos);
# cuando exista generación por secciones, este límite se aplicará por
# sección, no al conjunto completo, así que ya está expresado como
# límite "por llamada" y no "por nota".
MAX_FRAGMENTS_CHARS_PER_CALL = 24000


class NoteGeneratorError(RuntimeError):
    """Error al generar el cuerpo del apunte."""


class NoteGenerator:
    def __init__(self, ollama_client: OllamaClient, prompts_dir: Path) -> None:
        self._ollama_client = ollama_client
        self._prompt_template = (prompts_dir / PROMPT_FILENAME).read_text(encoding="utf-8")

    def _render_fragments_block(
        self,
        fragments: list[RetrievedFragment],
    ) -> tuple[str, list[str]]:
        """
        Serializa un conjunto de fragmentos a texto plano para el prompt,
        con una cabecera por fragmento que identifica su procedencia
        (note_title + heading) — información de contexto para el LLM,
        no una invitación a inventar fuentes nuevas: las únicas fuentes
        válidas en la respuesta final son las de estos mismos fragmentos,
        y eso se garantiza en frontmatter_generator.py, no aquí.

        Reutilizable tal cual cuando se generen secciones individuales:
        se le pasaría solo el subconjunto de fragmentos de esa sección.
        """
        warnings: list[str] = []
        blocks: list[str] = []
        total_chars = 0

        for index, fragment in enumerate(fragments, start=1):
            header = f"[Fragmento {index} — {fragment.note_title} — {fragment.heading_label}]"
            block = f"{header}\n{fragment.content.strip()}"

            if total_chars + len(block) > MAX_FRAGMENTS_CHARS_PER_CALL:
                warnings.append(
                    f"Se han omitido {len(fragments) - index + 1} fragmentos de menor relevancia "
                    "por límite de longitud del contexto enviado al modelo."
                )
                break

            blocks.append(block)
            total_chars += len(block)

        return "\n\n".join(blocks), warnings

    def _generate_from_fragments(
        self,
        topic: str,
        description: str,
        fragments: list[RetrievedFragment],
    ) -> tuple[str, list[str]]:
        """
        Una única llamada al LLM para un conjunto de fragmentos. Esta es
        la unidad de trabajo que se reutilizará por sección en el
        siguiente milestone (una llamada por apartado del outline en
        vez de una llamada para el tema completo).
        """
        fragments_block, warnings = self._render_fragments_block(fragments)

        prompt = self._prompt_template.format(
            topic=topic,
            description=description or "(sin descripción adicional)",
            fragments_block=fragments_block,
        )

        markdown = self._ollama_client.generate(prompt).strip()

        if not markdown:
            raise NoteGeneratorError("El modelo no ha devuelto contenido para el apunte.")

        return markdown, warnings

    def generate_body(
        self,
        topic: str,
        description: str,
        fragments: list[RetrievedFragment],
    ) -> tuple[str, list[str]]:
        """
        Orquestación pública de este milestone: una sola llamada con
        todos los fragmentos recuperados. Cuando exista outline_builder,
        esta función pasará a iterar secciones y llamar a
        `_generate_from_fragments()` una vez por cada una, concatenando
        los Markdown resultantes — el resto del módulo no cambia.
        """
        if not fragments:
            raise NoteGeneratorError(
                "No hay fragmentos con evidencia suficiente para generar el apunte."
            )

        return self._generate_from_fragments(topic, description, fragments)
