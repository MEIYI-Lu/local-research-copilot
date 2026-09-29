from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .config import Settings
from .ingest import chunk_documents, load_documents
from .models import Chunk, RetrievalHit
from .retrieval.bm25 import BM25Retriever
from .retrieval.chroma import ChromaRetriever
from .retrieval.hybrid import reciprocal_rank_fusion


class KnowledgeBase:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.chunks: list[Chunk] = []
        self.lookup: dict[str, Chunk] = {}
        self.bm25: BM25Retriever | None = None
        self.chroma: ChromaRetriever | None = None

    @property
    def manifest_path(self) -> Path:
        return self.settings.index_dir / "chunks.json"

    def build(self, document_dir: Path) -> int:
        docs = load_documents(document_dir)
        self.chunks = chunk_documents(
            docs,
            chunk_size=self.settings.chunk_size,
            overlap=self.settings.chunk_overlap,
        )
        self.lookup = {chunk.chunk_id: chunk for chunk in self.chunks}
        self.settings.index_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(
            json.dumps([asdict(chunk) for chunk in self.chunks], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        self.bm25 = BM25Retriever(self.chunks)
        self.chroma = ChromaRetriever(
            self.settings.index_dir,
            self.settings.collection_name,
            self.settings.embedding_model,
        )
        self.chroma.rebuild(self.chunks)
        return len(self.chunks)

    def load(self) -> None:
        if not self.manifest_path.exists():
            raise FileNotFoundError(
                f"No index found at {self.manifest_path}. Run the index command first."
            )
        raw = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.chunks = [Chunk(**item) for item in raw]
        self.lookup = {chunk.chunk_id: chunk for chunk in self.chunks}
        self.bm25 = BM25Retriever(self.chunks)
        self.chroma = ChromaRetriever(
            self.settings.index_dir,
            self.settings.collection_name,
            self.settings.embedding_model,
        )

    def search(self, query: str, k: int | None = None) -> list[RetrievalHit]:
        if self.bm25 is None or self.chroma is None:
            self.load()
        final_k = k or self.settings.final_k
        bm25_hits = self.bm25.retrieve(query, k=self.settings.retrieve_k_each)  # type: ignore[union-attr]
        dense_hits = self.chroma.retrieve(  # type: ignore[union-attr]
            query, self.lookup, k=self.settings.retrieve_k_each
        )
        return reciprocal_rank_fusion(
            bm25_hits,
            dense_hits,
            rrf_k=self.settings.rrf_k,
            final_k=final_k,
        )
