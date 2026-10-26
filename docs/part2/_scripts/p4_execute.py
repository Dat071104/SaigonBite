"""Capture P4 executions without overwriting evidence. Author: 722I0004 · AI-assisted (Codex)."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
R = Path(__file__).resolve().parents[3]
N = R.parent / 'Part2/notes/P4-root'
N.mkdir(exist_ok=True)
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=R, text=True).strip()
mode = sys.argv[1]
if mode == 'design':
    assert not (N.parent / 'P3-root' / f'design_crosscheck_{head[:7]}.json').exists()
    command = [r'C:\Users\ADMIN\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe',
               '-X','utf8','-I',str(R/'docs/part2/_scripts/p3_design_crosscheck.py'),'--commit','HEAD']
else:
    command = [str(R/'.venv/Scripts/python.exe'),'-X','utf8','-B','-m','pytest',*sys.argv[2:]]
    if '--collect-only' not in command:
        command += ['--junitxml='+str(N/f'{mode}_{stamp}.xml')]
    command += ['--basetemp='+str(N.parent/'P4_test_scratch'/f'{mode}_{stamp}')]
env = os.environ.copy()
env.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',
           SAIGONBITE_DATABASE=str(N.parent/'P4_test_scratch/UNUSED_DEFAULT_DO_NOT_CREATE.db'),SAIGONBITE_ENV='testing')
env.pop('PYTHONPATH',None)
inputs = {}
for base in ['saigonbite','tests','db']:
    for p in (R/base).rglob('*'):
        if p.is_file() and p.suffix in ('.py','.sql','.html','.css','.js','.md'):
            inputs[p.relative_to(R).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['init_db.py','app.py','pytest.ini','requirements.txt']:
    inputs[name] = hashlib.sha256((R/name).read_bytes()).hexdigest()
result = subprocess.run(command,cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',timeout=240)
log = N/f'{mode}_{head[:7]}_{stamp}.log'
log.write_text(result.stdout+'\nSTDERR:\n'+result.stderr,encoding='utf-8')
receipt = dict(command=command,cwd=str(R),head=head,started_at_utc=stamp,
    ended_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit=result.returncode,
    log=str(log),log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),executable_inputs=inputs,
    label='Static' if mode=='design' else 'Executed')
log.with_suffix('.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(result.stdout[-14000:]);print(result.stderr);print('RECEIPT',log.with_suffix('.json'))
raise SystemExit(result.returncode)
