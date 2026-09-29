# Retrieval Evaluation

Retrieval evaluation should be separated from answer style. Precision at K measures how many of the top K retrieved results are relevant. Recall at K measures how many known relevant documents were found. Hit at K records whether at least one relevant result appears. Mean Reciprocal Rank (MRR) rewards systems that place the first relevant result near the top.

A useful test set contains realistic questions and a small set of relevant document IDs for each question. Because evaluation is deterministic at the retrieval layer, it can be repeated after changes to chunk size, overlap, embedding model, retrieval depth, or fusion settings.
