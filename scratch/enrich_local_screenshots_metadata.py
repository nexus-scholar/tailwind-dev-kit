import json
from pathlib import Path

def main():
    root = Path.cwd()
    tpl_dir = root / "scraped_components" / "templates"
    screens_base = tpl_dir / "screens"

    for tpl_json in sorted(tpl_dir.glob("*.json")):
        slug = tpl_json.stem
        with open(tpl_json, "r", encoding="utf-8") as f:
            tdata = json.load(f)

        screens_dir = screens_base / slug
        if not screens_dir.exists():
            continue

        # All local image files
        local_files = sorted([
            str(p.relative_to(root)).replace("\\", "/")
            for p in screens_dir.rglob("*")
            if p.is_file() and p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".svg"]
        ])

        # Pick best banner image
        banner = None
        for cand in ["screenshot.png", "preview-01.png", "detail-01.png"]:
            matched = [f for f in local_files if f.endswith(cand)]
            if matched:
                banner = matched[0]
                break
        if not banner and local_files:
            banner = local_files[0]

        tdata["local_screens_dir"] = str(screens_dir.relative_to(root)).replace("\\", "/")
        tdata["local_banner_image"] = banner
        tdata["local_screenshots"] = local_files

        # Oatmeal rich theme enrichment
        if slug == "oatmeal" and "themes" in tdata:
            for th in tdata["themes"]:
                th_slug = th.get("slug")
                th_dir = screens_dir / "themes" / th_slug
                if th_dir.exists():
                    th_files = sorted([
                        str(p.relative_to(root)).replace("\\", "/")
                        for p in th_dir.rglob("*")
                        if p.is_file() and p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".svg"]
                    ])
                    th["local_screens_dir"] = str(th_dir.relative_to(root)).replace("\\", "/")
                    th["local_screenshots"] = th_files
                    light_thumb = th_dir / "thumbnail-light.png"
                    dark_thumb = th_dir / "thumbnail-dark.png"
                    if light_thumb.exists():
                        th["local_thumbnail_light"] = str(light_thumb.relative_to(root)).replace("\\", "/")
                    if dark_thumb.exists():
                        th["local_thumbnail_dark"] = str(dark_thumb.relative_to(root)).replace("\\", "/")

        with open(tpl_json, "w", encoding="utf-8") as f:
            json.dump(tdata, f, indent=2)

        print(f"[OK] {tdata.get('name', slug)}: {len(local_files)} screens linked ({tdata.get('local_screens_dir')})")

if __name__ == "__main__":
    main()
