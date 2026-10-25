# Phase 3 lane A — UC-01 and UC-05 design packages

Author: 722I0004 · AI-assisted (Codex)

**Wave 4 update (26/10/2026):** The bounded UC-01/UC-05 R1–R4 repairs and changed-image QA are complete. Read the appended **Independent review repair R1–R4** section for current counts, evidence and the continuation-checker request; earlier delivery/integration entries are retained as history.

**Integration update:** R-A01–R-A05 were adopted by root and the bounded repair is complete. The final **Integration repair** section supersedes the initial-delivery pending statements below; those statements are retained as history.

25/10/2026, Asia/Bangkok. Committed code baseline C0: `45ac76221b0a103174c7c01d17577e6e49cfd665`, supplied by root and matched to the inventory/model. Evidence is **Static / target design**. No application import, execution, tests, database initialization, Git command, configuration change, external action, deletion or child agent was used.

The lane artifacts and local checks are delivered. **Root-owned reconciliation remains necessary before a global G3 pass:** requests R-A01–R-A05 below concern the shared signature, dependency resolver/model and responsibility annotations. This report does not qualify those unresolved shared inputs as correct implementation.

## Files written

- `docs/part2/UC-01/design_classes.md`, `crc.md`; `docs/part2/UC-05/design_classes.md`, `crc.md`.
- `docs/part2/design/uc01_view.json`, `uc05_view.json`: explicit shared-model class/member selections and ordered figure lists.
- `docs/part2/report/III_3-1_UC-01.md`, `III_3-5_UC-05.md`: exact 3.x / .1–.5 headings, .2 i–v, include directives, figures/captions and per-operation realization/guard/effect tables.
- `models/UC-01/dcd_uc01_*`, `seq_uc01_*`; corresponding `UC-05/dcd_uc05_*`, `seq_uc05_*`. Every actual plate has its own `.py`, `.json`, `.drawio`, `.png` and `.svg`. There are **127 plates: 108 DCD member/relationship projections and 19 sequence parts**. UC-01 has 67 plates; UC-05 has 60. The 19 sequence parts preserve **all 16 SSD occurrences: UC-01 seven, UC-05 nine**. Parts do not introduce another operation/request.
- This report. Total canonical lane files: **644**, including this report; exact generated paths are in `D:/RAD/FINAL/Part2/notes/P3-A/generation_manifest.json` (643 paths before this report). No unreferenced owned JSON stem remains.

Scratch and QA evidence are confined to `D:/RAD/FINAL/Part2/notes/P3-A/`. There are no writes to shared design sources, frozen Phase 2 files, Part 1, application/tests/schema, workbook, checklist, plan, links or staging.

## Checklist IDs and evidence

| ID | Worker disposition / evidence |
|---|---|
| P3-10 | Delivered: UC-01 `design_classes.md`; 44 selected real classes/modules/value types/enums; full selected signatures, all inventoried attributes, visibility, inferred flags and method-specific status/P4 inputs. |
| P3-11 | Five filtered views delivered via `uc01_view.json`; typed member plates plus navigable relationship plates, Order composition, Customer generalization, HubMenuItem association-class label, both multiplicities and enum dependencies. Shared reconciliation R-A01–R-A03 remains root-owned. |
| P3-12 | Delivered: UC-01 `crc.md`; real AST targets and typed collaborators. Local `order` variables resolve to Order, never to the `order` blueprint. |
| P3-13 | Delivered: `seq_uc01_*`; seven exact SSD occurrences in nine plates, including full fingerprint/T consent, replay, busy suggestions, local simulator, creation and release-through-COMMIT targets. Supporting cancellation uses SUC04-PC01/02 and its own unchanged-order failure invariant. No DAO/SQL lifeline. |
| P3-14 | Final selected member/relationship DCD delivered, with changes note. Every displayed call/SSD adapter receiver method resolves in the final DCD; implicit dataclass construction is separately checked. Root must add the real missing navigation dependencies in R-A02. |
| P3-15 | Exact UC-01 report source/includes/captions delivered; 230 mm landscape, 9.78 pt minimum; PNG/independent SVG visual QA evidence below. |
| P3-16 | Delivered: UC-05 `design_classes.md`; 37 selected classes/modules/value types/enums, same full-table rules. |
| P3-17 | Five filtered UC-05 DCD views delivered via `uc05_view.json`; shared dependency reconciliation R-A02/R-A03 remains. |
| P3-18 | Delivered: UC-05 `crc.md`; KitchenController / OrderTrackingController / real module helpers and collaborators, including target behavior markers. |
| P3-19 | Delivered: `seq_uc05_*`; nine exact occurrences in ten plates. Customer response is a separate SUC-03 request; acceptance is not confirmation. Source/target/exact-open guards, offered price, unchanged quantity, preserved C and refund owed, invalid-target withdrawal-only, stale refusal and rollback are explicit. |
| P3-20 | Final DCD delivered; receiver-method checks pass locally. Real navigation omitted by the shared AST resolver requires R-A02 before global consistency qualification. |
| P3-21 | Exact UC-05 report source/includes/captions and this report delivered; visual/readability evidence below. |

These are worker evidence dispositions, not edits to the root-owned checklist and not a claim that the shared cross-check or G3 has passed. In particular, P3-11/14/17/20 still require root disposition/regeneration of the named shared-model requests.

## Design and semantic checks

`semantic_qa.json` records zero local errors across 127 plates. It checks valid XML and connected native edge IDs; all selected classes/attributes/methods against the shared model; exact operation ID/name/parameters/SSD pointer membership; all call and SSD adapter receiver methods in the UC's final DCD; property reads never represented as method calls; genuine dataclass construction; no DAO/Database lifeline in Section III; guarded failure result; and no upward dependency arrow in the layered projections. **This is a document/model check, not an application test.**

The class tables retain FK identifiers for accurate static mapping; domain diagram attributes omit them in favor of the frozen model associations. Diagrams project four non-FK fields per class for readability; full table fields remain available. Properties retain their source signatures with an explicit “read as .property” note. Blueprint nodes are the actual `order` and `kitchen` modules and route functions, with HTTP adapters in the report. Templates are listed as resources, never invented classes.

The all/final member projection is ordered view → controller → domain → data access and split at layer boundaries. Relationship plates use downward dashed dependencies; composition has a filled diamond and generalization a hollow triangle in both raster and vector exports. Source exclusions are displayed as notes, never drawn as allowed calls. Repeated class identities on separate plates are the same shared-model class. No new getters, business constructors, persistent Quote/report/receipt row, Busy/Quiet enum, refund payout or notification mechanism was invented.

Every JSON includes the common `phase3` contract. Sequence metadata preserves the exact catalogue parameter string and ledger pointer even on a continuation. Messages distinguish external SSD adapter invocation, real call, return and implicit `create`. State metadata records the enum values actually displayed in the plate. A target method retains † and the P4 input legend; MATCH means Static correspondence only.

## Visual QA

All **127 PNGs and 127 independently rasterized SVGs** were opened through **32 paired inspection sheets**, with lower-half/caption detail and additional full-size checks of the denser checkout, quote, controller and acceptance plates. The independent renderer is hidden Microsoft Edge, using an owned profile and captured stdout/stderr/exit status. Every render completed with a valid 1600×1200 image. The final changed checkout/cancellation/decline plates were reopened at full size in both forms.

Retained evidence:

- `visual_qa.json`: per-plate source and independent-render paths, SHA-256 hashes and inspection status.
- `inspection_sheet_01.png` … `inspection_sheet_32.png`: paired PNG / independently rendered SVG plus lower-half detail for every plate.
- `<stem>_from_svg.png`, `<stem>_A4_PNG.png`, `<stem>_A4_SVG.png`: independent raster and 300-dpi A4 landscape placement proofs.
- `<stem>_edge.log`: captured hidden-renderer output.
- `semantic_qa.json`, `excluded_upward_candidates.json`, `source_receipts.json`, `generation_manifest.json`, `final_receipt.json`.

Minimum font is **24 px × 230/1600 × 72/25.4 = 9.78 pt** at the prescribed **230 mm landscape** image width. Do not place these plates in a 170 mm portrait column. The source has text-fit/card-bound assertions. Checked exports show matching geometry/text, connected arrows, intact compartments and unclipped captions. Mutual continuation notes point to existing member/relationship plates; earlier dangling `view_links` / `controller_links` / `dao_links` wording was corrected.

**Native draw.io editing/reopen, native Excel and final DOCX/PDF placement remain UNTESTED.** This lane did not assemble or export the final report.

## BLOCKED / ASSUMED

- **Shared-source boundary:** no root-owned annotation, inventory, realisation row or design model was edited. Existing target signatures were faithfully projected, including the domain impurity identified in R-A01. The lane cannot independently close that shared mismatch.
- **Smallest faithful projection:** class tables carry all attributes and selected UC methods; figures carry a readable member filter and relationship projections rather than reducing the type size. The large all/final set is intentionally split. Root may choose appendix placement at final report assembly; no final pagination is asserted.
- **Implicit construction:** dataclass `create` messages show real initialization with a field/value note. They do not add an `__init__` business method to the final DCD.
- **Source facts:** default business rules and unanswered lecturer/client facts remain defaults, never approval. No time, execution result, grade or contribution by another member was invented.
- **Liveness:** the same lane identity resumed on root instruction after the reported usage interruption; existing drafts were preserved. No replacement agent or configuration change was used.

## Requests to root

| Request | Required root disposition / evidence / affected surface |
|---|---|
| **R-A01 — pure-domain fingerprint signature** | The current root target `Quote.fingerprint(self, payment: PaymentChoice) -> str` points from the domain to a controller value type. Please replace it with domain enum inputs, e.g. `fingerprint(self, payment_method: PaymentMethod, online_option: Optional[OnlineOption] = None) -> str`, retaining GAP / F-07 / P4.3. Controller callers adapt `PaymentChoice` into its method/option. Add Quote → PaymentMethod/OnlineOption typed dependencies. Regenerate the UC-01 domain/all/final cards, class table, requestQuote Part B and confirmCheckout Part A labels/metadata/prose after adopting the exact root signature. No shared edit was made here. |
| **R-A02 — real navigation omitted / blueprint-name collision** | The AST resolver incorrectly treats local variable `order` as the `order` blueprint, producing controller → view candidates. Remove `controllers.common → order`, `KitchenController → order`, `OrderTrackingController → order` as call dependencies; inspect the analogous DeliveryController/local `delivery` collision globally. Add the actual direct call dependencies already evidenced by C0 `body_ast`: `controllers.common → Order` (`order.move_to`), `controllers.common → Payment` (`payment.release_for_unfulfilled_order`), `PlaceOrderController → Hub` (`hub.distance_to`), `PlaceOrderController → Voucher` (`voucher.problem`, `discount_for`), `PlaceOrderController → domain.rules` (fee/quiet functions), `OrderTrackingController → Order` (`replace_line`), and `KitchenController → Order` (`line`). These seven absent navigations are used by the correct sequences; the root-owned shared model must supply them before final DCD navigation consistency can pass. Own relation plates exclude the false upward arrows and record the reason. |
| **R-A03 — layered diagram filter versus mapper typing** | `allowed_on_layered_diagram` currently also admits DAO → domain mapping/type dependencies. B5 requires downward application arrows in these per-UC projections. The lane omits those upward arrows and displays exclusion notes; `excluded_upward_candidates.json` lists the exact candidates/plates. Preserve real DAO construction/type imports for the actual-import assessment in 4.2 and the persistence mapping; do not automatically call every mapper type reference an application-layer runtime violation. Root should apply one consistent filter across A/B/C/E, then regenerate the accepted relation set. |
| **R-A04 — persist the full refund obligation in the helper target** | C0 `controllers.common.release_payment` calls the Payment method and `PaymentDAO.change_state`, but does not persist `refund_amount`. Merely changing the domain method under F-02 does not save C. Mark the helper behavior as P4-TARGET under existing F-02/P2-S01, P4.4, and require checked persistence of amount/refund_amount atomically with state (the existing annotated `PaymentDAO.set_amounts` target). Keep its real signature. Affected cancel/reject/decline sequences call the real helper and already show full-C target behavior; regenerate helper method daggers in the DCD/table/CRC after root adoption. |
| **R-A05 — modifying-operation responsibility anchors** | `operation_realisation.csv` currently labels UC-01 cancelOrder and UC-05 declineReplacement as “Read authorization / no persistent effect …”. They are write operations. Please replace this text with SUC04-PC01/02 plus the SUC-04 unchanged-order/offer/payment failure invariant for cancellation, and the UC05-MG01 / §3.3(8) decline + BR-17 outcome for decline. The lane's cancellation figure uses supporting anchors and explicitly says those PCs are not reached on refusal; it does not misuse checkout MG01 to erase a previously saved order. Preserve the frozen P2 catalogue/register and add no new anchor ID. |

No new application method beyond root's existing target was proposed. R-A02 is static dependency-resolution correction; R-A04 uses existing P4 input IDs, not a new scientific or runtime finding. The full global cross-check and final P4 handoff remain root-owned.

## Sources used

Complete controlling Phase 3 attachment; locked final plan §§2–5, P3/P4, 7.3 and 10–12; Part2 README, links and P3 checklist; the root's fresh primary extracts (`P3_primary_sources.json`) for report template, Requirements/Case Study, marking/workbook criteria and the supplied **balanced-diagrams** skill; frozen Part1 `content_master.md`, `proc_geom.py`, `diagram_changes.md` for reference/style; P3 brief/root, P2 brief/root/review, UC-01/05 descriptions, immutable SSD/domain/state outputs, operation catalogue/flow ledger, PC/MG/consistency tables and supporting SUC-04 contract; C0 AST inventory, operation realisation, design annotations and the one shared design model. No application module was imported or run. Hashes of the main local source inputs are retained in `source_receipts.json`; root owns the full frozen-boundary end check.

The local end comparison found 19/20 recorded input hashes unchanged. The sole change was root-owned `P3-root.md`; rereading it confirmed the added usage-interruption/same-identity recovery record. Shared inventory/annotations/model and the frozen analysis inputs in this receipt stayed unchanged. This worker did not edit the root report.

## Reproduction and remaining root work

Each checked-in diagram generator is standalone and reads its adjacent JSON. Example:

```powershell
& 'C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -I 'D:/RAD/FINAL/SaigonBite/models/UC-01/seq_uc01_confirmCheckout_PartA.py'
```

Local lane document check:

```powershell
& 'C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -I 'D:/RAD/FINAL/Part2/notes/P3-A/qa_lane.py'
```

Use the persistent per-plate JSON/renderer for reproducing the delivered exports. The scratch authoring builder preceded the documented post-filters/polish; a wholesale scratch rebuild must reapply `filter_upward.py`, `fix_continuations.py`, `final_semantic_polish.py` and `final_visual_polish.py`, then refresh actual displayed-state metadata. Root should instead regenerate accepted shared-model changes consistently from its single authoritative model and view selections. Do not present a local name/signature check as the full root cross-check.

Root next: accept/refuse each request, update shared sources, regenerate the affected member/navigation/sequence/prose projections, repeat visual checks on changed exports, run the global cross-check, assemble III/IV and commit explicit paths. No upload, push, tag or merge was performed.

## Integration repair

Author: 722I0004 · AI-assisted (Codex)

Completed in the same lane/identity against root's corrected, frozen shared model. No historical sequence builder was run. The existing JSON plates were refreshed in place, preserving all 19 polished sequence parts: exact SSD IDs/names/parameter strings/pointers, lifeline order, branch frames, main denial/rollback paths, continuation text and message count. The longer pure-domain fingerprint binding received only the extra label clearance required to keep it below the self-call loop. Application code/imports/execution/tests, Git, shared writes and child agents remained outside this repair.

### Adopted changes

| Original request | Applied repair |
|---|---|
| R-A01 | Quote now shows `fingerprint(self, payment_method: PaymentMethod, online_option: Optional[OnlineOption] = None) -> str` with GAP† / F-07. Both caller plates use `fingerprint(payment.method, payment.option)`. Quote's CRC identifies the two domain enum collaborators; no controller type is a Quote parameter or outward dependency. |
| R-A02 | Rebuilt relationship projections from the corrected shared source, with duplicate keys combined conservatively. Correct Order/Payment/Hub/Voucher/rules navigation replaces the false local-variable → blueprint candidates. Every call/create navigation used in the UC-01/05 sequences now occurs in that UC's final DCD. Same-layer controller/helper/response-value creation dependencies are included where actually used. |
| R-A03 | All projected dependency arrows obey the shared downward-direction flag. DAO mapping/type references remain in the authoritative model/import assessment; they are absent from the allowed application-call projection. Obsolete source-exclusion notes were replaced by the corrected relations. |
| R-A04 | `controllers.common.release_payment` is P4-TARGET† in cards, tables, CRC and messages, with F-02/P2-S01/P3-S03. The prose states checked, atomic persistence of the full captured-C refund amount together with state. No current implementation of that target is claimed. |
| R-A05 | Cancellation now maps to SUC04-PC01/02 and its own unchanged Order/offer/payment failure invariant. Decline maps to SUC03-PC04 and UC05-MG01. Both reports include an explicit controller/boundary/guarantee/status table derived from corrected `operation_realisation.csv`. The frozen P2 register/catalogue was not edited. |

Class tables, CRC, view selections and III 3.1/3.5 prose were reread/refreshed after the final diagram changes. Operation-derived view targets also cite their model-provided P4 inputs. All target markers remain controlled by the reviewed model; no signature match is treated as behavioral completion.

There are now **132 plates: 113 DCD plates and the unchanged 19 sequence parts covering 7 + 9 SSD occurrences**. The five additional readable relation plates are `dcd_uc01_domain_links_PartF`, `dcd_uc01_controller_links_PartA`, `dcd_uc01_all_links_PartN`, `dcd_uc01_final_links_PartN` and `dcd_uc05_controller_links_PartA`. Each has all five source/export companions. Current canonical lane file count is **669**, including this report. `generation_manifest.json` lists 668 generated paths; `integration_final_receipt.json` includes the report and current hashes.

### Archive, source freeze and checks

All 644 initial delivery files were copied byte-for-byte before repair to:

`D:/RAD/FINAL/Part2/notes/P3_trash/P3-A-integration-20261025T040358Z/`

`integration_archive.json` records their hashes; all 644 archived hashes were verified. Prior visual/receipt evidence is retained under that archive's `prior_qa/`. No superseded byte was deleted. The corrected model, annotations, AST inventory and realisation source hashes are recorded in `integration_sources.json` and remained unchanged throughout the repair. The corrected inventory still identifies C0 and `application_imported=false`.

`semantic_qa.json` and `integration_audit.json` report **zero document/model errors**: valid connected XML, exact 16-occurrence coverage, real receiver methods in final DCDs, genuine dataclass initialization, no property calls/DAO lifelines in III, no upward application dependency, exact member signatures/status refresh, no orphan owned stem, complete report headings/images, all final call/create navigation present, and preserved sequence frames/lifelines/message counts. These are document checks, not application tests or a global G3 verdict.

### Status refresh and reproduction

Every adjacent `.py` renderer now **refreshes its own JSON from the sole shared model before rendering**. It updates typed member signatures, explicit reviewed statuses/daggers, bound fingerprint arguments, message receiver signatures, relation statuses and P4 legends. Signature equality alone cannot clear a target. A reviewed explicit MATCH removes the corresponding member/message/relation dagger; other unresolved behavior targets remain marked. Unknown/disallowed relations or text that needs a new split fail visibly instead of being silently accepted or shrunk.

The standalone command was executed successfully against the actual UC-01 domain plate:

```powershell
& 'C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -I 'D:/RAD/FINAL/SaigonBite/models/UC-01/dcd_uc01_domain_PartA.py'
```

The same default command pattern applies to every owned plate. Refresh owned prose/tables/CRC after rerendering accepted model changes with:

```powershell
& 'C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -I 'D:/RAD/FINAL/Part2/notes/P3-A/refresh_repair_documents.py'
```

`integration_policy_probe.json` records a **synthetic document-policy probe** using only model copies in scratch: the unchanged target signature retained †; explicit copied MATCH removed its member/message dagger; other behavior targets remained †; conservative duplicate-relation precedence preserved the target marker; explicitly reviewed MATCH on every copied duplicate removed it. The actual shared model was not changed and no implementation/behavior review was simulated as a real result.

### Changed-export visual QA

Compared with the archived delivery hashes, **85 PNG plates changed, including the five new plates**. Every changed PNG and its independently rasterized SVG was opened in paired `integration_sheet_01.png` … `integration_sheet_22.png`, with lower-half/caption detail. The pure-domain member signature, checkout binding/self-call clearance and decline/full-C helper path were additionally reopened at full size in both forms. Exports show intact compartments/captions and matching geometry; minimum placement remains **9.78 pt at 230 mm landscape**. Fresh hidden Edge processes retain stdout/stderr, exit code and PID; unchanged exact SVG hashes reuse the previously verified independent raster. Updated per-plate hashes, raster paths and inspection dispositions are in `visual_qa.json` and the integration receipt.

**Native draw.io editing, native Excel and final DOCX/PDF placement remain UNTESTED.** No upload/staging/commit or application outcome is asserted. Root still owns global cross-check, assembly, frozen-boundary verification and commits.

### BLOCKED / ASSUMED and remaining root request

No blocking lane issue remains for R-A01–R-A05. One nonblocking source-maintenance request is recorded as **R-A06**: the shared dependency list contains both automatically derived MATCH and explicit P4-TARGET entries for Quote → PaymentMethod/OnlineOption. The projection deliberately keeps the stricter explicit F-07 target and its dagger, so no false MATCH is shown. Root should consolidate those duplicate keys/statuses in its model generator when convenient. The worker did not edit the frozen shared source; the default refresh continues to preserve the stricter target until all relevant records are explicitly reviewed as MATCH.


## Independent review repair R1–R4

Author: 722I0004 · AI-assisted (Codex)

26/10/2026, Asia/Bangkok. The independent review was read in full and its **NOT READY** verdict is preserved verbatim. This is the lane's bounded repair handoff, not a revised independent verdict or global G3 closure. The sole frozen design model remains `fe3e521d4eea7c66c2819a1acbb67101ecfd3fe49162650fb2dc273195079a6b`. Application C0, exact SSD parameters/pointers, selected DCD members, inferred-type distinctions and explicit P4 behavioral targets are retained. No application import/execution/test, database initialization, Git, shared-source change, configuration change, deletion, external action or child agent was used.

### Repair disposition and files

| Finding | Actual drawing change and evidence |
|---|---|
| R1 | Every one of the 27 owned sequence views now has actual guarded regions containing its governed message paths. Checkout A–E separates replay/denial, current quote/fingerprint **and T**, optional ONLINE authorization/decline, COD-or-approved creation, and exclusive commit success versus rollback. `seq_uc01_confirmCheckout_PartE` contains success only in `committed_operand`; `release(reference)` is enclosed by both `failed_operand` and nested `release_opt`, never the success region. COD skips authorization/release; declined ONLINE stops before creation. requestQuote A–C now encloses optional voucher validation and valid-only discount; Quote initialization precedes voucher subtotal access. acceptReplacement A–C separates stale refusal, invalid-target withdrawal-only commit/failure and valid-target replace_line/commit/failure. Existing real method names and genuine dataclass initialization are retained. |
| R2 | All 65 relationship plates across domain/controller/all/final families were regenerated. Each of the **93 association/composition projections** has **two separate adjacent multiplicity text cells** (186 labels total), with role in a distinct cell. Actual native endpoints touch their source/target class rectangles; native IDs, endpoint coordinates and label identities are recorded in `phase3.association_end_labels`. Repeated class representations and relation identities remain explicit. No cardinality is attached to inheritance or dependency. |
| R3 | cancelOrder, rejectOrder and declineReplacement now have Parts A/B. Part B contains respectively `cancelledOrderAndAmounts`, `rejectedOrder`, and `rejectedOrderAndAmounts` as explicit **dashed open replies**, inside the successful atomic-save/COMMIT region. Denial/stale and rollback outcomes remain separate. The continuation link prevents a premature success reply on Part A. |
| R4 | All **118 actual message edges** carry stable `native_edge_id`; solid synchronous calls, including boundary and constructor calls, use a closed filled head in native XML, SVG and Pillow output. Replies remain dashed/open. Native geometry contains explicit first/last points, intermediate self-loop points and port fractions on invisible anchors at the depicted lifeline positions. DCD navigation remains open. All **12 generalization projections** explicitly use native `endArrow=block;endFill=0` and a matching white-filled hollow triangle in SVG/Pillow. Composition retains its filled source diamond. |

The package now contains **140 figure sets: 113 DCD plates and 27 sequence parts for the unchanged 16 SSD occurrences** (UC-01: 62 DCD/14 sequence parts for seven occurrences; UC-05: 51 DCD/13 sequence parts for nine occurrences). Each has its adjacent `.py`, `.json`, `.drawio`, `.png`, `.svg`. There are **709 canonical lane files including this report**. Compared with the preserved pre-Wave4 state, 562 files excluding this report changed: 140 generators, 142 JSON files (140 plate specs and two view selections), 92 native files, 92 PNGs, 92 SVGs and four Markdown files. Eight new sequence parts account for 40 additional companion files; no old stem was deleted. `generation_manifest.json` and `wave4_receipt.json` list exact paths and hashes.

Both III reports were reread after changes and describe the actual branch/continuation semantics and named committed results; all figure links/includes and exact template headings resolve. The class tables and CRC were refreshed from the sole model; selected members/signatures did not change in this notation repair. Authorship remains on every figure and section. The footer, guard and message text retain **at least 24 px**, programmatically measured in the actual SVG/native text records: **9.78 pt at 230 mm landscape**. Split continuations identify previous/next parts in both directions.

### Native geometry, semantic and status checks

`wave4_audit.py` loaded root's `p3_notation_audit.py` read-only and called `audit` **only on the 140 owned JSON/diagram sets**. Together with lane checks it records **3,797 passing qualified document checks and zero unqualified artifact errors**, with the three per-part checker qualifications below reported explicitly. The checks resolve actual editable native edge/rectangle/text identities; validate explicit native waypoints and anchor ports; test **81 actual guarded regions**, including complete self-call vertical paths and parent/child containment; compare both end values with the canonical association; reject old combined labels; check source/target boundary attachment, distinct near-end labels, solid filled calls, dashed open replies, open navigation, hollow generalization and filled composition; verify status-refresh idempotence and all five companions; and verify all 669 preserved old-file hashes. R3 is additionally checked over each complete SSD occurrence, with exactly one named COMMIT-qualified success reply.

`qa_lane.py --render` reports zero semantic errors: exact 16-occurrence coverage, actual receiver methods present in the final DCD, no invented business constructor, no property-as-call, no DAO/SQL lifeline in III, allowed downward dependencies and valid connected XML. States metadata was recomputed from each actually rendered continuation's messages, guards and notes instead of inheriting invisible states from its earlier split. These are document/source checks, not application tests or proof of runtime atomicity.

Every adjacent generator continues to refresh signatures, explicit statuses, P4 labels and receiver bindings from the sole shared model before rendering. It does **not** clear a behavioral target merely because its signature matches. `integration_policy_probe.json` was rerun against model copies only: matching target signature retained †; explicit reviewed MATCH removed only the relevant member/message marker; unresolved behavior targets remained marked. The actual model was unchanged. The standalone `seq_uc01_confirmCheckout_PartE.py` was run and reproduced the inspected source/export hashes.

Reproduction commands (owned sources only):

```powershell
& 'C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -I 'D:/RAD/FINAL/SaigonBite/models/UC-01/seq_uc01_confirmCheckout_PartE.py'
& 'C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -I 'D:/RAD/FINAL/Part2/notes/P3-A/wave4_audit.py'
```

The same standalone pattern applies to any owned figure. `wave4_repair.py --resume` reconstructs the bounded branch repair from its preserved archive using the current owned renderer, without running the historical full lane builder. `wave4_finish_sources.py` refreshes the owned metadata and accompanying prose/CRC/tables after regeneration; these scratch commands never edit shared sources.

### Preservation and visual QA

Before repair, all **669 then-current canonical files** were copied byte-for-byte to `D:/RAD/FINAL/Part2/notes/P3_trash/P3-A-wave4-20261025T123315Z/`; `wave4_archive.json` records and verifies every hash. Root's `before_independent_review_repairs.zip` remains the separate whole-revision preservation supplied for this batch. Earlier integration/archive evidence remains history.

**All 92 changed PNGs and all 92 fresh independently rasterized final SVGs were opened**, paired in `wave4_sheet_01.png` … `wave4_sheet_23.png`, with complete figures and additional lower-half/footer detail. Checkout compensation, invalid/valid replacement, voucher method-result guards, decline success and hollow inheritance were additionally reopened at full size. The checked pairs show matching geometry, separate endpoint labels, filled calls versus open replies, intact guards/messages/compartments and uncut captions. `wave4_sheet_manifest.json` records the opened sheets and their hashes; `visual_qa.json` retains all 140 current source/export/raster hashes; `wave4_receipt.json` records fresh-this-repair Edge PID/exit/log hashes for every changed SVG. The second QA pass reused only exact previously rasterized SVG hashes; the final voucher-guard wording received a new independent raster. All helper processes used hidden creation with captured stdout/stderr and exit status. A4 230 mm proofs are retained for both forms.

Source/end-boundary hashes in `wave4_sources.json` remain unchanged, including the review file (`e738c01c10e34b5241aecfc62b4865dc005b678a085e6a622e41222cdb9ac891`). **Native draw.io editing, native Excel and final DOCX/PDF placement remain UNTESTED.** No global cross-check was run while the disjoint repair workers were unfinished. Root owns assembly, full cross-check, post-fix assessment, protected-byte checks and any Git work.

### BLOCKED / ASSUMED and Requests to root

No remaining lane artifact blocker was identified. Exact SSD operation identity spans explicitly linked continuation pages; it is not a separate request per plate. Inside an outcome `alt`, separately drawn `opt` regions carry mutually exclusive success/failure conditions and parent references, and geometrically contain the messages. This avoids claiming that a header note supplies control flow.

**R-A07 — checker continuation qualification (root-owned helper only):** the unmodified `p3_notation_audit.audit` success-result rule currently requires the final result on *each file* with OP-07/03/06. It therefore reports three `SSD_success_result` negatives on `seq_uc01_cancelOrder.json`, `seq_uc05_rejectOrder.json`, and `seq_uc05_declineReplacement.json`, which now explicitly continue to Part B. Their Part B files contain the exact committed success returns and pass that rule. The local audit records these three qualifications separately and independently proves one exact named success per whole occurrence; it does not change the helper or suppress an actual missing result. Please make the integrated rule aggregate explicitly linked parts by `(UC, op_id, ssd_occurrence)`, or apply its terminal-result obligation to the terminal continuation. Requiring the result prematurely on Part A would contradict the post-COMMIT qualification and the split-page legibility requirement. All other root-notation checks on this lane passed. No model or application request is added.
