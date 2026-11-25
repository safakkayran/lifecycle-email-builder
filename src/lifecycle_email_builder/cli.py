"""CLI commands for lifecycle-email-builder."""

from __future__ import annotations

import subprocess
from typing import Annotated

import httpx
import typer
from lifecycle_builder import __version__
from lifecycle_builder.config import get_settings
from rich.console import Console

app = typer.Typer(
    name="lifecycle",
    help="Build lifecycle email programs from product URLs",
    add_completion=False,
)
console = Console()


@app.command()
def build(
    url: Annotated[str, typer.Argument(help="Product URL to analyze")],
    slug: Annotated[
        str | None,
        typer.Option("--slug", "-s", help="Output slug (default: domain)"),
    ] = None,
    voice_file: Annotated[
        str | None,
        typer.Option("--voice-file", "-v", help="Path to existing voice.md"),
    ] = None,
    from_step: Annotated[int, typer.Option("--from-step", help="Resume from step (1-7)")] = 1,
):
    """Run full pipeline: URL -> context -> voice -> funnel ->
    drafts -> lint -> render -> export."""
    get_settings()  # validate settings
    console.print(f"[bold]Building lifecycle emails for {url}[/bold]")
    console.print("[yellow]Not implemented yet - M0 scaffold[/yellow]")


@app.command()
def context(url: str):
    """Step 1: Fetch site and generate product marketing context."""
    get_settings()
    console.print("[yellow]Step 1: Product context - not implemented yet[/yellow]")


@app.command()
def voice(url: str):
    """Step 2: Generate brand voice guide."""
    get_settings()
    console.print("[yellow]Step 2: Voice guide - not implemented yet[/yellow]")


@app.command()
def funnel(url: str):
    """Step 3: Generate funnel map (funnel.yaml)."""
    get_settings()
    console.print("[yellow]Step 3: Funnel map - not implemented yet[/yellow]")


@app.command()
def draft(url: str):
    """Step 4: Generate email drafts."""
    get_settings()
    console.print("[yellow]Step 4: Email drafts - not implemented yet[/yellow]")


@app.command()
def lint(url: str):
    """Step 5: Lint and fix email drafts."""
    get_settings()
    console.print("[yellow]Step 5: Lint - not implemented yet[/yellow]")


@app.command()
def render(url: str):
    """Step 6: Render MJML to HTML."""
    get_settings()
    console.print("[yellow]Step 6: Render - not implemented yet[/yellow]")


@app.command()
def export(url: str):
    """Step 7: Export to generic.json (and Loops/Customer.io if configured)."""
    get_settings()
    console.print("[yellow]Step 7: Export - not implemented yet[/yellow]")


@app.command()
def doctor():
    """Check environment: LLM reachable, Node present, submodule present."""
    settings = get_settings()

    # Check LLM
    console.print("[bold]Checking LLM proxy...[/bold]")
    try:
        resp = httpx.get(f"{settings.LITELLM_BASE_URL}/v1/models", timeout=5.0)
        if resp.status_code == 200:
            console.print("[green]✓[/green] LiteLLM reachable")
        else:
            console.print(f"[red]✗[/red] LiteLLM returned {resp.status_code}")
    except Exception as e:
        console.print(f"[red]✗[/red] LiteLLM unreachable: {e}")

    # Check Node
    console.print("[bold]Checking Node...[/bold]")
    try:
        result = subprocess.run(
            ["node", "--version"], check=False, capture_output=True, text=True
        )
        if result.returncode == 0:
            console.print(f"[green]✓[/green] Node {result.stdout.strip()}")
        else:
            console.print("[red]✗[/red] Node not found")
    except Exception:
        console.print("[red]✗[/red] Node not found")

    # Check submodule
    console.print("[bold]Checking submodule...[/bold]")
    if (settings.VENDOR_DIR / "skills" / "emails" / "SKILL.md").exists():
        console.print("[green]✓[/green] marketingskills submodule present")
    else:
        console.print("[red]✗[/red] marketingskills submodule missing")


@app.command()
def version():
    """Show version."""
    console.print(f"lifecycle-email-builder {__version__}")


if __name__ == "__main__":
    app()