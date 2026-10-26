# S7 Manager reports against the hand-calculated oracle; archiving a closed order

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Written before the run. Figures come from `tests/fixtures/report_oracle_expected.md` (hand arithmetic, written before any report query ran), not from the app.

Part A runs on a separate oracle database (`init_db.build_database(path)` without demo history, then `tests/fixtures/report_oracle.sql`, server on port 5101). Oracle day: 20/10/2026 (From = To = 2026-10-20). Hub 1 is "SaigonBite District 1 Hub", hub 2 is "SaigonBite Binh Thanh Hub" (archived in the fixture).

| Step | Profile | Action | Expected | Rules |
|---|---|---|---|---|
| 7.1 | manager | Sales, From 2026-10-20, To 2026-10-20, All hubs, Show | table rows: District 1: 1 order, 90,000 VND dishes, -10,000 VND vouchers, 10,000 VND delivery fees, 90,000 VND total, 10,000 VND refunds owed, 90,000 VND net. Binh Thanh: 1, 60,000, 0 (no minus sign for zero), 10,000, 70,000, 0, 70,000 VND. All hubs: 2, 150,000, -10,000, 10,000+10,000 = 20,000, 160,000, 10,000, 160,000 VND. Best-selling: "Renamed snapshot" quantity 3 revenue 100,000 VND; "Shared name" quantity 1 revenue 50,000 VND | BR-21, BR-24 |
| 7.2 | manager | same period, Hub = Binh Thanh | 1 order, total 70,000 VND, refunds owed 0, net 70,000 VND (the archived hub keeps its identity) | BR-21 |
| 7.3 | manager | Delivery performance, same period, All hubs | overall: delivered 2, failed 1, failure rate 33.3%, average wait "20.0 min (n=3)", average ride "25.0 min (n=2)". By hub: District 1: 1, 0, 0.0%, 10.0 min (n=1), 20.0 min (n=1); Binh Thanh: 1, 1, 50.0%, 25.0 min (n=2), 30.0 min (n=1). By shipper: one row (Shipper One) with the overall figures | BR-23 |
| 7.4 | manager | Workload | both hubs appear: District 1 with New 0, Confirmed 0, Preparing 0 and "0 / 12"; Binh Thanh (marked Archived) with New 1 and "1 / 8" | BR-22 |
| 7.5 | manager | Sales and Delivery for the empty day 2026-01-01 | Sales: "No delivered orders in this period." and the All hubs row 0 orders, 0 VND everywhere; Delivery: failure rate "n/a", wait "n/a (n=0)", ride "n/a (n=0)" | BR-21, BR-23 |

Part B runs back on the main database (port 5100, after S6):

| Step | Profile | Action | Expected | Rules |
|---|---|---|---|---|
| 7.6 | manager | Sales, From 2026-10-01, To 2026-10-27, All hubs: note the table text | (reference text for 7.8) | |
| 7.7 | admin | Archive orders: Closed order ID 1 (DELIVERED), "Archive this order" | banner "The closed order is archived. Its history and reports are kept."; the "Recently archived" table lists order 1 as Delivered; the history page of order 1 opens | BR-24 |
| 7.8 | customer | open /order/1/receipt; manager repeats 7.6 | the receipt opens ("Receipt · Order 1", Total T 130,000 VND); the Sales table text is identical to 7.6 (archiving changes no total); the customer's My orders no longer lists Order 1 (archived orders leave the operational screens) | BR-13, BR-24 |
| 7.9 | admin | Closed order ID 9 (PLACED, open), "Archive this order" | banner "Only a closed, unarchived order can be archived."; order 9 stays unarchived | BR-24 |

Corroboration (read-only): oracle DB unchanged by the report screens (report queries never write); main DB order 1 has archived_at, order 9 has none.

Correction log (before any run): steps 7.1 and 7.5 first wrote the zero voucher cell as "-0 VND", copying what the draft template printed. A zero discount is "0 VND"; the minus sign belongs only to a real discount. Test-design error in the expectation (it encoded a display wart, not a rule); the template was corrected in commit dc87741 and the expectation corrected before the first run. First hash prefix was `69744e90f64e3b08`.
