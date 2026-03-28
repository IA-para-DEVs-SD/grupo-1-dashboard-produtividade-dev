import { useEffect, useState } from "react";
import { api, type GitHubStatus } from "../../api/client";

export default function Header() {
  const [status, setStatus] = useState<GitHubStatus | null>(null);

  useEffect(() => {
    api.getGitHubStatus().then(setStatus).catch(() => setStatus({ connected: false }));
  }, []);

  return (
    <header style={{
      display: "flex", justifyContent: "space-between", alignItems: "center",
      marginBottom: 24, paddingBottom: 16, borderBottom: "1px solid #e2e8f0",
    }}>
      <h1 style={{ fontSize: 22, color: "#1e293b", margin: 0 }}>
        📊 Dashboard Produtividade Dev
      </h1>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{
          width: 10, height: 10, borderRadius: "50%",
          background: status?.connected ? "#10b981" : "#ef4444",
        }} />
        <span style={{ fontSize: 13, color: "#64748b" }}>
          {status?.connected ? `GitHub: ${status.username}` : "GitHub: desconectado"}
        </span>
      </div>
    </header>
  );
}
