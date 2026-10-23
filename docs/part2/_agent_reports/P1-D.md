# Phase 1 Wave 1 D — Requirements and traceability

Author: 722I0004 · AI-assisted (Codex)

## Checklist evidence

- **P1-16 — complete.** [I_1-7_requirements.md](../report/I_1-7_requirements.md) retains and refines the interrupted draft's 40 FRs, all in “The system shall …” form with MoSCoW, UC/SUC, primary Case/Requirements pointer, linked plan interpretation, and objective acceptance criterion. All six main UCs, nine SUCs, and BR-01–BR-26 are referenced. Coverage includes Tourist registration and privacy, receipt contents, consent fingerprint, capacity and pickup races, every §3.3 replacement/money rule, the exact reporting periods and metrics, minimum CRUD, and archive/history boundaries.
- **P1-17 — complete.** The report has 12 NFRs. NFR-01–NFR-05 retain the checklist meanings. NFR-06–NFR-11 cover CSRF, secrets, HTTPS/session cookies, 360 CSS-pixel usability, layering, and archive retention. NFR-12 adds the frozen plan's independent-connection/barrier races, serialized outcomes, atomic rollback through COMMIT, and controlled lock-contention response. Every NFR has a concrete planned measurement method; no implementation, application-test, deployment, or performance result is claimed.
- **P1-18 — complete.** [traceability.csv](../traceability.csv) has the exact 13-field header and 52 unique data rows (40 FR + 12 NFR), synchronized to the report's sources and UC/SUC fields. PC/MG ID through result evidence are seven blank fields in every row; report section = I.1.7, actual author = 722I0004, status = Planned.
- **P1-19 — complete with source-boundary note.** The exclusion table links complaint/refund decision, payout, and rating to A-09/L3, without treating L3 as answered. Loyalty, subscriptions, group orders, and scheduled orders point to Case p.2 future scope. The carried A-01–A-19 authority does not assign these future items individual A-IDs; the table explicitly says “None assigned” rather than creating unauthorized IDs.

## Files written

- docs/part2/report/I_1-7_requirements.md — reused correct draft content; refined primary-source pointers, report intervals and empty-sample handling, raw-distance fee examples, replacement consent wording and hand oracle, privacy, and measurement methods; added NFR-12. SHA-256: 2ca376f2789aa4398df31f3b574cca290e35d676655ff3009de2f604104a4593
- docs/part2/traceability.csv — regenerated only from the owned requirements table to keep 52 rows synchronized. SHA-256: 97a3eadedbef46534cf2ad620c1c65e236badbee03bb5acce349e33021f12b32
- docs/part2/_agent_reports/P1-D.md — this completion report.

## BLOCKED / ASSUMED

- No drafting blocker remains. Plan §3 figures and refinements remain team defaults, not client-confirmed facts. All in-scope requirements are Must because this list represents the locked minimum portfolio.
- Q1–Q5 remain Submitted with no answer recorded; the original submission dates are unknown. L1–L6 remain future course clarifications. No approval or feedback is invented.
- Future case features have no assigned A-ID. This is an explicit source limitation, not a proposed amendment to the locked plan or assumption register.
- Unauthorized-request and CSRF methods compare row values and request-connection total_changes as well as counts: counts alone cannot detect an UPDATE. This improves the check without changing the mandated zero-change target.
- Source pointers use actual printed PDF pages and feature topics. No PDF line numbers were invented. The source key distinguishes the case's business need from the plan's team-default refinement.
- No architectural choice, source-code edit, application-test run, git action, workbook edit, or write outside the three-file lane was performed. App/Part 1 hash verification and all phase recordkeeping outside this lane remain with root.

## Open items for root / later phases

- Root may tick P1-16–P1-19 with these evidence paths after its integration review; this worker did not edit the checklist.
- Root must merge AI-use evidence, workbook requirements, and final phase records. This worker did not read any other worker report.
- P2–P5 must populate future traceability fields only as analysis, design, screens, implementation, tests, and result evidence exist. The plan's eventual test linkage is not a Phase 1 completed-test claim.
- Obtain actual Q/L answers and review affected rules at the 31/10 checkpoint. The A-09/L3 exclusions remain conditional; future-item A-IDs may be added only by authorized scope/assumption maintenance, if desired.
- Measure all NFR targets in their relevant implementation/testing/deployment phases; NFR-04's <1 s VM target and NFR-08's HTTPS target are unmeasured.

## Sources read and used in this continuation

- docs/part2/_agent_reports/P1-brief.md; complete Part2/codex/P1_PROMPT.md; Part2/README.md; Part2/content/links.json; Part2/codex/P1_CHECKLIST.md.
- Locked PLAN_SaigonBite_Part2_Final.md §§1–4 and P1, plus §5.1–5.4, P4.3–P4.9 and §7.2 for measurement/concurrency contracts.
- docs/part2/rules.md and docs/part2/decision_log.md for current default and Q/L status.
- Primary Lec_re/RAD_Sem01_2627_Case_Study_SaigonBite.pdf, both pages; primary Lec_re/RAD_Sem01_2627_FinalProject_Requirements_SaigonBite.pdf, complete eight-page text extraction, especially §2 and §4.
- Primary Lec_re/RAD_Sem01_2627_Report_Template.docx: paragraph text read directly from word/document.xml, including section I and exact “1.7 List of Requirements” heading.
- Part1_v2/content/content_master.md §10.1: carried A-01–A-11, especially A-09, read only. No new ID for future case features is present there.
- Part2_Plan_Review/source_evidence/RAD_Sem01_2627_Case_Study_SaigonBite.txt, convenience text, cross-checked against direct primary PDF extraction.
- PDF skill read for source-extraction guidance. No PDF or DOCX was authored or edited.

## Commands and checks run

All commands used explicit cwd D:/RAD/FINAL/SaigonBite in the built-in shell. Bundled Python was invoked as `C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -I -X utf8 -` with inline code; no helper script or intermediate file was written.

1. `Get-Content` / targeted `rg -n` reads of the assigned authorities, owned drafts, source rules and assumption IDs; no git commands.
2. Direct `pypdf.PdfReader` extraction of the two primary PDFs; `zipfile` + ElementTree extraction of the primary report template.
3. Python artifact checks printed: `PASS: 40 FR and 12 NFR; exact 13-column CSV; 52 unique synchronized rows; 7 future columns blank; all Planned/authored 722I0004.`
4. The same check printed: `PASS: all 6 UC, 9 SUC, and 26 BR referenced by FRs; primary Case/Requirements pointer for every FR.` This verifies documentary linkage, not implemented behavior.
5. A normalized contiguous-nine-word comparison of every requirement and acceptance cell against the primary Case PDF printed `PRIMARY CASE nine-word matches in requirement and acceptance cells: []`. This is an own-words aid, not an originality guarantee for every artifact.
6. SHA-256 values for both owned deliverables were computed from their final bytes and are recorded above. No application test suite, browser measurement, deployment, or race experiment was run in Phase 1.
