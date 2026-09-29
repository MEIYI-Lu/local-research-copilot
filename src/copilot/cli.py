from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .agent import ResearchAgent
from .config import Settings
from .evaluation import (
    evaluate_comparison,
    evaluate_comparison_by_group,
    evaluation_set_summary,
)
from .knowledge_base import KnowledgeBase


app = typer.Typer(help="Local hybrid RAG + agentic research copilot")
console = Console()


@app.command()
def index(directory: Path = typer.Argument(..., exists=True, file_okay=False)) -> None:
    settings = Settings()
    kb = KnowledgeBase(settings)
    count = kb.build(directory)
    console.print(f"[green]Indexed {count} chunks[/green] into {settings.index_dir}")


@app.command()
def ask(question: str) -> None:
    settings = Settings()
    kb = KnowledgeBase(settings)
    kb.load()
    result = ResearchAgent(kb, settings).ask(question)

    console.print(f"[bold]Route:[/bold] {result.route}")
    console.print(f"[bold]Confidence:[/bold] {result.confidence:.2f}")
    console.print("\n[bold]Answer[/bold]")
    console.print(result.answer)

    if result.citations:
        console.print("\n[bold]Sources[/bold]")
        for citation in result.citations:
            console.print(f"- {citation}")


def _render_metrics_table(title: str, results: dict[str, dict[str, float]], k: int) -> None:
    table = Table(title=title)
    table.add_column("Retriever")
    table.add_column(f"Precision@{k}", justify="right")
    table.add_column(f"Recall@{k}", justify="right")
    table.add_column(f"Hit@{k}", justify="right")
    table.add_column("MRR", justify="right")

    for retriever, metrics in results.items():
        table.add_row(
            retriever,
            f"{metrics['precision@k']:.4f}",
            f"{metrics['recall@k']:.4f}",
            f"{metrics['hit@k']:.4f}",
            f"{metrics['mrr']:.4f}",
        )
    console.print(table)


@app.command(name="eval")
def eval_command(
    questions: Path = typer.Argument(..., exists=True, dir_okay=False),
    k: int = typer.Option(3, min=1),
    by_group: bool = typer.Option(
        True,
        "--by-group/--overall-only",
        help="Also report metrics for each query_type label in the evaluation set.",
    ),
) -> None:
    settings = Settings()
    kb = KnowledgeBase(settings)
    kb.load()

    summary = evaluation_set_summary(questions)
    group_text = ", ".join(
        f"{name}={count}" for name, count in summary.items() if name != "total"
    )
    console.print(
        f"[dim]Evaluation set: {summary['total']} queries"
        + (f" ({group_text})" if group_text else "")
        + "[/dim]"
    )

    overall = evaluate_comparison(kb, questions, k=k)
    _render_metrics_table(f"Overall retrieval benchmark @ {k}", overall, k)

    if by_group:
        grouped = evaluate_comparison_by_group(kb, questions, k=k)
        for group, results in grouped.items():
            _render_metrics_table(f"Query type: {group} @ {k}", results, k)


if __name__ == "__main__":
    app()
