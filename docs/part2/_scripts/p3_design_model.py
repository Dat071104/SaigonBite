"""Generate the sole shared design model from committed AST facts and annotations.
Author: 722I0004 · AI-assisted (Codex). Does not import the application.
"""
from pathlib import Path
import ast,copy,csv,json,re
R=Path(__file__).resolve().parents[3];D=R/'docs/part2/design'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def layer(path):
    if '/presentation/' in path:return 'view'
    if '/controllers/' in path:return 'controller'
    if '/domain/' in path:return 'domain'
    return 'data_access'
def build():
    inventory=read(D/'code_inventory.json');annotations=read(D/'design_annotations.json');classes={}
    for path,module in inventory['modules'].items():
        if path in ('app.py','init_db.py','saigonbite/__init__.py') or path.endswith('/__init__.py'):continue
        role=layer(path)
        for source in module['classes']:
            c=copy.deepcopy(source);name=c['name'];c.update(module=path,layer=role,stereotype='enumeration' if c['enum_members'] else 'DAO' if name.endswith('DAO') else 'gateway' if name=='PaymentGatewaySimulator' else 'controller' if name.endswith('Controller') else 'entity' if role=='domain' else 'value',status='MATCH',responsibility=annotations.get('responsibilities',{}).get(name,{'view':'Accept a request and render the controller result.','controller':'Coordinate authorization, domain decisions and data access.','domain':'Hold typed business state and its local rules.','data_access':'Read or write parameterized records.'}[role]),source_kind='class')
            for a in c['attributes']:
                a.update(status='MATCH',inferred=not a['annotated'])
                a['diagram_omit']=role=='domain' and a['name'].endswith('_id')
                if a['type']=='Any' and a['default'] and '.' in a['default']:
                    a['type']=a['default'].split('.')[0];a['inferred']=True
            for m in c['methods']:m.update(status='MATCH',inferred=not m['annotated'])
            classes[name]=c
        if module['functions']:
            name=path.rsplit('/',1)[-1][:-3]
            if role=='view' and not module['blueprints']:name='presentation.'+name
            elif role=='data_access':name='data_access.'+name
            elif role=='controller':name='controllers.'+name
            elif role=='domain':name='domain.'+name
            methods=copy.deepcopy(module['functions'])
            for m in methods:m.update(status='MATCH',inferred=not m['annotated'])
            classes[name]={'name':name,'module':path,'layer':role,'stereotype':'view' if module['blueprints'] else 'module','source_kind':'blueprint' if module['blueprints'] else 'module','attributes':[],'methods':methods,'responsibility':annotations.get('responsibilities',{}).get(name,'Module functions with their original Python signatures.'),'status':'MATCH','bases':[],'enum_members':[],'routes':module['routes']}
    for name,c in classes.items():
        for override in annotations.get('elements',{}).get(name,[]):
            kind=override.get('kind','method');bucket=c['attributes'] if kind=='attribute' else c['methods'];existing=next((x for x in bucket if x['name']==override['name']),None)
            if existing is None:
                existing={'visibility':'-' if override['name'].startswith('_') else '+','annotated':True,'inferred':False,'source_kind':'proposed'};bucket.append(existing)
            existing.update(override)
            if kind=='method' and override.get('signature'):
                node=ast.parse('def '+override['signature']+':\n pass').body[0]
                existing['return']=ast.unparse(node.returns) if node.returns else 'Any'
                existing['return_annotated']=node.returns is not None
                # Full target signature is authoritative; never leave baseline
                # parameter/return metadata attached to a changed signature.
                params=node.args.posonlyargs+node.args.args;defaults=[None]*(len(params)-len(node.args.defaults))+node.args.defaults
                existing['parameters']=[{'name':p.arg,'type':ast.unparse(p.annotation) if p.annotation else 'Any','annotated':p.annotation is not None,'default':ast.unparse(v) if v is not None else None,'kind':'positional_or_keyword'} for p,v in zip(params,defaults)]
        if any(x['status']!='MATCH' for x in c['methods']+c['attributes']):c['status']='P4-TARGET'
    dependencies=[]
    for name,c in classes.items():
        attrs={a['name']:a['type'] for a in c['attributes']}
        calls=set()
        for m in c['methods']:
            for call in m.get('calls',[]):
                target=call['target'];parts=target.split('.')
                if parts[0]=='self' and len(parts)>2:
                    dest=attrs.get(parts[1]);
                    if dest in classes:calls.add(dest)
                elif parts[0] in classes and parts[0]!=name:
                    # Local entity variables named order/delivery are not the
                    # identically named Flask blueprint modules.
                    if not (c['layer']!='view' and classes[parts[0]].get('source_kind')=='blueprint'):calls.add(parts[0])
                elif len(parts)==1:
                    for module_name,module_class in classes.items():
                        if module_class['source_kind']=='module' and any(x['name']==target for x in module_class['methods']):calls.add(module_name)
        for a in c['attributes']:
            for dest in re.findall(r'\b[A-Za-z_]\w*\b',a['type']):
                if dest in classes and dest!=name:calls.add(dest)
        for method in c['methods']:
            for dest in re.findall(r'\b[A-Za-z_]\w*\b',method.get('signature','')):
                if dest in classes and dest!=name:calls.add(dest)
        rank={'view':0,'controller':1,'domain':2,'data_access':3}
        for dest in sorted(calls):dependencies.append({'source':name,'target':dest,'kind':'dependency','status':'MATCH','source_evidence':'AST call or typed attribute/signature','allowed_on_layered_diagram':rank[classes[dest]['layer']]>=rank[c['layer']] and not (c['layer']=='domain' and classes[dest]['layer']!='domain')})
    for dep in annotations.get('target_dependencies',[]):dependencies.append(dep)
    for name,fields in annotations.get('class_annotations',{}).items():
        if name in classes:classes[name].update(fields)
    associations=copy.deepcopy(annotations['associations'])
    for name,c in classes.items():
        for base in c.get('bases',[]):
            if base in classes and not any(x['source']==name and x['target']==base and x['kind']=='generalization' for x in associations):associations.append({'source':name,'target':base,'source_multiplicity':None,'target_multiplicity':None,'role':'inherits','kind':'generalization','navigable':False,'status':'MATCH','evidence':'AST class base'})
    for relation in associations:
        if relation['kind']=='generalization':relation['source_multiplicity']=None;relation['target_multiplicity']=None
    model={'author':inventory['author'],'C0':inventory['commit'],'evidence_label':'Static / target design','classes':classes,'associations':associations,'dependencies':dependencies,'annotations_source':'docs/part2/design/design_annotations.json','operation_rows':list(csv.DictReader((D/'operation_realisation.csv').open(encoding='utf-8-sig',newline=''))),'notation':{'domain_fk_attributes':'Retained in inventory and mapping; omitted on domain DCD in favor of named associations.','generated_constructors':'Dataclass initialization is implicit; use a create message plus field note rather than inventing public methods.','status':'MATCH means static code correspondence only. A behavior target stays marked until reviewed evidence clears it.'}}
    (R/'models/shared/design_model.json').write_text(json.dumps(model,indent=2,ensure_ascii=False),encoding='utf-8');print('Shared model:',len(classes),'class/module roles,',len(model['operation_rows']),'SSD occurrences')
    return model
if __name__=='__main__':build()
