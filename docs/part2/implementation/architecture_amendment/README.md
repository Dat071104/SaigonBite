# SB-P4-B02-20261026 — current P4 dependency overlay

Author: 722I0004 · AI-assisted (Codex). Adopted 26 October 2026, Asia/Bangkok, by the owner's actual continuation message. Team decision; no lecturer/client approval.

`policy.json` is the exact pair/symbol/member/use authority. `dependency_overlay.json` binds the untouched P3 model hash and affected frozen declarations. This is an overlay, not a duplicate class model. `active_disposition.csv`, `symbol_use_review.json` and `runtime_use_review.json` record retained dependencies, 101 imported-name uses and reviewed mapper method/property/serialization contexts. Counts are observations, never the compliance rule. `source_hashes.json` contains binary source hashes at adoption; the audit also reports normalized source-text hashes.

Run with the project Python from the repository:

```powershell
& '.venv\Scripts\python.exe' -X utf8 -I 'docs/part2/_scripts/p4_dependency_policy_audit.py'
& '.venv\Scripts\python.exe' -m pytest tests/test_p4_dependency_policy.py -q
```

The audit defaults to nonwriting mode and imports no application code. `--output NEW_PATH` explicitly saves a new receipt and refuses overwrite. It parses every actual application Python file plus `app.py`; unknown modules/use bodies fail closed. Exact full-application dependency-set equality is required; mutation fixtures use subset permission only for explicitly reviewed valid examples. Re-exports resolve to effective definitions. The named controller presentation facade and report error export are explicit reviewed contracts; a new export is not automatically allowed. Bootstrap imports are exact records. Cross-role cycles exclude bootstrap assembly, which is independently sealed and restricted.

`reviewed_scope.json` is a fixed manual review record. AST seals bind reviewed code; they are not permission to regenerate the record after arbitrary changes. Constructors/factories/enum conversions are runtime uses; instance serialization/property reads are documented in the method ledger. New semantics, imports, symbols, reflective constructs or bodies require a fresh explicit disposition. The validator conservatively rejects harmless unreviewed edits too. It does not infer arbitrary Python runtime behavior or prove all possible dynamic execution. Controllers retain authorization, state checks, orchestration and transaction ownership; the reviewed database context implements the caller's transaction.

`package_4_2A.py` reads policy and actual adoption audit, reuses the original P3 PIL/SVG/mxGraph renderer, and exports editable `.drawio`/`.json` plus `.svg`/`.png`. Its 1800×1360 layered layout follows the installed balanced-diagrams workflow. Figure 4.2A is a named current P4 projection. The C0 package graph is historical; frozen DCDs describe scoped declarations/responsibility slices rather than a complete current dependency graph. All original models remain unchanged. Native draw.io editing is UNTESTED. Both the PNG and separately rasterized SVG were visually inspected; see `visual_review.json`.

The historical strict audit, original known-12 test and BLOCKED receipt/report stay unchanged. The legacy P3 checker accounts for 28 strict-direction import findings at the current application; its PASS means Static consistency, not adoption of this policy. The active audit supplies separate current-policy evidence. Final test/revision/G4 facts are in `Part2/notes/P4_B02_final_receipt.json`. No P5 execution, upload, remote action or release is included.
