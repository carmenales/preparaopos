"""
services/knowledge/text_utils.py

Utilidad de texto pura (sin dependencias externas, sin I/O), para no
duplicar el slugify de scripts/build_knowledge_index.py dentro de un
servicio que vive en un contenedor distinto y no importa ese módulo.
Módulo plano, sin subcarpeta utils/.
"""

from __future__ import annotations

import re
import unicodedata


def slugify(text: str) -> str:
    """
    Convierte texto libre en un slug ASCII en minúsculas, con guiones
    como separador. Mismo comportamiento esperado que el slugify ya
    usado en el resto del repo: minúsculas, sin acentos, solo [a-z0-9-].
    """
    text = text.strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = text.strip()

    if not text:
        return ""

    return re.sub(r"\s+", "-", text)
