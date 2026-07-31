#!/usr/bin/env python3
"""
Extrae en lote todos los .pdf y .pptx de una carpeta (recursivo) a Markdown,
reutilizando extract_pdf_text.py y extract_pptx_text.py. Mantiene la misma
estructura de subcarpetas relativa en la salida.

Uso:
    python3 scripts/batch_extract.py ruta/a/mis-pdfs tmp/extraido

    # Volver a procesar aunque el .md de salida ya exista:
    python3 scripts/batch_extract.py ruta/a/mis-pdfs tmp/extraido --force

    # Sin imágenes, más rápido si solo quieres repasar el texto:
    python3 scripts/batch_extract.py ruta/a/mis-pdfs tmp/extraido --no-images
"""

import argparse
from pathlib import Path

from extract_pdf_text import extract_pdf_to_markdown
from extract_pptx_text import extract_pptx_to_markdown

SUPPORTED_EXTENSIONS = {".pdf", ".pptx"}


def find_source_files(input_dir: Path) -> list[Path]:
    return sorted(
        path for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def batch_extract(input_dir: Path, output_dir: Path, extract_images: bool, force: bool) -> None:
    if not input_dir.exists():
        raise FileNotFoundError(f"No existe la carpeta de entrada: {input_dir}")

    source_files = find_source_files(input_dir)

    if not source_files:
        print(f"No se ha encontrado ningún .pdf/.pptx en {input_dir}")
        return

    print(f"Encontrados {len(source_files)} ficheros para procesar.\n")

    processed = 0
    skipped = 0
    failed = 0

    for source_path in source_files:
        relative_path = source_path.relative_to(input_dir)
        output_md = (output_dir / relative_path).with_suffix(".md")

        if output_md.exists() and not force:
            print(f"  [omitido, ya existe] {relative_path}")
            skipped += 1
            continue

        print(f"  [procesando] {relative_path}")

        try:
            if source_path.suffix.lower() == ".pdf":
                extract_pdf_to_markdown(source_path, output_md, extract_images=extract_images)
            else:
                extract_pptx_to_markdown(source_path, output_md, extract_images=extract_images)
            processed += 1
        except Exception as error:
            print(f"    ERROR: {error}")
            failed += 1

    print(f"\nHecho. Procesados: {processed} · Omitidos: {skipped} · Con error: {failed}")
    print(f"Salida en: {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrae en lote PDF/PPTX de una carpeta a Markdown.")
    parser.add_argument("input_dir", help="Carpeta con los PDF/PPTX de origen (busca recursivamente)")
    parser.add_argument("output_dir", help="Carpeta de salida (se replica la estructura relativa de entrada)")
    parser.add_argument("--no-images", action="store_true", help="No extraer imágenes incrustadas.")
    parser.add_argument("--force", action="store_true", help="Reprocesar aunque el .md de salida ya exista.")

    args = parser.parse_args()

    batch_extract(
        input_dir=Path(args.input_dir),
        output_dir=Path(args.output_dir),
        extract_images=not args.no_images,
        force=args.force,
    )


if __name__ == "__main__":
    main()
