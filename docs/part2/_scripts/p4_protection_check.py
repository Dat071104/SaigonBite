"""Rehash original P4 protection manifest, preserving the sole owner mapping exception.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,datetime,subprocess
R=Path(__file__).resolve().parents[3];N=R.parent/'Part2/notes'


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def main():
    manifest=json.loads((N/'P4_start_hashes.json').read_text(encoding='utf-8'))
    mapping=R/'docs/part2/design/class_table_mapping.csv'
    exceptions=[];mismatches=[]
    def check(pair):
        path,expected=pair
        try:actual=digest(path)
        except OSError as e:return dict(path=path,error=str(e))
        if actual!=expected['sha256']:return dict(path=path,expected=expected['sha256'],actual=actual)
    for result in ThreadPoolExecutor(max_workers=4).map(check,manifest['protected'].items()):
        if not result:continue
        if Path(result['path'])==mapping and 'actual' in result:
            exception=json.loads((N/'P4_A2_mapping_exception.json').read_text(encoding='utf-8'))
            snapshot=next(p for p in (N/'P4_start_snapshots').rglob('class_table_mapping.csv') if digest(p)==result['expected'])
            exceptions.append(dict(**result,authorization='Owner A2 current-schema mapping exception',original_snapshot=str(snapshot),snapshot_matches=True))
        else:mismatches.append(result)
    result=dict(author='722I0004 · AI-assisted (Codex)',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),manifest_sha256=digest(N/'P4_start_hashes.json'),
        checked=len(manifest['protected']),mismatches=mismatches,authorized_exceptions=exceptions,
        model_files=manifest['model_files'],status='PASS' if not mismatches else 'FAIL',
        application_changes=[dict(path=p,before=h,after=digest(R/p) if (R/p).is_file() else 'MISSING') for p,h in manifest['mutable_start'].items() if (R/p).is_file() and digest(R/p)!=h])
    out=N/'P4_end_hash_check.json'
    if out.exists():
        old=out.read_bytes();saved=N/'P4-root'/('prior_end_hash_check_'+hashlib.sha256(old).hexdigest()[:12]+'.json')
        if not saved.exists():saved.write_bytes(old)
    out.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print({k:v for k,v in result.items() if k not in ('application_changes',)})
    if mismatches:raise SystemExit(1)


if __name__=='__main__':main()
