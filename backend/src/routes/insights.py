"""Rota de insights — chat RAG com perguntas sobre produtividade."""

from fastapi import APIRouter, HTTPException, Request
from loguru import logger
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.rag.pipeline import RAGPipeline

router = APIRouter(tags=["insights"])
limiter = Limiter(key_func=get_remote_address)


class InsightRequest(BaseModel):
    """Payload para consulta ao pipeline RAG."""

    query: str


@router.post("/insights")
@limiter.limit("10/minute")
async def create_insight(request: Request, req: InsightRequest):
    """Processa uma pergunta via pipeline RAG e retorna insight estruturado."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query não pode ser vazia")
    try:
        pipeline = RAGPipeline()
        insight = await pipeline.query(req.query)
        return insight.model_dump()
    except RuntimeError as e:
        logger.bind(cid="insights").error(f"Erro LLM: {e}")
        raise HTTPException(
            status_code=503,
            detail="Serviço LLM indisponível. Verifique se o Ollama está rodando.",
        )
    except Exception as e:
        logger.bind(cid="insights").error(f"Erro no pipeline: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao processar insight. Tente novamente.",
        )
