import json
from tailwind_dev_kit.auth import create_authenticated_client
from tailwind_dev_kit.client import TailwindPlusClient

client, _ = create_authenticated_client()
tp = TailwindPlusClient(client)
d = tp.get_inertia('https://tailwindcss.com/plus/kits/oatmeal')
p = d.get('props', {}).get('product', {})

themes_summary = []
for t in p.get('themes', []):
    slug = t.get('slug')
    hyphenated = slug.replace('_', '-')
    zip_name = f"oatmeal-{hyphenated}.zip"
    zip_path = f"scraped_components/templates/oatmeal-themes/{zip_name}"
    themes_summary.append({
        'name': t.get('name'),
        'slug': slug,
        'color': t.get('styles', {}).get('color', {}).get('title'),
        'font': t.get('styles', {}).get('font', {}).get('title'),
        'thumbnail_light': t.get('thumbnail_url'),
        'thumbnail_dark': t.get('thumbnail_dark_url'),
        'local_archive': zip_path,
        'download_url': f"https://tailwindcss.com/plus/templates/oatmeal/download?theme={slug}",
    })

meta = {
    'id': 8,
    'name': 'Oatmeal',
    'slug': 'oatmeal',
    'type': 'SaaS marketing kit',
    'url': 'https://tailwindcss.com/plus/kits/oatmeal',
    'default_download_url': 'https://tailwindcss.com/plus/templates/oatmeal/download?theme=olive_instrument',
    'summary': p.get('summary') or 'SaaS marketing kit with 12 theme combinations across 4 color palettes (Mauve, Mist, Olive, Taupe) and 3 typography styles (Familjen, Instrument, Mona).',
    'total_themes': len(themes_summary),
    'themes': themes_summary,
    'categories': p.get('categories', []),
    'total_components': len(p.get('components', [])),
}

with open('scraped_components/templates/oatmeal.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2)

print('Updated oatmeal.json successfully with', len(themes_summary), 'themes!')
