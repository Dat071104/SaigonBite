"""Update only evidence-backed Phase 2 checklist boxes and a closure ledger."""
from pathlib import Path
import argparse
import json
import re

ROOT=Path(r'D:\RAD\FINAL'); CHECK=ROOT/'Part2/codex/P2_CHECKLIST.md'
def main():
    p=argparse.ArgumentParser(); p.add_argument('--evidence',required=True); args=p.parse_args()
    evidence=json.loads(Path(args.evidence).read_text(encoding='utf-8'))
    text=CHECK.read_text(encoding='utf-8')
    for key,item in evidence.items():
        assert re.fullmatch(r'P2-\d\d',key)
        assert item.get('evidence')
        checked='x' if item['done'] else ' '
        text,count=re.subn(r'(?<=\| )- \[[ x]\] '+key+r'\b',f'- [{checked}] {key}',text)
        assert count==1,(key,count)
    marker='\n## Phase 2 evidence ledger\n'
    text=text.split(marker)[0]
    lines=[marker,'','Author: 722I0004 · AI-assisted (Codex)','','| ID | Disposition | Evidence / reason |','|---|---|---|']
    for key,item in sorted(evidence.items()):
        lines.append(f"| {key} | {'Done' if item['done'] else 'Open'} | {item['evidence'].replace('|','/')} |")
    CHECK.write_text(text.rstrip()+'\n'+'\n'.join(lines)+'\n',encoding='utf-8')
    counts={'checked':len(re.findall(r'(?<=\| )- \[x\] P2-\d\d\b',text)),'unchecked':re.findall(r'(?<=\| )- \[ \] (P2-\d\d)\b',text),'evidence_records':len(evidence)}
    (ROOT/'Part2/notes/P2_checklist_summary.json').write_text(json.dumps(counts,indent=2),encoding='utf-8'); print(json.dumps(counts,indent=2))

if __name__=='__main__': main()
