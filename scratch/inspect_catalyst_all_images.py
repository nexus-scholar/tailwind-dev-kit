from tailwind_dev_kit.client import TailwindPlusClient
from tailwind_dev_kit.auth import create_authenticated_client
import json

c, _ = create_authenticated_client()
tp = TailwindPlusClient(c)

data = tp.get_inertia("https://tailwindcss.com/plus/ui-kit")
props = data.get("props", {})
print("Catalyst props keys:", list(props.keys()))
prod = props.get("product") or props.get("template") or {}
print("Catalyst prod keys:", list(prod.keys()))
for k, v in prod.items():
    if isinstance(v, (str, list, dict)):
        s = str(v)
        if "png" in s or "jpg" in s or "img" in s or "screen" in s:
            print(f"  {k}: {s[:120]}")
