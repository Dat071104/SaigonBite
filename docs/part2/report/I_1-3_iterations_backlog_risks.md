# 1.3 Iteration Plan, User Story Backlog and Risks

Author: 722I0004 · AI-assisted (Codex)

The iteration dates below retain the six windows in the Part 1 roadmap. The locked Part 2 plan adds phase work and release gates over those windows. Dates and bars are planned; estimates are not measured results. The official Part 2 eLearning deadline is pending confirmation when the slot opens.

## Six-Iteration Plan

| Iteration | Planned dates | Goal and UC/SUC focus | Planned deliverables and exit evidence |
|---|---|---|---|
| I1 | 17–22/10/2026 | Persist one COD order on a runnable base. UC-01 subset and initial login support. | Vision, initial UC-01 analysis, activity/SSD/state artifacts, schema, seed, data access and checkout slice. Local Git records changes dated 19–20/10; this section does not assert that every I1 acceptance criterion passed. |
| I2 | 27–31/10/2026 | Hub CRUD/capacity and the kitchen decision/queue path. UC-03, UC-05, UC-01 capacity check; analyse UC-02 and UC-06; SUC-01, SUC-05. | Draft Report I and G1 by 29/10; UC-03/UC-05 analysis and tests; hub state model; UC-02/UC-06 analysis; P4.1 foundation work and local Docker path. Ask L1–L6 at the 26/10 presentation and review answers at the 31/10 checkpoint. |
| I3 | 01–05/11/2026 | Complete ordering, delivery and menu management. UC-01, UC-02, UC-06; UC-05 replacement; SUC-02–04, SUC-06–07. | Full quote and payment choices, tourist registration path, voucher and distance rules, shipper outcome path, catalogue/listing work, designs and tests. P3/P4 work overlaps this window under the phase schedule. |
| I4 | 06–10/11/2026 | Reports, integrated use cases and Figma evidence. UC-04 plus all six UCs; SUC-03, SUC-08–09. | Hand-calculated report oracle before report implementation; cross-role integration evidence; Figma progression; remaining P4 tests and P6 backup/restore or deployed-path evidence as scheduled. |
| I5 | 11–15/11/2026 | Final models, regression, deployment instructions and Part 2 report. All six UCs and nine SUCs. | Feature freeze 12/11; buffer on 13/11 for real defects only; PDF/package QA 14/11; Part 2 submission target 15/11. The official eLearning deadline must still be checked. |
| I6 | 17–29/11/2026 | Address Part 2 feedback, make the final release and prepare Part 3. All six UCs. | Feedback fixes, planned v1.0-final release, Part 3 material and submission target 29/11. This iteration follows the Part 2 presentation and submission. |

Backlog linkage: I1 contains early COD and login slices of BL-03 and BL-04; I2 focuses on BL-04–07, BL-09 and BL-19–20; I3 on BL-01–03, BL-07–08, BL-10–14 and BL-18–20; I4 on BL-08 and BL-15–20; I5 closes the BL-19–20 verification and recovery gates with the full release. I6 is post-Part-2 feedback and Part 3 follow-up, not a separate Part 2 Must item.

## Changes from the Part 1 Proposal

| Topic | Part 1 proposal | Locked Part 2 plan |
|---|---|---|
| Supporting use cases and CRUD | A-08 treated several supporting paths as analysis-only or seed-backed. | D-4 supersedes A-08: persistent classes need minimal running create/read/update/archive paths through supporting use cases. The current backlog includes all nine SUCs. |
| Clarification timing | Proposal expected lecturer questions to shape later iterations. | D-3 says to proceed with conservative defaults, ask L1–L6 at the 26/10 presentation, and record answers or no answer at the 31/10 checkpoint. Q1–Q5 remain the five client questions. |
| Part 2 delivery gates | The proposal placed final work and submission in I5 and already named the 12/11 freeze, 13/11 buffer and 15/11 target. | D-10 / plan §8 retain those gates, add 14/11 PDF/package QA and state that the official eLearning deadline must still be checked. |
| Deployment route | The Part 1 draft included a Vercel demo. | D-5 retires Vercel for Part 2 and plans one GCP VM, with local Docker Compose as the reproducible path and fallback. No cloud resource or deployment outcome is claimed here. |
| Authorship record | Proposal ownership separated six main UCs among three students. | D-1 retains those ownership labels but records 722I0004 as actual author of Part 2 artifacts. Ownership is not evidence of another member's Part 2 work. |
| I6 | A post-submission iteration for feedback and Part 3 was already planned. | The role remains post-Part-2: feedback fixes, final release and Part 3 work. |

The report uses BL-01–BL-20 as stable row IDs for this current backlog. The proposal's US-01–US-22 IDs are not silently reassigned because the scope of some proposal stories changed under D-4.

## Prioritised User Story Backlog

MoSCoW reflects the locked release scope. The six main UCs, nine SUCs and release-wide verification/recovery work are Must items. The listed Won't items remain deferred or future scope; they are not presented as lecturer-approved exclusions.

| ID | User story | MoSCoW | Iteration | UC/SUC link |
|---|---|---|---|---|
| BL-01 | As a customer, I want to register for a local or tourist account and maintain my profile and addresses so that I can place an order using my customer details. | Must | I3 | SUC-02, UC-01 |
| BL-02 | As a customer, I want to browse active hubs, brands and available items so that I can choose what and where to order. | Must | I3 | UC-01, UC-06 |
| BL-03 | As a customer, I want to review the complete quote, voucher and payment choice before confirming so that I can make an informed order decision. | Must | I3 | UC-01, SUC-07 |
| BL-04 | As a user, I want to log in and log out with role-appropriate access so that each task is performed by an authorised account. | Must | I1–I5 | SUC-01 |
| BL-05 | As an administrator, I want to create, read, update and archive hubs and maintain capacity so that current hub operations are represented. | Must | I2 | UC-03 |
| BL-06 | As a customer, I want a full hub to refuse the order and present eligible quieter hubs so that I can choose another option before confirming. | Must | I2 | UC-01, UC-03 |
| BL-07 | As kitchen staff, I want to confirm or reject an incoming order, or offer a valid replacement, so that I can handle an order against current stock. | Must | I2–I3 | UC-05 |
| BL-08 | As a customer, I want to track my order, view its receipt and answer an open replacement offer so that I can see and decide the order outcome. | Must | I3 | SUC-03, UC-01, UC-05 |
| BL-09 | As kitchen staff, I want to start preparation and mark an order READY so that a shipper can take a prepared order. | Must | I2 | SUC-05, UC-05, UC-02 |
| BL-10 | As kitchen staff, I want to change availability for items at my hub so that new orders use the current listing. | Must | I3 | SUC-06, UC-06 |
| BL-11 | As a shipper, I want to take a ready order and record delivery, exact COD cash or a failed outcome so that fulfilment is traceable per order. | Must | I3 | UC-02 |
| BL-12 | As an administrator, I want to maintain brands, menu items and hub listings so that customers see the catalogue used by the kitchens. | Must | I3 | UC-06 |
| BL-13 | As an administrator, I want to create, update and archive vouchers so that eligible customers can use the configured discount rules. | Must | I3 | SUC-07, UC-01 |
| BL-14 | As a customer, I want to cancel my own order while it is PLACED or CONFIRMED so that an early cancellation follows the defined payment rules. | Must | I3 | SUC-04, UC-01 |
| BL-15 | As an administrator, I want to create accounts and deactivate or reactivate them so that access can be maintained. | Must | I4 | SUC-08, SUC-01 |
| BL-16 | As an administrator, I want to archive closed orders and read their history so that operational lists stay current while authorised history remains available. | Must | I4 | SUC-09 |
| BL-17 | As a manager, I want reports for sales, hub workload and delivery performance so that I can compare operations using shared definitions. | Must | I4 | UC-04 |
| BL-18 | As a customer, I want rejection, cancellation, replacement and delivery-failure outcomes to show the correct payment state and amount owed so that I know what remains due. | Must | I3–I4 | UC-01, UC-02, UC-05, SUC-03–04 |
| BL-19 | As a reviewer, I want postcondition, boundary, role and concurrency tests for each main use case so that release claims have recorded evidence. | Must | I2–I5 | UC-01–UC-06, SUC-01–SUC-09 |
| BL-20 | As a reviewer, I want a fresh local run path and documented backup/restore steps so that the planned release can be run and recovered reproducibly. | Must | I2–I5 | Release-wide |
| W-01 | Complaint handling and refund decisions, refund payout, and customer rating. These remain deferred under A-09 / L3; the L3 answer is pending. | Won't this release | — | A-09, L3 |
| W-02 | Loyalty points, subscription meals, group orders and scheduled orders. The case study lists these as future features. | Won't this release | — | Case study future scope; no A-ID was assigned |
| W-03 | Menu translation for tourists. Part 1 §1.3 explicitly leaves translation outside this release. | Won't this release | — | Part 1 §1.3; no A-ID was assigned |

## Risks

Likelihood and impact are qualitative planning judgments, not measured frequencies. IDs R-06–R-11 continue the proposal's R-01–R-05 numbering without changing the earlier risk meanings. Dat 722I0004 is the recorded owner because D-1 assigns actual Part 2 authorship to Dat; this does not claim work by another member.

| ID | Risk | Likelihood | Impact | Owner | Trigger | Mitigation |
|---|---|---|---|---|---|---|
| R-06 | Sole-author delivery and contribution-factor exposure: one person carries the Part 2 artifact workload, while the course marks contribution by actual evidence. | High | High | Dat 722I0004 | Required section, test or release evidence slips beyond the plan, or contribution records cannot substantiate what each person actually authored. | Track planned deliverables and actual evidence; preserve prompts, authored artifacts and commit history; record contribution facts accurately and mark unmet per-student items Partial. Review scope and hours at the 31/10 checkpoint. |
| R-07 | AI-policy clarification L6 may conflict with planned AI-assisted code or artifact work. | Medium | High | Dat 722I0004 | L6 answer does not permit the declared AI-assisted approach. | Declare each AI use, retain prompts/outputs and verification notes, ask L6 at the 26/10 presentation, and stop or replan the affected work if the answer requires it. |
| R-08 | SQLite lock contention or racing transitions may cause concurrent ordering/delivery requests to fail or miss response-time targets. | Medium | High | Dat 722I0004 | P4 lock, last-capacity-slot or shipper race checks fail, or a controlled database-locked case is unclear. | Keep writes within the planned transaction boundary, use the planned timeout/locking controls, and run the specified contention, race and rollback checks before calling the path ready. |
| R-09 | School-account organisation policy, static IP or TLS constraints may prevent the planned cloud demonstration. | Medium | High | Dat 722I0004 | Compute Engine, an external IP or certificate issuance is unavailable during the first-deploy window. | Check account/org restrictions before provisioning; follow the D-7 hostname fallback order if needed; keep local Docker Compose as the reproducible demo path and record any cloud limitation. |
| R-10 | Lecturer clarification L1 or L3 may change CRUD or deferred-feature scope. | Medium | High | Dat 722I0004 | The 26/10 answer contradicts D-4 or requires complaint/refund/rating work now deferred. | Proceed with conservative defaults, record actual answers or no answer by 31/10, assess effects on BRs, models, schema, screens, tests and dates, then replan explicitly. Do not record silence as approval. |
| R-11 | The remaining schedule may exceed the available focused time. | Medium | High | Dat 722I0004 | At the 31/10 checkpoint, recorded hours and remaining scope project beyond the 7 h/day budget. | Compare actual hours with the plan estimate. The plan budgets about 154 hours against an estimated 92–130 hours, leaving about 24 hours of estimated reserve; apply plan §9 cuts in order if forecasts exceed the remaining budget, while protecting the six UCs, truthful authorship, data safety and reproducible demo. |
