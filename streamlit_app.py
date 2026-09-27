from __future__ import annotations

import streamlit as st

from copilot.agent import ResearchAgent
from copilot.config import Settings
from copilot.knowledge_base import KnowledgeBase


st.set_page_config(page_title="Local Research Copilot", page_icon="🔎", layout="wide")
st.title("🔎 Local Research Copilot")
st.caption("Hybrid RAG + LangGraph evidence routing, running from your local knowledge base.")


@st.cache_resource
def load_agent() -> ResearchAgent:
    settings = Settings()
    kb = KnowledgeBase(settings)
    kb.load()
    return ResearchAgent(kb, settings)


try:
    agent = load_agent()
except FileNotFoundError:
    st.error("No local index found. Run: research-copilot index data/sample_docs")
    st.stop()

question = st.chat_input("Ask a question about your indexed documents")
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        result = agent.ask(question)
        st.write(result.answer)
        st.caption(f"Route: {result.route} · confidence: {result.confidence:.2f}")
        if result.hits:
            with st.expander("Retrieved evidence"):
                for hit in result.hits:
                    st.markdown(f"**{hit.chunk.chunk_id}** — {hit.chunk.title}")
                    st.write(hit.chunk.text)
