# Tailwind Dev Kit (Tailwind CSS Plus / UI Scraper & Toolkit)

A high-performance, resilient scraper and developer toolkit to catalog and download all official UI components and full application templates from **Tailwind CSS Plus** ([tailwindcss.com/plus](https://tailwindcss.com/plus)).

---

## Features

- **Full Component Coverage**: Catalogs and downloads all **657 official components** (representing all 1,314 light/dark preview variations) across all **93 subcategories** in:
  - **Marketing** (Heroes, Feature Sections, Pricing, Bento Grids, Testimonials, Footers, etc.)
  - **Application UI** (Stacked/Sidebar Layouts, Tables, Input Groups, Modals, Command Palettes, etc.)
  - **Ecommerce** (Product Overviews, Category Filters, Shopping Carts, Checkout Forms, Reviews, etc.)
- **Multi-Framework Code Extraction**:
  - `component.html`: Pure HTML with Tailwind CSS v4 utility classes
  - `component.jsx`: React / JSX variant with Headless UI / modern component patterns
  - `component.vue`: Vue 3 Single File Component variant
  - `preview.html`: Self-contained, rendered preview for local offline testing
  - `metadata.json`: Component UUID, dimensions, credit info, and options
- **Full Templates & Kits**:
  - Downloads all 14 standalone website templates and kits (Catalyst UI Kit, Oatmeal, Salient, Spotlight, Radiant, Compass, Studio, Primer, Protocol, Commit, Transmit, Pocket, Syntax, Keynote).
- **Resilient & Resumable**:
  - Tracks progress in `.cache/progress.json`.
  - Safely pause and resume scraping at any time without re-downloading existing components.
- **Local Index & Search**:
  - Generates a master `manifest.json` index.
  - Fast instant CLI search across all scraped components by name, category, or product.

---

## Authentication Setup

Tailwind CSS Plus serves licensed code to authenticated accounts. Provide your credentials in [.env](file:///.env) using either option below:

### Option 1: Browser Session Cookie (Recommended)
*Works with all login providers (Google OAuth, GitHub, 2FA, or standard email/password).*

1. In your browser where you are logged in to [tailwindcss.com/plus](https://tailwindcss.com/plus), open Developer Tools (`F12`).
2. Go to **Application** > **Cookies** > `https://tailwindcss.com`.
3. Copy the value of the `tailwind_plus_session` cookie.
4. Add it to [.env](file:///.env):
   ```env
   TAILWIND_SESSION="your_session_cookie_value_here"
   ```

### Option 2: Direct Email & Password Login
If your account uses a direct email and password login:
```env
TAILWIND_EMAIL="your_email@example.com"
TAILWIND_PASSWORD="your_password"
```

---

## CLI Usage

### 1. Verify Authentication Status
Verify that your credentials in `.env` are active and that full license access is recognized:
```bash
uv run tailwind-dev-kit verify-auth
```

### 2. List the Full Catalog
Inspect all 93 subcategories and 14 templates available on Tailwind Plus:
```bash
uv run tailwind-dev-kit list-catalog
```

### 3. Run the Scraper

**Scrape everything (all components in HTML, React, Vue + all templates):**
```bash
uv run tailwind-dev-kit scrape
```

**Scrape only specific formats (e.g., React and HTML):**
```bash
uv run tailwind-dev-kit scrape --formats "html,react"
```

**Scrape only a specific product category (e.g., Application UI):**
```bash
uv run tailwind-dev-kit scrape --product "application-ui"
```

**Scrape components only without templates:**
```bash
uv run tailwind-dev-kit scrape --no-templates
```

**Test run on the first 5 components:**
```bash
uv run tailwind-dev-kit scrape --limit 5
```

**Custom output directory:**
```bash
uv run tailwind-dev-kit scrape --output ./my_components
```

### 4. Search Local Components
Search through your downloaded component catalog:
```bash
uv run tailwind-dev-kit search "modal"
uv run tailwind-dev-kit search "hero"
uv run tailwind-dev-kit search "table"
```

### 5. Download & Sync Template Screens
Download all 318 official template screenshots, banners, and preview screens locally:
```bash
uv run tailwind-dev-kit download-screens
```

### 6. Start the MCP Server (Model Context Protocol)
Run the built-in MCP server for seamless AI pair programming tool integration:
```bash
uv run tailwind-dev-kit mcp
```
The server exposes high-level tools:
- `search_components`: Search components by keyword or category
- `get_component_code`: Retrieve exact React JSX, HTML, or Vue source code
- `get_catalyst_component`: Get Catalyst UI Kit component code (.tsx / .jsx)
- `list_categories`: Browse all 93 subcategories with item counts
- `list_templates`: Check availability of all 14 standalone templates
- `get_template_info`: Full template stack, archive path, and local screens

### 7. Workspace Agent Skill
A native Agent Skill is configured in [.agents/skills/tailwind-plus/SKILL.md](file:///.agents/skills/tailwind-plus/SKILL.md) and automatically discovered by Antigravity IDE and compatible AI coding assistants.

---

## Scraped Directory Structure

```text
scraped_components/
  manifest.json                         # Master searchable index
  marketing/
    page-sections/
      hero-sections/
        01-simple-centered/
          component.html                # HTML (Tailwind v4)
          component.jsx                 # React JSX
          component.vue                 # Vue SFC
          preview.html                  # Standalone offline preview
          metadata.json                 # Component metadata & IDs
        ...
  application-ui/
    forms/
      input-groups/
        ...
  ecommerce/
    components/
      shopping-carts/
        ...
  ui-kit/
    catalyst/                           # Unpacked Catalyst Application UI Kit
      typescript/                       # 27 production components in TypeScript (.tsx)
      javascript/                       # 27 components in JavaScript (.jsx)
      demo/                             # Complete Next.js demo applications
  templates/
    screens/                            # 318 high-resolution screenshots & banners
      catalyst/                         # Dashboard & detail screenshots
      oatmeal/                          # 205 screens across all 12 themes
      radiant/, salient/, ...           # Hero banners, Twitter cards, previews
    oatmeal-themes/                     # All 12 Oatmeal theme .zip archives
    catalyst.zip, radiant.zip, ...      # Standalone website template .zip archives
    catalyst.json, radiant.json, ...    # Full metadata, tech stacks, and screen paths
```
