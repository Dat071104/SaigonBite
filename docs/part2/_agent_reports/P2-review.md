# Phase 2 independent G2 review

Author: 722I0004 · AI-assisted (Codex)

Review date: 24/10/2026, Asia/Bangkok. Assigned canonical revision: **3097dca**, supplied by root. This review assessed the current final sources and exports, rather than treating workers' pre-integration assumptions as the final contract. No Git command, application execution, test, build, renderer, network request or child agent was used. The sole file written is this report.

**G2 verdict: NOT READY at the reviewed revision.** The package is substantially complete and its protected boundaries are intact, but the disconnected activities and the specific contradictions below prevent a clean B5/P2-71 consistency verdict. These are bounded analysis corrections; they require no application change or locked-plan rewrite. Item 17's declared J2 shortfall is separate from these correctable defects. Final commit, checklist closure and staging remain root actions after disposition.

## Findings, severity first

### R1 — HIGH / G2 blocker: UC-02, UC-04 and UC-06 do not each form one logical activity

**Authority:** P2_PROMPT.md B5 explicitly requires one activity per UC. Readability permits split views of that activity; it does not authorize replacing one UC activity with several independently started activities.

**Evidence:**

- `models/UC-02/activity_uc02_PartA.drawio`, Figure 2.12A: `I → A_request → D_valid ... → A_result → M_end → F`. The successful `A_result` says “Continue B or C later”, but there is no connector or control edge to either continuation. Parts B and C each have their own `I` and `F`. Pickup therefore reaches an activity final before the selected deliver/failure goal is represented. A03's resume/bypass and A04's empty/read-only outcome are notes rather than alternate paths in this graph.
- `models/UC-04/activity_uc04_PartA.drawio`, `_PartB.drawio`, `_PartC.drawio`, Figures 2.16A–C: each independently executes `I → A_request ... → M_end → F`. There is no common report-choice dispatcher, continuation or loop matching description step 5 and SSD Figure 2.17.
- `models/UC-06/activity_uc06_PartA.drawio`, `_PartB.drawio`, `_PartC.drawio`, Figures 2.20A–C: the independent `CA-start/CA-final`, `CB-start/CB-final`, `CC-start/CC-final` graphs have no cross-page dispatch/continuation. Their base multipage file does not join their control flows.
- `report/II_2-2-2_UC-02.md:13`, `II_2-2-4_UC-04.md:13`, and `II_2-2-6_UC-06.md:27` explicitly describe independent episodes/requests. F's assumption at `P2-F.md:86` explains the choice but does not waive B5.

**Fix:** preserve the readable split layout while adding one explicit logical entry and named, paired continuation connectors per UC. For UC-02, dispatch new pickup versus resumed own assignment, continue successful pickup to travel and an exclusive delivered/failure choice, and show empty/read-only/end outcomes. The committed pickup must remain durable across later requests; no transaction spans travel. For UC-04, dispatch sales/workload/performance from one entry, merge results/refusals and show repeat/end. For UC-06, dispatch brand/item/listing maintenance from one entry, merge outcomes and show repeat/end. Remove independent initials from continuation views. Retain activity finals only for a complete outcome of the logical activity; do not add concurrency or misuse flow finals to conceal the split. Regenerate source/export sets, update source prose and native-ID mappings where affected, then reassemble Section II.

### R2 — MEDIUM / consistency correction: active-only uniqueness wording survives the root disposition

**Evidence:** `UC-06/description.md:70` explicitly includes retained archived names in duplicate checks. Root's Wave 3 disposition rejects active-only uniqueness. Nevertheless, `models/UC-06/ssd_uc06_PartA.json:39` and the final Figure 2.21A `note` still say **“Active-name uniqueness”**. The same label is visible in the final PNG and independently rendered SVG. `analysis_consistency.csv:28` describes UC06-MG02 as **“Duplicate active names/pair”**.

**Effect:** the package gives conflicting answers for create/update after a prior matching name has been archived. This is a current source/export contradiction, not merely a stale worker report.

**Fix:** change the generator data/annotation and UC06-MG02 fact text to the adopted uniqueness scope, including retained archived names, and regenerate the base/Part A SSD exports. Preserve the no-restore/no-reparenting boundary and do not change the plan or application.

### R3 — MEDIUM / consistency correction: the item-create activity requires an existing ACTIVE target

**Evidence:** Figure 2.20B `CB-validate`, also `models/UC-06/activity_uc06_PartB.json:12`, says **“A04–A06: active Admin; valid fields; ACTIVE target”** without limiting the target guard to updates/archives. A04 is `createMenuItem`, whose description at `UC-06/description.md:55` requires an active Brand and creates a new ACTIVE item. Figure 2.20A correctly uses the narrower “update/archive: ACTIVE target” wording for Brand.

**Fix:** qualify the item target-exists/ACTIVE guard as **update/archive only**. Creation validates the active parent and new-item fields/uniqueness/price; it does not require a pre-existing item target. Regenerate the item activity and any base alias/container that contains it. This is an annotation/guard correction, not a new operation.

### R4 — MEDIUM / consistency correction: UC-03's archived inspection contract contradicts E03

**Evidence:** `UC-03/description.md:27` permits reads to inspect archived records, consistent with UC03-PC02 and `listHubs(includeArchived?)`. However, `UC-03/description.md:59` makes an **“archived target”** an E03 condition **“at any request”**, explicitly returning `refusal` for `getHub`. These statements disagree when an authorized Admin inspects a retained archived Hub.

**Fix:** limit the archived-target refusal to commands that require an ACTIVE target, particularly update/archive. Keep authorized retained-record inspection valid; missing records and denied contexts still refuse. Reassemble the description into Section II. While making this correction, state the active-Admin recheck before `H-read` / `CA-read` / `CB-read` / `CC-read`, or add their denial paths: the current activities explicitly show it only on the maintenance branch, although the descriptions require it on every read. The latter is a diagram-completeness clarification, not a finding of an application security defect.

### R5 — MEDIUM / failure-path correction: UC-05 Customer SSD results omit E04's failed atomic save

**Evidence:** `UC-05/description.md:55` requires rollback and a controlled retry outcome for every modifying request on lock/write/commit failure. Activity Figure 2.18C explicitly has `05C-COMMIT → 05C-ROLL` and says invalid-target withdrawal also rolls back on save failure. In Figure 2.19B, `05S-R08a` is guarded only by own PLACED/exact open/valid target, `05S-R08b` only by eligible offer/invalid target, and the remaining operand is explicitly stale/wrong owner/terminal. Neither success/withdrawal result requires successful atomic persistence, nor is failed persistence represented. Figure 2.19C similarly describes valid own/open guards as leading to rejection, with only `staleRefusal` otherwise. Catalogue OP-05/OP-06 enumerate no controlled technical-failure return, unlike the description's E04 outcome.

**Fix:** qualify committed success and committed withdrawal/rejection results by atomic-save success, and add a controlled failed-save/rollback outcome with UC05-MG01 and no partial effects. Distinguish a technical failure from a stale answer. Align OP-05/OP-06's return descriptions and the SSDs with that existing failure contract; keep the same operation names, parameters, operation count and anchors. No controller/DAO/SQL lifeline or internal call belongs in the SSD.

### R6 — LOW / editorial corrections

- `UC-01/description.md:36` still says the simulator choice precedes **“step 6's transaction”**, although step 5 now begins it (`:25`) and step 6 continues it. Say “before step 5 begins the checkout transaction”; the current graph's actual ordering is correct.
- `report/II_2-1-6_2-1-7_models.md`, the Validate accepted checkout relation explanation, says **every attempt** validates the accepted full quote. UC-01 A01 intentionally resolves an authorized existing-token replay before the new-checkout validation at step 6. Qualify that explanation for creation attempts and explicitly preserve the replay short circuit; do not cause a replay to reprice or reauthorize.
- `report/II_2-2-3_UC-03.md:47` is catalogue boilerplate referring to A–C figures and first-page aliases, although this UC has one activity and one SSD. Replace it with the actual UC-03 source/export statement.

## Independent verification and B5 assessment

The checks below were performed with inline, stateless `python -X utf8 -I` and read-only document/XML/image access. Existing root audits were also read, but they were not treated as substitutes for source inspection. No audit helper that writes notes was executed.

| Area | Evidence and assessment |
|---|---|
| Description structure | Directly read all six final descriptions and primary DOCX table. All nine fields occur in the required order: Use case name; Scenario / trigger; Actors; Related use cases; Stakeholders and interests; Pre-conditions; Post-conditions; Flow of activities; Exception conditions. Titles identify the exact locked goals and author. Main flows have Actor/System columns and numbering. A/E branches identify their departure and rejoin/end; failure guarantees are stated. R4/R6 identify the remaining wording contradictions. |
| Main anchors | Independently parsed plan P2.3 and compared with `pc_mg_register.csv`: **30/30 verbatim**, no missing/extra anchor and no text difference. The consistency matrix has **30 unique rows**, with every register ID present. **271 native activity/SSD pointers** resolve to actual draw.io cell IDs. ID resolution alone does not establish the control-flow correctness missing in R1. |
| SSD catalogue and flow membership | **60 operations; 41 request occurrences; 38 distinct operations.** Independently checked each request ledger row's operation, catalogue ID and exact parameters, description operation occurrence and native SSD cell: zero mismatches. The 12 §4 lifecycle names are retained. Request membership remains separate from creation effects, so a query is not claimed to create later facts. All inspected SSD fragments use one human actor plus `:System`, dashed results and guarded frames; no controller, DAO, SQL or widget lifeline is present. R5 remains a failure-result completeness gap. |
| Activities | Actor/System responsibility partitions, exclusive valid/invalid or complementary guards, and merges before common result/end paths are present. UC-01 and UC-05 have paired continuation connectors and only their first view has an initial node. UC-03 has one connected activity. R1 prevents a six-UC pass; R3 and the read-check clarification in R4 concern actual annotations rather than XML validity. |
| State machines | Read all 17 state views and owning PC/fact tables. Order covers all 12 plan events and the four terminal states. Delivery's paired lifecycle, COD PENDING→PAID/VOIDED and ONLINE PAID→REFUND_PENDING with full captured C are consistent. Partial refund owed remains an attribute while PAID. REFUNDED is grey and has no incoming payout transition; a simulator decline creates no FAILED Payment. Busy/quiet and waiting-for-customer are notes. Hub/Brand/MenuItem archive; listing AVAILABLE↔SOLD_OUT and unlist; Offer OFFERED→ACCEPTED/DECLINED/WITHDRAWN; UserAccount ACTIVE↔INACTIVE and BR-25 are represented. Continuation projections repeat the same state identities, not new lifecycles. The account's disconnected final is explicitly unreachable because no account-end command exists. UC-04 has no fake Report state. |
| Checkout boundary | Final UC-01 step 5 and Figure 2.10B begin the short transaction before token lookup, preventing authorization on replay. A02's simulator choice is before that boundary; deterministic local decision and new-order writes are inside it. Capacity, raw radius, full fingerprint plus T and voucher are rechecked; no user wait/network request holds the transaction. Failure through COMMIT releases authorization and saves no order/payment/line. R6 is the stale step-number phrase, not a rejection of this corrected boundary. |
| Replacement and money | Whole line, unchanged quantity, unavailable source, one open offer, same-hub eligible different target absent from other lines, equal/lower snapshot price, offered price on acceptance, exact-open ownership/PLACED recheck, D_new=min(D_old,S_new), unchanged F/Q, COD new T and ONLINE unchanged C/owed=C−T are explicit. Invalid target withdraws only the exact offer and returns a reason; Order/lines/payment stay unchanged. No persistent withdrawal_reason is required. Later cancel/decline/reject/failure replaces any partial owed amount with full C. The fixed 100,000→90,000 example is a contract oracle, not a measured result. R5 concerns failed persistence of these outcomes. |
| Delivery | UC-02 explicitly permits any active shipper to take READY work without a one-delivery cap, but only the assigned shipper may finish. Exact COD cash=T, ONLINE absent/zero cash, zero-change repeated/wrong/lost commands, paired terminal facts/timestamps, and full-C failure obligation are described and mapped. R1 concerns activity coverage, not these business rules. |
| Reports and archive | Sales use DELIVERED/finish-time VN-day→UTC half-open filters, order grain without line double-counting, item identity grouping and refunds owed separate from T. Workload is “now”, with retained archived Hub identities and zero open work under BR-18. This conservative reading is consistent with UC03-PC02, not a permission to invent historical workload. Wait uses finished deliveries with valid READY/pickup pairs; ride uses successes; each metric shows its own N, failed/(delivered+failed) and n/a for zero denominators. Reports write zero rows and enforce Manager access. Archived history/snapshots/obligations remain readable; operational visibility is distinct. R4 is the narrower retained-Hub inspection contradiction. |
| UC model | Figures 2.1A–C have the named boundary, outside actors, correctly directed Customer specialization and include/extend arrows, named extension points, groups a–d and all 6+9 portfolio goals. The two factored UC-01 behaviors do not add portfolio IDs or catalogue operations. Deferred complaint/refund decision, payout and rating are notes only. R6 qualifies the overly broad include explanation on replay. |
| Domain | Figures 2.2A–C contain 13 persistent base classes plus LocalCustomer/TouristCustomer, typed attributes, both-end ordinary multiplicities, specialization, Order composition of ≥1 OrderLine, the HubMenuItem association class, Order–Payment 1:1, Delivery 1:0..1, Offer 1:0..*, and offer→same-order line/target links. No methods, FK attributes, Shipper class, persisted Quote/receipt/report rows were added. `id` is a local identity attribute, not an FK. Current Part C removes withdrawal_reason. The sole absent drawn SQL attribute, UserAccount.created_at, is already a named P3/P4 obligation. |
| CRUD | Independently reconstructed actor cells from final report tables and parsed original plan §2.4. Actor qualified-cell counts: Customer 33, Kitchen staff 15, Shipper 9, Admin 37, Manager 6. The reconciled union has **96 qualified cells**, retains **all 89 original cells**, and adds exactly **7 Read qualifiers**, with **zero added C/U/D grants**. All five actor tables map the 13 actual SQL tables. The scoped authentication, address-snapshot, own-hub, delivery-payment-summary and authorized-history readings are supported by existing goals. This is an explicitly documented reconciliation of inconsistent plan tables, not a claim of exact original equality or a seed-as-Create pass. |
| Traceability and assembly | Six descriptions are present in assembled Section II, no include directive or unresolved PENDING remains there, numbered headings follow the primary template with the documented five-actor extension. State figures appear once under their owning iv subsections. `traceability.csv` has **44 Analysed** anchored rows and **8 Planned** NFR rows; all design/screen/code/test/result cells remain blank. The 8 cross-cutting NFRs are not falsely qualified by unrelated PCs. |
| English, provenance and author | No invented lecturer/client answer, executed oracle, member artifact authorship or application result was found. Artifacts are English; names/IDs and contract excerpts are properly specific. An independent nine-word comparison against the primary case PDF found zero overlap candidates; that supports, but is not a universal proof of, own wording. All 52 actual figure captions/views identify 722I0004 and AI-assisted (Codex). Proposal owners remain separate from actual author. The AI log records root and A–G, their use, kept/corrected work and checks. Root should add the completed reviewer use/disposition at final integration. |

## Marking Checklist items 14–20

Direct primary reading: `Lec_re/RAD_Sem01_2627_MarkingSheet.xlsx`, **Checklist column B item numbers**, physical rows below. These are evidence assessments, not awarded grades.

| Item / physical row | Evidence pointer or named gap |
|---|---|
| 14 / row 27 — events, actors, UC list with owners, UC diagram | `report/II_2-1_team_analysis.md` §§2.1.1–2.1.5; `II_2-1-6_2-1-7_models.md` §2.1.6; Figures 2.1A–C. 20 events, all portfolio goals/actors, exact proposal owners and separate actual author. R6 is a narrow relation-explanation correction. |
| 15 / row 28 — domain model | §2.1.7; Figures 2.2A–C; final static schema mapping. Required generalization, whole-part and association class are present; implementation gaps are separately named P4 inputs. |
| 16 / row 29 — description/activity/SSD for every main UC | Six `UC-0x/description.md`, six `II_2-2-x_UC-0x.md` parts and Figures 2.10–2.21. All artifacts exist, but **R1–R5 prevent a clean correctness/consistency pass**. |
| 17 / row 30 — at least one state machine per student | **Partial under J2**: Figures 2.3–2.9 and captions show actual author 722I0004. No state-machine authorship evidence for 523K0049 or 523K0050. This records the shortfall; it does not satisfy the per-student requirement for those members. |
| 18 / row 31 — CRUD per actor; every persistent class covered | `II_2-3_crud.md` §§2.3.1–2.3.5, derived union, archive and SQL coverage tables; workbook CRUD Check rows 5–17. Analysis coverage is present for 13/13 classes. Actual running Create/Read/Update/Archive correctness remains P4/G4. |
| 19 / row 32 — ordering, fulfilment, CRUD and reports | §2.1.5 and Figure 2.1: (a) UC-01; (b) UC-02/05; (c) UC-03/06; (d) UC-04. |
| 20 / row 33 — author on every diagram and UC | All six UC titles, report sections, 52 figure views/captions and source/export annotations identify 722I0004 plus AI-assisted (Codex). No other member is presented as actual Part 2 model author. |

## Each P2-II Excellent criterion

Direct primary reading: MarkingSheet **Rubric Guide row 8**, P2-II, Excellent cell. The criteria are evaluated separately; no promise of Excellent follows from artifact existence.

| Excellent criterion | Evidence / gap |
|---|---|
| Events table complete | §2.1.3 and workbook Events Table rows 5–24: 20 External/on-demand Temporal entries cover ordering, all lifecycle commands, supporting maintenance/access/history and reporting; no scheduler or database actor is invented. |
| Domain model correct, with generalization, whole-part and association classes where needed | §2.1.7 / Figures 2.2A–C meet these structural requirements. Static SQL/behavior gaps remain explicit future mapping/implementation obligations. |
| Use case descriptions fully developed with pre- and post-conditions | Six nine-field descriptions, explicit A/E continuations, all 30 verbatim PC/MG anchors and supporting contracts provide the evidence. **R4/R6** qualify the remaining contradictory wording. |
| Activity diagram, SSD and state machine consistent with each other | The two ledgers resolve all anchor IDs and request signatures; state/fact mappings and money semantics are present. **R1–R5 are named current gaps**, so this criterion is not yet clean. |
| CRUD verification complete | Five actor tables, 96-cell reconciled union with no original cell loss or new write grants, 13/13 SQL coverage, archive/snapshot semantics and 13 workbook OK rows. Running-path evidence belongs to P4; seed is explicitly excluded as Create. |

## Protected-boundary and workbook evidence

- **Independently rehashed all 1,368 manifest-listed files** against `Part2/notes/P2_start_hashes.json`: 1,245 Part1_v2; 11 repo Part 1; 85 app; 12 tests; 4 db; 2 entrypoints; 2 plan/links; 7 Section I. **Zero missing files and zero hash differences.** This directly supports byte preservation of those listed files. The retained `P2_end_hash_check.json` separately records `pass=true` and root's `git_app_diff_exit=0`; that Git check was not rerun by this reviewer. The manifest's established exclusions remain its boundary.
- Current working workbook SHA-256 is **eb9a97714afa92cfdab30943f827883b3de996045d62c340e4268d1159ba31d9**, exactly the published candidate in `P2_workbook_preservation.json`.
- Independently compared `P2-root/workbook_before.xlsx` with the published workbook: **118 formula texts unchanged; 321 green lecturer cells (FFDDF0DF) retain values and styles; all 25 validation rules unchanged**. Direct data-only read finds 20 events and 13 used CRUD rows cached as OK. The guard report additionally records the controlled Gap→OK probe, 244 allowed input changes, three modified worksheet parts and client count 5; this reviewer did not rerun the calculation/probe.
- Opened all seven `P2-root/workbook_preview/final_*.png` views. Changed-region text is visible; proposal ownership and sole actual authorship are distinguished. Native Excel opening/recalculation remains untested.

## Visual inspection scope and limits

Independently opened the **52 unique Phase 2 figure views in both PNG and existing independently rasterized SVG form**, using supplied visual pairs where available: B's 6 UC/domain views; C's 17 state views; E's 12 UC-01/05 activity/SSD views; F's 9 UC-02/04 views; G's 8 UC-03/06 views. For revised files, used root's current SVG reviews for domain Part C, UC-01 activity Part B and SSD Part A, UC-04 activity Part B, UC-06 activities A/B and SSD B. Current PNGs were opened alongside these where the worker pair was superseded. The eight unsuffixed first-page PNG aliases were independently pixel-compared with their Part A counterparts: all identical.

All **60 draw.io/SVG source-export sets parse**; **591 edge endpoint references resolve**, and all 60 draw.io hashes still match root's final structural audit. All extracted SVG minimum font sizes scale to at least 9 pt at 230 mm; the lowest is **9.4173 pt** for the domain model. Labels, arrow directions, multiplicities, guards and author annotations are visible in the inspected forms. R1 is a semantic control-flow defect despite individually readable pages; R2/R3 are readable but incorrect annotations. No new render, cache, scratch or proof file was created.

Native draw.io editing, native Excel and final DOCX/PDF landscape placement remain **UNTESTED**. The minimum-size calculation assumes the specified 230 mm placement; it is not evidence that the eventual final report renderer preserves that size. Existing inspections/proofs support current exports, not final submission placement or application correctness.

## Checklist disposition for the assigned lane

| ID | Reviewer disposition |
|---|---|
| P2-70 | Review completed; **cannot assert B5 holds** until R1–R3/R5 and the identified wording/denial clarifications are disposed. |
| P2-71 | Review completed; ledgers/domain/CRUD evidence verified, but R1–R5 leave current cross-artifact contradictions. |
| P2-72 | English/provenance/actual authorship checks completed with the limits above. Completed reviewer AI-log row remains a root integration action. |
| P2-73 | Done in this report: pointer or named gap for every item 14–20 and each Excellent criterion; item 17 explicitly Partial. |
| P2-74 | Protected-file hashes independently pass for all 1,368 listed files. Retained root Git evidence is identified separately; no reviewer Git execution. |
| P2-75 | **Open for root**: findings above have not been repaired by the read-only reviewer. Root must record each fix or reasoned disposition and verify revised exports/mappings/assembly. |
| P2-76 | **Pending root**: final phase commit follows integration. No commit fabricated or created here. |

The existing unchecked final-review/staging boxes are administrative timing, not additional content defects. P2-80/81 staging is outside this reviewer's write lane.

## BLOCKED / ASSUMED and next actions

No access blocker prevented the review. The review assumes the root-supplied revision label 3097dca; source hashes were checked without Git. Locked defaults remain unanswered, particularly L1/L3/L6; no differing lecturer answer was found in the decision log. Existing root P4 inputs, including schema/validation/transaction/report differences, remain future work and were not repaired or relabelled as runtime findings.

Root should resolve R1–R5, apply the low-cost R6 text corrections, regenerate only affected models, update native mappings if IDs change, reassemble Section II, retain truthful J2 Partial, append reviewer AI use/dispositions, then close the final commit and staging checks. A G2-ready declaration can follow that concrete correction evidence. G2 remains analysis readiness; it does not qualify the app, a running CRUD portfolio, measured report accuracy, deployment or any future grade.

## Sources used

- First reads: `docs/part2/_agent_reports/P2-brief.md` and `P2-root.md`.
- Locked `D:/RAD/FINAL/PLAN_SaigonBite_Part2_Final.md` §§1–5, P2, P3.1, §§7/10/11; `Part2/README.md`, `content/links.json`, `codex/P2_PROMPT.md` B5/B6/B8 and `P2_CHECKLIST.md`.
- Direct primary reads: Case Study PDF (both pages), Final Project Requirements PDF (all eight pages), Report_Template.docx headings and nine-field table, MarkingSheet.xlsx Checklist 27–33 and Rubric Guide row 8, Team_Workbook_Template.xlsx relevant sheets. Retained direct-source index: `Part2/notes/P2_primary_sources.json`.
- Final assembled Section II, all source parts, six descriptions, `SUC.md`, `rules.md`, `decision_log.md`, both operation/anchor catalogues, both consistency/request ledgers, traceability and AI log; all Phase 2 shared/UC model XML/SVG/data and the existing visual evidence detailed above. Worker reports were used only to identify provenance/assumptions; final sources control the findings.
- Frozen Part 1 content/master vocabulary and `notes/diagram_changes.md` for history/style and connector/final conventions, read only.
- Start/end manifests, published workbook and before copy, preservation evidence, seven final previews; root structural/consistency/domain/CRUD/wording audits named in the assignment. No external source or application result was introduced.

**Files written:** `docs/part2/_agent_reports/P2-review.md` only.
