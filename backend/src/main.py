from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.config import settings
from src.logging_config import get_correlation_id, logger
from src.routes import export, github, health, insights, metrics
from src.routes import settings as settings_routes
from src.services.ingestion import start_scheduler

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    logger.bind(cid="startup").info("Scheduler de ingestão iniciado")
    yield
    scheduler.shutdown(wait=False)
    logger.bind(cid="shutdown").info("Scheduler encerrado")


app = FastAPI(
    title="Dashboard Produtividade Dev",
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    cid = get_correlation_id()
    with logger.contextualize(cid=cid):
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = cid
        return response


app.include_router(health.router)
app.include_router(github.router)
app.include_router(insights.router)
app.include_router(metrics.router)
app.include_router(export.router)
app.include_router(settings_routes.router)
