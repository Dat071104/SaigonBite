# P2-A — Wave 1 A: Team analysis

Author: 722I0004 · AI-assisted (Codex)

## Files written

- `docs/part2/report/II_2-1_team_analysis.md` — sections 2.1.1–2.1.5.
- `docs/part2/SUC.md` — contracts for SUC-01–SUC-09.
- `docs/part2/_agent_reports/P2-A.md` — this completion report.

No files outside the assigned write set were changed. No git commands or tests were run.

## Checklist evidence

- **P2-10 — Done:** system narrative covers the scoped workflow and the alternate outcomes for busy hubs, out-of-range addresses, payment declines, kitchen rejection, replacement acceptance/decline, cancellation, and delivery failure. Evidence: `docs/part2/report/II_2-1_team_analysis.md`, §2.1.1.
- **P2-11 — Done:** user-to-goal-to-UC/SUC table covers Customer, Kitchen staff, Shipper, Admin and Manager. Evidence: same file, §2.1.2.
- **P2-12 — Done:** 20 events, within the 14–20 requirement and 20 workbook slots; external, state and temporal types are present; the temporal row explicitly says validity is checked on demand with no scheduler; no database actor is named. Evidence: same file, §2.1.3.
- **P2-13 — Done:** actor descriptions include Customer generalization to Local/Tourist, Payment simulator as external actor, and the reason there is no time-based actor. Evidence: same file, §2.1.4.
- **P2-14 — Done:** six main use cases show full names, proposal owners and actual author 722I0004; nine supporting cases and groups (a)–(d) are listed. Evidence: same file, §2.1.5.
- **P2-15 — Done:** all nine supporting contracts have actors, preconditions, `SUCxx-PCnn` postconditions, BR guards, CRUD cells, served main UCs and conservative failure outcomes. Evidence: `docs/part2/SUC.md`.

## BLOCKED / ASSUMED

- **No blocked items.** Event rows 3–14 classify the plan §4 operation names as `State` because each row describes the resulting lifecycle transition; the named actor command appears as the trigger/source. This keeps the event name and state vocabulary traceable to §4 while preserving that a human action initiates it.
- The locked-plan defaults remain assumptions, not approvals. The current preflight record has no differing answer for L1/L3/L6; the plan schedules L1–L6 clarifications for 26/10. The narrative therefore labels strict CRUD (L1), the payment simulator (L2), and the proposed deferral of complaint/refund/rating (L3) as pending. No approval or implementation result is inferred.
- The 20-row event count uses the workbook's 20 available rows. Several closely related read/maintenance operations are grouped into single events while each remains named in its UC/SUC coverage.

## Open items

- The planned lecturer clarifications and the 31/10 replan checkpoint can change scope or defaults. Update this analysis only after those answers are recorded by the owner.
- Figure 2.1 determines any UML include/extend relationships; this A workstream records serving links only.

## Requests to root

- At P2-28, align the event-type interpretation for rows 3–14 with the root's P2-03 catalogue. If P2-03 treats the actor command rather than the resulting §4 transition as the event, change only the Type cells consistently; the operation names, triggers and responses already match the frozen contracts.

## Sources used

- Shared brief `docs/part2/_agent_reports/P2-brief.md` (read first); locked plan `PLAN_SaigonBite_Part2_Final.md` §§1–5, P2/P2.3, §§7, 10 and 11; `Part2/codex/P2_CHECKLIST.md`; `Part2/README.md`; `Part2/content/links.json`.
- Primary-source extracts in `Part2/notes/P2_primary_sources.json`: case study and final-project requirements PDFs; report-template paragraphs/tables; direct workbook extracts for Team & Use Cases, Events Table, CRUD Check and MarkingSheet Checklist.
- Convenience extracts in `Part2_Plan_Review/source_evidence/` for the case study, final-project requirements and report template; frozen `Part1_v2/content/content_master.md`, Part 1 process diagram source, and submitted Part 1 proposal PDF.
- `docs/part2/rules.md`, `decision_log.md`, `pc_mg_register.csv`, `ssd_operations.csv`, and the locked Part 1 report/materials.

