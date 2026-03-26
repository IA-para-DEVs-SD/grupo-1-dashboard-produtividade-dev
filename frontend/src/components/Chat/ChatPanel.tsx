import { useState } from "react";
import { api } from "../../api/client";

interface Message {
  role: "user" | "assistant";
  content: string;
  evidence?: string;
  recommendation?: string;
}

export default function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim() || loading) return;
    const query = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", content: query }]);
    setLoading(true);
    try {
      const res = await api.postInsight(query);
      setMessages((m) => [
        ...m,
        { role: "assistant", content: res.summary, evidence: res.evidence, recommendation: res.recommendation },
      ]);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Erro ao consultar o RAG.";
      setMessages((m) => [...m, { role: "assistant", content: `❌ ${msg}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: "#fff", borderRadius: 12, padding: 20, marginTop: 24 }}>
      <h3 style={{ margin: "0 0 16px", fontSize: 16, color: "#1e293b" }}>🧠 Chat RAG</h3>
      <div style={{ maxHeight: 300, overflowY: "auto", marginBottom: 12, display: "flex", flexDirection: "column", gap: 8 }}>
        {messages.map((m, i) => (
          <div key={i} style={{
            alignSelf: m.role === "user" ? "flex-end" : "flex-start",
            background: m.role === "user" ? "#06b6d4" : "#f1f5f9",
            color: m.role === "user" ? "#fff" : "#1e293b",
            padding: "8px 14px", borderRadius: 12, maxWidth: "80%",
          }}>
            <div>{m.content}</div>
            {m.evidence && <div style={{ fontSize: 12, marginTop: 4, opacity: 0.8 }}>📊 {m.evidence}</div>}
            {m.recommendation && <div style={{ fontSize: 12, marginTop: 2, opacity: 0.8 }}>💡 {m.recommendation}</div>}
          </div>
        ))}
        {loading && <div style={{ opacity: 0.5 }}>Pensando...</div>}
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Pergunte sobre sua produtividade..."
          style={{ flex: 1, padding: "8px 12px", borderRadius: 8, border: "1px solid #cbd5e1", outline: "none" }}
          aria-label="Pergunta para o chat RAG"
        />
        <button onClick={send} disabled={loading}
          style={{ padding: "8px 16px", borderRadius: 8, background: "#06b6d4", color: "#fff", border: "none", cursor: "pointer" }}>
          Enviar
        </button>
      </div>
    </div>
  );
}
