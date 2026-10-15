"""Módulo centralizado de plantillas Jinja2 para test-engine con soporte de ROOT_PATH."""

from __future__ import annotations

import os
from fastapi.templating import Jinja2Templates

from config import ROOT_PATH, TEMPLATES_DIR, prefix_url

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Registrar helpers globales en el entorno Jinja2
templates.env.globals["url"] = prefix_url
templates.env.globals["prefix_url"] = prefix_url
templates.env.globals["root_path"] = lambda: os.getenv("ROOT_PATH", ROOT_PATH).rstrip("/")
