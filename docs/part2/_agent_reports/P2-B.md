# P2-B — use case diagram and domain model

Author: 722I0004 · AI-assisted (Codex)
Date: 24/10/2026, Asia/Bangkok
Scope: Phase 2 Wave 1 B, P2-16–19. Starting revision supplied by root: `9404ec4`; no git commands executed.

## Files written

- `models/shared/use_case_diagram.{py,json,drawio,png,svg}` and `use_case_diagram_Part{A,B,C}.{py,json,drawio,png,svg}`.
- `models/shared/domain_model.{py,json,drawio,png,svg}` and `domain_model_Part{A,B,C}.{py,json,drawio,png,svg}`.
- `docs/part2/report/II_2-1-6_2-1-7_models.md`.
- This report, `docs/part2/_agent_reports/P2-B.md`.
- Scratch only in `D:/RAD/FINAL/Part2/notes/P2-B/`: verification script, primary source extracts/hashes, Static mapping, Edge render logs/raster reviews, A4 PDF proofs and export QA.

All source writes stayed in the assigned stems/report/scratch. No app/schema/contracts/P1/config/Section I changes, deletes, git, external contact or child agents. The main drawio files contain three editable pages each; the unsuffixed PNG/SVG are first-page aliases. The report embeds every split figure and does not treat an alias as the complete model.

## Checklist evidence

| ID | Status | Evidence |
|---|---|---|
| P2-16 | Done | Figure 2.1A–C, all six exact main goals and nine SUCs, all external actors, Customer generalisation, a–d group labels, boundary and L3 note. One real mandatory include and two conditional extends; directions, conditions and extension points documented in report 2.1.6. |
| P2-17 | Done | Figure 2.2A–C contains 13 persistent base classes + LocalCustomer/TouristCustomer. Typed attributes, both-end multiplicities, Customer generalisation, Order–OrderLine composition, HubMenuItem association-class tether, all required Order/payment/delivery/offer relations and offer→line. No methods/FKs/controllers/DAOs/Shipper class/persistent Quote/report/receipt. |
| P2-18 | Done (Static) | Report's 13-row all-attribute/schema map + P4 inputs; scratch `static_mapping.json` has SQL PRAGMA columns/FKs and Python AST field inventory. SQL inspected in memory only. No schema/code fixes or runtime claims. |
| P2-19 | Done after visual QA | 26-unit minimum text at 230 mm landscape = 10.59 pt (UC) / 9.42 pt (domain); XML/SVG parse, connected endpoints and ID/count checks; all 8 PNG exports and 8 SVG render reviews opened. `export_qa.json`, 8 Edge render logs, raster reviews and 8-page `A4_landscape_proofs.pdf` retained in scratch. Native draw.io GUI not opened. |

## Relation and modelling decisions

- Exactly 15 portfolio goals retain IDs: UC-01…06 + SUC-01…09. Two named, unnumbered UC-01 subgoals provide genuine include/extend semantics without inventing a new user goal or catalogue operation: mandatory accepted-checkout validation; conditional ONLINE simulator behaviour at `payment authorization`.
- SUC-04 extends SUC-03 at `order action selected`, guarded by customer cancellation request + PLACED/CONFIRMED. Tracking remains independently useful; cancel is optional. Other support links/sequence dependencies are not arbitrarily called includes.
- Customer's offer answer is through SUC-03; UC-05 Customer participation is secondary across sessions. No extra human SSD lifeline decision is imposed on Wave 2.
- Customer subtypes are complete/disjoint. Role-specific account links and offered-line same-order constraints are annotations; SQL does not enforce all of them.
- Reference boxes repeat existing class definitions. HubMenuItem is the association class of Hub–MenuItem, not a surrogate ordinary class with FK attributes. Internal `listing_link` is a tiny diagram anchor on that association, not a domain class.
- Shipper = UserAccount role SHIPPER. No one-active-delivery constraint. Archives on transactional children are inherited from parent Order visibility; receipts/report rows remain computed views.

## BLOCKED / ASSUMED

- No blocking uncertainty prevented delivery. No answer to L1/L2/L3/L6 is invented; the locked defaults govern.
- Three parts per figure are required to preserve readable full names/attributes. All six report images need **230 mm A4 landscape** placement. A 170 mm portrait placement would violate the 9 pt floor and requires further splitting rather than scaling down.
- `created_at` on UserAccount follows plan §5.3 despite its absence in draft SQL/dataclass. Optional `withdrawal_reason` is the conservative persisted fact for plan §3.3(5)'s invalid-target withdrawal with reason; final design mapping needs root disposition/P3–P4 follow-up.
- No native draw.io GUI, Excel GUI, application test run, measured UC correctness, deployment or grading result is claimed. Edge was used only as a hidden local SVG rasterizer, with stdout/stderr/exit retained. Pillow native PNG and browser-rendered SVG are separate export reviews.

## Requests to root

1. Accept/carry the P4 input list in report 2.1.7: UserAccount creation timestamp; Tourist nationality + CUSTOMER role linkage; withdrawal reason persistence; Payment timestamp optionality and scoped states; cross-row checkout/offer/shipper invariants; archive/snapshot mapping; known F-02/F-05/F-07. No shared contract edits requested during the wave.
2. In report assembly, place Figure 2.1A–C and Figure 2.2A–C on A4 landscape pages at 230 mm. Use split assets; unsuffixed images are first-page aliases. Mirror all owned sources/exports in root's staging manifest.
3. Record AI use in root's AI log: 24/10/2026, Codex; analysed locked requirements/contracts, generated UML sources/text, kept the split models and Static map, verified XML/counts/endpoints/font math + PNG/SVG visual QA. The supplied **balanced-diagrams** ZIP skill (`balanced-diagrams/SKILL.md`) was read and applied for bounded page ratio, split layout and export checks; reused immutable Phase 1 `stakeholder_chart.py` font/wrap/SVG/drawio text helpers by read-only import. No skill file was modified.

## Sources used

Authority order: locked `PLAN_SaigonBite_Part2_Final.md` §§1–5, P2, P3.1, §§7/10/11; direct `Lec_re/` case/requirements PDF texts, report-template headings and description table via python-docx, marking items 14–20 and rubric via openpyxl, team workbook Team & Use Cases / Events Table / CRUD Check headers. Also read `Part2/notes/P2_primary_sources.json` and source-evidence manifest as convenience, `Part2/README.md`, `content/links.json`, P2 checklist/prompt and supplied P2 brief.

Read-only contracts: `docs/part2/rules.md`, `decision_log.md`, `ssd_operations.csv`, `pc_mg_register.csv`. Frozen P1: `Part1_v2/content/content_master.md`, business-process model names, `build/proc_build.py`, `proc_geom.py`, `proc_views.py`, `notes/diagram_changes.md`. Reused Phase 1 shared renderer by import. Static draft comparison: `db/schema.sql`, `saigonbite/business/domain/models.py`. Direct-primary extracts and exact SHA-256 values are in scratch `source_audit.json`.

## Visual QA

Every output was reviewed after final generation: three UC parts, three domain parts and both first-page aliases in native PNG; every corresponding SVG opened through a local Edge raster review. Initial review found crowded ellipse text/actor labels, an actor-association gap, a boundary-title crossing and class-note/relationship overlaps; these were corrected in the generators and all exports regenerated. Final views retain clear class compartments, line endpoints, arrow directions, labels and captions. The local A4 landscape proof PDF fixes placement width at 230 mm and contains all eight PNG exports. All eight PDF pages were also rasterised with bundled Poppler at 90 dpi and opened; page bounds and placement were visually checked. The PDF skill was read for this proof verification. Programmatic checks and actual image review are separate evidence; none implies application behaviour.
