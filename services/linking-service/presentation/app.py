"""Aplicación FastAPI para Linking Service."""

from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

from config import APUNTES_SERVICE_URL, SQLITE_PATH, TEST_ENGINE_URL
from domain.service import LinkingService
from infrastructure.clients.apuntes_client import ApuntesClient
from infrastructure.clients.test_engine_client import TestEngineClient
from infrastructure.db.engine import get_connection, init_db
from infrastructure.db.repository import QuestionNoteLinkRepository
from presentation.routes.links import router as links_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar esquema
    init_db(SQLITE_PATH)

    conn = get_connection(SQLITE_PATH)
    repo = QuestionNoteLinkRepository(conn)
    apuntes_client = ApuntesClient(APUNTES_SERVICE_URL)
    test_engine_client = TestEngineClient(TEST_ENGINE_URL)

    service = LinkingService(
        repo=repo,
        apuntes_client=apuntes_client,
        test_engine_client=test_engine_client,
    )

    app.state.db_conn = conn
    app.state.repo = repo
    app.state.linking_service = service
    yield
    conn.close()


app = FastAPI(
    title="Linking Service",
    description="Servicio de enlaces entre preguntas de test y notas de temario",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(links_router)


@app.get("/health")
async def health(request: Request):
    count = request.app.state.repo.count() if hasattr(request.app.state, "repo") else 0
    return {
        "status": "ok",
        "service": "linking-service",
        "links_count": count,
    }

