"""Página Chat RAG — perguntas sobre produtividade com visual de chat."""

import streamlit as st

from src.api_client import post_insight


def render():
    """Renderiza a página de Chat RAG."""
    st.markdown(
        "<h1 style='margin:0; font-size:28px;'>💬 Chat RAG</h1>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Faça perguntas sobre sua produtividade. O sistema usa RAG para buscar "
        "contexto dos seus commits, PRs e issues."
    )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Inicializa histórico
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Container do chat
    chat_container = st.container(height=450)

    with chat_container:
        if not st.session_state.chat_messages:
            st.markdown(
                "<div style='text-align:center; padding:60px 0; color:#94a3b8;'>"
                "<p style='font-size:40px; margin-bottom:8px;'>🧠</p>"
                "<p>Nenhuma conversa ainda.<br>"
                "Pergunte algo sobre sua produtividade!</p></div>",
                unsafe_allow_html=True,
            )
        else:
            for msg in st.session_state.chat_messages:
                avatar = (
                    "🧑‍💻" if msg["role"] == "user" else "🤖"
                )
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])
                    if msg.get("evidence"):
                        st.info(f"📊 {msg['evidence']}", icon=None)
                    if msg.get("recommendation"):
                        st.success(f"💡 {msg['recommendation']}", icon=None)

    # Input do usuário
    if prompt := st.chat_input("Pergunte sobre sua produtividade..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        with chat_container:
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Pensando..."):
                    try:
                        res = post_insight(prompt)
                        content = res.get("summary", "Sem resposta.")
                        evidence = res.get("evidence", "")
                        recommendation = res.get("recommendation", "")

                        st.markdown(content)
                        if evidence:
                            st.info(f"📊 {evidence}", icon=None)
                        if recommendation:
                            st.success(f"💡 {recommendation}", icon=None)

                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": content,
                            "evidence": evidence,
                            "recommendation": recommendation,
                        })
                    except Exception as e:
                        error_msg = str(e)
                        st.error(f"❌ {error_msg}")
                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": f"❌ {error_msg}",
                        })
