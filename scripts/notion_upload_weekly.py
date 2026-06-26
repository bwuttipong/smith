import json, subprocess, sys, requests

NOTION_KEY = subprocess.getoutput("cat ~/.config/notion/api_key").strip()
PARENT_PAGE = "3680da1b-1be6-807b-9d22-ce2a5a212ad0"

children = []

def add_heading(text, level=2):
    children.append({
        "object": "block",
        "type": f"heading_{level}",
        f"heading_{level}": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    })

def add_paragraph(text):
    children.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    })

def add_bullet(bold, normal):
    rt = []
    if bold:
        rt.append({"type": "text", "text": {"content": bold}, "annotations": {"bold": True}})
    rt.append({"type": "text", "text": {"content": normal}})
    children.append({
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rt}
    })

def add_callout(text, icon="📋"):
    children.append({
        "object": "block",
        "type": "callout",
        "callout": {
            "icon": {"type": "emoji", "emoji": icon},
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    })

def add_code(text):
    children.append({
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "language": "plain text"
        }
    })

# Status callout
add_callout("STATUS AT A GLANCE — Week of June 15–19, 2026", "📋")

# Project status table
children.append({
    "object": "block", "type": "table", "table": {
        "table_width": 4, "has_column_header": True, "has_row_header": False,
        "children": [
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "Project"}}],
                [{"type": "text", "text": {"content": "Status"}}],
                [{"type": "text", "text": {"content": "Key Update"}}],
                [{"type": "text", "text": {"content": "Blocker"}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "MRP (Infor Food Pkg)"}}],
                [{"type": "text", "text": {"content": "On Track"}}],
                [{"type": "text", "text": {"content": "Daily 2:00 PM planning cleanup & workbench troubleshooting (Test DB)"}}],
                [{"type": "text", "text": {"content": ""}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "Returnable Box"}}],
                [{"type": "text", "text": {"content": "On Track"}}],
                [{"type": "text", "text": {"content": "Background notification flow completed"}}],
                [{"type": "text", "text": {"content": "Article/Material number link missing in MES"}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "Move Apps"}}],
                [{"type": "text", "text": {"content": "Blocked"}}],
                [{"type": "text", "text": {"content": "Git initialized, config decoupled. Centralized DB design blocks migration."}}],
                [{"type": "text", "text": {"content": "DB hosting decision required (TPN vs TPK)"}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "TPK QA Hold"}}],
                [{"type": "text", "text": {"content": "On Track"}}],
                [{"type": "text", "text": {"content": "Clean Architecture refactoring & UI modernization completed"}}],
                [{"type": "text", "text": {"content": "—"}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "Store Ink"}}],
                [{"type": "text", "text": {"content": "In Progress"}}],
                [{"type": "text", "text": {"content": "No updates this week (newly marked)"}}],
                [{"type": "text", "text": {"content": "—"}}]
            ]}}
        ]
    }
})

# Executive summary
add_heading("Executive Summary")
add_paragraph("Mon 15 June – Fri 19 June: Returnable Box notification flow completed with SignalR, client auto-connect, structured payloads, and thread-safe UI badge updates. TPK QA Hold refactored to Clean Architecture with modern slate dashboard UI. MRP daily workbench troubleshooting and ERP Manager alignment meeting completed. Move Apps blocked on database hosting decision. Store Ink — no updates.")

# This week
add_heading("This Week (June 15–19)")
add_bullet("[Box] ", "Notification flow completed — Integrated SignalR notification service, client auto-connect, structured payloads, and thread-safe UI badge updates")
add_bullet("[ShopFloor] ", "TPK QA Hold Architecture — Refactored to Clean Architecture, decoupled database access, injected flat dashboard UI theme")
add_bullet("[ShopFloor] ", "TPK QA Hold UI Modernization — Expanded FormModernizer.cs with flat controls, slate palette, themed calendar, custom ToolStripRenderer, redesigned tab drawing")
add_bullet("[MRP] ", "Daily Workbench Troubleshooting & Cleanup — Test DB sessions, cleaned up out-of-date recommendations, archived legacy history")
add_bullet("[MRP] ", "ERP Manager Alignment Meeting — On-site visit at TPK, aligned on MRP system configurations and database setups")
add_bullet("[Move Apps] ", "Blocked: Outsource Migration — Git initialized, config decoupled, v1.0.0.64 deployed. Database hosting decision required (TPN vs TPK)")
add_bullet("[StoreInk] ", "No updates this week")
add_bullet("[Box] ", "Blocked: Dimension criteria dig-in — Article and Material numbers have no linking software in MES")

# MRP Flow
add_heading("MRP & Manufacturing Flow")
add_code("Customer Order -> Job Order Qty Released -> MRP Engine -> Material Planner Workbench\n  |-> Job BOM Explosion (material requirements)\n  |-> Item Cross-Reference (alternate parts)\n  +-> Workbench branches:\n      |-> Firm Planned POs\n      |-> Backlog POs (past due)\n      +-> Time-Phased Inventory -> Planning Detail Display")

add_heading("Flow Logic")
add_bullet("", "Demand Entry: Customer Order triggers Job Order Qty Released")
add_bullet("", "Parallel Processing: Job BOM Explosion + Item Cross-Reference")
add_bullet("", "MRP Engine: Runs regeneration or net-change; outputs to Workbench")
add_bullet("", "Workbench: Branches into Firm Planned POs, Backlog POs, Time-Phased Inventory")
add_bullet("", "Output: Time-Phased Inventory feeds Planning Detail Display")

# Easy Issues
add_heading("Easy Issue Troubleshooting")
add_heading("Issue 1: Ref Type is (Blank) for JOB...", 3)
add_bullet("", "Select Customer Orders form -> Input Order #K*2487 -> Filter In Place")
add_bullet("", "Go to Lines #1 -> Releases #1 -> Source -> References tab")
add_bullet("", "Set: Destination = Order, Order Number = #K000012487, Order Line = #1, Order Release = #1")

add_heading("Issue 2: PO Requisition Line does not exist...", 3)
add_bullet("", "Select Job Orders form -> Input Job -> Filter -> Operations -> Materials -> Source tab -> Set Source = Inventory")

add_heading("Issue 3: Outdated planning recommendation remains active...", 3)
add_bullet("", "Material Planner Workbench -> Uncheck Purchase Order + All Orders filters")
add_bullet("", "Select target item -> Time Phased -> Source -> Job -> Status to Stopped -> Save -> Status to History -> Save")
add_bullet("", "Planning Detail -> Find outdated PRs -> PO Requisitions form -> Input requisition number -> Filter -> Status to Stopped -> Save")

# Move Apps table
add_heading("Move Apps - Project List")
children.append({
    "object": "block", "type": "table", "table": {
        "table_width": 6, "has_column_header": True, "has_row_header": False,
        "children": [
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "Program"}}],
                [{"type": "text", "text": {"content": "Status"}}],
                [{"type": "text", "text": {"content": "Writer"}}],
                [{"type": "text", "text": {"content": "SQL Instance"}}],
                [{"type": "text", "text": {"content": "Database"}}],
                [{"type": "text", "text": {"content": "Remark"}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "Outsource"}}],
                [{"type": "text", "text": {"content": "Tracking"}}],
                [{"type": "text", "text": {"content": "Phutorn"}}],
                [{"type": "text", "text": {"content": "192.168.10.19\\SQLEXPRESS02"}}],
                [{"type": "text", "text": {"content": "TPNprinting"}}],
                [{"type": "text", "text": {"content": "Phutorn's IP 192.168.6.189"}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "OutsourceMobile"}}],
                [{"type": "text", "text": {"content": "Tracking"}}],
                [{"type": "text", "text": {"content": "Phutorn"}}],
                [{"type": "text", "text": {"content": "—" }}],
                [{"type": "text", "text": {"content": "—" }}],
                [{"type": "text", "text": {"content": "\\\\192.168.10.2\\ShareCenter\\Program\\Outsource"}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "StockTPN"}}],
                [{"type": "text", "text": {"content": "Tracking"}}],
                [{"type": "text", "text": {"content": "Phutorn"}}],
                [{"type": "text", "text": {"content": "192.168.10.19\\SQLEXPRESS02"}}],
                [{"type": "text", "text": {"content": "InventoryRMTPK"}}],
                [{"type": "text", "text": {"content": "storerm"}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "AI"}}],
                [{"type": "text", "text": {"content": "Done"}}],
                [{"type": "text", "text": {"content": "Manoon"}}],
                [{"type": "text", "text": {"content": "eset.tpk.thsg MySQL"}}],
                [{"type": "text", "text": {"content": "QC_Hand"}}],
                [{"type": "text", "text": {"content": "AI QC/ASM - prod data"}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "Parameter Viewer"}}],
                [{"type": "text", "text": {"content": "Done"}}],
                [{"type": "text", "text": {"content": "Manoon"}}],
                [{"type": "text", "text": {"content": "PDDB.tpk.thsg MySQL"}}],
                [{"type": "text", "text": {"content": "Target_speed_DB"}}],
                [{"type": "text", "text": {"content": "TPN host"}}]
            ]}},
            {"object": "block", "type": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "QC_HandSET"}}],
                [{"type": "text", "text": {"content": "Done"}}],
                [{"type": "text", "text": {"content": "Manoon"}}],
                [{"type": "text", "text": {"content": "PDDB.tpk.thsg\\SQLEXPRESS"}}],
                [{"type": "text", "text": {"content": "QC_Hand"}}],
                [{"type": "text", "text": {"content": "Assembly/Glue"}}]
            ]}}
        ]
    }
})

# Next week
add_heading("Next Week")
add_bullet("[ShopFloor] ", "TPK QA Hold - Implement core business logic for hold entry and search")
add_bullet("[Move Apps] ", "Resolve TPN vs TPK database hosting decision for Outsource migration")
add_bullet("[Box] ", "Dimension search functionality mapping")
add_bullet("[Box] ", "Update User Manual & Developer Guide")
add_bullet("[StoreInk] ", "Scrap - Begin implementation of disposal transaction")
add_bullet("[MRP] ", "Clear backlog CO, PR, optimize workbench profiles (Test DB)")

# Notes
add_heading("Notes to Self")
add_bullet("", "Move Apps: 3/7 done. Remaining: Outsource, OutsourceMobile, StockTPN, StoreTPN (all P'Phutorn's apps)")
add_bullet("", "Move Apps: 1 month deadline (or at least 2 weeks)")
add_bullet("", "Move Apps: BOXSOFT instance = TPK-REGULUS, DB = csgwin-tpk")
add_bullet("", "Box: Dimension search blocked - Article and Material numbers have no linking software in MES")
add_bullet("", "MRP: Operating on Test Database for workbench simulation and cleanup")

# References
add_heading("References")
add_bullet("", "Notion Page: https://app.notion.com/p/MRP-Infor-Food-Packaging-3680da1b1be6807b9d22ce2a5a212ad0")
add_bullet("", "Slack Canvas (Previous): https://flexpakhq.slack.com/docs/T0AMK5LU20P/F0BABJ39FJ6")

# Divider and footer
children.append({"object": "block", "type": "divider", "divider": {}})
add_callout("Updated by SMITH on 2026-06-19", "📝")

# Create page
page_payload = {
    "parent": {"type": "page_id", "page_id": PARENT_PAGE},
    "properties": {
        "title": {
            "title": [{"type": "text", "text": {"content": "Weekly (June 15–19, 2026)"}}]
        }
    },
    "children": children[:100]
}

headers = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

resp = requests.post("https://api.notion.com/v1/pages", headers=headers, json=page_payload)
if resp.status_code == 200:
    page = resp.json()
    page_id = page["id"]
    url = page["url"]
    print(f"Page created: {page_id}")
    print(f"URL: {url}")
    print(f"Blocks in first batch: {len(children[:100])}")

    remaining = children[100:]
    if remaining:
        for i in range(0, len(remaining), 100):
            batch = remaining[i:i+100]
            r2 = requests.patch(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=headers, json={"children": batch})
            print(f"Batch {i//100 + 1}: {r2.status_code}")
else:
    print(f"Error {resp.status_code}: {resp.text}")
