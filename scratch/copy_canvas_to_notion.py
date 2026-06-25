import json
import urllib.request
import os
import re

def parse_inline_styles(text):
    # Simple regex parsing for bold (*bold*) and links [text](url)
    parts = []
    
    # regex pattern to match bold text and markdown links
    # Group 1: bold text (e.g. *bold*)
    # Group 2: link label, Group 3: link url (e.g. [label](url))
    pattern = r'(\*[^*]+\*)|(?:\[([^\]]+)\]\(([^)]+)\))'
    
    last_end = 0
    for match in re.finditer(pattern, text):
        start, end = match.span()
        # Add plain text before match
        if start > last_end:
            parts.append({
                "type": "text",
                "text": {"content": text[last_end:start]}
            })
            
        bold_match = match.group(1)
        link_label = match.group(2)
        link_url = match.group(3)
        
        if bold_match:
            parts.append({
                "type": "text",
                "text": {"content": bold_match[1:-1]},
                "annotations": {"bold": True}
            })
        elif link_label and link_url:
            parts.append({
                "type": "text",
                "text": {
                    "content": link_label,
                    "link": {"url": link_url}
                }
            })
            
        last_end = end
        
    if last_end < len(text):
        parts.append({
            "type": "text",
            "text": {"content": text[last_end:]}
        })
        
    return parts if parts else [{"type": "text", "text": {"content": text}}]

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    blocks = []
    in_code_block = False
    code_content = []
    code_lang = "plain text"
    
    in_table = False
    table_headers = []
    table_rows = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Handle code blocks
        if line_stripped.startswith("```"):
            if in_code_block:
                # End of code block
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": "\n".join(code_content)}}],
                        "language": code_lang
                    }
                })
                code_content = []
                in_code_block = False
            else:
                # Start of code block
                in_code_block = True
                lang = line_stripped[3:].strip()
                code_lang = lang if lang else "plain text"
                # Notion only supports specific languages, let's map some common ones
                if code_lang == "mermaid":
                    code_lang = "mermaid"
            continue
            
        if in_code_block:
            code_content.append(line.rstrip('\r\n'))
            continue
            
        # Handle tables
        if line_stripped.startswith("|"):
            in_table = True
            # Parse table row
            cells = [cell.strip() for cell in line_stripped.split("|")[1:-1]]
            # Check if this is a separator line (e.g. | --- | --- |)
            if all(re.match(r'^:?-+:?$', cell) for cell in cells):
                continue
                
            if not table_headers:
                table_headers = cells
            else:
                table_rows.append(cells)
            continue
        elif in_table:
            # End of table, construct the table block
            if table_headers:
                table_width = len(table_headers)
                children_rows = []
                # Header row
                children_rows.append({
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [parse_inline_styles(cell) for cell in table_headers]
                    }
                })
                # Data rows
                for row in table_rows:
                    children_rows.append({
                        "object": "block",
                        "type": "table_row",
                        "table_row": {
                            "cells": [parse_inline_styles(cell) for cell in row]
                        }
                    })
                    
                blocks.append({
                    "object": "block",
                    "type": "table",
                    "table": {
                        "table_width": table_width,
                        "has_column_header": True,
                        "has_row_header": False,
                        "children": children_rows
                    }
                })
            table_headers = []
            table_rows = []
            in_table = False
            
        if not line_stripped:
            continue
            
        # Headers
        if line_stripped.startswith("# "):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": parse_inline_styles(line_stripped[2:])
                }
            })
        elif line_stripped.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": parse_inline_styles(line_stripped[3:])
                }
            })
        elif line_stripped.startswith("### "):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": parse_inline_styles(line_stripped[4:])
                }
            })
        # Divider
        elif line_stripped == "---":
            blocks.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })
        # Bullet list items
        elif line_stripped.startswith("- ") or line_stripped.startswith("* ") or line_stripped.startswith("• "):
            content = line_stripped[2:].strip()
            # Check if it's a checkbox todo
            if content.startswith("[ ]"):
                blocks.append({
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": parse_inline_styles(content[3:].strip()),
                        "checked": False
                    }
                })
            elif content.startswith("[x]") or content.startswith("[X]"):
                blocks.append({
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": parse_inline_styles(content[3:].strip()),
                        "checked": True
                    }
                })
            else:
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": parse_inline_styles(content)
                    }
                })
        # Normal paragraphs
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": parse_inline_styles(line_stripped)
                }
            })
            
    # Clean up any leftover table
    if in_table and table_headers:
        table_width = len(table_headers)
        children_rows = []
        children_rows.append({
            "object": "block",
            "type": "table_row",
            "table_row": {
                "cells": [parse_inline_styles(cell) for cell in table_headers]
            }
        })
        for row in table_rows:
            children_rows.append({
                "object": "block",
                "type": "table_row",
                "table_row": {
                    "cells": [parse_inline_styles(cell) for cell in row]
                }
            })
        blocks.append({
            "object": "block",
            "type": "table",
            "table": {
                "table_width": table_width,
                "has_column_header": True,
                "has_row_header": False,
                "children": children_rows
            }
        })
        
    return blocks

# Read Notion API Key
with open(os.path.expanduser('~/.config/notion/api_key'), 'r') as f:
    notion_key = f.read().strip()

# Target file
md_filepath = "memory/artifacts/2026-06-19-weekly-report-june-15-19.md"
parsed_blocks = parse_markdown(md_filepath)

# Let's clean false/true boolean mapping for json (Notion expects lowercase true/false in python dict structure)
# In Python, we use True and False which serialize to true and false in json.dumps().

# Notion Page Info
parent_page_id = "3870da1b-1be6-81bc-9d45-c1fe1a9959f9" # Weekly page ID
page_title = "Weekly (June 15–19, 2026)"

# Construct payload
payload = {
    "parent": {"page_id": parent_page_id},
    "properties": {
        "title": {
            "title": [{"type": "text", "text": {"content": page_title}}]
        }
    },
    "children": parsed_blocks
}

url = "https://api.notion.com/v1/pages"
headers = {
    "Authorization": f"Bearer {notion_key}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        print("Success! Created Notion page:")
        print(f"URL: {res.get('url')}")
        print(f"Page ID: {res.get('id')}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
