---
name: tailwind-plus
description: >-
  Search, inspect, and retrieve official Tailwind CSS Plus (Tailwind UI) components (HTML, React/JSX, Vue 3) and full website templates. Use when the user asks for UI components (heroes, navbars, modals, pricing, bento grids, tables, checkout, etc.) styled with Tailwind CSS v4, offline browser previews, or standalone website templates (Catalyst, Salient, Radiant, etc.).
---

# Tailwind CSS Plus (Tailwind UI) Component & Template Skill

This skill guides the agent in searching, retrieving, and integrating official **Tailwind CSS Plus** UI components and full website templates from the local `scraped_components` catalog.

---

## 1. What's Available in This Workspace

The local catalog contains **657 official components** across **93 subcategories** and **14 standalone website templates**:

- **Products**:
  - `Marketing`: Heroes, Feature Sections, Bento Grids, Pricing, Testimonials, Footers, Navbars, 404s, Landing Pages
  - `Application UI`: Stacked/Sidebar Shells, Tables, Input Groups, Modals, Slide-overs, Command Palettes, Steps, Stats
  - `Ecommerce`: Product Overviews, Shopping Carts, Category Filters, Checkout Pages, Order History, Reviews
- **Multi-Framework Formats**:
  - `component.html`: Pure HTML with official Tailwind CSS v4 utility classes
  - `component.jsx`: React / JSX component with Headless UI and Heroicons
  - `component.vue`: Vue 3 Single File Component (SFC) with `<template>` and `<script setup>`
  - `preview.html`: Standalone rendered preview (opens offline in any web browser)
  - `metadata.json`: UUID, slug, large & small dimensions, and category taxonomy
- **Full Templates**:
  - 14 complete `.zip` application templates (Catalyst UI Kit, Oatmeal, Salient, Radiant, Spotlight, Studio, etc.) in `scraped_components/templates/`

For the complete subcategory sitemap, see [references/catalog_overview.md](./references/catalog_overview.md).

---

## 2. Searching & Retrieving Components

### Option A: Using the Tailwind Plus MCP Tools (Recommended)

If the `tailwind-plus` MCP server is active, use the dedicated tools:

1. **Search Components**:
   - `search_components(query="modal", product="Application UI", limit=10)`
   - `search_components(query="hero", product="Marketing")`
2. **Get Component Code**:
   - `get_component_code(identifier="simple-centered", format="react")`
   - `get_component_code(identifier="simple-centered", format="html")`
   - `get_component_code(identifier="simple-centered", format="vue")`
3. **Catalyst Application UI Kit**:
   - `get_catalyst_component(name="button", language="typescript")`
   - `get_catalyst_component(name="dialog", language="javascript")`
   - Directly inspect files in `scraped_components/ui-kit/catalyst/typescript` or `javascript`
4. **List Templates & Status**:
   - `list_templates()`
   - `get_template_info(slug="oatmeal")` (shows all 12 downloaded themes)
   - `get_template_info(slug="catalyst")` (shows all 27 UI kit components)

### Option B: Using the CLI

Run queries from the workspace terminal:

```bash
# Search for components
uv run tailwind-dev-kit search "pricing"
uv run tailwind-dev-kit search "bento"
uv run tailwind-dev-kit search "sidebar"

# List full taxonomy
uv run tailwind-dev-kit list-catalog

# Sync or refresh all template screenshots & preview screens locally
uv run tailwind-dev-kit download-screens

# Rebuild manifest if new components were added
uv run tailwind-dev-kit rebuild-manifest
```

### Option C: Direct File System Access

Navigate directly into `scraped_components/`:

```text
scraped_components/
├── marketing/
│   └── page-sections/
│       └── hero-sections/
│           └── 01-simple-centered/
│               ├── component.html
│               ├── component.jsx
│               ├── component.vue
│               ├── preview.html
│               └── metadata.json
├── application-ui/
├── ecommerce/
├── ui-kit/
│   └── catalyst/
│       ├── typescript/ (27 .tsx components)
│       ├── javascript/ (27 .jsx components)
│       └── demo/
├── templates/
│   ├── screens/ (318 high-res screenshots & banners)
│   │   ├── catalyst/ (5 screens)
│   │   ├── oatmeal/ (205 screens across 12 themes)
│   │   └── radiant/ (9 screens: banner, twitter, previews, details)
│   ├── oatmeal-themes/ (12 theme zip archives)
│   ├── catalyst.zip, radiant.zip, ...
│   └── catalyst.json, radiant.json, ...
└── manifest.json
```

Use `view_file` on `scraped_components/.../component.jsx`, `component.html`, or `component.vue` to inspect and copy code into your application.

---

## 3. Integrating Components into Projects

### Step 1: Tailwind CSS v4 Setup

Ensure Tailwind CSS v4 is configured in your project's main stylesheet (e.g. `src/index.css`):

```css
@import "tailwindcss";
```

### Step 2: Dependencies

For React components:
```bash
npm install @headlessui/react @heroicons/react
```

For Vue components:
```bash
npm install @headlessui/vue @heroicons/vue
```

### Step 3: Dark Mode Handling

Tailwind Plus components use native `dark:` modifier classes (e.g., `bg-white dark:bg-gray-900 text-gray-900 dark:text-white`). Ensure your app or root element toggles the `.dark` class or respects `prefers-color-scheme`.

---

## 4. UI Kit (Catalyst) & Multi-Theme Kits (Oatmeal)

### Catalyst UI Kit (Extracted & Ready)
Catalyst is fully extracted in `scraped_components/ui-kit/catalyst/`:
- **TypeScript**: `scraped_components/ui-kit/catalyst/typescript/` (27 production-ready `.tsx` components)
- **JavaScript**: `scraped_components/ui-kit/catalyst/javascript/` (27 production-ready `.jsx` components)
- **Next.js Demos**: `scraped_components/ui-kit/catalyst/demo/`
- **Component List**: `alert`, `avatar`, `badge`, `button`, `checkbox`, `combobox`, `description-list`, `dialog`, `divider`, `dropdown`, `fieldset`, `heading`, `input`, `link`, `listbox`, `navbar`, `pagination`, `radio`, `select`, `sidebar`, `sidebar-layout`, `stacked-layout`, `switch`, `table`, `text`, `textarea`.

### Oatmeal SaaS Marketing Kit (12 Themes Downloaded)
All 12 theme combinations are downloaded in `scraped_components/templates/oatmeal-themes/`:
- **Mauve**: `oatmeal-mauve-familjen.zip`, `oatmeal-mauve-instrument.zip`, `oatmeal-mauve-mona.zip`
- **Mist**: `oatmeal-mist-familjen.zip`, `oatmeal-mist-instrument.zip`, `oatmeal-mist-mona.zip`
- **Olive**: `oatmeal-olive-familjen.zip`, `oatmeal-olive-instrument.zip`, `oatmeal-olive-mona.zip`
- **Taupe**: `oatmeal-taupe-familjen.zip`, `oatmeal-taupe-instrument.zip`, `oatmeal-taupe-mona.zip`
Full metadata and color/font pairings are in `scraped_components/templates/oatmeal.json`.

---

## 5. Unpacking Standalone Templates

To inspect or start a project from an official template:

1. Locate the archive in `scraped_components/templates/<slug>.zip` (or specific theme in `oatmeal-themes/`)
2. Extract the archive into a destination folder:
   - On Windows PowerShell:
     ```powershell
     Expand-Archive -Path "scraped_components\templates\salient.zip" -DestinationPath "my-salient-app"
     ```
3. Install dependencies and run:
   ```bash
   cd my-salient-app
   npm install
   npm run dev
   ```
