from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    doc_id: str
    text: str
    title: str
    source_file: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    title: str
    source_file: str
    chunk_index: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrievalHit:
    chunk: Chunk
    score: float
    rank: int
    method: str
    components: dict[str, float] = field(default_factory=dict)


@dataclass
class CopilotAnswer:
    question: str
    answer: str
    citations: list[str]
    confidence: float
    route: str
    hits: list[RetrievalHit] = field(default_factory=list)
