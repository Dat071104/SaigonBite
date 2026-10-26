"""Record evidence-backed P4 progress, without asserting unexecuted checklist closure.
Author: 722I0004 · AI-assisted (Codex).
Usage: p4_gate.py SUBPHASE LOG_RECEIPT [LOG_RECEIPT...]
"""
from pathlib import Path
import csv, json, subprocess, sys, datetime
R=Path(__file__).resolve().parents[3]; I=R/'docs/part2/implementation'
phase=sys.argv[1]; receipts=[json.loads(Path(p).read_text(encoding='utf-8')) for p in sys.argv[2:]]
assert receipts and all(r['exit']==0 for r in receipts)
progress=json.loads((I/'P4_progress.json').read_text(encoding='utf-8'))
progress.update(current_subphase='P4.'+str(int(phase)+1) if int(phase)<9 else 'G4 root assessment',
    blocker=None,resume_condition='Continue existing P4 run; preserve snapshots and all prior receipts.',G4='IN PROGRESS')
progress['completed_subphases']=list(dict.fromkeys(progress.get('completed_subphases',[])+['P4.'+phase]))
progress['last_code_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
progress['last_log']=receipts[-1]['log']
progress['exact_resume_command']='Read docs/part2/implementation/P4_progress.json; continue '+progress['current_subphase']
gate=dict(author='722I0004 · AI-assisted (Codex)',subphase='P4.'+phase,
    at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),mode='sequential',workers=0,
    code_commit_before_gate=progress['last_code_commit'],executed_receipts=sys.argv[2:],
    evidence_worktree_inputs=receipts[-1]['executable_inputs'],exit=0,
    limitation='Subphase-specific execution evidence; checklist/coverage closure is separately verified. '
    'Commit and unchanged design check follow root staged-diff review.')
p=I/f'P4.{phase}_handoff.json'; assert not p.exists();p.write_text(json.dumps(gate,indent=2),encoding='utf-8')
(I/'P4_progress.json').write_text(json.dumps(progress,indent=2),encoding='utf-8')
print('Recorded',p)
