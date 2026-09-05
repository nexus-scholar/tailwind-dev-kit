from __future__ import annotations

import html
import os
import re
import urllib.parse
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
import httpx
from rich.console import Console

console = Console()

BASE_URL = "https://tailwindcss.com"
LOGIN_URL = f"{BASE_URL}/plus/login"
HOME_URL = f"{BASE_URL}/plus"

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


@dataclass
class AuthStatus:
    is_authenticated: bool
    user_email: Optional[str] = None
    has_full_license: bool = False
    details: str = ""
    cookies: Dict[str, str] = None


def parse_cookie_header(cookie_str: str) -> Dict[str, str]:
    """Parse a raw HTTP 'Cookie:' header string into a dictionary."""
    cookies = {}
    for item in cookie_str.split(";"):
        item = item.strip()
        if not item or "=" not in item:
            continue
        key, val = item.split("=", 1)
        cookies[key.strip()] = val.strip()
    return cookies


def get_stored_credentials() -> Dict[str, Optional[str]]:
    """Load credentials from .env without logging secret values."""
    load_dotenv(override=True)
    return {
        "session": os.getenv("TAILWIND_SESSION"),
        "cookies": os.getenv("TAILWIND_COOKIES"),
        "email": os.getenv("TAILWIND_EMAIL"),
        "password": os.getenv("TAILWIND_PASSWORD"),
    }


def login_with_password(client: httpx.Client, email: str, password: str) -> bool:
    """Attempt email/password login on /plus/login."""
    # Step 1: Initial GET to obtain XSRF-TOKEN and Inertia version
    res = client.get(
        LOGIN_URL,
        headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "text/html"}
    )
    
    xsrf_token = client.cookies.get("XSRF-TOKEN")
    if xsrf_token:
        xsrf_token = urllib.parse.unquote(xsrf_token)

    # Extract Inertia version from HTML
    unescaped = html.unescape(res.text)
    m_ver = re.search(r'"version":\s*"([^"]+)"', unescaped)
    version = m_ver.group(1) if m_ver else ""

    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Content-Type": "application/json",
        "X-Inertia": "true",
        "Accept": "text/html, application/xhtml+xml",
        "X-Requested-With": "XMLHttpRequest",
    }
    if version:
        headers["X-Inertia-Version"] = version
    if xsrf_token:
        headers["X-XSRF-TOKEN"] = xsrf_token

    payload = {"email": email, "password": password, "remember": True}
    login_res = client.post(LOGIN_URL, json=payload, headers=headers, follow_redirects=False)

    # In Laravel/Inertia, successful login redirects (302/303) away from /plus/login
    location = login_res.headers.get("Location", "")
    if login_res.status_code in (302, 303) and "/login" not in location:
        return True
    return False


def create_authenticated_client() -> Tuple[httpx.Client, AuthStatus]:
    """
    Creates an httpx.Client with authentication loaded from .env.
    Checks license and authentication status.
    """
    creds = get_stored_credentials()

    # 1. Fetch initial landing page with a temporary client to extract current Inertia version
    version = ""
    try:
        with httpx.Client(headers={"User-Agent": DEFAULT_USER_AGENT}) as temp_client:
            init_res = temp_client.get(
                f"{BASE_URL}/plus",
                headers={"Accept": "text/html"}
            )
            unescaped = html.unescape(init_res.text)
            m_ver = re.search(r'"version":\s*"([^"]+)"', unescaped)
            if m_ver:
                version = m_ver.group(1)
    except Exception:
        pass

    # 2. Build the main client
    client = httpx.Client(
        base_url=BASE_URL,
        timeout=30.0,
        headers={"User-Agent": DEFAULT_USER_AGENT}
    )

    # 3. Check if session cookie is provided
    session_val = None
    if creds["session"]:
        session_val = creds["session"].strip()
    elif creds["cookies"]:
        raw_cookie = creds["cookies"].strip()
        if "=" in raw_cookie and not raw_cookie.endswith("="):
            parsed = parse_cookie_header(raw_cookie)
            for k, v in parsed.items():
                client.cookies.set(k, v, domain="tailwindcss.com", path="/")
        else:
            session_val = raw_cookie

    if session_val:
        client.cookies.set("tailwind_plus_session", session_val, domain="tailwindcss.com", path="/")

    # 4. If session cookie is not set, but email/password are, attempt direct login
    has_session = False
    try:
        has_session = bool(client.cookies.get("tailwind_plus_session"))
    except Exception:
        has_session = False

    if not has_session and creds["email"] and creds["password"]:
        success = login_with_password(client, creds["email"], creds["password"])
        if not success:
            return client, AuthStatus(
                is_authenticated=False,
                details="Login with TAILWIND_EMAIL and TAILWIND_PASSWORD failed. Check credentials."
            )

    # 5. Verify session by querying /plus with Inertia headers
    try:
        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html, application/xhtml+xml",
            "X-Requested-With": "XMLHttpRequest",
            "X-Inertia": "true",
        }
        if version:
            headers["X-Inertia-Version"] = version

        res = client.get(HOME_URL, headers=headers)

        if res.status_code == 409:
            # Version refreshed by server
            new_version = res.headers.get("X-Inertia-Version")
            if new_version:
                headers["X-Inertia-Version"] = new_version
                res = client.get(HOME_URL, headers=headers)

        if res.status_code == 200:
            data = res.json()
            props = data.get("props", {})
            auth = props.get("auth")
            can_purchase = props.get("canPurchasePlus", True)

            if auth and isinstance(auth, dict):
                user_info = auth.get("user")
                if isinstance(user_info, dict):
                    user_email = user_info.get("email")
                else:
                    user_email = auth.get("email")

                has_license = (can_purchase is False) or (user_email is not None)
                return client, AuthStatus(
                    is_authenticated=True,
                    user_email=user_email,
                    has_full_license=has_license,
                    details="Authenticated successfully with active Tailwind Plus session.",
                    cookies=dict(client.cookies)
                )

        # If direct cookie verification didn't work but we have email/password, try fallback login
        if creds["email"] and creds["password"]:
            client.cookies.clear()
            success = login_with_password(client, creds["email"], creds["password"])
            if success:
                res = client.get(HOME_URL, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    props = data.get("props", {})
                    auth = props.get("auth")
                    can_purchase = props.get("canPurchasePlus", True)
                    if auth and isinstance(auth, dict):
                        user_info = auth.get("user")
                        user_email = user_info.get("email") if isinstance(user_info, dict) else auth.get("email")
                        return client, AuthStatus(
                            is_authenticated=True,
                            user_email=user_email,
                            has_full_license=(can_purchase is False),
                            details="Authenticated successfully with active Tailwind Plus session.",
                            cookies=dict(client.cookies)
                        )

        return client, AuthStatus(
            is_authenticated=False,
            details="Not authenticated. Add TAILWIND_SESSION or credentials to .env file."
        )
    except Exception as e:
        return client, AuthStatus(
            is_authenticated=False,
            details=f"Connection error while verifying authentication: {e}"
        )
