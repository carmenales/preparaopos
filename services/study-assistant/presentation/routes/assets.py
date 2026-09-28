"""Ruta de servicio seguro de assets (imágenes embebidas en apuntes)."""

import mimetypes

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from infrastructure.knowledge_fs.repository import KnowledgeFSRepository

router = APIRouter()

# Extensiones permitidas para assets
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "svg"}


@router.get("/assets/notes/{note_id}/{file_path:path}")
async def serve_asset(note_id: str, file_path: str):
    """Sirve imágenes y recursos embebidos en los apuntes Markdown.

    Implementa protección estricta contra Path Traversal:
    la ruta resuelta DEBE estar dentro de KNOWLEDGE_BASE_PATH.
    """
    from config import KNOWLEDGE_INDEX_PATH, KNOWLEDGE_BASE_PATH

    # Validar extensión
    suffix = file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=403,
            detail=f"Extensión no permitida: .{suffix}",
        )

    # Resolver ruta segura
    repo = KnowledgeFSRepository(
        index_path=KNOWLEDGE_INDEX_PATH,
        knowledge_base_path=KNOWLEDGE_BASE_PATH,
    )
    resolved_path = repo.resolve_asset_path(note_id, file_path)

    if resolved_path is None:
        raise HTTPException(status_code=404, detail="Asset no encontrado.")

    # Detectar content-type
    content_type, _ = mimetypes.guess_type(str(resolved_path))
    if content_type is None:
        content_type = "application/octet-stream"

    return FileResponse(
        path=resolved_path,
        media_type=content_type,
        headers={"Cache-Control": "public, max-age=86400"},
    )

