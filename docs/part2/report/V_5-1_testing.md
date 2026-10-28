# 5.1 Testing: Test Plan and Test Cases

Author: 722I0004 · AI-assisted (Codex)

The test plan checks postconditions at three levels: automated unit and postcondition tests on a local database, browser integration across roles, and checks against the deployed VM. Entry requires the intended revision, a fresh or isolated database where applicable, and available test tools. Exit for the automated run requires the recorded suite to complete without failures; the browser and deployed checks require their own recorded steps. A passing suite alone does not establish that every workflow was demonstrated.

At `252ada1`, the 27 October 2026 local JUnit report records 928 passing test cases. The P5 local browser walkthrough records 60 of 60 passing steps, and the adapted P6 deployed scenarios record 22 of 22 passing steps; their environments and limitations are described in 4.3.6 and 5.2. The P7 entry rerun at `97574bd` recorded 928 passing tests on 28 October.

The table maps every one of the 30 main-use-case postconditions and minimal guarantees to its recorded test nodes. The actual result is a passing node in the JUnit report; the assertions linked in the coverage register qualify the check. The full node list and reconciliation are in `docs/part2/test_report/p7_2026-10-28/test_cases.csv`.

| Test ID | Use case | Post-condition tested | Input / steps | Expected result | Actual result | Pass / fail |
|---|---|---|---|---|---|---|
| UC01-PC01 | UC-01 | one PLACED order owned by the customer | Execute the named test node(s), with their recorded fixtures. | one PLACED order owned by the customer | All named nodes passed | PASS |
| UC01-PC02 | UC-01 | lines with snapshot names/prices | Execute the named test node(s), with their recorded fixtures. | lines with snapshot names/prices | All named nodes passed | PASS |
| UC01-PC03 | UC-01 | address snapshot + distance | Execute the named test node(s), with their recorded fixtures. | address snapshot + distance | All named nodes passed | PASS |
| UC01-PC04 | UC-01 | S/D/F/Q/T stored and consistent | Execute the named test node(s), with their recorded fixtures. | S/D/F/Q/T stored and consistent | All named nodes passed | PASS |
| UC01-PC05 | UC-01 | payment PENDING (COD) or PAID (ONLINE, amount C) | Execute the named test node(s), with their recorded fixtures. | payment PENDING (COD) or PAID (ONLINE, amount C) | All named nodes passed | PASS |
| UC01-PC06 | UC-01 | hub load +1 | Execute the named test node(s), with their recorded fixtures. | hub load +1 | All named nodes passed | PASS |
| UC01-MG01 | UC-01 | refused/declined/invalid → no order, no payment, no line | Execute the named test node(s), with their recorded fixtures. | Invariant / refusal outcome: refused/declined/invalid → no order, no payment, no line | All named nodes passed | PASS |
| UC01-MG02 | UC-01 | replay → same single order | Execute the named test node(s), with their recorded fixtures. | Invariant / refusal outcome: replay → same single order | All named nodes passed | PASS |
| UC01-MG03 | UC-01 | busy → suggestions, nothing saved | Execute the named test node(s), with their recorded fixtures. | Invariant / refusal outcome: busy → suggestions, nothing saved | All named nodes passed | PASS |
| UC02-PC01 | UC-02 | one shipper assigned, Delivery PICKED_UP, order OUT_FOR_DELIVERY | Execute the named test node(s), with their recorded fixtures. | one shipper assigned, Delivery PICKED_UP, order OUT_FOR_DELIVERY | All named nodes passed | PASS |
| UC02-PC02 | UC-02 | delivered: Delivery DELIVERED, order DELIVERED, COD PAID with cash = T | Execute the named test node(s), with their recorded fixtures. | delivered: Delivery DELIVERED, order DELIVERED, COD PAID with cash = T | All named nodes passed | PASS |
| UC02-PC03 | UC-02 | failed: Delivery FAILED + reason, order DELIVERY_FAILED, BR-17 | Execute the named test node(s), with their recorded fixtures. | failed: Delivery FAILED + reason, order DELIVERY_FAILED, BR-17 | All named nodes passed | PASS |
| UC02-MG01 | UC-02 | second shipper / wrong shipper / wrong cash / repeat → 0 rows changed | Execute the named test node(s), with their recorded fixtures. | Invariant / refusal outcome: second shipper / wrong shipper / wrong cash / repeat → 0 rows changed | All named nodes passed | PASS |
| UC03-PC01 | UC-03 | hub created/updated with valid code, coordinates, fee, capacity | Execute the named test node(s), with their recorded fixtures. | hub created/updated with valid code, coordinates, fee, capacity | All named nodes passed | PASS |
| UC03-PC02 | UC-03 | archived hub hidden from browse/checkout, visible in history/reports | Execute the named test node(s), with their recorded fixtures. | archived hub hidden from browse/checkout, visible in history/reports | All named nodes passed | PASS |
| UC03-MG01 | UC-03 | duplicate code / capacity < 1 / archive with open order → nothing changed | Execute the named test node(s), with their recorded fixtures. | Invariant / refusal outcome: duplicate code / capacity < 1 / archive with open order → nothing changed | All named nodes passed | PASS |
| UC04-PC01 | UC-04 | sales, workload, performance equal the hand oracle for the filter | Execute the named test node(s), with their recorded fixtures. | sales, workload, performance equal the hand oracle for the filter | All named nodes passed | PASS |
| UC04-PC02 | UC-04 | n/a on empty denominators | Execute the named test node(s), with their recorded fixtures. | n/a on empty denominators | All named nodes passed | PASS |
| UC04-MG01 | UC-04 | 0 rows written by any report request | Execute the named test node(s), with their recorded fixtures. | Invariant / refusal outcome: 0 rows written by any report request | All named nodes passed | PASS |
| UC04-MG02 | UC-04 | non-manager denied | Execute the named test node(s), with their recorded fixtures. | Invariant / refusal outcome: non-manager denied | All named nodes passed | PASS |
| UC05-PC01 | UC-05 | confirm: own-hub PLACED → CONFIRMED | Execute the named test node(s), with their recorded fixtures. | confirm: own-hub PLACED → CONFIRMED | All named nodes passed | PASS |
| UC05-PC02 | UC-05 | reject: REJECTED + reason + BR-17 + offer WITHDRAWN | Execute the named test node(s), with their recorded fixtures. | reject: REJECTED + reason + BR-17 + offer WITHDRAWN | All named nodes passed | PASS |
| UC05-PC03 | UC-05 | offer: one OFFERED offer per §3.3 | Execute the named test node(s), with their recorded fixtures. | offer: one OFFERED offer per §3.3 | All named nodes passed | PASS |
| UC05-PC04 | UC-05 | accepted offer applied per §3.3 5–7 | Execute the named test node(s), with their recorded fixtures. | accepted offer applied per §3.3 5–7 | All named nodes passed | PASS |
| UC05-MG01 | UC-05 | wrong hub / open offer / stale / invalid target → order unchanged | Execute the named test node(s), with their recorded fixtures. | Invariant / refusal outcome: wrong hub / open offer / stale / invalid target → order unchanged | All named nodes passed | PASS |
| UC06-PC01 | UC-06 | brand/item created, updated, archived | Execute the named test node(s), with their recorded fixtures. | brand/item created, updated, archived | All named nodes passed | PASS |
| UC06-PC02 | UC-06 | listing added/removed, availability per hub | Execute the named test node(s), with their recorded fixtures. | listing added/removed, availability per hub | All named nodes passed | PASS |
| UC06-PC03 | UC-06 | archived/sold-out items not orderable | Execute the named test node(s), with their recorded fixtures. | archived/sold-out items not orderable | All named nodes passed | PASS |
| UC06-MG01 | UC-06 | old order lines unchanged after price change/archive | Execute the named test node(s), with their recorded fixtures. | Invariant / refusal outcome: old order lines unchanged after price change/archive | All named nodes passed | PASS |
| UC06-MG02 | UC-06 | duplicates/invalid prices refused | Execute the named test node(s), with their recorded fixtures. | Invariant / refusal outcome: duplicates/invalid prices refused | All named nodes passed | PASS |

For all rows: local pytest, 27 October 2026, commit `252ada1`. See the CSV for the individual named test nodes and evidence paths.

Sources: `pc_mg_register.csv`; `implementation/p4_test_coverage.csv`; `test_report/2026-10-27_252ada1.xml`; P5 and P6 integration evidence.
