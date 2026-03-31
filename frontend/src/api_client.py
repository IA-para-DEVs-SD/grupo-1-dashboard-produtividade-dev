"""Cliente HTTP para comunicação com o backend FastAPI."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")
PUBLIC_URL = os.getenv("BACKEND_PUBLIC_URL", BASE_URL)


def _get(path: str, params: dict | None = None):
    """GET request ao backend."""
    resp = requests.get(f"{BASE_URL}{path}", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _post(path: str, json_data: dict | None = None):
    """POST request ao backend."""
    resp = requests.post(f"{BASE_URL}{path}", json=json_data, timeout=60)
    resp.raise_for_status()
    return resp.json()


# --- GitHub ---

def get_github_status():
    """Retorna status da conexão GitHub."""
    return _get("/github/status")


def get_github_config():
    """Retorna configuração GitHub salva."""
    return _get("/settings/github")


def save_github_config(token: str, username: str):
    """Salva token e username do GitHub."""
    return _post("/settings/github", {"token": token, "username": username})


# --- LLM ---

def get_llm_config():
    """Retorna configuração LLM atual."""
    return _get("/settings/llm")


def save_llm_config(provider: str, model: str, api_key: str = ""):
    """Salva configuração LLM."""
    return _post(
        "/settings/llm",
        {
            "provider": provider,
            "model": model,
            "api_key": api_key,
        },
    )


# --- Métricas ---

def get_metrics(date_from: str | None = None, date_to: str | None = None):
    """Retorna KPIs agregados."""
    params = {}
    if date_from:
        params["from"] = date_from
    if date_to:
        params["to"] = date_to
    return _get("/metrics", params or None)


def get_metrics_weekly(date_from: str | None = None, date_to: str | None = None):
    """Retorna métricas semanais para gráficos."""
    params = {}
    if date_from:
        params["from"] = date_from
    if date_to:
        params["to"] = date_to
    return _get("/metrics/weekly", params or None)


# --- RAG / Insights ---

def post_insight(query: str):
    """Envia pergunta ao pipeline RAG."""
    return _post("/insights", {"query": query})


# --- Ingestão ---

def trigger_ingest():
    """Dispara ingestão manual."""
    return _post("/ingest")


def get_ingest_status():
    """Retorna status da ingestão."""
    return _get("/ingest/status")


# --- Export ---

def get_export_url(
    fmt: str,
    date_from: str | None = None,
    date_to: str | None = None,
) -> str:
    """Retorna URL de export (CSV ou PDF)."""
    params = []
    if date_from:
        params.append(f"from={date_from}")
    if date_to:
        params.append(f"to={date_to}")
    qs = f"?{'&'.join(params)}" if params else ""
    return f"{PUBLIC_URL}/export/{fmt}{qs}"
