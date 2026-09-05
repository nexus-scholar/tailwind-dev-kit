import httpx, html, re
from tailwind_dev_kit.auth import get_stored_credentials, login_with_password, DEFAULT_USER_AGENT, BASE_URL

creds = get_stored_credentials()
client = httpx.Client(base_url=BASE_URL, headers={"User-Agent": DEFAULT_USER_AGENT})

# 1. Login with credentials
print('Logging in...')
success = login_with_password(client, creds['email'], creds['password'])
print('Login success:', success)

# 2. Get Inertia version from /plus
r_html = client.get(f"{BASE_URL}/plus", headers={"Accept": "text/html"})
unescaped = html.unescape(r_html.text)
m_ver = re.search(r'"version":\s*"([^"]+)"', unescaped)
version = m_ver.group(1) if m_ver else ""
print('Version:', version)

# 3. Request /plus with X-Inertia
r_json = client.get(
    f"{BASE_URL}/plus",
    headers={
        "X-Inertia": "true",
        "X-Inertia-Version": version,
        "Accept": "text/html, application/xhtml+xml",
        "X-Requested-With": "XMLHttpRequest",
    }
)
print('JSON status:', r_json.status_code)
if r_json.status_code == 200:
    data = r_json.json()
    auth = data.get('props', {}).get('auth')
    print('Auth:', auth)
    print('canPurchasePlus:', data.get('props', {}).get('canPurchasePlus'))
