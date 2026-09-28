"""Ruta de búsqueda semántica — proxy al servicio de embeddings."""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/api/search")
async def semantic_search(
    q: str = Query("", description="Consulta de búsqueda en lenguaje natural"),
    top_k: int = Query(8, ge=1, le=20, description="Número de resultados"),
):
    """Proxy de búsqueda semántica al microservicio de embeddings.

    Enriquece cada resultado con la URL de navegación al visor de notas.
    """
    if not q.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "El parámetro 'q' es obligatorio."},
        )

    from infrastructure.embeddings.client import EmbeddingsClient
    from config import EMBEDDINGS_SERVICE_URL

    client = EmbeddingsClient(EMBEDDINGS_SERVICE_URL)
    results = await client.search(query=q, top_k=top_k)

    # Enriquecer resultados con URL del visor
    for result in results:
        note_id = result.get("note_id", "")
        anchor = result.get("anchor", "")
        url = f"/notes/{note_id}"
        if anchor:
            url += f"#{anchor}"
        result["url"] = url

    return results

