from copilot.ingest import chunk_document
from copilot.models import Document


def test_chunking_overlap_and_ids():
    doc = Document("demo", " ".join(f"w{i}" for i in range(20)), "Demo", "demo.txt")
    chunks = chunk_document(doc, chunk_size=8, overlap=2)
    assert len(chunks) == 3
    assert chunks[0].chunk_id == "demo#chunk-000"
    assert chunks[1].text.split()[0] == "w6"
