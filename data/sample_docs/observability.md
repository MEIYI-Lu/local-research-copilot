# Observability

Observability combines signals such as logs, metrics, and distributed traces so operators can understand how a running system behaves. Metrics summarize numeric trends, logs record discrete events, and traces connect work across service boundaries.

Useful observability is designed around questions the team may need to answer during failures. High-cardinality identifiers belong in carefully chosen trace or log fields rather than blindly becoming metric labels. Instrumentation should help explain latency, errors, saturation, and dependency behaviour without exposing sensitive data.
