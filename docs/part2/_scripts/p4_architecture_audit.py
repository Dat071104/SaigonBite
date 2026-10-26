"""Current strict import audit; never waives frozen architecture contradictions.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import ast,csv,json,hashlib,subprocess
R=Path(__file__).resolve().parents[3];I=R/'docs/part2/implementation'


def inventory():
    records=[];domain_io=[];view_sql=[]
    for path in sorted((R/'saigonbite').rglob('*.py')):
        source=path.relative_to(R).with_suffix('').as_posix().replace('/','.')
        package=source if path.name=='__init__.py' else source.rsplit('.',1)[0]
        tree=ast.parse(path.read_text(encoding='utf-8-sig'))
        for n in ast.walk(tree):
            if isinstance(n,ast.ImportFrom):
                base=('.'.join(package.split('.')[:len(package.split('.'))-n.level+1])+'.' if n.level else '')+(n.module or '')
                base=base.rstrip('.')
                for name in n.names:
                    target=base+'.'+name.name if (R/Path(*(base+'.'+name.name).split('.'))).is_dir() or (R/Path(*(base+'.'+name.name).split('.'))).with_suffix('.py').exists() else base
                    if target.startswith('saigonbite'):records.append(dict(source=source,target=target,name=name.name,line=n.lineno))
            if isinstance(n,ast.Import):
                for name in n.names:
                    if name.name.startswith('saigonbite'):records.append(dict(source=source,target=name.name,name=name.name,line=n.lineno))
            if source.startswith('saigonbite.business.domain') and isinstance(n,ast.Call):
                name=ast.unparse(n.func)
                if name in ('open','print','input') or any(name.startswith(x) for x in ('sqlite3.','requests.','subprocess.','os.','Path(')):domain_io.append((source,n.lineno,name))
            if source.startswith('saigonbite.presentation') and isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('execute','executemany','executescript'):view_sql.append((source,n.lineno))
    return records,domain_io,view_sql


def main():
    records,domain_io,view_sql=inventory()
    annotations=json.loads((R/'docs/part2/design/design_annotations.json').read_text(encoding='utf-8'))
    model=json.loads((R/'models/shared/design_model.json').read_text(encoding='utf-8'))
    rows=[]
    for old in annotations['import_violations']:
        current=[r for r in records if r['source']==old['source'] and r['target']==old['target']]
        source=old['source'];cls=next((c for c in model['classes'].values() if c.get('module','').replace('/','.').removesuffix('.py')==source and c['name'].endswith('DAO')),None)
        signatures=[m['signature'] for m in cls['methods'] if m['name'] not in ('__init__',)][:4] if cls else []
        rows.append(dict(source=source,target=old['target'],historical_records=old['records'],current_records=len(current),
            lines=';'.join(str(r['line']) for r in current),status='BLOCKED_FROZEN_CONTRACT' if current else 'RESOLVED',
            action=('Retained actual violation; no persistence mapper/type exception. Frozen DAO/domain signatures and domain ownership require a boundary decision; see p4_architecture_conflict.md.' if current else 'Views now use the explicit controller presentation contract; NAV endpoint injection is composition-root configuration. No direct forbidden import remains.'),
            frozen_signature_examples='; '.join(signatures)))
    assert len(rows)==23 and sum(r['historical_records'] for r in rows)==44
    with (I/'p4_import_disposition.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    result=dict(author='722I0004 · AI-assisted (Codex)',revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),
        source_hashes={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'saigonbite').rglob('*.py')},
        records=records,domain_io_calls=domain_io,view_sql_calls=view_sql,registered_pairs=23,historical_records=44,
        resolved_pairs=sum(r['status']=='RESOLVED' for r in rows),blocked_pairs=sum(r['status']!='RESOLVED' for r in rows),
        G4='BLOCKED',evidence_label='Static; not a runtime behavior result')
    (I/'p4_architecture_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print({k:v for k,v in result.items() if k not in ('records','source_hashes')})


if __name__=='__main__':main()
