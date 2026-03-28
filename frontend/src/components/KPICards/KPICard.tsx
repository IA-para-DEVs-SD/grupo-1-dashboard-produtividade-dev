interface Props {
  title: string;
  value: string | number;
  icon: string;
}

export default function KPICard({ title, value, icon }: Props) {
  return (
    <div style={{
      background: "#fff", borderRadius: 12, padding: 20, minWidth: 180,
      boxShadow: "0 1px 3px rgba(0,0,0,0.1)", display: "flex", alignItems: "center", gap: 16,
    }}>
      <span style={{ fontSize: 28 }}>{icon}</span>
      <div>
        <div style={{ fontSize: 12, color: "#64748b", textTransform: "uppercase" }}>{title}</div>
        <div style={{ fontSize: 24, fontWeight: 700, color: "#1e293b" }}>{value}</div>
      </div>
    </div>
  );
}
