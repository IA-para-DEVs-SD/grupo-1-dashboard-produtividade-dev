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
    """Reseta singletons e caches entre testes."""
    yield
    # Reset LLMClient singleton
    try:
        from src.rag.llm_client import LLMClient
        LLMClient.reset()
    except Exception:
        pass
    # Limpa lru_cache do modelo de embeddings
    try:
        from src.rag.embeddings import _get_model
        _get_model.cache_clear()
    except Exception:
        pass
    # Limpa lru_cache do cliente ChromaDB
    try:
        from src.rag.vector_store import _get_client
        _get_client.cache_clear()
    except Exception:
        pass
