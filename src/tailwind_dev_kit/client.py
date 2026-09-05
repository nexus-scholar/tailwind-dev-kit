from __future__ import annotations

import html
import re
import urllib.parse
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
import httpx
from rich.console import Console

from .models import Subcategory, Component, Snippet, Template
from .auth import DEFAULT_USER_AGENT, BASE_URL

console = Console()


def slugify(text: str) -> str:
    """Convert a human-readable title into a clean URL/filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


class TailwindPlusClient:
    def __init__(self, client: httpx.Client):
        self.client = client
        self.version: Optional[str] = None
        self.csrf_token: Optional[str] = None
        self._init_inertia_session()

    def _init_inertia_session(self, url: str = f"{BASE_URL}/plus") -> None:
        """Fetch the landing page to extract current Inertia version and XSRF-TOKEN."""
        res = self.client.get(
            url,
            headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "text/html"}
        )
        unescaped = html.unescape(res.text)
        m = re.search(r'"version":\s*"([^"]+)"', unescaped)
        if m:
            self.version = m.group(1)

        xsrf = self.client.cookies.get("XSRF-TOKEN")
        if xsrf:
            self.csrf_token = urllib.parse.unquote(xsrf)

    def _inertia_headers(self, additional: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html, application/xhtml+xml",
            "X-Requested-With": "XMLHttpRequest",
            "X-Inertia": "true",
        }
        if self.version:
            headers["X-Inertia-Version"] = self.version
        if self.csrf_token:
            headers["X-XSRF-TOKEN"] = self.csrf_token
        if additional:
            headers.update(additional)
        return headers

    def get_inertia(self, url: str) -> Dict[str, Any]:
        """Make an Inertia GET request, handling version conflict retries automatically."""
        res = self.client.get(url, headers=self._inertia_headers())
        if res.status_code == 409:
            # Inertia version mismatch; server sends new version header or location
            new_version = res.headers.get("X-Inertia-Version")
            if new_version:
                self.version = new_version
            else:
                self._init_inertia_session()
            res = self.client.get(url, headers=self._inertia_headers())

        res.raise_for_status()
        return res.json()

    def get_taxonomy(self) -> Tuple[List[Subcategory], List[Template]]:
        """Fetch full taxonomy of products, categories, subcategories, and templates."""
        # 1. UI Blocks subcategories
        data = self.get_inertia(f"{BASE_URL}/plus/ui-blocks")
        props = data.get("props", {})
        subcategories: List[Subcategory] = []

        for prod in props.get("products", []):
            prod_name = prod.get("name", "")
            for cat in prod.get("categories", []):
                cat_name = cat.get("name", "")
                for sub in cat.get("subcategories", []):
                    sub_name = sub.get("name", "")
                    sub_url = sub.get("url", "")
                    subcategories.append(
                        Subcategory(
                            name=sub_name,
                            slug=slugify(sub_name),
                            category=cat_name,
                            product=prod_name,
                            url=sub_url,
                            component_count=sub.get("componentCount", 0),
                        )
                    )

        # 2. Templates
        home_data = self.get_inertia(f"{BASE_URL}/plus")
        home_props = home_data.get("props", {})
        templates: List[Template] = []

        for t in home_props.get("templates", []):
            t_name = t.get("name", "")
            t_url = t.get("url", "")
            t_slug = slugify(t_name)
            download_url = f"{BASE_URL}/plus/templates/{t_slug}/download"
            if t_slug == "oatmeal":
                download_url = f"{BASE_URL}/plus/templates/oatmeal/download?theme=olive_instrument"

            templates.append(
                Template(
                    id=t.get("id"),
                    name=t_name,
                    slug=t_slug,
                    type=t.get("type"),
                    url=t_url,
                    download_url=download_url,
                    preview_url=t.get("thumbnail"),
                )
            )

        # Add Catalyst UI Kit if not in templates
        if not any(tpl.slug == "catalyst" for tpl in templates):
            templates.append(
                Template(
                    name="Catalyst",
                    slug="catalyst",
                    type="Application UI Kit",
                    url=f"{BASE_URL}/plus/templates/catalyst",
                    download_url=f"{BASE_URL}/plus/templates/catalyst/download",
                )
            )

        return subcategories, templates

    def get_subcategory_components(self, subcat: Subcategory) -> List[Component]:
        """Fetch all components for a specific subcategory."""
        data = self.get_inertia(subcat.url)
        props = data.get("props", {})
        sub_data = props.get("subcategory", {})
        raw_components = sub_data.get("components", [])

        components: List[Component] = []
        for c in raw_components:
            uuid = c.get("uuid") or c.get("id")
            name = c.get("name", "Unnamed Component")
            slug = slugify(name)
            
            raw_snippet = c.get("snippet")
            snippets: Dict[str, Snippet] = {}
            if raw_snippet:
                lang_name = raw_snippet.get("name", "html")
                snippets[lang_name] = Snippet(
                    name=lang_name,
                    language=raw_snippet.get("language", lang_name),
                    version=str(raw_snippet.get("version", "4.3")),
                    mode=raw_snippet.get("mode"),
                    supports_dark_mode=raw_snippet.get("supportsDarkMode", False),
                    code=raw_snippet.get("code"),
                    preview=raw_snippet.get("preview"),
                )

            comp = Component(
                id=str(c.get("id")),
                uuid=str(uuid),
                name=name,
                slug=slug,
                product=subcat.product,
                category=subcat.category,
                subcategory=subcat.name,
                subcat_url=subcat.url,
                downloadable=c.get("downloadable", False),
                is_new=c.get("isNew", False),
                archived=c.get("archived", False),
                image_credits_html=c.get("imageCreditsHtml"),
                large_width=c.get("largeWidth"),
                large_height=c.get("largeHeight"),
                small_width=c.get("smallWidth"),
                small_height=c.get("smallHeight"),
                snippets=snippets,
            )
            components.append(comp)

        return components

    def fetch_snippet_variant(
        self,
        component: Component,
        language: str,
        version: str = "4.3",
        mode: Optional[str] = None
    ) -> Optional[str]:
        """
        Request a specific language snippet (HTML, React, Vue) for a component.
        Uses Inertia PUT /plus/ui-blocks/language and follows the 303 redirect.
        """
        # Read existing snippet's version and mode if available
        snip = next(iter(component.snippets.values()), None)
        use_version = snip.version if (snip and snip.version) else version
        use_mode = snip.mode if (snip and snip.mode) else mode

        snippet_lang = f"{language}-v{use_version}"
        if use_mode:
            snippet_lang = f"{snippet_lang}-{use_mode}"

        # Refresh CSRF token if needed
        xsrf = self.client.cookies.get("XSRF-TOKEN")
        if xsrf:
            self.csrf_token = urllib.parse.unquote(xsrf)

        put_url = f"{BASE_URL}/plus/ui-blocks/language"
        payload = {"uuid": component.uuid, "snippet_lang": snippet_lang}

        headers = self._inertia_headers({
            "Content-Type": "application/json",
            "Referer": component.subcat_url,
        })

        # PUT request returns 303 redirect to subcat_url
        res = self.client.put(put_url, json=payload, headers=headers, follow_redirects=False)

        redirect_url = res.headers.get("Location") or component.subcat_url
        get_res = self.client.get(redirect_url, headers=self._inertia_headers())

        if get_res.status_code == 200:
            data = get_res.json()
            comps = data.get("props", {}).get("subcategory", {}).get("components", [])
            for c in comps:
                if (c.get("uuid") or c.get("id")) == component.uuid:
                    snip = c.get("snippet")
                    if snip and snip.get("code"):
                        return snip.get("code")

        return None

    def download_template_archive(self, download_url: str, dest_path: Path) -> bool:
        """Stream download a template zip archive to disk."""
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with self.client.stream(
            "GET",
            download_url,
            headers={"User-Agent": DEFAULT_USER_AGENT},
            follow_redirects=True,
        ) as res:
            if res.status_code != 200:
                return False
            with open(dest_path, "wb") as f:
                for chunk in res.iter_bytes(chunk_size=65536):
                    f.write(chunk)
        return True
