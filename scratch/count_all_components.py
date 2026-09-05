import urllib.request
import json
import time

subcats = json.load(open('scratch/subcategories.json'))
print(f"Checking {len(subcats)} subcategories...")

all_components = []
version = '34780f1f2ee1b970f2e7ec06d306888b'

for i, sub in enumerate(subcats):
    url = sub['url']
    req = urllib.request.Request(
        url,
        headers={
            'X-Inertia': 'true',
            'X-Inertia-Version': version,
            'User-Agent': 'Mozilla/5.0'
        }
    )
    try:
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode('utf-8'))['props']
        comps = data.get('subcategory', {}).get('components', [])
        for c in comps:
            all_components.append({
                'id': c.get('id'),
                'uuid': c.get('uuid'),
                'name': c.get('name'),
                'product': sub['product'],
                'category': sub['category'],
                'subcategory': sub['name'],
                'subcat_url': sub['url'],
                'downloadable': c.get('downloadable'),
                'has_snippet': c.get('snippet') is not None,
                'supports_dark_mode': c.get('snippet', {}).get('supportsDarkMode') if c.get('snippet') else False
            })
        print(f"[{i+1}/{len(subcats)}] {sub['name']}: {len(comps)} components (Total so far: {len(all_components)})")
    except Exception as e:
        print(f"[{i+1}/{len(subcats)}] {sub['name']} ERROR: {e}")
    time.sleep(0.1)

print(f"\nFINISHED! Total unique components discovered: {len(all_components)}")
with open('scratch/all_components_manifest.json', 'w', encoding='utf-8') as f:
    json.dump(all_components, f, indent=2)
