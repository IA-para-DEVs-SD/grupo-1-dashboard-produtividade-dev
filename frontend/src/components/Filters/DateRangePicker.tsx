interface Props {
  from: string;
  to: string;
  onChange: (from: string, to: string) => void;
}

export default function DateRangePicker({ from, to, onChange }: Props) {
  return (
    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
      <label style={{ fontSize: 13, color: "#64748b" }}>De:</label>
      <input type="date" value={from} onChange={(e) => onChange(e.target.value, to)}
        style={{ padding: "4px 8px", borderRadius: 6, border: "1px solid #cbd5e1" }} />
      <label style={{ fontSize: 13, color: "#64748b" }}>Até:</label>
      <input type="date" value={to} onChange={(e) => onChange(from, e.target.value)}
        style={{ padding: "4px 8px", borderRadius: 6, border: "1px solid #cbd5e1" }} />
    </div>
  );
}
