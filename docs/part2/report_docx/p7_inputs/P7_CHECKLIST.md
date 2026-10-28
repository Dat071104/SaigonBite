# P7 checklist — report (LaTeX + DOCX), release, submission → G7

Tick `[x]` only with an evidence pointer (file path, commit, or screenshot). "Not run" items keep `[ ]` with the reason.

## Stage 1 — LaTeX zip + DOCX (stop and tell Dat)

### Entry
- [x] P7-01 Entry HEAD `97574bd4a6834978978e0b6bdb16ca7c6a642d52`, clean, branch `part2` (A1.1; updated prompt supersedes stale checklist hash) — `Part2/notes/P7/progress.json`
- [x] P7-02 Runtime diff since `252ada1` empty (A1.2) — `Part2/notes/P7/progress.json`
- [x] P7-03 Full suite 928 passed — `Part2/notes/P7/entry_pytest.txt`
- [x] P7-04 Requirements §4/§6/§7/§8/§9, template, plan §P7/§7.3/§10/§11 and writing skill read — source files specified in attached P7 prompt
- [x] P7-05 Owner-facts message F1–F5 sent to Dat (Vietnamese) — `Part2/notes/P7/owner_facts.md`

### Owner facts and markers
- [x] P7-06 F1 Part 1 feedback → report 1.1 approval row — `docs/part2/report/I_1-1_vision.md`; `Part2/notes/P7/meaning_lock/1.1.json`
- [x] P7-07 F2 L1–L6 → 1.4.2 + decision_log 31/10 entry (answer or "no answer; default followed") — F2 corrected 28/10: L2–L5 accepted at review, L1 no approval needed, L6 open — Part2/notes/P7/owner_facts.md; docs/part2/decision_log.md
- [x] P7-08 F3 Q1–Q5 dates/answers (no guessed dates) — submission date not recorded; no client answer — Part2/notes/P7/owner_facts.md
- [x] P7-09 A-11 quoted placeholder explained — quoted Part 1 placeholder explained — docs/part2/report/I_1-4_narrative_assumptions.md
- [ ] P7-10 Zero `⟦…⟧` markers left in `docs/part2/report/` and `decision_log.md` (grep output saved) — Historical A-11 quotation retained as required by A2; rendered using glyph commands. See docs/part2/report/I_1-4_narrative_assumptions.md.

### Sources and figures
- [x] P7-11 `source_map.csv`: one canonical source per template heading; aggregates diffed — 144 mapped headings and ranges — Part2/notes/P7/source_map.csv
- [x] P7-12 `figure_manifest.csv`: every body/appendix figure, author, AI label, width, orientation — 607 placements, 604 images — docs/part2/latex/figure_manifest.csv
- [x] P7-13 No duplicate PNG, no unreferenced PNG; readability checked; issues in `diagram_issues.md` (not fixed) — owner-approved team PartA repetition and readability exceptions — Part2/notes/P7/diagram_issues.md
- [x] P7-14 Status refresh: no `† P4-TARGET` left in the body without its final status from `p4_design_resolution.csv`; rows without test evidence stay "not implemented" — generated from resolution register; policy rows static — docs/part2/report/Appendix_P4_status.md

### New content
- [x] P7-15 4.3.4 SQL: create DB, tables (schema.sql), sample data, 3–5 queries with real output from a fresh DB — fresh DB outputs — Part2/notes/P7/sql_sample_results.json
- [x] P7-16 4.3.5 key methods per UC: byte-exact excerpts, author ID, tag link — 16 exact excerpts — docs/part2/test_report/p7_2026-10-28/docx_checks.txt
- [x] P7-17 4.3.6 integration: P5 scenario + P6 deployed rerun, order IDs, screenshots — scenario and deployed evidence — docs/part2/report/IV_4-3-6_integration.md
- [x] P7-18 5.1 test plan + table for all 6 UCs, 30 PC/MG rows, test nodes, actual/pass/date/env/commit, `test_cases.csv` — 30 PC/MG rows — docs/part2/test_report/p7_2026-10-28/test_cases.csv
- [x] P7-19 5.2 deployment (RUNBOOK + V_5-2) — deployment instructions — Part2/notes/P7/source_map.csv
- [x] P7-20 5.3 demo steps + screenshots + `\LinkVideo` — demo steps; video pending — Part2/notes/P7/source_map.csv
- [ ] P7-21 Executive Summary (1 page) and Conclusions/Recommendations from the claim ledger; L6/§9 risk in limitations — Claims drafted; one-page layout cannot be verified without rendering.
- [x] P7-22 References: only verified items (textbook 7th ed. + tools with access dates) — verified references — docs/part2/report/References.md
- [x] P7-23 Appendices 1–5 (full-size UC / sequence / class diagrams; Contribution Statement; AI log) — team diagrams and per-UC references per owner decision; contribution and AI log — Part2/notes/P7/source_map.csv
- [x] P7-24 AI log: P7 rows + the 28/10 Claude Opus G6 re-check/P7-prompt row — P7 and Claude recheck entries — docs/part2/ai_usage_log.md; docs/part2/report/Appendix_5.md

### Writing and labels
- [x] P7-25 Prose pass with the skill (Mixed mode, gates 1–4); glossary added; hashes/agent notes moved out of the body — 40-source prose pass — Part2/notes/P7/progress.json
- [x] P7-26 Meaning-lock diff per section: no changed number, ID, state, rule or claim — 40 meaning-lock records — docs/part2/report_docx/p7_inputs/meaning_lock/
- [x] P7-27 `claim_ledger.csv` for ES, 4.3.6, 5.1–5.3, Conclusions; every claim has evidence — claim ledger — Part2/notes/P7/claim_ledger.csv
- [ ] P7-28 Every UC title and figure caption has the author ID; every AI-made section/figure keeps its AI label — Figure labels checked; all section AI labels have not been independently audited.
- [x] P7-29 Contribution facts as recorded (114 commits by Dat; rows 17/39 Partial for Quan L., Quan N.) — contribution statement — docs/part2/report/Appendix_4.md

### LaTeX build tree
- [x] P7-30 Headings verbatim from the template, same order, template numbers; bookmarks + TOC entries per heading — 87 headings, order checked — docs/part2/test_report/p7_2026-10-28/static_checks.txt
- [x] P7-31 Front matter: title page, document table, abstract, IP page (Team 02, 2026), TOC; guidance and instruction page removed — template front matter and Word checks — docs/part2/test_report/p7_2026-10-28/docx_checks.txt
- [x] P7-32 Template tables keep their column headings — template prefix checks PASS for both editions; all 423 content-table headers compared in parity. `docs/part2/test_report/p7_2026-10-28/`
- [x] P7-33 `links.tex` generated from links.json; PENDING renders red — generated macros — docs/part2/latex/links.tex; Part2/content/links.json
- [x] P7-34 Stand-alone `contribution_statement.tex` and `ai_usage_log.tex` — standalone TeX files — docs/part2/latex/contribution_statement.tex; docs/part2/latex/ai_usage_log.tex
- [x] P7-35 Static checks clean (inputs, images, refs/labels, environments, braces, escapes, markers, heading compare, author IDs) — `static_checks.txt` — static PASS, readability exceptions listed — docs/part2/test_report/p7_2026-10-28/static_checks.txt
- [x] P7-36 **No PDF produced** (no pdflatex/latexmk, no Word/LibreOffice export) — no compilation or export — Part2/notes/P7/pack_receipt.json
- [x] P7-37 Zip `Part2/deliverables/Team02_BRS_SRS_for_SaigonBite_latex.zip` + `README_BUILD.txt`; size + sha256 recorded — ZIP integrity, size and SHA-256 — Part2/notes/P7/pack_receipt.json
- [x] P7-37a LaTeX zip contains the screenshots it uses (UI + integration + deployed), nothing else — 604 unique manifest-selected PNGs included — Part2/notes/P7/pack_receipt.json
- [x] P7-37b DOCX built on a copy of the template: Word heading styles, TOC field, guidance removed, landscape plates, links from links.json — `docx_checks.txt` — structural checks PASS; layout and field display await Word — docs/part2/test_report/p7_2026-10-28/docx_checks.txt
- [x] P7-37c Parity LaTeX ↔ DOCX: headings, figure IDs, tables, test rows, ES/5.1/Conclusions numbers — `parity.txt` — structural parity PASS — docs/part2/test_report/p7_2026-10-28/parity.txt
- [x] P7-38 Local commit `P7: report LaTeX source …`; no push, no tag — local B9 commit, no push/tag — git log
- [ ] P7-39 Reply to Dat (Vietnamese) with zip path, compile command, open owner facts, diagram issues, policy risk; **STOP** — verdict `G7-STAGE1 = …`

## Stage 2 — after Dat returns the PDF / log

- [ ] P7-40a Dat chose the edition to submit (recommended DOCX→PDF); the other kept as source —
- [ ] P7-40 Compile errors from Dat's log fixed; static checks rerun; zip rebuilt (≤ 3 rounds) —
- [ ] P7-41 PDF QA: bookmarks, TOC, all template headings, figures readable at 100 %, captions, no PENDING/`??` — `pdf_qa.md` —
- [ ] P7-42 `Readme.txt` from links.json (all required items) —
- [ ] P7-43 Self-assessment xlsx: student cells only, formulas/lecturer cells unchanged (before/after check), rows 9–30 + 39–42 with evidence —
- [ ] P7-44 Team workbook Part 2 sheets filled and staged —
- [ ] P7-45 Contribution Statement signed by all three (Dat's step) —
- [ ] P7-46 Final regression at the final commit; runtime diff vs `28d6b33` empty (VM = tag runtime) —
- [ ] P7-47 Dat's explicit "OK push" recorded; `main` fast-forwarded; tag `v0.9-part2`; pushed —
- [ ] P7-48 GitHub Release with assets; URL in links.json; checked logged out —
- [ ] P7-49 `drive_upload/eLearning/` and `drive_upload/Part2/` staged per the submission map —
- [ ] P7-50 Drive upload + all links checked in a private window (Dat + executor) —
- [ ] P7-51 eLearning submission receipt saved (Dat) —
- [ ] P7-51a If a domain was attached (P6D): links.json, both editions and Readme use it; sslip.io kept as fallback —
- [ ] P7-52 `final_receipt.json` + last commit; verdict G7 —
