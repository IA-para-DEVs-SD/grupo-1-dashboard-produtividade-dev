"""Serviço de embeddings — gera vetores a partir de texto usando MiniLM."""

from functools import lru_cache

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    """Carrega o modelo de embeddings (singleton via lru_cache)."""
    return SentenceTransformer("all-MiniLM-L6-v2")


class EmbeddingService:
    """Serviço para geração de embeddings de texto."""

    def embed(self, text: str) -> list[float]:
        """Gera embedding para um texto."""
        return _get_model().encode(text).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Gera embeddings para uma lista de textos."""
        return _get_model().encode(texts).tolist()
