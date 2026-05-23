from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .core import generate
from .render import to_markdown

cli = typer.Typer()
console = Console()


@cli.command()
def gen(
    repo: Path = typer.Option(Path.cwd, help="Path to git repository"),
    from_ref: str = typer.Option("", help="Starting ref/tag (default: latest tag)"),
    to_ref: str = typer.Option("HEAD", help="Ending ref"),
    version: str = typer.Option("", help="Version label for the changelog"),
    output: Path | None = typer.Option(None, help="Write to file instead of stdout"),
) -> None:
    """Generate a changelog from git history."""
    cl = generate(repo=repo, from_ref=from_ref, to_ref=to_ref, version=version)
    md = to_markdown(cl)

    if output:
        output.write_text(md)
        console.print(f"[green]Changelog written to {output}[/green]")
    else:
        console.print(md)


@cli.command()
def preview(
    repo: Path = typer.Option(Path.cwd),
    version: str = typer.Option("next", help="Version label"),
) -> None:
    """Preview changelog for unreleased changes (latest tag to HEAD)."""
    cl = generate(repo=repo, to_ref="HEAD", version=version)
    md = to_markdown(cl)
    console.print(md)


def main() -> None:
    cli()
