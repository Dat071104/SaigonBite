# P3-B — UC-02 and UC-04 Design Packages

Author: 722I0004 · AI-assisted (Codex)  
Baseline: C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`  
Scope: P3-22–33; UC-02 and UC-04 only.

## Files written

For each diagram stem below, the lane produced `.py`, normalized `.json` (including `phase3` metadata), `.drawio`, `.png`, and `.svg` siblings.

- UC-02 DCDs: `dcd_uc02_all` and Parts A–J; `dcd_uc02_controller` and Parts A–B; `dcd_uc02_domain` and Parts A–B; `dcd_uc02_dao`; `dcd_uc02_view`; `dcd_uc02_final` and Parts A–J (30 stems).
- UC-02 SSD-derived design sequences (5): `seq_uc02_viewReadyDeliveries`, `seq_uc02_viewDelivery`, `seq_uc02_takeDelivery`, `seq_uc02_confirmDelivered`, `seq_uc02_reportFailure`.
- UC-04 DCDs: `dcd_uc04_all` and Parts A–I; `dcd_uc04_controller` and Parts A–F; `dcd_uc04_domain`; `dcd_uc04_dao`; `dcd_uc04_view`; `dcd_uc04_final` and Parts A–I (30 stems).
- UC-04 SSD-derived design sequences (3): `seq_uc04_salesReport`, `seq_uc04_workloadReport`, `seq_uc04_deliveryReport`.
- Class tables and CRCs: `docs/part2/UC-02/{design_classes.md,crc.md}` and `docs/part2/UC-04/{design_classes.md,crc.md}`.
- Filter views: `docs/part2/design/uc02_view.json` and `uc04_view.json`.
- Report sections: `docs/part2/report/III_3-2_UC-02.md` and `III_3-4_UC-04.md`.
- Visual receipts and scratch: `D:/RAD/FINAL/Part2/notes/P3-B/visual_qa.json`, `rasterize_and_audit.py`, logs, and independent Edge SVG raster images under `svg_review/`.

There are 68 diagram stems total (60 DCDs, 8 sequences; 340 required sibling files). A final receipt audit found all siblings present, no receipt hash mismatches, and no unresolved Draw.io edge endpoints.

## P3-22–33 evidence

| Checklist | Evidence |
|---|---|
| P3-22 | UC-02 design-class table covers the participating shared-model roles with visibility, full signatures, status and inferred markers. |
| P3-23 | UC-02 domain, controller, view, DAO, and all-layer filtered DCD sets are generated; machine-readable views and phase3 metadata are present. |
| P3-24 | UC-02 CRC cards document real participating collaborators and responsibilities. |
| P3-25 | Five operation occurrences retain the SSD operation, exact boundary parameter string, SSD occurrence pointer, guards and UC/PC/MG references. Static metadata validation passed; no DAO/SQL lifelines are drawn. |
| P3-26 | UC-02 final DCD set carries the reconciliation and changes note; received sequence messages are represented on final DCD views. |
| P3-27 | UC-02 report has the required 3.2.1–3.2.5 structure, includes, figure captions and source links. Readability and visual checks are recorded below. |
| P3-28 | UC-04 design-class tables include Period and report row/result value roles in the controller module and explicitly mark rows, filters, and returned reports non-persisted. No invented Report domain class is introduced. |
| P3-29 | UC-04 domain, controller, view, DAO, and all-layer filtered DCD sets are generated; machine-readable views and phase3 metadata are present. |
| P3-30 | UC-04 CRC cards document the participating collaborators and responsibilities. |
| P3-31 | Three report sequences preserve their SSD operation/parameter strings and pointers. Every report read follows UC04-MG01 authorization; only the manager-denial operand is UC04-MG02. No writes or DAO/SQL lifelines are drawn. Zero-denominator output is typed as a non-persisted value/display case. |
| P3-32 | UC-04 final DCD set and changes note reconcile displayed messages and mark P4 targets; no Report entity is modeled. |
| P3-33 | UC-04 report has the required 3.4.1–3.4.5 structure, includes, captions and source links. Visual checks and this lane report are recorded here. |

The lane’s final metadata check covered all 8 sequence JSON files: UC-02 has five occurrences and UC-04 has three; each first actor-to-view boundary matches the SSD operation and parameter string, every called receiver method is represented in the final DCD element union, and no sequence introduces DAO/SQL participants. UC-04 report reads are modeled read-only. Data-access and transactional behavior is noted for §4.3.2 as required by the design convention.

## BLOCKED / ASSUMED

No lane work item is blocked. The artifacts describe a static design correspondence at C0, not runtime behavior or P4 implementation. P4-TARGET/GAP marks remain targets. UC-04 `Period`, `SalesRow`, `WorkloadRow`, `DeliveryRow`, and report result roles are controller-module values, not persisted domain entities. Blueprint modules are represented as actual «view» roles; controllers/helpers are represented using their actual module/class roles. Dataclass construction and property reads are shown distinctly from business-method calls.

Filtered views and the supplied shared design model are treated as authoritative lane inputs. The suspicious shared-model edge and top-item identity annotation issue are escalated below; no shared model or target annotation was modified in this lane.

## Open items and limits

- Root integration should review the two shared-model requests below and regenerate/reconcile the shared model after the wave barrier.
- The normalized `phase3` records contain full displayed signatures. Some shared target parameter/return metadata was already identified for root-owned integration correction; this lane did not mutate shared model metadata.
- Draw.io native-app opening, Excel embedding, and final DOCX/PDF placement remain **UNTESTED**. No app, test suite, database initializer, or runtime was imported or executed.

## Sources used

- `docs/part2/_agent_reports/P3-brief.md` and `P3-root.md`; `Part2/notes/P3_primary_sources.json` fresh extracts (including the balanced-diagrams guidance).
- Locked `PLAN_SaigonBite_Part2_Final.md` sections 2–5, P3/P4, 7.3, and 10–12; `Part2/README.md`, `content/links.json`, and `Part2/codex/P3_CHECKLIST.md`.
- Frozen Part1_v2 and Part2 renderer/style patterns; P2 brief/root/review, UC-02 and UC-04 descriptions, SSD/domain/state sources, operation/anchor/flow registers, assembled II, and traceability.
- `docs/part2/design/code_inventory.json` AST inventory only, plus root-owned `design_model.json`, `design_annotations.json`, and `operation_realisation.csv` as read-only design inputs.

## Visual QA and integrity

`visual_qa.json` SHA-256: `50FF2402D292DCDC64DB7A3AE641B3137E7CA4833F933B4B92358B269E6E996C`. Its per-stem receipts contain PNG, SVG, Draw.io, normalized-JSON, and Edge-raster hashes. All 68 source PNGs and independently rasterized SVG PNGs were opened individually for visual inspection. The final independent audit confirmed 68/68 receipts, 340/340 sibling files, zero hash mismatches, zero XML/endpoint failures, and Edge exit code 0 for all SVG rasters.

All 60 DCD stems use portrait placement at 170 mm with minimum rendered text 9.27 pt; all 8 sequence stems use landscape placement at 230 mm with minimum 9.31 pt. Diagrams were split into readable continuations rather than reduced below the minimum size. Branch-condition labels meet a frame divider in a few sequence views but remain readable and do not obscure message text. This verifies generated exports and inspected rasters only; native Draw.io/Excel and final report rendering remain UNTESTED.

## Requests to root

1. Review/remap the shared-model dependency `DeliveryController → delivery`: the inventory AST `body_ast`/`calls` evidence for `delivery.move_to` identifies the receiver as a local `Delivery` entity/value, not the presentation blueprint module. Keep the view-to-controller dependency distinct.
2. F-09 top-item identity must retain `menu_item_id`. Current shared-model `ReportDAO.top_items` / `SalesReport.top_items` shapes omit that identity (`list[tuple[str, int, int]]`); annotate a minimal typed result shape that carries it through grouping and presentation. The UC-04 report marks this as a P4 target.
3. Reconcile root-owned target parameter/return metadata corrections during the shared-model integration and regenerate the shared model/views after the four-lane report barrier. This lane relied on full signature strings where prior target metadata was stale.

No application code, tests, database initializer, shared model, annotations, plan, workbook, config, or Git state was changed.
