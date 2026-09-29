from __future__ import annotations

import json
from collections import defaultdict
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
    cases = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    for idx, case in enumerate(cases, start=1):
        if "question" not in case or "relevant_doc_ids" not in case:
            raise ValueError(f"Evaluation case {idx} must contain question and relevant_doc_ids")
        if not case["relevant_doc_ids"]:
            raise ValueError(f"Evaluation case {idx} has no relevant documents")
        case.setdefault("query_type", "unlabelled")
    return cases


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


def _retrievers(kb: "KnowledgeBase") -> dict[str, Callable[[str, int], list[RetrievalHit]]]:
    return {
        "BM25": lambda query, limit: kb.search_bm25(query, k=limit),
        "Dense": lambda query, limit: kb.search_dense(query, k=limit),
        "Hybrid RRF": lambda query, limit: kb.search(query, k=limit),
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
        name: _aggregate(cases, search, k)
        for name, search in _retrievers(kb).items()
    }


def evaluate_comparison_by_group(
    kb: "KnowledgeBase", path: Path, k: int = 3
) -> dict[str, dict[str, dict[str, float]]]:
    """Return the same comparison broken down by the optional query_type field."""
    cases = _load_cases(path)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for case in cases:
        grouped[str(case.get("query_type", "unlabelled"))].append(case)

    return {
        group: {
            name: _aggregate(group_cases, search, k)
            for name, search in _retrievers(kb).items()
        }
        for group, group_cases in sorted(grouped.items())
    }


def evaluation_set_summary(path: Path) -> dict[str, int]:
    """Return query counts by label for display in the CLI and documentation checks."""
    cases = _load_cases(path)
    counts: dict[str, int] = defaultdict(int)
    counts["total"] = len(cases)
    for case in cases:
        counts[str(case.get("query_type", "unlabelled"))] += 1
    return dict(counts)
