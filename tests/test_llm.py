from copilot.config import Settings
from copilot.llm import AnswerGenerator
from copilot.models import Chunk, RetrievalHit


def test_extract_mode_rewrite_uses_keywords():
    generator = AnswerGenerator(Settings(llm_provider="extractive"))
    assert generator.rewrite("What is Reciprocal Rank Fusion?") == "reciprocal rank fusion"


def test_extract_mode_answer_is_grounded_and_cleans_heading():
    generator = AnswerGenerator(Settings(llm_provider="extractive"))
    chunk = Chunk(
        chunk_id="hybrid#chunk-000",
        doc_id="hybrid",
        text="# Hybrid Retrieval\nReciprocal Rank Fusion combines ranked lists without comparing raw scores.",
        title="Hybrid Retrieval",
        source_file="hybrid.md",
        chunk_index=0,
    )
    hit = RetrievalHit(chunk=chunk, score=1.0, rank=1, method="hybrid_rrf")
    answer = generator.generate("What does Reciprocal Rank Fusion combine?", [hit])
    assert "# Hybrid Retrieval" not in answer
    assert "Reciprocal Rank Fusion combines ranked lists" in answer
    assert "[hybrid#chunk-000]" in answer
