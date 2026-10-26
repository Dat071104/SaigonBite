"""Finish the P4-B01 blocked checkpoint; never changes application/protected design.
Author: 722I0004 · AI-assisted (Codex).
Usage: existing project Python p4_checkpoint.py prepare|final
"""
from pathlib import Path
import csv
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

R = Path(__file__).resolve().parents[3]
W = R.parent
P = W / 'Part2'
N = P / 'notes'
D = R / 'docs/part2'
I = D / 'implementation'
T = D / 'test_report'
AUTHOR = '722I0004 · AI-assisted (Codex)'


def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def save(p, obj):
    p.parent.mkdir(exist_ok=True, parents=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def git(*args):
    return subprocess.check_output(['git', '-C', str(R), *args], text=True, encoding='utf-8').strip()


def csvread(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def prepare():
    initial = read(N / 'P4_start_hashes.json')
    pre = read(I / 'p4_preflight_receipt.json')
    probe = read(T / 'p4_frozen_mapping_conflict.json')
    assert not probe['variants']['baseline']['failures']
    assert len(probe['variants']['required_created_at_candidate']['failures']) == 1
    flows = csvread(D / 'ssd_flow_membership.csv')
    counts = pre['counts']
    counts['catalogue_op_ids'] = counts['operations']
    counts['operations'] = len({r['catalogue_id'] for r in flows})
    counts.update(SSD_occurrences=len(flows),
                  UC_operation_pairs=len({(r['UC'], r['catalogue_id']) for r in flows}),
                  listCatalogue_occurrences=sum(r['operation'] == 'listCatalogue' for r in flows),
                  traceability_rows=len(csvread(D / 'traceability.csv')))
    assert (counts['SSD_occurrences'], counts['UC_operation_pairs'], counts['operations'],
            counts['main_anchors'], counts['design_rows'], counts['design_elements'],
            counts['traceability_rows'], counts['listCatalogue_occurrences']) == (41,39,38,30,121,96,52,3)
    save(I / 'p4_counts.json', counts)
    pins = []
    for line in (R / 'requirements.txt').read_text().splitlines():
        if '==' in line:
            package, expected = line.strip().split('==')
            actual = importlib.metadata.version(package)
            pins.append(dict(package=package, expected=expected, actual=actual, match=actual == expected))
    assert all(r['match'] for r in pins)
    save(T / 'p4_pinned_environment.json', dict(interpreter=sys.executable, version=sys.version,
        requirements_sha256=sha(R / 'requirements.txt'), pins=pins,
        bundled_python='3.12.14; Flask unavailable; static checker only'))
    original_trace = csvread(D / 'traceability.csv')
    save(I / 'p4_traceability_negative_evidence.json', dict(source_sha256=sha(D / 'traceability.csv'),
        rows=len(original_trace), examples=[r for r in original_trace if r['Req ID'] in ('FR-01','FR-02','FR-03')],
        audit_status='NOT RUN; no mapping repair before the foundation gate',
        required_join='For all 52 rows: exact Req ID + complete UC/SUC IDs + complete PC/MG tokens. '
        'Resolve each token to its actual contract and operation; supporting-only rows cite supporting '
        'controllers and explicitly lack a standalone main-UC diagram. No ordinal or digit-substring join.',
        regression_plan='Reject original FR-01->DeliveryController.pick_up, FR-02->delivery finish/failure, '
        'and FR-03->PlaceOrderController.confirm_order mappings. These regressions are NOT RUN.'))
    def verify(item):
        name, record = item
        p = Path(name)
        return None if p.is_file() and sha(p) == record['sha256'] else name
    with ThreadPoolExecutor(max_workers=4) as pool:
        mismatches = [p for p in pool.map(verify, initial['protected'].items()) if p]
    assert not mismatches, mismatches
    application = {p: sha(R / p) for p in initial['mutable_start']}
    assert application == initial['mutable_start'], 'No original mutable input should have changed yet'
    save(N / 'P4_end_hash_check.json', dict(author=AUTHOR, at_utc=datetime.now(timezone.utc).isoformat(),
        protected_checked=len(initial['protected']), mismatches=mismatches,
        model_files=initial['model_files'], staging_files=initial['staging_files'],
        original_mutable_inputs_unchanged=True, manifest_sha256=sha(N / 'P4_start_hashes.json')))
    save(I / 'p4_changed_application_manifest.json', dict(baseline=initial['head'],
        changed_application_files=[], app_tests_schema_configuration_unchanged=True,
        note='P4 evidence/tooling only; no runtime qualification.'))
    checklist = P / 'codex/P4_CHECKLIST.md'
    text = checklist.read_text(encoding='utf-8-sig')
    # Only fully evidenced entry obligations. Partial inventory/source review is left unchecked.
    accepted = {
        'P4-001': 'P4_start_hashes.json and exact start snapshots; all preparation/plan hashes MATCH.',
        'P4-004': 'p4_preflight_receipt.json / P4_start_hashes.json: clean part2 G3 baseline, no prior P4 run.',
        'P4-005': 'decision_log.md inspected; no new answers; locked defaults and 31/10 checkpoint retained.',
        'P4-006': 'P4_start_hashes.json / P4_end_hash_check.json; all model/staging bytes included; zero mismatches.',
        'P4-007': 'test_report/p4_pinned_environment.json and p4_environment.log; all 14 pins MATCH; isolated scratch.',
        'P4-011': 'P4-brief.md, P4_progress.json, p4_performance.csv; sequential root workers=0; credits UNAVAILABLE.',
        'P4-012': 'Start traceability snapshot and p4_traceability_negative_evidence.json; all-52 exact-token audit specified, not executed.'}
    for ident, evidence in accepted.items():
        pattern = r'(?m)^\| - \[ \] ' + ident + r' \|.*$'
        matches = re.findall(pattern, text)
        assert len(matches) == 1, ident
        text = text.replace(matches[0], matches[0].replace('- [ ]', '- [x]', 1)[:-1] + ' ' + evidence + ' |')
    checked = len(re.findall(r'- \[x\] P4-\d+', text))
    unchecked = len(re.findall(r'- \[ \] P4-\d+', text))
    assert checked == len(accepted) and checked + unchecked == 144
    text = text.replace('**Preparation state: 0/144 checked. P4 has NOT RUN.** This is a working checklist for the new session, not a completion report. Replace this preparation sentence with derived live counts when executing; preserve its initial bytes in the start snapshot.',
        f'**Live state: {checked}/144 checked; {unchecked} unchecked. G4 BLOCKED at entry to P4.1 (P4-B01).** '
        'Only evidenced preflight items are checked. No application change or passing application test is claimed. '
        'See `_agent_reports/P4-root.md`; preserve and resume this checkpoint after owner disposition.')
    checklist.write_text(text, encoding='utf-8')
    end = datetime.now(timezone.utc)
    save(I / 'P4_progress.json', dict(author=AUTHOR, current_subphase='P4.1 ENTRY BLOCKED',
        completed_ids=list(accepted), remaining_ids=[f'P4-{i:03}' for i in range(1,145) if f'P4-{i:03}' not in accepted],
        completed_subphases=[], last_code_commit=initial['head'],
        last_log='docs/part2/test_report/p4_baseline_collection.log', mode='sequential', workers=0,
        blocker='P4-B01: adding mandatory created_at fails unchanged checker against protected mapping',
        exact_resume_command='Get-Content -LiteralPath D:/RAD/FINAL/SaigonBite/docs/part2/implementation/P4_progress.json -Raw',
        resume_condition='Owner authorizes a narrow mapping-boundary amendment; verify start hashes and resume '
        'existing run at P4.1. Do not rerun preflight main or regenerate snapshots.', G4='BLOCKED'))
    with (I / 'p4_performance.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['task_set','mode','accepted_tasks','start_utc','end_utc',
            'elapsed_seconds','credits','regressions_introduced','manual_interventions','scope_limit'])
        writer.writeheader()
        writer.writerow(dict(task_set='P4 entry evidence and frozen mapping compatibility probe',
            mode='sequential; workers=0', accepted_tasks=';'.join(accepted),
            start_utc=initial['started_at_utc'], end_utc=end.isoformat(),
            elapsed_seconds=(end-datetime.fromisoformat(initial['started_at_utc'])).total_seconds(),
            credits='UNAVAILABLE', regressions_introduced=0,
            manual_interventions='2: resume after existing-model count mismatch (2327 tracked + 2 ignored pyc); '
                'stop dependent writes on reproduced protected-contract conflict',
            scope_limit='Measured snapshot/probe/checkpoint interval; earlier reading and later commit excluded; no mode comparison'))
    fail = probe['variants']['required_created_at_candidate']['failures'][0]
    report = f'''# P4 blocked entry assessment

Author: {AUTHOR}

Date: 26 October 2026, Asia/Bangkok. **G4: BLOCKED. {checked}/144 checklist items checked; {unchecked} unchecked.** This is an early contract-blocker assessment, not the consolidated post-P4.9 assessment or an independent approval. Workers=0. P4.1–P4.9 have not passed; P5–P8 have not started.

## Top finding: P4-B01 — mandatory schema repair cannot pass the frozen design gate

P4 B1/checklist P4-019 and locked plan §5.3 require `user_account.created_at` end to end. P4 A2 protects `design/class_table_mapping.csv` and P1–P3 scripts; C1 mandates the unchanged checker on each current commit and prohibits weakening/ignoring it.

The protected mapping row 30 names `UserAccount.created_at` as `target gap`, with column `— (column absent at C0)`. In `p3_design_crosscheck.py:28–44`, `audit_mapping` takes all columns from the selected commit as its expected set, skips target-gap rows, then requires exact equality with mapped columns. Therefore the mandatory new column has no accepted mapping. Its type, default or nullability cannot remove this set mismatch.

`test_report/p4_frozen_mapping_conflict.json` reproduces this with the actual unchanged checker function and SQL parser: the actual baseline mapping passes; an in-memory candidate adding only `created_at TEXT NOT NULL` produces exactly one failure: `{fail['kind']}`, `{fail['message']}`. No candidate application/schema file or real database was changed. This is a Static compatibility counterexample, not a failed runtime implementation.

Changing only the authorized application or the new P4 design-resolution register cannot change the checker's protected mapping input. Omitting the column would violate P4-019; editing the protected mapping/checker or overlooking a failed gate would violate the current authority. Dependent implementation stops here under C1's genuine frozen-contract-blocker rule.

**Concrete unblock proposal:** authorize a narrowly scoped current-schema update to `docs/part2/design/class_table_mapping.csv`, retaining its exact original bytes/hash in the starting snapshot and keeping historical P3 GAP/MATCH classifications attributable to C0. At minimum, map the existing UserAccount.created_at target to the implemented `user_account.created_at` TEXT column with its actual nullability/default. Any later authorized SQL CHECK strengthening must also have matching current constraint facts in that mapping. Keep the checker unchanged. No model redraw, plan rewrite, new feature or blanket protected-path permission is requested. After that disposition, resume this same run at P4.1, complete preflight reading/register detail, then implement and test in the prescribed order.

## Actual execution and limits

- Application revision: `{initial['head']}` on `part2`, initially clean. Application, tests, schema and configuration remain byte-identical. No application fix commit exists.
- Existing project interpreter is Python 3.13.2; all 14 requirement pins match. Bundled Python is 3.12.14 with Flask unavailable; it remains suitable for the static checker. No dependency install/global upgrade occurred.
- Baseline collection before F-01 repair exited **{pre['baseline']['exit']}**. See `test_report/p4_baseline_collection.log` and its command/timestamps/hash receipt. No passing test/JUnit result exists; the full suite was NOT RUN. Historical passing I1 results are not transferred.
- Frozen counts recomputed: {counts['SSD_occurrences']} SSD occurrences / {counts['UC_operation_pairs']} UC-operation pairs / {counts['operations']} op IDs, including {counts['listCatalogue_occurrences']} listCatalogue occurrences; {counts['main_anchors']} main anchors; {counts['design_rows']} P4 rows / {counts['design_elements']} elements; {counts['traceability_rows']} requirement rows. SUC has {counts['supporting_PCs']} explicit PCs and nine guard/failure sections each. Registry presence is not behavioral coverage.
- Register skeletons preserve every input row's source line/hash and all current test-function obligations. They have NOT RUN dispositions. Exact expanded pytest node IDs remain unavailable because collection failed; assertion/fixture review and future-case inventory are incomplete. P4-008/009/010 remain unchecked.
- FR-01/02/03 semantic mismatches are archived with the original traceability bytes; the complete all-52-row repair/regression remains NOT RUN.
- Protected manifest/end verification covers {len(initial['protected'])} files, including all {initial['model_files']} existing model-directory files and {initial['staging_files']} staging files. The historical 2,327 tracked model files are all present; two pre-existing ignored pyc files explain the on-disk total of 2,329. See `p4_model_count_reconciliation.json`. The complete operation catalogue has {counts['catalogue_op_ids']} IDs; the SSD occurrence set references 38 of them. Zero immutable mismatches. Existing database bytes/sidecars remain untouched. Final receipt binds the post-commit Static check; its success is no runtime evidence.
- Required race, transaction, security, independent report oracle and coverage tests remain NOT RUN. No skipped/xfail test is used to qualify G4. No report-oracle dataset/query was executed.

## Ownership, schedule and later evidence

No new L/Q answers, feedback, AI-policy approval, roster change or official deadline appears in the decision log. Keep defaults and the 31 October checkpoint. All five client-question slots remain consumed. The 92–130-hour estimate exceeds the old 84-hour capacity; no schedule promise or unmeasured speed/cost claim is made. `p4_performance.csv` records the bounded measured interval; credits are UNAVAILABLE.

Original P3 independent NOT READY remains historical; later root design disposition is separate. This root checkpoint claims no independent review and no P4 readiness.

All changes in this commit are P4 tooling/evidence and an append-only AI-log entry. Post-commit identity, commit list, full design-check command/log/hash, source-equivalence proof and actual checklist counts are recorded outside the repo in `D:/RAD/FINAL/Part2/notes/P4_final_receipt.json`.

No new upload is required in P4. Future Figma/browser integration evidence belongs to P5 and `Part2/evidence/figma/`; deployment/restore evidence to P6 and `Part2/evidence/deploy/`; final native/document/submission packaging to P7 and `Part2/deliverables/` / `Part2/drive_upload/`. No mirror, push, tag, merge, release, upload, contact or spend occurred. Next action is the named mapping-boundary disposition and P4.1 resume, not P5.
'''
    (D / '_agent_reports/P4-root.md').write_text(report, encoding='utf-8')
    with (D / 'ai_usage_log.md').open('a', encoding='utf-8') as f:
        f.write('\n\n## 26 October 2026 — P4 entry and frozen-contract blocker\n\n'
            f'Author: {AUTHOR}. Root used the owner-supplied P4 prompt to verify hashes, snapshot originals, '
            'inventory entry evidence, reproduce original collection failure and probe the unchanged static mapping auditor. '
            'No application edit, passing runtime test, delegation, independent approval or external action is claimed. '
            'P4-B01 blocks mandatory created_at against the protected absent-C0 mapping. '
            'See `_agent_reports/P4-root.md`, implementation registers and `Part2/notes/P4_final_receipt.json`.\n')
    print(json.dumps(dict(G4='BLOCKED', checked=checked, unchecked=unchecked, counts=counts,
        protected_checked=len(initial['protected']), mismatches=mismatches), indent=2))


def final():
    head = git('rev-parse', 'HEAD')
    out = N / 'P4-root'
    out.mkdir(exist_ok=True)
    # Post-commit checker output is outside repo, avoiding an evidence-only commit loop.
    historical_receipt = N / 'P3-root' / f'design_crosscheck_{head[:7]}.json'
    assert not historical_receipt.exists(), 'Do not overwrite an existing same-commit receipt'
    command = [r'C:\Users\ADMIN\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe',
        '-X', 'utf8', '-I', str(D / '_scripts/p3_design_crosscheck.py'), '--commit', 'HEAD']
    before = datetime.now(timezone.utc).isoformat()
    run = subprocess.run(command, cwd=R, capture_output=True, text=True, encoding='utf-8', timeout=180)
    log = out / f'design_crosscheck_{head[:7]}.log'
    assert not log.exists()
    log.write_text(run.stdout + '\nSTDERR:\n' + run.stderr, encoding='utf-8')
    assert run.returncode == 0, run.stdout + run.stderr
    static = read(historical_receipt)
    assert static['audited_commit'] == head and static['pass'] and not static['incomplete_mode']
    initial = read(N / 'P4_start_hashes.json')
    executable_paths = ['saigonbite','tests','db','app.py','init_db.py','requirements.txt','pytest.ini']
    equivalence = {p: dict(baseline=git('rev-parse', initial['head'] + ':' + p),
                          final=git('rev-parse', head + ':' + p)) for p in executable_paths}
    assert all(v['baseline'] == v['final'] for v in equivalence.values())
    assert git('status', '--porcelain=v1') == '', 'Review unexpected derived change before closing'
    checklist = (P / 'codex/P4_CHECKLIST.md').read_text(encoding='utf-8')
    receipt = dict(author=AUTHOR, at_utc=datetime.now(timezone.utc).isoformat(),
        G4='BLOCKED', blocker='P4-B01: required created_at versus protected current-schema mapping gate',
        head=head, branch=git('branch','--show-current'), status=git('status','--porcelain=v1'),
        tested_code_revision=initial['head'], full_suite='NOT RUN', executed_test_cases=0, passing_tests=None, junit=None,
        baseline_collection=read(T / 'p4_baseline_collection.json'),
        counts=read(I / 'p4_counts.json'), executable_input_equivalence=equivalence,
        commits=git('log','--format=%H %s',initial['head']+'..HEAD').splitlines(),
        checklist=dict(checked=len(re.findall(r'- \[x\] P4-\d+',checklist)),
                       unchecked=len(re.findall(r'- \[ \] P4-\d+',checklist)), sha256=sha(P / 'codex/P4_CHECKLIST.md')),
        design_check=dict(command=command,cwd=str(R),started_at_utc=before,exit=run.returncode,
            audited_commit=head,evidence_label='Static',checks=static['checks'],failures=static['failures'],
            log=str(log),log_sha256=sha(log),receipt=str(historical_receipt),receipt_sha256=sha(historical_receipt)),
        oracle='NOT RUN',security='NOT RUN',race='NOT RUN',behavioral_coverage='NOT RUN',
        protected_manifest=read(N / 'P4_end_hash_check.json'),
        immutable_gate_files_match={p:sha(Path(p))==v for p,v in
            read(N / 'P4_preparation_receipt.json')['artifact_hashes'].items() if not p.endswith('P4_CHECKLIST.md')},
        report_sha256=sha(D / '_agent_reports/P4-root.md'),
        pending_items=read(I / 'P4_progress.json')['remaining_ids'],
        application_changed_files=[], all_changed_files=git('diff','--name-only',initial['head'],head).splitlines(),
        prompt_archived=str(N / 'P4_start_snapshots/Part2/codex/P4_PROMPT.md'),
        transcript='Unavailable through current task tools; no full transcript fabricated',
        workers=0,credits='UNAVAILABLE',no_new_upload_required=True,no_external_action=True,
        resume='Read implementation/P4_progress.json; obtain narrow mapping-boundary disposition; resume P4.1.')
    save(N / 'P4_final_receipt.json', receipt)
    print(json.dumps(dict(head=head,G4=receipt['G4'],checklist=receipt['checklist'],
                         static_checks=static['checks'],receipt=str(N / 'P4_final_receipt.json')),indent=2))


if __name__ == '__main__':
    {'prepare': prepare, 'final': final}[sys.argv[1]]()
