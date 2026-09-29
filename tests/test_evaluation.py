from pathlib import Path

from copilot.evaluation import evaluate_case, evaluation_set_summary


def test_metrics():
    m = evaluate_case(["a", "b", "c"], ["b", "x"], k=3)
    assert round(m.precision_at_k, 4) == round(1 / 3, 4)
    assert m.recall_at_k == 0.5
    assert m.hit_at_k == 1.0
    assert m.mrr == 0.5


def test_multi_relevant_precision_and_recall():
    m = evaluate_case(["a", "b", "z"], ["a", "b", "c"], k=3)
    assert round(m.precision_at_k, 4) == round(2 / 3, 4)
    assert round(m.recall_at_k, 4) == round(2 / 3, 4)
    assert m.hit_at_k == 1.0
    assert m.mrr == 1.0


def test_evaluation_set_summary(tmp_path: Path):
    path = tmp_path / "questions.jsonl"
    path.write_text(
        '\n'.join([
            '{"question":"q1","relevant_doc_ids":["a"],"query_type":"lexical"}',
            '{"question":"q2","relevant_doc_ids":["b"],"query_type":"semantic"}',
            '{"question":"q3","relevant_doc_ids":["c"],"query_type":"semantic"}',
        ]),
        encoding="utf-8",
    )
    assert evaluation_set_summary(path) == {"total": 3, "lexical": 1, "semantic": 2}
