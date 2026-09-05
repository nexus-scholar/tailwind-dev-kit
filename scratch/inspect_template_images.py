import json
from pathlib import Path

p = Path('scraped_components/templates')
jsons = sorted(list(p.glob('*.json')))
all_imgs = {}

for j in jsons:
    d = json.load(open(j, encoding='utf-8'))
    imgs = []
    if d.get('banner_image_url'):
        imgs.append(d['banner_image_url'])
    if d.get('preview_url'):
        imgs.append(d['preview_url'])
    for s in d.get('screenshots', []):
        if s: imgs.append(s)
    for img in d.get('images', []):
        if isinstance(img, dict) and img.get('url'):
            imgs.append(img['url'])
        elif isinstance(img, str):
            imgs.append(img)
    for th in d.get('themes', []):
        if th.get('thumbnail_light'): imgs.append(th['thumbnail_light'])
        if th.get('thumbnail_dark'): imgs.append(th['thumbnail_dark'])
    slug = d.get('slug')
    all_imgs[slug] = sorted(list(set(imgs)))
    print(f"{d.get('name', slug)} ({slug}): {len(all_imgs[slug])} images")

total = sum(len(v) for v in all_imgs.values())
print(f"\nTotal images across all templates: {total}")
