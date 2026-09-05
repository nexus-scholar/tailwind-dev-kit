from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, Set, List, Optional
from datetime import datetime

from .models import Component, Template, ScrapeManifest, Snippet
from .client import slugify


class ComponentStorage:
    def __init__(self, base_dir: Path = Path("scraped_components")):
        self.base_dir = base_dir
        self.cache_dir = Path(".cache")
        self.progress_file = self.cache_dir / "progress.json"
        
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load_progress(self) -> Dict[str, Any]:
        """Load already completed component IDs and template slugs."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"completed_components": [], "completed_templates": []}

    def save_progress(self, progress: Dict[str, Any]) -> None:
        """Persist progress to disk."""
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2)

    def is_component_completed(
        self,
        component: Component,
        index: int,
        formats: List[str],
        progress: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Check if all requested formats exist on disk for this component."""
        comp_dir = self.get_component_dir(component, index)
        if not (comp_dir / "metadata.json").exists():
            return False
        fmt_files = {
            "html": "component.html",
            "react": "component.jsx",
            "vue": "component.vue",
        }
        for fmt in formats:
            fname = fmt_files.get(fmt)
            if fname and not (comp_dir / fname).exists():
                return False
        return True

    def load_existing_snippets(self, component: Component, index: int = 1) -> None:
        """Populate component.snippets with any existing format files already saved on disk."""
        comp_dir = self.get_component_dir(component, index)
        if not comp_dir.exists():
            return

        fmt_mapping = [
            ("html", "component.html", "html"),
            ("react", "component.jsx", "jsx"),
            ("vue", "component.vue", "vue"),
        ]
        for fmt, fname, lang in fmt_mapping:
            fpath = comp_dir / fname
            if fpath.exists() and (fmt not in component.snippets or not component.snippets[fmt].code):
                try:
                    code = fpath.read_text(encoding="utf-8")
                    component.snippets[fmt] = Snippet(
                        name=fmt,
                        language=lang,
                        version="4.3",
                        code=code,
                    )
                except Exception:
                    pass

        preview_path = comp_dir / "preview.html"
        if preview_path.exists():
            try:
                preview_html = preview_path.read_text(encoding="utf-8")
                for snip in component.snippets.values():
                    if not snip.preview:
                        snip.preview = preview_html
            except Exception:
                pass

    def mark_component_completed(self, comp_id: str, progress: Dict[str, Any]) -> None:
        if comp_id not in progress.setdefault("completed_components", []):
            progress["completed_components"].append(comp_id)
            self.save_progress(progress)

    def is_template_completed(self, tpl_slug: str, progress: Dict[str, Any]) -> bool:
        tpl_dir = self.get_templates_dir()
        return (tpl_dir / f"{tpl_slug}.zip").exists() or tpl_slug in set(progress.get("completed_templates", []))

    def mark_template_completed(self, tpl_slug: str, progress: Dict[str, Any]) -> None:
        if tpl_slug not in progress.setdefault("completed_templates", []):
            progress["completed_templates"].append(tpl_slug)
            self.save_progress(progress)

    def get_component_dir(self, component: Component, index: int = 1) -> Path:
        """Generate nested output directory path for a component."""
        prod_slug = slugify(component.product)
        cat_slug = slugify(component.category)
        sub_slug = slugify(component.subcategory)
        comp_folder = f"{index:02d}-{component.slug}"

        comp_dir = self.base_dir / prod_slug / cat_slug / sub_slug / comp_folder
        comp_dir.mkdir(parents=True, exist_ok=True)
        return comp_dir

    def save_component(self, component: Component, index: int = 1) -> Path:
        """Save all snippets and metadata for a component to disk."""
        comp_dir = self.get_component_dir(component, index)

        # 1. Save HTML variant
        if "html" in component.snippets and component.snippets["html"].code:
            with open(comp_dir / "component.html", "w", encoding="utf-8") as f:
                f.write(component.snippets["html"].code)

        # 2. Save React variant
        if "react" in component.snippets and component.snippets["react"].code:
            with open(comp_dir / "component.jsx", "w", encoding="utf-8") as f:
                f.write(component.snippets["react"].code)

        # 3. Save Vue variant
        if "vue" in component.snippets and component.snippets["vue"].code:
            with open(comp_dir / "component.vue", "w", encoding="utf-8") as f:
                f.write(component.snippets["vue"].code)

        # 4. Save Preview HTML if present
        for snip in component.snippets.values():
            if snip.preview:
                with open(comp_dir / "preview.html", "w", encoding="utf-8") as f:
                    f.write(snip.preview)
                break

        # 5. Save metadata JSON
        meta_dict = {
            "id": component.id,
            "uuid": component.uuid,
            "name": component.name,
            "slug": component.slug,
            "product": component.product,
            "category": component.category,
            "subcategory": component.subcategory,
            "subcat_url": component.subcat_url,
            "downloadable": component.downloadable,
            "is_new": component.is_new,
            "archived": component.archived,
            "dimensions": {
                "large": {"width": component.large_width, "height": component.large_height},
                "small": {"width": component.small_width, "height": component.small_height},
            },
            "available_formats": sorted(list(
                set(component.snippets.keys()) | {
                    fmt for fmt, fname in [("html", "component.html"), ("react", "component.jsx"), ("vue", "component.vue")]
                    if (comp_dir / fname).exists()
                }
            )),
            "image_credits": component.image_credits_html,
        }
        with open(comp_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(meta_dict, f, indent=2)

        return comp_dir

    def get_templates_dir(self) -> Path:
        tpl_dir = self.base_dir / "templates"
        tpl_dir.mkdir(parents=True, exist_ok=True)
        return tpl_dir

    def load_manifest(self) -> Optional[ScrapeManifest]:
        """Load existing master manifest from disk if present."""
        manifest_path = self.base_dir / "manifest.json"
        if manifest_path.exists():
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return ScrapeManifest.model_validate(data)
            except Exception:
                pass
        return None

    def rebuild_manifest_from_disk(self) -> Path:
        """Scan scraped_components directory and generate a fresh, comprehensive manifest."""
        components: List[Component] = []
        templates: List[Template] = []

        # 1. Scan components
        for meta_file in sorted(self.base_dir.rglob("metadata.json")):
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                comp_dir = meta_file.parent
                snippets: Dict[str, Snippet] = {}

                # HTML
                html_file = comp_dir / "component.html"
                if html_file.exists():
                    snippets["html"] = Snippet(
                        name="html",
                        language="html",
                        version="4.3",
                        code=html_file.read_text(encoding="utf-8"),
                    )

                # React
                jsx_file = comp_dir / "component.jsx"
                if jsx_file.exists():
                    snippets["react"] = Snippet(
                        name="react",
                        language="jsx",
                        version="4.3",
                        code=jsx_file.read_text(encoding="utf-8"),
                    )

                # Vue
                vue_file = comp_dir / "component.vue"
                if vue_file.exists():
                    snippets["vue"] = Snippet(
                        name="vue",
                        language="vue",
                        version="4.3",
                        code=vue_file.read_text(encoding="utf-8"),
                    )

                # Preview
                prev_file = comp_dir / "preview.html"
                if prev_file.exists():
                    preview_str = prev_file.read_text(encoding="utf-8")
                    for snip in snippets.values():
                        snip.preview = preview_str

                dims = meta.get("dimensions") or {}
                comp = Component(
                    id=meta.get("id"),
                    uuid=meta.get("uuid"),
                    name=meta.get("name"),
                    slug=meta.get("slug"),
                    product=meta.get("product"),
                    category=meta.get("category"),
                    subcategory=meta.get("subcategory"),
                    subcat_url=meta.get("subcat_url"),
                    downloadable=meta.get("downloadable", True),
                    is_new=meta.get("is_new", False),
                    archived=meta.get("archived", False),
                    image_credits_html=meta.get("image_credits"),
                    large_width=(dims.get("large") or {}).get("width"),
                    large_height=(dims.get("large") or {}).get("height"),
                    small_width=(dims.get("small") or {}).get("width"),
                    small_height=(dims.get("small") or {}).get("height"),
                    snippets=snippets,
                )
                components.append(comp)
            except Exception:
                continue

        # 2. Scan templates
        tpl_dir = self.get_templates_dir()
        for tpl_json in sorted(tpl_dir.glob("*.json")):
            try:
                with open(tpl_json, "r", encoding="utf-8") as f:
                    tdata = json.load(f)
                templates.append(Template.model_validate(tdata))
            except Exception:
                continue

        return self.save_manifest(components, templates, merge=False)

    def save_manifest(
        self,
        components: List[Component],
        templates: List[Template],
        merge: bool = True,
    ) -> Path:
        """Save searchable master index manifest, optionally merging with existing entries."""
        manifest_path = self.base_dir / "manifest.json"
        comp_map: Dict[str, Component] = {}
        tpl_map: Dict[str, Template] = {}

        if merge:
            existing = self.load_manifest()
            if existing:
                for c in existing.components:
                    comp_map[c.id] = c
                for t in existing.templates:
                    tpl_map[t.slug] = t

        for c in components:
            if c.id in comp_map:
                for k, v in c.snippets.items():
                    comp_map[c.id].snippets[k] = v
            else:
                comp_map[c.id] = c

        for t in templates:
            tpl_map[t.slug] = t

        final_components = list(comp_map.values()) if merge else components
        final_templates = list(tpl_map.values()) if merge else templates

        manifest = ScrapeManifest(
            scraped_at=datetime.utcnow().isoformat() + "Z",
            tailwind_version="4.3",
            total_components=len(final_components),
            total_templates=len(final_templates),
            products=sorted(list(set(c.product for c in final_components))),
            components=final_components,
            templates=final_templates,
        )
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest.model_dump_json(indent=2))
        return manifest_path
