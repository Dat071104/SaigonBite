"""Audit assembled design sources, local figures and future evidence boundaries.
Author: 722I0004 · AI-assisted (Codex). Read-only except its private receipt.
"""
from pathlib import Path
import collections,csv,hashlib,json,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[3];D=R/'docs/part2';N=R.parent/'Part2/notes/P3-root'
def main():
    checks=[]
    def check(key,ok,detail):checks.append({'key':key,'pass':bool(ok),'detail':detail})
    III=D/'report/III_system_requirements_design.md';IV=D/'report/IV_system_requirements_implementation.md';texts={p.name:p.read_text(encoding='utf-8') for p in (III,IV)}
    for path in (III,IV):
        text=texts[path.name];check(path.name+':includes','<!-- include:' not in text,'All source includes resolved');check(path.name+':author','Author: 722I0004 · AI-assisted (Codex)' in text,'Actual author declared')
        for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text):
            value=target.strip('<>');file=(path.parent/value).resolve();check(path.name+':image:'+value,file.is_file(),'Local image exists')
            if file.is_file():
                try:file.relative_to(R.resolve());valid=True
                except ValueError:valid=False
                check(path.name+':source_image:'+value,valid,'Repo artifact source; no hand-made staging source')
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',text):
            value=target.strip('<>').split('#',1)[0]
            if not value or re.match(r'[A-Za-z]+:',value):continue
            check(path.name+':link:'+value,(path.parent/value).resolve().is_file(),'Editable source/vector/data/report links resolve, not just image embeds')
        for caption in re.findall(r'^\*{0,2}Figure\s+[34][.\w -]*\..*$',text,re.M):check(path.name+':caption:'+caption[:65],'722I0004' in caption and 'AI-assisted' in caption,'Figure caption attribution')
    for uc in range(1,7):
        for number in range(1,6):check(f'heading:3.{uc}.{number}',bool(re.search(r'^### 3\.'+str(uc)+r'\.'+str(number)+r' ',texts[III.name],re.M)),'Required exact template subsection level')
        for sub in ('i. Domain design class','ii. Controller','iii. UI (view)','iv. Data access','v. Design class (all layers together)'):check(f'UC{uc:02}:DCD:'+sub,sub in (D/f'report/III_3-{uc}_UC-{uc:02}.md').read_text(encoding='utf-8'),'Five template DCD views')
    iv=texts[IV.name]
    for n in range(3,7):
        match=re.search(r'^### 4\.3\.'+str(n)+r' .*?\n(.*?)(?=^### |\Z)',iv,re.M|re.S);body=match[1].strip() if match else ''
        check(f'future:4.3.{n}',bool(re.fullmatch(r'⟦PENDING: .*?⟧',body,re.S)),'Only the later-phase pending marker belongs in this subsection')
    trace=list(csv.DictReader((D/'traceability.csv').open(encoding='utf-8-sig',newline='')))
    for row in trace:
        check('trace:'+row['Req ID'],all(not row[c] for c in ('screen/control','code method','test ID','result evidence')) and row['status'] in ('Analysed','Planned'),'No invented implementation, test, result, or status')
    figures=[]
    for path in (R/'models').rglob('*.json'):
        data=json.loads(path.read_text(encoding='utf-8-sig'))
        if 'phase3' not in data:continue
        files={ext:hashlib.sha256(path.with_suffix(ext).read_bytes()).hexdigest() for ext in ('.py','.json','.drawio','.svg','.png') if path.with_suffix(ext).is_file()}
        figures.append({'stem':path.relative_to(R).with_suffix('').as_posix(),'hashes':files,'diagram_type':data['phase3'].get('diagram_type')})
        check(path.stem+':source-set',len(files)==5,'Generator+JSON+editable source+both exports')
    sources={III,IV,D/'traceability.csv',Path(__file__),Path(__file__).with_name('p3_assemble.py')}
    sources.update((D/'report').glob('III_3-*.md'));sources.update((D/'report').glob('IV_4-*.md'))
    sources.update(D.glob('UC-*/design_classes.md'));sources.update(D.glob('UC-*/crc.md'))
    source_hashes={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sources)}
    failures=[c for c in checks if not c['pass']];out={'author':'722I0004 · AI-assisted (Codex)','pass':not failures,'checks':checks,'failures':failures,'figures':figures,'source_hashes':source_hashes,'counts':dict(collections.Counter(f['diagram_type'] for f in figures))};N.mkdir(exist_ok=True);(N/'artifact_audit.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps({'pass':out['pass'],'checks':len(checks),'figures':len(figures),'counts':out['counts'],'failures':failures[:20]},indent=2,ensure_ascii=False));assert out['pass']
if __name__=='__main__':main()
