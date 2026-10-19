"""
services/knowledge/markdown_normalizer.py

Normalización determinista y genérica de texto Markdown extraído de documentos (PDF/PPTX).
Diseñado bajo principios de código limpio:
- Cero hardcodeo de nombres de academias, empresas o procesos selectivos.
- Reglas genéricas basadas en patrones sintácticos (fechas, paginación, avisos legales, URLs).
- Preservación estricta de la estructura de párrafos y de la prosa legítima.
"""

from __future__ import annotations

import re
from collections import Counter


class MarkdownNormalizer:
    """Normaliza texto Markdown eliminando ruido de extracción sin alterar el contenido real."""

    # Marcadores de paginación universales
    PAGE_MARKER_RE = re.compile(
        r"^\s*#{0,6}\s*(?:p[áa]g(?:ina)?\.?|diapositiva)\s*\d+\s*(?:(?:\||/|de|-)\s*\d+)?\s*$",
        re.IGNORECASE,
    )
    LONE_PAGE_NUMBER_RE = re.compile(
        r"^\s*#{0,6}\s*\d+\s*(?:(?:\||/|de)\s*\d+)\s*$",
        re.IGNORECASE,
    )

    # Avisos legales y metadatos de distribución genéricos (universales, sin nombres comerciales)
    LEGAL_BOILERPLATE_RE = re.compile(
        r"^\s*(?:todos\s+los\s+derechos\s+reservados"
        r"|prohibida\s+(?:su\s+)?reproducci[óo]n[^\n]*"
        r"|dep[óo]sito\s+legal[^\n]*"
        r"|copyright\s+[^\n]*"
        r"|©[^\n]*"
        r"|https?://\S+"
        r"|www\.[a-z0-9\-\.]+\.[a-z]{2,})\s*$",
        re.IGNORECASE,
    )

    # Viñetas y listas
    BULLET_PREFIX_RE = re.compile(r"^[-*+•·●○▪▫⁃–—\uf0b7\uf0a7\uf0d8]\s+")

    # Abreviaturas comunes en español que terminan en punto y no son fin de frase
    ABBREVIATIONS_RE = re.compile(r"\b(art|arts|p[áa]g|p[áa]gs|n[úu]m|n[úu]ms|vol|ej|apdo|disp|letra|etc)\.\s*$", re.IGNORECASE)

    # Conectores, preposiciones y artículos colgantes que indican continuación de frase
    DANGLING_CONNECTIVE_RE = re.compile(
        r"\b(de|del|en|con|por|para|sobre|tras|y|o|u|e|que|a|al|el|la|los|las|un|una|unos|unas|su|sus|este|esta|estos|estas|como|seg[úu]n|sin|ni|si)\s*$",
        re.IGNORECASE,
    )

    # Siglas / acrónimos
    SIGLAS_INTRO_RE = re.compile(
        r"^\s*las\s+siglas\s+empleadas\s+en\s+este\s+documento\s+son\s+las\s+siguientes\s*:?\s*$",
        re.IGNORECASE,
    )
    SIGLA_RE = re.compile(r"^[A-ZÁÉÍÓÚÜÑ0-9]{2,15}[a-z]?$")

    @classmethod
    def clean_inline_noise(cls, text: str) -> str:
        """
        Limpia ruido sintáctico incrustado (fechas de actualización, paginación, URLs).
        No altera oraciones normales ni términos técnicos.
        """
        text = text.replace("\u200b", "").replace("\u00a0", " ")

        # 1. Fechas universales de actualización y edición (antes de evaluar fracciones numéricas)
        text = re.sub(r"\bactualizado\s+(?:a|en|el|de)?\s*:?\s*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b", "", text, flags=re.I)
        text = re.sub(r"\bactualizado\s+(?:a|en|el|de)?\s*:?\s*[a-záéíóú]+\s+de\s+\d{4}\b", "", text, flags=re.I)
        text = re.sub(r"\bactualizado\s*:?\s*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b", "", text, flags=re.I)
        text = re.sub(r"\bfecha\s*:?\s*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}\b", "", text, flags=re.I)
        text = re.sub(r"\bconvocatoria\s+\d{4}\b", "", text, flags=re.I)
        text = re.sub(r"\bedici[óo]n\s+\d{4}\b", "", text, flags=re.I)

        # 2. URLs y enlaces web genéricos
        text = re.sub(r"https?://\S+", "", text)
        text = re.sub(r"\bwww\.[a-z0-9\-\.]+\.[a-z]{2,}\b", "", text, flags=re.I)

        # 3. Marcadores de paginación explícitos ('Página 1 | 12', 'Pág. 3 / 10', 'Página1 | 12', 'Página1')
        text = re.sub(r"\bp[áa]g(?:ina)?\.?\s*\d+\s*(?:\||/|de)\s*\d+\b", "", text, flags=re.I)
        text = re.sub(r"\bp[áa]g\.\s*\d+\b", "", text, flags=re.I)
        text = re.sub(r"\bp[áa]gina\d+\b", "", text, flags=re.I)

        # Marcador de página al inicio de línea o heading (ej. '^Página1 | 12 ## ...')
        text = re.sub(r"^\s*p[áa]g(?:ina)?\.?\s*\d+\s*(?:(?:\||/|de|-)\s*\d+)?\s*", "", text, flags=re.I)

        # 4. Fracciones de página sueltas con barras o pipes ('1 | 12')
        text = re.sub(r"\b\d{1,3}\s*\|\s*\d{1,3}\b", "", text)

        # 5. Símbolos residuales de bordes
        text = re.sub(r"\s*\|\s*\d+\s*$", "", text)
        text = re.sub(r"\|\s*\d+\b", "", text)
        text = re.sub(r"\s*\|\s*$", "", text)
        text = re.sub(r"^\s*\|\s*", "", text)
        text = re.sub(r"\s*-\s*$", "", text)
        if re.match(r"^[\s\-\|]+$", text):
            return ""

        # 6. Normalizar headings con ruido al inicio (ej. 'Página1 | 12 ## Título' -> '## Título')
        if not text.strip().startswith("#") and re.search(r"\s(#{1,6}\s+)", text):
            m = re.search(r"(#{1,6}\s+.*)", text)
            if m:
                text = m.group(1).strip()

        # Si solo quedan almohadillas (como '###' derivado de '### Página2 | 12')
        if re.match(r"^#{1,6}\s*$", text.strip()):
            return ""

        text = re.sub(r"[ \t]+", " ", text).strip()
        return text

    @classmethod
    def is_pure_page_or_header_noise(cls, text: str) -> bool:
        """Detecta si una línea es únicamente un marcador de página o metadato descartable."""
        s = text.strip()
        if not s:
            return True
        if cls.PAGE_MARKER_RE.match(s) or cls.LONE_PAGE_NUMBER_RE.match(s):
            return True
        if re.match(r"^\s*#{0,6}\s*\d+\s*$", s):
            return True
        if cls.LEGAL_BOILERPLATE_RE.match(s):
            return True
        if re.match(r"^\s*actualizado\s+[^\n]+$", s, re.I):
            return True
        return False

    @classmethod
    def remove_obvious_extraction_noise(cls, text: str) -> str:
        """Elimina líneas completas que contengan únicamente ruido de paginación o metadatos."""
        lines = text.splitlines()
        cleaned: list[str] = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                cleaned.append("")
                continue

            if cls.PAGE_MARKER_RE.match(stripped) or cls.LONE_PAGE_NUMBER_RE.match(stripped):
                continue

            if cls.LEGAL_BOILERPLATE_RE.match(stripped):
                continue

            if stripped.lower() in {"mostrar menos", "mostrar más"}:
                continue

            if cls.is_pure_page_or_header_noise(stripped):
                continue

            cleaned_line = cls.clean_inline_noise(line)
            if not cleaned_line.strip() or cls.is_pure_page_or_header_noise(cleaned_line):
                continue

            cleaned.append(cleaned_line)

        return "\n".join(cleaned)

    @classmethod
    def convert_acronym_blocks_to_table(cls, text: str) -> str:
        """Detecta bloques estándar de siglas/definiciones y los formatea como tabla Markdown."""
        lines = text.splitlines()
        out: list[str] = []
        i = 0

        while i < len(lines):
            line = lines[i].rstrip()
            stripped = line.strip()

            if cls.SIGLAS_INTRO_RE.match(stripped):
                out.append("## Siglas")
                out.append("")
                i += 1

                entries: list[tuple[str, str]] = []
                while i < len(lines):
                    current = lines[i].strip()
                    if not current:
                        i += 1
                        continue
                    if current.startswith("#") or current.startswith("|"):
                        break
                    if not (current and len(current) <= 20 and " " not in current and cls.SIGLA_RE.match(current)):
                        break

                    sigla = current
                    i += 1
                    if i >= len(lines):
                        entries.append((sigla, ""))
                        break

                    definition = lines[i].strip()
                    if (
                        definition
                        and not (len(definition) <= 20 and " " not in definition and cls.SIGLA_RE.match(definition))
                        and not definition.startswith("#")
                    ):
                        entries.append((sigla, definition))
                        i += 1
                    else:
                        entries.append((sigla, ""))

                if entries:
                    out.append("| Sigla | Significado |")
                    out.append("| --- | --- |")
                    for sigla, definition in entries:
                        out.append(f"| {sigla} | {definition} |")
                    out.append("")
                continue

            out.append(line)
            i += 1

        return "\n".join(out)

    @classmethod
    def dedupe_repeated_lines(cls, text: str) -> str:
        """Elimina líneas consecutivas exactamente duplicadas."""
        lines = text.splitlines()
        out: list[str] = []
        prev_line: str | None = None

        for line in lines:
            stripped = line.strip()
            if stripped and stripped == prev_line:
                continue
            out.append(line)
            prev_line = stripped if stripped else None

        return "\n".join(out)

    @classmethod
    def join_broken_paragraphs(cls, text: str) -> str:
        """Une párrafos o viñetas rotas a mitad de frase por saltos de línea arbitrarios."""
        lines = text.splitlines()
        out: list[str] = []
        i = 0

        while i < len(lines):
            current = lines[i].rstrip()

            if not current.strip():
                out.append("")
                i += 1
                continue

            while i + 1 < len(lines):
                nxt = lines[i + 1].strip()
                if not nxt:
                    break

                # No unir si nxt es un heading, tabla, o bloque destacado
                if nxt.startswith(("#", "|", ">", "**")):
                    break

                # Si nxt es una nueva viñeta, no unir
                if cls.BULLET_PREFIX_RE.match(nxt) or re.match(r"^\d+\.\s+", nxt):
                    break

                # Si la línea actual termina en puntuación de cierre de frase
                if current.endswith((".", ":", ";", "!", "?", "|")):
                    if not (nxt and nxt[0].islower()):
                        has_unclosed_paren = current.count("(") > current.count(")")
                        is_abbreviation = bool(cls.ABBREVIATIONS_RE.search(current))
                        closes_paren = has_unclosed_paren and (nxt.startswith(")") or bool(re.match(r"^\d+\)", nxt)))
                        is_dangling = bool(cls.DANGLING_CONNECTIVE_RE.search(current))
                        if not (has_unclosed_paren or is_abbreviation or closes_paren or is_dangling):
                            break

                # Si la línea actual termina en guion de palabra partida
                if current.endswith("-"):
                    current = current[:-1] + nxt
                else:
                    current += " " + nxt

                i += 1

            out.append(current)
            i += 1

        return "\n".join(out)

    @classmethod
    def normalize_whitespace(cls, text: str) -> str:
        """Normaliza espacios y saltos de línea conservando párrafos."""
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[\t\f\v]+", " ", text)
        text = re.sub(r"[ ]{2,}", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"

    @classmethod
    def normalize(cls, content: str) -> str:
        """Aplica el flujo de normalización completo de forma determinista."""
        if not content or not content.strip():
            return ""

        text = cls.remove_obvious_extraction_noise(content)
        text = cls.convert_acronym_blocks_to_table(text)
        text = cls.dedupe_repeated_lines(text)
        text = cls.join_broken_paragraphs(text)
        text = cls.normalize_whitespace(text)
        return text.strip()


# Funciones de conveniencia para compatibilidad con código existente
def clean_inline_noise(text: str) -> str:
    return MarkdownNormalizer.clean_inline_noise(text)


def is_pure_page_or_header_noise(text: str) -> bool:
    return MarkdownNormalizer.is_pure_page_or_header_noise(text)


def normalize_markdown(content: str) -> str:
    return MarkdownNormalizer.normalize(content)
