"""Mirror committed model sources to local staging, preserving replaced bytes.
Author: 722I0004 · AI-assisted (Codex). No network, deletes or Git mutation.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parents[3];B=R.parent/'Part2';DEST=B/'drive_upload/Part2/models';TRASH=B/'notes/P3_trash'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inside(p,base):p.resolve().relative_to(base.resolve());return p
def preserve(path,kind):
    inside(path,B);rel=path.relative_to(B/'drive_upload');saved=inside(TRASH/kind/rel,B);saved.parent.mkdir(parents=True,exist_ok=True)
    if saved.exists():
        if sha(saved)==sha(path):return saved
        saved=saved.with_name(saved.name+'.'+sha(path)[:12]);assert not saved.exists() or sha(saved)==sha(path)
    shutil.copyfile(path,saved);assert sha(saved)==sha(path);return saved
def main():
    workbook=B/'workbook/Team02_RAD_Sem01_2627_Team_Workbook.xlsx';staged=B/'drive_upload'/workbook.name
    start=json.loads((B/'notes/P3_start_hashes.json').read_text(encoding='utf-8'))
    originals={name.replace('\\','/'):digest for name,digest in start['protected']['workbook'].items()}
    assert len(originals)==len(start['protected']['workbook']),'Ambiguous workbook path normalization'
    assert staged.exists() and sha(workbook)==sha(staged)
    assert sha(workbook)==originals[workbook.relative_to(B.parent).as_posix()]
    assert sha(staged)==originals[staged.relative_to(B.parent).as_posix()]
    paths=subprocess.check_output(['git','ls-files','--','models'],cwd=R,text=True).splitlines();assert paths
    untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard','--','models'],cwd=R,text=True).splitlines()
    assert not untracked,'All model sources must be committed before staging: '+str(untracked)
    model_tree=subprocess.check_output(['git','rev-parse','HEAD:models'],cwd=R,text=True).strip()
    # A Git checkout may normalize text line endings. Require a clean committed
    # model tree, then hash the actual bytes being copied; do not falsely demand
    # that a CRLF worktree file equal its LF Git blob byte for byte.
    subprocess.run(['git','diff','--quiet','HEAD','--','models'],cwd=R,check=True)
    records=[];preserved=[];expected={Path(p).relative_to('models').as_posix() for p in paths};DEST.mkdir(parents=True,exist_ok=True)
    # Recover any already-preserved bytes after an interrupted earlier copy.
    # Never replace the original hash manifest or discard a saved staging copy.
    for kind in ('replaced_staging','superseded_staging'):
        for saved in sorted((TRASH/kind).rglob('*')):
            if saved.is_file():preserved.append({'saved':str(saved),'sha256':sha(saved),'recovered_preservation':True})
    for path in sorted(DEST.rglob('*')):
        if path.is_file() and path.relative_to(DEST).as_posix() not in expected:
            saved=preserve(path,'superseded_staging');target=inside(TRASH/'relocated_extras'/path.relative_to(DEST),B);target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();shutil.move(str(inside(path,DEST)),str(target));preserved.append({'from':str(path),'saved':str(saved),'relocated':str(target),'sha256':sha(target)})
    for rel in sorted(expected):
        source=inside(R/'models'/rel,R/'models');target=inside(DEST/rel,DEST);assert source.is_file();digest=sha(source)
        if target.exists() and sha(target)!=digest:
            saved=preserve(target,'replaced_staging');preserved.append({'from':str(target),'saved':str(saved),'sha256':sha(saved)})
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);assert sha(target)==digest;records.append({'source':str(source),'target':str(target),'sha256':digest})
    elearning=[p for p in (B/'drive_upload/eLearning').rglob('*') if p.is_file()];assert not elearning
    assert {p.relative_to(DEST).as_posix() for p in DEST.rglob('*') if p.is_file()}==expected
    result={'author':'722I0004 · AI-assisted (Codex)','at_utc':datetime.now(timezone.utc).isoformat(),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'models_tree_oid':model_tree,'model_files':len(records),'records':records,'preserved':preserved,'workbook_unchanged':True,'workbook_sha256':sha(staged),'eLearning_files':0,'no_external_upload':True}
    (B/'notes/P3_staging_manifest.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ('records','preserved')},indent=2))
if __name__=='__main__':main()
