import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Multi-Agent Researcher", page_icon="🤖")
st.title("🤖 Multi-Agent Researcher")
st.caption("Powered by a Search Agent + Summariser Agent working together")

question = st.text_input(
    "Ask a research question:", placeholder="e.g. What is quantum computing?"
)

is_loading = st.session_state.get("is_loading", False)
button_clicked = st.button("🔍 Research", type="primary", disabled=is_loading)
enter_pressed = question.strip() and question != st.session_state.get("last_question")

if (button_clicked or enter_pressed) and question.strip() and not is_loading:
    st.session_state.is_loading = True
    with st.spinner("Agents are working... this may take a minute."):
        response = requests.post(
            f"{API_URL}/research", json={"question": question}, timeout=300
        )
        st.session_state.result = response.json()
        st.session_state.last_question = question
    st.session_state.is_loading = False

if st.session_state.get("result"):
    result = st.session_state.result

    with st.expander("🔎 Raw research (from Search Agent)", expanded=False):
        st.markdown(result.get("raw_research", ""))

    st.divider()
    st.subheader("📋 Final Report (from Summariser Agent)")
    st.markdown(result.get("report", ""))
