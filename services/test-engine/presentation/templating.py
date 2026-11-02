"""Módulo centralizado de plantillas Jinja2 para test-engine con soporte de ROOT_PATH."""

from __future__ import annotations

import os
from fastapi.templating import Jinja2Templates

from config import ROOT_PATH, TEMPLATES_DIR, prefix_url
from presentation.icons import icon

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Registrar helpers globales en el entorno Jinja2
templates.env.globals["url"] = prefix_url
templates.env.globals["prefix_url"] = prefix_url
templates.env.globals["root_path"] = lambda: os.getenv("ROOT_PATH", ROOT_PATH).rstrip("/")


def study_assistant_home() -> str:
    """URL pública de la portada de Study Assistant (servicio distinto, sin ROOT_PATH)."""
    import config

    return f"{config.STUDY_ASSISTANT_PUBLIC_URL.rstrip('/')}/"


templates.env.globals["study_assistant_home"] = study_assistant_home
templates.env.globals["icon"] = icon


def nav_active(request, *prefixes: str) -> bool:
    """¿La página actual pertenece a esta sección del menú? (rutas sin ROOT_PATH)."""
    path = request.url.path if request is not None else ""
    root = os.getenv("ROOT_PATH", ROOT_PATH).rstrip("/")
    if root and path.startswith(root + "/"):
        path = path[len(root):]
    return any(path == p if p == "/" else path.startswith(p) for p in prefixes)


templates.env.globals["nav_active"] = nav_active
