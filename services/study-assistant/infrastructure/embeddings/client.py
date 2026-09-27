"""Cliente HTTP para el microservicio de embeddings."""

import logging
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)


class EmbeddingsClient:
    """Cliente para interactuar con el microservicio de embeddings."""

    def __init__(self, base_url: str) -> None:
        """Inicializa el cliente con la URL base del microservicio."""
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, top_k: int = 8) -> List[Dict[str, Any]]:
        """Realiza una búsqueda semántica de notas."""
        url = f"{self.base_url}/search"
        params = {"q": query, "top_k": top_k}
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error al buscar embeddings: {e}")
            return []

    async def health(self) -> Optional[Dict[str, Any]]:
        """Comprueba el estado de salud del microservicio."""
        url = f"{self.base_url}/health"
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error al verificar la salud del servicio de embeddings: {e}")
            return None
