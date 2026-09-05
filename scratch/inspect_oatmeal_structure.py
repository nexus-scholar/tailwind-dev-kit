from tailwind_dev_kit.client import TailwindPlusClient
from tailwind_dev_kit.auth import create_authenticated_client
import json

c, _ = create_authenticated_client()
tp = TailwindPlusClient(c)

data = tp.get_inertia("https://tailwindcss.com/plus/kits/oatmeal")
props = data.get("props", {})
prod = props.get("product") or {}
print("Oatmeal prod keys:", list(prod.keys()))
themes = prod.get("themes", [])
print(f"Number of themes: {len(themes)}")
if themes:
    print("Theme 0 keys:", list(themes[0].keys()))
    print("Theme 0 screenshots:", themes[0].get("screenshots"))
categories = prod.get("categories", [])
print(f"Number of categories: {len(categories)}")
if categories:
    print("Category 0:", categories[0].get("name"))
