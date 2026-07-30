import re
from pathlib import Path
from pypdf import PdfReader
import argparse


def _sanitize_filename(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-")
    return name or "img"


def extract_pdf_to_markdown(input_pdf: Path, output_md: Path, extract_images: bool = True) -> None:
    if not input_pdf.exists():
        raise FileNotFoundError(f"No existe el PDF: {input_pdf}")

    output_md.parent.mkdir(parents=True, exist_ok=True)

    images_dir = output_md.parent / output_md.stem / "images"
    images_dir_relative = f"{output_md.stem}/images"
    reader = PdfReader(str(input_pdf))

    lines = [
        f"# Texto extraído: {input_pdf.name}",
        "",
        "> Texto extraído automáticamente desde PDF. Puede contener errores de formato.",
        "",
        f"- Archivo origen: `{input_pdf.as_posix()}`",
        f"- Número de páginas: {len(reader.pages)}",
        "",
    ]

    total_images = 0

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        lines.append(f"## Página {index}")
        lines.append("")

        if text.strip():
            lines.append(text.strip())
        else:
            lines.append("_No se pudo extraer texto de esta página._")

        lines.append("")

        if extract_images:
            try:
                page_images = list(page.images)
            except Exception:
                page_images = []

            for img_index, image_file in enumerate(page_images, start=1):
                total_images += 1
                original_name = Path(image_file.name).name if image_file.name else "img"
                suffix = Path(original_name).suffix or ".png"
                filename = f"pagina-{index}-img-{img_index}{suffix}"
                filename = _sanitize_filename(filename)

                images_dir.mkdir(parents=True, exist_ok=True)
                (images_dir / filename).write_bytes(image_file.data)

                lines.append(f"![Imagen de la página {index}]({images_dir_relative}/{filename})")
                lines.append("")

    output_md.write_text("\n".join(lines), encoding="utf-8")

    if total_images:
        print(f"Extraídas {total_images} imágenes en: {images_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrae texto (e imágenes) de un PDF a Markdown.")
    parser.add_argument("input_pdf", help="Ruta del PDF de origen")
    parser.add_argument("output_md", help="Ruta del Markdown de salida")
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="No extraer imágenes incrustadas, solo texto (comportamiento anterior).",
    )

    args = parser.parse_args()

    extract_pdf_to_markdown(
        input_pdf=Path(args.input_pdf),
        output_md=Path(args.output_md),
        extract_images=not args.no_images,
    )


if __name__ == "__main__":
    main()