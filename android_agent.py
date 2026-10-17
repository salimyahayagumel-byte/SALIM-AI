"""SALIM AI V6 Android agent. Runs only allowlisted actions in a dedicated workspace."""
import os, time, json, subprocess, urllib.parse
from pathlib import Path
import requests
from dotenv import load_dotenv
load_dotenv()
CLOUD=os.getenv('SALIM_CLOUD_URL','').rstrip('/')
TOKEN=os.getenv('SALIM_AGENT_TOKEN','')
WORKSPACE=Path(os.getenv('SALIM_WORKSPACE',str(Path.home()/'salim-ai-workspace'))).expanduser().resolve()
POLL=max(3,int(os.getenv('POLL_SECONDS','5')))
HEADERS={'X-SALIM-AGENT-TOKEN':TOKEN}
WORKSPACE.mkdir(parents=True,exist_ok=True)
def safe_path(rel):
    p=(WORKSPACE/str(rel or '.')).resolve()
    if p != WORKSPACE and WORKSPACE not in p.parents: raise ValueError('An hana fita daga SALIM workspace.')
    return p
def execute(task):
    action=task['action']; payload=task.get('payload') or {}
    if action=='open_url':
        url=str(payload.get('url','')); u=urllib.parse.urlparse(url)
        if u.scheme not in ('https','http','tel','sms','mailto'): raise ValueError('Ba a yarda da wannan URL ba.')
        subprocess.run(['termux-open-url',url],check=True,timeout=15)
        return {'opened':url}
    if action=='list_files':
        p=safe_path(payload.get('path','.'))
        if not p.is_dir(): raise ValueError('Ba directory ba ne.')
        return {'files':[{'name':x.name,'directory':x.is_dir()} for x in list(p.iterdir())[:100]]}
    if action=='read_file':
        p=safe_path(payload.get('path',''))
        if not p.is_file(): raise FileNotFoundError('Ba a sami fayil ba.')
        if p.stat().st_size>200000: raise ValueError('Fayil ya wuce 200KB.')
        return {'content':p.read_text(encoding='utf-8')[:200000]}
    if action=='write_file':
        p=safe_path(payload.get('path','')); content=str(payload.get('content',''))
        if len(content)>100000: raise ValueError('Rubutu ya wuce 100KB.')
        p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding='utf-8')
        return {'written':str(p.relative_to(WORKSPACE))}
    if action=='run_python':
        p=safe_path(payload.get('path',''))
        if not p.is_file() or p.suffix!='.py': raise ValueError('Dole ne fayil .py a cikin workspace.')
        proc=subprocess.run(['python',str(p)],cwd=str(WORKSPACE),capture_output=True,text=True,timeout=20)
        return {'returncode':proc.returncode,'stdout':proc.stdout[-4000:],'stderr':proc.stderr[-4000:]}
    raise ValueError('Ba a yarda da wannan aikin ba.')
def main():
    if not CLOUD.startswith('https://') or not TOKEN: raise SystemExit('Cika SALIM_CLOUD_URL (HTTPS) da SALIM_AGENT_TOKEN a .env')
    print('SALIM AI Android Agent V6.0 ya fara. Workspace:',WORKSPACE)
    while True:
        try:
            r=requests.get(CLOUD+'/api/agent/next',headers=HEADERS,timeout=20); r.raise_for_status(); task=r.json().get('task')
            if task:
                try: result={'id':task['id'],'ok':True,'result':execute(task)}
                except Exception as e: result={'id':task['id'],'ok':False,'error':str(e)}
                requests.post(CLOUD+'/api/agent/result',headers=HEADERS,json=result,timeout=20).raise_for_status()
                print(json.dumps(result,ensure_ascii=False))
        except Exception as e: print('Cloud connection:',str(e)[:180])
        time.sleep(POLL)
if __name__=='__main__': main()
