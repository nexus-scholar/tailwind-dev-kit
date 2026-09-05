from tailwind_dev_kit.auth import create_authenticated_client
from tailwind_dev_kit.client import TailwindPlusClient
import json

client, _ = create_authenticated_client()
tp = TailwindPlusClient(client)

uuid = "b9bcab4538776a17fff93d18f82a8272"
payload = {"uuid": uuid, "snippet_lang": "html-v3-system"}

headers = tp._inertia_headers({
    "Content-Type": "application/json",
    "Referer": "https://tailwindcss.com/plus/ui-blocks/marketing/sections/heroes"
})

res = client.put("https://tailwindcss.com/plus/ui-blocks/language", json=payload, headers=headers, follow_redirects=False)

# Follow redirect with inertia headers
get_res = client.get(res.headers["Location"], headers=tp._inertia_headers())
data = get_res.json()
comps = data.get("props", {}).get("subcategory", {}).get("components", [])
c0 = [c for c in comps if c.get("uuid") == uuid][0]
print("Component snippet after PUT html-v4.3:")
print("Name:", c0["snippet"]["name"])
print("Language:", c0["snippet"]["language"])
print("Version:", c0["snippet"]["version"])
print("Mode:", c0["snippet"]["mode"])
print("Code starts with:\n", c0["snippet"]["code"][:150])
