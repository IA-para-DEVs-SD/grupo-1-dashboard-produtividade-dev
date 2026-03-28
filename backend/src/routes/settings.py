from fastapi import APIRouter
from pydantic import BaseModel

from src.config import settings

router = APIRouter(tags=["settings"])


class GitHubConfig(BaseModel):
    token: str
    username: str


class LLMConfig(BaseModel):
    provider: str  # ollama or openai
    model: str
    api_key: str = ""


@router.get("/settings/github")
def get_github_config():
    return {
        "username": settings.github_username or "",
        "has_token": bool(settings.github_token),
    }


@router.post("/settings/github")
def save_github_config(config: GitHubConfig):
    import re
    # Validate token format (ghp_, ghs_, gho_, ghu_, github_pat_)
    if config.token and not re.match(r"^(gh[psou]_|github_pat_)[a-zA-Z0-9_]{20,}$", config.token):
        from fastapi import HTTPException
        raise HTTPException(400, "Token inválido. Use formato ghp_xxx, ghs_xxx ou github_pat_xxx")
    
    settings.github_token = config.token
    settings.github_username = config.username
    
    # Persist to .env
    _save_to_env({"GITHUB_TOKEN": config.token, "GITHUB_USERNAME": config.username})
    return {"status": "ok"}


@router.get("/settings/llm")
def get_llm_config():
    return {
        "provider": settings.llm_provider,
        "model": settings.llm_model,
        "has_api_key": bool(settings.openai_api_key),
    }


@router.post("/settings/llm")
def save_llm_config(config: LLMConfig):
    import os
    settings.llm_provider = config.provider
    settings.llm_model = config.model
    
    env_updates = {"LLM_PROVIDER": config.provider, "LLM_MODEL": config.model}
    
    if config.api_key:
        settings.openai_api_key = config.api_key
        os.environ["OPENAI_API_KEY"] = config.api_key
        env_updates["OPENAI_API_KEY"] = config.api_key
    
    _save_to_env(env_updates)
    
    # Reset LLM client singleton to pick up new config
    from src.rag.llm_client import LLMClient
    LLMClient._instance = None
    return {"status": "ok"}


def _save_to_env(updates: dict):
    """Persist settings to .env file."""
    import os
    env_path = os.path.join(os.path.dirname(__file__), "../../.env")
    
    # Read existing
    existing = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    existing[key] = val
    
    # Update
    existing.update(updates)
    
    # Write back
    with open(env_path, "w") as f:
        for key, val in existing.items():
            f.write(f"{key}={val}\n")
