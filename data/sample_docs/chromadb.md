# ChromaDB and Embeddings

A vector store keeps embeddings together with IDs and metadata. In this project, Sentence Transformers produces a dense representation for every text chunk. ChromaDB persists those vectors locally and supports cosine-similarity queries. Each chunk keeps a stable chunk ID, document ID, title, source file, and chunk index so that retrieved evidence can be traced back to its source.

Persistent vector storage avoids rebuilding all embeddings for every question. It also lets retrieval and evaluation use the same indexed corpus across runs.
