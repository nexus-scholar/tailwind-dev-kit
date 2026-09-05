import json
import time
from pathlib import Path
from tailwind_dev_kit.auth import create_authenticated_client
from tailwind_dev_kit.client import TailwindPlusClient, slugify

client, _ = create_authenticated_client()
tp = TailwindPlusClient(client)

templates_to_fetch = [
    ("Catalyst", "catalyst", "https://tailwindcss.com/plus/ui-kit"),
    ("Oatmeal", "oatmeal", "https://tailwindcss.com/plus/kits/oatmeal"),
    ("Radiant", "radiant", "https://tailwindcss.com/plus/templates/radiant"),
    ("Salient", "salient", "https://tailwindcss.com/plus/templates/salient"),
    ("Spotlight", "spotlight", "https://tailwindcss.com/plus/templates/spotlight"),
    ("Studio", "studio", "https://tailwindcss.com/plus/templates/studio"),
    ("Primer", "primer", "https://tailwindcss.com/plus/templates/primer"),
    ("Protocol", "protocol", "https://tailwindcss.com/plus/templates/protocol"),
    ("Commit", "commit", "https://tailwindcss.com/plus/templates/commit"),
    ("Transmit", "transmit", "https://tailwindcss.com/plus/templates/transmit"),
    ("Pocket", "pocket", "https://tailwindcss.com/plus/templates/pocket"),
    ("Syntax", "syntax", "https://tailwindcss.com/plus/templates/syntax"),
    ("Keynote", "keynote", "https://tailwindcss.com/plus/templates/keynote"),
    ("Compass", "compass", "https://tailwindcss.com/plus/templates/compass"),
]

tpl_dir = Path("scraped_components/templates")
results = {}

for name, slug, url in templates_to_fetch:
    print(f"Fetching details for {name} ({slug}) from {url}...")
    try:
        data = tp.get_inertia(url)
        props = data.get("props", {})
        prod = props.get("product") or props.get("template") or {}

        # Preserve existing metadata (e.g. Oatmeal themes, Catalyst components)
        dest_json = tpl_dir / f"{slug}.json"
        existing = {}
        if dest_json.exists():
            try:
                with open(dest_json, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                pass

        technologies = prod.get("technologies") or []
        tech_list = [f"{t.get('name')} {t.get('version', '')}".strip() for t in technologies] if isinstance(technologies, list) and technologies and isinstance(technologies[0], dict) else technologies

        zip_file = tpl_dir / f"{slug}.zip"
        zip_size_kb = (zip_file.stat().st_size // 1024) if zip_file.exists() else 0

        # Build enriched object
        merged = {
            **existing,
            "name": name,
            "slug": slug,
            "type": prod.get("type") or existing.get("type") or "Website Template",
            "summary": prod.get("summary") or existing.get("summary"),
            "description": prod.get("description") or existing.get("description"),
            "technologies": technologies if technologies else existing.get("technologies", []),
            "technologies_summary": tech_list,
            "url": url,
            "demo_preview_url": prod.get("preview_url") or existing.get("preview_url"),
            "download_url": prod.get("download_url") or existing.get("download_url"),
            "local_archive": str(zip_file),
            "archive_size_kb": zip_size_kb,
            "banner_image_url": prod.get("banner_image_url"),
            "screenshots": [img.get("url") for img in prod.get("images", []) if isinstance(img, dict) and img.get("url")],
        }

        # Catalyst specific additions
        if slug == "catalyst":
            cat_extracted = Path("scraped_components/ui-kit/catalyst")
            if cat_extracted.exists():
                comps = sorted([p.stem for p in (cat_extracted / "typescript").glob("*.tsx")])
                merged["total_components"] = len(comps)
                merged["components"] = comps
                merged["directories"] = {
                    "typescript": "scraped_components/ui-kit/catalyst/typescript",
                    "javascript": "scraped_components/ui-kit/catalyst/javascript",
                    "demo": "scraped_components/ui-kit/catalyst/demo",
                }
                merged["documentation_url"] = "https://catalyst.tailwindui.com/docs"

        # Oatmeal specific additions
        if slug == "oatmeal":
            merged["themes_dir"] = "scraped_components/templates/oatmeal-themes"
            merged["total_themes"] = 12

        with open(dest_json, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2)

        results[slug] = merged
        print(f"[OK] {name}: summary='{merged.get('summary')[:50] if merged.get('summary') else 'None'}...', tech={tech_list}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
    time.sleep(0.2)

print(f"\nEnriched {len(results)} templates successfully!")
