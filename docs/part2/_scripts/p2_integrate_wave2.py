"""Apply root's concrete Wave 2 notation and conservative contract decisions."""
from pathlib import Path
import importlib.util
import json
import re

ROOT=Path(r'D:\RAD\FINAL'); REPO=ROOT/'SaigonBite'; DOC=REPO/'docs/part2'
OUT=ROOT/'Part2/notes/P2-root'
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def main():
    plan=(ROOT/'PLAN_SaigonBite_Part2_Final.md').read_text(encoding='utf-8')
    names={}
    for line in plan.split('### 2.1 Main use cases',1)[1].split('### 2.2 Supporting',1)[0].splitlines():
        if line.startswith('| UC-'):
            f=[s.strip() for s in line.strip('|').split('|')]; names[f[0]]=f[1]
    for uc,name in names.items():
        n=int(uc[-2:]); p=DOC/uc/'description.md'; lines=p.read_text(encoding='utf-8').splitlines()
        lines[0]=f'# {uc} — {name} (author: 722I0004)'
        result=[]; i=0
        while i<len(lines):
            if lines[i].strip()=='| Step | Actor | System |':
                result+=['| Actor | System |','|---|---|']; i+=2
                while i<len(lines) and lines[i].startswith('|'):
                    f=[s.strip() for s in lines[i].strip('|').split('|')]
                    assert len(f)==3,(uc,f)
                    step,actor,system=f
                    if actor: actor=step+'. '+actor
                    else: system=step+'. '+system
                    result.append('| '+actor+' | '+system+' |'); i+=1
                continue
            result.append(lines[i]); i+=1
        p.write_text('\n'.join(result).rstrip()+'\n',encoding='utf-8')
        p=DOC/'report'/f'II_2-2-{n}_{uc}.md'; t=p.read_text(encoding='utf-8')
        t=re.sub(r'^#+ 2\.2\.\d+ Use Case \d+:.*$',f'# 2.2.{n} Use Case {n}: {name} (author: 722I0004)',t,count=1,flags=re.M)
        p.write_text(t.rstrip()+'\n',encoding='utf-8')
    p=DOC/'UC-04/description.md'; t=p.read_text(encoding='utf-8')
    t=t.replace('current snapshot per active operational hub:', 'current snapshot per hub, retaining archived hub identities for reporting (BR-18 / UC03-PC02):')
    t=t.replace('historical archive flags do not remove relevant retained order facts.', 'historical archive flags do not remove relevant retained facts. An archived hub has zero open cooking/READY/OUT_FOR_DELIVERY work under BR-18; identify its archived status rather than hiding it from reports.')
    p.write_text(t,encoding='utf-8')
    # Exact main names and no implicit archived-name reuse.
    p=DOC/'UC-06/description.md'; t=p.read_text(encoding='utf-8')
    for a,b in [('uniqueness among active brands','unique Brand name'),('unique active-brand name','unique Brand name'),('unique active item name within that Brand','unique item name within that Brand'),('duplicate active name','duplicate name')]: t=t.replace(a,b)
    if 'Duplicate checks include retained archived names' not in t:
        t+='\nDuplicate checks include retained archived names in their uniqueness scope; this conservative analysis promises neither archived-name reuse nor restore/reparenting. Draft-only maximum lengths, prices, capacity and HCMC coordinate bounds are not promoted into new locked business rules.\n'
    p.write_text(t,encoding='utf-8')
    for p in (REPO/'models/UC-06').glob('*.json'):
        if not p.name.startswith(('activity_uc06','ssd_uc06')): continue
        text=p.read_text(encoding='utf-8')
        for a,b in [('unique active-brand name','unique Brand name'),('unique active name within Brand','unique name within Brand'),('unique active item name in Brand','unique item name in Brand')]: text=text.replace(a,b)
        p.write_text(text,encoding='utf-8')
    # Each F generator writes only its own named page; update common embedded data.
    for folder in ['UC-02','UC-04']:
        for p in (REPO/'models'/folder).glob('*.py'):
            if not p.name.startswith(('activity_uc02','ssd_uc02','activity_uc04','ssd_uc04')): continue
            t=p.read_text(encoding='utf-8').replace('A01: Current active hubs\\n','A01: Hubs incl. archived\\n')
            p.write_text(t,encoding='utf-8')
    fdir=OUT/'F-integration'; fdir.mkdir(exist_ok=True)
    m=load(REPO/'models/UC-04/activity_uc04_PartB.py','p2_f_root_rebuild'); m.SCRATCH=fdir; m.main()
    gdir=OUT/'G-integration'; gdir.mkdir(exist_ok=True)
    for stem in ['activity_uc06','ssd_uc06']:
        m=load(REPO/f'models/UC-06/{stem}.py','p2_g_root_'+stem); m.SCR=gdir; m.build(REPO/f'models/UC-06/{stem}.json')
    # Correct the root catalogue's earlier spacing typo consistently in E's return.
    for folder in ['UC-01','UC-05']:
        for p in (REPO/'models'/folder).glob('*.py'):
            if p.name.startswith(('activity_uc','ssd_uc')):
                value=p.read_text(encoding='utf-8').replace('quoteWithFingerprintAndSD FQT','quoteWithFingerprintAndSDFQT')
                value=value.replace('5 Recheck active role; token ownership\\nDo not authorize a replay','5 Begin short checkout transaction\\nRecheck active role; token ownership\\nDo not authorize a replay')
                p.write_text(value,encoding='utf-8')
    p=DOC/'UC-01/description.md'; value=p.read_text(encoding='utf-8').replace('quoteWithFingerprintAndSD FQT','quoteWithFingerprintAndSDFQT')
    value=value.replace('Revalidates active session/role; token is distinct from CSRF. Checks token ownership:', 'Begins the short checkout transaction and revalidates active session/role; token is distinct from CSRF. Checks token ownership inside that same atomic boundary:')
    value=value.replace('in one short write transaction, rechecks all step-3 guards', 'continuing the same short write transaction from step 5, rechecks all step-3 guards')
    p.write_text(value,encoding='utf-8')
    edir=OUT/'E-integration'; edir.mkdir(exist_ok=True)
    m=load(REPO/'models/UC-01/ssd_uc01.py','p2_e_root_rebuild'); m.S=edir
    pages=m.build_ssd01(); m.aliases('UC-01','ssd',pages)
    pages=m.build_activity01(); m.aliases('UC-01','activity',pages)
    p=DOC/'report/II_2-3_crud.md'; t=p.read_text(encoding='utf-8').replace('delivery contact/address snapshots','delivery contact and the saved address snapshot'); p.write_text(t,encoding='utf-8')
    print('Wave 2 root corrections applied; all descriptions use two-column numbered flows and exact titles.')

if __name__=='__main__': main()
