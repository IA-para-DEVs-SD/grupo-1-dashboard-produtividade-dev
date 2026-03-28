interface Props {
  metrics: { key: string; label: string; visible: boolean }[];
  onToggle: (key: string) => void;
}

export default function MetricToggle({ metrics, onToggle }: Props) {
  return (
    <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
      {metrics.map((m) => (
        <button key={m.key} onClick={() => onToggle(m.key)}
          style={{
            padding: "4px 12px", borderRadius: 16, fontSize: 12, cursor: "pointer",
            background: m.visible ? "#06b6d4" : "#e2e8f0",
            color: m.visible ? "#fff" : "#64748b",
            border: "none",
          }}>
          {m.label}
        </button>
      ))}
    </div>
  );
}
