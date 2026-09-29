from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    index_dir: Path = Path("index")
    chunk_size: int = 180
    chunk_overlap: int = 40
    embedding_model: str = os.getenv(
        "COPILOT_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    collection_name: str = "research_copilot"
    rrf_k: int = 60
    retrieve_k_each: int = 8
    final_k: int = 5
    confidence_threshold: float = 0.40
    llm_provider: str = os.getenv("COPILOT_LLM_PROVIDER", "extractive")
    ollama_model: str = os.getenv("COPILOT_OLLAMA_MODEL", "qwen2.5:7b")
    ollama_url: str = os.getenv("COPILOT_OLLAMA_URL", "http://localhost:11434")
