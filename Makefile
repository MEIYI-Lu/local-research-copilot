.PHONY: install codespaces-install index ask eval test ui

install:
	pip install -r requirements.txt
	pip install -e .

codespaces-install:
	pip install --no-cache-dir -r requirements.txt
	pip install -e . --no-deps

index:
	research-copilot index data/sample_docs

ask:
	research-copilot ask "How can search combine exact terms with semantic similarity?"

eval:
	research-copilot eval data/eval/questions.jsonl --k 3

test:
	pytest -q

ui:
	streamlit run streamlit_app.py
