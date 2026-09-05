from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from mcp.server.mcpserver import MCPServer

app = MCPServer(
    name="tailwind-plus",
    instructions=(
        "Access the local catalog of 657 official Tailwind CSS Plus (Tailwind UI) "
        "components (HTML, React/JSX, Vue) and 14 complete website templates/kits."
    ),
)


def _find_base_dir() -> Path:
    """Resolve the directory containing scraped_components and manifest.json."""
    candidates = [
        Path.cwd() / "scraped_components",
        Path(__file__).resolve().parents[2] / "scraped_components",
        Path(__file__).resolve().parents[1] / "scraped_components",
    ]
    for c in candidates:
        if (c / "manifest.json").exists():
            return c
    return Path.cwd() / "scraped_components"


def _load_manifest() -> Dict[str, Any]:
    base_dir = _find_base_dir()
    manifest_file = base_dir / "manifest.json"
    if manifest_file.exists():
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"components": [], "templates": []}


def _find_component_file(comp: Dict[str, Any], filename: str) -> Optional[Path]:
    """Locate a component's specific file on disk."""
    base_dir = _find_base_dir()
    slug = comp.get("slug", "")
    uuid = comp.get("uuid", "") or comp.get("id", "")

    # Search pattern in base_dir
    for p in base_dir.rglob(filename):
        # Check if the folder contains this component's metadata
        meta_p = p.parent / "metadata.json"
        if meta_p.exists():
            try:
                with open(meta_p, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                if meta.get("uuid") == uuid or meta.get("id") == uuid or meta.get("slug") == slug:
                    return p
            except Exception:
                continue
    return None


@app.tool()
def search_components(
    query: str,
    product: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10,
) -> str:
    """
    Search Tailwind CSS Plus components by keyword, product, or category.

    Args:
        query: Search term (e.g. 'hero', 'modal', 'pricing', 'bento', 'table', 'sidebar').
        product: Optional filter by product ('Marketing', 'Application UI', 'Ecommerce').
        category: Optional category filter (e.g. 'Page Sections', 'Overlays', 'Forms').
        limit: Maximum number of results to return (default 10).
    """
    manifest = _load_manifest()
    components = manifest.get("components", [])
    q = query.lower().strip()

    matches = []
    for c in components:
        prod_match = True
        if product:
            prod_match = product.lower() in (c.get("product") or "").lower()

        cat_match = True
        if category:
            cat_match = (
                category.lower() in (c.get("category") or "").lower()
                or category.lower() in (c.get("subcategory") or "").lower()
            )

        if not (prod_match and cat_match):
            continue

        searchable_text = f"{c.get('name', '')} {c.get('slug', '')} {c.get('product', '')} {c.get('category', '')} {c.get('subcategory', '')}".lower()
        if q in searchable_text:
            matches.append(c)

    if not matches:
        return f"No components found matching '{query}'" + (f" in product '{product}'" if product else "") + "."

    lines = [f"### Found {len(matches)} components for '{query}' (showing up to {limit}):\n"]
    for c in matches[:limit]:
        snippets = c.get("snippets", {})
        available_formats = list(snippets.keys())
        dims = f"{c.get('large_width', '-')}x{c.get('large_height', '-')}"
        lines.append(
            f"- **{c.get('name')}** (`{c.get('slug')}`)\n"
            f"  - **ID / UUID**: `{c.get('uuid') or c.get('id')}`\n"
            f"  - **Location**: `{c.get('product')} > {c.get('category')} > {c.get('subcategory')}`\n"
            f"  - **Available Formats**: `{', '.join(available_formats) if available_formats else 'html, react'}`\n"
            f"  - **Dimensions**: {dims} | **URL**: {c.get('subcat_url')}\n"
        )
    return "\n".join(lines)


@app.tool()
def get_component_code(
    identifier: str,
    format: str = "react",
) -> str:
    """
    Retrieve the exact source code for a Tailwind CSS Plus component.

    Args:
        identifier: The component UUID, ID, or slug (e.g. 'b9bcab4538776a17fff93d18f82a8272' or 'simple-centered').
        format: The target format ('react', 'html', or 'vue'). Defaults to 'react'.
    """
    manifest = _load_manifest()
    components = manifest.get("components", [])
    target = identifier.lower().strip()

    comp = None
    for c in components:
        if (
            (c.get("uuid") or "").lower() == target
            or (c.get("id") or "").lower() == target
            or (c.get("slug") or "").lower() == target
            or (c.get("name") or "").lower() == target
        ):
            comp = c
            break

    fmt = format.lower().strip()
    if fmt in ["jsx", "tsx", "js"]:
        fmt = "react"

    # Try to read code directly from manifest snippets
    code = None
    if comp:
        snippets = comp.get("snippets", {})
        if fmt in snippets and snippets[fmt].get("code"):
            code = snippets[fmt]["code"]

    # Fallback: check file on disk
    file_map = {"react": "component.jsx", "html": "component.html", "vue": "component.vue"}
    filename = file_map.get(fmt, "component.jsx")

    if not code and comp:
        fpath = _find_component_file(comp, filename)
        if fpath and fpath.exists():
            code = fpath.read_text(encoding="utf-8")

    # If still not found, search disk by folder slug
    if not code:
        base_dir = _find_base_dir()
        for folder in base_dir.rglob(f"*{target}*"):
            if folder.is_dir() and (folder / filename).exists():
                code = (folder / filename).read_text(encoding="utf-8")
                break

    if not code:
        return f"Error: Could not find '{fmt}' code for component '{identifier}'. Available formats may include html, react, or vue."

    comp_name = comp.get("name", identifier) if comp else identifier
    lang = "jsx" if fmt == "react" else fmt
    header = f"// Component: {comp_name} ({fmt.upper()})\n"
    if comp:
        header += f"// Product: {comp.get('product')} | Category: {comp.get('category')} > {comp.get('subcategory')}\n"
        header += f"// Tailored for Tailwind CSS v4\n\n"

    return f"```{lang}\n{header}{code}\n```"


@app.tool()
def get_component_details(identifier: str) -> str:
    """
    Get full metadata and available file paths for a component.

    Args:
        identifier: The component UUID, ID, or slug.
    """
    manifest = _load_manifest()
    components = manifest.get("components", [])
    target = identifier.lower().strip()

    comp = None
    for c in components:
        if (
            (c.get("uuid") or "").lower() == target
            or (c.get("id") or "").lower() == target
            or (c.get("slug") or "").lower() == target
        ):
            comp = c
            break

    if not comp:
        return f"Component '{identifier}' not found in manifest."

    snippets = comp.get("snippets", {})
    available = list(snippets.keys())

    return (
        f"### {comp.get('name')}\n"
        f"- **UUID**: `{comp.get('uuid')}`\n"
        f"- **Slug**: `{comp.get('slug')}`\n"
        f"- **Product**: {comp.get('product')}\n"
        f"- **Category**: {comp.get('category')}\n"
        f"- **Subcategory**: {comp.get('subcategory')}\n"
        f"- **Subcategory URL**: {comp.get('subcat_url')}\n"
        f"- **Available Formats**: {', '.join(available) if available else 'html, react'}\n"
        f"- **Dimensions**: Large ({comp.get('large_width')}x{comp.get('large_height')}), Small ({comp.get('small_width')}x{comp.get('small_height')})\n"
        f"- **Dark Mode**: Built-in Tailwind v4 dark: variants\n"
    )


@app.tool()
def list_categories(product: Optional[str] = None) -> str:
    """
    List all products, categories, and 93 subcategories available on Tailwind Plus.

    Args:
        product: Optional filter by product ('Marketing', 'Application UI', 'Ecommerce').
    """
    manifest = _load_manifest()
    components = manifest.get("components", [])

    taxonomy: Dict[str, Dict[str, Dict[str, int]]] = {}
    for c in components:
        p = c.get("product", "Other")
        cat = c.get("category", "General")
        sub = c.get("subcategory", "General")

        if product and product.lower() not in p.lower():
            continue

        taxonomy.setdefault(p, {}).setdefault(cat, {}).setdefault(sub, 0)
        taxonomy[p][cat][sub] += 1

    lines = ["# Tailwind Plus Taxonomy & Component Counts:\n"]
    for p, cats in sorted(taxonomy.items()):
        lines.append(f"## {p}")
        for cat, subs in sorted(cats.items()):
            lines.append(f"### {cat}")
            for sub, count in sorted(subs.items()):
                lines.append(f"- **{sub}**: {count} components")
            lines.append("")

    return "\n".join(lines)


@app.tool()
def list_templates() -> str:
    """
    List all 14 official Tailwind CSS website templates and UI kits.
    Shows template names, types, and whether the local .zip archive is available.
    """
    manifest = _load_manifest()
    templates = manifest.get("templates", [])
    base_dir = _find_base_dir()
    tpl_dir = base_dir / "templates"

    lines = ["# Standalone Website Templates & Kits (14 Available):\n"]
    for t in templates:
        slug = t.get("slug", "")
        zip_file = tpl_dir / f"{slug}.zip"
        status = "Downloaded" if zip_file.exists() else "Download Pending"
        size_str = f" ({zip_file.stat().st_size // 1024} KB)" if zip_file.exists() else ""
        lines.append(
            f"- **{t.get('name')}** (`{slug}`)\n"
            f"  - **Type**: {t.get('type')}\n"
            f"  - **Local Archive**: `{zip_file}` [{status}{size_str}]\n"
            f"  - **Official URL**: {t.get('url')}\n"
        )

    return "\n".join(lines)


@app.tool()
def get_template_info(slug: str) -> str:
    """
    Get detailed information about a specific website template or UI kit.

    Args:
        slug: The template slug (e.g. 'catalyst', 'oatmeal', 'salient', 'radiant', 'spotlight').
    """
    manifest = _load_manifest()
    templates = manifest.get("templates", [])
    target = slug.lower().strip()

    tpl = None
    for t in templates:
        if (t.get("slug") or "").lower() == target or (t.get("name") or "").lower() == target:
            tpl = t
            break

    if not tpl:
        return f"Template '{slug}' not found."

    base_dir = _find_base_dir()
    tpl_dir = base_dir / "templates"
    zip_path = tpl_dir / f"{tpl.get('slug')}.zip"
    meta_path = tpl_dir / f"{tpl.get('slug')}.json"

    meta_details = {}
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta_details = json.load(f)
        except Exception:
            pass

    tech_list = meta_details.get("technologies_summary", [])
    if not tech_list and meta_details.get("technologies"):
        t_raw = meta_details.get("technologies")
        tech_list = [f"{t.get('name')} {t.get('version', '')}".strip() for t in t_raw] if isinstance(t_raw, list) and t_raw and isinstance(t_raw[0], dict) else t_raw

    lines = [
        f"### {tpl.get('name')} ({tpl.get('type')})",
        f"- **Slug**: `{tpl.get('slug')}`",
        f"- **Summary**: {meta_details.get('summary') or 'Full multi-page production website template'}",
        f"- **Technologies**: {', '.join(tech_list) if tech_list else 'Next.js, React, Tailwind CSS'}",
        f"- **Local Archive**: `{zip_path}` ({'Available' if zip_path.exists() else 'Missing'} - {zip_path.stat().st_size // 1024 if zip_path.exists() else 0} KB)",
        f"- **Live Demo / Preview**: {meta_details.get('demo_preview_url') or tpl.get('preview_url') or meta_details.get('url')}",
        f"- **Official URL**: {tpl.get('url')}",
    ]

    local_screens_dir = meta_details.get("local_screens_dir")
    local_screens = meta_details.get("local_screenshots", [])
    local_banner = meta_details.get("local_banner_image")
    if local_screens_dir or local_screens:
        lines.append(f"- **Local Screens Directory**: `{local_screens_dir}` ({len(local_screens)} images)")
        if local_banner:
            lines.append(f"- **Main Screenshot / Banner**: `{local_banner}`")

    if meta_details.get("description"):
        lines.append(f"\n**Description**:\n{meta_details.get('description')}")

    # Specific details for Oatmeal (12 Themes)
    if tpl.get("slug") == "oatmeal":
        themes = meta_details.get("themes", [])
        lines.append(f"\n#### Oatmeal Themes ({len(themes)} Available):")
        for th in themes:
            lines.append(f"- **{th.get('name')}** (`{th.get('slug')}`): Color `{th.get('color')}`, Font `{th.get('font')}` -> `{th.get('local_archive')}`")

    # Specific details for Catalyst (27 Core UI Components)
    if tpl.get("slug") == "catalyst":
        comps = meta_details.get("components", [])
        lines.append(f"\n#### Catalyst UI Kit Components ({len(comps)} Available):")
        lines.append(f"Located in: `{meta_details.get('directories', {}).get('typescript')}` and `{meta_details.get('directories', {}).get('javascript')}`")
        lines.append(f"- Components: {', '.join(comps)}")

    return "\n".join(lines)


@app.tool()
def get_catalyst_component(
    name: str,
    language: str = "typescript",
) -> str:
    """
    Retrieve source code for a Catalyst Application UI Kit component.

    Args:
        name: Component name (e.g. 'button', 'dialog', 'dropdown', 'table', 'input', 'sidebar', 'navbar', 'badge').
        language: 'typescript' (.tsx) or 'javascript' (.jsx). Defaults to 'typescript'.
    """
    base_dir = _find_base_dir()
    cat_dir = base_dir / "ui-kit" / "catalyst"
    clean_name = name.lower().strip().replace(".tsx", "").replace(".jsx", "").replace(".ts", "").replace(".js", "")

    lang_folder = "typescript" if "ts" in language.lower() else "javascript"
    ext = ".tsx" if lang_folder == "typescript" else ".jsx"

    comp_file = cat_dir / lang_folder / f"{clean_name}{ext}"
    if not comp_file.exists():
        # Search for partial match
        matches = list((cat_dir / lang_folder).glob(f"*{clean_name}*{ext}"))
        if matches:
            comp_file = matches[0]

    if not comp_file.exists():
        available = [p.stem for p in (cat_dir / "typescript").glob("*.tsx")]
        return f"Component '{name}' not found in Catalyst UI Kit. Available components: {', '.join(available)}"

    code = comp_file.read_text(encoding="utf-8")
    header = f"// Catalyst UI Kit: {comp_file.stem} ({lang_folder.upper()})\n// Path: {comp_file}\n\n"
    code_lang = "tsx" if ext == ".tsx" else "jsx"
    return f"```{code_lang}\n{header}{code}\n```"


def main() -> None:
    """Run the MCP server over stdio transport."""
    app.run(transport="stdio")


if __name__ == "__main__":
    main()
