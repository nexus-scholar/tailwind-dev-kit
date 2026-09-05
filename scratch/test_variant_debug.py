from tailwind_dev_kit.auth import create_authenticated_client
from tailwind_dev_kit.client import TailwindPlusClient

client, status = create_authenticated_client()
print('Authenticated:', status.is_authenticated)

tp = TailwindPlusClient(client)
subcats, _ = tp.get_taxonomy()
heroes = [s for s in subcats if s.name == 'Hero Sections'][0]
comps = tp.get_subcategory_components(heroes)
c0 = comps[0]
print('C0 name:', c0.name, 'UUID:', c0.uuid)
print('Initial snippet name:', c0.snippets.keys())
initial_snip = list(c0.snippets.values())[0]
print('Initial lang:', initial_snip.name, 'code sample:', initial_snip.code[:60] if initial_snip.code else 'None')

# Now request html
print('\nRequesting HTML...')
html_code = tp.fetch_snippet_variant(c0, 'html')
print('HTML code sample:\n', html_code[:100] if html_code else 'None')

# Now request vue
print('\nRequesting Vue...')
vue_code = tp.fetch_snippet_variant(c0, 'vue')
print('Vue code sample:\n', vue_code[:100] if vue_code else 'None')

# Now request react
print('\nRequesting React...')
react_code = tp.fetch_snippet_variant(c0, 'react')
print('React code sample:\n', react_code[:100] if react_code else 'None')
