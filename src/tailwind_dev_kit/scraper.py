from __future__ import annotations

import time
import json
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)

from .client import TailwindPlusClient
from .storage import ComponentStorage
from .models import Component, Template, Snippet

console = Console(legacy_windows=False)


class TailwindPlusScraper:
    def __init__(
        self,
        client: TailwindPlusClient,
        storage: Optional[ComponentStorage] = None,
        formats: Optional[List[str]] = None,
        include_templates: bool = True,
        rate_limit_delay: float = 0.1,
    ):
        self.client = client
        self.storage = storage or ComponentStorage()
        self.formats = formats or ["html", "react", "vue"]
        self.include_templates = include_templates
        self.rate_limit_delay = rate_limit_delay

    def run(
        self,
        product_filter: Optional[str] = None,
        limit: Optional[int] = None,
        force: bool = False,
    ) -> None:
        """Run the end-to-end scraper with rich progress monitoring."""
        console.print("\n[bold cyan]=== Tailwind CSS Plus / UI Component Scraper ===[/bold cyan]\n")
        
        progress_data = self.storage.load_progress()
        if force:
            progress_data = {"completed_components": [], "completed_templates": []}

        # Step 1: Discover Taxonomy
        with console.status("[bold green]Discovering taxonomy and templates from Tailwind Plus..."):
            subcategories, templates = self.client.get_taxonomy()

        console.print(f"Discovered [bold]{len(subcategories)}[/bold] subcategories and [bold]{len(templates)}[/bold] templates.")

        if product_filter:
            subcategories = [s for s in subcategories if product_filter.lower() in s.product.lower()]
            console.print(f"Filtered to [bold]{len(subcategories)}[/bold] subcategories for product '{product_filter}'.")

        all_scraped_components: List[Component] = []
        components_scraped_count = 0

        # Step 2: Scrape UI Blocks / Components
        with Progress(
            SpinnerColumn("line"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as prog:
            subcat_task = prog.add_task("[yellow]Scraping subcategories...", total=len(subcategories))

            for subcat in subcategories:
                prog.update(subcat_task, description=f"[yellow]{subcat.product} > {subcat.name}")

                try:
                    components = self.client.get_subcategory_components(subcat)
                except Exception as e:
                    console.print(f"[red]Failed to fetch subcategory {subcat.name}: {e}[/red]")
                    prog.advance(subcat_task)
                    continue

                for idx, comp in enumerate(components, start=1):
                    if limit and components_scraped_count >= limit:
                        break

                    # Check if component was already scraped with all requested formats
                    if not force and self.storage.is_component_completed(comp, idx, self.formats, progress_data):
                        self.storage.load_existing_snippets(comp, index=idx)
                        all_scraped_components.append(comp)
                        continue

                    # Pre-load whatever formats already exist on disk
                    self.storage.load_existing_snippets(comp, index=idx)

                    # Fetch requested language formats (HTML, React, Vue)
                    for fmt in self.formats:
                        # If the snippet is already populated with code for this format, keep it
                        if fmt in comp.snippets and comp.snippets[fmt].code:
                            continue

                        try:
                            code = self.client.fetch_snippet_variant(comp, language=fmt)
                            if code:
                                comp.snippets[fmt] = Snippet(
                                    name=fmt,
                                    language="jsx" if fmt == "react" else fmt,
                                    version="4.3",
                                    code=code,
                                )
                            time.sleep(self.rate_limit_delay)
                        except Exception as e:
                            # Non-fatal: continue with remaining formats
                            pass

                    # Persist component to disk
                    self.storage.save_component(comp, index=idx)
                    self.storage.mark_component_completed(comp.id, progress_data)
                    all_scraped_components.append(comp)
                    components_scraped_count += 1

                prog.advance(subcat_task)
                if limit and components_scraped_count >= limit:
                    console.print(f"[yellow]Reached limit of {limit} components.[/yellow]")
                    break

        # Step 3: Download Standalone Templates (if enabled)
        if self.include_templates and templates:
            console.print("\n[bold cyan]=== Downloading Standalone Website Templates ===[/bold cyan]")
            tpl_dir = self.storage.get_templates_dir()

            with Progress(
                SpinnerColumn("line"),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console,
            ) as prog:
                tpl_task = prog.add_task("[green]Downloading templates...", total=len(templates))

                for tpl in templates:
                    prog.update(tpl_task, description=f"[green]Template: {tpl.name}")
                    dest_zip = tpl_dir / f"{tpl.slug}.zip"
                    dest_json = tpl_dir / f"{tpl.slug}.json"

                    # Save metadata
                    with open(dest_json, "w", encoding="utf-8") as f:
                        json.dump(tpl.model_dump(), f, indent=2)

                    if not force and self.storage.is_template_completed(tpl.slug, progress_data):
                        prog.advance(tpl_task)
                        continue

                    if tpl.download_url:
                        try:
                            success = self.client.download_template_archive(tpl.download_url, dest_zip)
                            if success:
                                self.storage.mark_template_completed(tpl.slug, progress_data)
                            time.sleep(self.rate_limit_delay)
                        except Exception as e:
                            console.print(f"[red]Failed downloading template {tpl.name}: {e}[/red]")

                    prog.advance(tpl_task)

        # Step 4: Write Master Manifest
        manifest_file = self.storage.save_manifest(all_scraped_components, templates)
        console.print(f"\n[bold green][OK] Scraping Complete![/bold green]")
        console.print(f"Total components indexed: [bold]{len(all_scraped_components)}[/bold]")
        console.print(f"Master manifest generated at: [underline]{manifest_file}[/underline]\n")
