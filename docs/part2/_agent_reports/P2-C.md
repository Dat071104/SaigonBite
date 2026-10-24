# P2-C — state machines completed

Author: 722I0004 · AI-assisted (Codex)

24/10/2026, Asia/Bangkok. Assigned Wave 1 C scope P2-20–24 is complete. Root-supplied wave baseline: `9404ec4`; the brief identifies the earlier Phase 1 closure `657089b`. No git command was run. No child was spawned. Writes were confined to the assigned stems, this report, `II_state_machines.md`, and `D:/RAD/FINAL/Part2/notes/P2-C/` scratch. No app, DB, tests, P1, Section I, shared contract, configuration or checklist was changed; no file was deleted.

## Files written

Each stem below has **`.py`, `.json`, `.drawio`, `.svg`, `.png`**. Base filenames hold part A when split. Base generators rebuild all their parts; each split part also has a standalone generator/data file. The shared renderer is the owned `sm_order.py`, adapting the read-only P1 proc_/business_process_v2 conventions (one geometry for XML/SVG, Arial measurement, hidden Edge rendering) and balanced-diagrams guidance. Native mxGraph edges retain source/target references and explicit port/waypoint geometry.

| Location | Stems | Figures |
|---|---|---|
| `models/shared/` | `sm_order`, `sm_order_PartB`, `sm_order_PartC`, `sm_order_PartD`, `sm_order_PartE` | 2.3A–E |
| `models/shared/` | `sm_payment`, `sm_payment_PartB` | 2.4A–B |
| `models/UC-02/` | `sm_delivery`, `sm_delivery_PartB` | 2.5A–B |
| `models/UC-03/` | `sm_hub` | 2.6 |
| `models/UC-05/` | `sm_replacement_offer`, `sm_replacement_offer_PartB` | 2.7A–B |
| `models/UC-06/` | `sm_catalogue`, `sm_catalogue_PartB`, `sm_catalogue_PartC`, `sm_catalogue_PartD` | 2.8A–D |
| `models/shared/` | `sm_user_account` | 2.9 |

Total: 17 figure views × 5 adjacent files = **85 model files**, plus `docs/part2/report/II_state_machines.md` and this report. No helper was written under another agent’s stem. Scratch contains `build_specs.py`, `write_report.py`, `qa_state_diagrams.py`, inventory, geometry/source-check logs, independent SVG review rasters, paired PNG/SVG visual sheets, A4 proof PDF and browser profiles. The delivered report source contains named BEGIN/END blocks for ORDER, PAYMENT, DELIVERY, HUB, REPLACEMENT_OFFER, CATALOGUE, USER_ACCOUNT and UC04_READ_ONLY, so root can inject each block under the appropriate iv subsection.

## Checklist evidence

| ID | Done | Evidence |
|---|---|---|
| P2-20 | Yes | Order 2.3A–E covers all twelve exact §4.1 events, all nine persisted states, four terminal states, ownership/hub/offer/cash guards and paired effects. Waiting for customer is a derived note. `state_diagrams_qa.json` records all twelve names. |
| P2-21 | Yes | COD/ONLINE separate 2.4A–B; no persisted declined-attempt state; partial owed is a PAID attribute; REFUNDED is grey with no incoming edge; full unfulfilled owed amount replaces partial owed. Delivery 2.5A–B pairs markReady/takeDelivery/confirmDelivered/reportFailure with Order/Payment facts. |
| P2-22 | Yes | Hub derived BUSY/QUIET notes; Brand and MenuItem ACTIVE→ARCHIVED; listing AVAILABLE↔SOLD_OUT/unlist; Offer terminal ACCEPTED/DECLINED/WITHDRAWN including invalid-target withdrawal; UserAccount ACTIVE↔INACTIVE, BR-25 and next-request session rejection. CRUD event names match the operation catalogue. |
| P2-23 | Yes | `II_state_machines.md` gives owning placement, exact author captions, export/source links and PC/MG→transition/stored-fact/refusal tables. All **30** registered main-UC anchors occur; 85 artifact links resolve. UC-04 explicitly reads facts and has no Report state. Cancellation is identified as SUC-04/BR-15/17 because P2.3 contains no dedicated cancellation PC. |
| P2-24 | Yes | Direct enum/SQL/dataclass comparison, representation table and Static P4 inputs in `II_state_machines.md`; all 17 PNG and all 17 SVG visual forms inspected. A4 landscape proof is 230 mm wide with **9.48 pt** minimum text. |

Evidence files outside repo: `D:/RAD/FINAL/Part2/notes/P2-C/state_diagrams_qa.json`, `report_checks.json`, `sm_*_qa.json`, `*_visual_pair.png`, `*_svg_review.png`, and `state_machine_A4_landscape_proofs.pdf`. Syntax parsing passes for all 17 adjacent generators. The seven main generators completed successfully; a split generator was also invoked directly. XML parses, every edge endpoint references an existing cell, geometry is orthogonal, node/label text fits, node/label overlaps and labels masking arcs are rejected by the renderer; initial nodes have exactly one outgoing edge, finals have none. The listing’s intermediate diamond is a transient choice, with complementary true/false guards, not an extra persisted state.

## Visual QA

Every exported PNG was opened as the left side of a full-width paired review sheet; every SVG was independently reopened in headless Edge at 1×, rasterized into scratch and opened on the right. All 17 pairs were inspected; changed routes/labels were reopened after correction. Inspection covered readable labels and author line, complete arrows, unambiguous terminal states, no clipped text, no white label masking of an arc and agreement between both visual forms. The SVG and PNG exports use 1100×760 logical geometry / 2200×1520 PNG pixels. Minimum font is 16 logical px: `16×230/25.4×72/1100 = 9.48 pt`.

The 17-page proof PDF uses A4 landscape and a 230 mm image width. This is a diagram-size proof, not a final assembled report. The draw.io XML was parsed and its editable cells/edges checked; it was **not** opened in native draw.io. No application test, UI correctness, measured report result or grade is claimed. Native report DOCX/PDF assembly remains root/later-phase work.

## Static P4 inputs

1. Order, Delivery and Offer persisted strings match the enum and SQL sets exactly. Hub/Brand/MenuItem lifecycle states are represented by nullable `archived_at`, listing availability by `is_available`, account activation by `is_active`; no artificial enums are needed.
2. Payment enum/SQL allow `FAILED` and `REFUNDED` beyond the current persisted lifecycle. `models.py` also permits `REFUND_PENDING→REFUNDED`. This is a permissive draft representation, not evidence that payout occurs; P4 must prove no declined Payment row/no current payout route and method-specific legality.
3. `Payment.release_for_unfulfilled_order()` changes state only and does not set `refund_amount=C` (Static F-02). P4 must correct/test full owed amounts, including cancellation after a partial amount.
4. Delivery SQL assignment/reason checks do not establish atomic paired Order/Payment changes, exact cash or timestamp behaviour. Those remain P4 obligations.
5. Offer SQL enforces one OFFERED/order but source-unavailable and target-still-valid guards are behavioural obligations (F-05). Withdrawal reason is shown to the user; there is no dedicated withdrawal-reason field in the draft offer, and no persisted reason history is claimed.
6. Plan §5.3 shorthand `available`/`active` maps to draft `is_available`/`is_active`. The plan also names UserAccount `created_at`, absent from the draft account dataclass/table. Retain these mapping differences for P3/P4.
7. Parent archive visibility, Hub no-open-order guard, BR-25 deactivation and next-request session checks need later behavioural verification. These models do not stand in for those tests.

## BLOCKED / ASSUMED

No blocking condition remains in the assigned workstream.

- Plan defaults remain team defaults, not lecturer/client approval; no new L1/L3/L6 answer was inferred.
- The requested initial/final convention conflicts with an account lifecycle that has reversible inactivity but no termination event. The UserAccount final is therefore explicitly **unreachable in Part 2**, labelled beside the symbol; no account deletion/end operation was invented. The Payment final likewise denotes the end of current modeled scope while a refund remains owed; payout is still unreachable.
- Cancellation uses existing catalogue operation `cancelOrder` and existing BR-15/17. Main-register checkout PCs describe the earlier creation boundary, not a claim that a later CANCELLED order remains PLACED/PENDING. No extra shared anchor was fabricated.
- ACTIVE/ARCHIVED, AVAILABLE/SOLD_OUT and ACTIVE/INACTIVE are analysis abstractions over the existing flags/timestamps, as allowed by P3’s cross-check rule.
- Withdrawal “reason” is an operation message under frozen §3.3 5; persisting a new reason field is not assumed.

## Requests to root

No new operation, state, PC/MG anchor or shared-contract change is requested. Integrate the named blocks once: Order/Payment under UC-01; Delivery UC-02; Hub + shared UserAccount UC-03; UC-04 cross-reference only; Offer UC-05 with Order cross-reference; Catalogue UC-06. Preserve 230 mm landscape placement; 170 mm portrait would reduce 16 px text to 7.01 pt. Carry the Static inputs above into the P4 list. Authorship remains 722I0004 for all seven machines; checklist item 17 remains a team **Partial** under J2, not a claim for either other student.

## Sources used

- First read: `docs/part2/_agent_reports/P2-brief.md`.
- Locked `PLAN_SaigonBite_Part2_Final.md` §§1–5, P2/P3.1, §§7/10/11; `Part2/README.md`, `Part2/content/links.json`, `Part2/codex/P2_CHECKLIST.md`.
- Primary direct reads in `Lec_re/`: report-template §2.2 and use-case table pre/postcondition rows; Requirements PDF state-machine/authorship/postcondition provisions; marking workbook Checklist item 17 and Rubric Guide P2-II; team workbook Team & Use Cases / Events Table / CRUD Check headings; Case Study PDF known lifecycle facts. `Part2/notes/P2_primary_sources.json` and `Part2_Plan_Review/source_evidence/` were supporting extracts, not substituted for primary authority.
- Read-only frozen `Part1_v2/content/content_master.md`, model/process source conventions, `build/proc_build.py`, `proc_geom.py`, `proc_views.py`, and `notes/diagram_changes.md`; repo P1 `models/shared/business_process_v2.py` pipeline.
- ZIP `balanced-diagrams.skill.txt`, actual member `balanced-diagrams/SKILL.md`; balanced landscape pages and split views were used instead of shrinking labels.
- Frozen `docs/part2/rules.md`, `decision_log.md`, `ssd_operations.csv`, `pc_mg_register.csv`.
- Static draft reads: `db/schema.sql`, `saigonbite/business/domain/enums.py`, `saigonbite/business/domain/models.py`. Source SHA-256 values are retained in scratch QA JSON.
