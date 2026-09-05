import re
import httpx
r = httpx.get("https://catalyst.tailwindui.com/docs", follow_redirects=True)
links = set(re.findall(r'href="(/docs/[^"#?]*)"', r.text))

print(f"Found {len(links)} doc links:")
for l in sorted(links):
    print(" ", l)
