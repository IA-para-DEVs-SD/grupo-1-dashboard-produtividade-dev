from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    github_token: str = ""
    github_username: str = ""

    llm_provider: str = "ollama"
    llm_model: str = "llama3.1"
    openai_api_key: str = ""

    chroma_path: str = "./data/chroma"
    chroma_collection: str = "github_activity"

    sqlite_db_path: str = "./data.db"

    ingestion_days_back: int = 90

    cors_origins: list[str] = ["http://localhost:8501"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
