# Phase 1 independent review

Author: 722I0004 · AI-assisted (Codex)

Scope: P1-26–P1-31, current integrated Phase 1 files. This reviewer wrote only this report, ran no git commands, application tests, builder or writer helper, and spawned no agents. Inspection used explicit cwd `D:/RAD/FINAL/SaigonBite`.

## Findings, highest priority first

### R1 — Medium: A-19 conflates the case's receipt requirement with the team's detailed receipt contract

Locations: `docs/part2/report/I_1-4_narrative_assumptions.md:48`; assembled `docs/part2/report/I_business_requirements.md:224`; working workbook `Assumption Log!J23` (and its source explanation in `L23`).

The primary case p.1 requires customers to receive a receipt. It does not prescribe the entire A-19 list: printable own-order view, snapshot fields, S/D/F/Q/T, payment state, refund owed and simulator label. Those details come from locked-plan BR-13/A-19. The current status, “Case requirement in the locked plan; no client confirmation needed or inferred”, applies that exemption to the entire detailed assumption. It also sits beside workbook F23, which correctly says “Team decision (not confirmed)”. This is a source-status inconsistency, not an invented client answer or a defect in the chosen receipt contents.

Correction before closing P1-31: distinguish the fixed receipt need from its default implementation contract in the section source, rebuilt assembly and working workbook. Suggested status: “Receipt availability is a case requirement. The detailed contents and presentation are team defaults under BR-13/A-19, not client-confirmed.” Keep the existing field contract, sources, typed team-review date and blank lecturer cells. No new client question or locked-plan edit is needed.

### R2 — Low, nonblocking: make Part G's two activity scopes explicit in the drawing

Locations: `models/shared/swimlane_v2.json:1287` (Part G), especially initial/final nodes at lines 1292/1316 and 1323/1353; corresponding Part G page in `swimlane_v2.drawio`, `swimlane_v2_PartG.drawio/.svg/.png`; explanation `docs/part2/report/I_1-5_1-6_process.md:28`, `:34`, `:82`.

The two disconnected flows share one lane panel and both use activity finals. Read as one activity, that picture would give the finals a broader scope than intended. The title/subtitle and report explicitly identify two separate activities, so I accept the documented interpretation: an admin maintenance request and an independent manager report request. I found no control edge that makes a report depend on a maintenance write. This is notation ambiguity, not evidence that the business contract requires concurrency or that one real request terminates another.

Recommended refinement: put the two flows in named activity frames, or split Part G into separately named activity diagrams. Preserve each flow's own System responsibility and final. A short local scope label beside each flow is a smaller improvement if the current page structure is retained. Do not add a fork/join: these requests are independent.

## G1 recommendation

**Conditional acceptance of the Phase 1 content after R1's narrow provenance correction. No high-severity business-contract, coverage, workbook-preservation or frozen-boundary blocker was found.** R2 can be fixed or retained explicitly as a minor notation limitation. This recommendation covers documentary readiness only; it does not assess application correctness or satisfy later analysis, implementation, testing, deployment or final-PDF gates.

P1-31 remains root-owned: record the finding disposition, complete the final commit and final integrity receipt. P1-32/33 staging and closure are correctly still pending by sequence; they are not missing-business-content findings. The independent review itself should be added to the root-owned AI logs before closure.

## Checklist evidence

| Item | Independent disposition | Evidence |
|---|---|---|
| P1-26 | Pass | 40 FRs, each with at least one UC/SUC and a populated source; all six main UCs and all nine SUCs have FR coverage. All 26 BR IDs appear in FR source cells. All 12 NFRs have observable criteria and a measurement method, without a claimed result. Report and CSV sources/UC scopes match exactly. |
| P1-27 | Pass subject to R1 | No newly invented lecturer feedback, client answer, member contribution or measured performance found. Approval table distinguishes D-4 from lecturer approval; 26/10 feedback is pending; L1–L6 are planned; Q1–Q5 answer dates remain unknown. Gantt actual ticks are repository-change dates, not completed iterations or submissions. R1 corrects the receipt-detail provenance. |
| P1-28 | Pass within the stated source conventions | Report prose is English; all numbered template sections and all eleven figure sets have the required author/AI labels. A normalized contiguous-nine-word comparison of every I_*.md file against the primary case returned no matches. Human reading found no copied case narrative. Historical A-11 is clearly quoted as history and immediately followed by the current roster. |
| P1-29 | Pass | Primary marking workbook Checklist column B items 11/12/13/41 are at physical rows 24/25/26/56. Each has a relevant evidence pointer in P1-root.md; sources exist and contain the requested material. This is coverage evidence, not a predicted grade. |
| P1-30 | Pass at review time | Binary SHA-256 comparison with P1_start_hashes.json found zero changed/missing entries in all seven boundaries. Full inventory comparison found no added/missing non-cache files in the five tree boundaries. Counts below. |
| P1-31 | Pending root disposition and final commit | R1 requires a small synchronized correction; R2 is a recorded nonblocking recommendation. Reviewer did not edit sources, workbook, checklist or root records. |

The exact 13-column CSV has 52 unique rows, all authored 722I0004 with Planned status; all seven future columns from PC/MG ID through result evidence remain blank. The 40 FR and 12 NFR IDs are identical in report, CSV and workbook canonical-ID cells. NFR-01/06 check row values as well as counts; NFR-12 distinguishes exclusive winners from legal serialized accept-then-cancel outcomes. The <1 second target and HTTPS/VM requirements are explicitly unmeasured.

The assembly contains the primary template's exact I title and ordered 1.1–1.7 headings, including 1.4.1/1.4.2. After removing heading-level prefixes, each section source's full body is contained in the assembly. The narrative body is **773 words**, inside the required 500–900 range. A-01–A-11 preserve the frozen source wording apart from formatting/typographic normalization; A-12–A-19 are present. A-08 is superseded by D-4 and not labelled lecturer-approved.

## Diagram semantics and visual review

I opened all eleven current PNG exports with view_image: stakeholder chart, Gantt, business-process overview, swimlane overview, and Parts A–G. I separately opened all nine A4 process proofs in `Part2/notes/P1_diagram_a4/` and the two actual SVG browser previews `P1_stakeholder_chart_svg_review.png` and `P1_gantt_svg_review.png`. I read the two process model specifications and QA JSON, parsed every current draw.io/XML and SVG source, and checked endpoint references. These checks do not rely solely on worker assertions or XML node counts.

- Stakeholders include operations/management, hub managers/kitchen/shippers, admin/analysts, Local/Tourist customers and contextual payment provider. Grouping is expressly interaction-based, so no company reporting hierarchy is invented. The expanded administration card contains its current text in both raster and SVG preview.
- Gantt retains six iteration windows and planned milestones. The grey dates 19–20/10 and 23/10 are supported by direct read-only HEAD reflog records, including the 23/10 package-sync entry. Planned bars do not masquerade as elapsed work. The proposal roadmap and locked §8 support the schedule.
- The business overview distinguishes enabling activities and grey deferred work. It is a scope map, not a detailed activity or a claim that replacement consent occurs after delivery; the report states that timing and Part D shows it before confirmation.
- Continuations are coherent: A→P→B→K→C; C→R→D; accepted or invalid-target-withdrawn offers return to K; C→D→E means READY delivery. K's alternative re-entries are not a synchronizing join. Part F is explicitly a separate cancellation request. Refusal flow finals do not claim that an existing order becomes terminal.
- Raw radius, busy/quiet derivation, quote fingerprint/transaction revalidation, simulator decline and atomic save are represented. C/D preserve PLACED while an offer awaits/resolves, require customer consent, and block confirmation with an open offer. Target invalidation withdraws the offer rather than changing the order. Detailed eligibility/ownership/stale-answer guards are supplied in the report and page notes; the summary nodes do not replace those rules.
- Money contracts agree across prose, FRs and diagrams: COD PENDING→PAID only with exact cash T, otherwise VOIDED on an unfulfilled terminal outcome. ONLINE partial liability remains an attribute while PAID; later rejection/cancellation/decline/failure owes the full captured C in REFUND_PENDING, replacing a partial liability. No payout or REFUNDED path is claimed. The 100,000→90,000 oracle is arithmetically consistent, including subsequent cancellation and no second report deduction.
- Delivery has AWAITING_PICKUP→PICKED_UP→DELIVERED/FAILED paired with the Order transitions. Invalid finish preserves OUT_FOR_DELIVERY; no redelivery transition is introduced. Receipt/privacy/tourist contracts match the plan, subject to R1's status wording.
- Part G's maintenance/report flows are disconnected and expressly independent; reports write nothing, archives preserve history and liabilities, and the shipper deactivation guard is present. R2 addresses only the visual scope ambiguity.

No clipped node text or unreadable labels were observed at the required placements. Stakeholder minimum explicit SVG text is 26 units on a 1460-unit width: **9.09 pt at 180 mm portrait**. Gantt is 32/2300: **9.03 pt at 229 mm landscape**. All nine process figures are 16/1100: **9.48 pt at 230 mm landscape**, about 158.9 mm high. C/E have short shared incident-edge stems; the guards and endpoints remain distinguishable, but I do not claim crossing-free routing. All nine current process SVG/PNG hashes match their QA records. Final report insertion must preserve these widths/orientations; final PDF and native draw.io rendering remain untested.

## Workbook audit

Compared the actual working workbook with the frozen Part 1 workbook using openpyxl and direct ZIP/OOXML reads, rather than accepting the preservation note as proof.

- All **101 original formula texts** are unchanged.
- All **309 original green lecturer cells** (fill FFDDF0DF), including their values and styles, are unchanged. Q&A I5:J14 remain empty.
- All **20 original validation rules** are byte-equivalent in their serialized definitions. Exactly five new rules extend the risk/requirement continuation ranges; they do not replace the originals.
- Original styled-cell comparison found only the eight permitted `Assumption Log!G16:G23` number-format changes, from General to the existing G5 `dd/mm/yyyy` format. The values are typed dates. No original colour/style changes were found elsewhere.
- ZIP comparison shows changes only in the six intended sheet XML parts: Client Q&A, Assumption Log, Iteration Plan, Backlog & Risks, Requirements List and AI Usage Log. Other package parts, including original styles, are byte-identical. This resolves apparent None-versus-zero-style differences on blank cells when traversing openpyxl objects; those are not changes to the saved workbook.
- Requirements B/E/F/J/K and canonical I cells match the report's requirement text, scope, source, criterion and priority for all 52 rows. The original block remains rows 5–44; continuation is 49–60. C63/D63 formulas cover both blocks; cached values and independent counts are **40/12**. Canonical FR-xx/NFR-xx IDs sit beside retained template formula IDs.
- Q1–Q5 are Submitted, all five slots are consumed, C16/C17 cached values are **5/5**, and C18 is **OK**. Course-question student inputs in rows 10–14 are clear; L1–L6 remain separately recorded. No submission date or answer was created.
- Cached formula-error scan found zero error-typed cells. I inspected existing current preview ranges for Q&A, new assumptions, NFRs and risk overflow; they were readable. I did not recalculate or export the workbook, change inputs, or claim a native Excel engine check. The root's earlier recalculation experiment is source-attributed evidence only.

The workbook shares R1 in J23. Its F23 already retains the correct not-confirmed team-decision label.

## Frozen-boundary verification

| Manifest boundary | Files checked | Hash mismatches | Added/missing inventory entries |
|---|---:|---:|---|
| Part1_v2 | 1,245 | 0 | 0 / 0 |
| docs/part1 | 11 | 0 | 0 / 0 |
| saigonbite | 85 | 0 | 0 / 0 |
| tests | 12 | 0 | 0 / 0 |
| db | 4 | 0 | 0 / 0 |
| app.py and init_db.py | 2 | 0 | Both present |
| Locked plan and links.json | 2 | 0 | Both present |

The tree inventory applies the start manifest's __pycache__/.pytest_cache exclusions. This includes the submitted deliverables, Part1 staging/model trees and original team workbook through the complete Part1_v2 boundary. The plan hash remains `cbadf1c3833fecba16769d9036cb4ebfe1e563f845379ab3559dbe6f990790f3`; links hash remains `4e8b5df5a2b0f2ee6eb11f80b489debe359ec5276c8b34a697281df62de8f150`.

## Sources and checks actually used

Read all current `docs/part2/report/I_*.md`, `traceability.csv`, `rules.md`, `decision_log.md`, `ai_usage_log.md`, P1-brief, P1-A/B/C/D and P1-root. Read the controlling Part2/codex/P1_PROMPT.md and P1_CHECKLIST.md, locked plan (especially §§1–4, P1, 8, 10, 11), Part2/README.md and links.json. Read model sources/specifications/QA and the two chart builders; no builder was run.

Primary authorities inspected directly: both case-PDF pages; requirements-PDF relevant sections including §§2, 4, 7–9; Report_Template.docx paragraph headings; MarkingSheet.xlsx Checklist items; Team_Workbook_Template.xlsx Instructions; StudentList roster rows matching all three IDs. Frozen sources: content_master.md assumptions/roadmap, original Part 1 process source, original Gantt builder, submitted workbook. Diagram skill ZIP and supplied read-only PDF/Documents/Spreadsheets guidance were consulted. P1_start_hashes.json, P1_structure_check.json, P1_workbook_preservation.json and previews were read as secondary audit evidence and independently checked where asserted above.

Executed only built-in shell reads and inline bundled Python (`python.exe -I -X utf8 -`) for direct pypdf/python-docx/openpyxl/XML/ZIP parsing, text/CSV matching, normalized nine-word overlap, counts, formula/style/validation comparison and hashlib SHA-256 comparisons. Displayed images through view_image. No helper was imported/executed to write notes, no application test suite was run, and no source/workbook/export was changed.

## BLOCKED / ASSUMED and open items

- No inspection blocker remained. No external account, network service or model pricing was needed for this bounded review.
- Template “1 point” versus rubric 5 marks, marking item numbers versus physical rows, future features without assigned A-IDs, historic A-11 placeholder, and the common Codex caption versus checklist alias are accurately disclosed source limitations. I did not invent replacement evidence or require a locked-source edit.
- Existing I1 results, submission status and D-13 cloud facts are source-attributed historical/owner statements. This review does not rerun historical tests, independently prove a submission receipt or verify cloud billing. Gantt actual markers were checked only as dated repository changes.
- Client answers, 26/10 feedback, L1–L6 outcomes, official eLearning deadline, later performance/deployment results, and final native/PDF rendering remain pending as documented. A pending approval is not converted into approval.
- Root should apply R1, record R2's disposition, synchronize assembly/workbook/AI declarations, finish P1-31–33 and closure, then repeat the relevant read-only integrity checks. No broad rework, application edit or new phase is recommended by this audit.

## Files changed by this reviewer

Only `docs/part2/_agent_reports/P1-review.md`.
