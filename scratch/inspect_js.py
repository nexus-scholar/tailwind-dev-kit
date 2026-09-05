import urllib.request
import re

url = 'https://tailwindcss.com/plus-assets/build/assets/ComponentPreview-BSFR6WD2.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read().decode('utf-8')
print('Length:', len(content))

# Look for endpoints, URLs, router visits, axios/fetch calls
endpoints = re.findall(r'["\'](/plus/[^"\']+)["\']', content)
print('Endpoints:', set(endpoints))

with open('scratch/preview_js.txt', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved to scratch/preview_js.txt')
