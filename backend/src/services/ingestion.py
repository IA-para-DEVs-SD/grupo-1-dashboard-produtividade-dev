import hashlib
from dataclasses import dataclass, field
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

from src.config import settings
from src.github.collector import GitHubCollector
from src.rag.embeddings import EmbeddingService
from src.rag.vector_store import VectorStore


@dataclass
class IngestionStatus:
    running: bool = False
    step: str = ""
    progress: int = 0
    total: int = 0
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error: str | None = None
    logs: list[str] = field(default_factory=list)


_status = IngestionStatus()


def get_ingestion_status() -> dict:
    return {
        "running": _status.running,
        "step": _status.step,
        "progress": _status.progress,
        "total": _status.total,
        "started_at": _status.started_at.isoformat() if _status.started_at else None,
        "finished_at": _status.finished_at.isoformat() if _status.finished_at else None,
        "error": _status.error,
        "logs": _status.logs[-10:],
    }


def _log(msg: str):
    _status.logs.append(f"{datetime.now().strftime('%H:%M:%S')} {msg}")
    logger.bind(cid="ingestion").info(msg)


async def run_ingestion() -> int:
    global _status
    _status = IngestionStatus(running=True, started_at=datetime.now(), logs=[])
    
    try:
        _status.step = "Verificando configuração"
        _log("Iniciando ingestão...")

        if not settings.github_token:
            _status.error = "GITHUB_TOKEN não configurado"
            _log("❌ " + _status.error)
            return 0

        _status.step = "Coletando commits"
        _log("Buscando commits do GitHub...")
        collector = GitHubCollector(settings.github_token, settings.ingestion_days_back)
        
        commits = await collector.fetch_commits()
        _log(f"✓ {len(commits)} commits coletados")

        _status.step = "Coletando PRs"
        _log("Buscando PRs...")
        prs = await collector.fetch_pull_requests()
        _log(f"✓ {len(prs)} PRs coletados")

        _status.step = "Coletando issues"
        _log("Buscando issues...")
        issues = await collector.fetch_issues()
        _log(f"✓ {len(issues)} issues coletadas")

        chunks_with_meta = (
            [(c.to_chunk(), c.to_metadata()) for c in commits]
            + [(p.to_chunk(), p.to_metadata()) for p in prs]
            + [(i.to_chunk(), i.to_metadata()) for i in issues]
        )
        _status.total = len(chunks_with_meta)
        _log(f"Total: {_status.total} chunks para processar")

        if not chunks_with_meta:
            _status.step = "Concluído"
            _log("Nenhum dado para processar")
            return 0

        _status.step = "Gerando embeddings"
        _log("Gerando embeddings...")
        embedder = EmbeddingService()
        store = VectorStore()

        chunks = [c[0] for c in chunks_with_meta]
        metadatas = [c[1] for c in chunks_with_meta]
        ids = [hashlib.sha256(c.encode()).hexdigest() for c in chunks]
        embeddings = embedder.embed_batch(chunks)
        _status.progress = len(chunks)
        _log(f"✓ {len(embeddings)} embeddings gerados")

        _status.step = "Salvando no ChromaDB"
        _log("Salvando no banco vetorial...")
        store.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        _log(f"✓ {len(chunks)} chunks armazenados no ChromaDB")

        _status.step = "Concluído"
        _log("🎉 Ingestão concluída com sucesso!")
        return len(chunks)

    except Exception as e:
        _status.error = str(e)
        _log(f"❌ Erro: {e}")
        return 0
    finally:
        _status.running = False
        _status.finished_at = datetime.now()


def _sync_ingestion():
    import asyncio
    asyncio.run(run_ingestion())


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(_sync_ingestion, "interval", hours=12, id="github_ingestion")
    scheduler.start()
    return scheduler
