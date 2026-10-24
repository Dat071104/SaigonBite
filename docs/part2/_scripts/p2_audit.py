"""Deterministic structural checks for the Phase 2 analysis artifact bundle.

This is document validation, never an application test or native-app qualification.
"""
from pathlib import Path
from html import unescape
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(r'D:\RAD\FINAL'); REPO=ROOT/'SaigonBite'; DOC=REPO/'docs/part2'
OUT=ROOT/'Part2/notes/P2-root'
def readcsv(name):
    with (DOC/name).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def plain(value): return re.sub('<[^>]+>',' ',unescape(value or ''))

def main():
    ops=readcsv('ssd_operations.csv'); anchors=readcsv('pc_mg_register.csv')
    names={r['operation'] for r in ops}; ids={r['id'] for r in anchors}
    assert len(names)==len(ops) and all(re.fullmatch('[a-z][A-Za-z0-9]*',n) for n in names)
    assert len(ids)==len(anchors)==30
    p=(ROOT/'PLAN_SaigonBite_Part2_Final.md').read_text(encoding='utf-8').split('**P2.3 Postcondition anchors',1)[1].split('Exit G2:',1)[0]
    for a in anchors: assert a['text'] in p,(a['id'],'anchor text drift')
    assert {'confirmCheckout','confirmOrder','rejectOrder','offerReplacement','acceptReplacement','declineReplacement','cancelOrder','startPreparing','markReady','takeDelivery','confirmDelivered','reportFailure'}<=names
    drawings=[]; suspicious=[]
    new_drawings=[]
    for path in (REPO/'models').rglob('*.drawio'):
        if path.name.startswith(('use_case_diagram','domain_model','sm_','activity_uc','ssd_uc')): new_drawings.append(path)
    for path in sorted(new_drawings):
        tree=ET.parse(path); pages=tree.findall('.//diagram'); assert pages,path
        for page in pages:
            cs=page.findall('.//mxCell'); assert cs,(path,'compressed/empty source not inspected')
            lookup={c.get('id') for c in cs}
            assert len(lookup)==len(cs),(path,'duplicate IDs')
            for c in cs:
                if c.get('edge')=='1':
                    assert c.get('source') in lookup and c.get('target') in lookup,(path,c.get('id'),'dangling edge')
                if path.name.startswith('ssd_uc'):
                    label=plain(c.get('value'))
                    for match in re.finditer(r'(?<![-\w])([a-z][A-Za-z0-9]*)\(',label):
                        # Nested lines(itemId, quantity) is a parameter type;
                        # result (PCxx) and AI-assisted (Codex) are not calls.
                        prefix=label[:match.start()]
                        if prefix.count('(')>prefix.count(')'): continue
                        n=match.group(1)
                        if n not in names: suspicious.append({'file':str(path.relative_to(REPO)),'cell':c.get('id'),'label':label,'unregistered_token':n})
        for ext in ('.png','.svg'): assert path.with_suffix(ext).exists(),(path,'missing export',ext)
        svg=ET.parse(path.with_suffix('.svg')); root=svg.getroot()
        drawings.append({'path':path.relative_to(REPO).as_posix(),'pages':len(pages),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'svg_viewBox':root.get('viewBox'),'svg_width':root.get('width')})
    desc={}
    for n in range(1,7):
        uc=f'UC-{n:02}'; text=(DOC/uc/'description.md').read_text(encoding='utf-8')
        needed=[a['id'] for a in anchors if a['UC']==uc]
        assert all(i in text for i in needed),(uc,'missing PC/MG')
        assert '722I0004' in text and 'AI-assisted (Codex)' in text
        fields=['Use case name','Scenario / trigger','Actors','Related use cases','Stakeholders and interests','Pre-conditions','Post-conditions','Flow of activities','Exception conditions']
        positions=[text.lower().find(f.lower()) for f in fields]
        assert min(positions)>=0 and positions==sorted(positions),(uc,'template order',positions)
        assert '| Step | Actor | System |' not in text,(uc,'main flow must have two columns')
        assert '| Actor | System |' in text,(uc,'main flow missing')
        desc[uc]={'anchors':needed,'template_fields_in_order':True}
    matrix=readcsv('analysis_consistency.csv')
    assert ids <= {r['PC/MG'] for r in matrix},'Unresolved anchor'
    for r in matrix:
        assert all(r[k].strip() for k in ['UC','PC/MG','description step','activity node','SSD message','state transition or stored fact','BR']),(r,'empty consistency field')
        assert r['PC/MG'] in ids
    requests=readcsv('ssd_flow_membership.csv')
    assert len(requests)==41
    for r in requests:
        assert r['operation'] in names and r['operation'] in (DOC/r['UC']/'description.md').read_text(encoding='utf-8')
    trace=readcsv('traceability.csv')
    for r in trace:
        for col in ['design operation','screen/control','code method','test ID','result evidence']: assert not r[col],(r['Req ID'],col,'premature evidence')
        if r['status']=='Analysed': assert r['PC/MG ID'],r['Req ID']
    assembled=(DOC/'report/II_system_requirements_analysis.md').read_text(encoding='utf-8')
    assert '<!-- include:' not in assembled,'Unresolved include'
    numbered=re.findall(r'^#{2,3} (2\.[123](?:\.\d+)?)(?:\s|$)',assembled,re.M)
    expected=['2.1']+[f'2.1.{n}' for n in range(1,8)]+['2.2']+[f'2.2.{n}' for n in range(1,7)]+['2.3']+[f'2.3.{n}' for n in range(1,6)]
    assert numbered==expected,numbered
    captions=[line for line in assembled.splitlines() if re.match(r'^Figure \d+(?:\.\d+)+[A-Z]?\.\s',line)]
    assert len(captions)==52,len(captions)
    assert all('Author: 722I0004 · AI-assisted (Codex)' in line for line in captions)
    for n in range(1,8): assert f'2.1.{n} ' in assembled
    for n in range(1,7):
        assert f'2.2.{n} Use Case {n}:' in assembled
        for prefix in ('ii. Activity diagram','iii. System sequence diagram','iv. State machine diagram'): assert f'{prefix} for Use Case {n}' in assembled
    for n in range(1,6): assert f'2.3.{n} Verifying use cases for ' in assembled
    assert not suspicious,suspicious
    # Every local report model reference must resolve after include assembly.
    missing=[]
    for href in re.findall(r'\]\(([^)]+)\)',assembled):
        if '://' in href or href.startswith('#'): continue
        target=(DOC/'report'/href.split('#')[0]).resolve()
        if not target.exists(): missing.append(href)
    assert not missing,missing
    out={'operation_count':len(ops),'anchor_count':len(anchors),'drawings':drawings,'descriptions':desc,'matrix_rows':len(matrix),'ssd_request_occurrences':len(requests),'trace_rows':len(trace),'numbered_headings_exact_order':True,'authored_figure_views':len(captions),'unregistered_ssd_tokens_for_manual_review':suspicious,'local_links_resolve':True,'application_tests_run':False,'structural_pass':True}
    (OUT/'analysis_structural_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('drawings','descriptions')},indent=2))

if __name__=='__main__': main()
