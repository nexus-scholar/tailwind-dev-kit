from tailwind_dev_kit.client import TailwindPlusClient
from tailwind_dev_kit.auth import create_authenticated_client

c, _ = create_authenticated_client()
tp = TailwindPlusClient(c)

data = tp.get_inertia("https://tailwindcss.com/plus/templates")
props = data.get("props", {})
print("Props keys:", list(props.keys()))
for k in ["templates", "products", "categories"]:
    val = props.get(k)
    print(k, type(val), len(val) if hasattr(val, "__len__") else val)
