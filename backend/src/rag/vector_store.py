"""Vector store — interface com ChromaDB para armazenamento e busca vetorial."""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

import chromadb

from src.config import settings

if TYPE_CHECKING:
    from chromadb.api import ClientAPI


@lru_cache(maxsize=1)
def _get_client() -> ClientAPI:
    """Retorna cliente ChromaDB persistente (singleton via lru_cache)."""
    return chromadb.PersistentClient(path=settings.chroma_path)


class VectorStore:
    """Interface para operações no ChromaDB."""

    def __init__(self) -> None:
        self.collection = _get_client().get_or_create_collection(
            name=settings.chroma_collection,
            metadata={"hnsw:space": "cosine"},
        )

    def upsert(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict] | None = None,
    ) -> None:
        """Insere ou atualiza documentos no ChromaDB."""
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(self, embedding: list[float], top_k: int = 5) -> list[dict]:
        """Busca os top-K documentos mais similares ao embedding."""
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=["documents", "distances", "metadatas"],
        )
        items = []
        for i in range(len(results["ids"][0])):
            items.append({
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "distance": (
                    results["distances"][0][i] if results.get("distances") else None
                ),
                "metadata": (
                    results["metadatas"][0][i] if results.get("metadatas") else {}
                ),
            })
        return items

    def count(self) -> int:
        """Retorna quantidade de documentos na collection."""
        return self.collection.count()
