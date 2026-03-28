"""Página Configurações — GitHub, LLM e Ingestão com visual profissional."""

import time

import streamlit as st

from src.api_client import (
    get_github_config,
    get_ingest_status,
    get_llm_config,
    save_github_config,
    save_llm_config,
    trigger_ingest,
)

OLLAMA_MODELS = ["llama3.1", "llama3.2:1b", "mistral", "codellama"]
OPENAI_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]


def render():
    """Renderiza a página de configurações."""
    st.markdown(
        "<h1 style='margin:0; font-size:28px;'>⚙️ Configurações</h1>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    col_main, col_status = st.columns([2, 1])

    with col_main:
        _render_github_section()
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        _render_llm_section()
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        _render_ingest_section()

    with col_status:
        _render_ingest_status()


def _render_github_section():
    """Seção de configuração do GitHub."""
    with st.container(border=True):
        st.markdown("### 🐙 GitHub")

        try:
            config = get_github_config()
            has_token = config.get("has_token", False)
            saved_username = config.get("username", "")
        except Exception:
            has_token = False
            saved_username = ""

        if has_token:
            st.success(f"✅ Conectado: **{saved_username}**")

        with st.form("github_form"):
            username = st.text_input("Username", value=saved_username)
            token = st.text_input(
                "Token",
                type="password",
                placeholder="ghp_xxxxxxxxxxxx" if not has_token else "••••••••",
            )
            submitted = st.form_submit_button("💾 Salvar GitHub", use_container_width=True)

            if submitted:
                if not token or not username:
                    st.error("Preencha token e username.")
                else:
                    try:
                        save_github_config(token, username)
                        st.success("GitHub configurado!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar: {e}")


def _render_llm_section():
    """Seção de configuração do LLM."""
    with st.container(border=True):
        st.markdown("### 🤖 LLM (Chat RAG)")

        try:
            config = get_llm_config()
            saved_provider = config.get("provider", "ollama")
            saved_model = config.get("model", "llama3.1")
            has_api_key = config.get("has_api_key", False)
        except Exception:
            saved_provider = "ollama"
            saved_model = "llama3.1"
            has_api_key = False

        with st.form("llm_form"):
            provider = st.selectbox(
                "Provider",
                ["ollama", "openai"],
                index=0 if saved_provider == "ollama" else 1,
                format_func=lambda x: "🖥️ Ollama (local)" if x == "ollama" else "☁️ OpenAI (API)",
            )

            models = OLLAMA_MODELS if provider == "ollama" else OPENAI_MODELS
            default_idx = models.index(saved_model) if saved_model in models else 0
            model = st.selectbox("Modelo", models, index=default_idx)

            api_key = ""
            if provider == "openai":
                api_key = st.text_input(
                    "API Key",
                    type="password",
                    placeholder="••••••••" if has_api_key else "sk-...",
                )

            info = "⚡ Local — mais lento, sem custo" if provider == "ollama" else "🚀 API — mais rápido, com custo"
            st.caption(info)

            submitted = st.form_submit_button("💾 Salvar LLM", use_container_width=True)
            if submitted:
                try:
                    save_llm_config(provider, model, api_key)
                    st.success("LLM configurado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")


def _render_ingest_section():
    """Seção de ingestão de dados."""
    with st.container(border=True):
        st.markdown("### 📥 Ingestão de Dados")

        try:
            config = get_github_config()
            has_token = config.get("has_token", False)
        except Exception:
            has_token = False

        if not has_token:
            st.warning("Configure o GitHub primeiro para executar a ingestão.")

        if st.button(
            "🔄 Executar Ingestão",
            disabled=not has_token,
            use_container_width=True,
        ):
            try:
                trigger_ingest()
                st.info("Ingestão iniciada! Acompanhe o status ao lado →")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao iniciar ingestão: {e}")


def _render_ingest_status():
    """Painel de status da ingestão."""
    try:
        status = get_ingest_status()
    except Exception:
        return

    logs = status.get("logs", [])
    running = status.get("running", False)
    error = status.get("error")

    if not running and not logs:
        with st.container(border=True):
            st.markdown("### 📋 Status")
            st.caption("Nenhuma ingestão executada ainda.")
        return

    with st.container(border=True):
        st.markdown("### 📋 Status")

        if running:
            st.warning("● Executando...")
            st.progress(
                min(status.get("progress", 0) / max(status.get("total", 1), 1), 1.0)
            )
        elif error:
            st.error(f"● Erro: {error}")
        elif logs:
            st.success("● Concluído")

        step = status.get("step", "")
        if step:
            st.caption(f"Etapa: {step}")

        if logs:
            with st.expander("📜 Logs", expanded=running):
                st.code("\n".join(logs[-20:]), language=None)

    # Auto-refresh enquanto roda
    if running:
        time.sleep(2)
        st.rerun()
