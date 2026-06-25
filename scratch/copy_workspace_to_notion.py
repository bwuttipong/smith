import json
import urllib.request
import os
import re
import time

def parse_inline_styles(text):
    parts = []
    pattern = r'(\*[^*]+\*)|(?:\[([^\]]+)\]\(([^)]+)\))'
    last_end = 0
    for match in re.finditer(pattern, text):
        start, end = match.span()
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
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return []
        
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
                in_code_block = True
                lang = line_stripped[3:].strip()
                code_lang = lang if lang else "plain text"
                # Map to valid Notion code languages
                valid_languages = ["abap", "arduino", "bash", "c", "c++", "c#", "css", "dart", "docker", "elixir", 
                                   "erlang", "flow", "fortran", "f#", "gherkin", "glsl", "go", "graphql", "groovy", 
                                   "haskell", "html", "java", "javascript", "json", "julia", "kotlin", "latex", 
                                   "less", "lisp", "livescript", "lua", "makefile", "markdown", "markup", "matlab", 
                                   "mermaid", "nix", "objective-c", "ocaml", "pascal", "perl", "php", "plain text", 
                                   "powershell", "prolog", "protobuf", "python", "r", "reason", "ruby", "rust", 
                                   "sass", "scala", "scheme", "scss", "shell", "sql", "swift", "typescript", 
                                   "vb.net", "verilog", "vhdl", "visual basic", "webassembly", "xml", "yaml"]
                if code_lang.lower() not in valid_languages:
                    code_lang = "plain text"
            continue
            
        if in_code_block:
            code_content.append(line.rstrip('\r\n'))
            continue
            
        # Handle tables
        if line_stripped.startswith("|"):
            in_table = True
            cells = [cell.strip() for cell in line_stripped.split("|")[1:-1]]
            if all(re.match(r'^:?-+:?$', cell) for cell in cells):
                continue
                
            if not table_headers:
                table_headers = cells
            else:
                table_rows.append(cells)
            continue
        elif in_table:
            if table_headers:
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

headers = {
    "Authorization": f"Bearer {notion_key}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

# 1. Create parent page 'Smith'
parent_page_id = "3680da1b-1be6-807b-9d22-ce2a5a212ad0" # Main MRP page
payload = {
    "parent": {"page_id": parent_page_id},
    "properties": {
        "title": {
            "title": [{"type": "text", "text": {"content": "Smith"}}]
        }
    }
}

req = urllib.request.Request("https://api.notion.com/v1/pages", data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        smith_parent_id = res.get('id')
        print(f"Created parent 'Smith' page: {res.get('url')}")
except Exception as e:
    print(f"Error creating parent page: {e}")
    exit(1)

# Files to copy
files_to_copy = [
    {"name": "README.md", "path": "README.md"},
    {"name": "IDENTITY.md", "path": "IDENTITY.md"},
    {"name": "SOUL.md", "path": "SOUL.md"},
    {"name": "USER.md", "path": "USER.md"},
    {"name": "AGENTS.md", "path": "AGENTS.md"},
    {"name": "TOOLS.md", "path": "TOOLS.md"},
    {"name": "MEMORY.md", "path": "MEMORY.md"}
]

for file_info in files_to_copy:
    print(f"Parsing and copying {file_info['name']}...")
    blocks = parse_markdown(file_info['path'])
    
    # Check block limit (Notion allows max 100 children per page creation request)
    chunk_size = 80
    first_chunk = blocks[:chunk_size]
    other_chunks = blocks[chunk_size:]
    
    payload = {
        "parent": {"page_id": smith_parent_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": file_info['name']}}]
            }
        },
        "children": first_chunk
    }
    
    req = urllib.request.Request("https://api.notion.com/v1/pages", data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            child_page_id = res.get('id')
            print(f"  Created child page {file_info['name']}: {res.get('url')}")
            
            # Append other chunks if they exist
            while other_chunks:
                current_chunk = other_chunks[:chunk_size]
                other_chunks = other_chunks[chunk_size:]
                
                append_payload = {"children": current_chunk}
                append_url = f"https://api.notion.com/v1/blocks/{child_page_id}/children"
                
                req_append = urllib.request.Request(append_url, data=json.dumps(append_payload).encode('utf-8'), headers=headers, method='PATCH')
                with urllib.request.urlopen(req_append) as response_append:
                    pass
                print(f"  Appended chunk of {len(current_chunk)} blocks to {file_info['name']}")
                time.sleep(0.5) # Rate limit safety
                
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error copying {file_info['name']}: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"  Error copying {file_info['name']}: {e}")
        
    time.sleep(1.0) # Rate limit safety between pages
