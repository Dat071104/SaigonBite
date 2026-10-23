# Phase 1 Workstream A — Vision, organisation and plan

Author: 722I0004 · AI-assisted (Codex)

## Checklist evidence

| ID | Status | Evidence |
|---|---|---|
| P1-01 | Done | docs/part2/report/I_1-1_vision.md — SaigonBite-specific problem description, paraphrased from the case study. |
| P1-02 | Done | docs/part2/report/I_1-1_vision.md — six UCs, nine SUCs and expected-benefit links; benefits are labelled as unmeasured and tourist menu translation remains out of scope. |
| P1-03 | Done | docs/part2/report/I_1-1_vision.md — D-4 is labelled a team decision; Q1–Q5 dates/answers are unknown/empty; 26/10 feedback and L1–L6 remain pending. |
| P1-04 | Done | models/shared/stakeholder_chart.drawio, .png, .svg and docs/part2/report/I_1-2_org_gantt.md Figure 1. Chart includes all required stakeholder groups and identifies the provider as contextual/simulated. |
| P1-05 | Done | docs/part2/report/I_1-2_org_gantt.md — proposal UC owners are kept separate from actual Part 2 authorship recorded under D-1/J2. |
| P1-06 | Done | models/shared/gantt.py, .drawio, .svg, .png and docs/part2/report/I_1-2_org_gantt.md Figure 2. All six planned iteration windows and plan milestones are present. Only dated Git change markers are shown for 19–20/10 and 23/10. |
| P1-07 | Done | docs/part2/report/I_1-3_iterations_backlog_risks.md — I1–I6 dates, goals, UC/SUC focus, deliverables, backlog linkage and changes from the proposal are documented. |
| P1-08 | Done | Same file — stable BL-01–BL-20 story IDs, MoSCoW, iteration and UC/SUC references; W-01–W-03 mark deferred/future items as Won't this release. |
| P1-09 | Done | Same file — R-06–R-11 cover sole-author/contribution exposure, L6 AI policy, SQLite contention, cloud/org/TLS, L1/L3 scope and schedule budget; all required risk fields are present. |

## Files written

- Updated docs/part2/report/I_1-1_vision.md.
- Added docs/part2/report/I_1-2_org_gantt.md and docs/part2/report/I_1-3_iterations_backlog_risks.md.
- Updated models/shared/stakeholder_chart.py and regenerated models/shared/stakeholder_chart.drawio, .png and .svg.
- Added models/shared/gantt.py and generated models/shared/gantt.drawio, .png and .svg.
- Added this report.

No files outside the assigned write set were edited. No Git commands were run. Part1_v2 builders were read as references and not executed.

## Evidence and checks

- Ran the bundled Python runtime with -I -X utf8 on the stakeholder chart and Gantt builders. The stakeholder layout reported balanced layered LR placement, target ratio 1.35, helper ratio 1.53, and canvas 1460 × 1160. The Gantt builder reported 18 rows, 17/10–30/11/2026, and canvas 2300 × 1544.
- Parsed both draw.io and SVG files as XML. Verified both PNGs at 300 DPI: stakeholder chart 1460 × 1160; Gantt 2300 × 1544.
- Opened both PNGs with view_image. Rendered each SVG locally from its exported SVG elements and opened the rendered previews with view_image; the SVGs match their PNG layouts. Temporary previews were removed.
- At A4 portrait width 246 mm, the stakeholder chart is about 195 mm high; minimum visible type is approximately 12.4 pt. At 180 mm width it remains approximately 9.1 pt. At 229 mm placed width on A4 landscape, Gantt minimum type is approximately 9.0 pt; its image height is about 154 mm before the caption.
- Checked backlog coverage for UC-01–UC-06 and SUC-01–SUC-09; all appear. The six risk IDs and all 23 BL/W row IDs are present. No eight-word phrase from the Case Study PDF is reproduced in the vision or iteration/backlog/risk section.
- No automated tests were run; this workstream changes report sources and diagrams only.

## Assumptions and open items

- Grey Gantt marks are one-day repository-change markers from the local .git/logs/HEAD, not measured work duration, acceptance evidence or proof of submission. The markers are I1 changes on 19–20/10 and the package-sync commit on 23/10. I2 onward remains planned.
- Risk likelihood and impact are qualitative planning judgments, not measured frequencies. BL-01–BL-20 are new report row IDs; proposal US-01–US-22 meanings are not silently reassigned after the D-4 scope change.
- Q1–Q5 still have no recorded answers or known submitted dates; L1–L6 and 26/10 feedback are pending. The official Part 2 eLearning deadline remains to be checked. No lecturer approval is claimed.
- Draw.io sources parsed successfully as XML but were not opened in a diagrams.net editor in this workstream. Root may open them during integration if an editor-level check is desired.

## Sources used

- docs/part2/_agent_reports/P1-brief.md; D:/RAD/FINAL/Part2/codex/P1_PROMPT.md; D:/RAD/FINAL/PLAN_SaigonBite_Part2_Final.md §§1–4, 6 P1, 8–11; D:/RAD/FINAL/Part2/README.md; Part2/content/links.json; Part2/codex/P1_CHECKLIST.md.
- Primary sources: D:/RAD/FINAL/Lec_re/RAD_Sem01_2627_Case_Study_SaigonBite.pdf (pp. 1–2); RAD_Sem01_2627_FinalProject_Requirements_SaigonBite.pdf (pp. 3–4, 6); RAD_Sem01_2627_Report_Template.docx (sections 1.1–1.3). The marking-sheet Checklist and workbook template were not used to author this workstream.
- Read-only Part 1 references: Part1_v2/content/content_master.md §§1, 4.1, 6, 8–10; Part1_v2/build/docx/gantt.py; Part1_v2/notes/diagram_changes.md. The local .git/logs/HEAD file was read directly for dated change evidence; no Git command was run.
- Existing draft and builder: docs/part2/report/I_1-1_vision.md; models/shared/stakeholder_chart.py. Read balanced-diagrams/SKILL.md and scripts/layout_drawio.py from D:/RAD/FINAL/balanced-diagrams.skill.txt as a ZIP, and followed the supplied PDF and Documents skill guidance for read-only source inspection.
