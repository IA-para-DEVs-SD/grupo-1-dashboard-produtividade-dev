"""Rotas de configuração — GitHub e LLM."""

import re

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.config import settings
from src.services.env_writer import save_to_env

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
    """Salva configuração do GitHub (token + username)."""
    if config.token and not re.match(
        r"^(gh[psou]_|github_pat_)[a-zA-Z0-9_]{20,}$", config.token
    ):
        raise HTTPException(
            400, "Token inválido. Use formato ghp_xxx, ghs_xxx ou github_pat_xxx"
        )

    settings.github_token = config.token
    settings.github_username = config.username

    save_to_env({"GITHUB_TOKEN": config.token, "GITHUB_USERNAME": config.username})
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
    """Salva configuração do LLM (provider, model, api_key)."""
    import os

    settings.llm_provider = config.provider
    settings.llm_model = config.model

    env_updates = {"LLM_PROVIDER": config.provider, "LLM_MODEL": config.model}

    if config.api_key:
        settings.openai_api_key = config.api_key
        os.environ["OPENAI_API_KEY"] = config.api_key
        env_updates["OPENAI_API_KEY"] = config.api_key

    save_to_env(env_updates)

    # Reset LLM client singleton to pick up new config
    from src.rag.llm_client import LLMClient

    LLMClient._instance = None
    return {"status": "ok"}

