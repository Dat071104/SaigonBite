"""One-time I1 fixture alignment. Author: 722I0004 · AI-assisted (Codex)."""
from pathlib import Path
import hashlib, json
R=Path(__file__).resolve().parents[3]
changes=[]
for name in ['test_uc01_confirm.py','test_review_findings.py','test_uc01_idempotency.py']:
    p=R/'tests'/name; old=p.read_text(encoding='utf-8'); new=old
    for a,b in [('160000','155000'),('160,000','155,000'),('180000','175000'),('180,000','175,000'),('70000','65000')]:
        new=new.replace(a,b)
    if name=='test_uc01_confirm.py':
        new=new.replace('header["item_subtotal"] + header["delivery_fee"]','header["item_subtotal"] + header["delivery_fee"] - 5000')
    if name=='test_uc01_idempotency.py':
        new=new.replace('results, errors = [], []','results, errors = [], []\n    barrier = threading.Barrier(5, timeout=10)')
        new=new.replace('        try:\n            results.append','        try:\n            barrier.wait()\n            results.append')
        new=new.replace('        t.join()','        t.join(timeout=20)\n        assert not t.is_alive()')
    assert new!=old, 'One-time tool: do not repeat fixture rewriting'
    p.write_text(new,encoding='utf-8'); changes.append(dict(file=name,BR='BR-03; BR-07; BR-11',
        before=hashlib.sha256(old.encode()).hexdigest(),after=hashlib.sha256(new.encode()).hexdigest(),
        retained='All original test identities and assertion branches retained; current pricing and synchronization'))
(R/'docs/part2/implementation/p4_fixture_changes.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
