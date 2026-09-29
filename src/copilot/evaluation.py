from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from .models import RetrievalHit

if TYPE_CHECKING:
    from .knowledge_base import KnowledgeBase


@dataclass
class Metrics:
    precision_at_k: float
    recall_at_k: float
    hit_at_k: float
    mrr: float


def evaluate_case(retrieved_doc_ids: list[str], relevant_doc_ids: list[str], k: int) -> Metrics:
    retrieved = retrieved_doc_ids[:k]
    relevant = set(relevant_doc_ids)
    unique_retrieved = set(retrieved)
    matches = unique_retrieved & relevant
    precision = len(matches) / max(1, k)
    recall = len(matches) / max(1, len(relevant))
    hit = 1.0 if matches else 0.0
    rr = 0.0
    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            rr = 1.0 / rank
            break
    return Metrics(precision, recall, hit, rr)


def _load_cases(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _aggregate(
    cases: list[dict],
    search: Callable[[str, int], list[RetrievalHit]],
    k: int,
) -> dict[str, float]:
    metrics: list[Metrics] = []
    for case in cases:
        hits = search(case["question"], k)
        retrieved_doc_ids = [hit.chunk.doc_id for hit in hits]
        metrics.append(evaluate_case(retrieved_doc_ids, case["relevant_doc_ids"], k))

    if not metrics:
        return {"precision@k": 0.0, "recall@k": 0.0, "hit@k": 0.0, "mrr": 0.0}

    n = len(metrics)
    return {
        "precision@k": sum(m.precision_at_k for m in metrics) / n,
        "recall@k": sum(m.recall_at_k for m in metrics) / n,
        "hit@k": sum(m.hit_at_k for m in metrics) / n,
        "mrr": sum(m.mrr for m in metrics) / n,
    }


def evaluate_file(kb: "KnowledgeBase", path: Path, k: int = 3) -> dict[str, float]:
    """Backward-compatible hybrid-only evaluation."""
    cases = _load_cases(path)
    return _aggregate(cases, lambda query, limit: kb.search(query, k=limit), k)


def evaluate_comparison(
    kb: "KnowledgeBase", path: Path, k: int = 3
) -> dict[str, dict[str, float]]:
    """Compare lexical, dense, and hybrid retrieval on the same labelled questions."""
    cases = _load_cases(path)
    return {
        "BM25": _aggregate(cases, lambda query, limit: kb.search_bm25(query, k=limit), k),
        "Dense": _aggregate(cases, lambda query, limit: kb.search_dense(query, k=limit), k),
        "Hybrid RRF": _aggregate(cases, lambda query, limit: kb.search(query, k=limit), k),
    }
