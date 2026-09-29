# Citation Grounding

Grounded answers should retain enough provenance to show where their claims came from. During ingestion, each chunk can preserve a stable document ID, chunk ID, source filename, title, and position. Retrieval results can carry that metadata into answer generation.

A citation-first interface makes the evidence inspectable and helps distinguish “the model knows this” from “the indexed source supports this.” Citations do not guarantee correctness by themselves, but they make unsupported claims easier to detect and give a user a path back to the original source.
