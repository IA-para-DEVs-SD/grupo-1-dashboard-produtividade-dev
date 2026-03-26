import { useEffect, useState } from "react";
import { api, type Metrics, type WeeklyMetrics } from "../api/client";
import Header from "../components/Layout/Header";
import KPIGrid from "../components/KPICards/KPIGrid";
import CommitsChart from "../components/Charts/CommitsChart";
import PRsChart from "../components/Charts/PRsChart";
import DateRangePicker from "../components/Filters/DateRangePicker";
import MetricToggle from "../components/Filters/MetricToggle";
import ExportButtons from "../components/Filters/ExportButtons";

export default function Dashboard() {
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [weekly, setWeekly] = useState<WeeklyMetrics | null>(null);
  const [visibleMetrics, setVisibleMetrics] = useState(new Set(["commits", "prs", "issues"]));

  const loadData = () => {
    api.getMetrics(from || undefined, to || undefined).then(setMetrics).catch(console.error);
    api.getMetricsWeekly(from || undefined, to || undefined).then(setWeekly).catch(console.error);
  };

  useEffect(() => {
    loadData();
  }, [from, to]);

  const toggleMetric = (key: string) => {
    setVisibleMetrics((prev) => {
      const next = new Set(prev);
      if (next.has(key) && next.size > 1) {
        next.delete(key);
      } else {
        next.add(key);
      }
      return next;
    });
  };

  const metricOptions = [
    { key: "commits", label: "Commits", visible: visibleMetrics.has("commits") },
    { key: "prs", label: "PRs", visible: visibleMetrics.has("prs") },
    { key: "issues", label: "Issues", visible: visibleMetrics.has("issues") },
  ];

  return (
    <div>
      <Header />

      <div style={{
        display: "flex", justifyContent: "space-between", alignItems: "center",
        marginBottom: 20, flexWrap: "wrap", gap: 12,
      }}>
        <div style={{ display: "flex", gap: 16, alignItems: "center", flexWrap: "wrap" }}>
          <DateRangePicker from={from} to={to} onChange={(f, t) => { setFrom(f); setTo(t); }} />
          <MetricToggle metrics={metricOptions} onToggle={toggleMetric} />
        </div>
        <ExportButtons from={from} to={to} />
      </div>

      <KPIGrid metrics={metrics} visibleMetrics={visibleMetrics} />

      <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
        {visibleMetrics.has("commits") && (
          <CommitsChart labels={weekly?.weeks || []} data={weekly?.commits || []} />
        )}
        {visibleMetrics.has("prs") && (
          <PRsChart
            labels={weekly?.weeks || []}
            opened={weekly?.prs_opened || []}
            closed={weekly?.prs_closed || []}
          />
        )}
      </div>
    </div>
  );
}
