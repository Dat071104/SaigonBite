# P4 execution brief

Author: 722I0004 · AI-assisted (Codex)

Client date: 26 October 2026, Asia/Bangkok. Mode: sequential root execution, workers=0. No helper batch is needed for the immediate shared-schema dependency. Root owns source, tests, fixtures, schema, integration, evidence and Git; no other writer is assigned.

## Authority and baseline

- Controlling prompt: `D:/RAD/FINAL/Part2/codex/P4_PROMPT.md`; SHA-256 `d389194ef82880a0f7c62af293d82b04d5ea7d449687d3c65aa2bb495d1def4b`. The attached prompt has exactly the same bytes.
- Locked plan: `D:/RAD/FINAL/PLAN_SaigonBite_Part2_Final.md`; SHA-256 `cbadf1c3833fecba16769d9036cb4ebfe1e563f845379ab3559dbe6f990790f3`, verified before reading.
- Branch `part2`, initially clean HEAD `6e8cafe245c87d3aab7f99535960ad5d7111d320`, matching the preparation and P3 receipts. No earlier P4 run was found.
- Preparation prompt/review/checklist hashes were verified. Original bytes, schema, mapping, checker, traceability and derived consistency are in `D:/RAD/FINAL/Part2/notes/P4_start_snapshots/`. Do not regenerate this snapshot on resume.
- Original P3 independent review remains NOT READY at its reviewed revision. Later root design assessment and this entry investigation supply no independent runtime approval.

## Sources and implementation boundaries

Current prompt/checklist/advisor review, plan, decision log, workspace README/links, rules, SUC contracts, six UC descriptions, P2/P3 findings, frozen registers and the parser/checker/mapping were inspected for entry and blocker analysis. Full P4 source-review and implementation gates are incomplete. No uncompleted reading obligation is marked complete.

The decision log supplies no new L1–L6 or Q1–Q5 answers. Locked defaults apply; no presentation, approval, submitted date or official deadline is inferred from today's date. The 31 October checkpoint remains pending, and answered/closed Q1–Q5 still consume all five client slots. The old 92–130-hour baseline exceeds 84 available hours; no new completion schedule is claimed.

Allowed application scope is the prompt's application/tests/schema paths. P4 tooling/reports/registers are confined to `docs/part2/{_scripts/p4_*,_agent_reports/P4-*,implementation/,test_report/}`. Existing history, models, mapping, design sources, workbooks, staging, database files and their sidecars remain protected. Existing DB files are byte-hashed only, never opened as SQLite. No credentials are printed or read.

Use existing `.venv/Scripts/python.exe` (Python 3.13.2; checked package versions recorded in `test_report/p4_environment.log`). Bundled Python is 3.12.14 and lacks Flask, so do not infer application compatibility from its availability. The unchanged static checker uses the prompt's bundled interpreter.

Collection command, before F-01 repair:

```powershell
& 'D:/RAD/FINAL/SaigonBite/.venv/Scripts/python.exe' -m pytest --collect-only --basetemp=D:/RAD/FINAL/Part2/notes/P4_test_scratch/baseline_pytest
```

Environment: `SAIGONBITE_DATABASE` points to a new unused sentinel under P4 scratch, `SAIGONBITE_ENV=testing`, plugin autoload disabled, bytecode writes disabled. The original import-time fixture uses only its own in-memory SQLite database. No passing baseline is presumed.

Static gate after every new P4 commit:

```powershell
& 'C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -I 'D:/RAD/FINAL/SaigonBite/docs/part2/_scripts/p3_design_crosscheck.py' --commit HEAD
```

Do not overwrite a same-commit receipt, change the checker, or use incomplete mode. The design gate is Static and cannot establish runtime correctness.

## Immediate dependency

P4-B01 is a compatibility conflict between mandatory P4.1 `created_at` and the protected P3 mapping/checker. `p4_preflight.py` calls the actual frozen parser and `audit_mapping` on both actual schema and a minimally changed in-memory candidate. The candidate has one additional required column; no application file or database is modified. Preserve the resulting JSON and stop dependent writes if its failure is confirmed. Resume this run after a narrow owner disposition of the protected mapping boundary; do not restart or proceed to P4.2/P5.
