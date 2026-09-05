import urllib.request
import urllib.parse
import json
import http.cookiejar

cj = http.cookiejar.CookieJar()
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return fp
    def http_error_303(self, req, fp, code, msg, headers):
        return fp

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), NoRedirect())

# 1. Get initial cookies and XSRF token
res = opener.open(urllib.request.Request('https://tailwindcss.com/plus/login', headers={'User-Agent': 'Mozilla/5.0'}))
html = res.read().decode('utf-8')

cookies = {c.name: c.value for c in cj}
xsrf = urllib.parse.unquote(cookies.get('XSRF-TOKEN', ''))
print('Initial cookies:', list(cookies.keys()))
print('XSRF token present:', bool(xsrf))

# 2. Try POST /plus/login with dummy credentials to test login mechanism
login_data = json.dumps({'email': 'test@example.com', 'password': 'dummy_password', 'remember': True}).encode('utf-8')
req = urllib.request.Request(
    'https://tailwindcss.com/plus/login',
    data=login_data,
    headers={
        'Content-Type': 'application/json',
        'X-Inertia': 'true',
        'X-Inertia-Version': '34780f1f2ee1b970f2e7ec06d306888b',
        'X-XSRF-TOKEN': xsrf,
        'User-Agent': 'Mozilla/5.0'
    }
)

try:
    res2 = opener.open(req)
    print('Login test response status:', res2.status)
    body = res2.read().decode('utf-8')
    print('Response body sample:', body[:300])
except Exception as e:
    print('Login test error:', e)
