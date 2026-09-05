from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Any, Optional

import httpx
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
from rich.table import Table

console = Console(legacy_windows=False)


def _download_single_screen(task: dict, client: httpx.Client, force: bool = False) -> dict:
    url = task["url"]
    target = Path(task["target"])

    if not force and target.exists() and target.stat().st_size > 0:
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


def sync_template_screens(
    base_dir: Path,
    force: bool = False,
    max_workers: int = 12,
) -> int:
    """
    Download and link high-resolution template screenshots and preview screens locally.
    """
    from .auth import create_authenticated_client
    from .client import TailwindPlusClient

    tpl_dir = base_dir / "templates"
    screens_base = tpl_dir / "screens"
    screens_base.mkdir(parents=True, exist_ok=True)

    client, _ = create_authenticated_client()
    tp = TailwindPlusClient(client)

    # 1. Fetch index previews
    index_previews: Dict[str, List[str]] = {}
    try:
        data = tp.get_inertia("https://tailwindcss.com/plus/templates")
        for p in data.get("props", {}).get("products", []):
            name = (p.get("name") or "").lower()
            imgs = [img["url"] for img in p.get("images", []) if isinstance(img, dict) and img.get("url")]
            index_previews[name] = imgs
    except Exception:
        pass

    template_defs = [
        ("catalyst", "https://tailwindcss.com/plus/ui-kit"),
        ("oatmeal", "https://tailwindcss.com/plus/kits/oatmeal"),
        ("radiant", "https://tailwindcss.com/plus/templates/radiant"),
        ("salient", "https://tailwindcss.com/plus/templates/salient"),
        ("spotlight", "https://tailwindcss.com/plus/templates/spotlight"),
        ("studio", "https://tailwindcss.com/plus/templates/studio"),
        ("primer", "https://tailwindcss.com/plus/templates/primer"),
        ("protocol", "https://tailwindcss.com/plus/templates/protocol"),
        ("commit", "https://tailwindcss.com/plus/templates/commit"),
        ("transmit", "https://tailwindcss.com/plus/templates/transmit"),
        ("pocket", "https://tailwindcss.com/plus/templates/pocket"),
        ("syntax", "https://tailwindcss.com/plus/templates/syntax"),
        ("keynote", "https://tailwindcss.com/plus/templates/keynote"),
        ("compass", "https://tailwindcss.com/plus/templates/compass"),
    ]

    tasks: List[dict] = []
    for slug, url in template_defs:
        try:
            tdata = tp.get_inertia(url)
            props = tdata.get("props", {})
            prod = props.get("product") or props.get("template") or {}
        except Exception:
            continue

        s_dir = screens_base / slug

        for p_url in index_previews.get(slug, []):
            fname = p_url.split("/")[-1]
            tasks.append({"template": slug, "url": p_url, "target": str(s_dir / fname)})

        if prod.get("banner_image_url"):
            b_url = prod["banner_image_url"]
            tasks.append({"template": slug, "url": b_url, "target": str(s_dir / b_url.split("/")[-1])})

        if prod.get("twitter_image_url"):
            t_url = prod["twitter_image_url"]
            tasks.append({"template": slug, "url": t_url, "target": str(s_dir / t_url.split("/")[-1])})

        for img in prod.get("images", []):
            if isinstance(img, dict) and img.get("url"):
                i_url = img["url"]
                if any(i_url.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg"]):
                    tasks.append({"template": slug, "url": i_url, "target": str(s_dir / i_url.split("/")[-1])})

        if slug == "oatmeal":
            for th in prod.get("themes", []):
                th_slug = th.get("slug") or th.get("name", "").lower().replace(" ", "_")
                th_dir = s_dir / "themes" / th_slug
                if th.get("thumbnail_url"):
                    tasks.append({"template": slug, "url": th["thumbnail_url"], "target": str(th_dir / "thumbnail-light.png")})
                if th.get("thumbnail_dark_url"):
                    tasks.append({"template": slug, "url": th["thumbnail_dark_url"], "target": str(th_dir / "thumbnail-dark.png")})
                for sc in th.get("screenshots", []):
                    for k, v in sc.items():
                        if isinstance(v, dict):
                            if v.get("light"):
                                tasks.append({"template": slug, "url": v["light"], "target": str(th_dir / f"{k}-light.png")})
                            if v.get("dark"):
                                tasks.append({"template": slug, "url": v["dark"], "target": str(th_dir / f"{k}-dark.png")})

    # Deduplicate
    unique_tasks = {t["target"]: t for t in tasks}
    task_list = list(unique_tasks.values())

    console.print(f"[bold cyan]Syncing {len(task_list)} template screens locally...[/bold cyan]")
    headers = {"User-Agent": "Mozilla/5.0"}
    with httpx.Client(headers=headers, follow_redirects=True) as http_client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            prog_task = progress.add_task("Downloading screens...", total=len(task_list))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(_download_single_screen, t, http_client, force): t for t in task_list}
                for f in as_completed(futures):
                    progress.advance(prog_task)

    # Link into JSON metadata
    root = Path.cwd()
    linked_total = 0
    for tpl_json in sorted(tpl_dir.glob("*.json")):
        slug = tpl_json.stem
        try:
            with open(tpl_json, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception:
            continue

        s_dir = screens_base / slug
        if not s_dir.exists():
            continue

        local_files = sorted([
            str(p.resolve().relative_to(root.resolve())).replace("\\", "/")
            for p in s_dir.rglob("*")
            if p.is_file() and p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".svg"]
        ])

        banner = None
        for cand in ["screenshot.png", "preview-01.png", "detail-01.png"]:
            matched = [f for f in local_files if f.endswith(cand)]
            if matched:
                banner = matched[0]
                break
        if not banner and local_files:
            banner = local_files[0]

        meta["local_screens_dir"] = str(s_dir.resolve().relative_to(root.resolve())).replace("\\", "/")
        meta["local_banner_image"] = banner
        meta["local_screenshots"] = local_files

        if slug == "oatmeal" and "themes" in meta:
            for th in meta["themes"]:
                th_slug = th.get("slug")
                th_dir = s_dir / "themes" / th_slug
                if th_dir.exists():
                    th_files = sorted([
                        str(p.resolve().relative_to(root.resolve())).replace("\\", "/")
                        for p in th_dir.rglob("*")
                        if p.is_file() and p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".svg"]
                    ])
                    th["local_screens_dir"] = str(th_dir.resolve().relative_to(root.resolve())).replace("\\", "/")
                    th["local_screenshots"] = th_files
                    light_thumb = th_dir / "thumbnail-light.png"
                    dark_thumb = th_dir / "thumbnail-dark.png"
                    if light_thumb.exists():
                        th["local_thumbnail_light"] = str(light_thumb.resolve().relative_to(root.resolve())).replace("\\", "/")
                    if dark_thumb.exists():
                        th["local_thumbnail_dark"] = str(dark_thumb.resolve().relative_to(root.resolve())).replace("\\", "/")

        with open(tpl_json, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        linked_total += len(local_files)

    return linked_total
