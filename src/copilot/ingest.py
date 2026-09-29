from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

from .models import Chunk, Document


SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}


def _normalise_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _read_file(path: Path) -> str:
    if path.suffix.lower() in {".md", ".txt"}:
        return path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    raise ValueError(f"Unsupported file type: {path.suffix}")


def load_documents(directory: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        text = _normalise_text(_read_file(path))
        if not text:
            continue
        doc_id = path.stem.lower().replace(" ", "_")
        title = path.stem.replace("_", " ").title()
        documents.append(
            Document(
                doc_id=doc_id,
                text=text,
                title=title,
                source_file=str(path),
                metadata={"extension": path.suffix.lower()},
            )
        )
    return documents


def chunk_document(document: Document, chunk_size: int = 180, overlap: int = 40) -> list[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must satisfy 0 <= overlap < chunk_size")

    words = document.text.split()
    step = chunk_size - overlap
    chunks: list[Chunk] = []

    for idx, start in enumerate(range(0, len(words), step)):
        piece = words[start : start + chunk_size]
        if not piece:
            break
        chunks.append(
            Chunk(
                chunk_id=f"{document.doc_id}#chunk-{idx:03d}",
                doc_id=document.doc_id,
                text=" ".join(piece),
                title=document.title,
                source_file=document.source_file,
                chunk_index=idx,
                metadata=document.metadata.copy(),
            )
        )
        if start + chunk_size >= len(words):
            break
    return chunks


def chunk_documents(
    documents: list[Document], chunk_size: int = 180, overlap: int = 40
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        chunks.extend(chunk_document(document, chunk_size=chunk_size, overlap=overlap))
    return chunks
