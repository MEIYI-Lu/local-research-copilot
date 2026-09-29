# Evaluation set

`questions.jsonl` is the v0.3 expanded retrieval benchmark. It contains **30 labelled questions** across three query types:

- `lexical` — exact technical terms, acronyms, and identifiers;
- `semantic` — paraphrased intent with less direct token overlap;
- `multi_evidence` — questions with two or three relevant documents.

Each record contains a `question`, one or more `relevant_doc_ids`, and a `query_type`.

`questions_v0_2.jsonl` preserves the original seven-question sanity-check benchmark so the published v0.2 numbers remain reproducible.
