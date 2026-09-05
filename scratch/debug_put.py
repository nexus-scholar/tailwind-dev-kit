from tailwind_dev_kit.auth import create_authenticated_client
from tailwind_dev_kit.client import TailwindPlusClient
import urllib.parse

client, status = create_authenticated_client()
tp = TailwindPlusClient(client)

uuid = "b9bcab4538776a17fff93d18f82a8272"
payload = {"uuid": uuid, "snippet_lang": "html-v4.3-light"}

xsrf = client.cookies.get("XSRF-TOKEN")
if xsrf:
    tp.csrf_token = urllib.parse.unquote(xsrf)

headers = tp._inertia_headers({
    "Content-Type": "application/json",
    "Referer": "https://tailwindcss.com/plus/ui-blocks/marketing/sections/heroes"
})

res = client.put("https://tailwindcss.com/plus/ui-blocks/language", json=payload, headers=headers, follow_redirects=False)
print('PUT status:', res.status_code)
print('PUT headers:', dict(res.headers))
print('PUT cookies:', dict(client.cookies))
print('PUT body sample:', res.text[:200])

loc = res.headers.get("Location")
if loc:
    get_res = client.get(loc, headers=tp._inertia_headers())
    print('\nGET redirected status:', get_res.status_code)
    data = get_res.json()
    comps = data.get("props", {}).get("subcategory", {}).get("components", [])
    for c in comps:
        if c.get("uuid") == uuid:
            print('Component snippet:', c.get("snippet", {}).get("name"))
            print('Component snippet lang:', c.get("snippet", {}).get("language"))
            print('Component code sample:\n', c.get("snippet", {}).get("code")[:150])
