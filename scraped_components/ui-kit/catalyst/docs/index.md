# Getting Started — Catalyst UI Kit Documentation

> Official documentation from [catalyst.tailwindui.com/docs](https://catalyst.tailwindui.com/docs)

# Getting started

> Catalyst is a starter kit for building your own component systems with React and Tailwind CSS — designed and developed by the Tailwind CSS team. It's a collection of beautiful, production-ready UI components you drop into your projects alongside your own code that are yours to customize, adapt, and make your own.

Open in new tab

## Before you start

Before you do anything else, make sure you've got a Tailwind CSS project set up that you'd like to use with Catalyst.
Catalyst is built with React but isn't coupled to any specific React framework and can be used with Next.js, Remix,
Inertia, or in any other React project.

For help creating a project and configuring Tailwind CSS, check out the
framework guides in the Tailwind CSS documentation.

Catalyst is built around Tailwind's default theme configuration and relies on the default spacing scale, color palette,
shadow scale, and more. You're of course free to customize anything you like, but you won't get the expected results
out-of-the-box if you've made significant changes to the default theme and will need to edit the components to adapt
them for your customizations.

## Adding Catalyst to your project

To get started with Catalyst, first
download the latest version from within your Tailwind Plus
account.

Then, unzip `catalyst-ui-kit.zip` and copy the component files from either the `javascript` or `typescript` folders into
wherever you keep components in your own project:

### Installing dependencies

Next install the dependencies used by the components in Catalyst:

```tsx
npm install @headlessui/react motion clsx
```

Catalyst is also designed for the latest version of Tailwind CSS, which is currently Tailwind CSS v4.0. To make sure
that you are on the latest version of Tailwind, update it via npm:

```tsx
npm install tailwindcss@latest
```

### Client-side router integration

By default, the `Link` component in Catalyst renders a plain HTML `<a>` element. You should update this component in
your `link.tsx` or `link.jsx` file to use the link component provided by whichever framework or routing library you're
using in your project.

```tsx
import * as Headless from '@headlessui/react'
 import React, { forwardRef } from 'react'
 import NextLink, { type LinkProps } from 'next/link'

 export const Link = forwardRef(function Link(
   props: { href: string } & React.ComponentPropsWithoutRef<'a'>,
   props: LinkProps & React.ComponentPropsWithoutRef<'a'>,
   ref: React.ForwardedRef<HTMLAnchorElement>
 ) {
   return (
     <Headless.DataInteractive>
       <a {...props} ref={ref} />
       <NextLink {...props} ref={ref} />
     </Headless.DataInteractive>
   )
 })
```

We've provided ready-to-go examples for Next.js, Remix, and
Inertia.js at the bottom of this page.

### Optional: Setup Inter font family

We've designed Catalyst using Inter to ensure that the components look the same in all browsers
and operating systems.

If you'd like to use Inter in your own projects, start by checking the documentation for the framework you're using —
it's not uncommon for frameworks to have
dedicated APIs for configuring custom fonts to
simplify the developer experience.

If the framework you're using doesn't have a recommended way of setting up custom fonts, the easiest way to add Inter is
by pointing a `<link>` tag to the CDN:

```tsx
<link rel="stylesheet" href="https://rsms.me/inter/inter.css" />
```

Then update the `--font-sans` theme variable in your project to use Inter:

```tsx
@theme {
  --font-sans: Inter, sans-serif;
  --font-sans--font-feature-settings: 'cv11';
}
```

### Optional: Install Heroicons

We're using our own Heroicons icon set in Catalyst any time we need icons, and Heroicons has
been designed to integrate seamlessly with Catalyst projects.

If you'd like to use Heroicons in your own projects, you can install it via npm:

```tsx
npm install @heroicons/react
```

Most components in Catalyst — like the `Button`, `DropdownItem`, and `ListboxOption` components — are designed to work
best with 16×16 icons, so for these components import the icons you need from `@heroicons/react/16/solid`:

```tsx
import { Button } from '@/components/button'
import { PlusIcon } from '@heroicons/react/16/solid'

function Example() {
  return (
    <Button>
      <PlusIcon />
      Add item
    </Button>
  )
}
```

The only exceptions are the `NavbarItem` and `SidebarItem` components which are designed for 20×20 icons. For
these components, import from `@heroicons/react/20/solid` instead:

```tsx
import { SidebarItem, SidebarLabel } from '@/components/sidebar'
import { HomeIcon } from '@heroicons/react/20/solid'

function Example() {
  return (
    <SidebarItem href="/home">
      <HomeIcon />
      <SidebarLabel>Home</SidebarLabel>
    </SidebarItem>
  )
}
```

## Framework integration examples

By default, the `Link` component in Catalyst renders a plain HTML `<a>` element. These examples show you how to update
your `Link` component to use the `Link` component provided by your framework or routing library.

### Integrating with Next.js

Update your `link.tsx` or `link.jsx` file to use the `Link` component from Next.js:

```tsx
import * as Headless from '@headlessui/react'
import NextLink, { type LinkProps } from 'next/link'
import React, { forwardRef } from 'react'

export const Link = forwardRef(function Link(
  props: LinkProps & React.ComponentPropsWithoutRef<'a'>,
  ref: React.ForwardedRef<HTMLAnchorElement>
) {
  return (
    <Headless.DataInteractive>
      <NextLink {...props} ref={ref} />
    </Headless.DataInteractive>
  )
})
```

### Integrating with Remix

Update your `link.tsx` or `link.jsx` file to use the `Link` component from Remix:

```tsx
import * as Headless from '@headlessui/react'
import { Link as RemixLink, type LinkProps } from '@remix-run/react'
import React, { forwardRef } from 'react'

export const Link = forwardRef(function Link(
  props: { href: string | LinkProps['to'] } & Omit<LinkProps, 'to'>,
  ref: React.ForwardedRef<HTMLAnchorElement>
) {
  return (
    <Headless.DataInteractive>
      <RemixLink {...props} to={props.href} ref={ref} />
    </Headless.DataInteractive>
  )
})
```

### Integrating with Inertia.js

Update your `link.tsx` or `link.jsx` file to use the `Link` component from Inertia.js:

```tsx
import * as Headless from '@headlessui/react'
import { Link as InertiaLink, type InertiaLinkProps } from '@inertiajs/react'
import React, { forwardRef } from 'react'

export const Link = forwardRef(function Link(props: InertiaLinkProps, ref: React.ForwardedRef<HTMLAnchorElement>) {
  return (
    <Headless.DataInteractive>
      <InertiaLink {...props} ref={ref} />
    </Headless.DataInteractive>
  )
})
```
