# Phase 3 root report

Author: 722I0004 · AI-assisted (Codex)

25–26/10/2026, Asia/Bangkok. Scope: target design only, Section III and IV 4.1–4.3.2. No application import, execution, tests or runtime qualification. All code observations are **Static**.

## Sources read

Locked plan §§1–5, P3/P4/P5/P7, §§7.3/10–12; Part2 README, links, Phase 3 prompt/checklist; primary Requirements and Case Study PDFs directly extracted with pypdf, template paragraphs/tables with python-docx, marking and team-template cells with openpyxl. Direct extracts: `D:/RAD/FINAL/Part2/notes/P3_primary_sources.json`. Documents/PDF/Spreadsheets skills and supplied balanced-diagrams ZIP skill read. Frozen Part 1 content/style and P2 renderer patterns are read-only references. P2-root/review/brief, registers/ledgers, six descriptions, assembled II, traceability, models and AST facts are design inputs; no web source or newer library assumption is needed.

## Wave 0 and baseline

The repo was clean on `part2` before creating the preflight helper. C0 is **45ac76221b0a103174c7c01d17577e6e49cfd665**; no committed app changes since G2 and no uncommitted app changes. Start manifest `Part2/notes/P3_start_hashes.json` protects 1,730 files, including Part 1, application/tests/schema/entrypoints, plan/links, workbook working/staged bytes, sections I/II and all pre-existing model bytes plus P2 descriptions/registers/ledgers. New Phase 3 stems are allowed; traceability and AI log are explicitly mutable Phase 3 integration outputs. No differing lecturer answer to L1/L3/L6 is recorded; defaults remain unanswered and the stop rule does not fire.

`p3_code_inventory.py C0` inventories 48 modules, 83 classes, 63 route records and 13 tables using Git committed blobs + AST/SQL parsing. It never imports application code. `operation_realisation.csv` preserves all 41 SSD occurrences. `p3_seed_design.py` records explicit mappings/targets; `p3_design_model.py` builds the single shared source, including blueprint/module roles and per-element statuses. MATCH means static correspondence only. Target signatures are not silently presented as existing code. Shared transaction/rowcount defects propagate to affected write operations.

## Plan issues

| Issue | Conservative resolution / proposed clarification |
|---|---|
| Prompt counts 41 rows but per-UC distinct-name counts sum to 39 | Frozen `ssd_flow_membership.csv` has 41 occurrences / 39 distinct UC-operation pairs / 38 op IDs. UC-06 listCatalogue repeats in Parts A/B/C: 12 occurrences, 10 names. Preserve all 41 rows and sequence views, with their exact source pointers; never alter P2. |
| G3 says diagrams match code; P3 prompt explicitly permits target design before P4 | Every element is MATCH, P4-TARGET or GAP at C0; G3 is design readiness with disclosed P4 obligations, not implementation completion. Future cross-check retains behavioral targets until evidence clears them. |
| Existing domain dataclasses carry scalar relation IDs; B5 prohibits domain FK attributes on DCDs | Keep exact scalars in inventory/class-to-table mapping; project them to associations/multiplicities in diagrams, with omission stated. No fabricated domain attributes/methods. |
| L heading in locked plan is future-dated; trace status has no Designed value | Preserve truthful planned/unanswered L records. At integration retain Analysed for design-linked main rows and do not fabricate a new trace status. |
| 4.3.4 SQL / full item 24 and P2-IV completion are outside P3 | Supply mapping/design evidence only. Explicit P7 SQL/source and P5 UI/integration placeholders; no full implementation/rubric score claimed. |

## Additional Static P4 findings

| ID | Evidence at C0 | Required design / subphase |
|---|---|---|
| P3-S01 | PlaceOrderController.suggest_hubs sorts `(load/capacity, id)` | BR-04 requires `(load/capacity, raw distance, id)`; F-04 also covers raw range. P4.3. |
| P3-S02 | HubController.list_hubs has only user_id and always list_all | Honor optional includeArchived in OP-23 with default True; no removal of retained history. P4.2. |
| P3-S03 | Several controller mutation calls discard boolean DAO results; shared transaction helper omits COMMIT-error rollback | Conditional-save rowcount outcomes and controlled busy/commit failure are design targets in P4.1 and the affected UC subphase. P2-S13 remains the shared COMMIT finding. |
| P3-S04 | Strict import audit: 43 cross-layer records plus presentation.auth→root NAV, 44 records/23 pairs | Explicit boundary disposition in P4.9; no implicit persistence-mapper exception. A static policy finding does not prove runtime failure. |

## Shared mapping decisions

- P2-S06: propose minimal per-ID `OrderArchiveController.archive_order(user_id, order_id)` and conditional `OrderDAO.archive_one(order_id, now)` as GAP; retain separately named existing batch archive. SUC-09 stays supporting scope.
- P2-S14: propose one `MenuController.list_catalogue(user_id, hub_id=None)` wrapper (GAP) over the real catalogue/hub-menu/all-hub readers; preserve one SSD op and three UC-06 occurrences.
- P2-S15: `list_item_at_hub(..., available=True)` and `MenuDAO.add_listing(..., available=True)` insert initial availability atomically; no briefly orderable intermediate listing.
- P2-S16: updateMenuItem.brandId is current-parent form context; draft update_item pins current.brand_id. No reparenting or restore operation is proposed.
- P2-S18: workload_report uses all retained hub identities, archived hubs with no open work included.
- P2-S08: PaymentDAO.insert maps updated_at to the supplied value or created_at; optional Python typing is not a missing SQL value or demonstrated failure.

## Wave 1 integration

All four Wave 1 successful final handoffs arrived before root opened the reports. All requests were then read as one bundle. Originals are preserved in `Part2/notes/P3_trash/wave1_preintegration.zip`, with 1,746-file manifest in `P3-root/wave1_preintegration_manifest.json`. Accepted requests and evidence are recorded in `P3-root/wave1_adoption.json`.

| Requests | Root decision and reason |
|---|---|
| A R-A01 | Accepted: Quote.fingerprint uses domain PaymentMethod/OnlineOption parameters; a domain class must not depend on the controller PaymentChoice type. F-07 / P4.3 remains explicit. |
| A R-A02; B-1 | Accepted: typed Order/Delivery local receivers are not identically named Flask modules. Removed false upward navigation and added source-backed controller/common/entity dependencies, including DeliveryController→Payment. |
| A R-A03; D-1 | Accepted: layered DCDs draw only downward dependencies. All 44 strict import finding records /23 module pairs remain accounted for as P3-S04/P4.9, with no mapper exception or runtime-failure claim. |
| A R-A04 | Accepted: release_payment must persist the checked amount/refund and state within the transaction. Changing an in-memory state alone does not establish the SUC guarantee. |
| A R-A05 | Accepted: cancel/decline writes cite their supporting contracts; they are not labelled as queries with no persistent effect. Frozen main PC/MG anchors remain unchanged. |
| B-2 | Accepted: menu_item_id travels through ReportDAO grouping, SalesReport.top_items and presentation. The target tuple is (item ID, snapshot name, quantity, revenue), F-09/P4.8. |
| B-3; C-R3 | Accepted: target signature, parameter and return metadata agree. SQL extraction resolves literal fragments passed to execute methods and excludes a docstring's false table `an`; this is an inventory correction, not an app defect. |
| C-R1 / C-R2 | Accepted: mediated MenuController→HubMenuItem responsibility and HubMenuItem association-class metadata; no invented Python method. |
| C message kinds | Accepted: only call messages resolve as receiver methods; SSD, create, return and note roles have their own checks. |
| D-2 | Accepted: customer constraints P2-S03/S07 are P4.7 inputs and created_at P2-S02 is P4.1. P2-S08 has a real created_at fallback and needs no invented fix. |

Root's first 273-figure integration diagnostic found 200 failing checks: 68 missing native author labels, 68 footer legibility failures and 46 upward DCD dependencies in B; 17 native-font discrepancies in C; and one missing DeliveryController→Payment model dependency. The latter was corrected in the shared model. These are recorded defects to repair, not waived checks. Root dispatched three disjoint repair lanes: same A/C identities and a new Sol/high B-repair worker after original B had completed. Their report barrier applies to the entire three-worker batch. No report or unfinished artifact in this repair batch is read before all three final handoffs.

Root also replaced the package metadata's fictional `Database` class label with the actual `database (module)` role, clarified 14 bootstrap imports including app.py, and accepted D's request in section 4.2. Both the changed direct PNG and independently rasterized SVG were opened and inspected; `P3-root/package_integration_qa.json` records the source hashes. Native application opening remains UNTESTED.

All three successful repair handoffs were received before root opened P3-A's new section, P3-B-fix and P3-C's new section. No new model request remained from B/C. A's R-A06 was accepted: the model generator now consolidates 331 dependency records to 320 unique keys, retaining the stricter status and combined evidence. The effective status/direction graph and all non-dependency model fields are unchanged. Root reran every one of the 278 figure generators: all succeeded and no PNG/SVG bytes changed, so existing visual proofs remain applicable. `P3-root/R_A06_refresh.json` records before/after model hashes and actual source/export changes; originals are preserved in `P3_trash/wave1_before_dependency_consolidation.zip`.

The current Wave 1 checker passes **14,802 checks** for 278 figures, 44 design-sequence views, all 41 SSD occurrences and all 30 main PC/MG anchors. It is explicitly an **incomplete-mode integration checkpoint**, with no DAO views yet, and does not establish G3. Responsibility statuses are 10 MATCH, 28 P4-TARGET and 3 GAP occurrences. Root also normalized the two B-lane CRC headings to the exact template wording; previous source bytes are archived in `P3_trash/B_heading_reconciliation`. All six main names and 30 required subsection titles were checked against the frozen analysis/template.

Root's ERD semantic pass corrected four reversed manual multiplicity labels and one detached endpoint on Parts A/B. Schema/mapping metadata had been correct, so metadata-only FK coverage had missed these drawn defects. All 18 FKs now pass 126 schema/end-label/native-position/boundary checks; the auditor rejects the preserved original diagrams with the expected four label and one attachment failures. Both current image forms of every changed page were opened. Earlier border-clearance changes and the accepted P4.7 mapping assignments are reproducible in the coordinator. These are design-artifact corrections, not new application defects or P4 findings. Receipts: `erd_cardinality_qa.json`, `erd_auditor_regression.json`, `erd_label_qa.json` and the 328-check `mapping_crosscheck.json` under P3-root. The full checker normalizes in-memory FK tuples and serialized JSON lists before comparison.

Architecture/mapping commits are ef9af54, 328d564 and efa8762. The six package commits are UC-01 1987226, UC-02 32a54ea, UC-03 833eeec, UC-04 3a692ef, UC-05 33ae5a0 and UC-06 cab293e. Wave 2 was dispatched only after cab293e. During staged review root removed trailing empty source lines from 206 new P3 Python/CRC files; Python AST equality is recorded in EOF_normalization.json and all image bytes remain unchanged. Original B reports retain their intentional Markdown hard-break spaces and original handoff text.

### Wave 1 usage interruption and same-identity recovery

At 18:08 UTC (25/10 01:08 Asia/Bangkok), runtime status showed A/B/C/D errored with `usage_limit_exceeded`, all before a final report. The owner explicitly said to continue root and subagents. The live account tool returned `ordinaryUsageAllowed=true`; root resumed the same p3_a/p3_b/p3_c/p3_d identities with followup_task, preserving their lanes/drafts. No replacement, model/config change, credit purchase or reset was made. Metadata-only process/file timestamp/status inspection did not open unfinished reports or inspect worker artifact contents. The four-report barrier remains mandatory. Root prepared independent inventory/signature metadata corrections in its own scripts while the wave runs; shared model regeneration waits for integration.

Post-resumption runtime checks confirmed all four running. At 18:37 UTC, A/C/D had final notifications and B remained running with generation log timestamps in that minute. The next bounded liveness check at approximately 19:06 UTC again found B running; its builder and visual-audit metadata had fresh timestamps at 02:04–02:06 local time. No stalled-worker recovery or replacement was warranted. The three completed reports remained unopened while B finished.

B subsequently stopped on another usage-limit error before its final report. On the owner's second explicit continuation, 25/10 03:22 UTC / 10:22 Bangkok, the live account tool again returned ordinaryUsageAllowed=true. Root resumed the same p3_b identity from the latest 02:13 local QA files, with no restart, replacement, model/config change or credit action. A/C/D stayed completed; their reports remained unopened pending B's successful final handoff. Resume checks re-established the branch/HEAD and app-diff boundary before continuing.

The later three-worker repair batch had fresh scratch timestamps at approximately 04:10 UTC; metadata-only checks found A/C/B-fix running. B-fix then sent its successful final handoff. C subsequently failed with a usage-limit notification before its repair handoff, and A had no successful repair handoff recorded. On the owner's next continuation, 25/10 06:33 UTC /13:33 Bangkok, ordinaryUsageAllowed was true. Native followup_task restored the same A/C identities and list_agents confirmed them running. B-fix was not restarted. The three-repair-report barrier remains closed until A/C both finish; B-fix's completed report is still unopened. Root retained commits babbe4a and ef9af54 and rechecked the original protected-byte manifest and controlling prompt/plan hashes before integration.

## Wave 2 / Wave 3 integration

E and F were dispatched on 25/10 after all six package commits, both generic workers explicitly selected as gpt-6.1-sol / high. E owns only subsystem DCD/report4.1; F owns only seqdao prefixes/report4.3.2. Shared model is frozen at SHA256 fe3e521d4eea7c66c2819a1acbb67101ecfd3fe49162650fb2dc273195079a6b. Root will not open either unfinished report or artifact before both successful final handoffs. Metadata-only liveness/recovery stays bounded; no model/config change or replacement is inferred.

Both successful final handoffs were received before root opened E/F reports together. Neither requested a shared-model change; root accepts both packages with no status promotion. The model remains SHA256 fe3e521d4eea7c66c2819a1acbb67101ecfd3fe49162650fb2dc273195079a6b. E is committed as e33678d (subsystem DCD); F as ce62686 (eight DAO operations). Worker-local checks and all-image inspection receipts remain distinct from root verification.

The full C0 cross-check passes **20,297 checks, zero failures**, without incomplete mode: 389 figure/source sets, 44 design-sequence views, 43 DAO views, all 41 SSD occurrences and 30 PC/MG anchors. Root added explicit 4.1 presence, all-104-role, exact-once 365-method/278-attribute and all-38-association coverage guards. Root opened the dense subsystem declaration and composition figures and the paired replacement sequence proof. Every owned PNG/SVG was opened by its worker; proofs and hashes are retained under P3-E/P3-F.

Assembly resolves all includes and exact III/IV headings. Its first audit caught a stale UC-04 domain filename in five links; root preserved the source in P3_trash/report_link_reconciliation and changed the references to the actual dcd_uc04_domain stem. No figure changed. The strengthened audit checks ordinary source/vector links as well as images and now passes 1,987 checks. Traceability links 40/52 requirement rows to their applicable main-UC design operations; all future evidence columns remain blank and original statuses remain Analysed/Planned. The P4 register is 121 rows/96 elements, including 64 operation-linked and 57 explicitly shared/supporting rows. Report 4.3.3–6 contains only P5/P7 pending markers.

On the owner's continuation at 25/10 approximately 11:52 UTC /18:52 Bangkok, the native agent registry initially exposed only root. The live account tool reported ordinaryUsageAllowed=true. Root sent follow-up tasks to the same p3_e/p3_f identities to recover their existing workstreams, without replacing either worker or changing model/configuration. No report or unfinished worker artifact was opened. The original prompt still equals its saved controlling copy; the locked plan hash remains cbadf1c3833fecba16769d9036cb4ebfe1e563f845379ab3559dbe6f990790f3. A fresh binary check found all 1,730 original protected files unchanged (P3-root/resume_hash_check_20261025_1154.json). The E/F barrier remains closed until both successful final handoffs.

## Wave 4 independent review

The sole read-only reviewer delivered P3-review.md for integrated revision d85d067. Its independent verdict is **NOT READY for an unqualified G3/B5 closure at the reviewed artifact state**. That verdict is preserved verbatim; root has not relabelled it. The reviewer independently reproduced the 20,297-check structural pass and identified four gaps outside that checker's former scope: R1 guarded interaction geometry (MEDIUM), R2 separate adjacent multiplicities (MEDIUM), R3 three missing success results (LOW), and R4 dependency/synchronous-call arrow styles (LOW). Root accepts all four as design-artifact defects, not application failures.

Root preserved 2,430 current model/document files and the reviewer bytes in P3_trash/before_independent_review_repairs.zip; pre_review_repair_manifest.json records the original reviewer hash. Four disjoint same-identity repair lanes A/B-fix/C/F own only their original UC/DAO families. The whole-four-worker barrier applies: no unfinished report or artifact is read until every final handoff. E and the reviewer are completed; neither is restarted. The shared design model and all protected application/analysis sources remain frozen.

Root repaired the three package dependencies to actual dashed/open arrows in native XML, SVG and PNG, using an explicit local visual-preset adapter without modifying the frozen P2 renderer. Both current export forms were opened; review_package_qa.json checks all three styles and binds the fresh independent raster. Root is strengthening C6 to inspect actual fragment containment, native end-label geometry, success returns and call/reply styles. The earlier structural pass is not used to waive any of these findings.

All four successful repair handoffs arrived before root read A/B-fix/C/F together. F, then C, then A completed while their reports stayed closed; B-fix's final handoff released the barrier. No shared-model change was requested or adopted. Root accepted the notation repairs and separately handled R-A07 below.

### Root dispositions after the independent review

| Finding | Disposition and current evidence |
|---|---|
| R1 MEDIUM: guarded alternatives | Fixed. A adds actual exclusive outcome/compensation regions; F has102 actual guarded fragments with terminal invalid-target withdrawal and separate valid continuation; B adds real accepted/refusal operands plus conditional controller invocation. C fixes missing native dividers/lifelines while retaining its existing semantic operands. Root checks actual native bounds, visible guards and contained message paths. Root opened checkout E/DAO G and replacement DAO C/D in both PNG/independent-SVG forms; success cannot enter compensation and invalid withdrawal cannot fall through to valid writes. |
| R2 MEDIUM: detached multiplicities | Fixed across all six UC families: A93association projections/186end labels; B41/82; C10/20. Two native text cells carry the actual canonical end values beside attached endpoints; role text is separate. Root checks canonical values, actual native label text, adjacency and attachment, and rejects the former combined format. UC01 relationship A, UC06 domain A and UC02 all-layer were opened in both forms. |
| R3 LOW: missing success returns | Fixed. cancelOrder/rejectOrder/declineReplacement continue explicitly to PartB, with cancelledOrderAndAmounts/rejectedOrder/rejectedOrderAndAmounts as dashed open replies inside successful COMMIT-qualified operands. Root opened all three current PartB pairs. Exact SSD occurrence identity and failure paths remain unchanged. |
| R4 LOW: arrow roles | Fixed for the reported package and sequence roles. The package has three actual dashed/open dependencies. Actual synchronous sequence requests have filled closed heads; replies are dashed/open. B/C additionally repaired replies and native parity found in their own audit. A's twelve inheritance projections explicitly retain hollow triangles. Root checks native role styles and inspected the changed vector/raster samples. |
| R-A07: result required prematurely on each part | Accepted as a checker correction. The first combined run found exactly three per-page failures on the first pages of the split commands. C6 now aggregates by UC/op_id/immutable SSD occurrence, requires a visible named result inside a COMMIT-qualified native operand, and verifies a connected mutually linked continuation graph with visible text. It does not demand a premature success on PartA. The preserved original missing-result case still fails the regression. |

The strengthened full C0 check passes **24,849 checks, zero failures**, without incomplete mode: **397 figure/source sets**, **52 report-III sequence views**, **43 DAO views**, **41 SSD occurrences**, and **30 main PC/MG anchors**. Responsibility statuses remain10MATCH/28P4-TARGET/3GAP; the model SHA remains fe3e521d4eea7c66c2819a1acbb67101ecfd3fe49162650fb2dc273195079a6b. No target was promoted from a signature match.

`notation_auditor_regression.json` still rejects the preserved erroneous package arrows, combined end-label cells, out-of-frame replacement messages, missing success result and open synchronous calls. `final_visual_coverage.json` reconciles every current PNG/SVG/native set and independent-raster hash with completed inspection receipts: A140/B68/C72/D6/E68/F43. Workers inspected every changed pair; root independently reopened eleven critical post-repair pairs plus the package pair. Root's sample does not claim all397 were personally reopened. A's historical per-row visual_qa inspection string was not rewritten by its renderer; the opened wave4_sheet_manifest and wave4_receipt bind the92 changed pairs, and unchanged pairs retain their exact inspected hashes.

Reports were reassembled after repairs. The artifact audit passes **2,019 checks**, all links resolve, future4.3.3–6 bodies are P5/P7 pending only, and all required headings remain exact. Traceability stays40/52 design-linked, with the12 supporting-only/non-operation rows explicitly accounted for in traceability_scope_rationale.json. Future code/test/result columns remain blank. P4_design_inputs.csv remains121rows/96elements with operation IDs or explicit shared scope.

**Root post-fix assessment:** R1–R4 are resolved in the design artifacts and the P3 target-design scope is ready for G3 closure after the final integrity/staging receipt. This is root's assessment of the repaired state. The sole review's original NOT READY verdict for d85d067 is unchanged; no second independent approval is claimed. Runtime correctness, P4 implementation, native draw.io/Excel and final DOCX/PDF placement remain unqualified. Closure receipts record the final immutable-source and staging gates.

The integrated repair is committed as f823552. Its staged whitespace checker had exit2 for142 trailing empty EOF lines and two intentional Markdown hard breaks; root let the commit proceed before reviewing that result. The EOF-only follow-up preserves all original bytes in post_review_EOF_originals.zip, proves Python AST equality and leaves every PNG/SVG/native byte unchanged. Original B-fix report hard breaks remain untouched. The full24,849-check audit and2,019-check assembled-source audit were refreshed after normalization; source hash bindings now name the normalized bytes. post_review_EOF_normalization.json records this correction separately from the semantic repair evidence.

On 26/10 approximately00:09 Bangkok (25/10 17:09UTC), the owner again requested continuation. F's successful repair handoff was already recorded and remains unopened; C had stopped on a usage-limit error and A/B-fix had no successful repair handoffs recorded. Live ordinaryUsageAllowed=true; root resumed the same A/B-fix/C identities and confirmed them running. No replacement, reset/purchase, model/config change or restart was made. The four-worker report barrier remains closed. A fresh receipt resume_hash_check_20261026_0009.json confirms all1,730 protected bytes unchanged, the exact controlling prompt match and the locked plan hash; decision_log.md has no working-tree change. Pending lecturer discussion dated26/10 is still a plan, not a claim that it happened.

## Marking evidence pointers

Fresh primary marking workbook: the physical rows below are verified in P3-root/marking_rows.json; no full implementation score is claimed.

| Item / physical row | Evidence or scoped gap |
|---|---|
| 20 / Checklist 33: author on diagrams/use cases | All six III titles and captions; native editable-source author checks and each worker's exported image proofs. |
| 21 / Checklist 34: per-UC layered DCD | III 3.1.2–3.6.2, each five projections i–v; four package roles express presentation/business/data-access tiers. |
| 22 / Checklist 35: CRC and sequences | UC-01…06/crc.md and III 3.x.4; all 41 exact frozen SSD occurrences, receiver methods and 30 PC/MG anchors checked. No communication diagrams. |
| 23 / Checklist 36: final DCD | III 3.1.5–3.6.5, dcd_uc0x_final views and sequence receiver reconciliation; shared subsystem 4.1 supplies supporting declarations. |
| 24 / Checklist 37: packages, mapping, SQL | IV4.2 package/import audit and IV4.3.1 schema-v2 mapping, 13 tables/110 columns/18 FKs. SQL excerpts are explicitly P7 pending in4.3.4; item24 is not claimed fully satisfied by P3 alone. |
| Part3 item33 / Checklist47: design model shown | These DCD/CRC/sequence sources are presentation inputs. No presentation delivery, slide or video completion is claimed. |
| P2-III Excellent / Rubric Guide9: layered classes | Typed class tables, per-UC five-view DCDs, real blueprint routes; forbidden imports disclosed separately. |
| P2-III Excellent / row9: DCD/CRC/sequence consistent with analysis | Frozen descriptions/SSD pointers and PC/MG register; operation_realisation.csv, design_consistency.csv, full static cross-check and independent review. |
| P2-III Excellent / row9: complete final DCD | All six final views declare every actual/marked-target sequence receiver method, with visible inherited receivers checked. |
| P2-IV Excellent / row10: database mapping and SQL | Mapping and ERD supplied and statically checked; SQL excerpts and execution qualification remain P7/later evidence. |
| P2-IV Excellent / row10: code follows design | Explicit MATCH/P4-TARGET/GAP inventory and P4_design_inputs.csv are design inputs; application conformance remains P4 work. |
| P2-IV Excellent / row10: UI traces to SSDs | Design route responsibility is mapped; actual UI evidence remains P5 in4.3.3. |
| P2-IV Excellent / row10: integrated working system | Transaction/DAO design in4.3.2; runtime integration remains P5 in4.3.6. |
| P2-IV Excellent / row10: source files included | Every actual design figure has generator/JSON/editable source/PNG/SVG. Final tagged source/release links remain P7; no push/tag is invented. |

## P4 design inputs

The element-specific register is `docs/part2/design/design_annotations.json` (P4_inputs and target dependencies), joined to SSD op IDs in `operation_realisation.csv`. `docs/part2/design/P4_design_inputs.csv` currently carries 121 rows for 96 member/schema/import/dependency elements; shared/supporting obligations are explicit where there is no main-UC op ID. Existing F-01…09 and P2-S01…18 remain P2-root inputs; design additions P3-S01…04 above do not imply execution. The register is regenerated after final integration; the exact rerun command follows closure.

After each P4 commit, rerun against the committed code while retaining behavioral targets until their obligations are reviewed:

```powershell
Set-Location -LiteralPath 'D:\RAD\FINAL\SaigonBite'
& 'C:\Users\ADMIN\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 -I 'docs/part2/_scripts/p3_design_crosscheck.py' --commit HEAD
```

## Pending owner facts and limits

⟦PENDING: actual L1–L6 answers/unanswered records, discussion planned 26/10 and checkpoint 31/10⟧; ⟦PENDING: Q1–Q5 original submission dates and answers, Dat by 31/10⟧; ⟦PENDING: real feedback/approval and official Part 2 deadline, when received/slot opens⟧. Native draw.io editing, native Excel and final DOCX/PDF placement are UNTESTED. No external upload/push/tag/merge is authorized. Next prompt is P4.1 unless P4 has already started.
