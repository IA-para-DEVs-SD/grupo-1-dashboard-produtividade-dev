const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, options);
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || `API error: ${res.status}`);
  }
  return res.json();
}

export interface Metrics {
  total_commits: number;
  total_prs: number;
  total_issues: number;
  commits_por_semana: number;
  commits_por_dia: number;
  prs_merged: number;
  issues_fechadas: number;
  tempo_medio_merge_horas: number;
  hot_repos: { repo: string; commits: number }[];
  periodo_dias: number;
  error?: string;
}

export interface WeeklyMetrics {
  weeks: string[];
  commits: number[];
  prs_opened: number[];
  prs_closed: number[];
  error?: string;
}

export interface GitHubStatus {
  connected: boolean;
  username?: string;
  error?: string;
}

export interface Insight {
  summary: string;
  evidence: string;
  recommendation: string;
  sources: string[];
}

export const api = {
  getHealth: () => apiFetch<{ status: string }>("/health"),

  getGitHubStatus: () => apiFetch<GitHubStatus>("/github/status"),

  getGitHubConfig: () => apiFetch<{ username: string; has_token: boolean }>("/settings/github"),

  saveGitHubConfig: (token: string, username: string) =>
    apiFetch<{ status: string }>("/settings/github", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, username }),
    }),

  getLLMConfig: () => apiFetch<{ provider: string; model: string; has_api_key: boolean }>("/settings/llm"),

  saveLLMConfig: (provider: string, model: string, api_key: string) =>
    apiFetch<{ status: string }>("/settings/llm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ provider, model, api_key }),
    }),

  getMetrics: (from?: string, to?: string) => {
    const params = new URLSearchParams();
    if (from) params.set("from", from);
    if (to) params.set("to", to);
    const qs = params.toString();
    return apiFetch<Metrics>(`/metrics${qs ? `?${qs}` : ""}`);
  },

  getMetricsWeekly: (from?: string, to?: string) => {
    const params = new URLSearchParams();
    if (from) params.set("from", from);
    if (to) params.set("to", to);
    const qs = params.toString();
    return apiFetch<WeeklyMetrics>(`/metrics/weekly${qs ? `?${qs}` : ""}`);
  },

  postInsight: (query: string) =>
    apiFetch<Insight>("/insights", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    }),

  triggerIngest: () =>
    apiFetch<{ status: string; message: string }>("/ingest", { method: "POST" }),

  getIngestStatus: () =>
    apiFetch<{
      running: boolean;
      step: string;
      progress: number;
      total: number;
      started_at: string | null;
      finished_at: string | null;
      error: string | null;
      logs: string[];
    }>("/ingest/status"),
};
