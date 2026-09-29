from __future__ import annotations

from ..models import RetrievalHit


def reciprocal_rank_fusion(
    bm25_hits: list[RetrievalHit],
    dense_hits: list[RetrievalHit],
    rrf_k: int = 60,
    final_k: int = 5,
) -> list[RetrievalHit]:
    fused: dict[str, dict] = {}

    for method, hits in (("bm25", bm25_hits), ("dense", dense_hits)):
        for hit in hits:
            item = fused.setdefault(
                hit.chunk.chunk_id,
                {"chunk": hit.chunk, "score": 0.0, "components": {}},
            )
            item["score"] += 1.0 / (rrf_k + hit.rank)
            item["components"][f"{method}_rank"] = float(hit.rank)
            item["components"].update(hit.components)

    ordered = sorted(fused.values(), key=lambda item: item["score"], reverse=True)[:final_k]
    return [
        RetrievalHit(
            chunk=item["chunk"],
            score=float(item["score"]),
            rank=rank,
            method="hybrid_rrf",
            components=item["components"],
        )
        for rank, item in enumerate(ordered, start=1)
    ]
