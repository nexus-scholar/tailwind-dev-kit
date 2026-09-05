# Divider — Catalyst UI Kit Documentation

> Official documentation from [catalyst.tailwindui.com/docs/divider](https://catalyst.tailwindui.com/docs/divider)

# Divider

It's a line.

```tsx
import { Divider } from '@/components/divider'

function Example() {
  return <Divider />
}
```

## Component API
``````

| Prop | Default | Description |
| --- | --- | --- |
| Divider extends the JSX <hr> element |  |  |
| soft | false | Whether the divider should use a softer color. |

## Examples

### Basic example

Use the `Divider` component to add a horizontal rule between items:

### With reduced contrast

Use the `soft` prop for secondary dividers:

```tsx
import { Divider } from '@/components/divider'

function Example() {
  return <Divider soft />
}
```

### With spacing

Use utility classes like `my-*` to control the vertical spacing around a divider:

```tsx
import { Divider } from '@/components/divider'

function Example() {
  return <Divider className="my-6" />
}
```
