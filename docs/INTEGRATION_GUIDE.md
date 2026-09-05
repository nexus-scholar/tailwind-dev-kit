# Tailwind Dev Kit — Project Integration & Usage Guide

A comprehensive guide on leveraging **Tailwind Dev Kit** across your current and future web development projects. This guide covers AI pair-programming with the Model Context Protocol (MCP), global IDE skills, dropping the Catalyst UI Kit into Next.js/React apps, bootstrapping production sites from standalone templates, and extracting individual components in HTML, React, or Vue.

---

## Table of Contents

1. [Asset Inventory Overview](#1-asset-inventory-overview)
2. [Strategy 1: AI Pair-Programming with MCP Server](#2-strategy-1-ai-pair-programming-with-mcp-server)
   - [Setup in Antigravity IDE](#setup-in-antigravity-ide)
   - [Setup in Claude Desktop](#setup-in-claude-desktop)
   - [Setup in Cursor](#setup-in-cursor)
   - [Available MCP Tools & Signatures](#available-mcp-tools--signatures)
   - [Example AI Prompts](#example-ai-prompts)
3. [Strategy 2: Global Agent Skill Configuration](#3-strategy-2-global-agent-skill-configuration)
   - [Activating Globally across all Workspaces](#activating-globally-across-all-workspaces)
   - [How the AI Uses the Skill](#how-the-ai-uses-the-skill)
4. [Strategy 3: Using the Catalyst Application UI Kit](#4-strategy-3-using-the-catalyst-application-ui-kit)
   - [Component Inventory (27 Core Components)](#component-inventory-27-core-components)
   - [Step-by-Step Next.js 15/16 + Tailwind CSS v4 Setup](#step-by-step-nextjs-1516--tailwind-css-v4-setup)
   - [Example: Building a Dashboard Layout with Catalyst](#example-building-a-dashboard-layout-with-catalyst)
5. [Strategy 4: Bootstrapping Production Templates](#5-strategy-4-bootstrapping-production-templates)
   - [Template Catalog & Best Use Cases](#template-catalog--best-use-cases)
   - [Quick-Start: Unpacking & Launching a Template](#quick-start-unpacking--launching-a-template)
   - [Working with Oatmeal’s 12 Pre-Styled Themes](#working-with-oatmeals-12-pre-styled-themes)
6. [Strategy 5: Direct Component Extraction (HTML / React / Vue)](#6-strategy-5-direct-component-extraction-html--react--vue)
   - [Fast CLI Search](#fast-cli-search)
   - [Inspecting & Copying Component Source](#inspecting--copying-component-source)
   - [Offline Previews & Screen Inspiration](#offline-previews--screen-inspiration)
7. [Workflow Cheat Sheet](#7-workflow-cheat-sheet)

---

## 1. Asset Inventory Overview

Your local toolkit contains a complete, self-contained library:

```text
scraped_components/
├── marketing/                          # Marketing blocks (heroes, bento grids, pricing, etc.)
├── application-ui/                     # App UI blocks (sidebars, tables, modals, forms, etc.)
├── ecommerce/                          # Ecommerce blocks (product pages, carts, checkout, etc.)
├── ui-kit/
│   └── catalyst/                       # Catalyst Application UI Kit (Next.js + Tailwind v4)
│       ├── typescript/                 # 27 production components in TypeScript (.tsx)
│       ├── javascript/                 # 27 components in JavaScript (.jsx)
│       └── demo/                       # Full reference demo applications
├── templates/
│   ├── screens/                        # 318 high-resolution screenshots & banners
│   │   ├── catalyst/                   # 5 screens
│   │   ├── oatmeal/                    # 205 screens (12 themes × light/dark variants)
│   │   └── radiant/, salient/, ...     # 9 screens each (hero, twitter, previews, details)
│   ├── oatmeal-themes/                 # 12 ready-to-run Oatmeal theme .zip archives
│   ├── catalyst.zip, radiant.zip, ...  # Standalone template .zip archives
│   └── catalyst.json, radiant.json, .. # Complete metadata, tech stacks, and preview URLs
└── manifest.json                       # Master searchable index (657 components, 14 templates)
```

---

## 2. Strategy 1: AI Pair-Programming with MCP Server

The toolkit includes a built-in **Model Context Protocol (MCP)** server over standard input/output (stdio). When registered in your AI tools, the assistant can query your local dataset on demand.

### Setup in Antigravity IDE

Add the server to your global configuration file at `C:\Users\mouadh\.gemini\config\mcp_config.json`:

```json
{
  "mcpServers": {
    "tailwind-plus": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\mouadh\\Documents\\tailwind-dev-kit",
        "run",
        "tailwind-dev-kit",
        "mcp"
      ]
    }
  }
}
```

### Setup in Claude Desktop

Open `%APPDATA%\Claude\claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    "tailwind-plus": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\mouadh\\Documents\\tailwind-dev-kit",
        "run",
        "tailwind-dev-kit",
        "mcp"
      ]
    }
  }
}
```

### Setup in Cursor

In Cursor settings under **Features > MCP Servers**, add a new stdio server:
- **Name**: `tailwind-plus`
- **Command**: `uv --directory "C:\Users\mouadh\Documents\tailwind-dev-kit" run tailwind-dev-kit mcp`

---

### Available MCP Tools & Signatures

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `search_components` | `query: str`, `product?: str`, `category?: str`, `limit?: int` | Searches components by keyword, product, or category across all 657 items. |
| `get_component_code` | `identifier: str`, `format: str = "react"` | Returns exact code for React (`react`), HTML (`html`), or Vue (`vue`). |
| `get_catalyst_component` | `name: str`, `language: str = "typescript"` | Returns source code for any Catalyst UI component in `.tsx` or `.jsx`. |
| `list_categories` | `product?: str` | Lists all 93 subcategories with item counts. |
| `list_templates` | *(none)* | Lists all 14 standalone templates and local `.zip` statuses. |
| `get_template_info` | `slug: str` | Returns full summary, technologies, demo URL, and local screens path. |

---

### Example AI Prompts

Once the MCP server is configured, you can prompt your AI directly in any workspace:

- *"Search for a dark-mode pricing table from Tailwind Plus and adapt it into my `PricingSection.tsx`."*
- *"Import the Catalyst dropdown and button components into my project."*
- *"Show me what themes are available for Oatmeal and what their color palettes are."*
- *"Find an ecommerce product overview component in React and paste the code here."*

The AI will invoke the local tools, retrieve the exact verified code, and adapt it to your active project.

---

## 3. Strategy 2: Global Agent Skill Configuration

Antigravity IDE and compatible agents support **Agent Skills** (directory bundles containing instructions and catalog indices).

### Activating Globally across all Workspaces

By copying the skill into your global Antigravity config directory, every project you open will automatically recognize the skill:

```powershell
# Run once from PowerShell:
Copy-Item -Recurse -Force `
  "C:\Users\mouadh\Documents\tailwind-dev-kit\.agents\skills\tailwind-plus" `
  "C:\Users\mouadh\.gemini\config\skills\tailwind-plus"
```

### How the AI Uses the Skill

When active, the AI automatically:
1. Reads `catalog_overview.md` to see all 93 subcategories and 14 templates without making web requests.
2. Identifies exact component paths in `scraped_components/`.
3. Follows Tailwind CSS v4 best practices (e.g. `@import "tailwindcss";`, `@theme` directives, headless state management).

---

## 4. Strategy 3: Using the Catalyst Application UI Kit

**Catalyst** is Tailwind Labs' official application UI kit designed for modern SaaS and internal tools. Your toolkit contains the completely unpacked source in:
`scraped_components/ui-kit/catalyst/`

### Component Inventory (27 Core Components)

Located in `typescript/` (for TypeScript projects) and `javascript/` (for JS projects):

- **Layout & Structure**: `sidebar-layout`, `stacked-layout`, `auth-layout`, `navbar`, `sidebar`, `divider`
- **Forms & Inputs**: `button`, `input`, `textarea`, `checkbox`, `radio`, `switch`, `select`, `combobox`, `listbox`, `fieldset`
- **Overlays & Feedback**: `dialog` (modals), `dropdown`, `alert`, `badge`
- **Data Display**: `table`, `description-list`, `avatar`, `heading`, `text`, `link`, `pagination`

---

### Step-by-Step Next.js 15/16 + Tailwind CSS v4 Setup

#### Step 1: Create or open your Next.js project
```bash
npx create-next-app@latest my-app --typescript --tailwind --app --eslint
cd my-app
```

#### Step 2: Install headless dependencies
Catalyst components rely on Headless UI and clsx:
```bash
npm install @headlessui/react clsx
```

#### Step 3: Copy Catalyst components into your app
```powershell
# Copy the 27 components into your project's src/components/catalyst directory
New-Item -ItemType Directory -Force -Path "src\components\catalyst"
Copy-Item -Path "C:\Users\mouadh\Documents\tailwind-dev-kit\scraped_components\ui-kit\catalyst\typescript\*" `
          -Destination "src\components\catalyst\"
```

#### Step 4: Verify Tailwind CSS v4 stylesheet
In `src/app/globals.css`:
```css
@import "tailwindcss";
```

---

### Example: Building a Dashboard Layout with Catalyst

In your `src/app/dashboard/layout.tsx`:

```tsx
import { SidebarLayout } from '@/components/catalyst/sidebar-layout'
import { Sidebar, SidebarHeader, SidebarBody, SidebarItem, SidebarLabel } from '@/components/catalyst/sidebar'
import { Navbar, NavbarItem, NavbarSpacer } from '@/components/catalyst/navbar'
import { Avatar } from '@/components/catalyst/avatar'

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarLayout
      navbar={
        <Navbar>
          <NavbarSpacer />
          <NavbarItem href="/profile">
            <Avatar src="/avatar.jpg" className="size-8" />
          </NavbarItem>
        </Navbar>
      }
      sidebar={
        <Sidebar>
          <SidebarHeader>
            <span className="font-semibold text-lg text-zinc-950 dark:text-white">My SaaS</span>
          </SidebarHeader>
          <SidebarBody>
            <SidebarItem href="/dashboard" current>
              <SidebarLabel>Dashboard</SidebarLabel>
            </SidebarItem>
            <SidebarItem href="/orders">
              <SidebarLabel>Orders</SidebarLabel>
            </SidebarItem>
            <SidebarItem href="/settings">
              <SidebarLabel>Settings</SidebarLabel>
            </SidebarItem>
          </SidebarBody>
        </Sidebar>
      }
    >
      {children}
    </SidebarLayout>
  )
}
```

---

## 5. Strategy 4: Bootstrapping Production Templates

When you need a complete website (not just isolated components), use the 14 standalone templates located in `scraped_components/templates/`.

### Template Catalog & Best Use Cases

| Template | Slug | Best Use Case | Primary Framework |
| :--- | :--- | :--- | :--- |
| **Radiant** | `radiant` | Multi-page B2B SaaS marketing site | Next.js 16, React 19, Sanity CMS, Framer Motion |
| **Salient** | `salient` | Classic SaaS landing page + auth forms | Next.js 16, React 19, Headless UI |
| **Spotlight** | `spotlight` | Developer portfolio, personal website & blog | Next.js 16, MDX v3 |
| **Studio** | `studio` | Creative agency, design studio, client roster | Next.js 16, MDX, animated SVG line art |
| **Primer** | `primer` | E-book, digital product, course sales page | Next.js 16, Headless UI |
| **Protocol** | `protocol` | REST / GraphQL API documentation | Next.js 16, Markdoc v3 |
| **Syntax** | `syntax` | General software documentation portal | Next.js 16, Markdoc |
| **Commit** | `commit` | Developer changelog & product release notes | Next.js 16, MDX v3 |
| **Transmit** | `transmit` | Podcast website with audio player | Next.js 16, HTML5 Audio |
| **Pocket** | `pocket` | Mobile app showcase & download page | Next.js 16, Headless UI |
| **Keynote** | `keynote` | Tech conference & event schedule | Next.js 16, Headless UI |
| **Compass** | `compass` | Interactive online course platform | Next.js 16, MDX v3 |
| **Oatmeal** | `oatmeal` | Multi-theme calm marketing site (12 themes) | Next.js 16, Tailwind Plus Elements |

---

### Quick-Start: Unpacking & Launching a Template

```powershell
# 1. Unzip chosen template into your target project directory
Expand-Archive `
  -Path "C:\Users\mouadh\Documents\tailwind-dev-kit\scraped_components\templates\radiant.zip" `
  -DestinationPath "C:\Users\mouadh\Documents\my-saas-website"

# 2. Navigate and install dependencies
cd C:\Users\mouadh\Documents\my-saas-website
npm install

# 3. Start local development server
npm run dev
```

---

### Working with Oatmeal’s 12 Pre-Styled Themes

Oatmeal offers 12 pre-configured color and typography pairings. All 12 archives are ready in `scraped_components/templates/oatmeal-themes/`:

- **Mauve**: `oatmeal-mauve-familjen.zip`, `oatmeal-mauve-instrument.zip`, `oatmeal-mauve-mona.zip`
- **Mist**: `oatmeal-mist-familjen.zip`, `oatmeal-mist-instrument.zip`, `oatmeal-mist-mona.zip`
- **Olive**: `oatmeal-olive-familjen.zip`, `oatmeal-olive-instrument.zip`, `oatmeal-olive-mona.zip`
- **Taupe**: `oatmeal-taupe-familjen.zip`, `oatmeal-taupe-instrument.zip`, `oatmeal-taupe-mona.zip`

Pick the archive that matches your brand style, unzip it, and run `npm install`.

---

## 6. Strategy 5: Direct Component Extraction (HTML / React / Vue)

If you just need a single hero, modal, or pricing table:

### Fast CLI Search

Use the built-in search command:

```bash
uv run tailwind-dev-kit search "pricing"
uv run tailwind-dev-kit search "bento"
uv run tailwind-dev-kit search "stats"
uv run tailwind-dev-kit search "navbar"
```

The output gives you the exact subcategory path and component name.

### Inspecting & Copying Component Source

Navigate to the directory:
```text
scraped_components/marketing/page-sections/pricing-sections/02-three-tiers-with-toggle/
├── component.html      # Copy if using plain HTML, Astro, or non-React
├── component.jsx       # Copy if using React, Next.js, Remix, Vite
├── component.vue       # Copy if using Vue 3, Nuxt, Vite Vue
├── preview.html        # Open in any browser to see the live rendering
└── metadata.json       # Dimensions and UUID
```

### Offline Previews & Screen Inspiration

- **Component Previews**: Double-click any `preview.html` file to test animations and responsiveness offline in your browser.
- **Template Screens**: Open `scraped_components/templates/screens/` in your image viewer or file explorer to browse high-definition screenshots without needing an internet connection.

---

## 7. Workflow Cheat Sheet

| Task | Command or Action |
| :--- | :--- |
| **Search components locally** | `uv run tailwind-dev-kit search "<keyword>"` |
| **List entire catalog** | `uv run tailwind-dev-kit list-catalog` |
| **Sync / update offline screens** | `uv run tailwind-dev-kit download-screens` |
| **Rebuild manifest index** | `uv run tailwind-dev-kit rebuild-manifest` |
| **Start MCP server** | `uv run tailwind-dev-kit mcp` |
| **Copy Catalyst UI Kit** | Source: `scraped_components/ui-kit/catalyst/typescript/` |
| **Deploy starter website** | Unzip from `scraped_components/templates/<slug>.zip` |
