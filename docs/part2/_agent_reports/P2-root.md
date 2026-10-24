# Phase 2 root report

Author: 722I0004 · AI-assisted (Codex)

24/10/2026 (Asia/Bangkok). Scope: P2 analysis only. Starting clean branch `part2`, HEAD `657089b760e66585a52079ee44dbf8f336dbd694`. No app execution or correctness result is inferred from this phase.

## Sources read

Locked plan §§1–5, P2, P3.1, §§7/10/11; Part2 README, links and P2 checklist; Phase 1 Section I, traceability, rules, decision log and P1-root/brief; frozen Part 1 content and diagram style. Primary PDFs were extracted directly with pypdf; DOCX paragraphs and all tables read with python-docx (nine description fields, not just text extract); primary marking workbook Checklist and Rubric Guide; team template and working Team & Use Cases, Events Table, CRUD Check. Durable direct-source readings and controller AST inventory: `D:/RAD/FINAL/Part2/notes/P2_primary_sources.json`. Draft controllers, domain vocabulary/behaviour and schema v2 read only as Static evidence. PDF, Documents and Spreadsheets skills read; balanced-diagrams ZIP skill read, with Phase 1 generator patterns reused. No external project information was needed. Official Codex documentation was consulted only for runtime recovery; the live account-limit tool established availability before the same reviewer resumed.

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
| Literal §2.4 and §2.5 omit different scoped Read qualifiers | Retain all 89 original §2.4 qualified cells; reconcile seven already-scoped Read qualifiers, no new C/U/D grant. Proposed clarification: qualify own authentication, authorized profile/history, tracking/address, own-hub preparation/replacement and delivery-payment reads consistently in both tables. Locked plan unchanged; detailed cell-set proof is in Wave 1 integration. |

## P4 inputs

All findings below are **Static**, read at G1 `657089b`, not tests or measured results. No code fix is made here.

| ID | Evidence | Contract / later action |
|---|---|---|
| F-01 | tests/conftest.py:74 directly re-read: import-time _seed_prices queries obsolete delivery_fee_flat | P4.1 repair fixture/import collection; no P2 test pass claimed. |
| F-02 | business/domain/models.py:265–267 release_for_unfulfilled_order changes state only | BR-17 requires ONLINE refund_amount=C in the same change, including after a partial refund obligation. P4.4. |
| F-03 | data_access/report_dao.py sales and report_controller.py SalesRow.net | BR-21: do not subtract refunds owed again from already reduced T. P4.8. |
| F-04 | business/domain/rules.py:58 returns rounded Haversine distance | BR-05/06: use raw distance for radius/fee before display/storage rounding. P4.3. |
| F-05 | kitchen_controller.py:111–138; order_tracking_controller.py:76–99 | Require currently unavailable source; recheck target listed/available/not archived; invalid target withdraws offer without changing order. P4.4. |
| F-06 | presentation/templates/order/detail.html:18–19 directly re-read: difference/payment “is refunded”; line 33 says “to be refunded” | State refund owed, not paid out; payout is deferred L3. P4.4. |
| F-07 | place_order_controller.py:86–119 compares quoted_total only | BR-10 requires full content fingerprint plus T; catalogue describes required input, not existing implementation. P4.3. |
| F-08 | db/migrations contains README only; init_db.py:--migrate prints “up to date” when no scripts exist, without refusing user_version <2 | D-6 fresh v2 and explicit refusal of versions <2; do not claim a migration exists. P4.1. |
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

| Item | Physical Excel row | Evidence / disposition |
|---|---|---|
| 14 | 27 | report/II_2-1_team_analysis.md; report/II_2-1-6_2-1-7_models.md; Figure 2.1A–C (events, actors, full goals, proposal owners, actual author, UC relations). |
| 15 | 28 | Figure 2.2A–C; 13 base classes + 2 subtypes; final domain inventory in Part2/notes/P2-root/domain_model_final_audit.json. Static gaps remain P4 inputs. |
| 16 | 29 | Six docs/part2/UC-0x/description.md; Figures 2.10–2.21 split activities/SSDs; six report 2.2 source parts; analysis_consistency.csv and ssd_flow_membership.csv. |
| 17 | 30 | **Partial** under J2: all state machines are authored by 722I0004; no state-machine authorship exists for 523K0049 / 523K0050. This does not satisfy the per-student item for those members. |
| 18 | 31 | report/II_2-3_crud.md: five actor tables, reconciled 13-class union and 13/13 schema coverage; guarded workbook CRUD Check rows 5–17. Analysis only; running CRUD paths remain G4/P4 work. |
| 19 | 32 | Report 2.1.5 / Figure 2.1A–C: (a) UC-01; (b) UC-02/05; (c) UC-03/06; (d) UC-04. |
| 20 | 33 | Author 722I0004 plus AI-assisted (Codex) on six UC titles/sections and all report figure captions / model exports. |

| P2-II Excellent criterion (Rubric Guide row 8) | Evidence pointer / limit |
|---|---|
| Events table complete | 20 events in 2.1.3; workbook rows 5–24; External commands and on-demand Temporal date boundary, no fictitious scheduler/database actor. |
| Correct domain with generalisation, whole-part, association class | Figure 2.2A–C: Customer subtypes, Order composition OrderLine, HubMenuItem association class, multiplicities; Static differences listed, not hidden. |
| Fully developed descriptions with pre/postconditions | Six description sources, nine template fields in order, numbered two-column flow, A/E branches and 30 verbatim main anchors; SUC.md has nine supporting contracts. |
| Activity / SSD / state consistency | analysis_consistency.csv: 30 actual-ID mappings; ssd_flow_membership.csv: 41 request occurrences / 38 distinct catalogue operations with exact parameters and flow membership. No application result is inferred. |
| Complete CRUD verification | Five scoped actor tables and derived union retain every original §2.4 cell, explicitly reconcile literal plan omissions, cover all 13 tables. Running-path verification stays in P4. |

These are evidence pointers for review, not an awarded score or a promise of Excellent.

## Wave 1 integration

All four completion notifications were received before any Wave 1 report was opened. Root then read A/B/C/D reports together. Requests and dispositions:

| Request / finding | Disposition and reason |
|---|---|
| A: classify the 12 lifecycle events consistently | Accepted: External actor commands trigger the state changes; new states are responses. No autonomous state-event handler is invented. Temporal voucher boundaries remain checked on demand. |
| Root: event 2 said simulator decline before checkout | Corrected to deterministic decision within confirmCheckout before persistence. The customer's approve/decline choice precedes the transaction; commit failure also releases authorization, BR-14. |
| B: extra withdrawal_reason persistent attribute | Refused. §3.3(5) requires withdrawal with a shown reason, not new persistent reason history. Removed attribute from generator and regenerated all domain views; original B report is pre-integration evidence. Final PartC PNG and independently rendered SVG reopened by root. |
| B: domain/UC split placement | Accepted: Figure 2.1A–C / 2.2A–C need 230 mm landscape. Unsuffixed images are first-page aliases; editable base files contain all three pages. |
| B/C: Static P4 inputs | Accepted as mapping/behavior obligations, not runtime findings. See supplementary list below. |
| C: state placement | Accepted named machine blocks once under owning iv headings; shared cross-references elsewhere. Account final is explicitly unreachable because the contract has reversible inactivity and no deletion event. Future Payment REFUNDED remains disconnected grey. |
| D: §2.4/§2.5 literal CRUD discrepancies | Accepted narrow read-path reconciliation. Original §2.4 cells are all retained; seven extra Read qualifiers against literal §2.4 are from already-scoped §2.5 paths. Six missing actor qualifiers were filled from §2.4. No create/update/archive grant added. Authentication-context reads stay own-only, with credential lookup internal. |
| Root reverse-direction CRUD omission | Kitchen Order R SUC-05 occurs in §2.5 but not §2.4; retain own-hub preparation read. D's original report is superseded for closure by the root reconciliation, not silently presented as an exact original-plan match. |

Final five actor tables, reconciled union and all 13 schema tables are in `report/II_2-3_crud.md`; deterministic cell-set evidence: `Part2/notes/P2-root/crud_reconciliation.json` (zero missing original cells, zero additional write grants). Proposed future plan clarification: qualify own authentication, tracking/address selection, kitchen replacement/preparation, shipper payment-summary, Admin linked-profile/history reads explicitly in both tables. Locked plan unchanged. This is an analysis interpretation within existing scope, not a replan or new feature.

The UC model keeps six main + nine supporting portfolio goals. Two unnumbered factored UC-01 behaviors express mandatory validation and optional simulated payment; they do not add portfolio IDs, operations or persisted classes. The three real include/extend relations are defined in report 2.1.6; Wave 2 uses those decisions.

### Supplementary P4 inputs from B/C

- P2-S07: SQL does not enforce Customer's linked UserAccount role CUSTOMER; BR-12 type/role correctness remains a behavioral/schema-design obligation.
- P2-S08: Payment.updated_at is optional in the dataclass but NOT NULL in SQL. Direct PaymentDAO.insert inspection resolves the creation path: it writes updated_at or created_at. Document that mapping in P3; no unnecessary fix or failed-insert claim follows from optional typing alone.
- P2-S09: Cross-row guards require later verification: offer line belongs to its Order, target remains eligible at the same hub, active assigned SHIPPER, one Payment and ≥1 line per successful checkout, exact cash and paired Order/Delivery/Payment updates.
- P2-S10: Parent archive visibility, retained snapshots/history/refund obligations, Hub no-open-order archive, and BR-25 deactivation/next-request session checks need behavioral tests. Do not infer them from flags/CHECK constraints.
- No persisted withdrawal_reason requirement was adopted; P3 maps the withdrawal reason as an operation result.
- P2-S11: OrderTrackingController.answer_replacement and Order.replace_line lack an explicit PLACED recheck on acceptance. Existing no-open-offer confirmation/withdrawal logic is not a substitute for the §3.3(5) operation guard; verify/fix with F-05 in P4.4.
- P2-S12: data_access/database.py.connect configures foreign_keys and timeout=10, but does not set journal_mode=WAL or synchronous=NORMAL as required by §5.2. Retain for P4/P6 production connection setup; the timeout is already present and is not reported as missing.
- P2-S13: immediate_transaction performs COMMIT in its else branch outside the try/except around yield; no rollback handler covers a COMMIT exception. Audit this together with P2-S05 simulator-release behavior using forced commit failures in P4. No failure was induced in this phase.

## Workbook preparation (before Wave 2 integration)

Candidate only: `Part2/notes/P2-root/workbook_candidate.xlsx`; working/staged copies remain the G1 workbook until Wave 3. Payload is derived from versioned report events and reconciled CRUD, never hand-copied. Exactly 20 events and 13 union-class rows fit the template slots. Team & Use Cases corrections replace outdated short goals, distinguish proposal roles/owners from sole actual Part 2 authorship, and retain the proposal owner IDs.

Artifact Tool import omitted shared-formula followers (G6 was empty while the original read-only audit has a formula). The authoring script restores every original expanded expression before calculation; the guard retains original formula XML, styles and package. Empty formula-result caches on still-unused template rows are retained as empty. Explicit line breaks preserve wording while preventing preview overflow. A controlled missing-Create probe returned Gap, then OK after restoration; all 13 used rows evaluate OK, five client questions remain, and the error scan matches zero cells. Candidate audit preserves **118 formulas, 321 green lecturer cells and 25 validation rules**, with only three worksheet parts modified. All seven changed-region previews were opened; final publication/verification follows the Wave 2 barrier. Native Excel remains untested.

## Wave 2 liveness interruption and recovery

After the owner explicitly requested a process check, runtime inventory showed only root and no E/F/G reports or renderer processes. Metadata-only transcript inspection (no unfinished report read) found E/F had stopped before a final event; G ended at 04:41:53 UTC with `usage_limit_exceeded` and no final message. The same cause is not asserted for E/F without a terminal record. Root had waited too long without detecting the absent workers.

Root resumed the same p2_e / p2_f / p2_g identities with followup_task, preserving their original disjoint lanes and any existing drafts; no replacement agents, restart, deletes or model/config changes. Runtime then listed all three as running and their logs gained new timestamps. The owner's new instruction authorizes bounded process/liveness checks; it does not waive the report barrier. No Wave 2 report is opened until all three finish. Audit metadata is retained at `Part2/notes/P2-root/wave2_process_audit.json`; actual transcripts retain the terminal error and resume prompts.

## Wave 3 integration

F and G reported first; their reports remained unopened. Only after E's final notification did root open E/F/G together. All 30 main anchors and all 41 request occurrences were then integrated.

| Request / root finding | Accepted / refused and reason |
|---|---|
| E1 / F1 / G1: canonical state blocks under owning iv headings | Accepted via p2_assembly.json and p2_assemble.py: Order/Payment UC-01; Delivery UC-02; Hub/UserAccount UC-03; read-only explanation UC-04; Offer UC-05; Catalogue UC-06. Shared images appear once. |
| E2 / G2: anchor mappings plus query membership | Anchors accepted in analysis_consistency.csv. Request membership accepted in separate ssd_flow_membership.csv; mixing a read query into a creation-PC effect row was refused to avoid implying the query establishes a later write postcondition. Every request is still checked, including supporting receipt/tracking/cancel and Customer offer-response fragments. |
| E3 / F2 / G2: preserve all split views | Accepted: all report figure parts retained at 230 mm landscape; no first-page alias is presented as the complete multi-page diagram. |
| E4 / F3: no new operations or anchors; technical read failure | Accepted. Still 60 catalogue operations / 30 verbatim main anchors. Read-unavailable is an exception within existing report requests, with no fabricated figures or persistent writes; catalogue note records it. |
| G3: Static mapping obligations | Accepted into P4 inputs below. Composite catalogue reads, requested initial availability and current-parent brandId require P3 mapping; no code was changed. |
| Root: short UC-02/04 report names | Corrected to exact locked-plan goals. All six description titles now include the actual author. |
| Root: main flow used a separate Step column | Corrected to the required two Actor/System columns; numbering remains with the action/response and all existing branch references remain valid. |
| Root: active-only catalogue uniqueness wording | Refused as a promise of archived-name reuse. Root uses the conservative duplicate-name rule including retained archived names; diagrams/descriptions regenerated consistently. No restore/reparenting path added. |
| Root: F workload active-hub restriction derived from draft | Refused. BR-22 says per hub and UC03-PC02 retains archived identities in reports. Conservative analysis includes archived hub identities with no open work under BR-18; this becomes a named P4 draft gap, not a code fix. |
| Root: own catalogue return-name spacing typo | Corrected quoteWithFingerprintAndSD FQT to quoteWithFingerprintAndSDFQT in catalogue, description and generated UC-01 SSD. No operation or parameter changed. |
| Root: replay boundary clarity | Explicitly begins the short checkout transaction before the token lookup in step 5 / activity 2.10B; step 6 continues it. This preserves BR-11 under competing confirmations without any user/simulator choice held inside the transaction. |

`p2_consistency.py` resolves native node/edge IDs, rechecks all 41 actual request signatures against the catalogue and verifies description membership. `p2_audit.py` passes 60 new source/export sets, 30 anchor mappings, six nine-field descriptions and two-column flows, local assembled links and blank later evidence columns. All newly revised PNG/SVG forms were reopened by root, including first-page aliases; worker pre-integration QA remains historical evidence, while root's current hashes/structural checks cover final sources. Final diagram placement/native draw.io and native Excel remain later/native-engine limits, not hidden passes.

`p2_assemble.py` resolves all description includes and injects state blocks without hand-copying descriptions. Section II has the exact template numbered heading order, including the documented extension to five actors. A nine-word primary-case overlap scan found no candidates. Traceability has **44 Analysed** rows with specific main/SUC anchors and **8 Planned** cross-cutting NFRs (03–10) whose exact durability/performance/privacy/transport/config/UI/architecture guarantees are not established by P2.3 anchors. Their analysis constraints remain referenced; no unrelated PC or design/code/test/result evidence was invented.

Workbook published after the Wave 2 barrier and guard success. `P2_workbook_preservation.json` records 118 formula texts, 321 lecturer cells and 25 validations preserved, 244 allowed input-cell changes, three modified worksheet parts, 13 OK union rows and client count 5. Final Artifact Tool verification recalculated the preserved expressions, repeated the controlled Gap→OK probe and matched zero formula errors. All seven final renders are byte-identical to the reviewed candidate views. Native Excel was not used.

### Additional P3/P4 mapping inputs from Wave 2

- P2-S14: listCatalogue(hubId?) is a composite candidate over MenuController.catalogue / hub_menu; P3 confirms the observable-to-controller mapping.
- P2-S15: listItemAtHub accepts an initial availability choice, while draft list_item_at_hub has no flag. Map creation plus requested availability atomically; never expose a briefly orderable row when requested SOLD_OUT.
- P2-S16: updateMenuItem brandId is current-parent context; no item-reparenting or restore feature is promised by this phase.
- P2-S17: draft lifetime uniqueness, validation maxima/lengths and HCMC coordinate bounds must be reconciled explicitly in P3/P4. Retained archived names remain duplicate-constrained conservatively; no blanket relaxation or unapproved new locked default is implied.
- P2-S18: ReportController.workload_report currently iterates HubDAO.list_active. The adopted BR-22 / UC03-PC02 reading retains archived hub identities in reporting with zero open work; reconcile the query/result mapping in P4.

## Wave 4 independent review and root disposition

Author: 722I0004 · AI-assisted (Codex)

The sole reviewer completed its report before root opened it. Its first attempt stopped with a usage-limit error; after the owner's continuation, the live account-limit tool allowed ordinary usage and root resumed the same p2_review identity. No replacement worker, account purchase, configuration change or application work was introduced. Bounded metadata/status checks verified liveness without reading the unfinished report. The independent verdict remains **NOT READY at 3097dca** in the original report; that historical assessment is preserved rather than relabelled as a post-fix reviewer pass.

| Finding | Root disposition and correction evidence |
|---|---|
| R1 — disconnected UC-02/04/06 activities | Accepted and fixed. UC-02 has a sole initial, claim/resume/end choice, TF continuation, exclusive delivered/failed choice and FL continuation. A pickup transaction ends before travel. UC-04 has one report dispatcher, WB/DP continuations, R return to a common merge and repeat/end. UC-06 has one brand/item/listing dispatcher, MI/HL continuations, R return, entry/result merges and repeat/end. Continuation views have no independent initials. Source prose was rewritten; existing anchor node IDs retained. p2_review_audit.py checks every control node is reachable from the sole initial and can reach a complete activity final across the paired continuations. |
| R2 — surviving active-only uniqueness | Accepted and fixed. Brand SSD Part A and its base inputs/exports now include retained archived names; the consistency builder normalizes the historical G-row fact to the same scope. No restore/reparenting feature or application change. |
| R3 — create requires existing item target | Accepted and fixed. The MenuItem guard qualifies existing ACTIVE item as update/archive only. Creation checks active Brand, new fields, positive price and uniqueness. Base/Part B model data and exports agree. |
| R4 — archived Hub reads / authorization clarity | Accepted and fixed. UC-03 E03 restricts archived-target refusal to update/archive, explicitly allows authorized retained-record inspection. Hub and catalogue read nodes recheck active Admin before disclosure and state no-data denial with the appropriate MG; source flows state the same. This clarifies analysis, not a measured security defect. |
| R5 — Customer response save failures absent from SSD | Accepted and fixed. Acceptance returns require committed save for acceptance/withdrawal; a separate controlledFailure operand rolls back under UC05-MG01. Decline similarly separates committed rejection, stale refusal and technical failure. OP-05/06 returns/notes and UC-05 E04 agree. Extra return edges R08d/R09c are included in the MG matrix; operation names/count/parameters and all 30 anchors unchanged. |
| R6 — stale step / include / source boilerplate | Accepted and fixed. Simulator choice explicitly precedes the step-5 transaction. The include explanation applies to new checkout creation and preserves authorized token replay without repricing/reauthorization. UC-03 source statement now describes its actual single activity and SSD. |

All 13 changed unique figure views were opened as final PNG and independently Edge-rasterized SVG: UC-02 activities A–C; UC-03 activity; UC-04 activities A–C; UC-05 SSD B/C; UC-06 activities A–C and Brand SSD A. Revised first-page aliases match their Part A images. Final minimum placement remains at least 9 pt at the specified 230 mm width. Root retained the worker/reviewer reports as pre-fix evidence and recorded new structural/native-reference hashes, rather than relying on their earlier export hashes for changed files.

Root post-correction assessment: **G2 analysis-ready**, with the J2 item-17 **Partial** explicitly retained. Six complete packages, team analysis and five actor CRUD subsections exist; all 30 main anchors resolve to state/stored facts and SSD messages. The 41 requests remain in the 60-operation catalogue and their description flows. The two ledgers are distinct; later design/code/test/result columns stay blank and eight cross-cutting NFRs stay Planned. No unresolved R1–R6 correction is accepted as a hidden pass. This root assessment is not a second independent review, application qualification or grade prediction.

Verification evidence: `Part2/notes/P2-root/review_corrections_audit.json`, `analysis_structural_audit.json`, `Part2/notes/P2-root/consistency_audit.json`, final PNG/SVG reviews under `Part2/notes/P2-root/`, and the final start/end hash manifests. Native draw.io editing, native Excel and eventual final DOCX/PDF placement remain UNTESTED; later report assembly must preserve 230 mm landscape placement. No app tests were run in P2.

## Handoff and pending owner facts

Author: 722I0004 · AI-assisted (Codex)

- ⟦PENDING: actual L1–L6 lecturer answers or explicit unanswered records, planned discussion 26/10 and replan checkpoint 31/10⟧. A differing L1/L3/L6 answer triggers the locked-plan replan rule; silence remains unanswered.
- ⟦PENDING: Q1–Q5 answers and original submission dates, Dat to confirm by 31/10⟧. The five-question allowance remains exhausted; do not invent a further client question or answer.
- ⟦PENDING: real lecturer feedback/approval and official Part 2 submission date, when received / when the eLearning slot opens⟧. The team's 15/11 target is not presented as the official deadline.
- Dat should understand and explain the actual sole-authored models and AI assistance; no work is attributed to the other proposal owners.
- P3 may map these contracts into design; P4.1 may start the code/test foundation independently. The Static F-01…09 and P2-S01…18 inputs above are obligations for later phases, not P2 fixes or test results.

Submission staging follows only after the corrected model sources are committed. Exact local targets: `D:/RAD/FINAL/Part2/drive_upload/Team02_RAD_Sem01_2627_Team_Workbook.xlsx` and `D:/RAD/FINAL/Part2/drive_upload/Part2/models/` with shared/ and UC-01/ through UC-06/. Phase 1 flat copies are moved into shared/ without deletion; replaced staging bytes are preserved in P2_trash. Nothing is submitted to eLearning or pushed/tagged on GitHub by this phase. The staging manifest and final receipt outside the repo record the concrete copied hashes and final commit.
