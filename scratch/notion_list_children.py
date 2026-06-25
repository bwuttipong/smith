import json
import urllib.request
import os

with open(os.path.expanduser('~/.config/notion/api_key'), 'r') as f:
    notion_key = f.read().strip()

page_id = "3870da1b-1be6-81bc-9d45-c1fe1a9959f9"
url = f"https://api.notion.com/v1/blocks/{page_id}/children"
headers = {
    "Authorization": f"Bearer {notion_key}",
    "Notion-Version": "2025-09-03"
}

req = urllib.request.Request(url, headers=headers, method='GET')

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        for result in res.get('results', []):
            print(f"ID: {result['id']} | Type: {result['type']} | Has children: {result['has_children']}")
            if result['type'] == 'child_page':
                print(f"  Title: {result['child_page']['title']}")
except Exception as e:
    print(f"Error: {e}")
