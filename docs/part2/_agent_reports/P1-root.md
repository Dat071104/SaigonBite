# Phase 1 root report

Author: 722I0004 · AI-assisted (Codex)

Date: 23/10/2026 (Asia/Bangkok). Scope: P0 prerequisites and P1 only. Branch: part2. Starting main: 50a3e9f. Preserved WIP: 4b0103c. Application correctness is not assessed in this phase.

Continuation ran 23–24/10/2026; closure is dated 24/10/2026 (Asia/Bangkok). The Gantt and source facts retain their explicit 23/10 cutoff. All five current worker/reviewer dispatches occurred on 23/10, as verified from actual transcript timestamps.

## Sources read

- Locked PLAN_SaigonBite_Part2_Final.md, especially §§0–4, P0/P1, §§8–11; Part2/README.md; Part2/content/links.json; Part2/codex/P1_CHECKLIST.md.
- Primary Lec_re/RAD_Sem01_2627_FinalProject_Requirements_SaigonBite.pdf, §§2, 4, 6–9 (pypdf direct extraction); primary case PDF, both pages. Convenience text in Part2_Plan_Review/source_evidence was also read.
- Primary Lec_re/RAD_Sem01_2627_Report_Template.docx: section I headings read using python-docx; kept verbatim for assembly. No DOCX deliverable is built in Phase 1.
- Primary Lec_re/RAD_Sem01_2627_MarkingSheet.xlsx: Checklist identifiers 9–13 and 41 read from workbook cells; source not edited.
- Primary team workbook template Instructions and frozen Part1_v2/drive_upload/Team02_RAD_Sem01_2627_Team_Workbook.xlsx: sheet structure, existing input, lecturer cells, formulas and validation inspected.
- Frozen Part1_v2/content/content_master.md §10.1, §6 and §11; Part1_v2/build/docx/gantt.py. Diagram workers read the original process and style helpers.
- balanced-diagrams.skill.txt is ZIP content; balanced-diagrams/SKILL.md read using zipfile. PDF, Documents and Spreadsheets skills used. Documents skill is read-only for heading inspection; no Word output is claimed.

## Baseline and authorization

The user explicitly authorized four parallel drafting workstreams, one reviewer, local commits and submission staging. This is Heavy work; the root warned about scope/token cost before execution. No additional permission was needed. Source writes are disjoint. The root retains git, contracts, workbook, checklist, staging and integration.

The WIP commit preserves 81 pre-existing draft application changes; diff --cached --check exited 0. Staged scope and key schema/init/security/rules changes were inspected and added text scanned for obvious private-key/API-key patterns and forbidden local artifact paths. No such matches printed. This is preservation review, not a claim that the draft is correct. No pytest suite was run or repaired. The historical 8 accounts / 40 pages smoke is labelled Reachable only.

Canonical proposal in repo docs/part1 is byte-identical to the eLearning staging proposal. Dat's submitted status is owner-attributed from the locked plan; no receipt was invented or written inside frozen Part 1.

## Plan issues

| Issue | Conservative interpretation / proposed correction for owner |
|---|---|
| Checklist says marking workbook rows 11, 12, 13, 41, but these are item identifiers in column B | Evidence is mapped to identifiers 11/12/13/41 at physical Excel rows 24/25/26/56. Proposed clarification: write “Checklist item numbers”. No source edited. |
| Template title says I. Business Requirements (1 point); requirements PDF and rubric allocate 5 marks | Preserve the exact template title, use rubric allocation only when discussing marks; no score promised. Owner may seek a template correction. |
| Locked plan L heading says “asked 26/10”, a future date on 23/10 | Record as planned course questions, unanswered until a real response exists. No approval inferred. |
| Plan P0.3 mentions D-1…D-12 but §1 includes D-13 | Include D-13 because the checklist explicitly requires D-1…D-13. |
| Plan P1.2 says every FR has a test; Phase 1 checklist requires unknown future columns blank | Preserve blank test/result columns with Planned status; fill and verify them in P2–P4. Phase 1 does not pass G4. |
| Common process caption requests Codex; P1-15 names Codex/Sol 6.1 | Use the common authorship label; treat the longer checklist phrase only as its requested caption alias, never runtime-model evidence. |
| Future case features have no A-ID in the locked A-01–A-19 register | Cite the primary case and state None assigned. Do not invent an assumption ID to satisfy an empty column. Deferred core features retain A-09/L3. |
| The frozen content master A-11 contains an unresolved historical name token | Retain the original wording explicitly as history beside the current D-2 roster; the workbook uses the resolved Quan N. name and retains its source reference. No token is treated as a current fact. |
| P0 asks for a new receipt inside a frozen Part 1 directory | Request the actual owner receipt in Part2/evidence instead; no Part 1 file is written and no receipt is invented. |

## Marking evidence pointers

| Checklist item | Physical Excel row | Evidence |
|---|---|---|
| 11 | 24 | report/I_1-1_vision.md; report/I_1-2_org_gantt.md; models/shared/stakeholder_chart.*; gantt.* |
| 12 | 25 | report/I_1-3_iterations_backlog_risks.md; Part2/workbook/Team02_RAD_Sem01_2627_Team_Workbook.xlsx |
| 13 | 26 | report/I_1-4_narrative_assumptions.md; report/I_1-5_1-6_process.md; report/I_1-7_requirements.md; traceability.csv |
| 41 | 56 | report/I_1-4_narrative_assumptions.md; decision_log.md; working workbook Client Q&A and Assumption Log. Questions are Submitted; answers remain pending. |

## Workbook change note

Updated six existing sheets: Assumption Log, Client Q&A, Backlog & Risks, Requirements List, Iteration Plan and AI Usage Log. The latter two keep the roadmap and declarations consistent with the current report; other sheets remain untouched. Original proposal ownership and historical I1 evidence remain source-attributed.

Artifact Tool authored and recalculated the cells. A narrow OOXML merge retained the original package, styles, controls and unrelated content. The first guard attempts caught default-style normalization and an unstyled-cell fallback; these were corrected before publication. The guard now audits a candidate and replaces the working copy only after success.

Verified 101 original formula texts, 309 original green lecturer cells and all 20 original validation rules. Five validation extensions cover new rows. Original colours are preserved; eight previously blank assumption date cells reuse the existing G5 date format so 23/10/2026 is typed and displayed as a date. Rows were fitted only where content changed. The original 40-slot requirement block and counters remain; a labelled continuation carries 12 NFRs, canonical IDs are beside the template formula IDs, and complete totals are 40 FR / 12 NFR. High maps to Must; Draft maps to Planned, without a test claim.

Client Q&A retains Q1–Q5 as Submitted and empty lecturer answers/dates. The draft course-question rows were cleared from student input only; L1–L6 remain separately in report 1.4.2 and decision_log.md. In-memory recalculation changed the counter to 6 and an over-limit warning, then restored 5 and OK before export. Artifact Tool's saved-workbook formula-error scan matched zero entries. Evidence: Part2/notes/P1_workbook_preservation.json and P1_workbook_preview/. Native Microsoft Excel was not used; no native-engine claim is made.

## Cross-consistency and review

The continuation preserved all existing drafts in Part2/notes/P1_resume_existing_drafts.zip and reused WIP 4b0103c and contracts 63cfd44. The original start manifest was verified before resumed writes: all boundaries matched. Four disjoint workers ran: A/B gpt-6-luna at max, C/D gpt-6.1-sol at high. Their report files were opened together only after C's final notification, when all four had finished. Earlier automatic final notifications were not used for partial integration.

Root structure check: 40 FR + 12 NFR = 52 unique trace rows; all six main UCs, nine SUCs and BR-01–26 represented; seven future trace fields blank; author 722I0004 and Planned status throughout; exact template headings in order. A normalized nine-word primary-case overlap scan returned no candidates. Evidence: Part2/notes/P1_structure_check.json.

Root corrections: restored separate rule-table trace/Tests columns without changing contract wording; joined NFR-12 to its Markdown table; normalized assembled heading levels; corrected the impossible 246 mm A4-portrait caption to 180 mm; expanded a stakeholder service card to contain its text and regenerated all three exports. Root inspected the final stakeholder/Gantt/process overviews and every A-G activity proof. Process figures require A4 landscape at 230 mm wide (minimum 218.3 mm); final PDF placement is a P7 check. Draw.io XML and endpoints are verified; native draw.io application rendering remains untested.

The C worker's temporary deletion was rejected by automatic approval review as blocked by policy. Root used reversible moves: retained the isolated profile at Part2/notes/P1_diagram_browser_profile and nine A4 proofs at Part2/notes/P1_diagram_a4, outside the versioned source and upload set. The diagram builder now places its profile outside the repo. Nothing was deleted.

Independent review: P1-review.md conditionally accepted the content after one medium provenance correction; it found no high-severity contract, coverage, preservation or integrity blocker. Root closed both findings:

| Finding | Root disposition | Verification |
|---|---|---|
| R1: A-19 detailed receipt contract labelled wholly case-fixed | Closed. Receipt availability remains case-required; detailed fields/presentation are explicitly BR-13/A-19 team defaults, not client-confirmed. Updated source, assembly and workbook J23/L23. | Rebuilt assembly; Artifact Tool recalculation/export and preservation guard; final receipt-status preview inspected. Fields, lecturer cells and source contracts unchanged. |
| R2: two Part G activities lack visible scope boundaries | Closed. Added two named disjoint activity frames, each containing its own initial and activity-final node. Repositioned only final markers and routed the same seven control edges. No fork/join or business transition added. | p1_refine_part_g.py passed nine-node containment, disjoint scopes, XML references and renderer geometry/semantics; matching PNG and 230 mm A4 proof inspected. Updated the bundle, separate source/SVG/PNG, QA hashes and explanation. |

The independent review is preserved as its original pre-fix assessment. These are root-verified corrections, not a second independent sign-off. Final native Excel/draw.io and PDF placement remain untested later-phase checks. Root's G1 decision is documentary readiness only; the application is not qualified by this phase.

## Integrity and staging

Start manifest: D:/RAD/FINAL/Part2/notes/P1_start_hashes.json. Frozen boundaries: 1,245 Part1_v2 files (excluding interpreter caches), 11 docs/part1 files, 85 saigonbite files, 12 tests, 4 db files, app.py and init_db.py, plan and links. End comparison and staging hashes follow.

End comparison: **PASS, zero changes/additions/removals**. Part1_v2: 1,245 files; docs/part1: 11 files; app: 85; tests: 12; db: 4; and two entrypoints. Locked plan and links.json are unchanged. `git diff --exit-code 4b0103c -- saigonbite tests db app.py init_db.py` exited 0. No application test suite was run. Evidence: Part2/notes/P1_end_hash_check.json.

Staging copied the working workbook byte-for-byte and 39 model source/export/support files, each matching the repository source. Workbook SHA-256: 110ea5c940119e56e0495bc14a245f74f39d63b4896f19ab68d67c3794baac54. The eLearning staging folder contains 0 files. All staging paths and hashes: Part2/notes/P1_staging_manifest.json.

## Owner pending items

- Part 1 feedback and L1–L6: 26/10; record real answers, or no answer, at checkpoint 31/10.
- Q1–Q5: already Submitted, no answers yet; confirm original submitted date by 31/10 if available. All five slots are used.
- Save actual Part 1 submission receipt outside frozen Part1_v2 for final evidence audit; no new receipt claim.
- Explain the AI-assisted artifacts and retain full earlier prompts/outputs if available for a lecturer request within 48 hours. L6 remains unanswered.
- Official Part 2 eLearning deadline: check when the slot opens; 15/11 is a team target.

## Closure

**G1 READY for the Phase 1 documentary scope, closed 24/10/2026.** P0-01–P0-08: 8/8; P1-01–P1-33: 33/33. No checklist item is unticked and no review finding remains open. Client answers, feedback and later-phase measurements remain pending, as explicitly allowed by this draft gate.

| Commit | Message |
|---|---|
| 4b0103c | WIP: Part 2 draft (tests not collecting yet) |
| 63cfd44 | Part 2 Phase 1: preserve baseline and freeze business contracts |
| 93ba789 | Part 2 report I: vision, roadmap and risks |
| f08d729 | Part 2 report I: stakeholder chart and planned Gantt |
| 8191591 | Part 2 report I: business narrative and assumption log |
| 95adb56 | Part 2 report I: business process v2 and swimlane activities |
| cbe1d37 | Part 2 report I: measurable requirements and traceability |
| 7b597b6 | Part 2 Phase 1: integrate report and guarded workbook workflow |
| 0dd931c | Part 2 Phase 1: resolve G1 provenance and activity-scope findings |

The first two commits were reused from the preserved preflight; the rest were created in this continuation. The subsequent closure commit contains this receipt; its final hash is recorded in Part2/notes/P1_final_receipt.json and the user response. No push, tag, merge, author rewrite or configuration change occurred.

## Closure receipt

| Record | Disposition |
|---|---|
| Phase checklist | Updated 41 evidence-backed boxes; Part2/codex/P1_CHECKLIST.md and notes/P1_checklist_summary.json. |
| Report and traceability | Section I 1.1–1.7 assembled from six source parts; 40 FR / 12 NFR; 52 Planned rows with future evidence blank. |
| Contracts and decisions | Rule text unchanged; trace columns repaired; interpretation log records R1/R2. Locked plan not edited. |
| AI log and worker records | Prior attempt and current root/four workers/reviewer declared; report-reading barrier honored; full available prompts/transcripts retained privately in Part2/notes. |
| Workbook | Six existing sheets updated; preservation/recalculation and visual checks complete; 101 formulas, 309 lecturer cells, 20 original validations retained. |
| Integrity and staging | Zero frozen-boundary changes; workbook plus 39 model files copied with hashes; no eLearning files. |
| Managed ops | Not needed: target repository has no _agent_ops/. Phase records above hold implementation, decisions, milestone and handoff evidence; no unrelated infrastructure created. |

## Owner upload and next phase

Upload D:/RAD/FINAL/Part2/drive_upload/Team02_RAD_Sem01_2627_Team_Workbook.xlsx to the Drive top level, replacing the prior workbook. Upload D:/RAD/FINAL/Part2/drive_upload/Part2/models/ into Drive Part2/models/. Nothing is submitted to eLearning or pushed to GitHub in this phase; local report/contracts/model sources are on branch part2.

Next authorized prompt can address P4.1 foundation collection/green checks and then P2 analysis, using this requirement/trace/contract baseline. The locked plan requires foundation repair before further analysis; neither P4.1 nor P2 was executed here. Preserve all future result fields until their evidence exists. Native Excel/draw.io and final PDF placement are untested; final export/placement remains a later-phase gate.
