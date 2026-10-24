"""Root-only explicit-path UC commit, with a retained staged review patch."""
from pathlib import Path
import argparse
import subprocess

REPO=Path(r'D:\RAD\FINAL\SaigonBite'); OUT=Path(r'D:\RAD\FINAL\Part2\notes\P2-root')
def git(*args): return subprocess.check_output(['git',*args],cwd=REPO,text=True,encoding='utf-8')
def main():
    p=argparse.ArgumentParser();p.add_argument('uc',choices=[f'UC-{n:02}' for n in range(1,7)]);a=p.parse_args();uc=a.uc;n=int(uc[-2:])
    assert git('branch','--show-current').strip()=='part2'
    assert not git('diff','--cached','--name-only').strip(),'Do not mix an existing stage'
    paths=[f'docs/part2/{uc}/description.md',f'docs/part2/report/II_2-2-{n}_{uc}.md']
    paths += [x.relative_to(REPO).as_posix() for x in sorted((REPO/'models'/uc).iterdir()) if x.is_file() and x.name.startswith(('activity_uc'+uc[-2:],'ssd_uc'+uc[-2:])) and x.suffix in ('.py','.json','.drawio','.png','.svg')]
    if uc in ('UC-04','UC-05','UC-06'): paths.append('docs/part2/_agent_reports/P2-'+{'UC-04':'F','UC-05':'E','UC-06':'G'}[uc]+'.md')
    assert all((REPO/x).is_file() for x in paths)
    subprocess.run(['git','add','--',*paths],cwd=REPO,check=True,capture_output=True)
    subprocess.run(['git','diff','--cached','--check'],cwd=REPO,check=True,capture_output=True)
    staged=git('diff','--cached','--name-only').splitlines(); assert set(staged)<=set(paths) and staged
    patch=git('diff','--cached','--no-ext-diff')
    (OUT/f'staged_{uc}.patch').write_text(patch,encoding='utf-8')
    # Enforce the reviewed unit boundary; source/report structure was audited before staging.
    assert all(x.startswith(('models/'+uc+'/',f'docs/part2/{uc}/',f'docs/part2/report/II_2-2-{n}_','docs/part2/_agent_reports/P2-')) for x in staged)
    print(git('diff','--cached','--stat').splitlines()[-1])
    message=f'Part 2 report II: {uc} analysis package'
    subprocess.run(['git','commit','-m',message],cwd=REPO,check=True,capture_output=True)
    print(git('log','-1','--format=%h %s').strip())

if __name__=='__main__': main()
