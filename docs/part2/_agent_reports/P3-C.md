# Phase 3 — Lane C: UC-03 and UC-06 design packages

Author: 722I0004 · AI-assisted (Codex)

**Lane deliverables complete for root integration.** This is Static / target-design evidence at C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`, not G3 closure or application qualification. Root must resolve the shared-model requests below and run the integrated cross-check. No application import, execution, test, Git operation, further delegation, external action, deletion or shared-model write was performed by this lane.

## Files written

- `docs/part2/UC-03/design_classes.md`, `crc.md`; `docs/part2/UC-06/design_classes.md`, `crc.md`.
- `docs/part2/design/uc03_view.json`, `uc06_view.json`.
- `docs/part2/report/III_3-3_UC-03.md`, `III_3-6_UC-06.md`.
- 72 complete diagram source/export sets in the owned `models/UC-03/dcd_uc03_*`, `seq_uc03_*`, `models/UC-06/dcd_uc06_*`, `seq_uc06_*` stems. Every set has `.py`, `.json`, `.drawio`, `.png`, `.svg`: 360 diagram files. 55 are DCD projections and 17 are design sequences. There is no misleading unsuffixed first-page alias.
- This report, `docs/part2/_agent_reports/P3-C.md`.

The 368 pre-report files are listed exactly in `D:/RAD/FINAL/Part2/notes/P3-C/manifest.json` and hashed in `final_file_hashes.json`. This report makes 369 repo files in the lane bundle. Scratch, hidden Edge profiles/logs, proofs and audit helpers are exclusively under `Part2/notes/P3-C/`. No files outside the authorized write set were written.

## Checklist disposition and evidence

| ID | Disposition / evidence |
|---|---|
| P3-34 | Complete: `UC-03/design_classes.md`; typed declarations from the shared model, visibility, responsibilities, per-member status, inferred `Any`/annotations, actual templates and boundary adapters. |
| P3-35 | Complete projections: `uc03_view.json`; domain A–B, controller A–C, view A, DAO A–B, all A–E. Domain FK backing IDs are absent from domain figures. |
| P3-36 | Complete: `UC-03/crc.md`; collaborating classes, real AST call/typed-field targets and callers, inherited authorization through BaseController. |
| P3-37 | Complete: 5 exact SSD occurrences: listHubs, getHub, createHub, updateHub, archiveHub. `seq_uc03_*` preserves each parameter string and native SSD pointer. |
| P3-38 | Complete: `dcd_uc03_final_PartA`–`PartE`; union contains every callable receiver method used in the UC-03 sequences. Changes note explains the reconciled unchanged signatures and partial projections. |
| P3-39 | Complete: `III_3-3_UC-03.md`, exact .1–.5 headings, i–v subparts, includes, authors/captions and explicit placement sizes. All exports visually inspected. |
| P3-40 | Complete: `UC-06/design_classes.md`; types/status/inference, templates, transient DTOs, initial-availability target, current-parent context, snapshot and guarantee responsibility matrix. |
| P3-41 | Complete filtered projections: `uc06_view.json`; domain A–C, controller A–F, view A–C, DAO A–E, all A–J. Shared-model clarification C-R1 below remains for integration. |
| P3-42 | Complete: `UC-06/crc.md`; no invented public domain behavior or fictional view class. Marked OP-25/OP-43 targets are disclosed. |
| P3-43 | Complete: **12 occurrence sequences for 10 distinct operation names**, preserving frozen P2. OP-25 has `seq_uc06_listCatalogue_PartA`, `PartB`, `PartC`; the other nine names each have a separate `seq_uc06_*`. |
| P3-44 | Complete: `dcd_uc06_final_PartA`–`PartJ`; callable view/controller receiver methods reconcile; actual domain construction and field notes are explicitly distinguished from methods. Root must settle C-R1. |
| P3-45 | Complete: `III_3-6_UC-06.md`, exact template headings/includes/captions, all figures and this report; visual and structural evidence below. |

Root owns ticking the external checklist and integration commits; this lane did not edit either.

## Semantic decisions retained

- OP-23 keeps the explicit target `HubController.list_hubs(self, user_id: int, include_archived: bool = True) -> list[HubAdminView]` (P3-S02). Omitted includeArchived maps to True; retained archived inspection remains allowed.
- OP-25 remains the GAP `MenuController.list_catalogue(self, user_id: int, hub_id: Optional[int] = None) -> dict[str, object]` (P2-S14). It composes catalogue/retained-hub/optional hub-menu reads; route adapters are the real `admin.catalogue` and `admin.hub_menu` functions. The three SSD occurrences are not collapsed.
- OP-43 passes `available` into the proposed extended controller and DAO signatures. The initial flag is written in the same insert, not via a second availability update (P2-S15).
- OP-41 brandId is the **current parent** form context. `update_item` pins `current.brand_id`; no reparent/restore operation is proposed. Existing OrderLine snapshot names/prices are outside these writes.
- `_require_admin` delegates to active-user/role checks in BaseController. uid() is a session-derived alias; posted actor identity is not trusted. CamelCase-to-form/Python aliases are declared in .1.
- Domain classes are real dataclasses. Creation is an implicit dataclass create message, and state inspection is a `note`; no `Hub.update`, `MenuItem.archive`, listing setter or other nonexistent domain method was invented. Return labels are outcomes, not callable receiver operations.
- HubStatus, HubAdminView, Catalogue and HubMenu are transient projections. HubMenuItem is the association class represented by the canonical Hub–HubMenuItem–MenuItem relationships; scalar backing FKs stay in the typed table and are suppressed on domain DCDs. Role has its real enum dependency; BUSY/QUIET remain derived properties, and no artificial lifecycle enum was introduced.
- Mutation diagrams disclose P2-S13/P3-S03: success after commit, guard/rowcount failure, controlled busy/commit failure and rollback are design obligations. Section III has no DAO/SQL lifeline; every sequence has the required persistence note referring to 4.3.2. The design does not assert that those targets execute successfully at C0.
- Every PC/MG is mapped to named controller/DAO responsibilities plus read or BEGIN IMMEDIATE boundary in the .1 guarantee tables. UC06-PC03 also depends on the order consumer rechecking `HubDAO.get_available_item`, not merely an old catalogue page. Its `_ORDERABLE` AST literal is `m.archived_at IS NULL AND b.archived_at IS NULL`; the file hash was checked against the C0 AST inventory before that one targeted AST read.

## Visual QA and reproducibility

- Geometry: DCDs are 1200 × 850 at **230 mm landscape width**, minimum 18 px = **9.7795 pt**. Sequences are 1200 × 1250 at **170 mm portrait width**, minimum 23 px = **9.2362 pt**. Both fit their stated A4 content orientation without shrinking the text. Long surfaces split into explicit mutually referenced parts.
- All **72 draw.io files parse**, all **272 message/dependency edge endpoints resolve**. Every SVG parses; class/member selections resolve to the shared model. Both reports have ordered .1–.5 headings and local image/include paths. Lane audit: `Part2/notes/P3-C/semantic_audit.json` (`pass=true`).
- All **72 PNG exports and 72 independently headless-Edge-rasterized SVG exports were opened and visually inspected**, via the 18 `review_pairs_01.png`–`review_pairs_18.png` sheets and selected full-size views. Revised sequence labels, continuation text, listing dependency routing and enum links were reopened after correction. No remaining text clipping/overlap was observed in the final inspected forms.
- `visual_receipts.json` contains current PNG/SVG/draw.io/proof SHA-256 values and successful Edge exits for all 72 sets. Per-stem `*_edge.log`, `*_svg.png` and isolated hidden browser profiles retain renderer evidence. The SVG rendering path is independent of the Pillow PNG drawing path.
- All 72 generator ASTs parse. Two **standalone** owned generators (`seq_uc03_getHub.py`, `dcd_uc06_final_PartH.py`) rebuilt PNG/SVG/draw.io/JSON byte-identically; see `reproducibility.json`. These were artifact-generator checks, not application tests. Every diagram's `.py` and `.json` live together and require no application import.
- DCD member labels read the sole shared model at render time. JSON stores explicit projection selections and normalized `phase3` elements/dependencies. Sequences carry exact UC/op/parameters/native occurrence, lifelines, messages/kinds/guards/PC_MG and displayed concrete flag metadata. Sequence status is refreshed from the shared controller method on rerender, so a later model MATCH removes the message dagger.
- Matching prose was re-read after the diagram revisions. Final checksum evidence is `final_file_hashes.json`; current visual receipt hashes were rechecked after standalone rebuilds.

**Limits:** Native draw.io editing, native Excel and final DOCX/PDF placement remain UNTESTED. Actual application behavior, concurrency, rollback and target implementation were not run. Integrated root cross-check/review and the whole-workspace protected hash check are still root-owned gates; this lane audit does not replace them.

## Requests to root

| Request | Evidence / proposed conservative handling |
|---|---|
| **C-R1 — required shared-model disposition for MenuController → HubMenuItem note dependency** | The UC-06 listing sequences use the allowed conceptual attribute note on HubMenuItem (`item`, `is_available`), and their normalized metadata records MenuController → HubMenuItem. The canonical model's direct AST dependency builder does not expose that mediated relationship because the controller sends identifiers/flags to MenuDAO, which constructs/updates the association. Please record an explicit logical design dependency supported by the existing MenuDAO calls (clearly distinguish it from a direct Python method call), or document that note-only persistence projections are exempt from direct-call navigation checks. **Do not invent a HubMenuItem method.** If a dependency is added, refresh the all/final listing JSON dependency selections and regenerate those six projections. |
| **C-R2 — association-class annotation clarity** | Shared HubMenuItem currently has generic `entity` stereotype, while the locked design requires an association class. .1 explicitly explains it and domain Part A draws all three canonical relationships with multiplicities/navigation. Recommend an explicit shared-model association-class classification/note so every lane renders that meaning consistently; avoid a worker-only competing model. No new entity/relation is requested. |
| **C-R3 — known root metadata repair** | OP-35 currently contains spurious `an:W` from the HubDAO.update docstring, not a real SQL table. Root's continuation already identifies its prepared SQL-docstring filter and signature parameter/return synchronization. Apply those after the barrier. This is an inventory/ledger parsing issue, not an application defect, and this lane did not alter shared files. |
| **Cross-check interpretation** | Resolve only `call` messages as receiver methods. `ssd` is the exact external boundary alias, `create` is implicit dataclass construction, `note` is attribute/persistence inspection and `return` is an outcome. This follows the shared brief; treating those four kinds as invented methods would misclassify the legal notation. The lane audit checks the final DCD method union accordingly. |

No new operation, controller signature or business rule is requested. Existing root targets OP-23/25/43/41 were adopted as supplied. After root changes shared model/dependency selections, rerun affected owned `.py` generators with bundled Python `-X utf8 -I`, refresh affected SVG proofs/hashes and re-read corresponding prose.

## BLOCKED / ASSUMED

No access blocker remains. The initial turn was resumed by the same lane identity after the owner's continuation; existing drafts/proofs were reused. No replacement worker, restart, model/config change or extra delegate was introduced.

C0 and locked P2 semantics supplied by root remain authoritative; newer/uncommitted app content is not a design source. The shared model stayed root-owned and unchanged by this lane. P4 target behavior is disclosed rather than relabeled implemented. Unannotated types use visibly inferred Any or the root inventory's inferred type. Full class members remain in .1 and layer sheets; all/final sheets are explicitly declared operation projections whose union is checked for received callable methods. Root's integrated review must retain this projection qualification.

The P3-43 checklist wording says ten operations, whereas frozen SSD Parts A/B/C have twelve occurrences; the conservative resolution is twelve files/occurrences for ten names. No frozen Phase 2 ledger/model was edited.

## Sources used

First reads: `P3-brief.md` and `P3-root.md`; full controlling attachment `C:/Users/ADMIN/.codex/attachments/9c9f5083-d06d-4284-98a7-5f3e3677b4a7/Pasted text.txt`.

Locked plan §§2–5, P3/P4, §7.3 and §§10–12; `Part2/README.md`, `content/links.json`, `codex/P3_CHECKLIST.md`; fresh primary extracts in `Part2/notes/P3_primary_sources.json` (requirements, both case pages, template III/IV headings, marking/checklist/rubric cells and supplied balanced-diagrams ZIP skill text). The balanced-diagrams geometry principle and immutable P2 XML/SVG/Pillow + hidden Edge renderer conventions were applied.

`P2-brief.md`, `P2-root.md`, `P2-review.md`; six UC descriptions (UC-03/06 read in detail), `ssd_operations.csv`, `ssd_flow_membership.csv`, `pc_mg_register.csv`, P2 model JSON/generator sources, particularly UC-03/06 SSD/activity/state/domain relationships; frozen Part1_v2 `content/content_master.md`, `notes/diagram_changes.md`, `build/proc_build.py` for vocabulary/history/style, read-only. Locked Part 2 terms supersede historical Part 1 wording/placeholder ownership.

Static implementation inputs: `code_inventory.json` full class signatures, method body AST/calls, routes, SQL facts; `design_annotations.json`, `operation_realisation.csv`, `models/shared/design_model.json`. One additional hash-verified AST extraction of `_ORDERABLE` was read without importing/running the app. No web source or newer-library assumption was needed.

## Marking evidence pointers within this lane

| Primary item / physical row | Evidence / scope limit |
|---|---|
| 20 / Checklist 33 — author | Both UC section titles, class/CRC sources, all 72 figure captions and exported author footers identify 722I0004 plus AI-assisted (Codex). |
| 21 / Checklist 34 — layered DCD per UC | Both .1 tables, .2 i–v projections and `uc03_view.json` / `uc06_view.json`; C-R1 is disclosed for root integration. |
| 22 / Checklist 35 — CRC + sequences | Both CRC files and all 17 exact occurrence sequences; frozen parameters and native pointers independently checked by lane audit. |
| 23 / Checklist 36 — final DCD | .5 projections and callable receiver-method union checks; full table/layer-member qualification stated, shared-model requests pending root. |
| 24 / Checklist 37 — package, mapping and SQL | Outside lane C: lanes D/F and root own package/mapping/DAO work. Full SQL/implementation item remains P7/P4 scope; no claim from these Section III packages. |
| Part 3 item 33 / Checklist 47 | Both UC design packages provide design-model inputs; no presentation/video completion is claimed. |
| P2-III Excellent / Rubric Guide 9 | Explicit layers, single-source selections, CRC, parameter-exact SSD realization, final method reconciliation and named analysis guarantees. Root cross-check and C-R1/C-R2 dispositions are still required before any G3 claim. |
| P2-IV Excellent / Rubric Guide 10 | DAO responsibilities are referenced, but running code, UI, SQL completeness and integration are outside this lane's evidence. |

## AI-log handoff

Root should log Codex lane C for both class/CRC/report packages, generator/metadata authoring and artifact QA; retained work was checked against frozen SSD/PC/MG inputs, the sole shared model, 72 XML/source/export sets, independent SVG proofs and two deterministic standalone rebuilds. No work is attributed to another proposal owner.


## Integration repair — native text and adopted shared-model dispositions

Author: 722I0004 · AI-assisted (Codex)

**Repair complete in the same lane and identity.** This section supersedes the earlier pending C-R1–C-R3 dispositions and the incomplete native-font assessment. The original Wave 1 record above is retained as history. The previous checks measured SVG/Pillow text but missed the native draw.io text-cell fallback: all 17 sequence XML files carried 18 px native text (7.2283 pt at 170 mm), despite their 23 px SVG/PNG text.

### Native repair and evidence

Every native text-bearing cell now has exactly one explicit fontSize equal to the actual renderer size, explicit fontStyle matching SVG bold/normal, and matching left/centre alignment. This includes titles, authors, lifeline labels, guards and message labels. Empty rectangle cells no longer duplicate separately drawn sequence-header text. Source geometry and export font sizes were preserved; the 9 pt constraint was not relaxed.

All **17 sequence native minima are now 23 px / 9.2362 pt at 170 mm**. DCD native minima remain 18 px / 9.7795 pt at 230 mm; their titles correctly use 22 px and bold. The new audit compares a multiset of **every individual text line, font size and bold flag** between native XML and SVG for all **72 diagrams**, rather than trusting a nominal minimum. It passes exactly. All **278 edge endpoints** resolve; source/member and frozen SSD checks still pass for 5 UC-03 and 12 UC-06 occurrences.

Evidence: `Part2/notes/P3-C/repair_audit.json`, `semantic_audit.json`, refreshed `visual_receipts.json` and `reproducibility.json`. All 72 generator ASTs parse, all current source/export/proof hashes agree, and the two standalone generator rebuild checks remain byte-identical. Native draw.io editing/render-engine behavior and final DOCX/PDF placement remain **UNTESTED**; explicit native styles and source checks are not a native-application pass.

### Accepted C-R1–C-R3 reflected in owned views

- **C-R1 resolved:** the approved canonical logical MenuController → HubMenuItem dependency is filtered into all six UC-06 listing all/final projections (Parts H/I/J) and copied into corresponding normalized sequence metadata. Its source evidence explicitly states mediation by MenuDAO and an attribute note, not a direct Python method call. CRC collaborators and explanatory prose now distinguish that logical responsibility. No dataclass behavior method was invented.
- **C-R2 resolved:** the canonical `association_class = true` flag renders HubMenuItem as «association class» in every owned DCD where it appears. The approved association-class note and responsibility are reflected in .1/CRC prose, retaining the canonical multiplicities, navigation and suppressed domain FK scalars.
- **C-R3 resolved:** corrected inventory/matrix SQL facts contain only table `hub` for HubDAO.update; the docstring-derived `an` table is gone. Current target signature parameter/default/return metadata was read and reconciled. The .1 tables now include the reviewed admin adapter P4-TARGET statuses: hubs (P3-S02), catalogue/hub_menu (P2-S14), list_item (P2-S15). Their daggers are visible in DCDs and applicable sequence adapter labels. Existing symbols did not clear behavioral targets.

No further shared-model request remains from this repair. The canonical model was read only and its hash stayed **bd415d6b5874d373cd5eb928dc9b218d27d499e36052589304912a2c33cdd437** throughout the refresh checks.

### Forward maintenance verified

DCD generators read signatures, types, status markers, association-class classification and selected approved dependencies from the shared model at render time. Missing selected members fail clearly instead of silently disappearing. A target keeps its dagger even when the symbol/signature exists; only an explicitly reviewed model MATCH clears it.

Sequence generators read both controller and view-adapter status from the shared model. A changed controller signature fails before export and instructs the maintainer to review the SSD argument aliases. After that review, the explicit refresh command below updates controller/route mappings from the canonical responsibility rows, validates declared alias arity/keyword names against the reviewed signature, records that signature and rerenders the existing owned files:

```powershell
& 'C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -I 'D:/RAD/FINAL/Part2/notes/P3-C/repair_refresh.py'
```

Then refresh proofs with `proofs.py` and run `audit.py` plus `repair_audit.py` in the same scratch folder; review any changed figures and matching prose. The refresh helper updates existing diagram specifications and never runs the stale whole-package `build.py`; the guarantee matrices, report polish and CRC explanation were preserved.

Pure **in-memory synthetic formatting probes** verify refreshed DCD signatures, target dagger retention, controller/view dagger removal for a mock reviewed MATCH, and failure on a stale sequence signature. Canonical status was never modified. These probes are artifact-maintenance evidence, not implementation or behavioral qualification.

### Preservation, visual review and current limits

Before the repair, all 369 lane repo files and relevant scratch/proof bytes were copied to:

`D:/RAD/FINAL/Part2/notes/P3_trash/P3-C_integration_20261025T040039Z/`

Its `snapshot_manifest.json` retains original source paths and hashes; `P3-C/repair_snapshot.json` points to it. No deletion or stale whole-builder overwrite was used.

All 72 source/export sets were regenerated. **20 PNG/SVG views changed** (15 DCDs for classification/dependencies/adapter targets and 5 sequences for adapter daggers); the other 52 visual pairs remain byte-identical to their previously inspected forms. Every changed PNG and independently Edge-rasterized SVG was reopened through **repair_pairs_01.png–repair_pairs_05.png**. Dense `dcd_uc06_final_PartH`, `dcd_uc06_view_PartB` and `seq_uc06_listItemAtHub` were also reopened full size in both forms. No new clipping, label overlap or arrow-through-class text was observed. The original 17 sequence native-source repairs are additionally covered by the exhaustive XML/SVG text-line audit even where visual PNG/SVG bytes did not change.

The exact original repo write set was retained: owned 72 diagram families, two class tables, two CRC files, two selectors, two report sources and this report. Scratch helpers/proofs remain in P3-C, with the explicit superseded-byte archive above. No shared model/inventory/matrix, app, tests, schema, frozen Phase 1/2, Git or configuration was written or executed; no child agent or external action was introduced. Root's integrated cross-check, review and G3 decision remain root-owned. This repair has no remaining access blocker or new assumption requiring a decision.
