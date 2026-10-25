# P3-B-fix — UC-02 / UC-04 integration repair

Author: 722I0004 · AI-assisted (Codex)  
C0: `45ac76221b0a103174c7c01d17577e6e49cfd665`  
Date: 25 October 2026 (Asia/Bangkok)  
Scope: new bounded repair of P3-22–33 after completed Wave 1 P3-B.

## Result

All five assigned repair findings are addressed across the existing 68 figure stems (60 DCD, 8 design sequences). The original `P3-B.md` is preserved byte-for-byte against `P3_trash/wave1_preintegration.zip`; this separate report records the corrected evidence and does not relabel the original report.

1. Every native draw.io file now has one visible author mxCell and a native title cell. Native multiline values use actual line breaks. All native edge endpoints resolve.
2. Every SVG text element, including stereotypes, message labels, legends and footers, meets the 9 pt threshold at its declared placed width. DCD minimum is 9.2671 pt at 170 mm; sequence minimum is 9.3138 pt at 230 mm. Receipts use the actual minimum, not only the body font.
3. Exactly 46 forbidden upward DAO-to-domain arrows were removed from DCD exports and dependency metadata. Actual imports remain identified in CRC/prose as the static P4.9 architecture finding in section 4.2. They are not represented as permitted layered arrows.
4. Class members, types, complete signatures, parameter/return metadata and statuses were refreshed from the corrected shared model. DeliveryController → Delivery and → Payment dependencies are represented where their endpoints participate; the false DeliveryController → delivery blueprint dependency is absent. F-09/P4.8 retains menu_item_id in ReportDAO.top_items grouping, carries `list[tuple[int, str, int, int]]` in SalesReport.top_items (ID, snapshot name, quantity, revenue), and marks reports.sales presentation as a target.
5. Each plate generator now refreshes displayed class members and member daggers from the sole reviewed shared model when available, then saves the normalized adjacent JSON and exports. The adjacent static JSON remains sufficient for standalone reproduction when the shared model is unavailable. A signature match alone never clears a behavioral target. An isolated scratch probe changed reviewed member statuses to MATCH and verified the displayed member daggers disappear, without editing the authoritative model.

## Files written

The exact 348 repaired artifact paths and final SHA-256 values are in `Part2/notes/P3-B-fix/files_written.json` (plus this new report).

For every stem below, `.py`, `.json`, `.drawio`, `.png` and `.svg` were refreshed:

- UC-02 DCD: `dcd_uc02_all` and `_PartA`–`_PartJ`; `dcd_uc02_final` and `_PartA`–`_PartJ`; `dcd_uc02_controller` and `_PartA`–`_PartB`; `dcd_uc02_domain` and `_PartA`–`_PartB`; `dcd_uc02_dao`; `dcd_uc02_view` (30 stems).
- UC-02 sequence: `seq_uc02_viewReadyDeliveries`, `seq_uc02_viewDelivery`, `seq_uc02_takeDelivery`, `seq_uc02_confirmDelivered`, `seq_uc02_reportFailure` (5 stems).
- UC-04 DCD: `dcd_uc04_all` and `_PartA`–`_PartI`; `dcd_uc04_final` and `_PartA`–`_PartI`; `dcd_uc04_controller` and `_PartA`–`_PartF`; `dcd_uc04_domain`; `dcd_uc04_dao`; `dcd_uc04_view` (30 stems).
- UC-04 sequence: `seq_uc04_salesReport`, `seq_uc04_workloadReport`, `seq_uc04_deliveryReport` (3 stems).
- `docs/part2/UC-02/design_classes.md`, `docs/part2/UC-02/crc.md`.
- `docs/part2/UC-04/design_classes.md`, `docs/part2/UC-04/crc.md`.
- `docs/part2/design/uc02_view.json`, `docs/part2/design/uc04_view.json`.
- `docs/part2/report/III_3-2_UC-02.md`, `docs/part2/report/III_3-4_UC-04.md`.

Scratch, scripts, logs, native-scale detail crops and receipts are exclusively under `D:/RAD/FINAL/Part2/notes/P3-B-fix/`. Superseded pre-repair bytes are preserved in `D:/RAD/FINAL/Part2/notes/P3_trash/P3-B-fix_pre_repair.zip`. No shared artifact was written.

## P3-22–33 evidence

| Checklist | Repair evidence |
|---|---|
| P3-22 | UC-02 typed tables refreshed from shared model; full signatures and targets retained. |
| P3-23 | UC-02 five filtered DCD views refreshed; native author, font floor, allowed dependencies and exact member metadata checked. |
| P3-24 | UC-02 CRC refreshed; real Delivery/Payment collaborators retained and false blueprint collaborator removed. Actual DAO imports are labeled architecture findings. |
| P3-25 | Five SSD occurrences preserved with exact boundary names/parameters and pointers; receiver methods remain in final DCD union; no DAO/Database lifeline introduced. |
| P3-26 | UC-02 final DCDs contain the corrected dependencies/statuses and all receiver methods after sequence reconciliation. |
| P3-27 | Report 3.2 prose and repair evidence correspond to the corrected exports; all 35 UC-02 figure pairs and footers opened. |
| P3-28 | UC-04 typed tables carry the ID-preserving SalesReport.top_items type, DAO target grouping and reports.sales target. |
| P3-29 | UC-04 five filtered DCD views refreshed from shared model; author, 9 pt floor and layered dependencies checked. |
| P3-30 | UC-04 CRC refreshed; report filters/rows/results remain non-persisted controller values. |
| P3-31 | Three SSD-derived report sequences retain exact boundaries and PC/MG references; sales view dagger refreshed; report requests remain read-only. |
| P3-32 | UC-04 final DCDs retain the F-03/F-09/P2-S18 targets and contain all sequence receiver methods. |
| P3-33 | Report 3.4 now states the accepted F-09 identity annotation instead of an unresolved annotation request; all 33 UC-04 figure pairs and footers opened. |

Root retains responsibility for ticking the shared checklist and running the full cross-check after all repair lanes finish.

## Checks and visual QA

- `final_static_check.json`: 68 stems / 340 sibling files; exact shared-model member types, full signatures, parameter lists, returns and statuses; 8 preserved SSD boundaries; all call receivers present in final DCD union; no upward DAO DCD dependency or false DeliveryController → delivery dependency; connected native XML edges; one native author cell per plate.
- `removed_edges.json`: exact ledger of the 46 removed upward arrows.
- `visual_qa.json`: final per-plate source, JSON, draw.io, PNG, SVG and independent Edge-raster SHA-256 values; every SVG text element meets the declared 9 pt floor; every SVG text extent is within the canvas.
- Every changed PNG and independently rasterized SVG was opened through `pairs_01.png`–`pairs_17.png`; all author/footer details were opened through `footers_01.png`–`footers_09.png`. The six changed exports from the final identifier-wrap polish were re-opened on their updated sheets. Dense DAO/member cards were additionally opened at original pixel resolution in twelve PNG/SVG native-scale crops under `dense_crops/`.
- Visual review found and fixed long method identifiers crossing a class compartment, overlapping endpoint lifeline headers, and the alternate-operand label touching its divider. Identifier wrapping preserves the full name in typed metadata. The two sparse view-only plates were padded to 2:1, so all 68 canvases satisfy the balanced-diagrams 1:2–2:1 bounds without reducing fonts.
- `forward_refresh_probe.json`: isolated MATCH-status probe confirms displayed class-member daggers clear under reviewed model status. `native_text_export_identity.json`: the native multiline correction left all 68 PNG/SVG visible exports byte-identical before the separate two-plate aspect padding.
- `preservation_check.json`: locked-plan SHA-256 remains the read-start value; original P3-B report matches the preintegration archive.

Visual QA SHA-256: `18f8b5ea20d4b4b96f93f1150752d52bdf755f365887dc84296987ba36274715`  
Shared-model SHA-256: `bd415d6b5874d373cd5eb928dc9b218d27d499e36052589304912a2c33cdd437`

No application module was imported or executed. No application tests or database initializers ran. Checks executed only owned renderers, scratch audit/probe scripts and static metadata/XML/AST checks. No Git command, subagent, Phase 2 modification, plan write, shared-model write, workbook change, configuration change or external action occurred.

## Reproduction

Run any plate with the bundled interpreter, for example:

```powershell
& 'C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -I 'D:/RAD/FINAL/SaigonBite/models/UC-04/dcd_uc04_controller_PartB.py'
```

The generator uses adjacent JSON, refreshes reviewed members/statuses from `models/shared/design_model.json` when present, then regenerates its siblings. A new signature that no longer fits the current class compartment raises a layout-continuation error rather than silently shrinking text. The one-time scratch repair scripts are migration records; use the per-plate `.py` files for future reproduction.

## BLOCKED / ASSUMED

No assigned repair is blocked. The corrected root-owned model/inventory/annotations/realisation are authoritative read-only inputs. P4-TARGET/GAP remain design targets, including behavioral changes whose signatures already match C0. Upward DAO imports are a static P4.9 finding; omitting those arrows from the allowed design does not claim the code coupling is fixed. This lane covers the five UC-02 and three UC-04 occurrences only; the shared total remains 41 occurrences, including 12 in UC-06.

Native draw.io application opening/editing, native Excel, final DOCX/PDF embedding and runtime behavior remain **UNTESTED**. XML structure and exported/rasterized visuals do not establish native application compatibility or final document placement.

## Requests to root / open items

No further shared-model correction is requested by this lane. After the barrier, rerun the root-owned full design cross-check against C0 and review the assembled report. Carry actual upward DAO imports into the package audit/P4.9 work; retain F-09 identity/presentation and P2-S13/P3-S03 shared transaction targets until reviewed code evidence resolves them. Native application and final document-placement checks remain later-phase work.

## Sources used

- Authoritative controlling prompt in `Part2/notes/P3-root/controlling_prompt.txt`; locked plan §§2–5, P3/P4, 7.3 and 10–12; Part2 README, links and P3 checklist.
- `P3-brief.md`, original `P3-B.md`, corrected shared `design_model.json`, `code_inventory.json`, `design_annotations.json`, `operation_realisation.csv`, and the root cross-check diagnostic.
- Frozen UC-02/04 descriptions, SSD source/parameters/occurrence ledger and PC/MG register. Phase 2 artifacts were read only.
- `Part2/notes/P3_primary_sources.json`, including the balanced-diagrams skill extract and template/rubric source extracts; original Phase 2/Phase 3 renderer pattern. Existing continuation geometry and report polish were preserved except for the bounded readability/layout repairs stated above.


## Independent Wave 4 review repair — 26 October 2026

Author: 722I0004 · AI-assisted (Codex)

This is a separate post-review repair record. The sole review in `P3-review.md`, including its **NOT READY** verdict, is preserved as written. It was read fully. This section records only the UC-02/UC-04 lane; it does not replace root's phase-level disposition or G3 assessment. The frozen sole-model SHA-256 is `fe3e521d4eea7c66c2819a1acbb67101ecfd3fe49162650fb2dc273195079a6b`.

### Findings and changes

| Review finding | Own-family audit and bounded repair |
|---|---|
| R1 guarded interaction regions | All eight III sequences had accepted messages inside the main region but only a note in the alternate region. The SSD request is now outside the combined interaction. Two actual guarded operands contain accepted and refusal response arrows; a nested `opt [request reaches controller]` contains both the conditional controller invocation and its failure reply, so direct view denial does not imply a controller call. There are 24 operand/opt proof records, each tied to actual native bounds and its actual message indices. Notes are identified as notes rather than falsely assigned an arrow. Command save/commit qualification is kept on success, and rollback/refusal conditions remain on the alternate path. Read-only board/detail/workload guards have no invented write or date-filter condition. |
| R2 association ends | Twenty-one UC-02 DCD stems contained 41 association occurrences whose multiplicities were only summarized in prose or absent at the actual ends. Each now has two distinct native text cells at attached class-border ports and a separate role text cell: 82 end labels total. `phase3.association_end_labels` carries the actual native edge/text IDs and endpoints. Native exit/entry coordinates and explicit native source/target points agree with those endpoints. The exact canonical values, role and navigation are preserved. Other owned DCDs contain no qualifying association and were audited without visual changes. No owned composition/generalization needed alteration. |
| R3 successful responses | All eight owned operations already had controller-to-view and view-to-actor successful response messages. Their eight named SSD success results are retained, and the accepted actor reply now contains the success result alone. Sixteen explicit alternate response arrows and eight conditional invocations of existing controller methods were added for R1; they do not replace a success reply or invent a business method. |
| R4 message heads | Solid closed call heads were already selected in this family, but replies were also filled. All 32 current replies are now dashed/open. The renderer distinguishes genuinely open V heads from filled triangles in SVG and PNG, and native `endFill` agrees. Message endpoints attach at visible activation faces when active, and label backings no longer cover self-call head interiors. The final audit verifies 127 actual heads: 95 filled request/call/create heads and 32 open replies; the filled-head centroid is visible in the generated PNG for every filled head. The breakdown is {'ssd': 8, 'call': 72, 'create': 15, 'return': 32}. |

No class, business method, target signature, persisted state or responsibility status was added or promoted to MATCH. Sole-model dynamic member/dagger refresh remains in each changed standalone renderer. The root's corrected UC-04 `dcd_uc04_domain` source/image links were retained. Class tables, CRC and per-UC view manifests needed no semantic change for these notation repairs.

### Files, preservation and checks

- Changed: 29 existing stems (21 DCD + 8 sequence), all five siblings each; the two own III report sources received correspondence prose; this report received only this appended review-repair section. Exact paths and hashes are in `Part2/notes/P3-B-fix/review_repair/files_written.json`.
- Preserved: `P3_trash/P3-B_W4_pre_repair.zip` contains all original owned diagram bytes at this repair's entry. The prior repair report is separately preserved as `P3_trash/P3-B-fix_before_W4_report.md`; original `P3-B.md` remains untouched. Root also preserved the integrated originals in `before_independent_review_repairs.zip`.
- Local semantic/geometry evidence: `semantic_geometry_receipt.json` audits all 68 owned figures, 41 canonical association records, native text/port/end attachment, 82 separate end labels, three guarded operand/opt bounds per sequence, exact SSD boundaries, separate success results and all actual message head styles. Zero issues.
- Root's strengthened helper was loaded read-only and invoked only on this lane's 68 JSON/native pairs. `root_notation_local.json`: **872 checks, 0 failures**. The earlier local probe is preserved as `root_notation_before_native_endpoint_proof.json`; its failures exposed missing explicit straight-edge native endpoint evidence, note indices mistakenly treated as arrows, and an unexpressed operand operator. These were repaired in the actual native/source/metadata representations; no checker was edited or waived.
- `arrowhead_receipt.json`: native/XML role styles agree with actual SVG polygon/polyline heads; all 95 filled PNG head-centroid checks pass. `visual_qa.json` records final source/JSON/draw.io/PNG/SVG/fresh independent Edge raster hashes, actual SVG text bounds and native author presence. Font floors remain 9.2671 pt for DCDs at 170 mm and 9.3138 pt for sequences at 230 mm, including footers and end labels.
- Every changed PNG and fresh independently rasterized SVG was opened through all eight pair sheets; all four footer-detail sheets were opened. The final eight sequence revisions were reopened on sheets 06–08. Guard labels were checked after ensuring activation bars cannot obscure them. All changed canvases stay within the balanced-diagrams 1:2–2:1 bounds without shrinking text. The eight sequence canvases are 4200 × 3100 px: at the declared 230 mm width they occupy 169.76 mm vertically and retain 9.3138 pt text; the actual final document placement remains untested.

Final visual receipt SHA-256: `832ed5ac92fd4feaf963b431cc88d0df6c81bcf28f88ac80859bfab7e2da9f08`.  
Final local notation receipt SHA-256: `84b51c181bba44bb63835ad19288ad44b7ee871f7b2f8068ddb433c6e24f0135`.  
Final semantic/geometry receipt SHA-256: `a065b0da3e1ac30689b2f3d3834f762f6bf5fc26d4bcd0383e0c3260bdceecf0`.

**BLOCKED / ASSUMED:** no assigned lane item remains blocked. Technical report-read failure returns no fabricated figures and writes nothing; the notes distinguish this from denied/invalidFilter. P4 targets remain targets. Native draw.io application editing, final DOCX/PDF placement and runtime behavior remain **UNTESTED**.

No application import/execution/test, database initializer, Git command, global cross-check, shared-model/configuration/Phase 2 write, other-lane edit or subagent occurred. Root should run the full cross-check only after the four-worker barrier. Sources for this repair: full independent review, frozen shared model, existing owned source/JSON/native/export forms, frozen UC-02/04 descriptions and operation catalogue, balanced-diagrams guidance already read, and the root-provided read-only notation helper.
