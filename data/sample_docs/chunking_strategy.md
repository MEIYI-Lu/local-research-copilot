# Chunking Strategy

Long documents are usually split into smaller chunks before indexing. Chunk size determines how much context each retrievable unit contains, while overlap repeats a small boundary region between neighbouring chunks. Overlap can prevent an important sentence pair from being separated at exactly the wrong boundary.

Very small chunks can retrieve precise snippets but may lose context. Very large chunks preserve context but can mix unrelated topics and waste the model context window. A practical chunking strategy therefore treats size and overlap as parameters to evaluate rather than universal constants.
