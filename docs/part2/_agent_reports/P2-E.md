# Phase 2 E completion — UC-01 and UC-05

Author: 722I0004 · AI-assisted (Codex)

24/10/2026 (Asia/Bangkok). **Complete within the assigned E write set:** P2-31–35 and P2-51–55. Analysis artifacts only; no app/test/database execution, git command, shared-file edit, external contact, further agent or configuration change was performed. The updated P2 brief and root Wave 1 dispositions were read first; the root's uncommitted integration notes were treated as authoritative for this wave.

## Files written

- `docs/part2/UC-01/description.md`; `docs/part2/UC-05/description.md`.
- `docs/part2/report/II_2-2-1_UC-01.md`; `docs/part2/report/II_2-2-5_UC-05.md`.
- `models/UC-01/activity_uc01` and `ssd_uc01`, each unsuffixed and `_PartA`, `_PartB`, `_PartC`, each with `.py`, `.json`, `.drawio`, `.png`, `.svg`.
- `models/UC-05/activity_uc05` and `ssd_uc05`, with the same formats and Parts A–C.
- This completion report `docs/part2/_agent_reports/P2-E.md`.

The unsuffixed editable `.drawio` contains all three pages; unsuffixed PNG/SVG are declared Part A aliases. Use all A–C report figures, not only those aliases. The owned generator copies are self-contained and regenerate the entire E diagram bundle, using the bundled Python `-Xutf8 -I`; they do not import or edit a shared renderer. Geometry JSON exposes all action/decision/message IDs. Exact written-file hashes are in `D:/RAD/FINAL/Part2/notes/P2-E/owned_manifest.json` (84 package files before this completion report).

Scratch helpers, primary extracts, self-check data, consistency rows, independent SVG renders, A4 proofs, Edge stdout/stderr logs and profiles are confined to `D:/RAD/FINAL/Part2/notes/P2-E/`. Hidden subprocesses preserve logs and return codes; no external console window was launched.

## Checklist evidence

| Checklist | Done evidence |
|---|---|
| P2-31 | UC-01 description: exact nine template fields/order; numbered Actor/System steps 1–9; A01–A05/E01–E05; all nine UC01 anchor texts verbatim; F01 explicitly identifies supporting tracking/cancel scope. |
| P2-32 | Activity Figures 2.10A–C: quote refusal/busy, consent and pre-transaction chooser, explicit payment merge, token replay, transaction revalidation, deterministic payment, atomic commit/rollback and MG outcomes. |
| P2-33 | SSD Figures 2.11A–C: exact OP-13/14/15/01/16/17/07 signatures, query loop, mutually exclusive checkout-result alt, optional supporting receipt/tracking/cancel fragments; dashed returns; Customer + :System only. |
| P2-34 | `II_2-2-1_UC-01.md`: required i–iv headings, one description include, activity/SSD A–C figures, Order/Payment owner references and nine-row PC/MG→state/fact table. |
| P2-35 | This report plus `selfcheck.json`, `consistency_rows.csv`, `generation_qa.json`, `visual_qa.json`; 9/9 UC01 anchors mapped below. |
| P2-51 | UC-05 description: nine fields; main confirm 1–5; A01–A05/E01–E04; separate SUC-03 C1–C6; five anchor texts verbatim; source/target/exact-open and all §3.3 money rules. |
| P2-52 | Activity Figures 2.18A–C: kitchen choice + explicit merge, own-hub/command guards + commit, guarded replacement source/target/create, independent Customer response context and atomic money effects/rollback. |
| P2-53 | SSD Figures 2.19A–C: Kitchen staff + :System main fragment; separate Customer + :System acceptance and decline companion fragments; all nine catalogue requests and all response alternatives. |
| P2-54 | `II_2-2-5_UC-05.md`: required i–iv headings, include, A–C figures, ReplacementOffer owner reference, shared Order/Payment references and five-row PC/MG→state/fact table. |
| P2-55 | This report and the same self-check/visual bundle; 5/5 UC05 anchors mapped below; every query and command has an explicit flow membership entry. |

## PC/MG consistency rows for root

Program checks passed: **14 verbatim anchors; 16 request messages; 12 unique figure pages; 11 guarded decisions; zero missing IDs, missing flow operations, parameter mismatches, XML connection errors or action-text overflows.** The table below is also available as `D:/RAD/FINAL/Part2/notes/P2-E/consistency_rows.csv`. PC/MG wording is unchanged.

| Anchor | Verbatim text | Description steps | Activity node IDs | SSD message IDs | Shared state / fact |
|---|---|---|---|---|---|
| UC01-PC01 | one PLACED order owned by the customer | 7–8 | 01C-W;01C-S | 01S-M04;01S-R04b | 2.3A creation/customer identity |
| UC01-PC02 | lines with snapshot names/prices | 7–8 | 01C-W;01C-S | 01S-M04;01S-R04b | 2.3A line snapshots |
| UC01-PC03 | address snapshot + distance | 3;6–8 | 01A-6;01C-V;01C-W;01C-S | 01S-M03;01S-M04;01S-R04b | 2.3A address snapshot/distance |
| UC01-PC04 | S/D/F/Q/T stored and consistent | 3–4;6–8 | 01A-6;01B-4;01C-V;01C-W;01C-S | 01S-M03;01S-M04;01S-R04b | 2.3A stored S/D/F/Q/T |
| UC01-PC05 | payment PENDING (COD) or PAID (ONLINE, amount C) | 7;A02 | 01B-ON;01C-P;01C-D2;01C-W;01C-S | 01S-M04;01S-R04b | 2.4A/B COD PENDING / ONLINE PAID C |
| UC01-PC06 | hub load +1 | 6–8 | 01C-V;01C-W;01C-S | 01S-M04;01S-R04b | 2.3A PLACED in load set |
| UC01-MG01 | refused/declined/invalid → no order, no payment, no line | E01–E05 | 01A-E;01C-E;01C-DECL;01C-ROLL | 01S-M04;01S-R04c;01S-R04d;01S-R04e | 2.3A/2.4 no creation on refusal |
| UC01-MG02 | replay → same single order | 5;A01 | 01B-T;01B-D2;01B-RE | 01S-M04;01S-R04a | 2.3A retained token-owned identity |
| UC01-MG03 | busy → suggestions, nothing saved | E02;A03 | 01A-E;01C-E | 01S-M03;01S-R03;01S-M04;01S-R04c | 2.3A busy guard no transition |
| UC05-PC01 | confirm: own-hub PLACED → CONFIRMED | 3–5 | 05A-V;05A-G;05A-S | 05S-M03;05S-R03 | 2.3A PLACED→CONFIRMED |
| UC05-PC02 | reject: REJECTED + reason + BR-17 + offer WITHDRAWN | A02 | 05A-V;05A-G;05A-S | 05S-M04;05S-R04 | 2.3A reject;2.7B withdraw;2.4A/B BR17 |
| UC05-PC03 | offer: one OFFERED offer per §3.3 | A03 | 05B-V;05B-D;05B-O | 05S-M05;05S-R05 | 2.7A OFFERED;2.3B PLACED retained |
| UC05-PC04 | accepted offer applied per §3.3 5–7 | C3–C5 | 05C-V;05C-D;05C-M;05C-COMMIT;05C-S | 05S-M08;05S-R08a | 2.7A ACCEPTED;2.3B line/totals;2.4A/B amount |
| UC05-MG01 | wrong hub / open offer / stale / invalid target → order unchanged | E01–E04 | 05A-E;05B-E;05C-E;05C-ROLL | 05S-M03;05S-M05;05S-M08;05S-R08b;05S-R08c | 2.3B no Order transition;2.7B exact-offer withdrawal |

## Every SSD request is in its description flow

Returns have `R` IDs and dashed arrows; the request `M` IDs below are the complete operation membership list, including queries. Catalogue parameters are checked after whitespace normalization only; no parameter is omitted or renamed. No controller, DAO, SQL call or uncatalogued simulator message appears.

| UC | SSD message | Catalogue operation | Exact parameters | Description steps |
|---|---|---|---|---|
| UC-01 | 01S-M01 | OP-13 `browseHubs` | `(none)` | 1 |
| UC-01 | 01S-M02 | OP-14 `selectHub` | `hubId` | 2 |
| UC-01 | 01S-M03 | OP-15 `requestQuote` | `hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?` | 3;A03/A04 |
| UC-01 | 01S-M04 | OP-01 `confirmCheckout` | `hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?, simulatorOutcome?, quoteFingerprint, quotedTotal, checkoutToken` | 5–8;A01/A02;E01–E05 |
| UC-01 | 01S-M05 | OP-16 `viewReceipt` | `orderId` | 9;F01 |
| UC-01 | 01S-M06 | OP-17 `viewMyOrders` | `(none)` | F01 (UC01) / C1 (UC05) |
| UC-01 | 01S-M07 | OP-07 `cancelOrder` | `orderId` | F01 / SUC-04 |
| UC-05 | 05S-M01 | OP-19 `viewKitchenOrders` | `(none)` | 1;A01/A04 |
| UC-05 | 05S-M02 | OP-20 `viewKitchenOrder` | `orderId` | 2;A01/A04 |
| UC-05 | 05S-M03 | OP-02 `confirmOrder` | `orderId` | 3–5 |
| UC-05 | 05S-M04 | OP-03 `rejectOrder` | `orderId, reason` | A02 |
| UC-05 | 05S-M05 | OP-04 `offerReplacement` | `orderId, orderLineId, targetItemId` | A03 |
| UC-05 | 05S-M06 | OP-17 `viewMyOrders` | `(none)` | F01 (UC01) / C1 (UC05) |
| UC-05 | 05S-M07 | OP-18 `viewReplacement` | `orderId` | C1 |
| UC-05 | 05S-M08 | OP-05 `acceptReplacement` | `orderId, offerId` | C3–C5 |
| UC-05 | 05S-M09 | OP-06 `declineReplacement` | `orderId, offerId` | C6 |

## Guard and notation review

Each decision's full predicate is the adjacent validation/transaction action plus its diamond label. A boolean pass/fail or yes/no pair is complementary; a finite user/payment choice is exhaustive after input validation. Refused values outside those choices follow the description E flow before that decision. Merges are explicit; no concurrency/fork/join is invented. All final symbols are activity finals for this sequential scope; offer creation continues through a connector to the separately initiated Customer response without holding a transaction.

| Decision ID | Outgoing guards | Completeness / effect check |
|---|---|---|
| 01A-D | [not eligible]; [eligible] | Eligible quote vs any invalid/busy quote; refusal saves nothing. |
| 01B-D1 | [ONLINE]; [COD] | Validated method is exactly COD or ONLINE; chooser stays in Actor partition, before transaction; both paths merge at 01B-M. |
| 01B-D2 | [own token found]; [no own token] | An owned token is found or not; foreign token reaches refusal in 01C-V/D1; no foreign order disclosure. |
| 01C-D1 | [no]; [yes] | All request/ownership/capacity/radius/menu/voucher/fingerprint+T guards match or do not match. |
| 01C-D2 | [ONLINE declined]; [COD or ONLINE approved] | Validated COD or approved ONLINE permits creation; declined ONLINE does not. |
| 01C-D3 | [failed]; [committed] | All writes through COMMIT succeeded or failed; failure rolls back and releases simulated authorization. |
| 05A-D | [confirm]; [reject]; [offer] | Staff selects exactly confirm, reject or offer; confirm/reject merge at 05A-M before selected-command validation. |
| 05A-G | [fail]; [pass] | Selected own-hub PLACED command guards and atomic commit pass or fail; rejected command/rollback preserves Order. |
| 05B-D | [fail]; [pass] | All §3.3 creation guards plus atomic save pass or fail; successful result is exactly one OFFERED. |
| 05C-D | [no]; [yes] | Active owner + own PLACED + exact open offer; ACCEPT additionally needs current target eligibility; DECLINE does not require target availability. Complement routes stale/no-write or exact-offer withdrawal only. |
| 05C-COMMIT | [failed]; [committed] | Selected response and all money/line/offer effects commit together or roll back together. |

UC-01 retains Figure 2.1A's actual include/extend choices: mandatory Validate accepted checkout; ONLINE Simulate online payment at payment authorization; SUC-04 extends SUC-03 at order action selected. Other serving links remain serving links. The external simulator subgoal is described, while SSD exposes only confirmCheckout and no new simulator API.

UC-05 retains source **currently unavailable**, own-hub PLACED, one exact open offer, target same-hub active/listed/AVAILABLE/not another line, offered price ≤ source snapshot, same quantity, cross-brand allowed. Acceptance uses offered price even after catalogue price change; voucher concession is min(D_old,S_new), terms not re-evaluated; F/Q unchanged; COD new T; ONLINE C unchanged/PAID with owed=C−T_new. Invalid-target acceptance changes only the offer to WITHDRAWN and returns a reason. Decline applies REJECTED + BR-17; cancellation after acceptance owes full C, never C+partial. Stale responses never revive cancelled/rejected orders. These are model contracts, not measured outcomes.

## Visual QA and limits

All **16 PNG exports** (12 unique pages + four first-page aliases) and **all 16 SVG exports independently rendered by hidden Edge** were opened and visually inspected. Earlier layout faults (footer clipping, crowded Customer SSD alternatives and long response text) were corrected before final inspection; Customer decline has its own 2.19C fragment to preserve legibility. Final original PNG and independent SVG renders agree in content and routing, with normal font rasterization differences.

Each figure uses a 1600×1200 canvas (4:3) and minimum 26 px Arial. At 230 mm placed width this is **26×230/1600×72/25.4 = 10.59 pt**; do not reduce to a 170 mm portrait column (7.83 pt). A4 landscape proofs are saved for every export and independent render at 300 dpi, 230 mm image width. XML parse/native edge-reference checks and action text-fit checks passed. Every figure has the required author spelling and caption. No native draw.io editing/reopen or assembled final DOCX/PDF print result is claimed; final report assembly placement is root-owned.

Evidence: `visual_qa.json` lists every PNG/SVG render and its opened/inspected disposition; `*_from_svg.png`, `*_A4_png.png`, `*_A4_svg.png`, and `*_edge.log` retain the proofs and process logs. `generation_qa.json` contains geometry/readability checks. `selfcheck.json` contains template/anchor/signature/native-connection/final-node/text-fit evidence.

## BLOCKED / ASSUMED

- No E-scope blocker remains. Unanswered Q/L values remain team defaults, never lecturer approval; no external question or contact was sent.
- PC01–PC06 for UC-01 are creation-boundary postconditions. UC01-MG01 is relative to a refused checkout attempt and does not delete a previously saved order. F01 cancellation failure uses SUC-04's existing zero-change failure invariant; no false claim that a prior Order disappears is made and no new shared PC/MG is proposed.
- Kitchen request completion and Customer response are distinct sessions. The activity's connector continues the overall goal; no transaction is held during the Customer choice. SSD 2.19B/C explicitly use a single Customer actor, separate from 2.19A.
- Invalid-target withdrawal reason is an operation result/message only, consistent with root's Wave 1 rejection of a new persisted attribute.
- Shared state machines and every Wave 1 file remain read-only. Existing Static F-02/F-04/F-05/F-07/P2-S05 gaps remain later P4 obligations; no code fix or test pass is claimed.

## Requests to root

1. Inject C's existing `BEGIN/END STATE_MACHINE ORDER` and `PAYMENT` blocks once under UC-01 iv, and `REPLACEMENT_OFFER` once under UC-05 iv, using the actual marker spelling in `II_state_machines.md`. The owned report parts already provide named figure references and local PC/MG tables; no state figure was copied or modified by E.
2. Integrate the 14 consistency rows above / scratch CSV and all 16 request-flow membership rows into root's `analysis_consistency.csv`. The query rows are intentional.
3. Retain all activity/SSD Parts A–C for Figures 2.10/2.11/2.18/2.19 at 230 mm landscape during assembly. The extra 2.19C is a Customer decline companion fragment, not another UC or operation.
4. No additional operation, PC/MG, persisted field or shared-catalogue change is requested. Checklist/workbook/AI-log/assembly/git updates remain root-owned. No other open E implementation item remains.

## Sources used

- Locked `D:/RAD/FINAL/PLAN_SaigonBite_Part2_Final.md`: §§1–5, P2/P3.1, §§7/10/11; Part2 README, content/links.json and codex/P2_CHECKLIST.md.
- First-read updated `docs/part2/_agent_reports/P2-brief.md` and `P2-root.md`, including final Wave 1 dispositions; `rules.md`, `decision_log.md`, `pc_mg_register.csv`, `ssd_operations.csv`.
- Direct primary `Lec_re/` Requirements and Case PDFs (pypdf), Report_Template.docx (python-docx nine-field table), MarkingSheet.xlsx and Team_Workbook_Template.xlsx selected sheets (openpyxl). Durable extracted data: `Part2/notes/P2-E/primary_reading.json`; root's direct-source `Part2/notes/P2_primary_sources.json` was also read.
- Frozen Part1_v2 content master, diagram_changes.md, models/style, build/proc_build.py, proc_geom.py and proc_views.py (read only); balanced-diagrams ZIP's `balanced-diagrams/SKILL.md` read with zipfile. Owned renderer adapts only the geometry/font/export pattern from read-only Wave 1 `models/shared/use_case_diagram.py` and `sm_order.py`.
- Wave 1 report 2.1, Figure 2.1 relations/domain model, SUC contracts, reconciled CRUD and `II_state_machines.md` / Order, Payment and ReplacementOffer data; no other worker completion report was opened.
- Draft PlaceOrderController, KitchenController, Order/OrderLine/Payment/ReplacementOffer domain declarations and schema v2 read only for **Static** vocabulary/mapping, never as proof of contract compliance.

All resulting artifacts are English with actual author 722I0004 and declared Codex assistance. No team-member work or scientific/application result was invented.
