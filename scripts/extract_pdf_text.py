from pathlib import Path
from pypdf import PdfReader
import argparse


def extract_pdf_to_markdown(input_pdf: Path, output_md: Path) -> None:
    if not input_pdf.exists():
        raise FileNotFoundError(f"No existe el PDF: {input_pdf}")

    output_md.parent.mkdir(parents=True, exist_ok=True)

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

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        lines.append(f"## Página {index}")
        lines.append("")

        if text.strip():
            lines.append(text.strip())
        else:
            lines.append("_No se pudo extraer texto de esta página._")

        lines.append("")

    output_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrae texto de un PDF a Markdown.")
    parser.add_argument("input_pdf", help="Ruta del PDF de origen")
    parser.add_argument("output_md", help="Ruta del Markdown de salida")

    args = parser.parse_args()

    extract_pdf_to_markdown(
        input_pdf=Path(args.input_pdf),
        output_md=Path(args.output_md),
    )


if __name__ == "__main__":
    main()