# P2-D — CRUD verification report

Author: 722I0004 · AI-assisted (Codex)

## Files written

- `docs/part2/report/II_2-3_crud.md` — five template-numbered actor CRUD tables, bidirectional §2.4/§2.5 cell comparison, schema-table coverage, archive/persistence semantics, and root requests.

## Checklist evidence

- **P2-25 — completed as a plan-faithful draft.** The report has exactly the five required headings (2.3.1 Customer, 2.3.2 Kitchen staff, 2.3.3 Shipper, 2.3.4 Admin, 2.3.5 Manager), uses the report-template CRUD row structure, reproduces §2.5 cells, and marks intentional blanks. Actor cells without a UC/SUC qualifier remain explicitly unqualified.
- **P2-26 — audited; not satisfied until root resolves the listed mismatches.** The report compares the 13-class §2.4 union in both directions and maps all 13 `db/schema.sql` tables. The report records six unmatched qualified union reads (UserAccount/SUC-01, Customer/SUC-03, Address/UC-01, MenuItem/UC-05, HubMenuItem/UC-05, Payment/UC-02); unqualified Kitchen HubMenuItem and Admin Customer/Order reads; and separate Admin SUC-09 history reads on child classes that are absent from §2.4. Exact evidence and conservative requests appear under “Exact mismatches and requests to root.”
- **P2-27 — completed.** The report includes the archive parent/child visibility rule, history/receipt/report/refund-owed retention, the exact seed-is-not-Create rule, the non-persistent items and the absence of a Shipper table.

## BLOCKED / ASSUMED

- The locked plan contains literal §2.4/§2.5 differences. I preserved §2.5 actor privileges, did not silently amend the locked plan, and did not claim equality. The six missing qualified reads and three ambiguous/extra actor reads are listed in the main report, with one root request per discrepancy.
- Proposed conservative reconciliation for the specifically evidenced archive mismatch: qualify the already listed Admin history reads under SUC-09 and add those same read cells to §2.4 for Order, OrderLine, Payment, Delivery and ReplacementOffer. No privilege is added beyond §2.5.
- `UserAccount R SUC-01` is treated as a system-internal authentication/role lookup unless root explicitly assigns actor self-read cells; no actor grant was inferred.
- The workbook’s generic CRUD Check formula flags blank actor/class operations as “Gap”. These report tables mark such per-actor blanks intentionally; workbook union and formula treatment remain root-owned and were not edited.
- Schema/controller review is Static only. I did not execute the app or tests and make no runtime claim.

## Requests to root

1. Resolve the §2.4/§2.5 reads exactly as itemized in the main report before treating P2-26 as passed or updating the workbook union.
2. Specifically adopt or reject the narrow SUC-09 read reconciliation for archived Order and child rows; clarify the unqualified Admin Customer/Order reads and Kitchen HubMenuItem read.
3. Reconcile the primary workbook CRUD Check sheet with intentional actor-specific blanks without granting generic CRUD rights. No workbook changes were made by this worker.

## Sources used

- `D:/RAD/FINAL/PLAN_SaigonBite_Part2_Final.md`: locked plan §§2.4, 2.5, 3, 4, 5.3, P2, 7, 10 and 11.
- `D:/RAD/FINAL/Part2/README.md`, `content/links.json`, `codex/P2_CHECKLIST.md`, and `notes/P2_primary_sources.json` (direct extracts from the lecturer report-template DOCX, marking workbook, team-workbook template, requirements PDF and case-study PDF).
- `D:/RAD/FINAL/SaigonBite/docs/part2/_agent_reports/P2-brief.md`, Phase 1 report `report/I_business_requirements.md`, `rules.md`, `decision_log.md`, `ssd_operations.csv`, and `pc_mg_register.csv`.
- Frozen `D:/RAD/FINAL/Part1_v2/content/content_master.md`.
- Static draft sources: `SaigonBite/db/schema.sql`, domain `models.py`/`enums.py`, and controller method declarations under `saigonbite/business/controllers/`.
- `Part2_Plan_Review/source_evidence/` was consulted only as a convenience cross-check; plan and primary readings above control.

## Limits

Only the two files listed above were written. No checklist, workbook, app, tests, contracts, plan, links, Part 1, or Section I file was edited. No git command was run; no files were deleted.
