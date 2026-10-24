# P2-G — UC-03 and UC-06 completed packages

Author: 722I0004 · AI-assisted (Codex)

24/10/2026, Asia/Bangkok. Assigned scope: P2-41–45 and P2-56–60. Both analysis packages are complete within G's write set. No application/test/database execution, git command, shared-source edit, Part 1 edit, external contact or delegation was performed. This is analysis and diagram verification, not a measured implementation result.

## Files written

Author: 722I0004 · AI-assisted (Codex)

- `docs/part2/UC-03/description.md` and `docs/part2/UC-06/description.md`.
- `docs/part2/report/II_2-2-3_UC-03.md` and `docs/part2/report/II_2-2-6_UC-06.md`.
- `models/UC-03/activity_uc03.{drawio,png,svg,py,json}` and `ssd_uc03.{drawio,png,svg,py,json}`.
- `models/UC-06/activity_uc06.{drawio,png,svg,py,json}` and `ssd_uc06.{drawio,png,svg,py,json}`, plus all matching `_PartA`, `_PartB`, `_PartC` files for each stem.
- This report. Total: 55 repo files; the 54 preceding files and SHA-256 hashes are listed in `D:/RAD/FINAL/Part2/notes/P2-G/written_manifest.json`.

Scratch is confined to `D:/RAD/FINAL/Part2/notes/P2-G/`. Owned helpers: `p2_g_build.py`, `p2_g_renderer.py`, `p2_g_check.py`. All repo Python helpers use owned activity/SSD stems. The renderer follows the read-only `models/shared/sm_order.py` editable XML/SVG and hidden Edge export conventions, with independent Pillow PNG rendering; it does not import or edit that shared module. Bundled Python was invoked with `-X utf8 -I`; no app modules were imported.

## Checklist evidence

Author: 722I0004 · AI-assisted (Codex)

| ID | Disposition | Concrete evidence |
|---|---|---|
| P2-41 | Done | UC-03 description: nine template fields in order; numbered Actor / System main flow; A01–A04 and E01–E04; all three registered anchors verbatim. |
| P2-42 | Done | Figure 2.14, `activity_uc03.*`: inspection/create/update/archive; guarded decisions H-choice/H-valid; explicit H-merge; whole-request activity final. |
| P2-43 | Done | Figure 2.15, `ssd_uc03.*`: Admin/:System; OP-23/24/34/35/36 only, exact parameters, dashed returns, loop/opt/alt. |
| P2-44 | Done | `II_2-2-3_UC-03.md`: i–iv; description include; Hub Figure 2.6 and shared Account Figure 2.9 placement reference; PC/MG table. |
| P2-45 | Done | Anchor and operation tables below; scratch structural checks; final exports visually inspected. |
| P2-56 | Done | UC-06 description: nine fields in order; main flow 1–6; A01–A10 and E01–E04; five anchors verbatim; Brand, MenuItem and pair-listing paths. |
| P2-57 | Done | Figures 2.20A–C, `activity_uc06_PartA/B/C.*`: Brand, MenuItem and HubMenuItem read/create/update/archive or unlist; two guarded decisions and explicit merge per page. |
| P2-58 | Done | Figures 2.21A–C, `ssd_uc06_PartA/B/C.*`: Admin/:System; OP-25 and OP-37–45 only; parameters/returns and guarded loop/opt/alt. |
| P2-59 | Done | `II_2-2-6_UC-06.md`: exact i–iv headings, description include, Catalogue Figures 2.8A–D cross-reference and PC/MG→transition/stored-fact table. |
| P2-60 | Done | Every anchor/message mapped below; catalogue unchanged; structural checks and independent PNG/SVG visual inspection. |

## PC/MG consistency evidence for root

Author: 722I0004 · AI-assisted (Codex)

Node IDs are the editable draw.io IDs. SSD message IDs are also actual edge IDs; `saved` and `refused` are common dashed response edges after the command-selection alt. The catalogue uses one response alt because exactly one selected command occurs per request.

| Anchor | Description steps / branch | Activity node IDs | SSD message IDs | State transition or stored fact |
|---|---|---|---|---|
| UC03-PC01 | 3–5; A02 | H-request, H-validate, H-valid, H-save | M03-03 createHub; M03-04 updateHub; saved | Figure 2.6 create→ACTIVE or ACTIVE self-transition; valid code/coordinates/fee/capacity stored. |
| UC03-PC02 | A03; 6 | H-request, H-validate, H-save | M03-05 archiveHub; saved | Figure 2.6 ACTIVE→ARCHIVED; archived_at hides browse/checkout while history/report references survive. |
| UC03-MG01 | E01–E04; A03 open-order check | H-validate, H-valid, H-refuse | M03-03–05; refused; M03-02_return for missing detail | No transition/attribute change after duplicate, capacity<1, unsafe archive, denied/stale context or rollback. |
| UC06-PC01 | 3–5; A02–A06 | CA-request/validate/save; CB-request/validate/save | M06-A02–A04; M06-B02–B04; saved | Figures 2.8A/B creation→ACTIVE, attribute self-update, archive→ARCHIVED. |
| UC06-PC02 | A07–A09 | CC-request, CC-validate, CC-save | M06-C02–C04; saved | Figures 2.8C/D: pair inserted AVAILABLE/SOLD_OUT, flag switched, or association removed. |
| UC06-PC03 | A03; A06–A08 | CA-save; CB-save; CC-save; each validate | M06-A04; M06-B04; M06-C02/M06-C03; saved | Archived Brand/MenuItem exclusion and per-hub SOLD_OUT are stored eligibility facts; AVAILABLE cannot bypass archived parents. |
| UC06-MG01 | 5; A02–A09; E01–E04 | CA/CB/CC-save and CA/CB/CC-refuse | All M06-A02–A04/B02–B04/C02–C04; saved/refused | Historical OrderLine snapshot name/price/quantity unchanged through maintenance and refusals, including physical unlist. |
| UC06-MG02 | E01; A02/A04/A05/A07 validation | CA/CB/CC-validate, CA/CB/CC-valid, CA/CB/CC-refuse | M06-A02/A03; M06-B02/B03; M06-C02; refused | Duplicate active names/pair or invalid price is refused before any lasting change. |

All eight anchor texts were compared verbatim against `pc_mg_register.csv` by `p2_g_check.py`. No additional anchor was created. Minimum guarantees on other failures are stated as no-change outcomes while preserving the registered snapshot invariant; MG02 remains specifically the duplicate/price refusal guarantee.

## Every SSD call and query flow membership

Author: 722I0004 · AI-assisted (Codex)

Machine-readable root input: `D:/RAD/FINAL/Part2/notes/P2-G/operation_flow_membership.csv` (17 message occurrences, 15 distinct catalogue operations). It includes UC, operation, catalogue ID, description step, activity nodes, SSD file and actual message ID. Repeated listCatalogue messages are the same read operation in three independently initiated entity views, not three new operations.

| Message | Catalogue operation | Description membership | Activity membership |
|---|---|---|---|
| M03-01 | OP-23 listHubs(includeArchived?) | 1–2; A04 | H-browse → H-read |
| M03-02 | OP-24 getHub(hubId) | A01; used before A02/A03 | H-browse → H-read |
| M03-03 | OP-34 createHub(code, name, address, latitude, longitude, baseDeliveryFee, capacity) | 3–5 | H-request → H-validate → H-valid → H-save/H-refuse |
| M03-04 | OP-35 updateHub(hubId, code, name, address, latitude, longitude, baseDeliveryFee, capacity) | A02 | same maintenance route |
| M03-05 | OP-36 archiveHub(hubId) | A03 | same maintenance route |
| M06-A01 | OP-25 listCatalogue(hubId?) | 1–2; A01; before 3/A02/A03 | CA-browse → CA-read |
| M06-A02 | OP-37 createBrand(name) | 3–5 | CA-request → CA-validate → CA-valid → CA-save/CA-refuse |
| M06-A03 | OP-38 updateBrand(brandId, name) | A02 | same Brand maintenance route |
| M06-A04 | OP-39 archiveBrand(brandId) | A03 | same Brand maintenance route |
| M06-B01 | OP-25 listCatalogue(hubId?) | 1–2; A01; before A04–A06 | CB-browse → CB-read |
| M06-B02 | OP-40 createMenuItem(brandId, name, description, price) | A04 | CB-request → CB-validate → CB-valid → CB-save/CB-refuse |
| M06-B03 | OP-41 updateMenuItem(itemId, brandId, name, description, price) | A05 | same item maintenance route |
| M06-B04 | OP-42 archiveMenuItem(itemId) | A06 | same item maintenance route |
| M06-C01 | OP-25 listCatalogue(hubId?) | 1–2; A01; A07–A09 hub inspection | CC-browse → CC-read |
| M06-C02 | OP-43 listItemAtHub(hubId, itemId, available) | A07 | CC-request → CC-validate → CC-valid → CC-save/CC-refuse |
| M06-C03 | OP-44 setListingAvailability(hubId, itemId, available) | A08 | same listing maintenance route |
| M06-C04 | OP-45 unlistItemAtHub(hubId, itemId) | A09 | same listing maintenance route |

Every call is in its description and in the frozen catalogue with whitespace-normalized parameter equality. Mutation responses are exactly `savedRecord` or `controlledRefusal`; getHub uses `hubAndArchiveGuard | refusal`; other queries retain their catalogue response names. There are no controller/DAO/SQL/widget messages. SUC-06 `setMenuAvailability` is a supporting-reference name only, not a call in an Admin SSD.

## Guard and visual QA

Author: 722I0004 · AI-assisted (Codex)

All four activity pages have two decisions: H/CA/CB/CC-choice has `[inspect only]` versus `[maintain]`; H/CA/CB/CC-valid has `[guards pass; save completes]` versus `[else]`. Each pair is complete and exclusive within the active-Admin precondition. Conditional guard details are in each validate action; the change is attempted atomically only after valid guards, before the outcome decision. Read inspection, successful maintenance and failure converge at an explicit diamond merge before the actor observes the result; no join/fork is used. Each whole request ends in an activity final. Initial and final degrees, connected message/control edges, guarded branches and three merge inputs were checked programmatically.

Eight actual diagram pages plus two first-page aliases were opened and visually inspected as PNGs, and all ten SVGs were independently rendered in hidden Edge and their PNG proofs opened. Primary PNGs are independently drawn with Pillow, rather than screenshots of their SVG. Visual iterations corrected overlapping SSD headers/call labels, a two-line call touching its arrow, and competing activity merge routes. Final inspection found readable labels, arrows, guards, lifelines, captions and exact author text without clipping. The placement is 230 mm A4 landscape: 1100×760 canvas, 2200×1520 raster, minimum 16 px corresponding to **9.48 pt** at placed width. Catalogue figures are split A–C rather than shrunk. Unsuffixed catalogue PNG/SVG are byte-identical PartA aliases; unsuffixed draw.io contains all three pages.

Scratch evidence: `structural_checks.json` (8 pages; 8 anchors; 17 messages; PASS), the four `*_qa.json` files, individual `*_svg.png` independent-render proofs, `*_edge.log`, eight `*_A4.png` proofs at exactly 230 mm width/300 dpi, and captured Edge profiles. XML parses successfully; every message/control edge has valid source and target IDs; text-fit checks pass. Native draw.io and the application were not executed, so no native-editor or application correctness claim is made.

## BLOCKED / ASSUMED

Author: 722I0004 · AI-assisted (Codex)

No analysis blocker remains. Conservative interpretations:

- Each diagram page models one active-Admin request, not a transaction spanning the complete maintenance session; further commands repeat the scenario. Authentication denial and stale reads are described under exceptions, with active-Admin as the activity precondition.
- Valid coordinates are required without adopting draft-only HCMC bounds, code format, maximum price/fee/capacity or field-length limits as new business rules.
- Catalogue uniqueness is required among active names in the relevant scope; the draft schema is stricter (`brand.name UNIQUE`, `(brand_id,name) UNIQUE` include archived rows). No archived-name reuse is promised or new restore path added.
- The OP-41 brandId parameter identifies the current parent. UC-06 does not promise moving an item to another Brand; the Static draft deliberately fixes its parent.
- `savedRecord` on unlist is the catalogue's acknowledgement of removal, not a new persisted record or a retained HubMenuItem tombstone.
- A retained listing flag can change without overriding archived-parent exclusion; active parents are mandatory for a new listing. SOLD_OUT is never global.

## Requests to root

Author: 722I0004 · AI-assisted (Codex)

1. Insert canonical HUB and USER_ACCOUNT state blocks once under UC-03 iv, and CATALOGUE once under UC-06 iv, as already agreed in the shared brief. This worker did not duplicate shared state images.
2. Preserve the 230 mm landscape placement and use catalogue A–C together. Consume the operation-membership CSV and the eight-anchor mapping above for root `analysis_consistency.csv`; do not treat first-page aliases as complete catalogue diagrams.
3. Record as Static P3/P4 mapping obligations if not already covered: catalogue `listCatalogue(hubId?)` combines draft `catalogue`/`hub_menu`; OP-43 initial `available` needs an atomic draft mapping because `list_item_at_hub` accepts no flag; OP-41 brandId is current-parent context. Draft lifetime name uniqueness and hard-coded validation maxima/coordinate bounds must not silently become new locked rules. No shared catalogue edit is requested in this wave.

## Sources used

Author: 722I0004 · AI-assisted (Codex)

First reads: updated `P2-brief.md` and `P2-root.md`, including finalized Wave 1 dispositions. Locked plan §§1–5, P2/P3.1, §§7/10/11; Part2 README, links and checklist; direct `Part2/notes/P2_primary_sources.json`; direct primary Case/Requirements PDFs, Report_Template DOCX description tables, MarkingSheet Checklist/Rubric Guide and Team_Workbook_Template Team & Use Cases/Events Table/CRUD Check. The source read evidence is in scratch `sources_read.json`. Frozen Part1 content master, proc_build/proc_geom/proc_views and diagram_changes were read only for scope/style. `balanced-diagrams/SKILL.md` was read directly from the ZIP-format `balanced-diagrams.skill.txt`. Repo rules, decision log, PC/MG register and SSD catalogue govern the contracts; finalized team/use-case/domain, SUC, CRUD and state outputs were read-only references. Draft HubController, MenuController, domain and schema were inspected as Static names/mapping evidence only. No current rule or lecturer/client approval was inferred from draft code or unanswered defaults.
