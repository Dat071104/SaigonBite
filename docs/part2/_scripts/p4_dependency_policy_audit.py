"""Nonwriting bounded AST policy audit. No application/fixture imports or execution.
Author: 722I0004 · AI-assisted (Codex).
Structural rules plus exact reviewed semantic AST seals, NOT a Python proof engine.
"""
from pathlib import Path
import argparse, ast, hashlib, json, subprocess, sys
sys.dont_write_bytecode = True

R = Path(__file__).resolve().parents[3]
P = R / 'docs/part2/implementation/architecture_amendment'


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def semantic(tree):
    # Python 3.13 omits empty optional AST fields in repr; canonicalize explicitly
    # so the bundled 3.12 checker runtime and project 3.13 agree on source meaning.
    def normal(node):
        if isinstance(node,ast.AST):
            return [type(node).__name__, {k:normal(v) for k,v in ast.iter_fields(node) if v is not None and v != []}]
        if isinstance(node,list): return [normal(v) for v in node]
        if isinstance(node,bytes): return {'bytes':node.hex()}
        if isinstance(node,complex): return {'complex':str(node)}
        if node is Ellipsis: return {'constant':'Ellipsis'}
        return node
    return digest(json.dumps(normal(tree),sort_keys=True))


def sources(root=R):
    result = {}
    for path in sorted((root / 'saigonbite').rglob('*.py')):
        name = path.relative_to(root).with_suffix('').as_posix().replace('/', '.')
        result[name.removesuffix('.__init__')] = path.read_text(encoding='utf-8-sig')
    # The executable bootstrap is also part of the graph.
    if (root / 'app.py').is_file(): result['app'] = (root / 'app.py').read_text(encoding='utf-8-sig')
    return result


def role(module):
    for prefix, value in [('saigonbite.business.domain','domain'), ('saigonbite.business.controllers','controller'), ('saigonbite.data_access','dao'), ('saigonbite.presentation','view')]:
        if module == prefix or module.startswith(prefix + '.'): return value
    return 'root' if module in ('saigonbite', 'app') else 'other'


def base_for(module, node, packages):
    if not node.level: return node.module or ''
    parts = (module if module in packages else module.rsplit('.', 1)[0]).split('.')
    if node.level > len(parts): raise ValueError('relative import escapes package')
    return '.'.join(parts[:len(parts)-node.level+1] + ([node.module] if node.module else []))


def parse_graph(code, packages=None):
    packages = packages or {m for m in code if any(n.startswith(m+'.') for n in code)}
    trees, records, errors, exports = {}, [], [], {}
    for module, text in code.items():
        try: trees[module] = ast.parse(text)
        except SyntaxError as e: errors.append(f'{module}:unparseable:{e}'); continue
        exports[module] = {}
        for node in ast.walk(trees[module]):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                exports[module].setdefault(node.name, []).append((module, node.name))
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                for target in (node.targets if isinstance(node, ast.Assign) else [node.target]):
                    if isinstance(target, ast.Name): exports[module].setdefault(target.id, []).append((module, target.id))
            if not isinstance(node, (ast.Import, ast.ImportFrom)): continue
            try: base = base_for(module, node, packages) if isinstance(node, ast.ImportFrom) else ''
            except ValueError as e: errors.append(f'{module}:{e}'); continue
            for alias in node.names:
                if alias.name == '*': errors.append(f'{module}:{node.lineno}:wildcard'); continue
                target = base if base else alias.name
                symbol = alias.name if base else '<module>'
                if base and base+'.'+alias.name in code: target, symbol = base+'.'+alias.name, '<module>'
                local = alias.asname or (alias.name if base else alias.name.split('.')[0])
                records.append(dict(source=module, target=target, symbol=symbol, binding=local, line=node.lineno))
                exports[module].setdefault(local, []).append((target, symbol))
    return trees, records, errors, exports


def resolve(module, symbol, exports, seen=()):
    if symbol == '<module>': return [(module, symbol)]
    if (module, symbol) in seen: raise ValueError('cyclic re-export')
    bindings = set(exports.get(module, {}).get(symbol, []))
    if len(bindings) != 1: raise ValueError(f'unresolved/ambiguous export {module}.{symbol}')
    target, name = next(iter(bindings))
    if (target, name) == (module, symbol) or not target.startswith('saigonbite'): return [(target, name)]
    return resolve(target, name, exports, seen+((module,symbol),))


def audit(code=None, policy=None, reviewed=None):
    code = sources() if code is None else code
    policy = json.loads((P/'policy.json').read_text()) if policy is None else policy
    reviewed = json.loads((P/'reviewed_scope.json').read_text()) if reviewed is None else reviewed
    trees, records, errors, exports = parse_graph(code)
    allowed = {(x['source'], x['target']): x for x in policy['dependencies']}
    uses, edges, actual = [], set(), {}
    for rec in records:
        src, dst, sym = rec['source'], rec['target'], rec['symbol']
        sr, dr = role(src), role(dst)
        if dst.startswith('saigonbite'):
            if dst not in code: errors.append(f'{src}:unresolved module {dst}')
            else:
                try: rec['effective'] = resolve(dst, sym, exports)
                except ValueError as e: errors.append(f'{src}:{e}')
            edges.add((src,dst))
            if sr != dr and sr != 'root':
                if not ((sr,dr) in {('view','controller'), ('controller','domain'), ('controller','dao')} or (sr=='dao' and dr=='domain' and (src,dst) in allowed)):
                    errors.append(f'{src}:forbidden direction to {dst}')
            if sr == 'root' and (src,dst,sym) not in {tuple(e) for e in reviewed['bootstrap_imports']}:
                errors.append(f'{src}:unreviewed bootstrap import {dst}.{sym}')
            # Resolve re-exports without treating the named controller facade as
            # a new direct view->domain edge. Its exact AST is separately sealed.
            for effective, _ in rec.get('effective', []):
                er = role(effective)
                if sr in ('dao','domain') and er not in (sr, 'domain' if sr=='dao' else sr):
                    errors.append(f'{src}:hidden effective dependency {effective}')
                if sr=='view' and er in ('dao','domain','root'):
                    contract = reviewed['view_contract_exports'].get(dst, [])
                    if sym not in contract: errors.append(f'{src}:unreviewed view facade {dst}.{sym}')
        if sr=='dao' and dr=='domain':
            pair = (src,dst); permit = allowed.get(pair)
            logical = 'rules' if sym=='<module>' and dst.endswith('.rules') else sym
            actual.setdefault(pair,set()).add(logical)
            if not permit or logical not in permit['symbols']: errors.append(f'{src}:unapproved symbol/pair {dst}.{logical}')
            tree = trees[src]
            for node in ast.walk(tree):
                if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Load) and node.id==rec['binding']:
                    uses.append({**rec,'use_line':node.lineno,'expression':ast.unparse(node),'permitted_use':permit['use'] if permit else 'NONE'})
                if logical=='rules' and isinstance(node,ast.Attribute) and isinstance(node.value,ast.Name) and node.value.id==rec['binding']:
                    if not permit or node.attr not in permit.get('members',[]): errors.append(f'{src}:{node.lineno}:unapproved rules member {node.attr}')
    for module,tree in trees.items():
        r=role(module)
        local_imports={x['binding']:x['target']+'.'+x['symbol'] for x in records if x['source']==module}
        for node in ast.walk(tree):
            if isinstance(node,ast.Call):
                name=ast.unparse(node.func)
                resolved=name
                for binding,target in local_imports.items():
                    if name==binding or name.startswith(binding+'.'): resolved=target+name[len(binding):];break
                if any(x in resolved for x in ('__import__','import_module','spec_from','SourceFileLoader')) or name in ('exec','eval','compile'):
                    errors.append(f'{module}:{node.lineno}:dynamic/unresolved construct {name}')
                if r=='domain' and (name in ('open','input','print') or any(resolved.startswith(x) for x in ('sqlite3','requests','socket','subprocess','pathlib','os.'))): errors.append(f'{module}:domain I/O {name}')
                if r=='view' and isinstance(node.func,ast.Attribute) and node.func.attr in ('execute','executemany','executescript'): errors.append(f'{module}:view SQL')
                if r=='dao' and module!='saigonbite.data_access.database' and (name.endswith(('.commit','.rollback','.immediate_transaction')) or name=='immediate_transaction'):
                    errors.append(f'{module}:DAO transaction ownership')
        # Exact semantic review seal also catches local object methods, new decision
        # logic, reflective access, binding shadowing and import-free orchestration.
        # Unknown/new bodies fail closed; no automatic renewal from current bytes.
        expected=reviewed['module_ast'].get(module) or reviewed['facade_ast'].get(module)
        if expected != semantic(tree): errors.append(f'{module}:unreviewed semantic body/use')
    # Role-cycle detection uses actual module edges collapsed only by role.
    role_edges={(role(s),role(t)) for s,t in edges if role(s)!=role(t) and 'root' not in (role(s),role(t))}
    def visit(n, path):
        if n in path: errors.append('cross-role cycle: '+' -> '.join(path+(n,)));return
        for a,b in role_edges:
            if a==n: visit(b,path+(n,))
    for n in {x for e in role_edges for x in e}: visit(n,())
    # subset admits deletion, never a new pair/symbol. Full application acceptance
    # additionally requires exact equality to the owner-reviewed dependency set.
    expected={(s,t):set(p['symbols']) for (s,t),p in allowed.items()}
    return dict(pass_=not errors, errors=sorted(set(errors)), module_count=len(trees), import_records=records,
                pairs=[dict(source=s,target=t,symbols=sorted(v)) for (s,t),v in sorted(actual.items())],
                exact_dependency_set=actual==expected, uses=uses, role_edges=sorted(role_edges),
                source_hashes={m:digest(t) for m,t in code.items()},
                evidence_label='Static structural checks + manually reviewed semantic AST seals; no arbitrary dynamic Python proof')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=audit();result['revision']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
    result['pass']=result.pop('pass_') and result['exact_dependency_set']
    result['policy_sha256']=hashlib.sha256((P/'policy.json').read_bytes()).hexdigest()
    if args.output:
        if args.output.exists(): raise SystemExit('Refusing to overwrite audit evidence')
        args.output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('import_records','uses','source_hashes')},indent=2))
    return 0 if result['pass'] else 1


if __name__=='__main__': raise SystemExit(main())
