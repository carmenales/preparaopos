#!/usr/bin/env python3
"""Extrae en lote todos los .pdf y .pptx de una carpeta (recursivo) a Markdown.

Permite ejecutar:
- sólo extracción,
- extracción + normalización,
- extracción + normalización + refinado,
- o el pipeline completo.

También puede conservar o limpiar artefactos intermedios.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

from extract_pdf_text import extract_pdf_to_markdown
from normalize_markdown import normalize_markdown
from refine_markdown_llm import refine_markdown_document

SUPPORTED_EXTENSIONS = {".pdf"}
STAGE_EXTRACT = "extract"
STAGE_NORMALIZE = "normalize"
STAGE_REFINE = "refine"


def find_source_files(input_dir: Path) -> list[Path]:
    return sorted(
        path for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def build_stage_paths(base_output: Path, relative_source: Path) -> tuple[Path, Path, Path]:
    stem = relative_source.with_suffix(".md")
    extracted = base_output / "01_extracted" / stem
    normalized = base_output / "02_normalized" / stem
    refined = base_output / "03_refined" / stem
    return extracted, normalized, refined


def extract_stage(
    source_path: Path,
    output_md: Path,
    extract_images: bool,
) -> None:
    ensure_dir(output_md.parent)

    if source_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"Formato no soportado: {source_path.suffix}. "
            "Este pipeline solo procesa PDF."
        )

    extract_pdf_to_markdown(
        source_path,
        output_md,
        extract_images=extract_images,
    )


def normalize_stage(input_md: Path, output_md: Path) -> None:
    ensure_dir(output_md.parent)
    content = read_text(input_md)
    write_text(output_md, normalize_markdown(content))


def refine_stage(
    input_md: Path,
    output_md: Path,
    ollama_url: str,
    model: str,
    max_tokens: int,
    temperature: float,
    max_chunk_chars: int,
) -> None:
    ensure_dir(output_md.parent)

    content = read_text(input_md)

    refined_content = refine_markdown_document(
        markdown=content,
        ollama_url=ollama_url,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        max_chunk_chars=max_chunk_chars,
    )

    write_text(output_md, refined_content)


def cleanup_intermediate_files(extracted: Path | None, normalized: Path | None, keep_intermediate: bool, stage: str) -> None:
    if keep_intermediate:
        return

    if stage == STAGE_EXTRACT:
        return

    if extracted and extracted.exists():
        extracted.unlink(missing_ok=True)
        _remove_empty_parents(extracted.parent)

    if stage == STAGE_NORMALIZE:
        return

    if normalized and normalized.exists():
        normalized.unlink(missing_ok=True)
        _remove_empty_parents(normalized.parent)


def _remove_empty_parents(path: Path) -> None:
    current = path
    while current.name not in {"01_extracted", "02_normalized", "03_refined"}:
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent


def process_file(
    source_path: Path,
    input_dir: Path,
    output_dir: Path,
    stage: str,
    force: bool,
    extract_images: bool,
    keep_intermediate: bool,
    ollama_url: str,
    model: str,
    max_tokens: int,
    temperature: float,
    max_chunk_chars: int,
) -> tuple[bool, str]:
    relative_path = source_path.relative_to(input_dir)

    extracted_md, normalized_md, refined_md = build_stage_paths(
        output_dir,
        relative_path,
    )

    final_target = {
        STAGE_EXTRACT: extracted_md,
        STAGE_NORMALIZE: normalized_md,
        STAGE_REFINE: refined_md,
    }[stage]

    if final_target.exists() and not force:
        return False, f"[omitido, ya existe] {relative_path}"

    try:
        extract_stage(
            source_path=source_path,
            output_md=extracted_md,
            extract_images=extract_images,
        )

        if stage == STAGE_EXTRACT:
            return True, f"[ok] {relative_path}"

        normalize_stage(
            input_md=extracted_md,
            output_md=normalized_md,
        )

        if stage == STAGE_NORMALIZE:
            cleanup_intermediate_files(
                extracted=extracted_md,
                normalized=normalized_md,
                keep_intermediate=keep_intermediate,
                stage=stage,
            )
            return True, f"[ok] {relative_path}"

        refine_stage(
            input_md=normalized_md,
            output_md=refined_md,
            ollama_url=ollama_url,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            max_chunk_chars=max_chunk_chars,
        )

        cleanup_intermediate_files(
            extracted=extracted_md,
            normalized=normalized_md,
            keep_intermediate=keep_intermediate,
            stage=stage,
        )

    except Exception as error:
        return False, f"[error] {relative_path}: {error}"

    return True, f"[ok] {relative_path}"


def batch_extract(
    input_dir: Path,
    output_dir: Path,
    stage: str,
    extract_images: bool,
    force: bool,
    keep_intermediate: bool,
    ollama_url: str,
    model: str,
    max_tokens: int,
    temperature: float,
    max_chunk_chars: int,
) -> int:
    if not input_dir.exists() or not input_dir.is_dir():
        raise FileNotFoundError(f"No existe la carpeta de entrada: {input_dir}")

    ensure_dir(output_dir)

    source_files = find_source_files(input_dir)
    if not source_files:
        print(f"No se ha encontrado ningún PDF en {input_dir}")
        return 0

    print(f"Encontrados {len(source_files)} ficheros para procesar.")
    print(f"Salida base: {output_dir}")
    print(f"Modo: {stage}")
    print()

    processed = 0
    skipped = 0
    failed = 0

    for source_path in source_files:
        ok, message = process_file(
            source_path=source_path,
            input_dir=input_dir,
            output_dir=output_dir,
            stage=stage,
            force=force,
            extract_images=extract_images,
            keep_intermediate=keep_intermediate,
            ollama_url=ollama_url,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            max_chunk_chars=max_chunk_chars,
        )
        print(f"  {message}")
        if ok:
            if message.startswith("[omitido"):
                skipped += 1
            else:
                processed += 1
        elif message.startswith("[error"):
            failed += 1

    print()
    print(f"Hecho. Procesados: {processed} · Omitidos: {skipped} · Con error: {failed}")
    return 0 if failed == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extrae en lote PDF/PPTX de una carpeta a Markdown.")
    parser.add_argument("input_dir", help="Carpeta con los PDF/PPTX de origen (busca recursivamente)")
    parser.add_argument("output_dir", help="Carpeta base de salida")
    parser.add_argument(
        "--stage",
        choices=[STAGE_EXTRACT, STAGE_NORMALIZE, STAGE_REFINE],
        default=STAGE_REFINE,
        help="Paso final a ejecutar: extract, normalize o refine. Por defecto: refine.",
    )
    parser.add_argument("--no-images", action="store_true", help="No extraer imágenes incrustadas.")
    parser.add_argument("--force", action="store_true", help="Reprocesar aunque el .md de salida ya exista.")
    parser.add_argument(
        "--keep-intermediate",
        action="store_true",
        help="Conservar los .md intermedios de 01_extracted y 02_normalized.",
    )
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="URL base de Ollama.",
    )

    parser.add_argument(
        "--model",
        default="llama3.1:latest",
        help="Modelo de Ollama para el refinado.",
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=512,
        help="Máximo de tokens generados por bloque.",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Temperatura del modelo.",
    )

    parser.add_argument(
        "--max-chunk-chars",
        type=int,
        default=2000,
        help="Tamaño máximo de cada bloque enviado a Ollama.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        exit_code = batch_extract(
            input_dir=Path(args.input_dir),
            output_dir=Path(args.output_dir),
            stage=args.stage,
            extract_images=not args.no_images,
            force=args.force,
            keep_intermediate=args.keep_intermediate,
            ollama_url=args.ollama_url,
            model=args.model,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            max_chunk_chars=args.max_chunk_chars,
        )
    except Exception as error:
        print(f"ERROR FATAL: {error}", file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
