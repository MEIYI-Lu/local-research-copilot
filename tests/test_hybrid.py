from copilot.models import Chunk, RetrievalHit
from copilot.retrieval.hybrid import reciprocal_rank_fusion


def _hit(chunk_id: str, rank: int, method: str) -> RetrievalHit:
    chunk = Chunk(chunk_id, chunk_id, "text", chunk_id, "demo.md", 0)
    return RetrievalHit(chunk=chunk, score=1.0, rank=rank, method=method)


def test_rrf_rewards_items_found_by_both_retrievers():
    bm25 = [_hit("shared", 2, "bm25"), _hit("lexical", 1, "bm25")]
    dense = [_hit("shared", 1, "dense"), _hit("semantic", 2, "dense")]
    fused = reciprocal_rank_fusion(bm25, dense, rrf_k=60, final_k=3)
    assert fused[0].chunk.chunk_id == "shared"
