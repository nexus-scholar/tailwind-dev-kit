import urllib.request
import json

req = urllib.request.Request(
    'https://tailwindcss.com/plus/ui-blocks',
    headers={'X-Inertia': 'true', 'X-Inertia-Version': '34780f1f2ee1b970f2e7ec06d306888b', 'User-Agent': 'Mozilla/5.0'}
)
res = urllib.request.urlopen(req)
data = json.loads(res.read().decode('utf-8'))['props']

total_subcats = 0
total_comps = 0
subcat_list = []

for p in data['products']:
    p_name = p['name']
    for cat in p['categories']:
        cat_name = cat['name']
        for sub in cat.get('subcategories', []):
            total_subcats += 1
            count = sub.get('componentCount', 0)
            total_comps += count
            subcat_list.append({
                'product': p_name,
                'category': cat_name,
                'name': sub['name'],
                'url': sub['url'],
                'count': count
            })

print(f"Total products: {len(data['products'])}")
print(f"Total subcategories: {total_subcats}")
print(f"Total advertised components: {total_comps}")

with open('scratch/subcategories.json', 'w', encoding='utf-8') as f:
    json.dump(subcat_list, f, indent=2)

for item in subcat_list[:10]:
    print(f"[{item['product']} > {item['category']}] {item['name']} ({item['count']}) -> {item['url']}")
