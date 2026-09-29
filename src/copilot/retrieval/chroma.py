from __future__ import annotations

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ..models import Chunk, RetrievalHit


class ChromaRetriever:
    def __init__(self, index_dir: Path, collection_name: str, embedding_model: str):
        index_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(index_dir / "chroma"))
        self.collection_name = collection_name
        self.model = SentenceTransformer(embedding_model)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def rebuild(self, chunks: list[Chunk]) -> None:
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        if not chunks:
            return
        embeddings = self.model.encode(
            [chunk.text for chunk in chunks], normalize_embeddings=True, show_progress_bar=False
        ).tolist()
        metadatas = [
            {
                "doc_id": chunk.doc_id,
                "title": chunk.title,
                "source_file": chunk.source_file,
                "chunk_index": chunk.chunk_index,
            }
            for chunk in chunks
        ]
        self.collection.add(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def retrieve(self, query: str, chunk_lookup: dict[str, Chunk], k: int = 5) -> list[RetrievalHit]:
        if self.collection.count() == 0:
            return []
        query_embedding = self.model.encode([query], normalize_embeddings=True).tolist()
        result = self.collection.query(query_embeddings=query_embedding, n_results=k)
        ids = result.get("ids", [[]])[0]
        distances = result.get("distances", [[]])[0]

        hits: list[RetrievalHit] = []
        for rank, (chunk_id, distance) in enumerate(zip(ids, distances), start=1):
            chunk = chunk_lookup.get(chunk_id)
            if not chunk:
                continue
            similarity = 1.0 - float(distance)
            hits.append(
                RetrievalHit(
                    chunk=chunk,
                    score=similarity,
                    rank=rank,
                    method="chroma",
                    components={"dense": similarity},
                )
            )
        return hits
