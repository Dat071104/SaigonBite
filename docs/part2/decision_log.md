# Part 2 decision log

Author: 722I0004 · AI-assisted (Codex)

Recorded 23/10/2026 from the locked plan. Plan evidence claims are attributed to the plan; no new approval is inferred.

| # | Item | Decision | Evidence |
|---|---|---|---|
| D-1 | Who does the work | Dat does all of the Part 2 work (AI-assisted, declared; confirmed by Dat 23/10). The six main UCs keep the proposal owners (UC-01/03 722I0004, UC-02/04 523K0049, UC-05/06 523K0050) because the proposal fixed them. Every artifact shows its **actual author**; proposal owner is a separate column only in the UC list. Nothing is claimed for a member who did not do it. | Requirements §2.1, §8; user 23/10 |
| D-2 | Roster | 722I0004 Dat, 523K0049 Le Minh Quan (Quan L.), 523K0050 Nguyen Minh Quan (Quan N.). IDs verified in `Lec_re/RAD_N02_MonS3_StudentList.xlsx`. | Class list |
| D-3 | Lecturer questions | Do not wait. Build on the defaults in §3; ask at the Part 1 presentation (26/10); record answers or "no answer" on 31/10 (replan checkpoint). Silence is never written as approval. | User 23/10 |
| D-4 | CRUD coverage (L1) | Strict reading: every persistent class has a real minimal create/read/update/archive path in the running app, through supporting UCs. Supersedes Part 1 A-08 (J7). | Requirements §2.1; checklist 18 |
| D-5 | Deployment | One GCP Compute Engine VM: Docker Compose, gunicorn, Caddy (HTTPS), SQLite on a host directory on the VM's persistent disk. Local Docker Compose is the reproducible path and fallback. Vercel retired for Part 2 (separate `/tmp` DB per instance). Cloud deploy is not mandated (rubric V asks for deployment plan + instructions + demonstration). | User 23/10; `test_results/order_kitchen_20261021/` |
| D-6 | Schema | Fresh schema v2 everywhere; I1 demo data treated as disposable (J4). | §0.4 |
| D-7 | TLS hostname | `<static-IP>.sslip.io` via Caddy (no domain purchase); fallback nip.io, then DuckDNS; last fallback local demo (J5). | — |
| D-13 | Cloud account | GCP project "My First Project" on the account 523k0049@student.tdtu.edu.vn (school-managed profile), free trial: ₫7,791,151 (≈ USD 300) and 89 days left on 23/10 → trial ends about **20/01/2027**, after Part 3 grading. Dat operates it. Billing owner is recorded as fact in the runbook. | Screenshot 23/10 |
| D-8 | Client questions vs course clarifications | Q1–Q5 = client questions (limit 5). L1–L6 = course clarifications (J6). | Team workbook |
| D-9 | AI use | Declare all use (plans, code, diagrams, text) in the AI Usage Log; label AI-generated diagrams/text; keep prompts/outputs; Dat must be able to explain every model and code path. Ask L6. | Requirements §9 |
| D-10 | Dates (team targets) | Part 1 eLearning **25/10**; Part 1 live 26/10; replan checkpoint 31/10; feature freeze 12/11; buffer 13/11; PDF QA 14/11; Part 2 submit target **15/11**; presentation 16/11. Official Part 2 date checked when the eLearning slot opens. | Proposal §6; eLearning |
| D-11 | Git | Work on branch `part2`; `main` only moves by merge; release = tag `v0.9-part2` + GitHub Release. Small commits, one concern each. | — |
| D-12 | Test baseline | 96 tests passed at a3feb72 (I1, historical). Current draft: collection error (F-01). No Part 2 pass count exists yet. | pytest 20/10; F-01 |

### 1.1 Lecturer clarifications (course, not client) — planned for 26/10; not yet asked as of 23/10

| ID | Question | Default if no answer | Changes if answer differs |
|---|---|---|---|
| L1 | Must every persistent class have a running CRUD path, or is analysis + seed enough for non-main classes? | Running paths (D-4) | Nothing lost if relaxed |
| L2 | Is a clearly labelled payment simulator acceptable for "online payment"? | Simulator | Would need a sandbox provider — replan |
| L3 | Complaint/refund decision, refund payout and rating deferred (in process + backlog, not built)? | Deferred | Add 1–2 supporting UCs + CRUD + tests — replan |
| L4 | Python/Flask acceptable? | Yes | Replan (unlikely) |
| L5 | Roster/ownership confirmed? | As D-2 | Update UC list |
| L6 | AI-assisted code generation, fully declared in the AI log — acceptable? | Declare fully; continue | If not allowed: stop, ask what must be redone, replan |

### 1.2 Client questions (max 5) — status kept in the team workbook

Q1 busy/quiet figures · Q2 distance/fee · Q3 cancel window · Q4 payment options · Q5 report definitions (all from Part 1).

Q1–Q5 exhaust the five-question client allowance. Answered and closed questions continue to count (workbook `Client Q&A!C16` counts Submitted + Answered + Closed; `Instructions!B13` = 5). A further submitted client question requires the lecturer to increase or explicitly waive the limit. Course clarifications (L1–L6) remain separately labelled; their separate treatment is not proof of an unrestricted additional client allowance.

### 1.3 Replan checkpoint (31/10)

Checkpoint entry: ⟦PENDING: answers and replan assessment, due 31/10⟧.

On 31/10 write one entry in `docs/part2/decision_log.md`: each L/Q item = answered (date, text) or unanswered. For each change: affected rules (BR-xx), models, schema, screens, tests, and new dates. A change to scope, money meaning or roster is a replan, not a constant edit.

---

## Client answer status at Phase 1

| ID | Status in frozen workbook | Submitted date | Answer |
|---|---|---|---|
| Q1 | Submitted | ⟦PENDING: original submission date, Dat to confirm by 31/10⟧ | no answer yet |
| Q2 | Submitted | ⟦PENDING: original submission date, Dat to confirm by 31/10⟧ | no answer yet |
| Q3 | Submitted | ⟦PENDING: original submission date, Dat to confirm by 31/10⟧ | no answer yet |
| Q4 | Submitted | ⟦PENDING: original submission date, Dat to confirm by 31/10⟧ | no answer yet |
| Q5 | Submitted | ⟦PENDING: original submission date, Dat to confirm by 31/10⟧ | no answer yet |

## Accepted plan changes J1–J9

| ID | Earlier position | Locked decision | Reason |
|---|---|---|---|
| J1 | SUC-03/05/06/07 "coordination owner" 523K0050, SUC-09 523K0049 | SUC owner column removed. Each SUC records its **actual author** (currently Dat). | Naming members who did not do the work is the fake authorship both plans forbid. |
| J2 | State-machine authors fixed: Order 722I0004, Delivery 523K0049, MenuItem 523K0050 | **Dat authors all state machines and all other artifacts** (Dat's decision 23/10); every caption shows 722I0004. Checklist 17 and 39 are recorded as facts: met for 722I0004, not met for the two other members (row status Partial with the reason). | Only real work can meet a per-student item; Partial records the shortfall, it does not satisfy it. |
| J3 | Phases P0–P7 | P0–P8 (P8 = presentation 16/11 and Part 3 handoff); my slices S0–S9 kept as P4 subphases. | User asked to keep phases, subphases and checklists. |
| J4 | Migration: "choose fresh v2 or real v1 migration" | **Fresh v2.** Part 2 starts from a fresh v2 database because the team treats the I1 synthetic demo data as disposable and does not need its orders to continue. The I1 source, submitted package, fixtures and test evidence are preserved (tag `i1-evidence`). No existing I1 database is deleted as part of this decision without checking its contents first. The runner refuses `user_version` < 2 with a clear message; the first real migration file is written only if the schema changes after the VM goes live, and is tested on a copy. | Closes the decision without claiming that no data exists. |
| J5 | Hostname/TLS "to resolve" | Caddy + `<VM-IP>.sslip.io` hostname (Let's Encrypt); fallback DuckDNS subdomain; last fallback local Docker demo. | No domain purchase needed. |
| J6 | "Do not assume Q1–Q5 + L1–L6 are ten client questions" | Q1–Q5 are the 5 client questions (limit 5, team workbook `Instructions!B13`). L1–L6 are course clarifications, kept on a separate list, never in the Client Q&A sheet. | Matches the workbook. |
| J7 | Not mentioned | Part 1 assumption **A-08** ("supporting UCs analysed, not built; CRUD by analysis + seed") is **superseded** by D-4. Record the change in the Assumption Log and in report 1.1 approval record. | Part 2 must show feedback/changes applied, not silently contradict Part 1. |
| J8 | Part 1 not in P0 | P0.0 records the Part 1 submission (done by Dat before 23/10) and the 26/10 live presentation. | Part 1 is frozen; Part 2 never edits the submitted package. |
| J9 | Schedule leaves the current draft uncommitted | P0.2 commits the draft on branch `part2` as a WIP baseline before any change. | Preserves work and starts real commit history. |

## Phase 1 interpretations

- A-08 is Superseded by D-4 (23/10, team decision), never lecturer approval.
- Checklist identifiers 11/12/13/41 are values in marking Checklist column B, at Excel rows 24/25/26/56. Literal rows 11/12/13/41 do not describe the requested four items.
- The template heading I. Business Requirements (1 point) is retained verbatim; the requirements PDF and marking rubric allocate 5 marks. No score is claimed.
- The plan P1.2 future test linkage is completed in P2–P4; Phase 1 test/result cells remain blank per its checklist.
