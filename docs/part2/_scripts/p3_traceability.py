"""Fill design references without inventing code/test/result evidence or statuses.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import csv,json,re
R=Path(__file__).resolve().parents[3];D=R/'docs/part2';N=R.parent/'Part2/notes/P3-root'
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def main():
    trace=rows(D/'traceability.csv');real=rows(D/'design/operation_realisation.csv');byid={}
    for row in real:byid.setdefault(row['op_id'],[]).append(row)
    diagrams=[]
    for path in sorted((R/'models').rglob('seq_uc*.json')):
        meta=json.loads(path.read_text(encoding='utf-8')).get('phase3',{})
        if meta.get('diagram_type')=='sequence':diagrams.append((path,meta))
    # Supporting receipt/tracking/cancel/availability requirements that also have
    # explicit main-UC SSD messages are mapped to those exact occurrences.
    additional={4:['OP-13','OP-14','OP-25'],5:['OP-15'],6:['OP-13','OP-15','OP-01'],7:['OP-15'],8:['OP-15'],9:['OP-15'],15:['OP-17','OP-18'],16:['OP-16'],17:['OP-07'],18:['OP-21','OP-22'],23:['OP-27'],24:['OP-26'],25:['OP-28'],29:['OP-18','OP-05','OP-06'],33:['OP-06'],35:['OP-44']}
    changes=[]
    for row in trace:
        before=dict(row);anchors=set(re.findall(r'UC\d\d-(?:PC|MG)\d\d',row['PC/MG ID']));selected=[]
        for operation in real:
            if anchors & set(re.findall(r'UC\d\d-(?:PC|MG)\d\d',operation['PC/MG ensured'])):selected.append(operation)
        if row['Req ID'].startswith('FR-'):
            for oid in additional.get(int(row['Req ID'].split('-')[1]),[]):selected+=byid[oid]
        refs=[]
        for op in selected:
            for path,meta in diagrams:
                if meta.get('UC')==op['UC'] and meta.get('op_id')==op['op_id']:
                    ref=f"{op['controller.method(signature)'].split('(')[0]} [{op['status']}; {op['op_id']}; {meta['operation']}] + {path.relative_to(R).as_posix().replace('.json','.drawio')}"
                    if ref not in refs:refs.append(ref)
        row['design operation']='; '.join(refs)
        for column in ('screen/control','code method','test ID','result evidence'):assert not row[column],(row['Req ID'],column)
        assert row['status']==before['status'],'No Designed vocabulary was authorized'
        assert all(row[k]==v for k,v in before.items() if k!='design operation')
        if refs:changes.append({'Req ID':row['Req ID'],'design_references':len(refs),'status':row['status']})
    with (D/'traceability.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(trace[0]));w.writeheader();w.writerows(trace)
    N.mkdir(exist_ok=True);(N/'traceability_audit.json').write_text(json.dumps({'rows':len(trace),'design_linked_rows':len(changes),'unchanged_status_vocabulary':True,'future_evidence_blank':True,'design_links':changes},indent=2),encoding='utf-8');print('Design-linked requirements:',len(changes),'of',len(trace),'; status and future evidence preserved')
if __name__=='__main__':main()
