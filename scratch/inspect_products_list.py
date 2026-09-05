from tailwind_dev_kit.client import TailwindPlusClient
from tailwind_dev_kit.auth import create_authenticated_client
import json

c, _ = create_authenticated_client()
tp = TailwindPlusClient(c)

data = tp.get_inertia("https://tailwindcss.com/plus/templates")
props = data.get("props", {})
products = props.get("products", [])
for p in products:
    print(p.get("name"), p.get("slug"))
    for k, v in p.items():
        if "image" in k or "screen" in k or "preview" in k or "banner" in k:
            print(f"   {k}: {v}")
