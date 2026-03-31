"""Dashboard de Produtividade Dev — Frontend Streamlit."""

import sys
from pathlib import Path

# Garante que o diretório frontend/ está no sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Dashboard Produtividade Dev",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS Global ---
st.markdown("""
<style>
    /* Sidebar com gradiente vibrante */
    section[data-testid="stSidebar"] {
        background: linear-gradient(160deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #e0e7ff !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(139, 92, 246, 0.3);
    }

    /* Fundo principal */
    .stMainBlockContainer {
        background: #f8fafc;
    }

    /* Cards de métrica vibrantes */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f5f3ff 100%);
        border-radius: 16px;
        padding: 18px 22px;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.08);
        border-left: 4px solid #8b5cf6;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.15);
    }
    div[data-testid="stMetric"] label {
        color: #6b7280 !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #1e1b4b !important;
        font-weight: 700 !important;
    }

    /* Botões */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.25);
    }

    /* Forms */
    div[data-testid="stForm"] {
        border: 1px solid #e9d5ff;
        border-radius: 12px;
    }

    /* Containers com borda */
    div[data-testid="stVerticalBlock"]
    > div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
        border-color: #e9d5ff;
    }

    /* Esconde menu de navegação automático do Streamlit */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }
    section[data-testid="stSidebar"] > div > div:first-child > ul {
        display: none !important;
    }

    /* Chat messages */
    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 12px 16px;
    }

    /* Links */
    a {
        color: #7c3aed !important;
    }

    /* Multiselect tags */
    span[data-baseweb="tag"] {
        background-color: #8b5cf6 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown(
        "<h2 style='text-align:center; margin-bottom:4px; "
        "background: linear-gradient(90deg, #a78bfa, #06b6d4); "
        "-webkit-background-clip: text; -webkit-text-fill-color: transparent; "
        "font-size: 20px;'>📊 Produtividade Dev</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; font-size:11px;"
        " opacity:0.5; margin-bottom:20px;'>"
        "Análise inteligente de produtividade</p>",
        unsafe_allow_html=True,
    )

    page = option_menu(
        menu_title=None,
        options=["Dashboard", "Chat RAG", "Configurações"],
        icons=["bar-chart-fill", "chat-dots-fill", "gear-fill"],
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "#a78bfa", "font-size": "18px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px 0",
                "padding": "10px 16px",
                "border-radius": "10px",
                "color": "#1e1b4b",
                "background-color": "rgba(167, 139, 250, 0.08)",
                "--hover-color": "rgba(139, 92, 246, 0.2)",
            },
            "nav-link-selected": {
                "background": (
                    "linear-gradient(135deg,"
                    " rgba(139,92,246,0.3),"
                    " rgba(6,182,212,0.2))"
                ),
                "color": "#f5f3ff",
                "font-weight": "600",
                "border-left": "3px solid #a78bfa",
            },
        },
    )

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; font-size:10px; opacity:0.3;'>v0.1.0</p>",
        unsafe_allow_html=True,
    )

# --- Roteamento ---
if page == "Dashboard":
    from src.pages import dashboard
    dashboard.render()
elif page == "Chat RAG":
    from src.pages import chat
    chat.render()
elif page == "Configurações":
    from src.pages import settings
    settings.render()
