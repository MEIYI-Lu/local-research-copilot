from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .agent import ResearchAgent
from .config import Settings
from .evaluation import evaluate_file
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


@app.command(name="eval")
def eval_command(
    questions: Path = typer.Argument(..., exists=True, dir_okay=False),
    k: int = typer.Option(3, min=1),
) -> None:
    settings = Settings()
    kb = KnowledgeBase(settings)
    kb.load()
    results = evaluate_file(kb, questions, k=k)

    table = Table(title=f"Retrieval evaluation @ {k}")
    table.add_column("Metric")
    table.add_column("Score", justify="right")
    for key, value in results.items():
        table.add_row(key, f"{value:.4f}")
    console.print(table)


if __name__ == "__main__":
    app()
