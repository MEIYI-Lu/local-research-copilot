# BM25 Scoring

BM25 is a lexical ranking function built around exact term matches. It rewards documents that contain query terms, but reduces the benefit of repeating the same word many times. Two common tuning parameters are `k1` and `b`. The `k1` parameter controls term-frequency saturation: a larger value allows repeated occurrences of a term to keep contributing for longer. The `b` parameter controls document-length normalization, with larger values applying a stronger correction for long documents.

BM25 is often a strong first-stage retriever for identifiers, product names, error codes, acronyms, and rare technical vocabulary because these signals are represented directly rather than through semantic similarity.
