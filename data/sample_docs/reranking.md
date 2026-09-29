# Retrieval Reranking

A reranker is a stronger second-stage model applied after a fast retriever has produced a manageable candidate set. The first stage may use BM25, dense vectors, or a hybrid method to retrieve tens of candidates. A cross-encoder reranker can then score each query-document pair jointly and reorder those candidates.

This design separates recall from precision: the first stage tries not to miss useful evidence, while the reranker spends more computation deciding which candidates deserve the top positions. Reranking is useful when top-1 quality matters more than raw retrieval speed.
