import httpx
import re

r = httpx.get('https://catalyst.tailwindui.com/docs', follow_redirects=True)
print('Status:', r.status_code, 'URL:', r.url)
if r.status_code == 200:
    doc_links = set(re.findall(r'href="(/docs/[^"]*)"', r.text))
    print('Catalyst doc pages:', sorted(list(doc_links)))
