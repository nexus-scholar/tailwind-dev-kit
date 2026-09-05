import os
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import httpx
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
from rich.table import Table

console = Console(legacy_windows=False)

def download_file(task: dict, client: httpx.Client) -> dict:
    url = task["url"]
    target = Path(task["target"])
    
    # If already exists and has nonzero size, skip
    if target.exists() and target.stat().st_size > 0:
        return {"success": True, "status": "cached", "task": task, "size": target.stat().st_size}

    target.parent.mkdir(parents=True, exist_ok=True)
    temp_target = target.with_suffix(target.suffix + ".tmp")
    
    for attempt in range(3):
        try:
            with client.stream("GET", url, timeout=30.0, follow_redirects=True) as resp:
                if resp.status_code == 200:
                    with open(temp_target, "wb") as f:
                        for chunk in resp.iter_bytes(chunk_size=16384):
                            f.write(chunk)
                    if temp_target.stat().st_size > 0:
                        temp_target.replace(target)
                        return {"success": True, "status": "downloaded", "task": task, "size": target.stat().st_size}
                else:
                    time.sleep(1)
        except Exception as e:
            if attempt == 2:
                if temp_target.exists():
                    temp_target.unlink()
                return {"success": False, "status": "error", "error": str(e), "task": task, "size": 0}
            time.sleep(1)
            
    if temp_target.exists():
        temp_target.unlink()
    return {"success": False, "status": "failed", "task": task, "size": 0}


def main():
    console.print("\n[bold cyan]=== Tailwind CSS Plus: Template Screen & Image Downloader ===[/bold cyan]")
    
    tasks_path = Path("scratch/image_download_tasks.json")
    if not tasks_path.exists():
        console.print("[red]Tasks file scratch/image_download_tasks.json not found![/red]")
        return
        
    with open(tasks_path, "r", encoding="utf-8") as f:
        tasks = json.load(f)
        
    console.print(f"Loaded [bold green]{len(tasks)}[/bold green] image download targets across 14 templates.\n")

    total_downloaded = 0
    total_cached = 0
    total_failed = 0
    total_bytes = 0

    results_by_template = {}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    with httpx.Client(headers=headers, follow_redirects=True) as client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            prog_task = progress.add_task("[cyan]Downloading template screens...", total=len(tasks))
            
            with ThreadPoolExecutor(max_workers=12) as executor:
                futures = {executor.submit(download_file, t, client): t for t in tasks}
                
                for future in as_completed(futures):
                    res = future.result()
                    task = res["task"]
                    slug = task["template"]
                    
                    if slug not in results_by_template:
                        results_by_template[slug] = []
                    results_by_template[slug].append(res)
                    
                    if res["success"]:
                        if res["status"] == "downloaded":
                            total_downloaded += 1
                        else:
                            total_cached += 1
                        total_bytes += res["size"]
                    else:
                        total_failed += 1
                        console.print(f"[yellow]Failed {task['url']}: {res.get('error')}[/yellow]")
                        
                    progress.advance(prog_task)

    console.print(f"\n[bold green]Download Phase Complete![/bold green]")
    console.print(f"Downloaded: [bold]{total_downloaded}[/bold] | Cached: [bold]{total_cached}[/bold] | Failed: [bold]{total_failed}[/bold]")
    console.print(f"Total Size on Disk: [bold cyan]{total_bytes / (1024 * 1024):.2f} MB[/bold cyan]\n")

    # Update template JSON files with local screenshots
    tpl_dir = Path("scraped_components/templates")
    
    summary_table = Table(title="Downloaded Template Screens Summary", show_lines=True)
    summary_table.add_column("Template", style="bold cyan")
    summary_table.add_column("Screens Directory", style="green")
    summary_table.add_column("Screens Count", justify="right", style="yellow")
    summary_table.add_column("Size (MB)", justify="right", style="magenta")

    for tpl_json in sorted(tpl_dir.glob("*.json")):
        slug = tpl_json.stem
        try:
            with open(tpl_json, "r", encoding="utf-8") as f:
                tdata = json.load(f)
        except Exception:
            continue
            
        screens_dir = tpl_dir / "screens" / slug
        if not screens_dir.exists():
            continue
            
        # Collect all downloaded image files in screens_dir
        local_files = sorted([
            str(p.relative_to(Path.cwd())) 
            for p in screens_dir.rglob("*") 
            if p.is_file() and p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".svg"]
        ])
        
        screens_size = sum(Path(p).stat().st_size for p in local_files if Path(p).exists())
        
        # Determine local banner
        banner_candidates = [p for p in local_files if "screenshot.png" in p.lower() or "banner" in p.lower()]
        local_banner = banner_candidates[0] if banner_candidates else (local_files[0] if local_files else None)
        
        tdata["local_screens_dir"] = str(screens_dir.relative_to(Path.cwd()))
        tdata["local_banner_image"] = local_banner
        tdata["local_screenshots"] = local_files
        
        # For Oatmeal, enrich theme local screenshot references
        if slug == "oatmeal" and "themes" in tdata:
            for th in tdata["themes"]:
                th_slug = th.get("slug")
                th_dir = screens_dir / "themes" / th_slug
                if th_dir.exists():
                    th_files = sorted([
                        str(p.relative_to(Path.cwd()))
                        for p in th_dir.rglob("*")
                        if p.is_file() and p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".svg"]
                    ])
                    th["local_screens_dir"] = str(th_dir.relative_to(Path.cwd()))
                    th["local_screenshots"] = th_files
                    light_thumb = th_dir / "thumbnail-light.png"
                    dark_thumb = th_dir / "thumbnail-dark.png"
                    if light_thumb.exists():
                        th["local_thumbnail_light"] = str(light_thumb.relative_to(Path.cwd()))
                    if dark_thumb.exists():
                        th["local_thumbnail_dark"] = str(dark_thumb.relative_to(Path.cwd()))

        with open(tpl_json, "w", encoding="utf-8") as f:
            json.dump(tdata, f, indent=2)
            
        summary_table.add_row(
            tdata.get("name", slug),
            str(screens_dir.relative_to(Path.cwd())),
            str(len(local_files)),
            f"{screens_size / (1024 * 1024):.2f}"
        )

    console.print(summary_table)

if __name__ == "__main__":
    main()
