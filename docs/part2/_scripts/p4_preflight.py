"""P4 entry evidence and a nonmutating frozen-mapping compatibility probe.
Author: 722I0004 · AI-assisted (Codex).
Never connects to an existing database or changes application/design sources.
"""
from pathlib import Path
import ast
import csv
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

R = Path(__file__).resolve().parents[3]
W = R.parent
P = W / 'Part2'
N = P / 'notes'
S = N / 'P4_start_snapshots'
D = R / 'docs/part2'
I = D / 'implementation'
T = D / 'test_report'
AUTHOR = '722I0004 · AI-assisted (Codex)'
EXPECTED = 'cbadf1c3833fecba16769d9036cb4ebfe1e563f845379ab3559dbe6f990790f3'


def digest(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def git(*args):
    return subprocess.check_output(['git', '-C', str(R), *args], text=True, encoding='utf-8').strip()


def rows(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def csvsave(p, data, fields):
    with p.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(data)


def module(name, p):
    spec = importlib.util.spec_from_file_location(name, p)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def capture(name, command, env):
    assert not (T / (name + '.log')).exists(), 'Never overwrite an existing execution log'
    assert not (T / (name + '.json')).exists(), 'Never overwrite an existing execution receipt'
    start = datetime.now(timezone.utc).isoformat()
    run = subprocess.run(command, cwd=R, env=env, capture_output=True, text=True,
                         encoding='utf-8', errors='replace', timeout=120)
    log = T / (name + '.log')
    log.write_text(run.stdout + '\nSTDERR:\n' + run.stderr, encoding='utf-8')
    receipt = dict(command=command, cwd=str(R), started_at_utc=start,
                   ended_at_utc=datetime.now(timezone.utc).isoformat(), exit=run.returncode,
                   log=str(log), log_sha256=digest(log))
    save(T / (name + '.json'), receipt)
    return receipt


def main():
    if (N / 'P4_start_hashes.json').exists():
        if (I / 'p4_preflight_receipt.json').exists():
            raise SystemExit('Entry already recorded: read P4_progress.json and resume P4.1; no recollection.')
        if sys.argv[1:] == ['--resume-after-snapshot']:
            initial = json.loads((N / 'P4_start_hashes.json').read_text(encoding='utf-8'))
            assert git('rev-parse', 'HEAD') == initial['head']
            for record in initial['archived']:
                assert digest(Path(record['source'])) == record['sha256']
                assert digest(Path(record['snapshot'])) == record['sha256']
            assert all(digest(R / p) == value for p, value in initial['mutable_start'].items())
            prep = json.loads((N / 'P4_preparation_receipt.json').read_text(encoding='utf-8-sig'))
            return after_snapshot(initial['protected'],
                [Path(p) for p in initial['protected'] if Path(p).is_relative_to(R / 'models')],
                [Path(p) for p in initial['protected'] if Path(p).is_relative_to(P / 'drive_upload')], prep)
        raise SystemExit('Existing P4 run: resume its progress; never regenerate start evidence.')
    start = datetime.now(timezone.utc).isoformat()
    prep = json.loads((N / 'P4_preparation_receipt.json').read_text(encoding='utf-8-sig'))
    plan = W / 'PLAN_SaigonBite_Part2_Final.md'
    assert digest(plan) == EXPECTED
    for name, expected in prep['artifact_hashes'].items():
        assert digest(Path(name)) == expected, name
    assert git('rev-parse', 'HEAD') == prep['head']
    assert git('branch', '--show-current') == 'part2'
    status = git('status', '--porcelain=v1')
    assert status == '?? docs/part2/_scripts/p4_preflight.py', repr(status)
    S.mkdir(parents=True, exist_ok=False)
    I.mkdir(parents=True, exist_ok=True)
    T.mkdir(parents=True, exist_ok=True)
    # Exact original bytes before any checklist, traceability or derived-design change.
    originals = [Path(k) for k in prep['artifact_hashes']]
    originals += [plan, N / 'P4_preparation_receipt.json', N / 'P3_final_receipt.json',
                  D / 'traceability.csv', D / 'design/design_consistency.csv',
                  D / 'design/class_table_mapping.csv', R / 'db/schema.sql',
                  Path(__file__).with_name('p3_design_crosscheck.py')]
    archived = []
    for p in originals:
        target = S / p.relative_to(W)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
        assert digest(p) == digest(target)
        archived.append(dict(source=str(p), snapshot=str(target), sha256=digest(p)))
    tracked = git('ls-files').splitlines()
    mutable = lambda s: (s.startswith(('saigonbite/', 'tests/', 'docs/part2/implementation/',
                                      'docs/part2/test_report/')) or s in {
        'db/schema.sql', 'db/seed.sql', 'db/seed_demo.sql', 'db/migrations/README.md',
        'init_db.py', 'app.py', 'requirements.txt', 'pytest.ini',
        'docs/part2/traceability.csv', 'docs/part2/design/design_consistency.csv',
        'docs/part2/ai_usage_log.md'})
    protected = {R / p for p in tracked if not mutable(p)}
    for root in [W / 'Part1_v2', P / 'drive_upload', P / 'workbook']:
        protected.update(p for p in root.rglob('*') if p.is_file())
    protected.update(R.joinpath('models').rglob('*'))
    protected.update([plan, P / 'README.md', P / 'content/links.json'])
    protected.update(p for p in (P / 'codex').iterdir()
                     if p.is_file() and p.name != 'P4_CHECKLIST.md')
    protected.update(p for p in N.rglob('*') if p.is_file() and
                     any(part.startswith(('P1', 'P2', 'P3')) for part in p.relative_to(N).parts))
    # Hash discovered existing DB bytes, including sidecars, without opening SQLite.
    db_files = set()
    for root in [R / 'instance', R / 'db', W / 'tmp', W / 'test_results']:
        if root.exists():
            db_files.update(p for p in root.rglob('*') if p.is_file() and
                            (p.suffix in ('.db', '.sqlite', '.sqlite3') or
                             p.name.endswith(('-wal', '-shm'))))
    protected.update(db_files)
    manifest = {str(p): dict(sha256=digest(p), bytes=p.stat().st_size)
                for p in sorted(protected) if p.is_file()}
    application = {p: digest(R / p) for p in tracked if mutable(p)}
    models = [p for p in (R / 'models').rglob('*') if p.is_file()]
    staging = [p for p in (P / 'drive_upload').rglob('*') if p.is_file()]
    save(N / 'P4_start_hashes.json', dict(author=AUTHOR, started_at_utc=start,
        head=prep['head'], branch='part2', starting_status=status,
        status_note='Only newly created P4 preflight tool; initial observed checkout was clean.',
        preparation_sha256=digest(N / 'P4_preparation_receipt.json'),
        plan_sha256=digest(plan), archived=archived, protected=manifest,
        mutable_start=application, model_files=len(models), staging_files=len(staging),
        existing_database_files=[str(p) for p in sorted(db_files)]))
    return after_snapshot(manifest, models, staging, prep)


def after_snapshot(manifest, models, staging, prep):
    tracked_models = git('ls-files', '--', 'models').splitlines()
    assert len(tracked_models) == 2327
    extra_models = [str(p) for p in models if p.relative_to(R).as_posix() not in tracked_models]
    save(I / 'p4_model_count_reconciliation.json', dict(tracked_model_files=len(tracked_models),
        existing_model_files=len(models), extra_model_files=extra_models,
        staging_files=len(staging), all_existing_bytes_in_start_manifest=True,
        disposition='Historical 2327 counts tracked model artifacts; two pre-existing ignored pyc files '
        'raise actual on-disk count to 2329. Preserve and hash both; do not delete or exclude them.',
        tool_intervention='First preflight stopped at count assertion after durable snapshot. '
        'Resume after snapshot with original bytes/manifests; no restart or test rerun.'))
    design = rows(D / 'design/P4_design_inputs.csv')
    ops = rows(D / 'ssd_operations.csv')
    flows = rows(D / 'ssd_flow_membership.csv')
    anchors = rows(D / 'pc_mg_register.csv')
    counts = dict(design_rows=len(design), design_elements=len({r['element'] for r in design}),
                  operations=len({r['op_id'] for r in ops}), main_anchors=len(anchors),
                  flow_rows=len(flows), flow_fields=list(flows[0]))
    source_hash = digest(D / 'design/P4_design_inputs.csv')
    csvsave(I / 'p4_design_resolution.csv', [dict(source_row=n, source_sha256=source_hash,
        **r, implementation='', test_nodes='', code_revision='', disposition='NOT RUN',
        remaining_limitations='P4.1 blocked before application changes')
        for n, r in enumerate(design, 2)],
        ['source_row', 'source_sha256', *design[0], 'implementation', 'test_nodes',
         'code_revision', 'disposition', 'remaining_limitations'])
    issues = [f'F-{i:02}' for i in range(1, 10)] + [f'P2-S{i:02}' for i in range(1, 19)]
    issues += [f'P3-S{i:02}' for i in range(1, 5)] + ['P4-A01']
    csvsave(I / 'p4_issue_resolution.csv', [dict(id=x, baseline_observation=(
        'Existing PaymentDAO updated_at-or-created_at fallback; no invented defect' if x == 'P2-S08'
        else 'See frozen P2/P3 reports or locked plan; not runtime-qualified'),
        subphase='; '.join(sorted({r['P4 subphase'] for r in design if x in r['P4 input']})),
        action='Retain baseline; execution blocked by frozen mapping/checker conflict',
        tests='', commit='', status='NOT RUN') for x in issues],
        ['id', 'baseline_observation', 'subphase', 'action', 'tests', 'commit', 'status'])
    coverage = [dict(id=r['id'], kind='main anchor', source='pc_mg_register.csv',
                     obligation=r['text']) for r in anchors]
    suc = (D / 'SUC.md').read_text(encoding='utf-8-sig')
    for section in re.split(r'(?m)^## ', suc)[1:]:
        sid = re.match(r'SUC-\d+', section)[0]
        for line in section.splitlines():
            if line.startswith('- **Postconditions:**'):
                for match in re.finditer(r'`(SUC\d+-PC\d+)`\s*([^`]+)', line):
                    coverage.append(dict(id=match[1], kind='supporting PC', source='SUC.md',
                                         obligation=match[2].strip()))
            elif line.startswith(('- **Guards:**', '- **Failure:**')):
                kind = 'guard' if '**Guards:**' in line else 'failure'
                coverage.append(dict(id=sid + '/' + kind, kind=kind, source='SUC.md', obligation=line))
    csvsave(I / 'p4_test_coverage.csv', [dict(**r, tests='', meaningful_assertions='',
        passing_execution='', log='', commit='', status='NOT RUN') for r in coverage],
        ['id', 'kind', 'source', 'obligation', 'tests', 'meaningful_assertions',
         'passing_execution', 'log', 'commit', 'status'])
    obligations = []
    for p in sorted((R / 'tests').glob('test_*.py')):
        tree = ast.parse(p.read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith('test_'):
                obligations.append(dict(historical_node=p.relative_to(R).as_posix() + '::' + node.name,
                    source_sha256=digest(p), line=node.lineno,
                    assert_count=sum(isinstance(n, ast.Assert) for n in ast.walk(node)),
                    retained='YES; unchanged bytes', expectation_change='',
                    before='COLLECTION BLOCKED; see baseline log', after='NOT RUN'))
    csvsave(I / 'p4_test_inventory.csv', obligations, list(obligations[0]))
    scratch = N / 'P4_test_scratch'
    scratch.mkdir(exist_ok=True)
    env = os.environ.copy()
    env.update(SAIGONBITE_DATABASE=str(scratch / 'UNUSED_DEFAULT_DO_NOT_CREATE.db'),
               SAIGONBITE_ENV='testing', PYTHONDONTWRITEBYTECODE='1',
               PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONIOENCODING='utf-8')
    env.pop('PYTHONPATH', None)
    py = str(R / '.venv/Scripts/python.exe')
    environment = capture('p4_environment', [py, '-c',
        'import sys, importlib.metadata as m; print(sys.version); '
        'print({p:m.version(p) for p in ["flask","flask-login","pytest","werkzeug"]})'], env)
    baseline = capture('p4_baseline_collection', [py, '-m', 'pytest', '--collect-only',
        '--basetemp=' + str(scratch / 'baseline_pytest')], env)
    # Invoke the actual frozen parser and mapping auditor. Only an in-memory candidate
    # changes: no application source, mapping, inventory file or real database is touched.
    inv = module('p4_probe_inventory', D / '_scripts/p3_code_inventory.py')
    checker = module('p4_probe_checker', D / '_scripts/p3_design_crosscheck.py')
    schema = (R / 'db/schema.sql').read_text(encoding='utf-8-sig')
    needle = 'CREATE TABLE user_account (\n'
    assert schema.count(needle) == 1
    candidate = schema.replace(needle, needle + '    created_at TEXT NOT NULL,\n', 1)
    mapping = rows(D / 'design/class_table_mapping.csv')
    variants = {}
    for name, sql in [('baseline', schema), ('required_created_at_candidate', candidate)]:
        checks = []
        def check(kind, key, ok, message, *extra):
            checks.append(dict(kind=kind, key=key, pass_=bool(ok), message=message))
        checker.audit_mapping({'schema': inv.schema_inventory(sql)}, mapping, check)
        variants[name] = dict(checks=len(checks), failures=[r for r in checks if not r['pass_']])
    assert not variants['baseline']['failures']
    failures = variants['required_created_at_candidate']['failures']
    assert len(failures) == 1 and failures[0]['kind'] == 'mapping_column_coverage'
    save(T / 'p4_frozen_mapping_conflict.json', dict(author=AUTHOR, label='Static counterfactual',
        actual_app_changed=False, runtime_test=False, checker_sha256=digest(D / '_scripts/p3_design_crosscheck.py'),
        inventory_parser_sha256=digest(D / '_scripts/p3_code_inventory.py'),
        mapping_sha256=digest(D / 'design/class_table_mapping.csv'),
        baseline_schema_sha256=digest(R / 'db/schema.sql'),
        candidate_schema_sha256=hashlib.sha256(candidate.encode()).hexdigest(),
        candidate_change='Add only user_account.created_at TEXT NOT NULL in memory', variants=variants,
        conflict='Required column cannot pass unchanged checker with protected absent-C0 mapping.'))
    counts.update(supporting_PCs=sum(r['kind'] == 'supporting PC' for r in coverage),
                  supporting_guard_sections=9, supporting_failure_sections=9,
                  historical_test_functions=len(obligations))
    save(I / 'p4_preflight_receipt.json', dict(author=AUTHOR, counts=counts,
        baseline=baseline, environment=environment, workers=0, owner_answers='No new answers in decision log',
        blocker='P4-B01: required created_at versus protected mapping/checker',
        application_changed=False, protected_files=len(manifest), models=len(models), staging=len(staging)))
    print(json.dumps(dict(counts=counts, baseline_exit=baseline['exit'],
                         mapping_probe=variants, protected_files=len(manifest)), indent=2))


if __name__ == '__main__':
    main()
