# Phase 2 root report

Author: 722I0004 · AI-assisted (Codex)

24/10/2026 (Asia/Bangkok). Scope: P2 analysis only. Starting clean branch `part2`, HEAD `657089b760e66585a52079ee44dbf8f336dbd694`. No app execution or correctness result is inferred from this phase.

## Sources read

Locked plan §§1–5, P2, P3.1, §§7/10/11; Part2 README, links and P2 checklist; Phase 1 Section I, traceability, rules, decision log and P1-root/brief; frozen Part 1 content and diagram style. Primary PDFs were extracted directly with pypdf; DOCX paragraphs and all tables read with python-docx (nine description fields, not just text extract); primary marking workbook Checklist and Rubric Guide; team template and working Team & Use Cases, Events Table, CRUD Check. Durable direct-source readings and controller AST inventory: `D:/RAD/FINAL/Part2/notes/P2_primary_sources.json`. Draft controllers, domain vocabulary/behaviour and schema v2 read only as Static evidence. PDF, Documents and Spreadsheets skills read; balanced-diagrams ZIP skill read, with Phase 1 generator patterns reused. No external information was needed.

## Preflight and stop rule

Baseline was clean before the preflight helper was created; the helper is the sole untracked preflight file in its captured status. Binary start hashes: `D:/RAD/FINAL/Part2/notes/P2_start_hashes.json`: Part1_v2 1,245 files (same interpreter-cache exclusion as P1), docs/part1 11, app 85, tests 12, db 4, entrypoints 2, plan/links 2, Section I 7. L1/L3/L6 in decision_log.md are planned/unanswered defaults, no differing lecturer answer; the stop rule is not triggered. The user explicitly orders P2 before P4.1 in this prompt; that order overrides the older P1 handoff without changing the locked plan.

## Plan issues

| Issue | Conservative handling / proposed clarification |
|---|---|
| Template has 3 actor CRUD subsections; plan requires 5 | Extend 2.3.1–2.3.5 for the five real actors, preserve the heading wording and record the extension here. |
| CRUD workbook marks each blank C/R/U/D as a gap; genuine per-actor rows have intentional blanks | Enter the 13-class union once with all four operation cells; Actor names all cell holders. Five per-actor tables remain in report 2.3. No formula change. |
| Plan P4.1 precedes P2 in old order / P1 handoff | Current owner prompt explicitly authorizes analysis first; describe contracts, list draft gaps for P4, do not edit app. |
| Plan L heading says asked 26/10, a future date on 24/10 | Preserve P1's truthful planned/unanswered interpretation. |
| Item 17 is per-student, all Part 2 work authored by Dat (J2) | Partial: met for 722I0004 only; absent for 523K0049 / 523K0050. No invented authorship or promised grade. |
| Template description table has no separate minimum-guarantee field | Keep its nine-field order; place MGs beside PCs within Post-conditions and branch outcomes within Exception conditions. |

## P4 inputs

All findings below are **Static**, read at G1 `657089b`, not tests or measured results. No code fix is made here.

| ID | Evidence | Contract / later action |
|---|---|---|
| F-01 | tests/conftest.py:74 queries obsolete delivery_fee_flat (plan finding, current file retained) | P4.1 repair fixture/import collection; no P2 test pass claimed. |
| F-02 | business/domain/models.py:265–267 release_for_unfulfilled_order changes state only | BR-17 requires ONLINE refund_amount=C in the same change, including after a partial refund obligation. P4.4. |
| F-03 | data_access/report_dao.py sales and report_controller.py SalesRow.net | BR-21: do not subtract refunds owed again from already reduced T. P4.8. |
| F-04 | business/domain/rules.py:58 returns rounded Haversine distance | BR-05/06: use raw distance for radius/fee before display/storage rounding. P4.3. |
| F-05 | kitchen_controller.py:111–138; order_tracking_controller.py:76–99 | Require currently unavailable source; recheck target listed/available/not archived; invalid target withdraws offer without changing order. P4.4. |
| F-06 | templates/order/detail.html refund wording (plan F-06) | State refund owed, not paid out; payout is deferred L3. P4.4. |
| F-07 | place_order_controller.py:86–119 compares quoted_total only | BR-10 requires full content fingerprint plus T; catalogue describes required input, not existing implementation. P4.3. |
| F-08 | db/migrations README / init_db.py old-version handling (plan F-08) | D-6 fresh v2 and explicit refusal of versions <2; do not claim a migration exists. P4.1. |
| F-09 | report_dao.py:top_items GROUP BY item_name | BR-24 group by menu_item_id, snapshot name shown. P4.8. |
| P2-S01 | enums.py PaymentState and schema payment CHECK include FAILED/REFUNDED; models.py PAYMENT_TRANSITIONS allows REFUND_PENDING→REFUNDED | Contract has no persisted declined attempt and no payout path. Depict REFUNDED grey future; P4 must exclude unsupported reachable behaviour. |
| P2-S02 | schema user_account lacks created_at | §5.3 requires created_at; record mapping gap for P3/P4. |
| P2-S03 | schema customer CHECK does not require nationality for TOURIST; AccountController validates it | BR-12/§5.3 type CHECK should support nationality requirement; preserve current layered validation evidence, strengthen later. |
| P2-S04 | schema comments refer to obsolete docs/part2/domain_model.md and A-12 for district coordinates | Documentation/assumption mapping cleanup in P4 code phase; actual A-14 is district approximation. |
| P2-S05 | place_order_controller.py try/except releases simulator reference for inserts, enclosing context commits after try | BR-14 includes COMMIT failure; audit release on commit failure explicitly in P4, not only insert failure. |
| P2-S06 | OrderArchiveController exposes batch archive(closed_before), not per-ID archiveClosedOrder; catalogue is contract-level | P3 confirms interface granularity and P4 ensures minimal archive/history path; do not invent a matching draft method. |

## Wave 0 catalogue

`ssd_operations.csv` contains the 12 exact §4 events and query/CRUD/support operations; `pc_mg_register.csv` contains all 30 P2.3 anchors with verbatim text. Candidate controller references are Static names; gaps are explicit. Shared brief freezes file ownership, notation and figure numbering before any worker starts. No extra PC/MG has been added.

## Marking evidence pointers

Primary `RAD_Sem01_2627_MarkingSheet.xlsx`: items 14–20 are physical Checklist rows 27–33. Rubric Guide row 8 holds P2-II Excellent. Evidence pointers and dispositions are completed at integration/review.
