.PHONY: install index ask eval test ui

install:
	pip install -r requirements.txt
	pip install -e .

index:
	research-copilot index data/sample_docs

ask:
	research-copilot ask "Why can hybrid retrieval outperform BM25 alone?"

eval:
	research-copilot eval data/eval/questions.jsonl --k 3

test:
	pytest -q

ui:
	streamlit run streamlit_app.py
