import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger

from src.database import create_db_and_tables

load_dotenv(override=False)

log_level = os.getenv("LOG_LEVEL", "DEBUG")

logger.remove()
logger.add(sys.stderr, level=log_level)

app = FastAPI(title="Dashboard de Produtividade Dev - Backend")

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
    logger.info("Backend application started")

@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("APP_PORT", "8000"))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)
