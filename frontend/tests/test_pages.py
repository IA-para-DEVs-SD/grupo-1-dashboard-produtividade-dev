"""Testes unitários para as páginas do frontend Streamlit.

Valida: funções auxiliares do dashboard (_render_kpis, _render_charts),
constantes de configuração do settings, e lógica do chat.
"""

from unittest.mock import MagicMock, patch


class TestDashboardHelpers:
    """Testes para funções auxiliares do dashboard."""

    def test_render_kpis_filters_by_visible(self):
        """Regra: _render_kpis só mostra métricas selecionadas em 'visible'."""
        from src.pages.dashboard import _render_kpis

        metrics = {
            "total_commits": 42,
            "commits_por_semana": 6.0,
            "prs_merged": 5,
            "tempo_medio_merge_horas": 3.2,
            "issues_fechadas": 10,
        }
        # Sem métricas visíveis, não deve chamar st.columns
        with patch("src.pages.dashboard.st") as mock_st:
            _render_kpis(metrics, [])
            mock_st.columns.assert_not_called()

    def test_render_kpis_shows_commits_when_visible(self):
        """Regra: commits visíveis geram cards de KPI."""
        from src.pages.dashboard import _render_kpis

        metrics = {
            "total_commits": 42,
            "commits_por_semana": 6.0,
        }
        with patch("src.pages.dashboard.st") as mock_st:
            mock_cols = [MagicMock(), MagicMock()]
            mock_st.columns.return_value = mock_cols
            _render_kpis(metrics, ["commits"])
            # Deve criar 2 colunas (total + por semana)
            mock_st.columns.assert_called_once_with(2)

    def test_render_charts_returns_early_without_weeks(self):
        """Regra: sem dados semanais, gráficos não são renderizados."""
        from src.pages.dashboard import _render_charts

        with patch("src.pages.dashboard.st") as mock_st:
            _render_charts({"weeks": []}, ["commits"])
            mock_st.columns.assert_not_called()

    def test_render_charts_filters_by_visible(self):
        """Regra: gráficos só aparecem para métricas visíveis."""
        from src.pages.dashboard import _render_charts

        weekly = {
            "weeks": ["01/03", "08/03"],
            "commits": [5, 8],
            "prs_opened": [2, 3],
            "prs_closed": [1, 2],
        }
        with patch("src.pages.dashboard.st") as mock_st:
            mock_cols = [MagicMock()]
            mock_st.columns.return_value = mock_cols
            with patch("src.pages.dashboard.go"):
                _render_charts(weekly, ["commits"])
                mock_st.columns.assert_called_once_with(1)


class TestSettingsConstants:
    """Testes para constantes de configuração."""

    def test_ollama_models_contains_llama31(self):
        """Regra: lista de modelos Ollama inclui llama3.1 (default)."""
        from src.pages.settings import OLLAMA_MODELS

        assert "llama3.1" in OLLAMA_MODELS

    def test_openai_models_contains_gpt4o_mini(self):
        """Regra: lista de modelos OpenAI inclui gpt-4o-mini (default prod)."""
        from src.pages.settings import OPENAI_MODELS

        assert "gpt-4o-mini" in OPENAI_MODELS

    def test_ollama_and_openai_models_are_disjoint(self):
        """Regra: listas de modelos não se sobrepõem."""
        from src.pages.settings import OLLAMA_MODELS, OPENAI_MODELS

        overlap = set(OLLAMA_MODELS) & set(OPENAI_MODELS)
        assert not overlap, f"Modelos duplicados: {overlap}"


class TestChatLogic:
    """Testes para lógica do chat RAG."""

    def test_chat_module_has_render_function(self):
        """Regra: módulo chat expõe função render()."""
        from src.pages import chat

        assert hasattr(chat, "render")
        assert callable(chat.render)

    def test_dashboard_module_has_render_function(self):
        """Regra: módulo dashboard expõe função render()."""
        from src.pages import dashboard

        assert hasattr(dashboard, "render")
        assert callable(dashboard.render)

    def test_settings_module_has_render_function(self):
        """Regra: módulo settings expõe função render()."""
        from src.pages import settings

        assert hasattr(settings, "render")
        assert callable(settings.render)
