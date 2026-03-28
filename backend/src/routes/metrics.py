from fastapi import APIRouter, BackgroundTasks, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.services.ingestion import get_ingestion_status, run_ingestion
from src.services.metrics import MetricsService

router = APIRouter(tags=["metrics"])
limiter = Limiter(key_func=get_remote_address)


@router.get("/metrics")
@limiter.limit("30/minute")
async def get_metrics(
    request: Request,
    from_date: str | None = Query(None, alias="from"),
    to_date: str | None = Query(None, alias="to"),
):
    svc = MetricsService()
    return await svc.calculate(from_date, to_date)


@router.get("/metrics/weekly")
@limiter.limit("30/minute")
async def get_metrics_weekly(
    request: Request,
    from_date: str | None = Query(None, alias="from"),
    to_date: str | None = Query(None, alias="to"),
):
    svc = MetricsService()
    return await svc.weekly(from_date, to_date)


@router.post("/ingest")
@limiter.limit("5/hour")
async def trigger_ingest(request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(_run_ingest_task)
    return {"status": "started", "message": "Ingestão iniciada em background"}


@router.get("/ingest/status")
def ingest_status():
    return get_ingestion_status()


async def _run_ingest_task():
    await run_ingestion()
