const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface Props {
  from?: string;
  to?: string;
}

export default function ExportButtons({ from, to }: Props) {
  const params = new URLSearchParams();
  if (from) params.set("from", from);
  if (to) params.set("to", to);
  const qs = params.toString();

  return (
    <div style={{ display: "flex", gap: 8 }}>
      <a href={`${BASE}/export/csv${qs ? `?${qs}` : ""}`} target="_blank" rel="noreferrer"
        style={{
          padding: "6px 14px", borderRadius: 8, background: "#10b981", color: "#fff",
          textDecoration: "none", fontSize: 13,
        }}>
        📥 CSV
      </a>
      <a href={`${BASE}/export/pdf${qs ? `?${qs}` : ""}`} target="_blank" rel="noreferrer"
        style={{
          padding: "6px 14px", borderRadius: 8, background: "#8b5cf6", color: "#fff",
          textDecoration: "none", fontSize: 13,
        }}>
        📄 PDF
      </a>
    </div>
  );
}
