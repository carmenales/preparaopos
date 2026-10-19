"""
Study Assistant — Punto de entrada del servicio.

Servicio de visor de apuntes y búsqueda semántica del ecosistema PreparaOpos.
Migración del PHP Study Assistant a Python/FastAPI con estructura DDD.

Uso local:
    cd services/study-assistant
    pip install -r requirements.txt
    python main.py
"""

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Asegurar que el directorio del servicio está en sys.path
SERVICE_ROOT = Path(__file__).resolve().parent
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

from config import (
    HOST,
    PORT,
    KNOWLEDGE_INDEX_PATH,
    KNOWLEDGE_BASE_PATH,
    TEMPLATES_DIR,
    STATIC_DIR,
)
from domain.notes.service import NoteService
from infrastructure.knowledge_fs.repository import KnowledgeFSRepository

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("study-assistant")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def test_engine_home() -> str:
    """URL pública del catálogo de Test Engine (servicio distinto)."""
    import config

    return f"{config.TEST_ENGINE_PUBLIC_URL.rstrip('/')}/"


templates.env.globals["test_engine_home"] = test_engine_home


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga inicial: índice de notas y servicio de dominio."""
    logger.info("Cargando índice de notas desde %s", KNOWLEDGE_INDEX_PATH)

    repo = KnowledgeFSRepository(
        index_path=KNOWLEDGE_INDEX_PATH,
        knowledge_base_path=KNOWLEDGE_BASE_PATH,
    )
    notes = repo.load_index()
    logger.info("Cargadas %d notas del índice.", len(notes))

    note_service = NoteService(notes)
    metrics = note_service.get_dashboard_metrics()

    app.state.repository = repo
    app.state.note_service = note_service
    app.state.templates = templates
    app.state.notes_loaded = metrics.total_notes
    app.state.processes_count = metrics.total_processes

    logger.info(
        "Dashboard: %d notas, %d procesos, %d revisadas, %d borradores",
        metrics.total_notes,
        metrics.total_processes,
        metrics.reviewed_count,
        metrics.draft_count,
    )
    yield


app = FastAPI(
    title="Study Assistant",
    description="Visor de apuntes y búsqueda semántica — PreparaOpos",
    version="0.1.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# --- Registrar routers ---
from presentation.routes.dashboard import router as dashboard_router
from presentation.routes.notes import router as notes_router
from presentation.routes.search import router as search_router
from presentation.routes.assets import router as assets_router

app.include_router(dashboard_router)
app.include_router(notes_router)
app.include_router(search_router)
app.include_router(assets_router)


@app.get("/health")
async def health():
    """Liveness: el índice ya está en memoria; no recalcula métricas del dashboard."""
    return {
        "status": "ok",
        "service": "study-assistant",
        "notes_loaded": app.state.notes_loaded,
        "processes": app.state.processes_count,
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("Arrancando Study Assistant en %s:%d", HOST, PORT)
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)

