import httpx
import re

r = httpx.get('https://catalyst.tailwindui.com/docs')
links = [l for l in re.findall(r'href="([^"]+)"', r.text) if any(k in l.lower() for k in ['download', 'theme', 'kit', 'plus'])]
print("Relevant links:", set(links))
