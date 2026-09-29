# Changelog

## 0.3.1

- Added the measured 30-query v0.3 retrieval benchmark to the README.
- Added per-query-type interpretation for lexical, semantic, and multi-evidence retrieval.
- Documented that Hybrid RRF achieved the highest overall MRR while tying Dense retrieval on top-3 coverage metrics.
- Kept the benchmark conclusions scoped to the included project corpus.


## 0.3.0

- Expanded the included sample corpus from 6 to 24 documents.
- Expanded the labelled evaluation set from 7 to 30 questions.
- Added lexical, semantic, and multi-evidence query groups.
- Added grouped retrieval reporting to the CLI benchmark.
- Preserved the v0.2 seven-question benchmark for reproducibility.
- Added benchmark and web-app screenshots to the repository documentation.
- Added evaluation-set validation and additional metric tests.

## 0.2.0

- Improved the zero-API extractive answer fallback.
- Added deterministic query rewriting for non-LLM retry routing.
- Added BM25 vs dense vs Hybrid RRF benchmark comparison.
- Improved the Streamlit interface and Codespaces documentation.
