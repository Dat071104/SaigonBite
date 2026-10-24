# Phase 2 Wave 2 F — UC-02 and UC-04

Author: 722I0004 · AI-assisted (Codex)

Completed 24/10/2026, Asia/Bangkok. Scope: P2-36–40 and P2-46–50 only. English analysis artifacts; no application execution, test result, database change, shared-contract change, git command or additional agent. The updated P2 brief and root's finalized Wave 1 dispositions were read first. Existing state/domain/UC/CRUD artifacts were read-only.

## Files written

All repository writes are in the assigned allowlist (50 files including this report):

- `docs/part2/UC-02/description.md`; `docs/part2/UC-04/description.md`.
- `docs/part2/report/II_2-2-2_UC-02.md`; `docs/part2/report/II_2-2-4_UC-04.md`.
- `models/UC-02/activity_uc02_PartA.*`, `_PartB.*`, `_PartC.*` — each has `.drawio`, `.png`, `.svg`, `.py`, `.json`.
- `models/UC-02/ssd_uc02_PartA.*`, `_PartB.*` — same five formats.
- `models/UC-04/activity_uc04_PartA.*`, `_PartB.*`, `_PartC.*` — same five formats.
- `models/UC-04/ssd_uc04.*` — same five formats.
- `docs/part2/_agent_reports/P2-F.md`.

Scratch is exclusively `D:/RAD/FINAL/Part2/notes/P2-F/`. `ssd_uc04_manifest.json` records path + SHA-256 for the 49 package files other than this completion report. `activity_uc02_build.py` is the owned renderer adapted from the read-only Phase 1/State renderer primitives; each adjacent generator is a self-contained copy that writes only its named page. `activity_uc02_sources.py`, `ssd_uc04_qa.py`, `ssd_uc04_verify.py` are owned helpers. No shared generator was edited.

## Checklist evidence

| ID | Status | Concrete evidence |
|---|---|---|
| P2-36 | Done | UC-02 description: nine template fields in exact order; six numbered Actor/System steps; A01–04 and E01–06 branch/rejoin/end; four verbatim register anchors. |
| P2-37 | Done | Figure 2.12A–C: pickup, exclusive success and failure episodes; Actor/System partitions; guarded validation and operation outcome; alternatives merge before final. |
| P2-38 | Done | Figure 2.13A–B: five catalogue messages only; parameters, Shipper + :System, dashed returns, loop/opt and exclusive alt. |
| P2-39 | Done | Report 2.2.2 uses the exact i–iv headings, one description include, figures/captions, Delivery ownership and shared Order/Payment references, four anchor→fact rows. |
| P2-40 | Done | Trace tables below and `ssd_uc04_verification.json`; visual QA below. |
| P2-46 | Done | UC-04 description: nine exact fields; numbered sales flow; workload/performance/empty alternatives; explicit denied/invalid/read-unavailable exceptions; four verbatim anchors. |
| P2-47 | Done | Figure 2.16A–C: separately initiated sales/workload/performance; complete complementary guards and explicit merge/final; no persistent Report. |
| P2-48 | Done | Figure 2.17: Manager + :System; OP-26/27/28 only; loop over independently authorized requests, nested alt, parameters and dashed returns. |
| P2-49 | Done | Report 2.2.4: exact i–iv; include directive; explains zero own states and reads existing Order/Delivery/Payment/Hub figures. |
| P2-50 | Done | Eight total anchor mappings, eight SSD request mappings, XML/guard/field/register checks, nine final PNG and nine independently rendered SVG inspections. |

## PC/MG → description / activity / SSD / retained fact

Activity IDs are local to the named page. SSD IDs are UC-local. These rows are ready for the root's `analysis_consistency.csv`; anchor wording is retained verbatim in each description's Post-conditions.

| Anchor | Description step | Activity reference | SSD reference | Transition / stored fact |
|---|---|---|---|---|
| UC02-PC01 | 3 | activity_uc02_PartA:S_effect; D_valid; D_commit[yes] | ssd_uc02_PartA:M03 `takeDelivery` accepted return | Delivery AWAITING_PICKUP→PICKED_UP, one shipper, picked_up_at; Order READY→OUT_FOR_DELIVERY; state Figures 2.5A / 2.3D. |
| UC02-PC02 | 5; A01; 6 | activity_uc02_PartB:S_effect; D_valid; D_commit[yes]; A_result | ssd_uc02_PartB:M04 `confirmDelivered` accepted return | Delivery/Order DELIVERED; finished_at/closed_at; exact COD cash=T/PAID; ONLINE remains PAID/C/partial owed; 2.5B/2.3E/2.4A–B. |
| UC02-PC03 | A02; 6 | activity_uc02_PartC:S_effect; D_valid; D_commit[yes]; A_result | ssd_uc02_PartB:M05 `reportFailure` accepted return | FAILED + failure_reason and DELIVERY_FAILED; times; COD VOIDED or ONLINE REFUND_PENDING + refund_amount=C replacing partial; same state references. |
| UC02-MG01 | A04; E01–06 | activity_uc02_PartA/B/C:S_refuse, S_rollback; D_valid[invalid], D_commit[no], M_end | ssd_uc02_PartA:M01/M02 read-only/refusal, M03 refusal; PartB:M04/M05 refusal | No transition / zero rows changed for refused, lost, wrong, stale, repeated or failed commands. Prior commit preserved. Empty query is read-only. |
| UC04-PC01 | 2–4; A01; A02 | activity_uc04_PartA/B/C:S_effect; D_commit[yes]; A_result | ssd_uc04:M01 salesReport; M02 workloadReport; M03 deliveryReport | Reads source state/totals/times; same-filter oracle equality is required expected behaviour only. Order 2.3, Payment 2.4, Delivery 2.5, Hub 2.6; zero report transitions. |
| UC04-PC02 | A02/A03 | activity_uc04_PartC:A_result; N | ssd_uc04:M03 `waitRideFailureRatesWithNAndNA` (empty sample outcome) | Computed n/a with N=0 on zero metric denominator; no Report state. |
| UC04-MG01 | Post-conditions; 2–5; A01–03; E01–03 | activity_uc04_PartA/B/C:S_effect, S_refuse, S_rollback, A_result, M_end | ssd_uc04:M01/M02/M03, all returns | Zero inserts/updates/deletes/archive writes, including empty/refused/failed requests. |
| UC04-MG02 | Pre-conditions; E01 | activity_uc04_PartA/B/C:D_valid[invalid], S_refuse | ssd_uc04:M01/M02/M03 `denied` | Active Manager role guard before disclosure; non-manager denied; no lifecycle transition. |

## SSD request / query membership

| UC / SSD ID | Catalogue | Exact operation signature | Description membership | Activity membership |
|---|---|---|---|---|
| UC02 M01 | OP-21 | viewReadyDeliveries() | 1; 4; A03/A04 | PartA:A_request/N; PartB:N resume reference |
| UC02 M02 | OP-22 | viewDelivery(orderId) | 2; 4; A03 | PartA:A_request/N; PartB:N resume reference |
| UC02 M03 | OP-10 | takeDelivery(orderId) | 3 | PartA:A_request/S_effect |
| UC02 M04 | OP-11 | confirmDelivered(orderId, cashCollected?) | 5 COD; A01 ONLINE | PartB:A_request/D_valid/S_effect |
| UC02 M05 | OP-12 | reportFailure(orderId, reason) | A02 | PartC:A_request/D_valid/S_effect |
| UC04 M01 | OP-26 | salesReport(startDateVN, endDateVN, hubId?) | 2–4 | PartA:A_request/S_effect |
| UC04 M02 | OP-27 | workloadReport() | A01 | PartB:A_request/S_effect |
| UC04 M03 | OP-28 | deliveryReport(startDateVN, endDateVN, hubId?) | A02/A03 | PartC:A_request/S_effect/A_result |

No message authorizes an internal controller, DAO, SQL statement or widget. Actor identity is implicit authenticated context, not a trusted posted shipper/manager ID. No new operation, event, anchor, CRUD grant or persistent class is requested.

## Semantic self-check

- UC-02 retains BR-25: any active shipper may take any READY order, concurrent assignments allowed; one atomic claim winner; only the assigned active shipper finishes. Wrong cash/shipper/repeat changes zero rows. ONLINE is already paid and collects no cash. BR-17 failure sets full owed C, replacing partial, with paired states/times. BR-12 excludes passport from shipper views/logs and uses the address snapshot.
- UC-04 retains BR-20–24: inclusive Vietnam dates become a UTC half-open interval; sales are DELIVERED by finish, separate S/D/net fees/T/refunds owed, no second subtraction; workload is now and has no date/hub parameter; wait/ride/failure formulas and separate Ns/n/a are explicit; archive retained, order sums have no line join, items group by ID. Manager alone is authorized and requests write zero rows.
- UC-04's PC01 is a target for later independent verification. No hand-oracle equality, application pass count or scientific result is claimed. No numeric illustrative data set was introduced.
- Figure 2.1's actual relations are used: neither UC-02 nor UC-04 has an include/extend. Support dependencies are labelled serving/data references.

## Visual and structural QA

`ssd_uc04_verification.json`: passed two nine-field-order checks, eight verbatim anchors, eight catalogue-and-description request memberships, nine parseable XML sources with connected source/target IDs and all six activities' complementary decision guards/final checks. Six activity diagrams have 11 connected edges each; SSDs have 6, 4 and 6 message/return edges. No text overflow was reported by font measurements. These are artifact checks, not application tests.

Final render size: logical 1100×900, PNG 2200×1800, Arial minimum 18 logical px. At the **required 230 mm A4 landscape placement**, the minimum is **10.67 pt**. Do not shrink to 170 mm. `activity_uc02_A4_proofs.pdf` contains all 18 PNG/SVG-render proof pages at that width.

Opened and inspected all nine final repository PNGs and all nine independently Edge-rendered SVG views (Pillow PNG renderer versus Microsoft Edge SVG renderer). Checked lane ownership, text fit, diamond labels, arrow routing, merge/final placement, SSD lifelines, fragment operand separators and dashed returns. Initial diamond/fragment layout issues were corrected and final views reopened. No native draw.io GUI validation was performed. XML parses and connected edges are verified; this is not a claim of native application correctness.

`ssd_uc04_qa.json` lists every independent SVG render, exit code and proof path; each `<stem>_edge.log`, `<stem>_svg.png`, original PNG review image and SVG review image is retained in scratch. Edge used hidden, no-console subprocesses and dedicated scratch profiles. No existing jobs were stopped.

## BLOCKED / ASSUMED

- No workstream blocker. Q5 and L3 defaults remain unanswered assumptions, consistent with the locked plan and root brief; no approval is invented.
- Pickup and terminal delivery are separate activity episodes; Parts B/C start from an own PICKED_UP assignment and are exclusive alternatives. Finals end the pictured episode. Query browsing/empty-board details are retained in Part A's action/note and the full description/SSD, rather than inventing another operation.
- “Operation succeeds?” distinguishes a committed command / completed read from atomic-save/read failure. Read-unavailable handling is a conservative exception with zero writes and no fabricated numbers, not a new catalogue operation.
- Workload uses active operational hubs, consistent with the read-only draft and archived-hub guard; historical sales/performance still include archived records. Archived closed orders cannot add to current cooking/READY/out-for-delivery counts.
- Static controller/schema reading informs names only. Known root P4 F-02/F-03/F-09 remain future behaviour obligations; this package does not fix or measure them.

## Requests to root

1. Insert C's existing `STATE_MACHINE DELIVERY` block once under UC-02 iv during assembly, preserving Figures 2.5A–B; retain the shared Order/Payment cross-references. UC-04 already supplies a complete zero-own-state explanation and anchor table; do not duplicate a fake Report machine.
2. Place all nine figures at 230 mm landscape. Activities are three-view episodes (A/B/C); SSD UC-02 is A/B and UC-04 is unsuffixed. The report references only the actual split files, with no incomplete overview alias.
3. Accept the conservative read-unavailable E03 as generic exception handling within the existing report operations; no new catalogue operation or result shape is required. If the integration catalogue needs an explicit technical-error note, root owns that note.

## Sources used

Controlling: updated `P2-brief.md` and `P2-root.md` Wave 1 dispositions; locked `PLAN_SaigonBite_Part2_Final.md` §§1–5, P2/P3.1, §7/10/11; Part2 README, links and P2 checklist; rules, decision log, PC/MG register and SSD catalogue.

Primary-source readings: `Part2/notes/P2_primary_sources.json` directly supplies extracted primary requirements/case PDF pages, all report-template tables (the nine-field use-case table), marking workbook and team-template sheet values. The case source was also read from its convenience text under `Part2_Plan_Review/source_evidence/`. These are requirements/marking sources, not evidence that a future app meets them.

Frozen reference: Part1_v2 content master, proc geometry conventions and diagram_changes; Phase 1/shared `sm_order.py` primitives. Wave 1 `II_2-1-6_2-1-7_models.md`, domain/UC vocabulary and `II_state_machines.md` supply relations/state ownership; these files were not edited. Balanced-diagrams was read directly from ZIP member `balanced-diagrams/SKILL.md`; readable views were split instead of shrinking the font.

Static-only reads: delivery_controller.py, report_controller.py, business/domain/enums.py and db/schema.sql. The plan/root contract governs behaviour, not the current draft. All author labels are the exact `Author: 722I0004 · AI-assisted (Codex)`.
