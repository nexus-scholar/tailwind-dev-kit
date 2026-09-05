import re
import httpx

r = httpx.get("https://catalyst.tailwindui.com/docs/button", follow_redirects=True)
html = r.text

main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
if main_match:
    main_html = main_match.group(1)
    print("Found main content, length:", len(main_html))
    # print first 500 characters
    print(main_html[:500])
