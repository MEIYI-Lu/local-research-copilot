# RAG Fundamentals

Retrieval-augmented generation (RAG) separates knowledge retrieval from language generation. Before an answer is produced, the system searches a document collection for passages that are relevant to the user's question. Those passages become evidence for the answer. This design can reduce hallucination because the model is asked to ground claims in retrieved sources rather than rely only on parametric memory.

RAG quality depends on several independent stages: ingestion, cleaning, chunking, retrieval, ranking, context construction, answer generation, and evaluation. A fluent final answer does not prove that retrieval was correct, so retrieval metrics should be measured separately.
