# Phase 2 shared analysis brief

Author: 722I0004 · AI-assisted (Codex)

24/10/2026, Asia/Bangkok. Root executes P2 only on `part2`, starting `657089b`. Contracts govern behaviour; draft code supplies Static names, not measured results. No app, tests, db, entrypoint, Section I, Part 1, plan, links or configuration writes. No git by workers, further agents, external contact, deletes, push/tag/merge. Scratch only `D:/RAD/FINAL/Part2/notes/P2-<X>/`. Use bundled Python `C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -I`; set stdout UTF-8.

## Sources and vocabulary

Read `D:/RAD/FINAL/PLAN_SaigonBite_Part2_Final.md` §§1–5, P2/P3.1, §§7/10/11; `Part2/README.md`, `Part2/content/links.json`, `Part2/codex/P2_CHECKLIST.md`; primary authorities `Lec_re/` (direct extracts/tables in `Part2/notes/P2_primary_sources.json`), convenience `Part2_Plan_Review/source_evidence/`; `Part1_v2/content/content_master.md`, `build/proc_*.py`, `notes/diagram_changes.md` read-only. Repo `D:/RAD/FINAL/SaigonBite`; contracts `docs/part2/{rules.md,decision_log.md,ssd_operations.csv,pc_mg_register.csv}`. Phase 1 files in `models/shared/` are immutable. Follow their generator `.py` + `.json` → drawio/PNG/SVG pattern. `balanced-diagrams.skill.txt` is a ZIP; read `balanced-diagrams/SKILL.md` with zipfile. Read primary schema and controller/domain files only for Static comparisons.

Exact main goals: UC-01 Place an order with an accepted full price, voucher and payment choice; UC-02 Deliver an order: pick up, deliver with cash collection, or report failure; UC-03 Maintain hubs and kitchen capacity; UC-04 Produce management reports: sales, workload, delivery performance; UC-05 Decide an incoming order: confirm, reject, or offer a replacement the customer agrees to; UC-06 Maintain brands, menu items and hub listings. Proposal owners 01/03 722I0004; 02/04 523K0049; 05/06 523K0050. Actual author ALL 722I0004.

SUC-01 Log in / log out; SUC-02 Register (local or tourist), edit profile, manage addresses; SUC-03 Track my orders, view receipt, answer a replacement offer; SUC-04 Cancel an order (PLACED or CONFIRMED); SUC-05 Start preparing and mark ready; SUC-06 Set menu availability at my hub; SUC-07 Maintain vouchers; SUC-08 Maintain user accounts; deactivate/reactivate; SUC-09 Archive closed orders; read archived history.

Actors: Customer generalised into Local customer / Tourist customer; Kitchen staff; Shipper; Admin; Manager; external Payment simulator where shown (no real provider). Order: PLACED, CONFIRMED, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, REJECTED, CANCELLED. Delivery: AWAITING_PICKUP, PICKED_UP, DELIVERED, FAILED. COD: PENDING → PAID / VOIDED. ONLINE: PAID → REFUND_PENDING; partial refund owed is an attribute while PAID; REFUNDED is grey future only. ReplacementOffer: OFFERED → ACCEPTED / DECLINED / WITHDRAWN. Hub/Brand/MenuItem: ACTIVE → ARCHIVED; listing AVAILABLE ↔ SOLD_OUT then unlist; UserAccount ACTIVE ↔ INACTIVE. Busy/quiet and waiting for customer are derived notes. BR-01–26, A-01–19, Q1–Q5, L1–L6 and D-1–D-13 retain exact IDs. Defaults are not approval. No L1/L3/L6 differing answer recorded at preflight.

## Description and notation contract

Template fields, in order: **Use case name; Scenario / trigger; Actors; Related use cases; Stakeholders and interests; Pre-conditions; Post-conditions; Flow of activities; Exception conditions**. Add ID/author and brief scenario without reordering these fields. Put minimum guarantees with Post-conditions. Number main flow in Actor | System columns; Axx alternates / Exx exceptions name branch step and rejoin/end; every failure ends in MG. PC/MG text comes verbatim from register. UC relations cite B's diagram (A does not duplicate its decisions); supporting links need not be include/extend. Extra anchors/ops/events/CRUD/state requests go ONLY under **Requests to root** in report; only root accepts/rejects and changes shared contracts after the wave.

Report names: `II_2-2-<1..6>_UC-<01..06>.md`. Subheadings verbatim: `i. Fully developed use case description`; `ii. Activity diagram for Use Case N`; `iii. System sequence diagram for Use Case N`; `iv. State machine diagram for Use Case N`. Part i has only include directive `<!-- include: ../UC-0x/description.md -->` plus introduction if needed. Each section/caption contains author; caption `Figure <n>. <title> — Author: 722I0004 · AI-assisted (Codex)`. Figure IDs: B 2.1–2.2; C 2.3–2.9; activities/SSDs UC01 2.10/2.11, UC02 2.12/2.13, UC03 2.14/2.15, UC04 2.16/2.17, UC05 2.18/2.19, UC06 2.20/2.21. Split figures append A/B. State blocks identify owner; render Order/Payment once under UC01, Delivery UC02, Hub UC03, Offer UC05, Catalogue UC06; UserAccount once under UC03 as a shared supporting-account model. UC04 only cross-references; UC05 cross-references Order. Root assembly places C's figures in iv.

Activity: Actor | System partitions (simulator only if in description); every decision outgoing edge has complete mutually exclusive `[guard]`; explicit merge before rejoin; activity final ends whole activity, flow final only one branch. Actions match numbered description; expose IDs for consistency mapping. SSD: actor + `:System` only (simulator optional for UC01 if shown); only catalogue operations with parameters, dashed returns and guarded alt/opt/loop; no internals. UC05 Customer response is a cross-reference to SUC03/UC01 rather than a second human SSD lifeline; a separate companion SSD fragment can use Customer + System.

States: plan §4 transitions, `event [guard] / effect`, initial/final pseudostates, four terminal Order states; derived notes only; each PC/MG links to transition/stored fact. UC diagram: boundary SaigonBite system; actors outside, correct Customer generalisation; all 6+9 UCs; include base→included, extend extension→base with named extension point; groups a–d; deferred complaint/refund decision/payout/rating note only. Domain: 13 persistent classes + Local/Tourist subclasses, simple typed attributes, no methods/FKs; both-end multiplicities; HubMenuItem association class; Order composition OrderLine; Order–Payment 1:1, Delivery 1:0..1, Offer 1:0..*; offer→OrderLine; Shipper role on UserAccount; Quote/report/receipt not persistent.

Readability: ≥9 pt at placed width 170 mm portrait or 230 mm landscape; split `_PartA`, `_PartB` rather than shrink. Validate XML and connected edges. Open and visually inspect every PNG and SVG, retain A4 proofs/logs outside repo. Report actual inspection and limits; do not claim native draw.io/Excel or application correctness without evidence.

## Disjoint write sets

| Wave 1 | Exclusive repo write set (plus own scratch) |
|---|---|
| A P2-10–15 | report/II_2-1_team_analysis.md; docs/part2/SUC.md; _agent_reports/P2-A.md |
| B P2-16–19 | models/shared/use_case_diagram.*; domain_model.* (including split files); report/II_2-1-6_2-1-7_models.md; _agent_reports/P2-B.md |
| C P2-20–24 | models/shared/sm_order.*, sm_payment.*, sm_user_account.*; models/UC-02/sm_delivery.*; UC-03/sm_hub.*; UC-05/sm_replacement_offer.*; UC-06/sm_catalogue.* (including split files); report/II_state_machines.md; _agent_reports/P2-C.md |
| D P2-25–27 | report/II_2-3_crud.md; _agent_reports/P2-D.md |

| Wave 2 | Exclusive repo write set (plus own scratch) |
|---|---|
| E P2-31–35/51–55 | docs/part2/UC-01/description.md, UC-05/description.md; models/UC-01/activity_uc01.*, ssd_uc01.*; UC-05/activity_uc05.*, ssd_uc05.*; report/II_2-2-1_UC-01.md, II_2-2-5_UC-05.md; _agent_reports/P2-E.md |
| F P2-36–40/46–50 | same pattern for UC-02 / UC-04, report parts 2/4; _agent_reports/P2-F.md |
| G P2-41–45/56–60 | same pattern for UC-03 / UC-06, report parts 3/6; _agent_reports/P2-G.md |

Report paths above prefixed `docs/part2/` unless full `models/` path. Root owns all other writes, workbook/checklist/AI log/contracts/assembly/git. Marker: `⟦PENDING: what, expected when⟧`. Finish report with files, checklist evidence, BLOCKED / ASSUMED, Requests to root, sources, visual QA; one final notification only after whole workstream.
