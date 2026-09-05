import re
from tailwind_dev_kit.client import TailwindPlusClient
from tailwind_dev_kit.auth import create_authenticated_client

c, _ = create_authenticated_client()
tp = TailwindPlusClient(c)

for path in ['/plus', '/plus/templates', '/plus/ui-blocks', '/plus/ui-kit', '/plus/kits/oatmeal']:
    data = tp.get_inertia(f'https://tailwindcss.com{path}')
    props = data.get('props', {})
    s = str(props)
    imgs = set(re.findall(r'https?://[^\s\'\"]+\.(?:png|jpg|jpeg|webp|svg)', s))
    print(f"{path}: {len(imgs)} images found")
    for img in sorted(imgs)[:3]:
        print(" ", img)
