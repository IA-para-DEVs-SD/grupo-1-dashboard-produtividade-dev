import { useState, useEffect, useRef } from "react";
import { api } from "../api/client";

export default function SettingsPage() {
  const [token, setToken] = useState("");
  const [username, setUsername] = useState("");
  const [hasToken, setHasToken] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // LLM config
  const [llmProvider, setLlmProvider] = useState("ollama");
  const [llmModel, setLlmModel] = useState("llama3.1");
  const [apiKey, setApiKey] = useState("");
  const [hasApiKey, setHasApiKey] = useState(false);

  const [ingestStatus, setIngestStatus] = useState<{
    running: boolean;
    step: string;
    logs: string[];
    error: string | null;
  } | null>(null);
  const pollRef = useRef<number | null>(null);

  useEffect(() => {
    Promise.all([
      api.getGitHubConfig(),
      api.getLLMConfig(),
      api.getIngestStatus(),
    ]).then(([gh, llm, ingest]) => {
      setUsername(gh.username);
      setHasToken(gh.has_token);
      setLlmProvider(llm.provider);
      setLlmModel(llm.model);
      setHasApiKey(llm.has_api_key);
      setIngestStatus(ingest);
    }).catch(() => {}).finally(() => setLoading(false));

    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, []);

  const handleSaveGitHub = async () => {
    if (!token || !username) { alert("Preencha token e username"); return; }
    setSaving(true);
    try {
      await api.saveGitHubConfig(token, username);
      setHasToken(true);
      setToken("");
      alert("GitHub configurado!");
    } catch { alert("Erro ao salvar"); }
    setSaving(false);
  };

  const handleSaveLLM = async () => {
    setSaving(true);
    try {
      await api.saveLLMConfig(llmProvider, llmModel, apiKey);
      if (apiKey) setHasApiKey(true);
      setApiKey("");
      alert("LLM configurado!");
    } catch { alert("Erro ao salvar"); }
    setSaving(false);
  };

  const handleIngest = async () => {
    try {
      await api.triggerIngest();
      pollRef.current = window.setInterval(async () => {
        const status = await api.getIngestStatus();
        setIngestStatus(status);
        if (!status.running && pollRef.current) {
          clearInterval(pollRef.current);
          pollRef.current = null;
        }
      }, 1000);
    } catch { alert("Erro ao iniciar ingestão"); }
  };

  const models = llmProvider === "ollama" 
    ? ["llama3.1", "llama3.2:1b", "mistral", "codellama"]
    : ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"];

  return (
    <div style={{ maxWidth: 900, display: "flex", gap: 20, flexWrap: "wrap" }}>
      <div style={{ flex: "1 1 400px" }}>
        <h1 style={{ fontSize: 24, marginBottom: 20 }}>⚙️ Configurações</h1>

        {/* GitHub */}
        <section style={{ background: "#fff", padding: 20, borderRadius: 8, marginBottom: 20 }}>
          <h2 style={{ fontSize: 18, marginBottom: 12 }}>🐙 GitHub</h2>
          {loading ? <p>Carregando...</p> : (
            <div>
              {hasToken && <p style={{ color: "#16a34a", marginBottom: 16 }}>✅ Conectado: <strong>{username}</strong></p>}
              <input type="text" value={username} onChange={(e) => setUsername(e.target.value)}
                placeholder="Username" style={{ width: "100%", padding: 10, borderRadius: 6, border: "1px solid #d1d5db", marginBottom: 12 }} />
              <input type="password" value={token} onChange={(e) => setToken(e.target.value)}
                placeholder={hasToken ? "••••••••" : "ghp_xxxxxxxxxxxx"}
                style={{ width: "100%", padding: 10, borderRadius: 6, border: "1px solid #d1d5db", marginBottom: 12 }} />
              <button onClick={handleSaveGitHub} disabled={saving}
                style={{ background: "#3b82f6", color: "#fff", border: "none", padding: "10px 20px", borderRadius: 6, cursor: "pointer" }}>
                💾 Salvar GitHub
              </button>
            </div>
          )}
        </section>

        {/* LLM */}
        <section style={{ background: "#fff", padding: 20, borderRadius: 8, marginBottom: 20 }}>
          <h2 style={{ fontSize: 18, marginBottom: 12 }}>🤖 LLM (Chat RAG)</h2>
          <div style={{ marginBottom: 12 }}>
            <label style={{ display: "block", marginBottom: 4, fontSize: 14 }}>Provider</label>
            <select value={llmProvider} onChange={(e) => { setLlmProvider(e.target.value); setLlmModel(e.target.value === "ollama" ? "llama3.1" : "gpt-4o-mini"); }}
              style={{ width: "100%", padding: 10, borderRadius: 6, border: "1px solid #d1d5db" }}>
              <option value="ollama">Ollama (local)</option>
              <option value="openai">OpenAI (API)</option>
            </select>
          </div>
          <div style={{ marginBottom: 12 }}>
            <label style={{ display: "block", marginBottom: 4, fontSize: 14 }}>Modelo</label>
            <select value={llmModel} onChange={(e) => setLlmModel(e.target.value)}
              style={{ width: "100%", padding: 10, borderRadius: 6, border: "1px solid #d1d5db" }}>
              {models.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>
          {llmProvider === "openai" && (
            <div style={{ marginBottom: 12 }}>
              <label style={{ display: "block", marginBottom: 4, fontSize: 14 }}>API Key</label>
              <input type="password" value={apiKey} onChange={(e) => setApiKey(e.target.value)}
                placeholder={hasApiKey ? "••••••••" : "sk-..."}
                style={{ width: "100%", padding: 10, borderRadius: 6, border: "1px solid #d1d5db" }} />
            </div>
          )}
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <button onClick={handleSaveLLM} disabled={saving}
              style={{ background: "#8b5cf6", color: "#fff", border: "none", padding: "10px 20px", borderRadius: 6, cursor: "pointer" }}>
              💾 Salvar LLM
            </button>
            <span style={{ fontSize: 12, color: "#64748b" }}>
              {llmProvider === "ollama" ? "⚡ Local (mais lento)" : "🚀 API (mais rápido)"}
            </span>
          </div>
        </section>

        {/* Ingestão */}
        <section style={{ background: "#fff", padding: 20, borderRadius: 8 }}>
          <h2 style={{ fontSize: 18, marginBottom: 12 }}>📥 Ingestão de Dados</h2>
          <button onClick={handleIngest} disabled={!hasToken || ingestStatus?.running}
            style={{ background: hasToken && !ingestStatus?.running ? "#3b82f6" : "#94a3b8",
              color: "#fff", border: "none", padding: "10px 20px", borderRadius: 6,
              cursor: hasToken ? "pointer" : "not-allowed" }}>
            {ingestStatus?.running ? "⏳ Executando..." : "🔄 Executar Ingestão"}
          </button>
        </section>
      </div>

      {/* Status Panel */}
      {ingestStatus && (ingestStatus.running || ingestStatus.logs.length > 0) && (
        <div style={{ flex: "1 1 350px", background: "#1e293b", color: "#e2e8f0",
          padding: 16, borderRadius: 8, fontFamily: "monospace", fontSize: 13, maxHeight: 400, overflowY: "auto" }}>
          <div style={{ marginBottom: 12, display: "flex", justifyContent: "space-between" }}>
            <span style={{ fontWeight: 600 }}>📋 Status</span>
            {ingestStatus.running && <span style={{ color: "#fbbf24" }}>● Executando</span>}
            {!ingestStatus.running && !ingestStatus.error && ingestStatus.logs.length > 0 && <span style={{ color: "#4ade80" }}>● Concluído</span>}
            {ingestStatus.error && <span style={{ color: "#f87171" }}>● Erro</span>}
          </div>
          {ingestStatus.step && <div style={{ marginBottom: 8, color: "#94a3b8" }}>Etapa: {ingestStatus.step}</div>}
          <div style={{ borderTop: "1px solid #334155", paddingTop: 8 }}>
            {ingestStatus.logs.map((log, i) => <div key={i} style={{ marginBottom: 4 }}>{log}</div>)}
          </div>
        </div>
      )}
    </div>
  );
}
