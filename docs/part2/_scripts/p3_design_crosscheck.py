"""Re-runnable, fail-closed static design audit against a committed application.
Author: 722I0004 · AI-assisted (Codex).
No application imports, SQL execution or tests. --read-only writes nothing.
"""
from pathlib import Path
import argparse,ast,collections,csv,hashlib,html,importlib.util,json,re,subprocess,sys,xml.etree.ElementTree as ET
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[3];D=R/'docs/part2/design';N=R.parent/'Part2/notes/P3-root'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def csvread(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,encoding='utf-8').strip()
def canonical(signature):
    if not signature:return None
    try:
        n=ast.parse('def '+signature+':\n pass').body[0]
        return ast.dump(n.args,include_attributes=False)+'|'+(ast.dump(n.returns,include_attributes=False) if n.returns else '')
    except SyntaxError:return 'UNPARSEABLE:'+signature
def base_method(name):
    value=str(name).split('(')[0].strip().lstrip('+- ')
    return value.split('.')[-1]
def names(items):return [x.get('name') if isinstance(x,dict) else str(x) for x in items]
def canonical_type(value):
    try:return ast.dump(ast.parse(value,mode='eval').body,include_attributes=False)
    except (SyntaxError,TypeError):return str(value).replace(' ','')
def audit_mapping(inventory,mapping,check):
    schema=inventory['schema']['tables'];expected={(t,c['name']) for t,v in schema.items() for c in v['columns']};primary=[]
    normalize=lambda value:re.sub(r'\s+',' ',value).strip()
    for row in mapping:
        key=(row['table'],row['column'])
        if key not in expected:continue
        if row['mapping_kind'] in ('single-table discriminator','joined projection','computed, not persisted','target gap'):continue
        primary.append(key);column=next(c for c in schema[key[0]]['columns'] if c['name']==key[1]);name='.'.join(key)
        check('mapping_SQL_type',name,row['sql_type']==column['type'],'Actual C0 declared SQL type')
        nonnull=column['not_null'] or (column['primary_key'] and column['type']=='INTEGER')
        check('mapping_nullability',name,row['nullability'].startswith('NO' if nonnull else 'YES'),'Explicit NOT NULL or INTEGER PRIMARY KEY identity; nullable flags stay truthful')
        if column['primary_key']:check('mapping_primary_key',name,'PK' in row['primary_key'],'Actual inline primary key')
        if column['unique']:check('mapping_unique',name,'UNIQUE' in row['unique'],'Actual inline unique constraint')
        for table,target in column['references']:check('mapping_foreign_key',name,table+'.'+target in row['foreign_key'],'Actual FK target')
        for expression in column['checks']:check('mapping_CHECK',name+':'+expression,normalize(expression) in normalize(row['check']),'Actual inline CHECK represented verbatim in mapping')
    counts=collections.Counter(primary)
    check('mapping_column_coverage','schema columns',set(primary)==expected and all(n==1 for n in counts.values()),f'{len(primary)} primary mappings / {len(expected)} actual columns; each exactly once')
    for table,definition in schema.items():
        text=normalize(' '.join(row['check'] for row in mapping if row['table']==table))
        for expression in definition['checks']:check('mapping_table_CHECK',table+':'+expression,normalize(expression) in text,'All table-level and inline CHECK constraints are retained')
def audit_erd(inventory,path,data,meta,check):
    schema=inventory['schema'];native=[]
    for cell in ET.parse(path.with_suffix('.drawio')).findall('.//mxCell'):
        geometry=cell.find('mxGeometry')
        if geometry is not None and cell.get('value'):
            native.append((html.unescape(re.sub(r'<[^>]+>','',cell.get('value'))).strip(),float(geometry.get('x','0')),float(geometry.get('y','0'))))
    for relation in meta.get('dependencies',[]):
        child,parent,column=relation['source'],relation['target'],relation['column'];key=path.name+':'+child+'.'+column
        table=schema['tables'].get(child,{})
        field=next((c for c in table.get('columns',[]) if c['name']==column),None)
        check('ERD_actual_FK',key,bool(field and (parent,'id') in {tuple(r) for r in field['references']}),'Diagram relationship is an actual committed FK; normalize Python tuples and serialized JSON lists')
        if not field:continue
        unique=field['unique'] or field['primary_key'] or any(re.fullmatch(r'(?:UNIQUE|PRIMARY\s+KEY)\s*\(\s*'+re.escape(column)+r'\s*\)',c,re.I) for c in table['constraints'])
        unique=unique or any(i['unique'] and i['table']==child and not re.search(r'\bWHERE\b',i['definition'],re.I) and re.search(r'\(\s*'+re.escape(column)+r'\s*\)',i['definition']) for i in schema['indexes'])
        child_to_parent='1' if field['not_null'] else '0..1';parent_to_child='0..1' if unique else '0..*'
        check('ERD_multiplicity_metadata',key,relation['child_to_parent']==child_to_parent and relation['parent_to_child']==parent_to_child,'FK nullability and unconditional single-column uniqueness; partial uniqueness is not a global maximum')
        edge=next((e for e in data.get('edges',[]) if e['id']=='fk_'+child+'_'+column),{})
        ends=edge.get('ends',[])
        check('ERD_drawn_end_multiplicity',key,len(ends)==2 and [v[0] for v in ends]==[parent_to_child,child_to_parent],'UML label at child end counts children per parent; label at parent end counts parents per child')
        nodes={n['id']:n for n in data.get('nodes',[])};points=edge.get('points',[])
        for side,point in [('source',points[0] if points else None),('target',points[-1] if points else None)]:
            node=nodes.get(edge.get(side),{});attached=False
            if node and point:
                x,y,w,h=(float(node[n]) for n in ('x','y','w','h'));px,py=point
                attached=x-.5<=px<=x+w+.5 and y-.5<=py<=y+h+.5 and min(abs(px-x),abs(px-x-w),abs(py-y),abs(py-y-h))<=.5
            check('ERD_edge_boundary_attachment',key+':'+side,attached,'The actual polyline endpoint touches its table rectangle; an ID link alone does not prove visual attachment')
        for label,x,y in ends:
            check('ERD_native_end_label',key+':'+str((label,x,y)),(label,float(x),float(y)) in native,'Editable source actually contains the matching label at the declared relation-end position')
def import_graph(inv):
    available={p[:-3].replace('/','.') for p in inv['modules']};result=[]
    def layer(path):
        path=path+'.'
        if '.presentation.' in path:return 'view'
        if '.business.controllers.' in path:return 'controller'
        if '.business.domain.' in path:return 'domain'
        if '.data_access.' in path:return 'data_access'
        return 'composition'
    for path,m in inv['modules'].items():
        source=path[:-3].replace('/','.');parts=source.split('.')[:-1]
        for imp in m['imports']:
            if imp['level']:
                prefix=parts[:len(parts)-imp['level']+1];target='.'.join(prefix+([imp['module']] if imp['module'] else []))
            else:target=imp['module']
            if imp['name'] and target+'.'+imp['name'] in available:target+='.'+imp['name']
            if not target.startswith('saigonbite'):continue
            a,b=layer(source),layer(target)
            allowed=a=='composition' or a==b or (a,b) in {('view','controller'),('controller','domain'),('controller','data_access')}
            result.append({'source':source,'target':target,'imported_name':imp['name'],'line':imp['line'],'source_layer':a,'target_layer':b,'allowed':allowed})
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument('--commit');p.add_argument('--read-only',action='store_true');p.add_argument('--allow-incomplete',action='store_true');args=p.parse_args()
    model=read(R/'models/shared/design_model.json');annotations=read(D/'design_annotations.json');commit=git('rev-parse',args.commit or model['C0'])
    spec=importlib.util.spec_from_file_location('p3_inventory_static',Path(__file__).with_name('p3_code_inventory.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);inventory=module.inventory(commit)
    actual={};modules={}
    for path,m in inventory['modules'].items():
        for c in m['classes']:actual[c['name']]=c
        modules[path]=m
    def actual_class(cls):
        c=model['classes'].get(cls)
        if not c:return None
        if c.get('source_kind')=='class':return actual.get(cls)
        m=modules.get(c['module']);return {'attributes':[],'methods':m['functions'],'bases':[]} if m else None
    def get_method(c,name):
        if c is None:return None
        found=next((m for m in c.get('methods',[]) if m['name']==name),None)
        if found:return found
        for base in c.get('bases',[]):
            result=get_method(actual.get(base),name)
            if result:return result
        return None
    checks=[]
    def check(category,key,ok,detail='',classification=None):checks.append({'category':category,'key':key,'result':'PASS' if ok else 'FAIL','classification':classification,'detail':detail})
    dependency_keys=[(e['source'],e['target'],e['kind']) for e in model['dependencies']]
    check('shared_dependency_uniqueness','sole model',len(dependency_keys)==len(set(dependency_keys)),'One record per source/target/kind; unresolved targets retain their stricter status')
    def element(cls,member=None,kind='method'):
        c=model['classes'].get(cls)
        if not c:check('model_element',cls,False,'Class/module role absent from sole shared model');return None
        if member is None:
            check('class',cls,actual_class(cls) is not None or c['status'] in ('P4-TARGET','GAP'),'Code class or explicitly declared target',c['status']);return c
        bucket=c['attributes'] if kind=='attribute' else c['methods'];item=next((m for m in bucket if m['name']==member),None)
        if item is None:
            # Inherited methods retain the original receiver superclass evidence.
            for base in c.get('bases',[]):
                item=next((m for m in model['classes'].get(base,{}).get('methods',[]) if m['name']==member),None)
                if item:break
        if item is None:check('model_member',cls+'.'+member,False,'Member absent from shared model');return None
        code=actual_class(cls);found=next((a for a in (code or {}).get('attributes',[]) if a['name']==member),None) if kind=='attribute' else get_method(code,member)
        status=item.get('status','MATCH');target=next((x for x in annotations.get('elements',{}).get(cls,[]) if x['name']==member and x.get('kind','method')==kind),None)
        if status=='MATCH':
            ok=found is not None
            if ok and kind=='method':ok=canonical(item['signature'])==canonical(found['signature'])
            if ok and kind=='attribute' and item.get('annotated'):ok=item['type']==found['type']
            check(kind,cls+'.'+member,ok,'Same committed signature/type' if ok else 'MATCH does not correspond to committed code',status)
        else:
            check(kind,cls+'.'+member,bool(target and target.get('P4_input') and target.get('reason')),'Declared target: '+str(item.get('P4_input'))+'; '+str(item.get('reason')),status)
        return item
    # Always audit the whole shared model, not only the currently drawn subset.
    for cls,c in model['classes'].items():
        element(cls)
        if c.get('stereotype')=='enumeration':check('enum_values',cls,c.get('enum_members')==(actual_class(cls) or {}).get('enum_members'),'Same enum names and persisted values at the audited commit')
        if c.get('layer')=='domain':
            references=' '.join([a.get('type','') for a in c['attributes']]+[m.get('signature','') for m in c['methods']])
            outer=sorted({name for name in re.findall(r'\b[A-Za-z_]\w*\b',references) if name in model['classes'] and model['classes'][name]['layer']!='domain'})
            check('domain_type_purity',cls,not outer,'Domain type declarations must not depend on controller/view/data-access types: '+str(outer))
        for attr in c['attributes']:element(cls,attr['name'],'attribute')
        for method in c['methods']:element(cls,method['name'])
    audit_mapping(inventory,csvread(D/'class_table_mapping.csv'),check)
    diagrams=[];unrecognized=[]
    pattern=re.compile(r'^(dcd_|seq_|seqdao_|package_diagram|erd_schema_v2)')
    for path in sorted((R/'models').rglob('*.json')):
        if not pattern.match(path.stem):continue
        data=read(path);meta=data.get('phase3')
        if not meta:unrecognized.append(str(path.relative_to(R)));continue
        if not isinstance(meta,dict):check('metadata',str(path),False,'phase3 must be an object');continue
        diagrams.append((path,data,meta))
        kind=meta.get('diagram_type');key=path.relative_to(R).as_posix()
        check('diagram_type',key,kind in ('dcd','sequence','dao_sequence','package','erd'),'Known Phase3 diagram role; no unclassified figure is silently accepted')
        if kind=='erd':audit_erd(inventory,path,data,meta,check)
        for ext in ('.py','.drawio','.png','.svg'):check('artifact',key+ext,path.with_suffix(ext).is_file(),'Required generator/source/export')
        if path.with_suffix('.drawio').exists():
            try:
                xml=ET.parse(path.with_suffix('.drawio'));cells=xml.findall('.//mxCell');ids={c.get('id') for c in cells}
                edges=[c for c in cells if c.get('edge')=='1'];bad=[c.get('id') for c in edges if c.get('source') not in ids or c.get('target') not in ids]
                check('drawio_endpoints',key,not bad,str(bad));check('drawio_author',key,'722I0004' in path.with_suffix('.drawio').read_text(encoding='utf-8'),'Author in editable source')
            except Exception as e:check('drawio_parse',key,False,str(e))
        if path.with_suffix('.svg').exists():
            try:
                svg=ET.parse(path.with_suffix('.svg'));sizes=[float(x) for x in re.findall(r'font-size=["\']([\d.]+)',path.with_suffix('.svg').read_text(encoding='utf-8'))];width=float(svg.getroot().get('viewBox','0 0 0 0').split()[2]);width=width or float(svg.getroot().get('width','0').replace('px',''));placed=data.get('placed_width_mm',data.get('canvas',{}).get('placed_width_mm',data.get('qa',{}).get('placed_width_mm',170 if data.get('type') in ('sequence','seq') else 230)));pt=min(sizes)*float(placed)*72/(width*25.4) if sizes and width else 0
                check('legibility',key,pt>=8.999,f'minimum {pt:.3f} pt at {placed} mm')
                native=[]
                if path.with_suffix('.drawio').exists():
                    for cell in ET.parse(path.with_suffix('.drawio')).findall('.//mxCell'):
                        if not cell.get('value','').strip():continue
                        style=dict(part.split('=',1) for part in cell.get('style','').split(';') if '=' in part)
                        if 'fontSize' in style:native.append(float(style['fontSize']))
                    native_pt=min(native)*float(placed)*72/(width*25.4) if native else 0
                    check('native_font_declaration',key,native_pt>=8.999,f'editable XML minimum {native_pt:.3f} pt; native application opening remains untested')
            except Exception as e:check('svg_parse',key,False,str(e))
        for e in meta.get('elements',[]):
            if kind=='package':
                check('package_container',key+':'+e.get('class',''),not e.get('methods'),'Package contents/notes are not invented project classes with methods');continue
            if kind=='erd':
                match=re.search(r'\((?:reference )?table\s+(\w+)\)',e.get('class',''))
                if match:
                    table=match[1];check('ERD_table',key+':'+table,table in inventory['schema']['tables'],'Actual SQL table')
                    columns={c['name'] for c in inventory['schema']['tables'].get(table,{}).get('columns',[])}
                    for column in names(e.get('attributes',[])):check('ERD_column',key+':'+table+'.'+column,column in columns,'Actual C0 column; absent targets belong in explicitly marked notes/mapping')
                else:check('ERD_note',key+':'+e.get('class',''),not e.get('methods'),'Explicit schema/continuation note, not a project class')
                continue
            cls=e.get('class');element(cls)
            for a in names(e.get('attributes',[])):
                element(cls,a,'attribute')
                if kind=='dcd' and model['classes'].get(cls,{}).get('layer')=='domain':check('domain_DCD_attribute',key+':'+str(cls)+'.'+str(a),not str(a).endswith('_id'),'Domain DCD uses associations instead of scalar foreign-key attributes; identity id is allowed')
            for m in names(e.get('methods',[])):element(cls,base_method(m))
            # Some view formats retain full declarations, while others resolve
            # names dynamically from the model when rendering. Audit retained
            # snapshots too: member-name existence alone misses stale types.
            for attr,declared in e.get('attribute_types',{}).items():
                item=element(cls,attr,'attribute')
                check('figure_attribute_type',key+':'+cls+'.'+attr,bool(item and canonical_type(declared)==canonical_type(item['type'])),'Figure snapshot type agrees with sole model')
            for method,declared in e.get('method_signatures',{}).items():
                item=element(cls,base_method(method))
                check('figure_method_signature',key+':'+cls+'.'+method,bool(item and canonical(declared)==canonical(item['signature'])),'Full parameter/default/return declaration agrees with sole model')
        for dep in meta.get('dependencies',[]):
            source=dep.get('source');target=dep.get('target')
            if kind=='package':
                allowed={("presentation","controllers"),("controllers","domain"),("controllers","data_access")}
                check('package_dependency_allowed',key+':'+str(source)+'->'+str(target),(source,target) in allowed,'Only the three declared target package dependencies are permitted')
                continue
            if kind=='erd':continue
            # Metadata uses class identities, never invented duplicate classes.
            check('dependency_classes',key+':'+str(source)+'->'+str(target),source in model['classes'] and target in model['classes'],'Both endpoints in shared model')
            relations=model['associations']+model['dependencies'];exists=any(x['source']==source and x['target']==target for x in relations) or any(x['source']==target and x['target']==source and x['kind']!='dependency' for x in relations)
            check('dependency_model',key+':'+str(source)+'->'+str(target),exists,'Association/navigation/dependency in the sole model')
            if dep.get('kind')=='dependency' and source in model['classes'] and target in model['classes']:
                rank={'view':0,'controller':1,'domain':2,'data_access':3};sl=model['classes'][source]['layer'];tl=model['classes'][target]['layer'];check('dependency_allowed',key+':'+source+'->'+target,rank[tl]>=rank[sl] and (sl!='domain' or tl=='domain'),'Layered DCD depicts only allowed dependency directions; actual forbidden imports belong in the package audit')
        for state in meta.get('states',[]):
            cls=state.get('class');attr=state.get('attribute','state');values=state.get('values',[])
            state_map={'Order':('OrderState','orders'),'Payment':('PaymentState','payment'),'Delivery':('DeliveryState','delivery'),'ReplacementOffer':('OfferState','replacement_offer')}
            if cls in state_map:
                enum,table=state_map[cls];valid={m['value'] for m in actual.get(enum,{}).get('enum_members',[])};sql=' '.join(inventory['schema']['tables'][table]['checks']);sqlvalues=set(re.findall(r"'([^']+)'",sql))
                check('persisted_state',key+':'+cls,set(values)<=valid and set(values)<=sqlvalues,'Enum and SQL CHECK: '+str(values))
            elif attr in ('archived_at','is_active','is_available'):
                check('lifecycle_representation',key+':'+cls+'.'+attr,any(a['name']==attr for a in (actual_class(cls) or {}).get('attributes',[])),'Real flag/null representation; no artificial enum')
            elif cls=='HubStatus' and attr in ('busy','quiet','load_percent'):
                check('derived_representation',key+':'+cls+'.'+attr,get_method(actual.get(cls),attr) is not None,'Derived property, not a persisted state or artificial enum')
            elif cls in ('OrderState','PaymentState','DeliveryState','OfferState'):
                owner=next(name for name,pair in state_map.items() if pair[0]==cls);table=state_map[owner][1];valid={m['value'] for m in actual[cls]['enum_members']};sqlvalues=set(re.findall(r"'([^']+)'",' '.join(inventory['schema']['tables'][table]['checks'])))
                check('persisted_enum',key+':'+cls,set(values)<=valid and set(values)<=sqlvalues,'Displayed persisted enum values must also occur in SQL CHECK')
            else:
                check('state_representation',key+':'+str(cls)+'.'+str(attr),False,'Unresolved state representation; declare the actual enum/CHECK, nullable archive flag, boolean flag or derived property')
    check('phase3_metadata','all diagram sources',not unrecognized,'Missing normalized metadata: '+str(unrecognized))
    membership=csvread(R/'docs/part2/ssd_flow_membership.csv');operations={o['op_id']:o for o in csvread(R/'docs/part2/ssd_operations.csv')};realisation=csvread(D/'operation_realisation.csv')
    native_ids={}
    for row in membership:
        source,node=row['SSD message'].split('#',1)
        if source not in native_ids:
            path=R/source;native_ids[source]={c.get('id') for c in ET.parse(path).findall('.//mxCell')} if path.is_file() else set()
        check('frozen_SSD_native_pointer',row['SSD message'],node in native_ids[source],'Ledger points to a real immutable SSD node/edge')
    check('responsibility_coverage','41 frozen SSD occurrences',len(realisation)==len(membership)==41,f'{len(realisation)} rows / {len(membership)} ledger occurrences')
    seqs=[(p,d,m) for p,d,m in diagrams if m.get('diagram_type')=='sequence'];dao=[(p,d,m) for p,d,m in diagrams if m.get('diagram_type')=='dao_sequence'];finals=collections.defaultdict(lambda:collections.defaultdict(set))
    for path,data,meta in diagrams:
        if meta.get('diagram_type')=='dcd' and ('_final' in path.stem or meta.get('final')):
            uc=meta.get('UC');match=re.search(r'uc(\d\d)',path.stem)
            if not uc and match:uc='UC-'+match[1]
            if path.stem.startswith('dcd_subsystem'):continue
            check('final_DCD_identity',path.name,uc in {f'UC-{n:02}' for n in range(1,7)},'A per-UC final DCD identifies one main UC')
            if not uc:continue
            for e in meta.get('elements',[]):finals[uc][e['class']].update(base_method(m) for m in names(e.get('methods',[])))
    covered=set();consistency=[]
    def visible_final_method(uc,cls,method,seen=None):
        seen=set() if seen is None else seen
        if cls in seen:return False
        seen.add(cls)
        if method in finals[uc].get(cls,set()):return True
        return any(base in finals[uc] and visible_final_method(uc,base,method,seen) for base in model['classes'].get(cls,{}).get('bases',[]))
    for path,data,meta in seqs+dao:
        key=path.relative_to(R).as_posix();oid=meta.get('op_id');op=operations.get(oid);uc=meta.get('UC');source=meta.get('ssd_occurrence');is_dao=meta.get('diagram_type')=='dao_sequence'
        check('ssd_identity',key,bool(op and op['operation']==meta.get('operation') and op['parameters']==meta.get('parameters')),'Exact operation name and parameter string from immutable catalogue')
        match=[m for m in membership if m['UC']==uc and m['catalogue_id']==oid and m['SSD message']==source]
        check('ssd_occurrence',key,bool(match),'Exact frozen ledger pointer: '+str(source))
        if not is_dao and match:covered.add(source)
        lifelines={l['id']:l for l in meta.get('lifelines',[])}
        for line in lifelines.values():
            cls=line.get('class');role=line.get('role')
            if role in ('actor','database') or cls in ('Database',':Database',None):continue
            element(cls)
            if not is_dao:check('design_layers',key+':'+line['id'],model['classes'].get(cls,{}).get('layer')!='data_access' or cls in ('PaymentGatewaySimulator','Authorisation'),'No DAO in report III design sequence')
        for message in meta.get('messages',[]):
            mkind=message.get('kind','call');target=lifelines.get(message.get('to'));source_line=lifelines.get(message.get('from'))
            check('message_kind',key+':'+str(message.get('method')),mkind in ('call','return','ssd','create','note'),'Explicit UML message role; unknown roles do not bypass receiver checks')
            if mkind=='note':continue
            check('message_endpoints',key+':'+str(message.get('method')),target is not None and source_line is not None,'Connected lifelines')
            if mkind in ('return','ssd') or not target:continue
            cls=target.get('class');method=base_method(message.get('method',''))
            if target.get('role')=='database' or cls in ('Database',':Database'):continue
            if source_line:
                origin=model['classes'].get(source_line.get('class'),{});receiver=model['classes'].get(cls,{})
                rank={'view':0,'controller':1,'domain':2,'data_access':3}
                if origin.get('layer') in rank and receiver.get('layer') in rank:
                    allowed=rank[receiver['layer']]>=rank[origin['layer']] and (origin['layer']!='domain' or receiver['layer']=='domain') and not (origin['layer']=='view' and receiver['layer'] in ('domain','data_access'))
                    check('message_layer_direction',key+':'+str(source_line.get('class'))+'->'+str(cls)+'.'+method,allowed,'Requests go through controller; domain has no outward application calls')
            if mkind=='create':
                code=actual_class(cls);check('constructor',key+':'+str(cls),bool(code and (any('dataclass' in d for d in code.get('decorators',[])) or get_method(code,'__init__'))),'Existing dataclass or explicit constructor');continue
            element(cls,method)
            if not is_dao:check('sequence_final_DCD',key+':'+cls+'.'+method,visible_final_method(uc,cls,method),'Every message is declared on its receiver or a visibly drawn superclass in the UC final DCD')
        if is_dao:
            # Transaction guarantees must be visible, not hidden only in JSON.
            text=path.with_suffix('.svg').read_text(encoding='utf-8')
            if op and op['operation']=='salesReport':check('read_only_sequence',key,('UC04-MG01' in text and 'read' in text.lower()),'Read-only report guard explicitly visible')
            else:
                for token in ('BEGIN IMMEDIATE','COMMIT','ROLLBACK','rowcount'):
                    check('dao_transaction',key+':'+token,token.lower() in text.lower(),'Required transaction/conditional save notation')
                check('dao_busy_outcome',key,'busy' in text.lower() and 'retry' in text.lower(),'Visible busy/retry outcome; rollback/atomicity checked separately')
    if not args.allow_incomplete:
        for m in membership:check('SSD_sequence_coverage',m['SSD message'],m['SSD message'] in covered,m['UC']+' '+m['operation'])
        for uc in range(1,7):check('final_DCD',f'UC-{uc:02}',bool(finals[f'UC-{uc:02}']),'Final design class views exist')
        required={'UC-01':['confirmCheckout'],'UC-02':['takeDelivery','confirmDelivered'],'UC-03':['archiveHub'],'UC-04':['salesReport'],'UC-05':['rejectOrder','acceptReplacement'],'UC-06':['updateMenuItem']}
        for uc,opnames in required.items():
            for operation in opnames:check('DAO_sequence_coverage',uc+':'+operation,any(m.get('UC')==uc and m.get('operation')==operation for _,_,m in dao),'Required risk-focused DAO sequence')
    for member,row in zip(membership,realisation):
        ok=row['UC']==member['UC'] and row['op_id']==member['catalogue_id'] and row['operation']==member['operation'];check('responsibility_identity',member['SSD message'],ok,'Same ledger occurrence order and catalogue ID')
        target=row['status'] in ('P4-TARGET','GAP');check('responsibility_status',member['SSD message'],row['status'] in ('MATCH','P4-TARGET','GAP') and (not target or bool(row['P4 input'])),'Every target has its P4 input',row['status'])
        if row['transaction (none | read | BEGIN IMMEDIATE)']=='BEGIN IMMEDIATE':check('mutation_effect_label',member['SSD message'],'no persistent effect' not in row['PC/MG ensured'].lower(),'A supporting mutation must cite its own contract, never a no-effect query label')
        sequence=[p.relative_to(R).as_posix().replace('.json','.drawio') for p,_,m in seqs if m.get('ssd_occurrence')==member['SSD message']]
        daosequence=[p.relative_to(R).as_posix().replace('.json','.drawio') for p,_,m in dao if m.get('UC')==member['UC'] and m.get('op_id')==member['catalogue_id']]
        consistency.append({'UC':member['UC'],'SSD op':member['operation']+' / '+member['catalogue_id']+' / '+member['SSD message'],'design sequence':'; '.join(sequence),'view function':row['view function (blueprint.function, METHOD /rule)'],'controller method':row['controller.method(signature)'],'domain methods':row['domain calls'],'DAO methods (4.3.2)':('; '.join(daosequence)+' : '+row['DAO calls']) if daosequence else 'Not expanded here; responsibility table: '+row['DAO calls'],'transaction':row['transaction (none | read | BEGIN IMMEDIATE)'],'PC/MG ensured':row['PC/MG ensured'],'status':row['status']})
    anchors=csvread(R/'docs/part2/pc_mg_register.csv')
    for a in anchors:
        enforcing=[r for r in realisation if r['UC']==a['UC'] and a['id'] in r['PC/MG ensured']]
        check('PC_MG_realisation',a['id'],bool(enforcing) and all(r['controller.method(signature)'] and r['transaction (none | read | BEGIN IMMEDIATE)'] for r in enforcing),'Named method + transaction: '+'; '.join(r['controller.method(signature)'].split('(')[0]+' / '+r['transaction (none | read | BEGIN IMMEDIATE)'] for r in enforcing))
    # Representations are audited even when a figure has no state text.
    for cls,attr,table,column in [('Hub','archived_at','hub','archived_at'),('Brand','archived_at','brand','archived_at'),('MenuItem','archived_at','menu_item','archived_at'),('UserAccount','is_active','user_account','is_active'),('HubMenuItem','is_available','hub_menu_item','is_available')]:
        check('real_representation',cls+'.'+attr,any(a['name']==attr for a in actual[cls]['attributes']) and any(c['name']==column for c in inventory['schema']['tables'][table]['columns']),table+'.'+column)
    check('derived_classification','BUSY/QUIET',all(n not in actual for n in ('HubState','BusyState','QuietState')) and get_method(actual.get('HubStatus'),'busy') is not None and get_method(actual.get('HubStatus'),'quiet') is not None,'HubStatus properties; archive is a nullable timestamp')
    for enum,table in [('OrderState','orders'),('PaymentState','payment'),('DeliveryState','delivery'),('OfferState','replacement_offer')]:
        values={m['value'] for m in actual[enum]['enum_members']};sqlvalues=set(re.findall(r"'([^']+)'",' '.join(inventory['schema']['tables'][table]['checks'])))
        check('enum_SQL_CHECK',enum,values<=sqlvalues,'Every persisted lifecycle value is admitted by the actual schema CHECK')
    imports=import_graph(inventory);violations=[i for i in imports if not i['allowed']];listed=annotations.get('import_violations',[])
    for violation in violations:
        accounted=any(x.get('source')==violation['source'] and x.get('target')==violation['target'] for x in listed)
        check('actual_import_accounted',violation['source']+':'+str(violation['line'])+'->'+violation['target'],accounted,'Actual forbidden direction must be listed, not drawn as allowed','P4-TARGET' if accounted else None)
    failures=[c for c in checks if c['result']=='FAIL'];summary={'author':model['author'],'C0':model['C0'],'audited_commit':commit,'evidence_label':'Static','app_executed':False,'read_only':args.read_only,'incomplete_mode':args.allow_incomplete,'figure_files':len(diagrams),'design_sequence_views':len(seqs),'DAO_sequence_views':len(dao),'SSD_occurrences_covered':len(covered),'anchor_count':len(anchors),'checks':len(checks),'failures':len(failures),'pass':not failures,'status_counts':dict(collections.Counter(r['status'] for r in realisation)),'import_violations':violations,'results':checks}
    if not args.read_only:
        N.mkdir(parents=True,exist_ok=True);(N/f'design_crosscheck_{commit[:7]}.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
        with (D/'design_consistency.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(consistency[0]));w.writeheader();w.writerows(consistency)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('results','import_violations')},indent=2));print('FAILURES:',json.dumps(failures[:40],indent=2,ensure_ascii=False))
    return 0 if not failures else 1
if __name__=='__main__':raise SystemExit(main())
