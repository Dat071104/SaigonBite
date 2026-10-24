"""Build exact anchor references and a separate, exhaustive SSD request ledger."""
from pathlib import Path
from html import unescape
import csv
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(r'D:\RAD\FINAL'); REPO=ROOT/'SaigonBite'; DOC=REPO/'docs/part2'; NOTES=ROOT/'Part2/notes'
def csvrows(p):
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def table_rows(p,ids):
    result={}
    for line in p.read_text(encoding='utf-8').splitlines():
        if not re.match(r'^\| UC\d\d-(?:PC|MG)\d\d \|',line): continue
        cells=[x.strip() for x in line.strip('|').split('|')]
        if cells[0] in ids and len(cells)==5: result[cells[0]]=cells
    return result
def drawings(uc,kind):
    paths=sorted((REPO/'models'/uc).glob(kind+'_uc'+uc[-2:]+'*.drawio'))
    split=[p for p in paths if '_Part' in p.name]
    return split or paths
def plain(s): return re.sub('<[^>]+>',' ',unescape(s or ''))
def index(uc,kind):
    return {p:{c.get('id'):c for c in ET.parse(p).findall('.//mxCell')} for p in drawings(uc,kind)}
def references(uc,kind,ids,parts=None):
    idx=index(uc,kind); out=[]
    for ident in ids:
        hit=[p for p,cs in idx.items() if ident in cs and (not parts or p.stem in parts)]
        assert hit,(uc,kind,ident,parts)
        out += [p.relative_to(REPO).as_posix()+'#'+ident for p in hit]
    return '; '.join(dict.fromkeys(out))
def exact_refs(uc,kind,spec):
    return '; '.join(references(uc,kind,ids,[stem]) for stem,ids in spec.items())
def params_in(text,op):
    start=text.find(op+'(')
    if start<0: return None
    i=start+len(op)+1; begin=i; depth=1
    while i<len(text):
        depth += (text[i]=='(')-(text[i]==')')
        if depth==0: return text[begin:i]
        i+=1
    return None

def main():
    anchors=csvrows(DOC/'pc_mg_register.csv'); ids={a['id'] for a in anchors}; byid={a['id']:a for a in anchors}
    ecsv=csvrows(NOTES/'P2-E/consistency_rows.csv')
    f=table_rows(DOC/'_agent_reports/P2-F.md',ids); g=table_rows(DOC/'_agent_reports/P2-G.md',ids)
    matrix=[]
    def add(ident,steps,act,ssd,fact):
        a=byid[ident]; matrix.append({'UC':a['UC'],'PC/MG':ident,'description step':f"docs/part2/{a['UC']}/description.md: {steps}",'activity node':act,'SSD message':ssd,'state transition or stored fact':'docs/part2/report/II_state_machines.md; '+fact,'BR':a['BR']})
    for r in ecsv:
        uc=byid[r['id']]['UC']
        add(r['id'],r['description'],references(uc,'activity',r['activity_nodes'].split(';')),references(uc,'ssd',r['SSD_messages'].split(';')),r['state_fact'])
    next(r for r in matrix if r['PC/MG']=='UC05-MG01')['SSD message'] += '; '+references('UC-05','ssd',['05S-R08d','05S-R09c'])
    fact_nodes={
      'UC02-PC01':{'activity_uc02_PartA':['S_effect','D_valid','D_commit']},
      'UC02-PC02':{'activity_uc02_PartB':['S_effect','D_valid','D_commit','A_result']},
      'UC02-PC03':{'activity_uc02_PartC':['S_effect','D_valid','D_commit','A_result']},
      'UC02-MG01':{f'activity_uc02_Part{x}':['S_refuse','S_rollback','D_valid','D_commit','M_end'] for x in 'ABC'},
      'UC04-PC01':{f'activity_uc04_Part{x}':['S_effect','D_commit','A_result'] for x in 'ABC'},
      'UC04-PC02':{'activity_uc04_PartC':['A_result','N']},
      'UC04-MG01':{f'activity_uc04_Part{x}':['S_effect','S_refuse','S_rollback','A_result','M_end'] for x in 'ABC'},
      'UC04-MG02':{f'activity_uc04_Part{x}':['D_valid','S_refuse'] for x in 'ABC'}}
    fssd={
      'UC02-PC01':{'ssd_uc02_PartA':['M03','M03r']},'UC02-PC02':{'ssd_uc02_PartB':['M04','M04r']},
      'UC02-PC03':{'ssd_uc02_PartB':['M05','M05r']},
      'UC02-MG01':{'ssd_uc02_PartA':['M01','M01r','M02','M02r','M03','M03r'],'ssd_uc02_PartB':['M04','M04r','M05','M05r']},
      'UC04-PC01':{'ssd_uc04':['M01','M01r','M02','M02r','M03','M03r']},'UC04-PC02':{'ssd_uc04':['M03','M03r']},
      'UC04-MG01':{'ssd_uc04':['M01','M01r','M02','M02r','M03','M03r']},'UC04-MG02':{'ssd_uc04':['M01','M01r','M02','M02r','M03','M03r']}}
    for ident,r in f.items():
        uc=byid[ident]['UC']; add(ident,r[1],exact_refs(uc,'activity',fact_nodes[ident]),exact_refs(uc,'ssd',fssd[ident]),r[4])
    gact={
      'UC03-PC01':['H-request','H-validate','H-valid','H-save'],'UC03-PC02':['H-request','H-validate','H-save'],'UC03-MG01':['H-validate','H-valid','H-refuse'],
      'UC06-PC01':[p+'-'+x for p in ['CA','CB'] for x in ['request','validate','save']],
      'UC06-PC02':['CC-request','CC-validate','CC-save'],
      'UC06-PC03':[p+'-'+x for p in ['CA','CB','CC'] for x in ['save','validate']],
      'UC06-MG01':[p+'-'+x for p in ['CA','CB','CC'] for x in ['save','refuse']],
      'UC06-MG02':[p+'-'+x for p in ['CA','CB','CC'] for x in ['validate','valid','refuse']]}
    gssd={
      'UC03-PC01':{'ssd_uc03':['M03-03','M03-04','saved']},'UC03-PC02':{'ssd_uc03':['M03-05','saved']},'UC03-MG01':{'ssd_uc03':['M03-02_return','M03-03','M03-04','M03-05','refused']},
      'UC06-PC01':{f'ssd_uc06_Part{p}':[f'M06-{p}0{x}' for x in [2,3,4]]+['saved'] for p in 'AB'},
      'UC06-PC02':{'ssd_uc06_PartC':['M06-C02','M06-C03','M06-C04','saved']},
      'UC06-PC03':{'ssd_uc06_PartA':['M06-A04','saved'],'ssd_uc06_PartB':['M06-B04','saved'],'ssd_uc06_PartC':['M06-C02','M06-C03','saved']},
      'UC06-MG01':{f'ssd_uc06_Part{p}':[f'M06-{p}0{x}' for x in [2,3,4]]+['saved','refused'] for p in 'ABC'},
      'UC06-MG02':{'ssd_uc06_PartA':['M06-A02','M06-A03','refused'],'ssd_uc06_PartB':['M06-B02','M06-B03','refused'],'ssd_uc06_PartC':['M06-C02','refused']}}
    for ident,r in g.items():
        uc=byid[ident]['UC']; add(ident,r[1],references(uc,'activity',gact[ident]),exact_refs(uc,'ssd',gssd[ident]),r[4].replace('Duplicate active names/pair','Duplicate names including retained archived names / pair'))
    assert {r['PC/MG'] for r in matrix}==ids and len(matrix)==30
    matrix.sort(key=lambda r:(r['UC'],r['PC/MG']))
    with (DOC/'analysis_consistency.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['UC','PC/MG','description step','activity node','SSD message','state transition or stored fact','BR']); writer.writeheader();writer.writerows(matrix)
    # Requests belong to a separate coverage ledger: a read query does not
    # establish a later creation postcondition simply to fill a matrix cell.
    ops={r['operation']:r for r in csvrows(DOC/'ssd_operations.csv')}; requests=[]
    e=json.loads((NOTES/'P2-E/selfcheck.json').read_text(encoding='utf-8'))
    for r in e['operations']:
        refs=references(r['UC'],'ssd',[r['message']]); requests.append({'UC':r['UC'],'operation':r['operation'],'catalogue_id':r['catalogue'],'description step':r['description_steps'],'SSD message':refs})
    fdata=json.loads((NOTES/'P2-F/ssd_uc04_verification.json').read_text(encoding='utf-8'))
    fsteps={('UC-02','M01'):'1;4;A03/A04',('UC-02','M02'):'2;4;A03',('UC-02','M03'):'3',('UC-02','M04'):'5;A01',('UC-02','M05'):'A02',('UC-04','M01'):'2–4',('UC-04','M02'):'A01',('UC-04','M03'):'A02/A03'}
    for r in fdata['operations']:
        requests.append({'UC':r['UC'],'operation':r['operation'],'catalogue_id':r['catalogue'],'description step':fsteps[(r['UC'],r['message'])],'SSD message':references(r['UC'],'ssd',[r['message']],[r['SSD']])})
    for r in csvrows(NOTES/'P2-G/operation_flow_membership.csv'):
        requests.append({'UC':r['UC'],'operation':r['operation'],'catalogue_id':r['catalogue_id'],'description step':r['description_step'],'SSD message':Path(r['SSD_file']).relative_to(REPO).as_posix()+'#'+r['SSD_message']})
    for r in requests:
        op=ops[r['operation']]; assert op['op_id']==r['catalogue_id']
        uc=r['UC']; desc=(DOC/uc/'description.md').read_text(encoding='utf-8'); assert r['operation'] in desc
        loc=r['SSD message'].split('; ')[0]; path,ident=loc.split('#',1); tree=ET.parse(REPO/path)
        lookup={c.get('id'):c for c in tree.findall('.//mxCell')}; assert ident in lookup
        candidates=[params_in(plain(c.get('value')),r['operation']) for c in lookup.values()]
        expected=re.sub(r'\s+','',op['parameters']); assert any(x is not None and re.sub(r'\s+','',x)==expected for x in candidates),(r['operation'],expected,candidates)
        r['parameters']=op['parameters'];r['BR']=op['guards (BR)'];r['description step']=f'docs/part2/{uc}/description.md: '+r['description step']
    assert len(requests)==41,len(requests)
    with (DOC/'ssd_flow_membership.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['UC','operation','catalogue_id','parameters','description step','SSD message','BR']);writer.writeheader();writer.writerows(requests)
    out={'anchor_rows':len(matrix),'request_occurrences':len(requests),'distinct_operations':len({r['operation'] for r in requests}),'all_native_ids_resolved':True,'all_parameters_match_catalogue':True,'all_requests_in_descriptions':True,'read_queries_not_falsely_treated_as_creation_effects':True}
    (NOTES/'P2-root/consistency_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))

if __name__=='__main__': main()
