"""Página Dashboard — KPIs e gráficos com visual profissional."""

import plotly.graph_objects as go
import streamlit as st

from src.api_client import (
    get_export_url,
    get_github_status,
    get_metrics,
    get_metrics_weekly,
)


def render():
    """Renderiza a página do Dashboard."""
    # Header
    col_title, col_status = st.columns([4, 1])
    with col_title:
        st.markdown(
            "<h1 style='margin:0; font-size:28px;'>📊 Dashboard Produtividade Dev</h1>",
            unsafe_allow_html=True,
        )
    with col_status:
        try:
            status = get_github_status()
            if status.get("connected"):
                st.markdown(
                    f"<div style='text-align:right; padding:8px 0;'>"
                    f"<span style='color:#22d3ee;'>●</span> "
                    f"<span style='font-size:13px; color:#7c3aed;'>"
                    f"GitHub: {status.get('username', '')}</span></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div style='text-align:right; padding:8px 0;'>"
                    "<span style='color:#f472b6;'>●</span> "
                    "<span style='font-size:13px; color:#94a3b8;'>"
                    "GitHub: desconectado</span></div>",
                    unsafe_allow_html=True,
                )
        except Exception:
            st.markdown(
                "<div style='text-align:right; padding:8px 0;'>"
                "<span style='color:#f472b6;'>●</span> "
                "<span style='font-size:13px; color:#94a3b8;'>"
                "GitHub: desconectado</span></div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Filtros em barra horizontal
    with st.container():
        f1, f2, f3, f4, f5 = st.columns([1, 1, 2, 0.5, 0.5])
        with f1:
            date_from = st.date_input("De", value=None, key="dash_from")
        with f2:
            date_to = st.date_input("Até", value=None, key="dash_to")
        with f3:
            visible = st.multiselect(
                "Métricas visíveis",
                ["commits", "prs", "issues"],
                default=["commits", "prs", "issues"],
            )
        str_from = str(date_from) if date_from else None
        str_to = str(date_to) if date_to else None
        with f4:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            csv_url = get_export_url("csv", str_from, str_to)
            st.link_button("📥 CSV", csv_url, use_container_width=True)
        with f5:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            pdf_url = get_export_url("pdf", str_from, str_to)
            st.link_button("📄 PDF", pdf_url, use_container_width=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # KPIs
    try:
        m = get_metrics(str_from, str_to)
        if m.get("error"):
            st.warning(m["error"])
        else:
            _render_kpis(m, visible)
    except Exception:
        st.info("Carregando métricas... Execute a ingestão de dados primeiro.")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Gráficos
    try:
        w = get_metrics_weekly(str_from, str_to)
        if w and not w.get("error"):
            _render_charts(w, visible)
    except Exception:
        pass


def _render_kpis(m: dict, visible: list[str]):
    """Renderiza cards de KPI estilizados."""
    cards = []
    if "commits" in visible:
        cards.append(("📝 Commits total", m.get("total_commits", 0), None))
        cards.append(("📈 Commits/semana", m.get("commits_por_semana", 0), None))
    if "prs" in visible:
        cards.append(("🔀 PRs merged", m.get("prs_merged", 0), None))
        cards.append((
            "⏱️ Tempo merge",
            f"{m.get('tempo_medio_merge_horas', 0)}h",
            None,
        ))
    if "issues" in visible:
        cards.append(("🐛 Issues fechadas", m.get("issues_fechadas", 0), None))

    if not cards:
        return

    cols = st.columns(len(cards))
    for col, (label, value, delta) in zip(cols, cards):
        col.metric(label, value, delta)


def _render_charts(w: dict, visible: list[str]):
    """Renderiza gráficos semanais com Plotly estilizado."""
    weeks = w.get("weeks", [])
    if not weeks:
        return

    chart_cols = []
    if "commits" in visible:
        chart_cols.append("commits")
    if "prs" in visible:
        chart_cols.append("prs")

    if not chart_cols:
        return

    cols = st.columns(len(chart_cols))

    for i, chart_type in enumerate(chart_cols):
        with cols[i]:
            if chart_type == "commits":
                fig = go.Figure(
                    go.Bar(
                        x=weeks,
                        y=w.get("commits", []),
                        marker_color="#8b5cf6",
                        marker_line_width=0,
                    )
                )
                fig.update_layout(
                    title=dict(
                        text="Commits por Semana",
                        font=dict(size=16, color="#1e293b"),
                    ),
                    height=380,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(gridcolor="#f1f5f9"),
                    yaxis=dict(gridcolor="#f1f5f9"),
                    margin=dict(l=40, r=20, t=50, b=40),
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "prs":
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=weeks, y=w.get("prs_opened", []),
                        name="Abertos", line=dict(color="#f472b6", width=3),
                        mode="lines+markers",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=weeks, y=w.get("prs_closed", []),
                        name="Fechados", line=dict(color="#06b6d4", width=3),
                        mode="lines+markers",
                    )
                )
                fig.update_layout(
                    title=dict(
                        text="PRs Abertos vs Fechados",
                        font=dict(size=16, color="#1e293b"),
                    ),
                    height=380,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(gridcolor="#f1f5f9"),
                    yaxis=dict(gridcolor="#f1f5f9"),
                    margin=dict(l=40, r=20, t=50, b=40),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                    ),
                )
                st.plotly_chart(fig, use_container_width=True)
