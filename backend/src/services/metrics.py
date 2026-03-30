"""Serviço de métricas — cálculo de KPIs e dados semanais."""

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any

from src.config import settings
from src.github.collector import GitHubCollector

# Simple in-memory cache with TTL
_cache: dict[str, tuple[float, Any]] = {}
CACHE_TTL = 60  # seconds


def _get_cached(key: str) -> Any | None:
    """Retorna valor do cache se ainda válido (dentro do TTL)."""
    if key in _cache:
        ts, data = _cache[key]
        if datetime.now().timestamp() - ts < CACHE_TTL:
            return data
        del _cache[key]
    return None


def _set_cached(key: str, data: Any) -> None:
    """Armazena valor no cache com timestamp atual."""
    _cache[key] = (datetime.now().timestamp(), data)


class MetricsService:
    """Serviço para cálculo de KPIs de produtividade a partir de dados GitHub."""

    async def calculate(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> dict:
        """Calcula KPIs agregados (commits, PRs, issues, merge time, hot repos)."""
        cache_key = f"metrics:{from_date}:{to_date}"
        cached = _get_cached(cache_key)
        if cached:
            return cached

        if not settings.github_token:
            return {"error": "GITHUB_TOKEN não configurado"}

        collector = GitHubCollector(settings.github_token, settings.ingestion_days_back)

        try:
            commits = await collector.fetch_commits()
            prs = await collector.fetch_pull_requests()
            issues = await collector.fetch_issues()
        except Exception as e:
            return {"error": f"Falha ao buscar dados do GitHub: {e}"}

        # Filter by date range if provided
        if from_date:
            from_dt = datetime.fromisoformat(from_date).replace(tzinfo=timezone.utc)
            commits = [c for c in commits if c.date >= from_dt]
            prs = [p for p in prs if p.created_at >= from_dt]
            issues = [i for i in issues if i.created_at >= from_dt]
        if to_date:
            to_dt = datetime.fromisoformat(to_date).replace(tzinfo=timezone.utc)
            commits = [c for c in commits if c.date <= to_dt]
            prs = [p for p in prs if p.created_at <= to_dt]
            issues = [i for i in issues if i.created_at <= to_dt]

        total_commits = len(commits)
        total_prs = len(prs)
        total_issues = len(issues)
        prs_merged = [p for p in prs if p.merged_at]
        issues_closed = sum(1 for i in issues if i.closed_at)

        # Tempo médio de merge (em horas)
        merge_times = []
        for p in prs_merged:
            if p.merged_at:
                merged = datetime.fromisoformat(str(p.merged_at).replace("Z", "+00:00"))
                delta = merged - p.created_at
                merge_times.append(delta.total_seconds() / 3600)
        avg_merge_hours = round(sum(merge_times) / len(merge_times), 1) if merge_times else 0

        # Hot repos
        repo_counts = Counter(c.repository for c in commits)
        hot_repos = [{"repo": r, "commits": c} for r, c in repo_counts.most_common(5)]

        weeks = max(settings.ingestion_days_back / 7, 1)
        days = max(settings.ingestion_days_back, 1)

        result = {
            "total_commits": total_commits,
            "total_prs": total_prs,
            "total_issues": total_issues,
            "commits_por_semana": round(total_commits / weeks, 1),
            "commits_por_dia": round(total_commits / days, 1),
            "prs_merged": len(prs_merged),
            "issues_fechadas": issues_closed,
            "tempo_medio_merge_horas": avg_merge_hours,
            "hot_repos": hot_repos,
            "periodo_dias": settings.ingestion_days_back,
        }
        _set_cached(cache_key, result)
        return result

    async def weekly(self, from_date: str | None = None, to_date: str | None = None) -> dict:
        """Return weekly aggregated data for charts."""
        cache_key = f"weekly:{from_date}:{to_date}"
        cached = _get_cached(cache_key)
        if cached:
            return cached

        if not settings.github_token:
            return {"error": "GITHUB_TOKEN não configurado"}

        collector = GitHubCollector(settings.github_token, settings.ingestion_days_back)

        try:
            commits = await collector.fetch_commits()
            prs = await collector.fetch_pull_requests()
        except Exception as e:
            return {"error": f"Falha ao buscar dados do GitHub: {e}"}

        # Last 12 weeks
        now = datetime.now(timezone.utc)
        weeks_data = []

        for i in range(11, -1, -1):
            week_start = now - timedelta(weeks=i + 1)
            week_end = now - timedelta(weeks=i)
            label = week_start.strftime("%d/%m")

            week_commits = sum(1 for c in commits if week_start <= c.date < week_end)
            week_prs_opened = sum(1 for p in prs if week_start <= p.created_at < week_end)
            week_prs_closed = sum(
                1 for p in prs
                if p.merged_at and week_start <= datetime.fromisoformat(
                    str(p.merged_at).replace("Z", "+00:00")
                ) < week_end
            )

            weeks_data.append({
                "label": label,
                "commits": week_commits,
                "prs_opened": week_prs_opened,
                "prs_closed": week_prs_closed,
            })

        result = {
            "weeks": [w["label"] for w in weeks_data],
            "commits": [w["commits"] for w in weeks_data],
            "prs_opened": [w["prs_opened"] for w in weeks_data],
            "prs_closed": [w["prs_closed"] for w in weeks_data],
        }
        _set_cached(cache_key, result)
        return result
