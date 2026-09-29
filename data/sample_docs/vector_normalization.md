# Vector Normalization and Cosine Similarity

Cosine similarity compares the angle between vectors rather than their raw magnitude. When embedding vectors are L2-normalized to unit length, cosine similarity becomes equivalent to their dot product. Normalization can therefore simplify vector comparison and make score behaviour more consistent across queries.

A dense retriever should use a similarity measure that matches how its embedding model was intended to be compared. Mixing normalized and unnormalized representations without understanding the distance function can produce misleading rankings.
