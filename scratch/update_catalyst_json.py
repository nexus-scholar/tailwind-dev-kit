import json
from pathlib import Path

cat_dir = Path("scraped_components/ui-kit/catalyst")
ts_components = sorted([p.stem for p in (cat_dir / "typescript").glob("*.tsx")])

meta = {
    "name": "Catalyst",
    "slug": "catalyst",
    "type": "Application UI Kit",
    "url": "https://tailwindcss.com/plus/ui-kit",
    "documentation_url": "https://catalyst.tailwindui.com/docs",
    "download_url": "https://tailwindcss.com/plus/templates/catalyst/download",
    "local_archive": "scraped_components/templates/catalyst.zip",
    "extracted_path": "scraped_components/ui-kit/catalyst",
    "summary": "Modern, opinionated application UI kit built with React and Tailwind CSS. Includes 26 core application components implemented in both TypeScript (.tsx) and JavaScript (.jsx), plus full Next.js demo applications.",
    "frameworks": ["React", "Next.js", "Tailwind CSS v4", "Headless UI"],
    "total_components": len(ts_components),
    "components": ts_components,
    "directories": {
        "typescript": "scraped_components/ui-kit/catalyst/typescript",
        "javascript": "scraped_components/ui-kit/catalyst/javascript",
        "demo": "scraped_components/ui-kit/catalyst/demo"
    }
}

with open("scraped_components/templates/catalyst.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

print(f"Updated catalyst.json with {len(ts_components)} components!")
