import subprocess, requests

NOTION_KEY = subprocess.run(["cat", "/Users/Jeff/.config/notion/api_key"], capture_output=True, text=True).stdout.strip()
PARENT_PAGE = "3680da1b-1be6-807b-9d22-ce2a5a212ad0"

headers = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

# Archive old page
old_page_id = "3870da1b-1be6-81a4-9991-e42db1e0f567"
requests.patch(f"https://api.notion.com/v1/pages/{old_page_id}", headers=headers, json={"archived": True})

children = []

def b(type_name, props):
    return {"object": "block", "type": type_name, type_name: props}

def heading(level, text):
    return b(f"heading_{level}", {"rich_text": [{"type": "text", "text": {"content": text}, "annotations": {"bold": True}}]})

def para(text):
    return b("paragraph", {"rich_text": [{"type": "text", "text": {"content": text}}]})

def bul(text, bold_prefix=None):
    rt = []
    if bold_prefix:
        rt.append({"type": "text", "text": {"content": bold_prefix}, "annotations": {"bold": True}})
    rt.append({"type": "text", "text": {"content": text}})
    return b("bulleted_list_item", {"rich_text": rt})

def num(text):
    return b("numbered_list_item", {"rich_text": [{"type": "text", "text": {"content": text}}]})

def callout(text, icon="\U0001F4CB"):
    return b("callout", {"icon": {"type": "emoji", "emoji": icon}, "rich_text": [{"type": "text", "text": {"content": text}}]})

def codeb(text):
    return b("code", {"rich_text": [{"type": "text", "text": {"content": text}}], "language": "plain text"})

def toggle(title_text, inner):
    return b("toggle", {"rich_text": [{"type": "text", "text": {"content": title_text}}], "children": inner})

def table_row(cells_list):
    return b("table_row", {"cells": [[{"type": "text", "text": {"content": c}}] for c in cells_list]})

def table_def(width, has_header, rows):
    return b("table", {"table_width": width, "has_column_header": has_header, "has_row_header": False, "children": rows})

# Status callout
children.append(callout("WEEKLY REPORT — June 15–19, 2026"))
children.append(para("Updated by SMITH on 2026-06-19"))
children.append(b("divider", {}))

# Status table
children.append(heading(2, "Status at a Glance"))
children.append(table_def(4, True, [
    table_row(["Project", "Status", "Key Update", "Blocker"]),
    table_row(["MRP (Infor Food Pkg)", "On Track", "Daily 2:00 PM planning cleanup & workbench troubleshooting (Test DB)", ""]),
    table_row(["Returnable Box", "On Track", "Background notification flow completed", "Article/Material number link missing in MES"]),
    table_row(["Move Apps", "Blocked", "Git initialized, config decoupled. Centralized DB design blocks migration.", "DB hosting decision required (TPN vs TPK)"]),
    table_row(["TPK QA Hold", "On Track", "Clean Architecture refactoring & UI modernization completed", ""]),
    table_row(["Store Ink", "In Progress", "No updates this week (newly marked)", ""]),
]))

# Executive Summary toggle
children.append(toggle("Executive Summary", [
    para("Returnable Box: Completed real-time notification flow (Production -> Delivery Order -> Stock FG alert) using SignalR and custom DI on Consumable.vb. Client PCs now auto-connect on load. Handled structured JSON payloads, centralized native desktop toast alerts, and resolved multi-threaded UI badge update issues using thread-safe marshalling."),
    para("TPK QA Hold: Transitioned to active development. Refactored the legacy C# project into Clean Architecture (Core, Infrastructure, Presentation layers) and decoupled database access and Excel export logic into repositories. Modernized the WinForms UI via FormModernizer.cs to apply a flat, modern slate dashboard theme."),
    para("MRP (Infor Food Pkg): Supported the Food Packaging team with daily 2:00 PM on-site troubleshooting sessions for the Material Planner Workbench using the Test Database environment. Conducted an on-site visit at TPK and met with the ERP Manager to align on MRP system processes and configuration."),
]))

# This Week toggle
children.append(toggle("This Week (June 15–19)", [
    bul("Notification flow completed — Integrated SignalR, client auto-connect, structured payloads, thread-safe UI badge updates", "[Box] "),
    bul("TPK QA Hold Architecture — Refactored to Clean Architecture, decoupled database access, injected flat dashboard UI theme", "[ShopFloor] "),
    bul("TPK QA Hold UI Modernization — Expanded FormModernizer.cs with flat controls, slate palette, themed calendar, custom ToolStripRenderer, redesigned tab drawing", "[ShopFloor] "),
    bul("Daily Workbench Troubleshooting & Cleanup — Test DB sessions, cleaned outdated recommendations, archived legacy history", "[MRP] "),
    bul("ERP Manager Alignment Meeting — On-site visit at TPK, aligned on MRP configurations and database setups", "[MRP] "),
    bul("Blocked: Outsource Migration — Git initialized, config decoupled, v1.0.0.64 deployed. DB hosting decision required", "[Move Apps] "),
    bul("No updates this week", "[StoreInk] "),
    bul("Blocked: Dimension criteria dig-in — Article/Material numbers have no linking software in MES", "[Box] "),
]))

# MRP Flow toggle
children.append(toggle("MRP & Manufacturing Flow", [
    heading(3, "Flow Diagram"),
    codeb("Customer Order -> Job Order Qty Released -> MRP Engine -> Material Planner Workbench\n  |-> Job BOM Explosion (material requirements)\n  |-> Item Cross-Reference (alternate parts)\n  +-> Workbench branches:\n      |-> Firm Planned POs\n      |-> Backlog POs (past due)\n      +-> Time-Phased Inventory -> Planning Detail Display"),
    heading(3, "Flow Logic"),
    bul("Demand Entry: Customer Order triggers Job Order Qty Released"),
    bul("Parallel Processing: Job BOM Explosion + Item Cross-Reference"),
    bul("MRP Engine: Runs regeneration or net-change; outputs to Workbench"),
    bul("Workbench: Branches into Firm Planned POs, Backlog POs, Time-Phased Inventory"),
    bul("Output: Time-Phased Inventory feeds Planning Detail Display"),
]))

# Troubleshooting toggle
children.append(toggle("Easy Issue Troubleshooting", [
    heading(3, "Issue 1: Ref Type is (Blank) for JOB..."),
    num("Select Customer Orders form -> Input Order #K*2487 -> Filter In Place"),
    num("Go to Lines #1 -> Releases #1 -> Source -> References tab"),
    num("Set: Destination=Order, Order Number=#K000012487, Order Line=#1, Order Release=#1"),
    heading(3, "Issue 2: PO Requisition Line does not exist..."),
    num("Select Job Orders form -> Input Job -> Filter -> Operations -> Materials -> Source tab -> Set Source = Inventory"),
    heading(3, "Issue 3: Outdated planning recommendation remains active..."),
    num("Material Planner Workbench -> Uncheck Purchase Order + All Orders filters"),
    num("Select target item -> Time Phased -> Source -> Job -> Status to Stopped -> Save -> Status to History -> Save"),
    num("Planning Detail -> Find outdated PRs -> PO Requisitions form -> Input requisition number -> Filter -> Status to Stopped -> Save"),
]))

# Move Apps table toggle
children.append(toggle("Move Apps — Project List", [
    table_def(6, True, [
        table_row(["Program", "Status", "Writer", "SQL Instance", "Database", "Remark"]),
        table_row(["Outsource", "Tracking", "Phutorn", "192.168.10.19\\SQLEXPRESS02", "TPNprinting", "Phutorn's IP 192.168.6.189"]),
        table_row(["OutsourceMobile", "Tracking", "Phutorn", "", "", "\\\\192.168.10.2\\ShareCenter\\Program\\Outsource"]),
        table_row(["StockTPN", "Tracking", "Phutorn", "192.168.10.19\\SQLEXPRESS02", "InventoryRMTPK", "storerm"]),
        table_row(["AI", "Done", "Manoon", "eset.tpk.thsg MySQL", "QC_Hand", "AI QC/ASM - prod data"]),
        table_row(["Parameter Viewer", "Done", "Manoon", "PDDB.tpk.thsg MySQL", "Target_speed_DB", "TPN host"]),
        table_row(["QC_HandSET", "Done", "Manoon", "PDDB.tpk.thsg\\SQLEXPRESS", "QC_Hand", "Assembly/Glue"]),
    ])
]))

# Next Week toggle
children.append(toggle("Next Week", [
    bul("TPK QA Hold - Implement core business logic for hold entry and search", "[ShopFloor] "),
    bul("Resolve TPN vs TPK database hosting decision for Outsource migration", "[Move Apps] "),
    bul("Dimension search functionality mapping", "[Box] "),
    bul("Update User Manual & Developer Guide", "[Box] "),
    bul("Scrap - Begin implementation of disposal transaction", "[StoreInk] "),
    bul("Clear backlog CO, PR, optimize workbench profiles (Test DB)", "[MRP] "),
]))

# Notes toggle
children.append(toggle("Notes to Self", [
    bul("Move Apps: 3/7 done. Remaining: Outsource, OutsourceMobile, StockTPN, StoreTPN"),
    bul("Move Apps: 1 month deadline (or at least 2 weeks)"),
    bul("Move Apps: BOXSOFT instance = TPK-REGULUS, DB = csgwin-tpk"),
    bul("Box: Dimension search blocked - Article/Material numbers have no linking software in MES"),
    bul("MRP: Operating on Test Database for workbench simulation and cleanup"),
]))

# References
children.append(b("divider", {}))
children.append(heading(2, "References"))
children.append(bul("Notion Page: https://app.notion.com/p/MRP-Infor-Food-Packaging-3680da1b1be6807b9d22ce2a5a212ad0"))
children.append(bul("Slack Canvas (Previous): https://flexpakhq.slack.com/docs/T0AMK5LU20P/F0BABJ39FJ6"))

# Create page
page_payload = {
    "parent": {"type": "page_id", "page_id": PARENT_PAGE},
    "properties": {"title": {"title": [{"type": "text", "text": {"content": "Weekly (June 15–19, 2026)"}}]}},
    "children": children[:100]
}

resp = requests.post("https://api.notion.com/v1/pages", headers=headers, json=page_payload)
if resp.status_code == 200:
    page = resp.json()
    print(f"URL: {page['url']}")
    print(f"Total blocks: {len(children)}")
    remaining = children[100:]
    if remaining:
        for i in range(0, len(remaining), 100):
            batch = remaining[i:i+100]
            r2 = requests.patch(f"https://api.notion.com/v1/blocks/{page['id']}/children", headers=headers, json={"children": batch})
            print(f"Batch {i//100 + 1}: {r2.status_code}")
else:
    print(f"Error {resp.status_code}: {resp.text}")
