import { useState } from "react";
import MainLayout from "./components/Layout/MainLayout";
import Dashboard from "./pages/Dashboard";
import ChatPage from "./pages/ChatPage";
import SettingsPage from "./pages/SettingsPage";

export default function App() {
  const [page, setPage] = useState<"dashboard" | "chat" | "settings">("dashboard");

  return (
    <MainLayout currentPage={page} onNavigate={setPage}>
      {page === "dashboard" && <Dashboard />}
      {page === "chat" && <ChatPage />}
      {page === "settings" && <SettingsPage />}
    </MainLayout>
  );
}
