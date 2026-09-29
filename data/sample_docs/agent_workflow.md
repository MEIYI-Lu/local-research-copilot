# Agent Workflow

The research copilot uses a small stateful workflow rather than a single prompt. The graph first checks the query for suspicious prompt-injection language. It then retrieves evidence, estimates whether the evidence is strong enough, and chooses the next action. Strong evidence routes to answering. Weak evidence gets one query-rewrite retry. If evidence remains weak, the system refuses to invent an answer.

This control flow makes the decision process inspectable. The graph state records the original question, working query, retrieved hits, confidence, retry count, route, answer, and citations.
