from fastapi import APIRouter, HTTPException

from src.config import settings
from src.github.collector import GitHubCollector

router = APIRouter(prefix="/github", tags=["github"])


@router.get("/status")
async def github_status():
    if not settings.github_token:
        raise HTTPException(status_code=400, detail="GITHUB_TOKEN não configurado")
    collector = GitHubCollector(settings.github_token, settings.ingestion_days_back)
    result = await collector.check_connection()
    return result
