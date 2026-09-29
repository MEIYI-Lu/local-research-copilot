from copilot.evaluation import evaluate_case


def test_metrics():
    m = evaluate_case(["a", "b", "c"], ["b", "x"], k=3)
    assert round(m.precision_at_k, 4) == round(1 / 3, 4)
    assert m.recall_at_k == 0.5
    assert m.hit_at_k == 1.0
    assert m.mrr == 0.5
