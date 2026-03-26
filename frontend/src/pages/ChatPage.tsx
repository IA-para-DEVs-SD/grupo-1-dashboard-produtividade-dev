import ChatPanel from "../components/Chat/ChatPanel";

export default function ChatPage() {
  return (
    <div>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>💬 Chat RAG</h1>
      <p style={{ color: "#64748b", marginBottom: 20 }}>
        Faça perguntas sobre sua produtividade. O sistema usa RAG para buscar
        contexto dos seus commits, PRs e issues.
      </p>
      <ChatPanel />
    </div>
  );
}
