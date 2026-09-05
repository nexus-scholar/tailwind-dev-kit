import json
from pathlib import Path
from tailwind_dev_kit.auth import create_authenticated_client
from tailwind_dev_kit.client import TailwindPlusClient

client, _ = create_authenticated_client()
tp = TailwindPlusClient(client)

templates = [
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

all_images_by_template = {}

for name, slug, url in templates:
    data = tp.get_inertia(url)
    props = data.get("props", {})
    prod = props.get("product") or props.get("template") or {}
    
    urls = set()
    if prod.get("banner_image_url"):
        urls.add(prod["banner_image_url"])
    if prod.get("twitter_image_url"):
        urls.add(prod["twitter_image_url"])
    if prod.get("preview_url"):
        urls.add(prod["preview_url"])

    for img in prod.get("images", []):
        if isinstance(img, dict) and img.get("url"):
            urls.add(img["url"])

    # Oatmeal rich themes
    for th in prod.get("themes", []):
        if th.get("thumbnail_url"):
            urls.add(th["thumbnail_url"])
        if th.get("thumbnail_dark_url"):
            urls.add(th["thumbnail_dark_url"])
        for sc in th.get("screenshots", []):
            for k, v in sc.items():
                if isinstance(v, dict):
                    if v.get("light"): urls.add(v["light"])
                    if v.get("dark"): urls.add(v["dark"])

    all_images_by_template[slug] = sorted(list(urls))
    print(f"{name} ({slug}): {len(urls)} image URLs found")

total_urls = sum(len(v) for v in all_images_by_template.values())
print(f"\nTotal image URLs collected: {total_urls}")

with open("scratch/all_template_images.json", "w", encoding="utf-8") as f:
    json.dump(all_images_by_template, f, indent=2)
