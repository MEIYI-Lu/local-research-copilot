from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

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


def evaluate_file(kb: "KnowledgeBase", path: Path, k: int = 3) -> dict[str, float]:
    cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    metrics: list[Metrics] = []
    for case in cases:
        hits = kb.search(case["question"], k=k)
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
