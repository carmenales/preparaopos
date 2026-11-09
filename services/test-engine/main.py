"""Punto de entrada del Test Engine.

Uso:
    python main.py
    uvicorn main:app --host 0.0.0.0 --port 8096 --reload
"""

from __future__ import annotations

import uvicorn

from config import HOST, PORT
from presentation.app import app  # noqa: F401 — re-exportado para uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        reload_dirs=["services/test-engine"],
    )

