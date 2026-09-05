import re
import time
from pathlib import Path
from html.parser import HTMLParser
import httpx

DOC_ROUTES = [
    ("getting-started", "/docs", "Getting Started"),
    ("sidebar-layout", "/docs/sidebar-layout", "Sidebar Layout"),
    ("stacked-layout", "/docs/stacked-layout", "Stacked Layout"),
    ("auth-layout", "/docs/auth-layout", "Auth Layout"),
    ("alert", "/docs/alert", "Alert"),
    ("avatar", "/docs/avatar", "Avatar"),
    ("badge", "/docs/badge", "Badge"),
    ("button", "/docs/button", "Button"),
    ("checkbox", "/docs/checkbox", "Checkbox"),
    ("combobox", "/docs/combobox", "Combobox"),
    ("description-list", "/docs/description-list", "Description List"),
    ("dialog", "/docs/dialog", "Dialog"),
    ("divider", "/docs/divider", "Divider"),
    ("dropdown", "/docs/dropdown", "Dropdown"),
    ("fieldset", "/docs/fieldset", "Fieldset"),
    ("heading", "/docs/heading", "Heading"),
    ("input", "/docs/input", "Input"),
    ("listbox", "/docs/listbox", "Listbox"),
    ("navbar", "/docs/navbar", "Navbar"),
    ("pagination", "/docs/pagination", "Pagination"),
    ("radio", "/docs/radio", "Radio"),
    ("select", "/docs/select", "Select"),
    ("sidebar", "/docs/sidebar", "Sidebar"),
    ("switch", "/docs/switch", "Switch"),
    ("table", "/docs/table", "Table"),
    ("text", "/docs/text", "Text"),
    ("textarea", "/docs/textarea", "Textarea"),
]

class CatalystDocParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.in_pre = False
        self.in_code = False
        self.curr_code = []
        self.seen_codes = set()
        self.in_table = False
        self.table_row = []
        self.table_data = []
        self.in_lead = False
        self.curr_link = None
        self.skip_pre = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "").split()

        if tag in ["h1", "h2", "h3", "h4"]:
            level = int(tag[1])
            self.output.append(f"\n\n{'#' * level} ")
        elif tag == "p":
            if "lead" in classes:
                self.in_lead = True
                self.output.append("\n\n> ")
            else:
                self.output.append("\n\n")
        elif tag == "pre":
            self.in_pre = True
            self.curr_code = []
            # Check if this is the dark-mode duplicate pre
            if "dark:hidden" in classes or "hidden" in classes:
                self.skip_pre = True
            else:
                self.skip_pre = False
        elif tag == "code":
            if not self.in_pre:
                self.in_code = True
                self.output.append("`")
        elif tag == "li":
            self.output.append("\n- ")
        elif tag == "table":
            self.in_table = True
            self.table_data = []
        elif tag == "tr":
            self.table_row = []
        elif tag == "th" or tag == "td":
            self.table_row.append("")
        elif tag == "a":
            href = attrs_dict.get("href", "")
            if href:
                self.curr_link = href

    def handle_endtag(self, tag):
        if tag == "p" and self.in_lead:
            self.in_lead = False
            self.output.append("\n\n")
        elif tag == "pre":
            self.in_pre = False
            code_text = "".join(self.curr_code).strip()
            if code_text and code_text not in self.seen_codes:
                self.seen_codes.add(code_text)
                self.output.append(f"\n\n```tsx\n{code_text}\n```\n\n")
            self.curr_code = []
            self.skip_pre = False
        elif tag == "code" and not self.in_pre:
            self.in_code = False
            self.output.append("`")
        elif tag == "tr" and self.in_table:
            # Clean up empty strings or trailing spaces
            cleaned_row = [c.strip() for c in self.table_row]
            if any(cleaned_row):
                self.table_data.append(cleaned_row)
            self.table_row = []
        elif tag == "table":
            self.in_table = False
            if self.table_data:
                self.output.append("\n\n")
                header = self.table_data[0]
                self.output.append("| " + " | ".join(header) + " |\n")
                self.output.append("| " + " | ".join(["---"] * len(header)) + " |\n")
                for row in self.table_data[1:]:
                    while len(row) < len(header):
                        row.append("")
                    self.output.append("| " + " | ".join(row[:len(header)]) + " |\n")
                self.output.append("\n")
        elif tag == "a":
            self.curr_link = None

    def handle_data(self, data):
        if self.in_pre:
            self.curr_code.append(data)
        elif self.in_table:
            if self.table_row:
                self.table_row[-1] += data
        else:
            self.output.append(data)

    def get_markdown(self):
        raw = "".join(self.output)
        # Normalize whitespace and blank lines
        lines = [line.rstrip() for line in raw.split("\n")]
        text = "\n".join(lines)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


def scrape_all():
    base_dir = Path("scraped_components/ui-kit/catalyst/docs")
    md_dir = base_dir
    html_dir = base_dir / "html"
    assets_dir = base_dir / "assets"
    css_dir = assets_dir / "css"
    img_dir = assets_dir / "images"

    for d in [md_dir, html_dir, css_dir, img_dir]:
        d.mkdir(parents=True, exist_ok=True)

    headers = {"User-Agent": "Mozilla/5.0"}
    with httpx.Client(headers=headers, follow_redirects=True, timeout=30.0) as client:
        # 1. Download Static Assets
        print("[1/4] Downloading static assets (CSS, Images)...")
        css_url = "https://catalyst.tailwindui.com/_next/static/css/cc4524cdffce231c.css"
        r_css = client.get(css_url)
        if r_css.status_code == 200:
            with open(css_dir / "catalyst.css", "w", encoding="utf-8") as f:
                f.write(r_css.text)
            print("  [OK] Saved assets/css/catalyst.css")

        images_to_fetch = [
            ("demo-preview.jpeg", "https://catalyst.tailwindui.com/demo-preview.jpeg"),
            ("demo-preview-dark.jpeg", "https://catalyst.tailwindui.com/demo-preview-dark.jpeg"),
            ("copy-components.png", "https://catalyst.tailwindui.com/_next/static/media/copy-components.f99ada87.png"),
            ("favicon.ico", "https://catalyst.tailwindui.com/favicon.ico"),
        ]
        for fname, url in images_to_fetch:
            r_img = client.get(url)
            if r_img.status_code == 200:
                with open(img_dir / fname, "wb") as f:
                    f.write(r_img.content)
                print(f"  [OK] Saved assets/images/{fname}")

        # 2. Scrape Documentation Pages
        print("\n[2/4] Scraping 27 Documentation Pages...")
        docs_summary = []

        for slug, route, title in DOC_ROUTES:
            url = f"https://catalyst.tailwindui.com{route}"
            r = client.get(url)
            if r.status_code != 200:
                print(f"  [FAIL] {route} -> HTTP {r.status_code}")
                continue

            html = r.text

            # --- A. Save Clean Offline HTML ---
            # Rewrite asset paths to local assets
            offline_html = html
            offline_html = offline_html.replace('href="/_next/static/css/cc4524cdffce231c.css"', 'href="../assets/css/catalyst.css"')
            offline_html = offline_html.replace('src="/demo-preview.jpeg"', 'src="../assets/images/demo-preview.jpeg"')
            offline_html = offline_html.replace('src="/demo-preview-dark.jpeg"', 'src="../assets/images/demo-preview-dark.jpeg"')
            offline_html = offline_html.replace('src="/_next/static/media/copy-components.f99ada87.png"', 'src="../assets/images/copy-components.png"')
            offline_html = offline_html.replace('href="/favicon.ico"', 'href="../assets/images/favicon.ico"')
            
            # Rewrite doc links to local html
            offline_html = offline_html.replace('href="/docs"', 'href="index.html"')
            for s_sub, r_sub, _ in DOC_ROUTES:
                if s_sub != "getting-started":
                    offline_html = offline_html.replace(f'href="{r_sub}"', f'href="{s_sub}.html"')

            html_filename = "index.html" if slug == "getting-started" else f"{slug}.html"
            with open(html_dir / html_filename, "w", encoding="utf-8") as f:
                f.write(offline_html)

            # --- B. Parse Clean Markdown ---
            main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
            main_content = main_match.group(1) if main_match else html

            parser = CatalystDocParser()
            parser.feed(main_content)
            md_content = parser.get_markdown()

            # Prepend frontmatter/header
            full_md = f"# {title} — Catalyst UI Kit Documentation\n\n"
            full_md += f"> Official documentation from [catalyst.tailwindui.com{route}](https://catalyst.tailwindui.com{route})\n\n"
            full_md += md_content + "\n"

            md_filename = "index.md" if slug == "getting-started" else f"{slug}.md"
            with open(md_dir / md_filename, "w", encoding="utf-8") as f:
                f.write(full_md)

            docs_summary.append({
                "slug": slug,
                "title": title,
                "route": route,
                "md_file": f"scraped_components/ui-kit/catalyst/docs/{md_filename}",
                "html_file": f"scraped_components/ui-kit/catalyst/docs/html/{html_filename}",
            })
            print(f"  [OK] {title} -> {md_filename} & {html_filename}")

        # 3. Create Master README.md in docs
        print("\n[3/4] Generating Catalyst Docs README index...")
        readme_lines = [
            "# Catalyst UI Kit — Offline Documentation Library",
            "",
            "Complete offline documentation for Tailwind Labs' **Catalyst Application UI Kit**, including component API tables, code examples, layout patterns, and getting started guides.",
            "",
            "---",
            "",
            "## Table of Contents",
            "",
            "### Overview & Getting Started",
            f"- [**Getting Started Guide**](./index.md) ([Offline HTML](./html/index.html))",
            "",
            "### Layout Components",
        ]
        
        layouts = [d for d in docs_summary if "layout" in d["slug"].lower()]
        for d in layouts:
            readme_lines.append(f"- [**{d['title']}**](./{d['slug']}.md) ([Offline HTML](./html/{d['slug']}.html))")

        readme_lines.extend(["", "### UI Components"])
        components = [d for d in docs_summary if "layout" not in d["slug"].lower() and d["slug"] != "getting-started"]
        for d in components:
            readme_lines.append(f"- [**{d['title']}**](./{d['slug']}.md) ([Offline HTML](./html/{d['slug']}.html))")

        with open(base_dir / "README.md", "w", encoding="utf-8") as f:
            f.write("\n".join(readme_lines) + "\n")
        print("  [OK] Created scraped_components/ui-kit/catalyst/docs/README.md")

        # 4. Update catalyst.json
        print("\n[4/4] Updating catalyst.json metadata...")
        import json
        cat_json_path = Path("scraped_components/templates/catalyst.json")
        with open(cat_json_path, "r", encoding="utf-8") as f:
            cat_data = json.load(f)

        cat_data["local_docs_dir"] = "scraped_components/ui-kit/catalyst/docs"
        cat_data["total_docs_pages"] = len(docs_summary)
        cat_data["docs_pages"] = docs_summary
        cat_data["directories"]["docs"] = "scraped_components/ui-kit/catalyst/docs"

        with open(cat_json_path, "w", encoding="utf-8") as f:
            json.dump(cat_data, f, indent=2)
        print("  [OK] catalyst.json updated with docs metadata.")

if __name__ == "__main__":
    scrape_all()
