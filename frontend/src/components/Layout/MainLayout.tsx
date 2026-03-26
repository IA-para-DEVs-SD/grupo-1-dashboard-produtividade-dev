import { ReactNode } from "react";

type Page = "dashboard" | "chat" | "settings";

interface Props {
  children: ReactNode;
  currentPage: Page;
  onNavigate: (page: Page) => void;
}

export default function MainLayout({ children, currentPage, onNavigate }: Props) {
  const navItems: { key: Page; label: string }[] = [
    { key: "dashboard", label: "Dashboard" },
    { key: "chat", label: "Chat RAG" },
    { key: "settings", label: "Configurações" },
  ];

  return (
    <div style={{ display: "flex", minHeight: "100vh", fontFamily: "system-ui, sans-serif" }}>
      <aside style={{ width: 220, background: "#1e293b", color: "#fff", padding: 20 }}>
        <h2 style={{ fontSize: 16, marginBottom: 24 }}>📊 Produtividade Dev</h2>
        <nav style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {navItems.map((item) => (
            <span
              key={item.key}
              onClick={() => onNavigate(item.key)}
              style={{
                opacity: currentPage === item.key ? 1 : 0.6,
                cursor: "pointer",
                fontWeight: currentPage === item.key ? 600 : 400,
                padding: "8px 12px",
                borderRadius: 6,
                background: currentPage === item.key ? "#334155" : "transparent",
              }}
            >
              {item.label}
            </span>
          ))}
        </nav>
      </aside>
      <main style={{ flex: 1, background: "#f1f5f9", padding: 24 }}>{children}</main>
    </div>
  );
}
