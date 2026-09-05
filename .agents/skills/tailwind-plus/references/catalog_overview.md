# Tailwind CSS Plus Catalog Overview

This reference document outlines the complete inventory of 657 official components across 93 subcategories, plus all 14 standalone website templates and kits.

---

## 1. Standalone Website Templates & UI Kits (14)

All templates are archived as full `.zip` bundles in `scraped_components/templates/`:

## 1. Standalone Website Templates & UI Kits (14)

### Template Inventory Summary

| Template | Type | Archive File | Size | Screens | Key Tech Stack | Live Demo / Preview |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **Catalyst** | Application UI Kit | `catalyst.zip` | 4.6 MB | 5 screens | React 19, Next.js 16, Headless UI, Tailwind v4 | [catalyst.tailwindui.com](https://catalyst.tailwindui.com/docs) |
| **Oatmeal** | SaaS Marketing Kit | `oatmeal.zip` (+12 themes) | 3.2 MB | 205 screens | Next.js 16, React 19, Tailwind v4, Framer Motion | [Preview Live](https://tailwindcss.com/plus/kits/oatmeal/preview?theme=olive_instrument) |
| **Radiant** | SaaS Marketing Site | `radiant.zip` | 32.2 MB | 9 screens | Next.js 16, React 19, Sanity v3.5, Framer Motion | [Preview Live](https://tailwindcss.com/plus/templates/radiant/preview) |
| **Salient** | SaaS Landing & App | `salient.zip` | 3.1 MB | 9 screens | Next.js 16, React 19, Headless UI v2.1, Tailwind v4 | [Preview Live](https://tailwindcss.com/plus/templates/salient/preview) |
| **Spotlight** | Developer Portfolio | `spotlight.zip` | 19.2 MB | 9 screens | Next.js 16, React 19, MDX v3, Headless UI | [Preview Live](https://tailwindcss.com/plus/templates/spotlight/preview) |
| **Studio** | Agency Website | `studio.zip` | 26.0 MB | 9 screens | Next.js 16, React 19, MDX v2.3, Framer Motion | [Preview Live](https://tailwindcss.com/plus/templates/studio/preview) |
| **Primer** | Infoproduct / Book | `primer.zip` | 9.3 MB | 9 screens | Next.js 16, React 19, Headless UI v2.1, Tailwind v4 | [Preview Live](https://tailwindcss.com/plus/templates/primer/preview) |
| **Protocol** | API Documentation | `protocol.zip` | 318 KB | 9 screens | Next.js 16, React 19, Markdoc v3, Headless UI | [Preview Live](https://tailwindcss.com/plus/templates/protocol/preview) |
| **Commit** | Changelog Site | `commit.zip` | 1.7 MB | 9 screens | Next.js 16, React 19, MDX v3, Tailwind v4 | [Preview Live](https://tailwindcss.com/plus/templates/commit/preview) |
| **Transmit** | Podcast Website | `transmit.zip` | 375 KB | 9 screens | Next.js 16, React 19, Tailwind v4, HTML5 Audio | [Preview Live](https://tailwindcss.com/plus/templates/transmit/preview) |
| **Pocket** | Mobile App Landing | `pocket.zip` | 247 KB | 9 screens | Next.js 16, React 19, Headless UI v2.1, Tailwind v4 | [Preview Live](https://tailwindcss.com/plus/templates/pocket/preview) |
| **Syntax** | Documentation Site | `syntax.zip` | 1.3 MB | 9 screens | Next.js 16, React 19, Markdoc v0.1, Headless UI | [Preview Live](https://tailwindcss.com/plus/templates/syntax/preview) |
| **Keynote** | Conference Website | `keynote.zip` | 19.2 MB | 9 screens | Next.js 16, React 19, Headless UI v2.1, Tailwind v4 | [Preview Live](https://tailwindcss.com/plus/templates/keynote/preview) |
| **Compass** | Course Platform | `compass.zip` | 1.9 MB | 9 screens | Next.js 16, React 19, MDX v3, Tailwind v4 | [Preview Live](https://tailwindcss.com/plus/templates/compass/preview) |

> [!TIP]
> **Offline Template Screens & Images Available**: All 318 official template screenshots, banners, detail views, and theme variations are stored locally in `scraped_components/templates/screens/<slug>/` (~101 MB total). You can view them directly without an internet connection!

---

### Detailed Template Profiles

#### 1. Catalyst (Application UI Kit)
- **Summary**: Modern, opinionated application UI kit built with React and Tailwind CSS.
- **Description**: Designed as a starter kit for building your own component systems. Includes 27 production-grade core application components with dual TypeScript (`.tsx`) and JavaScript (`.jsx`) implementations, plus complete Next.js demo applications.
- **Components Included**: `alert`, `auth-layout`, `avatar`, `badge`, `button`, `checkbox`, `combobox`, `description-list`, `dialog`, `divider`, `dropdown`, `fieldset`, `heading`, `input`, `link`, `listbox`, `navbar`, `pagination`, `radio`, `select`, `sidebar`, `sidebar-layout`, `stacked-layout`, `switch`, `table`, `text`, `textarea`.
- **Extracted Location**: `scraped_components/ui-kit/catalyst/`

#### 2. Oatmeal (SaaS Marketing Kit — 12 Themes)
- **Summary**: A calm marketing site kit with multiple themes, flexible enough for any SaaS or startup project.
- **Themes (12 Archives)**: Combinations of 4 palettes (*Mauve*, *Mist*, *Olive*, *Taupe*) and 3 fonts (*Familjen*, *Instrument*, *Mona*).
- **Themes Location**: `scraped_components/templates/oatmeal-themes/` (each archive ~3.2 MB)
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, Tailwind Plus Elements, TypeScript 5.9.

#### 3. Radiant (SaaS Marketing Template)
- **Summary**: A beautiful multi-page marketing website for your SaaS business.
- **Description**: Features rich bento layouts, interactive demo showcases, pricing tables, testimonials, company pages, and blog integration with Sanity CMS.
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, Framer Motion v10, TypeScript 5.8, Sanity v3.5.

#### 4. Salient (SaaS Landing & Web App)
- **Summary**: A beautiful SaaS landing page to announce your next big idea.
- **Description**: Polished hero, interactive feature tabs, testimonial carousel, pricing tiers, and pre-built authentication pages (login, registration).
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, Headless UI v2.1, TypeScript 5.8.

#### 5. Spotlight (Personal Developer Portfolio)
- **Summary**: A personal website so nice you’ll actually be inspired to write content and showcase projects.
- **Description**: Includes a timeline feed, blog/articles with MDX, project showcase cards, speaking engagements, and social links.
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, Headless UI v2.1, MDX v3, TypeScript 5.8.

#### 6. Studio (Agency Website Template)
- **Summary**: Showcase your work and find new clients with this beautiful agency site.
- **Description**: Features custom animated vector line illustrations, case study pages, client rosters, process diagrams, and contact inquiries.
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, MDX v2.3, Framer Motion v10, TypeScript 5.8.

#### 7. Primer (Book & Infoproduct Landing Page)
- **Summary**: A stunning landing page for your first course, book, or digital product.
- **Description**: Editorial long-form reading experience, chapter preview accordion, author bio, sample downloads, and pricing tiers.
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, Headless UI v2.1, TypeScript 5.8.

#### 8. Protocol (API Reference Documentation)
- **Summary**: Probably the nicest API documentation website you've ever seen.
- **Description**: Split-pane layout with persistent interactive code examples, request/response payloads, endpoint navigation, and search.
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, Headless UI v2.1, Markdoc v3, TypeScript 5.8.

#### 9. Commit (Product Changelog Template)
- **Summary**: Share your work in progress with this beautiful changelog template.
- **Description**: Reverse-chronological timeline layout, version tags, image galleries, release badge callouts, and RSS support.
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, MDX v3, TypeScript 5.8.

#### 10. Transmit (Podcast Website Template)
- **Summary**: A clean and professional podcast template fit for any show.
- **Description**: Built-in HTML5 sticky audio player, episode playlists, guest bios, sponsor spots, and streaming platform badges (Apple Podcasts, Spotify).
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, TypeScript 5.8.

#### 11. Pocket (Mobile App Landing Page)
- **Summary**: The perfect website template for your exciting new mobile app.
- **Description**: Photorealistic smartphone mockups, feature cards, user reviews, download CTA badges (App Store, Google Play), and FAQs.
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, Headless UI v2.1, TypeScript 5.8.

#### 12. Syntax (Documentation Site Template)
- **Summary**: Educate your users in style with this documentation site template.
- **Description**: Clean documentation hierarchy, instant client-side search, callout boxes, syntax-highlighted code blocks, and next/prev page navigation.
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, Headless UI v2.1, Markdoc v0.1, TypeScript 5.8.

#### 13. Keynote (Conference & Event Template)
- **Summary**: Launch your next conference with a splash with this modern event template.
- **Description**: Multi-day schedule breakdown, speaker cards with social links, venue maps, sponsor grids, and ticket registration tiers.
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, Headless UI v2.1, TypeScript 5.8.

#### 14. Compass (Course & Learning Platform)
- **Summary**: A clean and sophisticated starter kit for publishing online courses.
- **Description**: Video lesson player view, modular curriculum outline, instructor profiles, student feedback, and resource downloads.
- **Technologies**: Next.js 16, React 19, Tailwind CSS v4.3, MDX v3, TypeScript 5.8.

---

## 2. UI Blocks Taxonomy (93 Subcategories)

### A. Marketing (33 Subcategories)

#### Page Sections
- **Hero Sections** (12 components): Centered, split with screenshot, angled images, image tiles, phone mockups
- **Feature Sections** (19 components): Grid, bento style, offset columns, alternating panels
- **Bento Grids** (4 components): 3-column, 4-column modern card grids with dark mode
- **CTA Sections** (10 components): Simple centered, cards, background glow
- **Pricing Sections** (12 components): 2-tier, 3-tier, 4-tier, toggle monthly/annual, comparison tables
- **Header Sections** (11 components): Simple, centered with badge, left-aligned
- **Newsletter Sections** (6 components): Stacked, side-by-side, cards
- **Stats** (8 components): Simple, grid, timeline, with descriptions
- **Testimonials** (8 components): Large avatar, grids, subtle cards, star ratings
- **Blog Sections** (6 components): 3-column cards, with authors, dates, tags
- **Contact Sections** (5 components): Split with map, centered cards, simple form
- **Team Sections** (9 components): Round avatars, cards with social links
- **Content Sections** (8 components): Two-column, long-form editorial, with image float
- **Logo Clouds** (6 components): Simple row, grid, split with CTA
- **FAQs** (8 components): Accordion, side-by-side, centered list
- **Footers** (8 components): Multi-column with newsletter, simple centered, social icons

#### Elements
- **Headers & Navbars** (8 components): Flyout menus, mobile drawers, search bars
- **Flyout Menus** (7 components): Simple list, two-column with icons, full-width
- **Banners** (12 components): Top banner, floating announcement, with dismiss

#### Feedback
- **404 Pages** (6 components): Simple, with popular links, split with image

#### Page Examples
- **Landing Pages** (4 components): Complete full-page layouts assembled from blocks
- **Pricing Pages** (3 components): Full-page pricing with FAQs & feature matrix
- **About Pages** (3 components): Company story, mission, timeline, team
- **Contact Pages** (3 components): Complete contact pages with forms & locations

---

### B. Application UI (40 Subcategories)

#### Application Shells
- **Stacked Layouts** (9 components): Top nav with multi-tier navigation, light and dark
- **Sidebar Layouts** (8 components): Collapsible sidebar, dark sidebar, branding header
- **Multi-Column Layouts** (7 components): Three-column, split dashboard, feed panels

#### Headings
- **Page Headings** (9 components): With actions, tabs, meta stats, avatars
- **Section Headings** (10 components): With description, action button, badge
- **Card Headings** (6 components): With menu dropdown, badge, toggle

#### Data Display
- **Stats Cards** (6 components): Metric trends, icon badges, progress bars
- **Calendars** (8 components): Monthly grid, weekly view, day agenda
- **Description Lists** (6 components): Two-column, striped, card style

#### Lists
- **Tables** (19 components): Sortable, checkable rows, avatar columns, pagination
- **Grid Lists** (6 components): Contact cards, project tiles, horizontal cards
- **Stacked Lists** (13 components): Feed items, status badges, avatars, action menus
- **Feeds** (5 components): Timeline events, activity history, comments

#### Forms
- **Form Layouts** (5 components): Two-column, stacked, card sections
- **Input Groups** (22 components): Leading icon, trailing button, inline addon, validation
- **Select Menus** (6 components): Custom dropdowns, avatar select, multi-select
- **Sign-in & Registration** (5 components): Split with image, centered card, social auth
- **Textareas** (5 components): Markdown editor, expandable, toolbar
- **Radio Groups** (9 components): Cards, color pickers, stacked list
- **Checkboxes** (4 components): Simple, with description, list
- **Toggles** (5 components): Simple switch, icon toggle, short label
- **Action Panels** (8 components): Callout cards, billing alerts, API key generation
- **Comboboxes** (4 components): Autocomplete, command palette search

#### Navigation
- **Pagination** (4 components): Card footer, simple numbered, previous/next buttons
- **Tabs** (7 components): Underline, pills, full-width, mobile dropdown
- **Vertical Navigation** (6 components): Sidebar links with count badges
- **Breadcrumbs** (4 components): Chevrons, slashes, bar style
- **Steps** (7 components): Progress wizard, circles, timeline, panels
- **Command Palettes** (9 components): Spotlight style, with groups, quick actions
- **Navbars** (4 components): Application header bars with search and profile dropdown

#### Overlays
- **Modal Dialogs** (6 components): Centered single action, wide buttons, alert dialogs
- **Slide-overs / Drawers** (12 components): Side panels, user profile drawer, form editor
- **Notifications / Toasts** (6 components): Top-right float, avatar alert, undo action
- **Dropdowns** (8 components): Menu items, icons, dividing lines, avatar trigger

#### Elements
- **Avatars** (10 components): Stacked group, presence indicator, initials
- **Badges** (12 components): Pill badges, status dots, dismissible
- **Buttons** (8 components): Primary, secondary, icon button, leading/trailing icons
- **Button Groups** (4 components): Joined buttons, dropdown button combo
- **Dividers** (7 components): With title, with icon, with toolbar buttons

---

### C. Ecommerce (20 Subcategories)

#### Components
- **Product Overviews** (6 components): Image gallery, color selector, add to cart
- **Product Lists** (11 components): Grid with hover effects, card tiles, quick view
- **Category Filters** (6 components): Sidebar filters, mobile drawer, dropdown pills
- **Product Quickviews** (4 components): Modal quick inspection
- **Shopping Carts** (6 components): Slide-over drawer, popover summary, full page
- **Category Previews** (6 components): Image cards, mosaic, collections
- **Product Features** (9 components): Alternating rows, spec tables, icon grids
- **Store Navigation** (5 components): Mega menus, mobile navigation
- **Promo Sections** (8 components): Hero banners, image grids, countdowns
- **Checkout Forms** (5 components): Single-page checkout, multi-step, summary sidebar
- **Reviews** (4 components): Rating breakdown, user testimonials, verified badges
- **Order Summaries** (4 components): Receipt breakdown, line items, shipment tracker
- **Order History** (4 components): Past orders table, expandable detail cards
- **Storefront Pages** (4 components): Complete retail homepages
- **Product Pages** (5 components): Complete e-commerce product pages
- **Category Pages** (5 components): Complete catalog browsing pages
- **Shopping Cart Pages** (3 components): Full checkout preparatory pages
- **Checkout Pages** (3 components): Full checkout order processing pages
- **Order Detail Pages** (3 components): Post-purchase order fulfillment views
