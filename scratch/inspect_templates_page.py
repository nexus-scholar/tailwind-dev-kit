import re, json
from tailwind_dev_kit.client import TailwindPlusClient
from tailwind_dev_kit.auth import create_authenticated_client

c, _ = create_authenticated_client()
tp = TailwindPlusClient(c)

data = tp.get_inertia("https://tailwindcss.com/plus/templates")
props = data.get("props", {})
templates = props.get("templates", [])
print(f"Number of templates on /plus/templates: {len(templates)}")
for t in templates:
    name = t.get("name")
    slug = t.get("slug")
    print(f"Template: {name} ({slug})")
    for k, v in t.items():
        if isinstance(v, str) and ("http" in v or ".png" in v):
            print(f"  {k}: {v}")
        elif isinstance(v, list) and v and isinstance(v[0], str) and ("http" in v[0] or ".png" in v[0]):
            print(f"  {k}: {v}")
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            # check dict for img urls
            sub_imgs = [d.get('url') for d in v if isinstance(d, dict) and d.get('url')]
            if sub_imgs:
                print(f"  {k} (list of dicts): {sub_imgs}")
