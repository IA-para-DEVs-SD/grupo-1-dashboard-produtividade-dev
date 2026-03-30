"""Conftest global — mocka dependências pesadas antes de qualquer import.

sentence-transformers e chromadb são pesados e podem não estar instalados
no ambiente de CI/dev. Mockamos no nível de sys.modules para que todos os
testes possam importar os módulos do src sem erro.
"""

import sys
from unittest.mock import MagicMock

# Mock sentence_transformers antes de qualquer import
_mock_st = MagicMock()
_mock_st.SentenceTransformer.return_value.encode.return_value = MagicMock(
    tolist=lambda: [0.1] * 384
)
sys.modules.setdefault("sentence_transformers", _mock_st)

# Mock openai se não estiver instalado
if "openai" not in sys.modules:
    sys.modules["openai"] = MagicMock()

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_singletons():
    """Reseta singletons de EmbeddingService, VectorStore e LLMClient."""
    yield
    # Reset após cada teste
    try:
        from src.rag.embeddings import EmbeddingService
        EmbeddingService._instance = None
    except Exception:
        pass
    try:
        from src.rag.vector_store import VectorStore
        VectorStore._instance = None
    except Exception:
        pass
    try:
        from src.rag.llm_client import LLMClient
        LLMClient._instance = None
    except Exception:
        pass
