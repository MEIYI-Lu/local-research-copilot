# Hybrid Retrieval

Lexical and semantic retrieval make different errors. BM25 is strong when the query and document share important terms, identifiers, or rare words. Dense embedding retrieval is useful when the wording differs but the meaning is similar. A hybrid system combines these signals instead of assuming that one method is always best.

Reciprocal Rank Fusion (RRF) combines ranked lists without requiring their raw scores to be directly comparable. Each retrieved item's contribution is based on its rank, commonly using 1 / (k + rank). Documents appearing near the top of multiple lists accumulate a larger fused score. RRF is simple, robust, and useful when BM25 and vector similarity operate on different score scales.
