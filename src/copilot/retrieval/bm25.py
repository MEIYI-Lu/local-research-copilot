from __future__ import annotations

import re

from rank_bm25 import BM25Okapi

from ..models import Chunk, RetrievalHit


TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


class BM25Retriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self._tokens = [tokenize(chunk.text) for chunk in chunks]
        self._index = BM25Okapi(self._tokens) if self._tokens else None

    def retrieve(self, query: str, k: int = 5) -> list[RetrievalHit]:
        if not self._index or not self.chunks:
            return []
        scores = self._index.get_scores(tokenize(query))
        ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)[:k]
        return [
            RetrievalHit(
                chunk=self.chunks[i],
                score=float(score),
                rank=rank,
                method="bm25",
                components={"bm25": float(score)},
            )
            for rank, (i, score) in enumerate(ranked, start=1)
        ]
