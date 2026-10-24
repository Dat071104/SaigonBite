"""Archive actual Phase 2 prompts and transcripts privately after all agents finish."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import zipfile

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--session-id',default=os.environ.get('CODEX_THREAD_ID')); args=parser.parse_args()
    if not args.session_id: raise SystemExit('Actual root session ID required')
    base=Path(r'C:\Users\ADMIN\.codex\sessions\2026\10')
    matches=list(base.glob(f'*/*{args.session_id}.jsonl'))
    assert len(matches)==1,'Expected one actual root session'
    source=matches[0]; prompts=[]
    for line in source.read_text(encoding='utf-8').splitlines():
        item=json.loads(line); p=item.get('payload',{})
        if item.get('type')=='response_item' and p.get('type')=='function_call' and any(name in p.get('name','') for name in ('spawn_agent','followup_task','send_message')):
            prompts.append({'timestamp':item.get('timestamp'),'tool':p['name'],'arguments':json.loads(p['arguments'])})
    logs=[source]
    for day in (base/'23',base/'24',base/'25'):
        if not day.exists(): continue
        for path in day.glob('*.jsonl'):
            if path==source: continue
            with path.open(encoding='utf-8') as f: meta=json.loads(f.readline()).get('payload',{})
            if args.session_id in json.dumps(meta.get('source',{})): logs.append(path)
    out=Path(r'D:\RAD\FINAL\Part2\notes'); controlling=Path(r'D:\RAD\FINAL\Part2\codex\P2_PROMPT.md')
    data={'source_session':source.name,'controlling_prompt':str(controlling),'controlling_prompt_sha256':hashlib.sha256(controlling.read_bytes()).hexdigest(),'dispatched_prompts':prompts,'transcripts':[p.name for p in logs]}
    (out/'P2_prompt_archive.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
    with zipfile.ZipFile(out/'P2_transcripts.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in logs: z.write(path,path.name)
        z.write(controlling,controlling.name)
        for report in Path(r'D:\RAD\FINAL\SaigonBite\docs\part2\_agent_reports').glob('P2-*.md'): z.write(report,report.name)
    print(json.dumps({'spawn_count':sum('spawn_agent' in p['tool'] for p in prompts),'coordination_prompts':len(prompts),'transcripts':len(logs),'path':str(out/'P2_prompt_archive.json')}))

if __name__=='__main__': main()
