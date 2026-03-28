import httpx
from fastapi import APIRouter

from src.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    """Basic health check."""
    return {"status": "ok"}


@router.get("/health/detailed")
async def health_detailed():
    """Detailed health check for all services."""
    checks = {
        "api": "ok",
        "chromadb": await _check_chromadb(),
        "github": await _check_github(),
        "llm": await _check_llm(),
    }
    all_ok = all(v == "ok" for v in checks.values())
    return {"status": "ok" if all_ok else "degraded", "checks": checks}


async def _check_chromadb() -> str:
    try:
        from src.rag.vector_store import VectorStore
        store = VectorStore()
        store.count()
        return "ok"
    except Exception as e:
        return f"error: {e}"


async def _check_github() -> str:
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
            return f"error: {resp.status_code}"
    except Exception as e:
        return f"error: {e}"


async def _check_llm() -> str:
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            return "not_configured"
        return "ok"  # Can't easily test without making a call
    else:  # ollama
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get("http://localhost:11434/api/tags", timeout=3)
                if resp.status_code == 200:
                    return "ok"
                return f"error: {resp.status_code}"
        except Exception:
            return "error: ollama not running"
