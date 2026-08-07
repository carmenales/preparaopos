#!/usr/bin/env python3
"""
Refina apuntes Markdown usando un modelo LLM de Ollama.

- Toma Markdown extraído (por ejemplo de extract_pdf_text.py).
- Envía el contenido a Ollama con instrucciones claras.
- Recibe Markdown refinado (misma estructura, sin resumir ni inventar).
- Soporta archivo único o carpeta recursiva, igual que refine_markdown_note.py.
"""

from __future__ import annotations

import argparse, re
import textwrap
from pathlib import Path
from typing import Optional
import requests
import hashlib

MAX_CHUNK_CHARS = 2000
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:latest"
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.0
CACHE_DIR = Path(".llm_cache")
CACHE_DIR.mkdir(exist_ok=True)
PAGE_HEADING_RE = re.compile(r"^## Página \d+\s*$", re.MULTILINE)

def cache_path(chunk: str) -> Path:
    digest = hashlib.sha256(chunk.encode("utf8")).hexdigest()
    return CACHE_DIR / f"{digest}.md"


def load_cache(chunk: str) -> Optional[str]:
    path = cache_path(chunk)

    if path.exists():
        return path.read_text("utf8")

    return None


def save_cache(chunk: str, refined: str) -> None:
    cache_path(chunk).write_text(refined, encoding="utf8")

def split_by_pages(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    chunks: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        if PAGE_HEADING_RE.match(line):
            if current:
                chunks.append(current)
                current = []
        current.append(line)

    if current:
        chunks.append(current)

    return ["\n".join(chunk).strip() + "\n" for chunk in chunks if any(l.strip() for l in chunk)]


def split_by_size(markdown: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    lines = markdown.splitlines()
    chunks: list[str] = []
    buffer: list[str] = []
    current_len = 0

    for line in lines:
        line_with_newline = line + "\n"
        line_len = len(line_with_newline)

        if line_len >= max_chars:
            if buffer:
                chunks.append("".join(buffer).strip() + "\n")
                buffer = []
                current_len = 0
            chunks.append(line_with_newline.strip() + "\n")
            continue

        if current_len + line_len > max_chars and buffer:
            chunks.append("".join(buffer).strip() + "\n")
            buffer = []
            current_len = 0

        buffer.append(line_with_newline)
        current_len += line_len

    if buffer:
        chunks.append("".join(buffer).strip() + "\n")

    return chunks


def split_markdown(markdown: str, max_chunk_chars: int) -> list[str]:
    page_chunks = split_by_pages(markdown)

    if len(page_chunks) <= 1:
        source_chunks = page_chunks or [markdown]
    else:
        source_chunks = page_chunks

    chunks: list[str] = []

    for page_chunk in source_chunks:
        if len(page_chunk) <= max_chunk_chars:
            chunks.append(page_chunk)
        else:
            chunks.extend(
                split_by_size(
                    page_chunk,
                    max_chars=max_chunk_chars,
                )
            )

    return [
        chunk.strip() + "\n"
        for chunk in chunks
        if chunk.strip()
    ]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_prompt(markdown_text: str) -> str:
    """
    Prompt en español, centrado en edición de apuntes TIC.
    """
    instructions = textwrap.dedent("""
    Eres un editor de Markdown.

    Devuelve exactamente el mismo contenido.

    No reformules.
    No resumas.
    No expliques.
    No cambies el orden.

    Únicamente:

    - une líneas partidas
    - une párrafos partidos
    - corrige listas Markdown
    - corrige tablas Markdown
    - elimina cabeceras repetidas
    - elimina pies repetidos

    No añadas contenido.
    No elimines contenido técnico.
    Devuelve solo Markdown.
    """).strip()

    return (
        instructions
        + "\n\n=== CONTENIDO ORIGINAL ===\n\n"
        + markdown_text
        + "\n\n=== FIN CONTENIDO ORIGINAL ===\n\n"
        + "Markdown refinado:"
    )


def check_ollama(base_url: str) -> None:
    url = base_url.rstrip("/") + "/api/tags"

    try:
        response = requests.get(url, timeout=(5, 15))
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(
            f"No se puede conectar con Ollama en {url}. "
            "Comprueba que Ollama está iniciado."
        ) from exc
    

def call_ollama(
    markdown_text: str,
    base_url: str,
    model: str,
    max_tokens: int,
    temperature: float,
) -> str:
    prompt = build_prompt(markdown_text)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }

    url = base_url.rstrip("/") + "/api/generate"

    response = requests.post(
        url,
        json=payload,
        timeout=(10, 600),
    )
    response.raise_for_status()

    data = response.json()
    result = (data.get("response") or "").strip()

    if not result:
        raise RuntimeError("Ollama ha devuelto una respuesta vacía.")

    return result


def refine_markdown_with_llm(
    text: str,
    base_url: str,
    model: str,
    max_tokens: int,
    temperature: float,
) -> str:
    return call_ollama(text, base_url, model, max_tokens, temperature)

def refine_markdown_document(
    markdown: str,
    ollama_url: str,
    model: str,
    max_tokens: int,
    temperature: float,
    max_chunk_chars: int = 2000,
) -> str:
    chunks = split_markdown(markdown, max_chunk_chars)

    if not chunks:
        return markdown

    refined_chunks: list[str] = []

    for index, chunk in enumerate(chunks, start=1):
        print(
            f"  Refinando bloque {index}/{len(chunks)} "
            f"({len(chunk)} caracteres)..."
        )

        cached = load_cache(chunk)

        if cached is not None:
            print(f"  Cache bloque {index}/{len(chunks)}")
            refined_chunks.append(cached.strip())
            continue

        refined = call_ollama(
            markdown_text=chunk,
            base_url=ollama_url,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        save_cache(chunk, refined)

        refined_chunks.append(refined.strip())

    return "\n\n".join(refined_chunks).strip() + "\n"


def process_file(
    input_path: Path,
    output_path: Path,
    base_url: str,
    model: str,
    max_tokens: int,
    temperature: float,
) -> None:

    original = read_text(input_path)

    refined = refine_markdown_document(
        markdown=original,
        ollama_url=base_url,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        max_chunk_chars=MAX_CHUNK_CHARS,
    )

    write_text(output_path, refined)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Refina Markdown usando un modelo LLM de Ollama."
    )
    parser.add_argument("input", help="Archivo .md o carpeta de entrada")
    parser.add_argument("output", help="Archivo .md o carpeta de salida")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescribir archivos existentes",
    )
    parser.add_argument(
        "--ollama-url",
        default=DEFAULT_OLLAMA_URL,
        help=f"URL base de Ollama (por defecto {DEFAULT_OLLAMA_URL})",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Nombre del modelo en Ollama (por defecto {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help="Máximo de tokens que puede generar el modelo",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help="Temperatura (0.0 recomienda determinismo para edición)",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    check_ollama(args.ollama_url)

    if input_path.is_file():
        target = output_path
        if output_path.exists() and output_path.is_dir():
            target = output_path / input_path.name

        if target.exists() and not args.overwrite:
            raise FileExistsError(
                f"Ya existe: {target}. Usa --overwrite para sobrescribir."
            )

        process_file(
            input_path,
            target,
            base_url=args.ollama_url,
            model=args.model,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
        return

    if not input_path.exists() or not input_path.is_dir():
        raise FileNotFoundError(f"No existe la carpeta de entrada: {input_path}")

    md_files = sorted(p for p in input_path.rglob("*.md") if p.is_file())
    if not md_files:
        print(f"No se han encontrado .md en {input_path}")
        return

    for source in md_files:
        rel = source.relative_to(input_path)
        target = output_path / rel
        if target.exists() and not args.overwrite:
            print(f"[omitido] {rel}")
            continue

        try:
            process_file(
                source,
                target,
                base_url=args.ollama_url,
                model=args.model,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
            )
            print(f"[ok] {rel}")
        except Exception as exc:
            print(f"[error] {rel}: {exc}")

if __name__ == "__main__":
    main()