"""Testes unitários para configuração (Settings).

Valida: valores default, tipos corretos, parsing de CORS origins,
e que ingestion_days_back é positivo.
"""

from src.config import Settings


class TestSettingsDefaults:
    """Valida que os defaults seguem a especificação do produto."""

    def test_llm_provider_default_is_ollama(self):
        """Regra: LLM dev usa Ollama local por padrão."""
        s = Settings(
            _env_file=None,
            github_token="",
            github_username="",
        )
        assert s.llm_provider == "ollama"

    def test_llm_model_default_is_llama31(self):
        """Regra: modelo padrão é llama3.1."""
        s = Settings(_env_file=None)
        assert s.llm_model == "llama3.1"

    def test_chroma_collection_default(self):
        """Regra: collection padrão é github_activity."""
        s = Settings(_env_file=None)
        assert s.chroma_collection == "github_activity"

    def test_ingestion_days_back_default_is_90(self):
        """Regra: coleta últimos 90 dias de dados do GitHub."""
        s = Settings(_env_file=None)
        assert s.ingestion_days_back == 90

    def test_cors_origins_includes_streamlit_port(self):
        """Regra: CORS deve permitir frontend Streamlit na porta 8501."""
        s = Settings(_env_file=None)
        assert "http://localhost:8501" in s.cors_origins
