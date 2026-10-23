# Phase 1 shared brief

Author: 722I0004 · AI-assisted (Codex)

Date: 23/10/2026. Repo: D:/RAD/FINAL/SaigonBite; branch part2; WIP 4b0103c. Only P0/P1 is authorized. No application changes, git by workers, pushes, tags, external actions or Part 1 writes. Artifacts in English. The locked plan governs; checklist adds evidence detail. Defaults are not approval.

Continuation: existing drafts were preserved in Part2/notes/P1_resume_existing_drafts.zip. The existing start manifest was rechecked successfully: zero changes in all frozen boundaries. Continue and verify your owned drafts rather than replacing correct content. Root will read none of this wave's reports until all four workers have finished. Use only the assigned model/effort; no further delegation. Actual runtime models are logged by root. No `_agent_ops/` exists in this target repository; the phase records provide its task and closure evidence.

## Authorities and vocabulary

Read D:/RAD/FINAL/PLAN_SaigonBite_Part2_Final.md, Part2/README.md, Part2/content/links.json, Part2/codex/P1_CHECKLIST.md and relevant primary authorities in Lec_re/. Convenience text: Part2_Plan_Review/source_evidence/. Part1_v2/content/content_master.md, models and build/proc_*.py are read-only. Diagram skill is a ZIP despite its .txt suffix: D:/RAD/FINAL/balanced-diagrams.skill.txt contains balanced-diagrams/SKILL.md and scripts/layout_drawio.py. Read with zipfile; use/adapt the layout helper without writing Part 1.

Main UC names/goals: UC-01 Place an order with an accepted full price, voucher and payment choice; UC-02 Deliver an order: pick up, deliver with cash collection, or report failure; UC-03 Maintain hubs and kitchen capacity; UC-04 Produce management reports: sales, workload, delivery performance; UC-05 Decide an incoming order: confirm, reject, or offer a replacement the customer agrees to; UC-06 Maintain brands, menu items and hub listings. Proposal owners: 01/03 Dat 722I0004; 02/04 Le Minh Quan 523K0049; 05/06 Nguyen Minh Quan 523K0050. Actual Part 2 author for ALL is 722I0004 (J2).

SUC-01 Log in / log out; SUC-02 Register (local or tourist), edit profile, manage addresses; SUC-03 Track my orders, view receipt, answer a replacement offer; SUC-04 Cancel an order (PLACED or CONFIRMED); SUC-05 Start preparing and mark ready; SUC-06 Set menu availability at my hub; SUC-07 Maintain vouchers; SUC-08 Maintain user accounts; deactivate/reactivate; SUC-09 Archive closed orders; read archived history.

Actors: Customer (Local / Tourist), Kitchen staff, Shipper, Admin, Manager, System; Payment simulator if shown. Stakeholders also include owner/management, hub managers and external payment provider (provider is contextual, simulated in this release).

Order: PLACED, CONFIRMED, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, REJECTED, CANCELLED. Delivery: AWAITING_PICKUP, PICKED_UP, DELIVERED, FAILED. Payment: COD PENDING → PAID / VOIDED; ONLINE PAID → REFUND_PENDING. Partial refund owed is an attribute while PAID; no payout or REFUNDED path. ReplacementOffer: OFFERED → ACCEPTED / DECLINED / WITHDRAWN. Hub/Brand/MenuItem ACTIVE → ARCHIVED; listing AVAILABLE ↔ SOLD_OUT; UserAccount ACTIVE ↔ INACTIVE. Waiting for customer and busy/quiet are derived, never stored states.

BR-01…BR-26: docs/part2/rules.md (plan §3 authoritative). A-01…A-11 preserve Part 1 wording with explicit current interpretation; A-08 superseded by D-4 (23/10, team decision). A-12 quiet figures, A-13 alternative hubs, A-14 district centroid/radius, A-15 fee, A-16 voucher/money, A-17 consent fingerprint, A-18 tourist validation/privacy, A-19 receipt. Q1–Q5 are Submitted in frozen workbook, answer/date cells empty, submitted dates unknown; all five slots consumed. L1–L6 planned course clarifications for 26/10, no answers yet. Checkpoint 31/10.

## Output conventions and write ownership

Every report section and diagram caption: `Author: 722I0004 · AI-assisted (Codex)`. For process captions also retain the checklist's `AI-assisted (Codex/Sol 6.1)` wording if required, without claiming a runtime model. Pending marker: `⟦PENDING: what, expected when⟧`; keep the explicitly requested `⟦PENDING: feedback 26/10⟧` where relevant. Do not invent work dates, approvals, performance or member contributions. Targets and schedule bars are planned, not measured. Retain exact template headings (including its stale 1 point label); actual rubric is 5 marks.

| Worker | Exclusive write set |
|---|---|
| A | docs/part2/report/I_1-1_vision.md; I_1-2_org_gantt.md; I_1-3_iterations_backlog_risks.md; models/shared/stakeholder_chart.*; gantt.*; docs/part2/_agent_reports/P1-A.md |
| B | docs/part2/report/I_1-4_narrative_assumptions.md; docs/part2/_agent_reports/P1-B.md |
| C | models/shared/business_process_v2.* and business_process_v2_Part*; models/shared/swimlane_v2.* and swimlane_v2_Part*; docs/part2/report/I_1-5_1-6_process.md; docs/part2/_agent_reports/P1-C.md |
| D | docs/part2/report/I_1-7_requirements.md; docs/part2/traceability.csv; docs/part2/_agent_reports/P1-D.md |
| Root | all other phase records, assembly, workbook, staging, checklist, git; no active worker write set |

Use bundled Python C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe, with -I for scripts; stdout UTF-8. No visible background console. Inspect every PNG/SVG export visually before claiming completion; process detail may be split across A4 pages to keep ≥9pt. Never run original Part 1 builders (their output paths point into the frozen tree).
