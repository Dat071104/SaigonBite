"""Inventory a committed application using AST and SQL text parsing only.
Author: 722I0004 · AI-assisted (Codex).
Usage: python -I p3_code_inventory.py <commit> [--output path]
No application imports, database connections, or application execution.
"""
from pathlib import Path
import argparse, ast, hashlib, json, re, subprocess

REPO=Path(__file__).resolve().parents[3]
AUTHOR='722I0004 · AI-assisted (Codex)'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def visibility(name):return '-' if name.startswith('_') else '+'
def infer(node):
    if node is None:return 'Any'
    if isinstance(node,ast.Constant):return type(node.value).__name__ if node.value is not None else 'None'
    if isinstance(node,ast.List):return 'list'
    if isinstance(node,ast.Dict):return 'dict'
    if isinstance(node,ast.Tuple):return 'tuple'
    if isinstance(node,ast.Call):return ast.unparse(node.func)
    return 'Any'
def parameters(args):
    result=[];pos=args.posonlyargs+args.args;defaults=[None]*(len(pos)-len(args.defaults))+args.defaults
    for idx,(arg,default) in enumerate(zip(pos,defaults)):
        result.append({'name':arg.arg,'type':ast.unparse(arg.annotation) if arg.annotation else infer(default),'annotated':arg.annotation is not None,'default':ast.unparse(default) if default is not None else None,'kind':'positional_only' if idx<len(args.posonlyargs) else 'positional_or_keyword'})
    if args.vararg:result.append({'name':args.vararg.arg,'type':ast.unparse(args.vararg.annotation) if args.vararg.annotation else 'Any','annotated':args.vararg.annotation is not None,'default':None,'kind':'vararg'})
    for arg,default in zip(args.kwonlyargs,args.kw_defaults):result.append({'name':arg.arg,'type':ast.unparse(arg.annotation) if arg.annotation else infer(default),'annotated':arg.annotation is not None,'default':ast.unparse(default) if default is not None else None,'kind':'keyword_only'})
    if args.kwarg:result.append({'name':args.kwarg.arg,'type':ast.unparse(args.kwarg.annotation) if args.kwarg.annotation else 'Any','annotated':args.kwarg.annotation is not None,'default':None,'kind':'kwarg'})
    return result
def balanced(text,start):
    depth=0;quote=None
    for i in range(start,len(text)):
        ch=text[i]
        if quote:
            if ch==quote:quote=None
            continue
        if ch in "'\"":quote=ch
        elif ch=='(':depth+=1
        elif ch==')':
            depth-=1
            if depth==0:return text[start+1:i],i+1
    raise ValueError('Unbalanced SQL parentheses')
def sql_facts(strings):
    statements=[]
    for value in strings:
        if not re.search(r'\b(SELECT|INSERT\s+INTO|UPDATE|DELETE\s+FROM|BEGIN\s+IMMEDIATE|COMMIT|ROLLBACK)\b',value,re.I):continue
        kinds=sorted(set(re.findall(r'\b(SELECT|INSERT|UPDATE|DELETE|BEGIN|COMMIT|ROLLBACK)\b',value,re.I)))
        tables=sorted(set(re.findall(r'\b(?:FROM|JOIN|INTO|UPDATE)\s+([a-z_][a-z_0-9]*)',value,re.I)))
        statements.append({'kinds':[k.upper() for k in kinds],'tables':tables,'sql':value.strip(),'conditional_state_update':bool(re.search(r'\bUPDATE\b.+\bWHERE\b.+\bstate\s*=',value,re.I|re.S))})
    return statements
def sql_text(node,bindings,seen=None):
    """Resolve literal SQL fragments without evaluating Python or SQL."""
    seen=set() if seen is None else seen
    if isinstance(node,ast.Constant) and isinstance(node.value,str):return node.value
    if isinstance(node,ast.Name) and node.id in bindings and node.id not in seen:return sql_text(bindings[node.id],bindings,seen|{node.id})
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Add):return sql_text(node.left,bindings,seen)+sql_text(node.right,bindings,seen)
    if isinstance(node,ast.JoinedStr):return ''.join(sql_text(v,bindings,seen) if isinstance(v,ast.Constant) else sql_text(v.value,bindings,seen) if isinstance(v,ast.FormattedValue) else '' for v in node.values)
    return '{'+ast.unparse(node)+'}'
def function(node,global_bindings=None):
    params=parameters(node.args);calls=[]
    for child in ast.walk(node):
        if isinstance(child,ast.Call):calls.append({'target':ast.unparse(child.func),'args':[ast.unparse(a) for a in child.args],'keywords':{k.arg or '**':ast.unparse(k.value) for k in child.keywords},'line':child.lineno})
    docstring=ast.get_docstring(node,clean=False)
    strings=[n.value for n in ast.walk(node) if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value!=docstring]
    # Reconstruct f-string SQL as one text statement; separate Constant pieces
    # would otherwise lose FROM/UPDATE tables and conditional state predicates.
    strings += [''.join(v.value if isinstance(v,ast.Constant) and isinstance(v.value,str) else '{'+ast.unparse(v.value)+'}' if isinstance(v,ast.FormattedValue) else '' for v in n.values) for n in ast.walk(node) if isinstance(n,ast.JoinedStr)]
    bindings=dict(global_bindings or {})
    for assign in ast.walk(node):
        if isinstance(assign,(ast.Assign,ast.AnnAssign)):
            for target in assign.targets if isinstance(assign,ast.Assign) else [assign.target]:
                if isinstance(target,ast.Name) and assign.value is not None:bindings[target.id]=assign.value
    sql_strings=[sql_text(n.args[0],bindings) for n in ast.walk(node) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('execute','executemany','executescript') and n.args]
    source=ast.unparse(node)
    returns=ast.unparse(node.returns) if node.returns else 'Any'
    return {'name':node.name,'line':node.lineno,'signature':f'{node.name}({ast.unparse(node.args)})'+(f' -> {ast.unparse(node.returns)}' if node.returns else ''),'parameters':params,'return':returns,'return_annotated':node.returns is not None,'visibility':visibility(node.name),'annotated':all(p['annotated'] for p in params if p['name'] not in ('self','cls')) and node.returns is not None,'decorators':[ast.unparse(n) for n in node.decorator_list],'calls':calls,'sql':sql_facts(sql_strings),'immediate_transaction':any(c['target'].endswith('immediate_transaction') for c in calls),'begin_immediate_literal':any('BEGIN IMMEDIATE' in s.upper() for s in strings),'rowcount_checks':[ast.unparse(n) for n in ast.walk(node) if isinstance(n,ast.Compare) and 'rowcount' in ast.unparse(n)],'body_ast':source}
def schema_inventory(sql):
    clean=re.sub(r'--[^\n]*','',sql);tables={}
    for match in re.finditer(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-z_]+)\s*\(',clean,re.I):
        content,end=balanced(clean,match.end()-1);parts=[];start=0;depth=0;quote=None
        for i,ch in enumerate(content):
            if quote:
                if ch==quote:quote=None
            elif ch in "'\"":quote=ch
            elif ch=='(':depth+=1
            elif ch==')':depth-=1
            elif ch==',' and depth==0:parts.append(content[start:i].strip());start=i+1
        parts.append(content[start:].strip());columns=[];constraints=[]
        for part in parts:
            if re.match(r'(CONSTRAINT|PRIMARY|FOREIGN|UNIQUE|CHECK)\b',part,re.I):constraints.append(part);continue
            field=re.match(r'(\w+)\s+(\w+)',part)
            if not field:continue
            checks=[]
            for check in re.finditer(r'CHECK\s*\(',part,re.I):checks.append(balanced(part,check.end()-1)[0])
            columns.append({'name':field[1],'type':field[2].upper(),'not_null':bool(re.search(r'\bNOT\s+NULL\b',part,re.I)),'primary_key':bool(re.search(r'\bPRIMARY\s+KEY\b',part,re.I)),'unique':bool(re.search(r'\bUNIQUE\b',part,re.I)),'checks':checks,'references':re.findall(r'REFERENCES\s+(\w+)\s*\(([^)]+)\)',part,re.I),'definition':part})
        allchecks=[balanced(content,m.end()-1)[0] for m in re.finditer(r'CHECK\s*\(',content,re.I)]
        tables[match[1]]={'columns':columns,'constraints':constraints,'checks':allchecks,'definition':content}
    return {'tables':tables,'indexes':[{'unique':bool(m[1]),'name':m[2],'table':m[3],'definition':m[0]} for m in re.finditer(r'CREATE\s+(UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s+ON\s+(\w+)[^;]*;',clean,re.I)],'user_version':int(re.search(r'PRAGMA\s+user_version\s*=\s*(\d+)',clean,re.I)[1]),'sha256':hashlib.sha256(sql.encode()).hexdigest()}
def inventory(commit):
    commit=git('rev-parse',commit).decode().strip()
    paths=git('ls-tree','-r','--name-only',commit,'--','saigonbite','db/schema.sql','init_db.py','app.py').decode().splitlines()
    out={'author':AUTHOR,'commit':commit,'evidence_label':'Static','application_imported':False,'modules':{},'schema':{}}
    for path in paths:
        if path=='db/schema.sql':out['schema']=schema_inventory(git('show',f'{commit}:{path}').decode('utf-8-sig'));continue
        if not path.endswith('.py'):continue
        content=git('show',f'{commit}:{path}').decode('utf-8-sig');tree=ast.parse(content,filename=path);module={'path':path,'sha256':hashlib.sha256(content.encode()).hexdigest(),'imports':[],'classes':[],'functions':[],'blueprints':{},'routes':[],'module_assignments':[]}
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):module['imports'] += [{'module':a.name,'name':None,'alias':a.asname,'level':0,'line':n.lineno} for a in n.names]
            elif isinstance(n,ast.ImportFrom):module['imports'] += [{'module':n.module or '', 'name':a.name,'alias':a.asname,'level':n.level,'line':n.lineno} for a in n.names]
        global_bindings={}
        for assign in tree.body:
            if isinstance(assign,(ast.Assign,ast.AnnAssign)):
                for target in assign.targets if isinstance(assign,ast.Assign) else [assign.target]:
                    if isinstance(target,ast.Name) and assign.value is not None:global_bindings[target.id]=assign.value
        for node in tree.body:
            if isinstance(node,(ast.Assign,ast.AnnAssign)):
                for target in node.targets if isinstance(node,ast.Assign) else [node.target]:
                    if isinstance(target,ast.Name):module['module_assignments'].append({'name':target.id,'value_ast':ast.unparse(node.value) if node.value else None,'annotation':ast.unparse(node.annotation) if isinstance(node,ast.AnnAssign) else None,'line':node.lineno})
            if isinstance(node,ast.Assign) and isinstance(node.value,ast.Call) and ast.unparse(node.value.func).endswith('Blueprint'):
                kw={k.arg:ast.literal_eval(k.value) for k in node.value.keywords if isinstance(k.value,ast.Constant)}
                for target in node.targets:
                    if isinstance(target,ast.Name):module['blueprints'][target.id]={'name':ast.literal_eval(node.value.args[0]),'url_prefix':kw.get('url_prefix','')}
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
                f=function(node,global_bindings);module['functions'].append(f)
                for d in node.decorator_list:
                    if isinstance(d,ast.Call) and isinstance(d.func,ast.Attribute) and d.func.attr in ('route','get','post'):
                        bp=module['blueprints'].get(ast.unparse(d.func.value),{});kw={k.arg:ast.literal_eval(k.value) for k in d.keywords if isinstance(k.value,(ast.List,ast.Constant,ast.Tuple))};rule=ast.literal_eval(d.args[0])
                        module['routes'].append({'blueprint_variable':ast.unparse(d.func.value),'blueprint':bp.get('name',ast.unparse(d.func.value)),'rule':bp.get('url_prefix','')+rule,'declared_rule':rule,'methods':kw.get('methods',[d.func.attr.upper()] if d.func.attr!='route' else ['GET']),'view_function':node.name,'signature':f['signature'],'decorators':f['decorators']})
            if not isinstance(node,ast.ClassDef):continue
            attrs={};methods=[];enums=[]
            for child in node.body:
                if isinstance(child,ast.AnnAssign) and isinstance(child.target,ast.Name):attrs[child.target.id]={'name':child.target.id,'type':ast.unparse(child.annotation),'annotated':True,'visibility':visibility(child.target.id),'default':ast.unparse(child.value) if child.value else None}
                elif isinstance(child,ast.Assign):
                    for target in child.targets:
                        if isinstance(target,ast.Name):
                            attrs[target.id]={'name':target.id,'type':infer(child.value),'annotated':False,'visibility':visibility(target.id),'default':ast.unparse(child.value)}
                            if any('Enum' in ast.unparse(b) for b in node.bases):enums.append({'name':target.id,'value':ast.literal_eval(child.value) if isinstance(child.value,ast.Constant) else ast.unparse(child.value)})
                elif isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef)):
                    f=function(child,global_bindings);methods.append(f)
                    if child.name=='__init__':
                        types={p['name']:p for p in f['parameters']}
                        for assign in ast.walk(child):
                            if isinstance(assign,(ast.Assign,ast.AnnAssign)):
                                for target in assign.targets if isinstance(assign,ast.Assign) else [assign.target]:
                                    if isinstance(target,ast.Attribute) and isinstance(target.value,ast.Name) and target.value.id=='self':
                                        hint=types.get(assign.value.id,{}) if isinstance(assign.value,ast.Name) else {};ann=ast.unparse(assign.annotation) if isinstance(assign,ast.AnnAssign) else None
                                        attrs[target.attr]={'name':target.attr,'type':ann or hint.get('type',infer(assign.value)),'annotated':bool(ann) or hint.get('annotated',False),'visibility':visibility(target.attr),'default':None}
            module['classes'].append({'name':node.name,'line':node.lineno,'bases':[ast.unparse(b) for b in node.bases],'decorators':[ast.unparse(d) for d in node.decorator_list],'attributes':list(attrs.values()),'methods':methods,'enum_members':enums,'visibility':visibility(node.name)})
        out['modules'][path]=module
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument('commit');p.add_argument('--output',type=Path,default=REPO/'docs/part2/design/code_inventory.json');a=p.parse_args();data=inventory(a.commit);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps({'commit':data['commit'],'modules':len(data['modules']),'classes':sum(len(m['classes']) for m in data['modules'].values()),'routes':sum(len(m['routes']) for m in data['modules'].values()),'schema_tables':len(data['schema']['tables']),'output':str(a.output)}))
if __name__=='__main__':main()
