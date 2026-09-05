import time
from pathlib import Path
from tailwind_dev_kit.auth import create_authenticated_client

client, _ = create_authenticated_client()

themes = [
    ('mauve_familjen', 'Mauve Familjen'),
    ('mauve_instrument', 'Mauve Instrument'),
    ('mauve_mona', 'Mauve Mona'),
    ('mist_familjen', 'Mist Familjen'),
    ('mist_instrument', 'Mist Instrument'),
    ('mist_mona', 'Mist Mona'),
    ('olive_familjen', 'Olive Familjen'),
    ('olive_instrument', 'Olive Instrument'),
    ('olive_mona', 'Olive Mona'),
    ('taupe_familjen', 'Taupe Familjen'),
    ('taupe_instrument', 'Taupe Instrument'),
    ('taupe_mona', 'Taupe Mona'),
]

oatmeal_dir = Path("scraped_components/templates/oatmeal-themes")
oatmeal_dir.mkdir(parents=True, exist_ok=True)

print(f"Downloading {len(themes)} Oatmeal themes...")
for slug, name in themes:
    dest = oatmeal_dir / f"oatmeal-{slug.replace('_', '-')}.zip"
    if dest.exists() and dest.stat().st_size > 100000:
        print(f"[OK] Already downloaded: {name} ({dest.stat().st_size // 1024} KB)")
        continue

    url = f"https://tailwindcss.com/plus/templates/oatmeal/download?theme={slug}"
    try:
        r = client.get(url, follow_redirects=True)
        if r.status_code == 200 and len(r.content) > 100000:
            with open(dest, "wb") as f:
                f.write(r.content)
            print(f"[OK] Downloaded {name} -> {dest.name} ({len(r.content) // 1024} KB)")
        else:
            print(f"[FAIL] {name}: Status {r.status_code}, Length {len(r.content)}")
    except Exception as e:
        print(f"[ERROR] {name}: {e}")
    time.sleep(0.2)

print("\nDone downloading Oatmeal themes!")
