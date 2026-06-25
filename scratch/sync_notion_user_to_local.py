import json
import urllib.request
import os

def rich_text_to_markdown(rich_text_list):
    md = ""
    for r in rich_text_list:
        content = r.get('plain_text', '')
        anno = r.get('annotations', {})
        if anno.get('bold'):
            content = f"*{content}*"
        if anno.get('italic'):
            content = f"_{content}_"
        if r.get('href'):
            content = f"[{content}]({r['href']})"
        md += content
    return md

def fetch_children(block_id, headers):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    req = urllib.request.Request(url, headers=headers, method='GET')
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res.get('results', [])
    except Exception as e:
        print(f"Error fetching children for {block_id}: {e}")
        return []

def block_to_markdown(block, headers):
    b_type = block['type']
    
    if b_type == 'heading_1':
        text = rich_text_to_markdown(block['heading_1']['rich_text'])
        return f"# {text}\n"
    elif b_type == 'heading_2':
        text = rich_text_to_markdown(block['heading_2']['rich_text'])
        return f"## {text}\n"
    elif b_type == 'heading_3':
        text = rich_text_to_markdown(block['heading_3']['rich_text'])
        return f"### {text}\n"
    elif b_type == 'paragraph':
        text = rich_text_to_markdown(block['paragraph']['rich_text'])
        return f"{text}\n"
    elif b_type == 'bulleted_list_item':
        text = rich_text_to_markdown(block['bulleted_list_item']['rich_text'])
        return f"- {text}\n"
    elif b_type == 'to_do':
        text = rich_text_to_markdown(block['to_do']['rich_text'])
        checked = "x" if block['to_do']['checked'] else " "
        return f"- [{checked}] {text}\n"
    elif b_type == 'divider':
        return "---\n"
    elif b_type == 'code':
        text = rich_text_to_markdown(block['code']['rich_text'])
        lang = block['code'].get('language', 'plain text')
        return f"```{lang}\n{text}\n```\n"
    elif b_type == 'table':
        rows = fetch_children(block['id'], headers)
        if not rows:
            return ""
        
        md_rows = []
        for i, row in enumerate(rows):
            if row['type'] != 'table_row':
                continue
            cells = row['table_row']['cells']
            cell_texts = [rich_text_to_markdown(cell) for cell in cells]
            md_rows.append("| " + " | ".join(cell_texts) + " |")
            
            # If header, add separator line
            if i == 0 and block['table'].get('has_column_header'):
                sep = "| " + " | ".join(["---"] * len(cells)) + " |"
                md_rows.append(sep)
                
        return "\n".join(md_rows) + "\n"
    else:
        # Fallback for unsupported blocks
        return ""

def sync_user_md():
    with open(os.path.expanduser('~/.config/notion/api_key'), 'r') as f:
        notion_key = f.read().strip()
        
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Notion-Version": "2025-09-03"
    }
    
    # Page ID for USER.md (extracted from URL: 3870da1b1be68178af8dd33348fef103)
    page_id = "3870da1b1be68178af8dd33348fef103"
    
    blocks = fetch_children(page_id, headers)
    if not blocks:
        print("No blocks found or error fetching page.")
        return
        
    md_content = []
    # Add title header
    # Let's fetch page details to get the exact title
    req_page = urllib.request.Request(f"https://api.notion.com/v1/pages/{page_id}", headers=headers, method='GET')
    try:
        with urllib.request.urlopen(req_page) as r:
            res = json.loads(r.read().decode('utf-8'))
            title_list = res.get('properties', {}).get('title', {}).get('title', [])
            if title_list:
                title = title_list[0].get('plain_text', 'USER.md')
                md_content.append(f"# {title}\n")
    except Exception as e:
        print(f"Error fetching page title: {e}")
        md_content.append("# USER.md\n")
        
    for block in blocks:
        md = block_to_markdown(block, headers)
        if md:
            md_content.append(md)
            
    # Join with newlines
    full_markdown = "\n".join(md_content)
    
    # Write to local USER.md
    local_path = "USER.md"
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(full_markdown)
        
    print(f"Successfully synced USER.md from Notion! Written {len(full_markdown)} characters.")

if __name__ == "__main__":
    sync_user_md()
