from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table

from .auth import create_authenticated_client
from .client import TailwindPlusClient
from .storage import ComponentStorage
from .scraper import TailwindPlusScraper

app = typer.Typer(
    name="tailwind-dev-kit",
    help="Developer kit & scraper for Tailwind CSS Plus / UI components and templates.",
    add_completion=False,
)
console = Console(legacy_windows=False)


@app.command()
def verify_auth() -> None:
    """Verify Tailwind Plus authentication status and license in .env."""
    console.print("\n[bold cyan]Checking Tailwind CSS Plus authentication...[/bold cyan]")
    client, status = create_authenticated_client()

    if status.is_authenticated:
        console.print(f"[bold green][OK] Authenticated successfully![/bold green]")
        if status.user_email:
            console.print(f"Account: [cyan]{status.user_email}[/cyan]")
        console.print(f"License: [green]{'Full Access Active' if status.has_full_license else 'Partial/Preview'}[/green]")
    else:
        console.print(f"[bold red][!] {status.details}[/bold red]")
        console.print("\n[yellow]To authenticate, open [.env] and set either:[/yellow]")
        console.print('  [bold]TAILWIND_SESSION="<your_session_cookie>"[/bold] (from browser cookies)')
        console.print("  OR")
        console.print('  [bold]TAILWIND_EMAIL="<email>"[/bold] and [bold]TAILWIND_PASSWORD="<password>"[/bold]\n')


@app.command()
def list_catalog() -> None:
    """List all categories, subcategories, and templates available on Tailwind Plus."""
    client, _ = create_authenticated_client()
    tp_client = TailwindPlusClient(client)

    with console.status("[bold green]Fetching Tailwind Plus taxonomy..."):
        subcategories, templates = tp_client.get_taxonomy()

    table = Table(title="Tailwind Plus Subcategories Catalog", show_lines=True)
    table.add_column("Product", style="cyan", no_wrap=True)
    table.add_column("Category", style="magenta")
    table.add_column("Subcategory", style="green")
    table.add_column("Components", justify="right", style="yellow")

    for sub in subcategories:
        table.add_row(sub.product, sub.category, sub.name, str(sub.component_count or "-"))

    console.print(table)
    console.print(f"\nTotal subcategories: [bold]{len(subcategories)}[/bold]")
    console.print(f"Total standalone templates: [bold]{len(templates)}[/bold]\n")


@app.command()
def scrape(
    formats: str = typer.Option(
        "html,react,vue",
        "--formats",
        "-f",
        help="Comma-separated component formats: html, react, vue",
    ),
    templates: bool = typer.Option(
        True,
        "--templates/--no-templates",
        help="Include full standalone website templates / kits",
    ),
    product: Optional[str] = typer.Option(
        None,
        "--product",
        "-p",
        help="Filter by product: marketing, application-ui, ecommerce",
    ),
    output: Path = typer.Option(
        Path("scraped_components"),
        "--output",
        "-o",
        help="Destination directory for scraped components",
    ),
    limit: Optional[int] = typer.Option(
        None,
        "--limit",
        "-l",
        help="Limit number of components (useful for test runs)",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force re-download of already completed components",
    ),
) -> None:
    """Scrape all Tailwind CSS Plus components and templates to disk."""
    client, status = create_authenticated_client()

    if not status.is_authenticated:
        console.print(
            "[bold yellow]Warning:[/bold yellow] No authenticated session detected in [.env]. "
            "Only free/preview components will include source code. "
            "Add [bold]TAILWIND_SESSION[/bold] in .env to scrape all licensed components."
        )

    format_list = [fmt.strip().lower() for fmt in formats.split(",") if fmt.strip()]
    storage = ComponentStorage(base_dir=output)
    tp_client = TailwindPlusClient(client)

    scraper = TailwindPlusScraper(
        client=tp_client,
        storage=storage,
        formats=format_list,
        include_templates=templates,
    )
    scraper.run(product_filter=product, limit=limit, force=force)


@app.command()
def search(query: str, manifest: Path = Path("scraped_components/manifest.json")) -> None:
    """Search locally scraped components by name, category, or subcategory."""
    if not manifest.exists():
        console.print(f"[red]Manifest file not found at {manifest}. Run scrape first.[/red]")
        raise typer.Exit(1)

    with open(manifest, "r", encoding="utf-8") as f:
        data = json.load(f)

    q = query.lower()
    matches = []
    for c in data.get("components", []):
        if (
            q in c.get("name", "").lower()
            or q in c.get("category", "").lower()
            or q in c.get("subcategory", "").lower()
            or q in c.get("product", "").lower()
        ):
            matches.append(c)

    table = Table(title=f"Search Results for '{query}' ({len(matches)} found)")
    table.add_column("Product", style="cyan")
    table.add_column("Category > Subcategory", style="magenta")
    table.add_column("Component Name", style="bold green")
    table.add_column("Formats", style="yellow")

    for m in matches[:50]:
        fmts = ", ".join(m.get("snippets", {}).keys()) or "None"
        table.add_row(
            m.get("product", ""),
            f"{m.get('category', '')} > {m.get('subcategory', '')}",
            m.get("name", ""),
            fmts,
        )

    console.print(table)


@app.command()
def mcp() -> None:
    """Start the Model Context Protocol (MCP) server for Tailwind Plus over stdio."""
    from .mcp_server import main as run_mcp
    run_mcp()


@app.command("download-screens")
def download_screens(
    force: bool = typer.Option(False, "--force", "-f", help="Re-download images even if already cached"),
    workers: int = typer.Option(12, "--workers", "-w", help="Number of concurrent download threads"),
) -> None:
    """Download all high-resolution template screenshots and preview screens locally."""
    from .screens import sync_template_screens
    storage = ComponentStorage()
    count = sync_template_screens(storage.base_dir, force=force, max_workers=workers)
    storage.rebuild_manifest_from_disk()
    console.print(f"[bold green][OK] Successfully linked {count} template screens across all templates![/bold green]")
    console.print(f"Screens location: [cyan]{storage.base_dir / 'templates' / 'screens'}[/cyan]")


@app.command("rebuild-manifest")
def rebuild_manifest() -> None:
    """Scan scraped_components directory and refresh master manifest.json."""
    storage = ComponentStorage()
    with console.status("[bold green]Scanning scraped_components on disk..."):
        p = storage.rebuild_manifest_from_disk()
        m = storage.load_manifest()
    count = m.total_components if m else 0
    tpl_count = m.total_templates if m else 0
    console.print(f"[bold green][OK] Manifest rebuilt successfully at {p}![/bold green]")
    console.print(f"Total components: [bold]{count}[/bold] | Templates: [bold]{tpl_count}[/bold]")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
