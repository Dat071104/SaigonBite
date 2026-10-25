"""Apply evidence to the local Phase 3 checklist without editing item wording.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parents[3];B=R.parent/'Part2'
def main():
    p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,default=B/'notes/P3_checklist_evidence.json');a=p.parse_args();e=json.loads(a.evidence.read_text(encoding='utf-8'));path=B/'codex/P3_CHECKLIST.md';lines=[];done=[];pending=[]
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        m=re.match(r'\| - \[[ x]\] (P3-\d+) \| (.*?) \| (.*?) \|$',line)
        if m:
            key=m[1];entry=e.get(key,{'done':False,'evidence':m[3]});checked=bool(entry['done']);line=f'| - [{"x" if checked else " "}] {key} | {m[2]} | {entry["evidence"].replace("|","/")} |';(done if checked else pending).append(key)
        lines.append(line)
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8');summary={'checked':len(done),'unchecked':pending,'total':len(done)+len(pending),'checked_ids':done};(B/'notes/P3_checklist_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
