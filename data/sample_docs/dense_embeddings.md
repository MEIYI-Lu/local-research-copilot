# Dense Embeddings

Dense retrieval maps both queries and text chunks into continuous vectors. A sentence embedding model is useful when a user and a document express the same idea with different words. Instead of requiring exact token overlap, retrieval compares vector similarity.

Dense search is especially helpful for paraphrases such as “prevent duplicate processing” versus “make retries idempotent.” It can be weaker on rare identifiers or exact codes that were not represented clearly during model training, which is one reason hybrid retrieval can combine dense and lexical signals.
