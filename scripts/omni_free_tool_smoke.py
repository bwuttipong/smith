#!/usr/bin/env python3
import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

ENV_PATH = Path('/Users/Jeff/Smith/.env')
if ENV_PATH.exists():
    for line in ENV_PATH.read_text().splitlines():
        line=line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k,v=line.split('=',1)
        k=k.strip(); v=v.strip().strip('"').strip("'")
        os.environ.setdefault(k,v)

key = os.environ.get('OMNIROUTER_API_KEY') or os.environ.get('HERMES_CUSTOM_NINE_PROXY_API_KEY') or 'dummy'
base='http://127.0.0.1:20128/v1/chat/completions'
models = sys.argv[1:] or [
    'auto/coding:free',
    'auto/best-free',
    'kc/openrouter/free',
    'kilocode/openrouter/free',
    'auto/smart',
    'auto/coding:cheap',
]

def call(model):
    payload={
      'model': model,
      'messages': [
        {'role':'system','content':'You are a concise tool-calling test agent.'},
        {'role':'user','content':'Use the provided tool to add 19 and 23, then answer with the result.'}
      ],
      'tools': [{
        'type':'function',
        'function': {
          'name':'add_numbers',
          'description':'Add two integers.',
          'parameters': {
            'type':'object',
            'properties': {'a': {'type':'integer'}, 'b': {'type':'integer'}},
            'required':['a','b']
          }
        }
      }],
      'tool_choice':'auto',
      'temperature':0,
      'max_tokens':120,
      'stream':False,
    }
    req=urllib.request.Request(base, data=json.dumps(payload).encode(), headers={'Content-Type':'application/json','Authorization':f'Bearer {key}'})
    t=time.time()
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            data=json.loads(r.read().decode())
            dt=round(time.time()-t,2)
            msg=data.get('choices',[{}])[0].get('message',{})
            return {'model':model,'ok':True,'seconds':dt,'tool_calls':msg.get('tool_calls') or [],'content':msg.get('content'),'finish_reason':data.get('choices',[{}])[0].get('finish_reason')}
    except urllib.error.HTTPError as e:
        body=e.read().decode(errors='replace')[:500]
        return {'model':model,'ok':False,'status':e.code,'error':body}
    except Exception as e:
        return {'model':model,'ok':False,'error':repr(e)}

results=[call(m) for m in models]
print(json.dumps(results, indent=2, ensure_ascii=False))
