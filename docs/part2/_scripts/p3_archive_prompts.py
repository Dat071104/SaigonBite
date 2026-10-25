"""Archive actual prompts/transcripts only after every Phase 3 worker finishes.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import argparse,hashlib,json,os,zipfile
def main():
    p=argparse.ArgumentParser();p.add_argument('--session-id',default=os.environ.get('CODEX_THREAD_ID'));a=p.parse_args();assert a.session_id,'Actual root session ID required'
    base=Path('C:/Users/ADMIN/.codex/sessions/2026/10');matches=list(base.glob('*/*'+a.session_id+'.jsonl'));assert len(matches)==1;source=matches[0];prompts=[]
    for line in source.read_text(encoding='utf-8').splitlines():
        item=json.loads(line);payload=item.get('payload',{})
        if item.get('type')=='response_item' and payload.get('type')=='function_call' and any(t in payload.get('name','') for t in ('spawn_agent','followup_task','send_message')):prompts.append({'timestamp':item.get('timestamp'),'tool':payload['name'],'arguments':json.loads(payload['arguments'])})
    logs=[source]
    for day in ('24','25','26'):
        folder=base/day
        if not folder.exists():continue
        for path in folder.glob('*.jsonl'):
            if path==source:continue
            with path.open(encoding='utf-8') as f:metadata=json.loads(f.readline()).get('payload',{})
            if a.session_id in json.dumps(metadata.get('source',{})):logs.append(path)
    out=Path('D:/RAD/FINAL/Part2/notes');controlling=out/'P3-root/controlling_prompt.txt'
    original=Path('C:/Users/ADMIN/.codex/attachments/9c9f5083-d06d-4284-98a7-5f3e3677b4a7/Pasted text.txt')
    assert original.read_bytes()==controlling.read_bytes(),'Controlling prompt archive must equal the supplied attachment bytes'
    result={'source_session':source.name,'controlling_prompt':str(controlling),'controlling_prompt_sha256':hashlib.sha256(controlling.read_bytes()).hexdigest(),'original_attachment':str(original),'original_equals_archived':True,'dispatched_prompts':prompts,'transcripts':[p.name for p in logs]}
    (out/'P3_prompt_archive.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    with zipfile.ZipFile(out/'P3_transcripts.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in logs:archive.write(path,path.name)
        archive.write(controlling,controlling.name)
        for report in Path('D:/RAD/FINAL/SaigonBite/docs/part2/_agent_reports').glob('P3-*.md'):archive.write(report,report.name)
    print(json.dumps({'actual_prompts':len(prompts),'transcripts':len(logs),'archive':str(out/'P3_transcripts.zip')}))
if __name__=='__main__':main()
