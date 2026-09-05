import urllib.request
import urllib.parse
import json
import http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Visit page to get initial cookies and inertia version
req = urllib.request.Request('https://tailwindcss.com/plus', headers={'User-Agent': 'Mozilla/5.0'})
res = opener.open(req)
html = res.read().decode('utf-8')

# extract inertia version
import re
m_ver = re.search(r'"version":\s*"([^"]+)"', html)
version = m_ver.group(1) if m_ver else '34780f1f2ee1b970f2e7ec06d306888b'
print('Inertia version:', version)

cookies = {c.name: c.value for c in cj}
xsrf = urllib.parse.unquote(cookies.get('XSRF-TOKEN', ''))
print('XSRF:', xsrf[:30] if xsrf else 'None')

# Now make PUT request
payload = json.dumps({'uuid': 'b9bcab4538776a17fff93d18f82a8272', 'snippet_lang': 'react-v4.3'}).encode('utf-8')
put_req = urllib.request.Request(
    'https://tailwindcss.com/plus/ui-blocks/language',
    data=payload,
    method='PUT',
    headers={
        'Content-Type': 'application/json',
        'X-Inertia': 'true',
        'X-Inertia-Version': version,
        'X-XSRF-TOKEN': xsrf,
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://tailwindcss.com/plus/ui-blocks/marketing/sections/heroes'
    }
)

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_303(self, req, fp, code, msg, headers):
        return fp

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), NoRedirectHandler())

try:
    put_res = opener.open(put_req)
    print('PUT status:', put_res.status)
    loc = put_res.headers.get('Location')
    print('Redirect location:', loc)
    if loc:
        get_req = urllib.request.Request(
            loc,
            headers={
                'X-Inertia': 'true',
                'X-Inertia-Version': version,
                'User-Agent': 'Mozilla/5.0'
            }
        )
        get_res = opener.open(get_req)
        print('Follow redirect status:', get_res.status)
        data = json.loads(get_res.read().decode('utf-8'))
        c0 = data['props']['subcategory']['components'][0]
        print('C0 updated snippet lang/name:', c0['snippet']['name'], c0['snippet']['language'])
        print('C0 updated code preview:\n', c0['snippet']['code'][:200])
except Exception as e:
    print('Error:', e)
