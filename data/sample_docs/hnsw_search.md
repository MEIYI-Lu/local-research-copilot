# HNSW Approximate Nearest Neighbour Search

Hierarchical Navigable Small World (HNSW) graphs support fast approximate nearest-neighbour search over large vector collections. The index connects vectors in a layered graph so a query can move quickly from coarse regions to nearby candidates.

Two practical parameters are `efConstruction`, which affects index-build quality and cost, and `efSearch`, which controls how many candidates are explored at query time. Increasing `efSearch` usually improves recall but costs more latency. HNSW therefore exposes an explicit speed-versus-recall trade-off instead of exhaustively comparing a query with every vector.
