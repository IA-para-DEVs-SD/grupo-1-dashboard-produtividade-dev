from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


class EmbeddingService:
    _instance: "EmbeddingService | None" = None

    def __new__(cls) -> "EmbeddingService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def embed(self, text: str) -> list[float]:
        return _get_model().encode(text).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return _get_model().encode(texts).tolist()
