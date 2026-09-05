import urllib.request
import re
import json

layout_content = open('scratch/layout_js.txt', encoding='utf-8').read()
app_content = open('scratch/app_js.txt', encoding='utf-8').read()

# Search for /plus/ calls
calls = re.findall(r'(?:get|post|put|delete)\([\'"]([^\'"]+)[\'"]', layout_content + app_content)
print('HTTP calls:', set(calls))

# Search for how mt is defined or axios/router
router_calls = re.findall(r'\b\w+\.(?:get|post|put|delete)\([^\)]+\)', layout_content)
print('Router calls sample:', router_calls[:10])

