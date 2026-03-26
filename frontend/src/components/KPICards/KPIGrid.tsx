import { api, type Metrics } from "../../api/client";
import KPICard from "./KPICard";

interface Props {
  metrics: Metrics | null;
  visibleMetrics: Set<string>;
}

export default function KPIGrid({ metrics, visibleMetrics }: Props) {
  if (!metrics || metrics.error) {
    return <div style={{ color: "#64748b", marginBottom: 24 }}>Carregando métricas...</div>;
  }

  const cards = [
    { key: "commits", icon: "📝", title: "Commits total", value: metrics.total_commits },
    { key: "commits", icon: "📈", title: "Commits/semana", value: metrics.commits_por_semana },
    { key: "prs", icon: "🔀", title: "PRs merged", value: metrics.prs_merged },
    { key: "prs", icon: "⏱️", title: "Tempo merge (h)", value: metrics.tempo_medio_merge_horas },
    { key: "issues", icon: "🐛", title: "Issues fechadas", value: metrics.issues_fechadas },
  ];

  return (
    <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 24 }}>
      {cards
        .filter((c) => visibleMetrics.has(c.key))
        .map((c, i) => (
          <KPICard key={i} icon={c.icon} title={c.title} value={c.value} />
        ))}
    </div>
  );
}
