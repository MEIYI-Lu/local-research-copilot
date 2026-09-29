from __future__ import annotations

import re
from typing import TypedDict

from langgraph.graph import END, StateGraph

from .config import Settings
from .guardrails import filter_untrusted_chunks, inspect_text
from .knowledge_base import KnowledgeBase
from .llm import AnswerGenerator
from .models import CopilotAnswer, RetrievalHit
from .retrieval.bm25 import tokenize


class AgentState(TypedDict, total=False):
    question: str
    working_query: str
    hits: list[RetrievalHit]
    confidence: float
    retries: int
    route: str
    answer: str
    citations: list[str]
    error: str


def _query_evidence_overlap(question: str, hits: list[RetrievalHit]) -> float:
    q_terms = set(tokenize(question))
    if not q_terms or not hits:
        return 0.0
    text_terms = set(tokenize(" ".join(hit.chunk.text for hit in hits[:3])))
    return len(q_terms & text_terms) / max(1, len(q_terms))


def _evidence_confidence(question: str, hits: list[RetrievalHit]) -> float:
    if not hits:
        return 0.0
    dense_scores = [hit.components.get("dense", 0.0) for hit in hits]
    semantic = max(0.0, min(1.0, max(dense_scores, default=0.0)))
    overlap = _query_evidence_overlap(question, hits)
    return max(0.0, min(1.0, 0.7 * semantic + 0.3 * overlap))


class ResearchAgent:
    def __init__(self, kb: KnowledgeBase, settings: Settings):
        self.kb = kb
        self.settings = settings
        self.generator = AnswerGenerator(settings)
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("guard", self._guard)
        graph.add_node("retrieve", self._retrieve)
        graph.add_node("assess", self._assess)
        graph.add_node("rewrite", self._rewrite)
        graph.add_node("answer", self._answer)
        graph.add_node("refuse", self._refuse)

        graph.set_entry_point("guard")
        graph.add_conditional_edges("guard", self._route_after_guard, {"retrieve": "retrieve", "refuse": "refuse"})
        graph.add_edge("retrieve", "assess")
        graph.add_conditional_edges(
            "assess",
            self._route_after_assessment,
            {"answer": "answer", "rewrite": "rewrite", "refuse": "refuse"},
        )
        graph.add_edge("rewrite", "retrieve")
        graph.add_edge("answer", END)
        graph.add_edge("refuse", END)
        return graph.compile()

    def _guard(self, state: AgentState) -> AgentState:
        result = inspect_text(state["question"])
        if not result.safe:
            return {**state, "route": "refuse", "error": result.reason}
        return {**state, "working_query": state["question"], "retries": 0, "route": "retrieve"}

    @staticmethod
    def _route_after_guard(state: AgentState) -> str:
        return state.get("route", "retrieve")

    def _retrieve(self, state: AgentState) -> AgentState:
        hits = self.kb.search(state["working_query"], k=self.settings.final_k)
        clean_texts, removed = filter_untrusted_chunks([hit.chunk.text for hit in hits])
        allowed = set(clean_texts)
        clean_hits = [hit for hit in hits if hit.chunk.text in allowed]
        updated = {**state, "hits": clean_hits}
        if removed:
            updated["error"] = f"Removed {removed} suspicious retrieved chunk(s)."
        return updated

    def _assess(self, state: AgentState) -> AgentState:
        confidence = _evidence_confidence(state["question"], state.get("hits", []))
        return {**state, "confidence": confidence}

    def _route_after_assessment(self, state: AgentState) -> str:
        if state.get("confidence", 0.0) >= self.settings.confidence_threshold:
            return "answer"
        if state.get("retries", 0) < 1:
            return "rewrite"
        return "refuse"

    def _rewrite(self, state: AgentState) -> AgentState:
        rewritten = self.generator.rewrite(state["question"])
        rewritten = re.sub(r"\s+", " ", rewritten).strip()
        return {
            **state,
            "working_query": rewritten or state["question"],
            "retries": state.get("retries", 0) + 1,
            "route": "rewrite",
        }

    def _answer(self, state: AgentState) -> AgentState:
        hits = state.get("hits", [])
        return {
            **state,
            "answer": self.generator.generate(state["question"], hits),
            "citations": [hit.chunk.chunk_id for hit in hits],
            "route": "answer",
        }

    @staticmethod
    def _refuse(state: AgentState) -> AgentState:
        message = (
            "I do not have enough trustworthy evidence in the local knowledge base to answer "
            "this question confidently. Add a relevant source or ask a narrower question."
        )
        if state.get("error") and not state.get("hits"):
            message = "The request was blocked by the input/evidence safety check."
        return {**state, "answer": message, "citations": [], "route": "refuse"}

    def ask(self, question: str) -> CopilotAnswer:
        state = self.graph.invoke({"question": question})
        return CopilotAnswer(
            question=question,
            answer=state.get("answer", ""),
            citations=state.get("citations", []),
            confidence=float(state.get("confidence", 0.0)),
            route=state.get("route", "unknown"),
            hits=state.get("hits", []),
        )
