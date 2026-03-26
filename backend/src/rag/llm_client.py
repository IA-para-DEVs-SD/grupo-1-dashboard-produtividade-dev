import aisuite as ai

from src.config import settings


class LLMClient:
    _instance: "LLMClient | None" = None

    def __new__(cls) -> "LLMClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        self.client = ai.Client()
        self.client.configure({"ollama": {"timeout": 120}})
        self.model = f"{settings.llm_provider}:{settings.llm_model}"

    def complete(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(
                f"Erro ao chamar LLM ({self.model}): {e}. "
                "Verifique se Ollama está rodando (ollama serve) "
                "ou configure OPENAI_API_KEY para usar OpenAI."
            )
