import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger

load_dotenv(override=False)

log_level = os.getenv("LOG_LEVEL", "DEBUG")

logger.remove()
logger.add(sys.stderr, level=log_level)

app = FastAPI(title="Dashboard de Produtividade Dev - Backend")


@app.on_event("startup")
async def startup_event():
    logger.info("Backend application started")


@app.get("/health")
async def health():
    return {"status": "healthy"}
