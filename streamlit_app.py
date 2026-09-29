from __future__ import annotations

import streamlit as st

from copilot.agent import ResearchAgent
from copilot.config import Settings
from copilot.knowledge_base import KnowledgeBase


st.set_page_config(page_title="Local Research Copilot", page_icon="🔎", layout="wide")
st.title("🔎 Local Research Copilot")
st.caption("Hybrid RAG + LangGraph evidence routing over a local knowledge base.")


@st.cache_resource
def load_agent() -> ResearchAgent:
    settings = Settings()
    kb = KnowledgeBase(settings)
    kb.load()
    return ResearchAgent(kb, settings)


try:
    agent = load_agent()
except FileNotFoundError:
    st.error("No local index found. Run: `research-copilot index data/sample_docs`")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Knowledge base")
    st.metric("Indexed chunks", len(agent.kb.chunks))
    st.caption("BM25 + dense retrieval → RRF → evidence assessment → answer / retry / refuse")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("**Try an example**")
examples = [
    "What is Reciprocal Rank Fusion?",
    "How does backpressure protect a slow consumer?",
    "What is the capital of Brazil?",
]
columns = st.columns(3)
selected_question = None
for column, example in zip(columns, examples):
    if column.button(example, use_container_width=True):
        selected_question = example


def render_assistant(message: dict) -> None:
    st.write(message["content"])
    route_icon = "✅" if message["route"] == "answer" else "🛑"
    st.caption(
        f"{route_icon} Route: {message['route']} · evidence confidence: {message['confidence']:.2f}"
    )
    st.progress(max(0.0, min(1.0, message["confidence"])), text="Evidence confidence")

    if message["hits"]:
        with st.expander("Retrieved evidence"):
            for hit in message["hits"]:
                st.markdown(f"**{hit['title']}** · `{hit['chunk_id']}`")
                component_parts = [f"hybrid={hit['score']:.4f}"]
                if "dense" in hit["components"]:
                    component_parts.append(f"dense={hit['components']['dense']:.3f}")
                if "bm25_rank" in hit["components"]:
                    component_parts.append(f"BM25 rank={int(hit['components']['bm25_rank'])}")
                if "dense_rank" in hit["components"]:
                    component_parts.append(f"dense rank={int(hit['components']['dense_rank'])}")
                st.caption(" · ".join(component_parts))
                st.write(hit["text"])
                st.divider()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            render_assistant(message)
        else:
            st.write(message["content"])

question = selected_question or st.chat_input("Ask a question about your indexed documents")
if question:
    user_message = {"role": "user", "content": question}
    st.session_state.messages.append(user_message)
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving and checking evidence..."):
            result = agent.ask(question)
        assistant_message = {
            "role": "assistant",
            "content": result.answer,
            "route": result.route,
            "confidence": result.confidence,
            "hits": [
                {
                    "chunk_id": hit.chunk.chunk_id,
                    "title": hit.chunk.title,
                    "text": hit.chunk.text,
                    "score": hit.score,
                    "components": hit.components,
                }
                for hit in result.hits
            ],
        }
        st.session_state.messages.append(assistant_message)
        render_assistant(assistant_message)
