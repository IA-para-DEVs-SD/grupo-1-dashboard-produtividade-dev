"""Rotas de métricas e ingestão."""

import re

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.services.ingestion import get_ingestion_status, run_ingestion
from src.services.metrics import MetricsService

router = APIRouter(tags=["metrics"])
limiter = Limiter(key_func=get_remote_address)

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _validate_date(value: str | None, param_name: str) -> None:
    """Valida formato de data ISO (YYYY-MM-DD)."""
    if value is not None and not DATE_PATTERN.match(value):
        raise HTTPException(
            status_code=400,
            detail=f"Parâmetro '{param_name}' deve estar no formato YYYY-MM-DD.",
        )


@router.get("/metrics")
@limiter.limit("30/minute")
async def get_metrics(
    request: Request,
    from_date: str | None = Query(None, alias="from"),
    to_date: str | None = Query(None, alias="to"),
):
    """Retorna KPIs agregados de produtividade."""
    _validate_date(from_date, "from")
    _validate_date(to_date, "to")
    svc = MetricsService()
    return await svc.calculate(from_date, to_date)


@router.get("/metrics/weekly")
@limiter.limit("30/minute")
async def get_metrics_weekly(
    request: Request,
    from_date: str | None = Query(None, alias="from"),
    to_date: str | None = Query(None, alias="to"),
):
    """Retorna métricas semanais para gráficos."""
    _validate_date(from_date, "from")
    _validate_date(to_date, "to")
    svc = MetricsService()
    return await svc.weekly(from_date, to_date)


@router.post("/ingest")
@limiter.limit("5/hour")
async def trigger_ingest(request: Request, background_tasks: BackgroundTasks):
    """Dispara ingestão de dados do GitHub em background."""
    background_tasks.add_task(_run_ingest_task)
    return {"status": "started", "message": "Ingestão iniciada em background"}


@router.get("/ingest/status")
def ingest_status():
    """Retorna status atual da ingestão."""
    return get_ingestion_status()


async def _run_ingest_task():
    await run_ingestion()
