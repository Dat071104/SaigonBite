# Phase 3 independent Wave 4 review

Author: 722I0004 · AI-assisted (Codex)

Review date: 25 October 2026, Asia/Bangkok. Assigned integrated revision: `d85d0671057a96ea1aee65aede574ab72fe29168` (root-supplied). Application baseline: `45ac76221b0a103174c7c01d17577e6e49cfd665` (C0). This review examines the available integrated files independently; the assigned integration commit was not separately queried because Git commands are outside the reviewer lane.

**Verdict: NOT READY for an unqualified G3/B5 closure at the reviewed artifact state.** The design inventory, responsibility coverage, explicit P4 obligations and persistence mapping are substantial and the full static cross-check passes. Four bounded diagram findings remain below. They concern what the actual drawings communicate, rather than an inferred application failure. R1–R2 need correction before a clean notation/analysis-consistency claim; R3–R4 are smaller explicit B5 gaps. No application change or plan rewrite is required to address these findings.

## Findings, material issues first

### R1 — MEDIUM: the alternatives are not consistently represented by actual guarded interaction operands

**Evidence:**

- `models/UC-05/seqdao_uc05_acceptReplacement_PartC.{json,drawio,png,svg}`, Figure **4.3.2.5.OP-05.C**: the box headed `alt [target invalid]` contains only an explanatory note. Its bottom is approximately y=478. The actual `decide(...WITHDRAWN...)`, return/rowcount and COMMIT messages occur below it (the decide arrow is y=591). Part D, Figure **4.3.2.5.OP-05.D**, repeats the pattern: an empty `alt [target valid]` header ends above `replace_line` (arrow y=466), save and rowcount messages. The branch descriptions and call-label guards are correct, but the drawings do not enclose either branch's messages in the claimed alternative. Two separate empty `alt` notes are not the two operands of that interaction.
- `models/UC-01/seq_uc01_confirmCheckout_PartB.{json,drawio,png,svg}`, Figure **3.1.4.OP-01B**: `authorise [ONLINE]`, `Order.place`, Payment creation and `release(reference) [failure through COMMIT]` all sit in the first operand; the second operand contains only the refusal return. Thus the success operand includes the failure compensation call. The note explains the intended distinction, but the actual fragment does not separate approved success from decline/failure/compensation.
- The DAO checkout continuation similarly places the success return and failure/release work sequentially across Parts F/G, relying on explanatory guards/notes rather than a containing success/failure fragment. The final general-failure plates use textual conditions; the repeated transaction-summary band by itself is not control flow.

**Why it matters:** B5 and B3 require guarded alternatives for refusal/rollback. These are the most consequential alternatives: invalid replacement must commit only withdrawal, valid acceptance must atomically change the line/totals/payment/offer, and successful checkout must retain its authorization while later failure releases it. The prose gets these rules right; the figure semantics should carry the same separation.

**Smallest correction:** preserve the existing messages, signatures and split-page identity, but make their actual vertical regions operands of `alt`/`opt`/`break` fragments. Draw the invalid-target branch, valid-target branch and their exclusive continuation explicitly; give checkout distinct COD/ONLINE approval/decline and later-failure compensation regions. Continuation pages may reference one continued enclosing fragment. Reopen affected PNG/SVG pairs and reread III/IV prose. Extend the checker beyond token presence so a fragment labelled as a branch must contain its guarded messages.

### R2 — MEDIUM: several per-UC DCDs put both multiplicities in a single detached label instead of at their association ends

**Evidence:**

- `models/UC-01/dcd_uc01_domain_links_PartA.{json,drawio,png,svg}`, Figure **3.1.2.i.R1**: Customer→Address is drawn with one text cell `1 → 0..* owns` at x=575,y=259. Its actual endpoints are x=555 and x=1035, y=298. The right endpoint has no adjacent `0..*` label. The same plate combines both end values for all six relationships (`0..1 → 1 linked account`, `1 → 0..* listings`, etc.). These are readable source-to-target summaries, but they are not the required UML end labels. The same renderer pattern is reused in UC-01/05 all-layer/final relationship plates.
- `models/UC-06/dcd_uc06_domain_PartA.{json,drawio,png,svg}`, Figure **3.6.2.i.A**: the Hub→HubMenuItem diagonal is near the upper class boxes, while its single `1 listings 0..*` label is much farther below, between the Hub and Brand areas. `1 offers 0..*` is likewise below the Brand→MenuItem line; `0..* item 1` is one mid-line label for the vertical listing→item association. The cardinalities in metadata are correct, but the visible placements do not identify the actual ends reliably.

**Why it matters:** an examiner must be able to tell which class end a multiplicity constrains. Correct relation metadata does not repair an ambiguous drawing. The subsystem plates demonstrate the required solution: **4.1BB** puts `1` at the Order end and `1..*` at the OrderLine end; ERD Part A likewise uses actual adjacent end labels.

**Smallest correction:** retain each relationship and its existing values, render two separate multiplicity labels adjacent to the two attached endpoints, and keep the role name separate. Apply the change to the affected per-UC renderer families and final projections, not to the frozen domain model. Audit actual label positions/attachments, as already done for ERD, rather than only comparing `source_multiplicity`/`target_multiplicity` metadata.

### R3 — LOW: three report III command sequences omit the successful result return

**Evidence:** `models/UC-01/seq_uc01_cancelOrder`, `models/UC-05/seq_uc05_rejectOrder` and `models/UC-05/seq_uc05_declineReplacement` (all source/export forms). Their success operands end at the domain/helper call; the only drawn return is the refusal in the alternative operand. The normalized messages agree with the images: there is no successful return message. The frozen operation catalogue requires respectively:

- OP-07: `cancelledOrderAndAmounts | refusal`;
- OP-03: `rejectedOrder | refusal`;
- OP-06: `rejectedOrderAndAmounts | staleRefusal | controlledFailure`.

**Why it matters:** B5 requests a dashed return with the result, and the diagrams call themselves complete design operations. The notes describe the effects but do not show the successful controller/view response that realizes the frozen SSD outcome.

**Smallest correction:** add the named dashed success return inside each success operand, after the atomic-save/commit qualification. Preserve failure returns and the operation identity; split if necessary to retain legibility. No new business method is needed.

### R4 — LOW: some arrow styles contradict the declared UML message/dependency role

**Evidence:**

- Figure **4.2**, `models/shared/package_diagram.drawio`: all three `dep_*` edges omit `dashed=1`; PNG/SVG show solid lines, although `IV_4-2_package.md` explicitly calls them dashed dependency arrows. B5 requires a dashed dependency arrow.
- DAO sequence method-call edges use `endArrow=open`, including `message1` (`confirm_order`) in `seqdao_uc01_confirmCheckout_PartA.drawio` and `message1` (`replace_line`) in `seqdao_uc05_acceptReplacement_PartD.drawio`. A read-only XML probe found **89 metadata-identified call edges** of this style across the DAO plates. UC-01/05 report III calls use the same open-headed style (for example `edge20` authorise in checkout Part B). These are synchronous Python calls, for which the UML call arrowhead should be closed/filled; dashed replies can retain open arrowheads. UC-06's exported sequence already distinguishes solid filled calls from dashed replies.

**Smallest correction:** set the three package dependencies to dashed in native/vector/raster output, and distinguish synchronous calls from replies in the affected sequence renderer styles. Keep navigability arrows on domain associations separate from call-arrow styling. Refresh affected exports and verify that native XML and SVG agree.

## Independent static evidence and checker limits

The exact required full command was run once, successfully, from `D:/RAD/FINAL/SaigonBite`:

```powershell
& 'C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -I -B docs/part2/_scripts/p3_design_crosscheck.py --commit 45ac76221b0a103174c7c01d17577e6e49cfd665 --read-only
```

Observed exit code **0**; `read_only=true`, `incomplete_mode=false`, `app_executed=false`; **20,297 checks, zero failures; 389 figures; 44 design-sequence views; 43 DAO views; 41 SSD occurrences; 30 anchors**. Responsibility statuses remain **10 MATCH / 28 P4-TARGET / 3 GAP**. Independent source enumeration found all five members (`.py`, `.json`, `.drawio`, `.png`, `.svg`) for each of the 389 figure stems. No separate inventory command was run.

This is a useful structural/signature check, not a semantic proof of every drawing. In `p3_design_crosscheck.py`, lines 291–298 test DAO transaction and busy tokens in SVG text, so the summary band can satisfy these checks without verifying the geometry of an actual branch. Lines 325–328 prove PC/MG IDs have a named responsibility and transaction field, not that the depicted guards/effects entail the guarantee. Final receiver checks and full signature comparison are valuable, but do not require a success return or inspect synchronous arrowhead style. Per-UC DCD relation checks compare metadata to the model; the specialized actual-end-label geometry audit is confined to ERD. These limitations explain why the passing checker does not contradict R1–R4.

The ERD regression receipt `Part2/notes/P3-root/erd_auditor_regression.json` records the four reversed multiplicities and detached endpoint in preserved originals. The current full checker includes the ERD geometry audit and passes; the current **126-check/18-FK** receipt and **328-check mapping** receipt have no failures. Current ERD Part A was opened directly and from its existing independent SVG raster; customer→account attachment and the actual adjacent end values are correct in that sample. I did not rerun a preservation/regeneration helper or create another regression artifact.

## Analysis, responsibilities and persistence assessment

The six reports provide .1–.5, all five .2 projections, CRC and final DCDs. The assembled III has the exact six frozen names, all required headings and resolved includes. The occurrence ledger has **41 occurrences / 39 UC-operation pairs / 38 op IDs**, with UC-06 listCatalogue repeated three times; the responsibility table and sequence coverage preserve this distinction. There is no justified reason to collapse the repeated catalogue occurrences or edit frozen Phase 2 analysis.

The sole model has **104 roles, 365 methods, 278 displayed attributes and 38 associations/generalizations**, and the full checker checks subsystem coverage and receiver reconciliation including visible superclass methods. Blueprint roles/routes and inferred types are grounded in the AST inventory. Domain FK scalars remain in the tables/mapping and are omitted from the DCD projection; no invented getter or view class was identified. Customer generalization and Order composition were opened in **4.1BE/4.1BB**; HubMenuItem is explicitly an association class in the model and UC-06 diagram. Per-UC relationship notation still needs R2. Pure-domain Quote fingerprint parameters use PaymentMethod/OnlineOption; property reads and implicit dataclass construction are distinguished from ordinary calls.

The model and mapping preserve real enum members, nullable archive timestamps and boolean availability/account flags. BUSY/QUIET are HubStatus properties; no fake Report lifecycle or archive enum was identified. Actual forbidden imports remain disclosed as **P3-S04/P4.9**, with 43 strict cross-layer records plus the NAV root import (44 records/23 pairs); the diagram does not claim these imports are allowed or already repaired. P4 architectural disposition remains with root/owner.

I compared the eight DAO operation sets' actual labels with frozen descriptions and selected committed AST bodies in the inventory:

| Operation | Supported contract and remaining review qualification |
|---|---|
| confirmCheckout | Token lookup precedes payment authorization; own replay skips authorization/repricing/insertion. New-token current eligibility, fingerprint AND T, raw radius, local deterministic simulator, snapshots and Payment insertion are stated. Authorization release through COMMIT failure is an explicit target. R1 needs the actual branch drawing to match these correct promises. Customer authentication is distinct from payment authorization. |
| takeDelivery | Actual AWAITING_PICKUP predicate and rowcount; paired READY→OUT_FOR_DELIVERY; rollback prior claim on later failure. No invented one-active-delivery cap. No race was executed. |
| confirmDelivered | Assigned shipper/PICKED_UP/OUT_FOR_DELIVERY guards; exact COD cash, conditional checked COD payment save; ONLINE preserves captured amount/refund owed. Paired saves and commit are stated. |
| archiveHub | Actual `id` plus nullable `archived_at` predicate; all nonterminal orders block archive; no fabricated state predicate or archive enum. |
| salesReport | SELECT-only scope, MG01 on all outcomes, active Manager gate, half-open VN→UTC finish-time filter, order-grain totals, F-03 T with separate refund owed, F-09 item identity retained. No oracle result was invented. |
| rejectOrder | Own-hub PLACED/reason guard, optional open-offer withdrawal, full captured-C refund obligation replacing a partial amount; no payout. Amount/state/helper corrections remain targets. R3 concerns the report III success response. |
| acceptReplacement | Stale/guard failures unchanged; invalid target commits only exact-offer withdrawal; valid acceptance uses offered price/whole line/same quantity, min(Dold,Snew), unchanged F/Q/C, owed C−T, Order PLACED. Correct in notes/prose; actual alternatives require R1. |
| updateMenuItem | Current parent pinned, actual active-item predicate/rowcount, duplicate/price refusal; writes menu_item only and preserves historical lines. |

No SQL or application code was executed. The targets do not establish measured atomicity, controlled busy behavior, privacy, payment correctness or numerical accuracy. The P4 register has **121 rows** and its element-specific reasons/subphases remain the handoff rather than implementation proof.

## P3-72 marking evidence or gaps

Primary authority: fresh `Part2/notes/P3-root/marking_rows.json` and `P3_primary_sources.json`, extracted from `Lec_re/RAD_Sem01_2627_MarkingSheet.xlsx`. Physical rows are not item numbers.

| Marking item / physical row | Independent evidence or scoped gap |
|---|---|
| Item 20 / Checklist row 33: author on every diagram/use case | All six III titles, native author text checked across all figures by the rerun, source/export captions, and opened examples show 722I0004 with AI assistance. Final DOCX/PDF placement is UNTESTED. |
| Item 21 / Checklist row 34: per-UC view/controller/domain/data-access DCD | III 3.1.2–3.6.2, each five projections; shared model, `uc0x_view.json`, class tables and final receiver audit. R2/R4 affect notation, not existence of the layers. |
| Item 22 / Checklist row 35: CRC or communication diagram and sequence per UC | Six `UC-0x/crc.md`; III 3.x.4; all 41 frozen occurrence pointers. CRC is the selected technique; no communication-diagram substitution. R1/R3/R4 remain specific sequence gaps. |
| Item 23 / Checklist row 36: final DCD | III 3.x.5 and corresponding final sources, changes notes, final receiver checks; IV4.1 adds complete shared declarations. R2 applies to affected final relation projections. |
| Item 24 / Checklist row 37: package diagram, mapping and SQL | IV4.2 and IV4.3.1, five ERDs, 110 primary column mappings and 18 FKs. R4 package-line correction remains. SQL excerpts in 4.3.4 are explicitly P7 pending, so this full item is not yet satisfied. |
| Part 3 item 33 / Checklist row 47: design model shown | DCD/CRC/sequence sources are available presentation inputs. Slide/video/transcript delivery and each student's explanation are pending; the row cannot be ticked as delivered by P3 design files. |
| Rubric Guide row 9, P2-III Excellent: three-layer classes | Four explicit design roles express presentation/business/data-access tiers, typed/status-aware member tables and real view modules. Actual strict-import violations remain disclosed P4 work. |
| Row 9: DCD/CRC/sequence consistent with analysis | Frozen descriptions, operation catalogue/flow membership, 30-anchor register, operation_realisation/design_consistency and exact cross-check. Required effects generally agree; R1–R3 prevent an unqualified claim about the actual diagrams. |
| Row 9: final DCD complete | Six final projections plus 4.1; all receiver methods, explicit targets, visible inherited methods and sole-model member coverage. R2 notation correction remains. No 15/15 or Excellent score is awarded by this review. |
| Rubric Guide row 10, P2-IV Excellent: correct database mapping and SQL | Static mapping/ERD evidence supplied for 4.3.1; SQL execution and final excerpts remain future evidence. |
| Row 10: code follows design | C0 correspondence is explicitly MATCH/P4-TARGET/GAP and `P4_design_inputs.csv` identifies future work. Application conformance is not complete. |
| Row 10: UI traces to SSDs | Route responsibility maps exist; actual UI/prototype/screenshot evidence is P5 pending in 4.3.3. |
| Row 10: one integrated working system | DAO/transaction design exists in 4.3.2; cross-role integration and actual results are P5 pending in 4.3.6. |
| Row 10: source files included | All 389 design source/export sets exist locally. Final packaged/tagged release/source inclusion remains P7 pending; no external delivery is inferred. |

## Scope, honesty and visual review

The controlling prompt's target-design allowance is the explicit P3 interpretation of locked-plan G3. Root has recorded that discrepancy rather than silently editing the plan. Even after these diagram corrections, G3 can mean only design readiness with disclosed P4 obligations, not running-code qualification. Full item 24/P2-IV, G4/G5/G7 and presentation delivery remain separate gates.

The assessed report text is English and uses SaigonBite-specific explanations rather than reproducing case-study paragraphs. No new lecturer answer, approval, client feedback, grade, payout or measured test result was identified in the reviewed design sources. Planned Q/L/date facts and future evidence remain pending. Authorship is Dat's actual ID, not the proposal owners' presumed work. Plan §§11–12 exclusions are respected: frozen SSDs remain system boundaries; no fake Report state, ORM, external payment/payout, notification service or communication diagram is added. These observations are scoped review findings, not a forensic plagiarism or all-facts certification.

Direct image inspection included the dense/error-prone checkout III Part B; checkout DAO Part A; replacement DAO Parts C/D; cancel/reject III sequences; UC-06 item update and domain/view DCDs; UC-04 deliveryReport; subsystem composition/generalization; the package diagram; and ERD Part A. Existing independent SVG evidence opened included `Part2/notes/P3-E/dcd_subsystem_PartAC_svg.png`, `Part2/notes/P3-F/paired_sheet_08.png`, and the current root ERD Part A SVG raster. These samples reveal the findings above while confirming usable text/compartments in the inspected plates. I did not independently open all 389 PNGs and SVG rasters; workers' all-image receipts are provenance, not a replacement claim that this reviewer viewed every image. The full checker independently checks declared native/vector minimum fonts at the declared 170/230 mm placement and required source members. Actual final document scaling remains UNTESTED.

## Checklist delivery, BLOCKED / ASSUMED and open items

- **P3-70: review performed**, with the independent verdict and R1–R4 above. This records completion of the review task, not a clean artifact verdict or an edit to the root-owned checklist.
- **P3-72: evidence/gap assessment supplied** in the table above, including physical rows and all P2-III/P2-IV Excellent criteria.
- **P3-71 and G3 closure remain root work:** disposition each finding separately, preserve this verdict verbatim, regenerate/reopen changed artifacts, assemble, strengthen/rerun appropriate static checks and record root's post-fix assessment separately.
- **BLOCKED / ASSUMED:** no access blocker. The integrated revision identifier is supplied by root; application C0 is independently used by the fresh read-only cross-check. No application runtime qualification is inferred from any count.
- Native draw.io opening/editing, native Excel, final DOCX/PDF placement and final upload/tag/release remain **UNTESTED / pending**. End protected-byte checks, staging, AI-log reviewer entry and transcript archive are root-owned closure tasks; this lane does not manufacture their receipts.
- Recommended escalation is the existing root integration lane for bounded diagram repairs. No architectural decision, additional reviewer, network action or application experiment is needed to resolve these findings.

## Files written and sources used

**Only file written:** `docs/part2/_agent_reports/P3-review.md`. No scratch, helper, log, renderer output, cache, test, SQL, installation or network artifact was created. No child agent was spawned. The exact authorized cross-check internally reads committed blobs; no separate Git command was issued.

Sources: full `Part2/notes/P3-root/controlling_prompt.txt`; locked `PLAN_SaigonBite_Part2_Final.md` §§2–5/P3/P4/P5/P7/7.3/10–12; Part2 README, links and P3 checklist; fresh primary Requirements PDF, Case Study PDF, template and marking extracts in `P3_primary_sources.json` and exact `marking_rows.json`; supplied balanced-diagrams skill extract; six frozen descriptions, SSD operation/occurrence ledger, PC/MG/analysis-consistency registers, domain/state/SSD JSON/XML; actual integrated III/IV/class/CRC/model/annotation/mapping/trace/target sources; static AST bodies in `code_inventory.json`; checker source and fresh stdout; current ERD/mapping/visual receipts and selected existing image proofs. P2/P3 brief/root/worker reports were read as context, not proof of their PASS conclusions. A lightweight memory registry read was used only to locate prior project scope and the warning to reverify historical facts; all substantive findings above use current files.
