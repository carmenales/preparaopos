"""
services/knowledge/topic_retriever.py

Recupera fragmentos relevantes para un tema dado. Sin ranking ni
deduplicación todavía (fuera de alcance de este milestone): llama a
SearchClient, filtra por min_score y respeta el top_k pedido. El orden
que devuelve /search (por score descendente) se conserva tal cual.
"""

from __future__ import annotations

from config import settings
from schemas import RetrievedFragment
from search_client import SearchClient


class TopicRetriever:
    def __init__(self, search_client: SearchClient) -> None:
        self._search_client = search_client

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        min_score: float | None = None,
    ) -> list[RetrievedFragment]:
        effective_top_k = top_k or settings.default_top_k
        effective_min_score = min_score if min_score is not None else settings.default_min_score

        fragments = self._search_client.search(query=query, top_k=effective_top_k)

        return [fragment for fragment in fragments if fragment.score >= effective_min_score]
