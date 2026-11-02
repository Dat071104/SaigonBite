**Glossary of terms and codes**

Author: 722I0004 · AI-assisted (Codex, Claude)

| Term or code | Meaning in this report |
|---|---|
| UC-01 … UC-06 | The six main use cases, two per student (2.1.5). |
| SUC-01 … SUC-09 | Supporting use cases that complete login, profile, tracking, cancellation, preparation, availability, vouchers, accounts and order archive (built under decision D-4). |
| FR-xx / NFR-xx | Functional / non-functional requirement (1.7). |
| BR-xx | Business rule, for example BR-09 "total T = S − D + F − Q". |
| PC / MG | Postcondition (what is true after the use case succeeds) / minimum guarantee (what stays true when it fails or is refused). IDs such as UC01-PC03 or UC05-MG01 are used by the state machines and the test cases. |
| OP-xx | A system operation, i.e. one SSD message, such as OP-01 `confirmCheckout`. |
| S, D, F, Q, T, C | Item subtotal, voucher discount, delivery fee, quiet-hub fee discount, order total, captured online amount. |
| A-xx | An entry in the Assumption Log (1.4.2). |
| Q1–Q5 | The five written questions submitted to the client (1.4.2). |
| L1–L6 | Course clarifications raised with the lecturer (1.4.2). |
| D-xx | A recorded team decision, for example D-4 "supporting use cases get running CRUD paths". |
| R-xx | A project risk (1.3). |
| P0–P8, G0–G7 | The phases of the Part 2 plan and the gate that closed each phase (1.3, "Actual progress"). |
| C0 | The first design commit (45ac762, 24/10/2026). Design tables compare this design with the code. |
| Matches code | The design element exists in the code with exactly the signature shown. |
| † | An element whose behaviour was completed during implementation; Table P4-1 gives the reason and the tests. |
| F-01 … F-09 | Defects found in the Iteration 1 draft and fixed in Part 2, for example F-04 "radius checked on a rounded distance" and F-07 "consent compared only the total". |
| P2-Sxx / P3-Sxx | Findings of the analysis (P2) and design (P3) reviews that the implementation had to satisfy, for example P2-S13 "transactions roll back on any failure" and P3-S03 "guarded updates check the affected row count". |
| Table P4-1 | The 121-row register (Appendix) that records how every design element was implemented and which tests prove it. |
| DCD / SSD / CRC | Design class diagram / system sequence diagram / class-responsibility-collaboration card. |
| DAO | Data access object: the only layer that runs SQL. |
| COD | Cash on delivery. |
| WAL, BEGIN IMMEDIATE | SQLite write-ahead logging, and the transaction mode that takes the write lock at once so two writers cannot interleave. |
