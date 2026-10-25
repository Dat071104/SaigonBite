# P3-D — Architecture and Persistence Report

Author: 722I0004 · AI-assisted (Codex)

## Files written

- `models/shared/package_diagram.py`, `.json`, `.drawio`, `.png`, `.svg`
- `models/shared/erd_schema_v2.py` and the five re-runnable split generators `erd_schema_v2_PartA.py` through `erd_schema_v2_PartE.py`; each PartA–PartE stem has its own `.json`, `.drawio`, `.png`, and `.svg`
- `docs/part2/design/class_table_mapping.csv`
- `docs/part2/report/IV_4-2_package.md`
- `docs/part2/report/IV_4-3-1_mapping.md`
- This report
- Scratch only: `D:/RAD/FINAL/Part2/notes/P3-D/` (import audit helper, structural/visual QA helper, independent Edge raster images, renderer stdout/stderr logs, and SHA-256 evidence)

## Checklist evidence

| ID | Result and evidence |
|---|---|
| P3-46 | Complete. `models/shared/package_diagram.drawio`, `models/shared/package_diagram.json`, and `docs/part2/report/IV_4-2_package.md`. The four allowed package edges are drawn; all 392 resolved internal imports are classified in the JSON, with each strict violation listed in the report and a P4.9 request. |
| P3-47 | Complete. The five ERD figures in `models/shared/erd_schema_v2_PartA` through `PartE` cover all 13 inventory tables and all 18 foreign keys at `user_version = 2`; target differences carry † notes. Structural evidence: `Part2/notes/P3-D/visual_qa_20261025_r3.json`. |
| P3-48 | Complete. `docs/part2/design/class_table_mapping.csv` has one primary mapping row for every 110 C0 SQL columns, plus explicit rows for the missing `UserAccount.created_at`, the joined `MenuItem.brand_name` projection, both single-table Customer subtype discriminators, and computed `OrderLine.line_total`. |
| P3-49 | Complete as a Static comparison with root requests. `IV_4-3-1_mapping.md` and this report identify P2-S02, P2-S03, P2-S07, P2-S08, P2-S01 and the P2-S09 cross-row limits. S03/S07 are marked P4-TARGET†; P2-S08 is explicitly resolved by the DAO fallback and is not called a defect. |
| P3-50 | Complete. `docs/part2/report/IV_4-3-1_mapping.md` contains all five captioned views, the mapping link and scope limits. XML, endpoints, direct PNGs and independent SVG rasters are recorded in `Part2/notes/P3-D/visual_qa_20261025_r3.json`. |

## BLOCKED / ASSUMED

- No blocking condition stopped this lane. I applied the strict dependency graph specified in the P3 brief and the delegated instruction: presentation→controllers; controllers→domain/data_access; no outward domain dependency. Actual imports that depart from it remain explicit findings; I did not assume a DAO-to-domain mapping exemption.
- `Customer.nationality` and linked-account role `CUSTOMER` are presented as P4 targets because the C0 schema does not enforce the plan’s required checks. P4.7 is proposed for P2-S03/S07; root should confirm the subphase.
- `user_account.created_at` is a GAP at C0 and maps to P2-S02/P4.1. The target is shown as absent, never as a current schema column.
- `Payment.updated_at` is SQL `NOT NULL`; the inventory AST for `PaymentDAO.insert` supplies `payment.updated_at or payment.created_at`. P2-S08 is therefore not represented as a missing-value failure.
- All import and schema observations are Static at C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`. No application import, execution, app/schema test, Git command, checklist edit, or write outside this lane and its scratch folder was performed.

## Visual and structural QA

The package figure and five ERD pages are each 1800 × 1360 px. Their conservative minimum placed sizes at 230 × 170 mm are 9.42 pt for the package view and 9.21 pt for each ERD page. Each split figure names its related continuation pages.

The P2 renderer parsed every `.drawio` and `.svg` and checked that all edge endpoints exist. The independent QA pass re-parsed all six XML sources, matched all 18 diagram foreign keys against the inventory, checked all 13 tables and all 110 CSV column mappings, and recorded hashes for each `.py`, `.json`, `.drawio`, `.png`, and `.svg`. All six direct PNGs and all six independently rasterized SVGs were opened and visually inspected. The SVGs were rasterized by a hidden Microsoft Edge process with captured stdout/stderr under `Part2/notes/P3-D/svg_review_20261025_r3/`.

Native draw.io editing, Excel, and final DOCX/PDF placement remain UNTESTED. The report contains no SQL code excerpt and makes no application correctness claim.

## Sources used

- Full Phase 3 controlling prompt and shared `P3-brief.md` / `P3-root.md`; locked `PLAN_SaigonBite_Part2_Final.md` §§2–5, P3/P4, §7.3, §10 items 20–24, §§11–12; Part 2 README, links and P3 checklist.
- Fresh primary extracts in `Part2/notes/P3_primary_sources.json`: all eight Requirements PDF pages and both Case Study pages; template IV headings; marking Checklist and Rubric Guide; supplied balanced-diagrams skill text.
- Frozen `Part1_v2/content/content_master.md` and `Part1_v2/notes/diagram_changes.md` as read-only content/style references.
- `P2-brief.md`, `P2-root.md`, the relevant P2-review domain/CRUD findings, `P2-D.md`, and the domain-model renderer pattern in `models/shared/domain_model.py`.
- `models/shared/design_model.json`, `docs/part2/design/design_annotations.json`, and `docs/part2/design/code_inventory.json`. The code and schema facts used here were read only through the inventory’s resolved imports, `calls`/`body_ast`, and parsed `schema.tables`, `schema.indexes`, and `schema.user_version`.
- `models/shared/use_case_diagram.py` as the immutable Phase 2 rendering pattern. No web sources were needed.

## Requests to root

1. Proposed P4.9 input: disposition the strict package-boundary violations before the package graph is treated as satisfied. In particular, decide whether the 28 `data_access→business.domain` materialisation imports are an approved mapper exception or require relocation; address the 12 `presentation→business.domain` imports, 3 `presentation→data_access` imports and the `presentation.auth→saigonbite.NAV` root import. They are listed in 4.2 and `package_diagram.json`; no forbidden direction is drawn as allowed.
2. Confirm whether P2-S03 and P2-S07 should be assigned to P4.7 as proposed. P2-S02 remains P4.1 and P2-S08 requires no change.

The shared model, annotations, inventory, operation realisation, checklist and all Phase 1/2/application files remain untouched. No Git command was run.

## Root integration addendum

The original lane report above is retained. Its P3-46 sentence should read **three allowed arrows across four packages**; the figure and metadata contain three. Root accepted both requests: strict import findings are P3-S04/P4.9 (44 records including the NAV root import, 23 module pairs), with no implicit mapper exception; S03/S07 are P4.7, S02 remains P4.1, S08 is resolved without a change. Section 4.2 and the mapping source now state these dispositions.

Root clarified the package's data-access role as the actual `database (module)` and the 14 bootstrap imports including app.py. The updated PNG and an independent SVG raster were both opened and inspected. Fresh structural/mapping/schema receipts are in `Part2/notes/P3-root/package_integration_qa.json`; unchanged ERD images retain the original visual receipt. Native application and final document placement claims remain UNTESTED.

Root's later image review moved seven multiplicity labels into edge whitespace on ERD Parts B–E, preserving all cardinality values, tables, columns and relationships. Both current image forms of all four changed pages were opened and inspected; fresh hashes and schema/mapping validation are in `Part2/notes/P3-root/erd_label_qa.json`. A renderer launcher returned before its file appeared; the receipt requires a real fresh raster and exact dimensions, rather than trusting exit zero. The ERD coordinator now regenerates the accepted P4.7 assignments instead of restoring the old pending-disposition text. Section 4.3.1 prose was re-read and retains the same schema meaning and scope.
