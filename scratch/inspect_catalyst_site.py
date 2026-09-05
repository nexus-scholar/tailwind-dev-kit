import httpx
import re

r = httpx.get('https://catalyst.tailwindui.com', follow_redirects=True)
print("Catalyst main page status:", r.status_code)
# Search for themes, colors, variations
matches = re.findall(r'(theme[s]?|color[s]?|variant[s]?|download[s]?)', r.text, re.I)
print("Keywords found:", set(matches))

# Check docs/overview or installation
r_docs = httpx.get('https://catalyst.tailwindui.com/docs', follow_redirects=True)
print("Docs text sample:\n", r_docs.text[:1000])
