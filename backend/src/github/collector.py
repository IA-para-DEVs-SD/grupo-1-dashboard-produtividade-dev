"""Coletor de dados do GitHub via GraphQL API."""

from datetime import datetime, timedelta, timezone

import httpx
from loguru import logger

from src.github.models import Commit, Issue, PullRequest

GRAPHQL_URL = "https://api.github.com/graphql"


class GitHubCollector:
    """Coleta commits, PRs e issues do GitHub via GraphQL API."""

    def __init__(self, token: str, days_back: int = 90):
        self.token = token
        self.days_back = days_back
        self.headers = {
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
        }

    async def _query(self, query: str, variables: dict | None = None) -> dict:
        """Executa query GraphQL na API do GitHub."""
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                GRAPHQL_URL,
                json={"query": query, "variables": variables or {}},
                headers=self.headers,
            )
            resp.raise_for_status()
            data = resp.json()
            if "errors" in data:
                logger.bind(cid="github").error(f"GraphQL errors: {data['errors']}")
            return data.get("data", {})

    async def check_connection(self) -> dict:
        """Verifica conexão com o GitHub e retorna login do usuário."""
        try:
            data = await self._query("query { viewer { login } }")
            login = data.get("viewer", {}).get("login", "")
            return {"connected": True, "username": login}
        except Exception as e:
            return {"connected": False, "error": str(e)}

    async def fetch_commits(self) -> list[Commit]:
        """Busca commits dos últimos N dias via GraphQL com paginação."""
        since = datetime.now(timezone.utc) - timedelta(days=self.days_back)
        query = """
        query($since: GitTimestamp!, $repoCursor: String, $commitCursor: String) {
          viewer {
            repositories(first: 20, after: $repoCursor,
                         orderBy: {field: PUSHED_AT, direction: DESC}) {
              pageInfo { hasNextPage endCursor }
              nodes {
                nameWithOwner
                defaultBranchRef {
                  target {
                    ... on Commit {
                      history(first: 100, after: $commitCursor, since: $since) {
                        pageInfo { hasNextPage endCursor }
                        nodes {
                          oid message
                          author { name }
                          committedDate additions deletions
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """
        commits = []
        repo_cursor = None

        for _ in range(5):  # max 5 pages of repos = 100 repos
            data = await self._query(query, {"since": since.isoformat(), "repoCursor": repo_cursor})
            repos = data.get("viewer", {}).get("repositories", {})

            for repo in repos.get("nodes", []):
                repo_name = repo.get("nameWithOwner", "")
                ref = repo.get("defaultBranchRef")
                if not ref:
                    continue

                history = ref.get("target", {}).get("history", {})
                for node in history.get("nodes", []):
                    commits.append(Commit(
                        sha=node["oid"],
                        message=node["message"],
                        author=node.get("author", {}).get("name", "") or "",
                        date=node["committedDate"],
                        additions=node.get("additions", 0),
                        deletions=node.get("deletions", 0),
                        repository=repo_name,
                    ))

            page_info = repos.get("pageInfo", {})
            if not page_info.get("hasNextPage"):
                break
            repo_cursor = page_info.get("endCursor")

        return commits

    async def fetch_pull_requests(self) -> list[PullRequest]:
        """Busca PRs dos últimos N dias via GraphQL com paginação."""
        since = datetime.now(timezone.utc) - timedelta(days=self.days_back)
        query = """
        query($cursor: String) {
          viewer {
            pullRequests(first: 100, after: $cursor,
                         orderBy: {field: CREATED_AT, direction: DESC}) {
              pageInfo { hasNextPage endCursor }
              nodes {
                title state number createdAt mergedAt
                repository { nameWithOwner }
              }
            }
          }
        }
        """
        prs = []
        cursor = None

        for _ in range(5):  # max 500 PRs
            data = await self._query(query, {"cursor": cursor})
            pr_data = data.get("viewer", {}).get("pullRequests", {})

            for node in pr_data.get("nodes", []):
                created = datetime.fromisoformat(node["createdAt"].replace("Z", "+00:00"))
                if created < since:
                    return prs  # PRs are ordered by date, stop when too old
                prs.append(PullRequest(
                    title=node["title"],
                    state=node["state"],
                    number=node.get("number", 0),
                    created_at=created,
                    merged_at=node.get("mergedAt"),
                    repository=node.get("repository", {}).get("nameWithOwner", ""),
                ))

            page_info = pr_data.get("pageInfo", {})
            if not page_info.get("hasNextPage"):
                break
            cursor = page_info.get("endCursor")

        return prs

    async def fetch_issues(self) -> list[Issue]:
        """Busca issues dos últimos N dias via GraphQL com paginação."""
        since = datetime.now(timezone.utc) - timedelta(days=self.days_back)
        query = """
        query($cursor: String) {
          viewer {
            issues(first: 100, after: $cursor, orderBy: {field: CREATED_AT, direction: DESC}) {
              pageInfo { hasNextPage endCursor }
              nodes {
                title state number createdAt closedAt
                labels(first: 10) { nodes { name } }
                repository { nameWithOwner }
              }
            }
          }
        }
        """
        issues = []
        cursor = None

        for _ in range(5):  # max 500 issues
            data = await self._query(query, {"cursor": cursor})
            issue_data = data.get("viewer", {}).get("issues", {})

            for node in issue_data.get("nodes", []):
                created = datetime.fromisoformat(node["createdAt"].replace("Z", "+00:00"))
                if created < since:
                    return issues
                issues.append(Issue(
                    title=node["title"],
                    state=node["state"],
                    number=node.get("number", 0),
                    created_at=created,
                    closed_at=node.get("closedAt"),
                    labels=[lb["name"] for lb in node.get("labels", {}).get("nodes", [])],
                    repository=node.get("repository", {}).get("nameWithOwner", ""),
                ))

            page_info = issue_data.get("pageInfo", {})
            if not page_info.get("hasNextPage"):
                break
            cursor = page_info.get("endCursor")

        return issues

    async def fetch_all_chunks(self) -> list[tuple[str, dict]]:
        """Returns list of (chunk_text, metadata) tuples."""
        chunks = []
        try:
            commits = await self.fetch_commits()
            for c in commits:
                chunks.append((c.to_chunk(), {
                    "type": "commit", "date": c.date.isoformat(),
                    "repository": c.repository, "author": c.author,
                }))
        except Exception as e:
            logger.bind(cid="github").error(f"Erro ao buscar commits: {e}")
        try:
            prs = await self.fetch_pull_requests()
            for p in prs:
                chunks.append((p.to_chunk(), {
                    "type": "pr", "date": p.created_at.isoformat(),
                    "repository": p.repository, "author": "",
                }))
        except Exception as e:
            logger.bind(cid="github").error(f"Erro ao buscar PRs: {e}")
        try:
            issues = await self.fetch_issues()
            for i in issues:
                chunks.append((i.to_chunk(), {
                    "type": "issue", "date": i.created_at.isoformat(),
                    "repository": i.repository, "author": "",
                }))
        except Exception as e:
            logger.bind(cid="github").error(f"Erro ao buscar issues: {e}")
        return chunks
