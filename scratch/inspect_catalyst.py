import re
import json
from tailwind_dev_kit.auth import create_authenticated_client
from tailwind_dev_kit.client import TailwindPlusClient

client, _ = create_authenticated_client()

# Check all downloads on https://tailwindcss.com/plus
r_home = client.get('https://tailwindcss.com/plus')
print("Home download URLs:", set(re.findall(r'href="([^"]*download[^"]*)"', r_home.text)))

# Check all downloads on https://tailwindcss.com/plus/ui-kit
r_uikit = client.get('https://tailwindcss.com/plus/ui-kit')
print("UI Kit download URLs:", set(re.findall(r'href="([^"]*download[^"]*)"', r_uikit.text)))

# Check all downloads on https://tailwindcss.com/plus/kits/oatmeal
r_oat = client.get('https://tailwindcss.com/plus/kits/oatmeal')
print("Oatmeal download URLs:", set(re.findall(r'href="([^"]*download[^"]*)"', r_oat.text)))
