import logging

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.rag.pipeline import RAGPipeline

logger = logging.getLogger(__name__)
router = APIRouter(tags=["insights"])
limiter = Limiter(key_func=get_remote_address)


class InsightRequest(BaseModel):
    query: str


@router.post("/insights")
@limiter.limit("10/minute")
async def create_insight(request: Request, req: InsightRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query não pode ser vazia")
    try:
        pipeline = RAGPipeline()
        insight = await pipeline.query(req.query)
        return insight.model_dump()
    except RuntimeError as e:
        logger.error(f"LLM RuntimeError: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Insights error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
