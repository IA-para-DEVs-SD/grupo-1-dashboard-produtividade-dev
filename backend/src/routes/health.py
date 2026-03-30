"""Rotas de health check — básico e detalhado."""

import httpx
from fastapi import APIRouter

from src.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    """Health check básico — retorna status ok."""
    return {"status": "ok"}


@router.get("/health/detailed")
async def health_detailed():
    """Health check detalhado — verifica API, ChromaDB, GitHub e LLM."""
    checks = {
        "api": "ok",
        "chromadb": await _check_chromadb(),
        "github": await _check_github(),
        "llm": await _check_llm(),
    }
    all_ok = all(v == "ok" for v in checks.values())
    return {"status": "ok" if all_ok else "degraded", "checks": checks}


async def _check_chromadb() -> str:
    """Verifica se o ChromaDB está acessível."""
    try:
        from src.rag.vector_store import VectorStore
        store = VectorStore()
        store.count()
        return "ok"
    except Exception:
        return "error: chromadb unavailable"


async def _check_github() -> str:
    """Verifica conexão com a API do GitHub."""
    if not settings.github_token:
        return "not_configured"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {settings.github_token}"},
                timeout=5,
            )
            if resp.status_code == 200:
                return "ok"
            return f"error: status {resp.status_code}"
    except Exception:
        return "error: github unreachable"


async def _check_llm() -> str:
    """Verifica se o provedor LLM está acessível."""
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            return "not_configured"
        return "ok"
    else:  # ollama
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{settings.ollama_host}/api/tags", timeout=3
                )
                if resp.status_code == 200:
                    return "ok"
                return f"error: status {resp.status_code}"
        except Exception:
            return "error: ollama not running"
