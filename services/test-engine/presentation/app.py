"""App FastAPI del Test Engine."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import SQLITE_PATH, STATIC_DIR
from infrastructure.db.engine import create_sqlite_engine, init_schema
from presentation.routers import catalog, sessions as sessions_router

# Inicializar esquema y datos semilla al arrancar
_engine = create_sqlite_engine(SQLITE_PATH)
init_schema(_engine)

app = FastAPI(title="Test Engine", docs_url=None, redoc_url=None)

# Archivos estáticos (CSS, JS mínimo)
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Routers
app.include_router(catalog.router)
app.include_router(sessions_router.router)
