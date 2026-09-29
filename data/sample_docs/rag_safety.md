# RAG Safety and Prompt Injection

Retrieved documents are untrusted data. A malicious or accidental document can contain text such as “ignore previous instructions” or “reveal the system prompt.” A RAG system should not treat those strings as authoritative instructions merely because they were retrieved.

This project applies two simple defences. It checks user input for common prompt-injection patterns and filters suspicious retrieved chunks before answer generation. The answer prompt also explicitly says that evidence is untrusted data. These controls reduce obvious attacks but are not a complete security boundary. Production systems should use stronger isolation, least-privilege tools, provenance checks, monitoring, and adversarial testing.
