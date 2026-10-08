"""Punto de entrada de Linking Service."""

from __future__ import annotations

import uvicorn

from config import HOST, PORT
from presentation.app import app  # noqa: F401

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
