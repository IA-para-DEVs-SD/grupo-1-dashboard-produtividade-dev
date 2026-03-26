from __future__ import annotations

from typing import TYPE_CHECKING

import chromadb

from src.config import settings

if TYPE_CHECKING:
    from chromadb.api import ClientAPI

_client: ClientAPI | None = None


def _get_client() -> ClientAPI:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.chroma_path)
    return _client


class VectorStore:
    _instance: VectorStore | None = None

    def __new__(cls) -> VectorStore:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_collection()
        return cls._instance

    def _init_collection(self):
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
    ):
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(self, embedding: list[float], top_k: int = 5) -> list[dict]:
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
                "distance": results["distances"][0][i] if results.get("distances") else None,
                "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
            })
        return items

    def count(self) -> int:
        return self.collection.count()
