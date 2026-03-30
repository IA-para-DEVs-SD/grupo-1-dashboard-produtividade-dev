"""Cliente LLM com suporte a Ollama (via OpenAI-compatible API) e OpenAI."""

from openai import OpenAI

from src.config import settings


class LLMClient:
    """Cliente singleton para chamadas LLM."""

    _instance: "LLMClient | None" = None

    def __new__(cls) -> "LLMClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        if settings.llm_provider == "ollama":
            self.client = OpenAI(
                base_url=f"{settings.ollama_host}/v1",
                api_key="ollama",
            )
            self.model = settings.llm_model
        else:
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.llm_model

    def complete(self, prompt: str) -> str:
        """Envia prompt ao LLM e retorna a resposta."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(
                f"Erro ao chamar LLM ({settings.llm_provider}:{self.model}): {e}. "
                f"OLLAMA_HOST={settings.ollama_host}. "
                "Verifique se Ollama está rodando ou configure "
                "OPENAI_API_KEY para usar OpenAI."
            )
