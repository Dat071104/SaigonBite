"""Build the operation/element P4 register from the accepted design annotations.
Author: 722I0004 · AI-assisted (Codex). Static documentation only.
"""
from pathlib import Path
import csv, json, re

R=Path(__file__).resolve().parents[3]
D=R/'docs/part2/design'

def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as handle:
        return list(csv.DictReader(handle))

def main():
    annotations=json.loads((D/'design_annotations.json').read_text(encoding='utf-8'))
    realisation=rows(D/'operation_realisation.csv')
    output=[]
    targets=list(annotations['P4_inputs'])
    for dependency in annotations.get('target_dependencies',[]):
        if dependency['status']=='MATCH':continue
        phases={e['P4_subphase'] for e in annotations['elements'].get(dependency['source'],[]) if set(e['P4_input'].split('; ')) & set(dependency.get('P4_input','').split('; '))}
        targets.append({'element':dependency['source']+' -> '+dependency['target'],'kind':'dependency','status':dependency['status'],'P4 input':dependency['P4_input'],'P4 subphase':dependency.get('P4_subphase') or '; '.join(sorted(phases)),'reason':dependency.get('source_evidence','Explicit typed design dependency')})
    for target in targets:
        name=target['element']
        # Link an exact method call; field targets can also occur in the return
        # type of the responsible controller. A shared-only row is explicit.
        cls=name.split(' -> ')[0] if target.get('kind')=='dependency' else name.rsplit('.',1)[0]
        linked=[]
        for operation in realisation:
            calls='; '.join(operation[c] for c in ('controller.method(signature)','domain calls','DAO calls'))
            exact=bool(re.search(r'(?<![\w.])'+re.escape(name)+r'(?=[(\s;,.]|$)',calls))
            returned_field=any(e['name']==name.rsplit('.',1)[-1] and e.get('kind')=='attribute' for e in annotations.get('elements',{}).get(cls,[])) and bool(re.search(r'\b'+re.escape(cls)+r'\b',calls))
            typed_dependency=target.get('kind')=='dependency' and bool(re.search(r'\b'+re.escape(cls)+r'\b',calls))
            if exact or returned_field or typed_dependency:
                key=(operation['UC'],operation['op_id'])
                if key not in [(x['UC'],x['op_id']) for x in linked]:linked.append(operation)
        if not linked:linked=[{'op_id':'','UC':'shared / supporting','operation':''}]
        for operation in linked:
            output.append({'op_id':operation['op_id'],'UC':operation['UC'],'operation':operation['operation'],'element':name,'kind':target.get('kind','import boundary' if ' -> ' in name else 'member'),'status':target['status'],'P4 input':target['P4 input'],'P4 subphase':target['P4 subphase'],'reason':target['reason'],'evidence':'design_annotations.json; shared design model; committed AST baseline'})
    # Preserve schema-only obligations which are absent from Python members.
    for mapping in rows(D/'class_table_mapping.csv'):
        if not mapping.get('p4_input') or mapping.get('c0_status') not in ('P4-TARGET†','GAP†'):continue
        column=mapping['attribute'] if mapping['column'].startswith('—') else mapping['column']
        element='schema.'+mapping['table']+'.'+column
        record={'op_id':'','UC':'shared / supporting','operation':'','element':element,'kind':'schema / mapping','status':mapping['c0_status'].rstrip('†'),'P4 input':mapping['p4_input'],'P4 subphase':'P4.1' if 'P2-S02' in mapping['p4_input'] else 'P4.7','reason':mapping.get('meaning',''),'evidence':'class_table_mapping.csv; schema.sql at C0'}
        if not any(x['element']==element and x['P4 input']==record['P4 input'] for x in output):output.append(record)
    path=D/'P4_design_inputs.csv'
    with path.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(output[0]));writer.writeheader();writer.writerows(output)
    assert all(x['status'] in ('P4-TARGET','GAP') and x['P4 input'] and x['P4 subphase'] for x in output)
    print(json.dumps({'rows':len(output),'elements':len({x['element'] for x in output}),'operation_linked':sum(bool(x['op_id']) for x in output),'shared_rows':sum(not x['op_id'] for x in output),'file':str(path)},indent=2))

if __name__=='__main__':main()
