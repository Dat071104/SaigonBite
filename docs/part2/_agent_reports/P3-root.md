# Phase 3 root report

Author: 722I0004 · AI-assisted (Codex)

25/10/2026, Asia/Bangkok. Scope: target design only, Section III and IV 4.1–4.3.2. No application import, execution, tests or runtime qualification. All code observations are **Static**.

## Sources read

Locked plan §§1–5, P3/P4/P5/P7, §§7.3/10–12; Part2 README, links, Phase 3 prompt/checklist; primary Requirements and Case Study PDFs directly extracted with pypdf, template paragraphs/tables with python-docx, marking and team-template cells with openpyxl. Direct extracts: `D:/RAD/FINAL/Part2/notes/P3_primary_sources.json`. Documents/PDF/Spreadsheets skills and supplied balanced-diagrams ZIP skill read. Frozen Part 1 content/style and P2 renderer patterns are read-only references. P2-root/review/brief, registers/ledgers, six descriptions, assembled II, traceability, models and AST facts are design inputs; no web source or newer library assumption is needed.

## Wave 0 and baseline

The repo was clean on `part2` before creating the preflight helper. C0 is **45ac76221b0a103174c7c01d17577e6e49cfd665**; no committed app changes since G2 and no uncommitted app changes. Start manifest `Part2/notes/P3_start_hashes.json` protects 1,730 files, including Part 1, application/tests/schema/entrypoints, plan/links, workbook working/staged bytes, sections I/II and all pre-existing model bytes plus P2 descriptions/registers/ledgers. New Phase 3 stems are allowed; traceability and AI log are explicitly mutable Phase 3 integration outputs. No differing lecturer answer to L1/L3/L6 is recorded; defaults remain unanswered and the stop rule does not fire.

`p3_code_inventory.py C0` inventories 48 modules, 83 classes, 63 route records and 13 tables using Git committed blobs + AST/SQL parsing. It never imports application code. `operation_realisation.csv` preserves all 41 SSD occurrences. `p3_seed_design.py` records explicit mappings/targets; `p3_design_model.py` builds the single shared source, including blueprint/module roles and per-element statuses. MATCH means static correspondence only. Target signatures are not silently presented as existing code. Shared transaction/rowcount defects propagate to affected write operations.

## Plan issues

| Issue | Conservative resolution / proposed clarification |
|---|---|
| Prompt counts 41 rows but per-UC distinct-name counts sum to 39 | Frozen `ssd_flow_membership.csv` has 41 occurrences / 39 distinct UC-operation pairs / 38 op IDs. UC-06 listCatalogue repeats in Parts A/B/C: 12 occurrences, 10 names. Preserve all 41 rows and sequence views, with their exact source pointers; never alter P2. |
| G3 says diagrams match code; P3 prompt explicitly permits target design before P4 | Every element is MATCH, P4-TARGET or GAP at C0; G3 is design readiness with disclosed P4 obligations, not implementation completion. Future cross-check retains behavioral targets until evidence clears them. |
| Existing domain dataclasses carry scalar relation IDs; B5 prohibits domain FK attributes on DCDs | Keep exact scalars in inventory/class-to-table mapping; project them to associations/multiplicities in diagrams, with omission stated. No fabricated domain attributes/methods. |
| L heading in locked plan is future-dated; trace status has no Designed value | Preserve truthful planned/unanswered L records. At integration retain Analysed for design-linked main rows and do not fabricate a new trace status. |
| 4.3.4 SQL / full item 24 and P2-IV completion are outside P3 | Supply mapping/design evidence only. Explicit P7 SQL/source and P5 UI/integration placeholders; no full implementation/rubric score claimed. |

## Additional Static P4 findings

| ID | Evidence at C0 | Required design / subphase |
|---|---|---|
| P3-S01 | PlaceOrderController.suggest_hubs sorts `(load/capacity, id)` | BR-04 requires `(load/capacity, raw distance, id)`; F-04 also covers raw range. P4.3. |
| P3-S02 | HubController.list_hubs has only user_id and always list_all | Honor optional includeArchived in OP-23 with default True; no removal of retained history. P4.2. |
| P3-S03 | Several controller mutation calls discard boolean DAO results; shared transaction helper omits COMMIT-error rollback | Conditional-save rowcount outcomes and controlled busy/commit failure are design targets in P4.1 and the affected UC subphase. P2-S13 remains the shared COMMIT finding. |

## Shared mapping decisions

- P2-S06: propose minimal per-ID `OrderArchiveController.archive_order(user_id, order_id)` and conditional `OrderDAO.archive_one(order_id, now)` as GAP; retain separately named existing batch archive. SUC-09 stays supporting scope.
- P2-S14: propose one `MenuController.list_catalogue(user_id, hub_id=None)` wrapper (GAP) over the real catalogue/hub-menu/all-hub readers; preserve one SSD op and three UC-06 occurrences.
- P2-S15: `list_item_at_hub(..., available=True)` and `MenuDAO.add_listing(..., available=True)` insert initial availability atomically; no briefly orderable intermediate listing.
- P2-S16: updateMenuItem.brandId is current-parent form context; draft update_item pins current.brand_id. No reparenting or restore operation is proposed.
- P2-S18: workload_report uses all retained hub identities, archived hubs with no open work included.
- P2-S08: PaymentDAO.insert maps updated_at to the supplied value or created_at; optional Python typing is not a missing SQL value or demonstrated failure.

## Wave 1 integration

⟦PENDING: read all four completed reports together, apply and record every request, regenerate affected model views, then commit six UC packages and architecture/mapping⟧.

## Wave 2 / Wave 3 integration

⟦PENDING: complete E/F barrier, integrate subsystem/DAO design, rerun full cross-check and assemble reports⟧.

## Wave 4 independent review

⟦PENDING: sole read-only review, root dispositions, cross-check and integrity/staging closure⟧.

## Marking evidence pointers

Fresh primary marking workbook: items 20–24 at physical Checklist rows 33–37; Part 3 item 33 at row 47. P2-III Excellent is Rubric Guide row 9; P2-IV row 10. Final pointers and scope limits follow integration.

## P4 design inputs

The element-specific register is `docs/part2/design/design_annotations.json` (P4_inputs), joined to SSD op IDs in `operation_realisation.csv`. Existing F-01…09 and P2-S01…18 remain P2-root inputs; design additions P3-S01…03 above do not imply execution. Final handoff CSV and exact rerun command follow closure.

## Pending owner facts and limits

⟦PENDING: actual L1–L6 answers/unanswered records, discussion planned 26/10 and checkpoint 31/10⟧; ⟦PENDING: Q1–Q5 original submission dates and answers, Dat by 31/10⟧; ⟦PENDING: real feedback/approval and official Part 2 deadline, when received/slot opens⟧. Native draw.io editing, native Excel and final DOCX/PDF placement are UNTESTED. No external upload/push/tag/merge is authorized. Next prompt is P4.1 unless P4 has already started.
