import re
import json
from pathlib import Path
from tailwind_dev_kit.auth import create_authenticated_client
from tailwind_dev_kit.client import TailwindPlusClient

c, _ = create_authenticated_client()
tp = TailwindPlusClient(c)

# 1. Fetch /plus/templates index for preview-01/02/03
templates_index = tp.get_inertia("https://tailwindcss.com/plus/templates")
index_products = templates_index.get("props", {}).get("products", [])

preview_imgs_by_name = {}
for p in index_products:
    name = p.get("name")
    imgs = [img["url"] for img in p.get("images", []) if isinstance(img, dict) and img.get("url")]
    preview_imgs_by_name[name.lower()] = imgs

# 2. Standalone templates + Catalyst + Oatmeal
template_definitions = [
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

download_tasks = []

for name, slug, url in template_definitions:
    data = tp.get_inertia(url)
    props = data.get("props", {})
    prod = props.get("product") or props.get("template") or {}

    screens_dir = Path("scraped_components/templates/screens") / slug

    # Add index preview images (preview-01.png, preview-02.png, preview-03.png)
    for p_url in preview_imgs_by_name.get(slug, []) or preview_imgs_by_name.get(name.lower(), []):
        filename = p_url.split("/")[-1]
        download_tasks.append({
            "template": slug,
            "url": p_url,
            "target": str(screens_dir / filename),
            "category": "preview"
        })

    # Banner image
    if prod.get("banner_image_url"):
        b_url = prod["banner_image_url"]
        fname = b_url.split("/")[-1]
        download_tasks.append({
            "template": slug,
            "url": b_url,
            "target": str(screens_dir / fname),
            "category": "banner"
        })

    # Twitter image
    if prod.get("twitter_image_url"):
        t_url = prod["twitter_image_url"]
        fname = t_url.split("/")[-1]
        download_tasks.append({
            "template": slug,
            "url": t_url,
            "target": str(screens_dir / fname),
            "category": "twitter"
        })

    # Detail screenshots
    for img in prod.get("images", []):
        if isinstance(img, dict) and img.get("url"):
            i_url = img["url"]
            if any(i_url.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg"]):
                fname = i_url.split("/")[-1]
                download_tasks.append({
                    "template": slug,
                    "url": i_url,
                    "target": str(screens_dir / fname),
                    "category": "detail"
                })

    # Oatmeal rich themes
    if slug == "oatmeal":
        for th in prod.get("themes", []):
            th_slug = th.get("slug") or th.get("name", "").lower().replace(" ", "_")
            th_dir = screens_dir / "themes" / th_slug
            
            if th.get("thumbnail_url"):
                download_tasks.append({
                    "template": slug,
                    "url": th["thumbnail_url"],
                    "target": str(th_dir / "thumbnail-light.png"),
                    "category": "theme_thumbnail"
                })
            if th.get("thumbnail_dark_url"):
                download_tasks.append({
                    "template": slug,
                    "url": th["thumbnail_dark_url"],
                    "target": str(th_dir / "thumbnail-dark.png"),
                    "category": "theme_thumbnail"
                })

            for sc in th.get("screenshots", []):
                for screen_key, variants in sc.items():
                    if isinstance(variants, dict):
                        if variants.get("light"):
                            download_tasks.append({
                                "template": slug,
                                "url": variants["light"],
                                "target": str(th_dir / f"{screen_key}-light.png"),
                                "category": "theme_screenshot"
                            })
                        if variants.get("dark"):
                            download_tasks.append({
                                "template": slug,
                                "url": variants["dark"],
                                "target": str(th_dir / f"{screen_key}-dark.png"),
                                "category": "theme_screenshot"
                            })

# Deduplicate tasks by target path
unique_tasks = {}
for task in download_tasks:
    unique_tasks[task["target"]] = task

tasks_list = list(unique_tasks.values())
print(f"Total unique download tasks: {len(tasks_list)}")

# Summary by template
counts = {}
for t in tasks_list:
    slug = t["template"]
    counts[slug] = counts.get(slug, 0) + 1

for slug, c in sorted(counts.items()):
    print(f"  {slug}: {c} screens/images")

with open("scratch/image_download_tasks.json", "w", encoding="utf-8") as f:
    json.dump(tasks_list, f, indent=2)
