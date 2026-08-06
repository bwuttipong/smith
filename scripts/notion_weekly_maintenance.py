#!/usr/bin/env python3
from pathlib import Path
import json, urllib.request, urllib.error, datetime
from zoneinfo import ZoneInfo
ENV=Path('/Users/Jeff/.openclaw/.env')
DS='3630da1b-1be6-8066-a159-000be09cb433'
TASK='Weekly System Maintenance'
token=''
for line in ENV.read_text().splitlines():
    if line.strip().startswith('#') or '=' not in line: continue
    k,v=line.split('=',1)
    if k in ('NOTION_API_KEY','NOTION_API_TOKEN'):
        token=v.strip().strip('"').strip("'"); break
if not token:
    raise SystemExit('Notion token missing')
H={'Authorization':'Bearer '+token,'Notion-Version':'2025-09-03','Content-Type':'application/json'}
def req(method,url,body=None):
    data=None if body is None else json.dumps(body).encode()
    r=urllib.request.Request(url,data=data,headers=H,method=method)
    try:
        with urllib.request.urlopen(r,timeout=25) as resp: return resp.status,json.load(resp)
    except urllib.error.HTTPError as e:
        raw=e.read().decode(errors='ignore')
        try: j=json.loads(raw)
        except Exception: j={'raw':raw}
        return e.code,j
now=datetime.datetime.now(ZoneInfo('Asia/Bangkok'))
due_date=now.date().isoformat()
due_start=f'{due_date}T17:30:00+07:00'
query={"filter":{"property":"Task name","title":{"equals":TASK}},"page_size":10}
s,j=req('POST',f'https://api.notion.com/v1/data_sources/{DS}/query',query)
if s!=200:
    raise SystemExit(f'query failed: {s} {j}')
props={
  'Task name': {'title':[{'type':'text','text':{'content':TASK}}]},
  'Status': {'status': {'name':'Not started'}},
  'Due date': {'date': {'start': due_start}},
  'Checked': {'checkbox': False},
}
if j.get('results'):
    page_id=j['results'][0]['id']
    s2,out=req('PATCH',f'https://api.notion.com/v1/pages/{page_id}',{'properties':props})
    action='updated'
else:
    s2,out=req('POST','https://api.notion.com/v1/pages',{'parent':{'data_source_id':DS},'properties':props})
    page_id=out.get('id')
    action='created'
if s2 not in (200,201):
    raise SystemExit(f'{action} failed: {s2} {out}')
# Silent on success for cron/no_agent. Uncomment for debugging:
# print(f'{action} {TASK} {due_start} {page_id}')
