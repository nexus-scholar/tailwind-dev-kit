"""Tailwind CSS Plus / UI component scraper and development toolkit."""

import sys
import io

if sys.platform == "win32":
    if hasattr(sys.stdout, "buffer") and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "buffer") and sys.stderr.encoding.lower() != "utf-8":
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from .auth import create_authenticated_client
from .client import TailwindPlusClient
from .scraper import TailwindPlusScraper
from .storage import ComponentStorage
from .cli import app, main

__all__ = [
    "Component",
    "Subcategory",
    "Snippet",
    "Template",
    "create_authenticated_client",
    "TailwindPlusClient",
    "TailwindPlusScraper",
    "ComponentStorage",
    "app",
    "main",
]
