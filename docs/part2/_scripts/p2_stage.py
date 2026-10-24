"""Copy committed model sources and the guarded workbook to local Drive staging.

No network operation, deletion, tag or push. Superseded staging files are moved.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

ROOT=Path(r'D:\RAD\FINAL'); REPO=ROOT/'SaigonBite'; BASE=ROOT/'Part2'
MODELS=BASE/'drive_upload/Part2/models'; TRASH=BASE/'notes/P2_trash'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def inside(p,base):
    p.resolve().relative_to(base.resolve()); return p
def move_preserved(source,target):
    inside(source,BASE); inside(target,BASE)
    assert source.is_file() and not target.exists(),(source,target)
    target.parent.mkdir(parents=True,exist_ok=True); shutil.move(str(source),str(target))

def main():
    MODELS.mkdir(parents=True,exist_ok=True); TRASH.mkdir(parents=True,exist_ok=True)
    records=[]; moves=[]
    paths=subprocess.check_output(['git','ls-files','--','models'],cwd=REPO,text=True).splitlines()
    assert paths and all((REPO/p).is_file() for p in paths)
    expected={Path(p).relative_to('models').as_posix() for p in paths}
    # Phase 1 staging was flat; relocate it before mirroring the repository hierarchy.
    for source in sorted(p for p in MODELS.iterdir() if p.is_file()):
        dest=MODELS/'shared'/source.name
        if dest.exists():
            assert sha(source)==sha(dest),(source,'conflicting staged duplicate')
            dest=TRASH/'duplicate_flat_models'/source.name
        old=str(source); move_preserved(source,dest); moves.append({'from':old,'to':str(dest),'sha256':sha(dest)})
    for source in sorted(p for p in MODELS.rglob('*') if p.is_file()):
        rel=source.relative_to(MODELS).as_posix()
        if rel not in expected:
            dest=TRASH/'superseded_staging'/rel
            old=str(source); move_preserved(source,dest); moves.append({'from':old,'to':str(dest),'sha256':sha(dest)})
    for rel in sorted(expected):
        src=REPO/'models'/rel; dst=MODELS/rel
        dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        assert sha(src)==sha(dst); records.append({'source':str(src),'target':str(dst),'sha256':sha(dst)})
    for name in ['shared']+[f'UC-{n:02}' for n in range(1,7)]: (MODELS/name).mkdir(exist_ok=True)
    workbook=BASE/'workbook/Team02_RAD_Sem01_2627_Team_Workbook.xlsx'
    staged=BASE/'drive_upload'/workbook.name
    if staged.exists() and sha(staged)!=sha(workbook):
        saved=TRASH/'pre_P2_staged_workbook.xlsx'
        assert not saved.exists(); shutil.copyfile(staged,saved)
    shutil.copyfile(workbook,staged); assert sha(staged)==sha(workbook)
    records.append({'source':str(workbook),'target':str(staged),'sha256':sha(staged)})
    ef=list((BASE/'drive_upload/eLearning').rglob('*')); assert not any(p.is_file() for p in ef)
    start=json.loads((BASE/'notes/P2_start_hashes.json').read_text(encoding='utf-8'))
    assert sha(BASE/'content/links.json')==start['contracts']['Part2/content/links.json']
    out={'records':records,'moves':moves,'model_files':len(expected),'eLearning_files':0,'links_unchanged':True,'no_external_upload':True}
    (BASE/'notes/P2_staging_manifest.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'model_files':len(expected),'moves':len(moves),'workbook_sha256':sha(staged),'eLearning_files':0},indent=2))

if __name__=='__main__': main()
