# Integration evidence P5.2: seven scenarios and the CSRF check in the browser

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5).

**Result of the final run: 60 of 60 steps pass, 0 fail.** Label: **Demonstrated** (browser walkthrough with screenshots, one browser profile per role, the same order id followed across the roles). A database query after a step only corroborates it (`S<n>/db_facts.json`); it never replaces the browser evidence.

## Environment

- Commit under test: `252ada102510ffd1bca9d50288f7ea44e9ff9149` on branch `part2` (the last commit that changed runtime files; every later commit changes documentation only). Git status of tracked files was clean; untracked: the new evidence folders.
- Server: local Flask development server (python -m flask run), debug off, ports 5100 (main) and 5101 (oracle). The secret key is random and exists only in the server process environment.
- Browser: Microsoft Edge 156.0.4314.42 driven by Playwright for Python 1.64.1 (Python 3.14.4), installed in the isolated venv `Part2/notes/P5/tools/venv`; headless, one persistent profile per role (customer and tourist and both shippers at 390×844 with touch, kitchen, kitchen_bt, admin, manager at 1440×900).
- Databases (new files, created with `init_db.py`): main `D:\RAD\FINAL\Part2\notes\P5\db\main_t4.db` (schema, seed, demo history orders 1 to 8); oracle `D:\RAD\FINAL\Part2\notes\P5\db\oracle_t4.db` (schema and seed without demo history, then `tests/fixtures/report_oracle.sql`).
- Started 2026-10-27T01:22:48, finished 2026-10-27T01:23:01 (Asia/Bangkok). Script: `scripts/run_integration.py` (library `scripts/p5lib.py`); one run goes through S1 to S8 on one database so that state carries forward.

## How the expected results were kept honest

`S<n>/expected.md` was written first, with hand-computed amounts, and its SHA-256 and time were recorded in `Part2/notes/P5/progress.json` before any run (hashes below; the first recording was 27/10/2026 01:13:27, the times in the table are the re-recording after the two edits below, and the other six files were unchanged between the two). To verify: `git show HEAD:docs/part2/test_report/integration_2026-10-27/S1/expected.md | sha256sum` gives the hash in the table (the hashes are over the LF bytes of the committed blob; a CRLF checkout changes the bytes on disk). No expected value was adjusted to fit an actual result. Two edits before the first complete run are recorded in the open: S7 (the zero-voucher cell "-0 VND" became "0 VND" when the template was corrected, commit dc87741; logged inside the file) and S3 step 3.6 (a wrong edit of mine, reverted to the original bytes after the first runs showed the original was right; the first hash reproduces, history in `S3/expected_history.md`).

| Scenario | expected.md SHA-256 | recorded |
|---|---|---|
| S1 | `b6125bfea338a265f45f720e124b3df9fe3f9e52d54cfb15e6d8cddfafe64ecd` | 2026-10-27T01:21:42+07:00 |
| S2 | `653bdca8704933d8aff4fc6cb89e9247dd918228a38058ccd0bc8e292e52802c` | 2026-10-27T01:21:42+07:00 |
| S3 | `4c16fcd9d6be8cdf571ed943f89a9ec96689564bb8455853bee5cae70ad2a522` | 2026-10-27T01:21:42+07:00 |
| S4 | `06ea4e3fa809df17ea7d09f4d3516fe3ff0d405455d2d6f311a34e05ecf7c981` | 2026-10-27T01:21:42+07:00 |
| S5 | `d466c781aa2d6beea6fd829e5b53b35f6a18c68fe7b39fc4f867e2c7c17f65f0` | 2026-10-27T01:21:42+07:00 |
| S6 | `3626f89ca27435e29068534f30deb36787204628e2c2862f174daa0f501f0c73` | 2026-10-27T01:21:42+07:00 |
| S7 | `e989549aed227b804835a562d0106726c8b51fb032a844803b5cea942438e795` | 2026-10-27T01:21:42+07:00 |
| S8 | `4c9f37f9c23367b5c3ab06ff8554349fe65b10048d822719cc6bfdcaf2de173d` | 2026-10-27T01:21:42+07:00 |

## Run history (the whole sequence is repeated from a fresh database every time)

| Run | Result | Reason |
|---|---|---|
| t1, t2 | stopped | my own script: a screenshot label for a two-role step, a selector for the Ready column in step 4.5, the page-load hook; step 3.6 failed only because of the expectation edit described above |
| t3 | 58 of 60 | steps 8.2 and 8.3: my script altered the CSRF token of the logout form in the top bar instead of the hub form, so the hub really was saved (a script error, not an application defect) |
| **t4 (final)** | **60 of 60** | at commit `252ada1`; the evidence below is this run |

Before the final run the browser found defects P5-D01 to P5-D05 (below); each was fixed with a regression test and its scenarios were repeated from a fresh database.

## S1 Catalogue and capacity reach the customer; archived and sold-out dishes cannot be ordered

Expected written first: [`S1/expected.md`](S1/expected.md). Corroboration: [`S1/db_facts.json`](S1/db_facts.json).

| Step | Role | Expected | Actual (page text, shortened) | Result | Screenshot | Order |
|---|---|---|---|---|---|---|
| 1.1 | admin | HUB-D1 shows 1 / 12 Quiet; HUB-BT shows 0 / 8 Quiet | Hubs and kitchen capacity Load = orders still to cook (new, confirmed, preparing). A hub at its capacity takes no new orders; below a quarter of it, delivery is 5,000 VND cheaper. New hub Code Hub Lo… | PASS (5/5 checks) | [S1_1.1_admin.png](S1/S1_1.1_admin.png) |  |
| 1.2 | admin | banner 'The hub is saved.'; D1 row 1 / 14 | The hub is saved. Hubs and kitchen capacity Load = orders still to cook (new, confirmed, preparing). A hub at its capacity takes no new orders; below a quarter of it, delivery is 5,000 VND cheaper. N… | PASS (2/2 checks) | [S1_1.2_admin.png](S1/S1_1.2_admin.png) |  |
| 1.3 | admin | banner 'The dish is on the hub's menu.'; row Che thai Sweet Che House 30,000 VND Available | The dish is on the hub's menu. Menu of SaigonBite District 1 Hub The dishes this hub cooks. Kitchen staff can also mark a dish sold out for the day. Dish Brand Price Status Pho bo tai Pho Saigon Kitc… | PASS (5/5 checks) | [S1_1.3_admin.png](S1/S1_1.3_admin.png) |  |
| 1.4 | customer | Sweet Che House / Che thai 30,000 VND with a quantity field; Com tam ga nuong Sold out without a field | Kitchen Dishes Confirm Done SaigonBite District 1 Hub 45 Le Loi, Ben Nghe Ward, District 1, Ho Chi Minh City · delivery from 15,000 VND This kitchen is quiet: 5,000 VND off the delivery fee. Pho Saig… | PASS (7/7 checks) | [S1_1.4_customer.png](S1/S1_1.4_customer.png) |  |
| 1.5 | admin | banner 'The dish is archived. It can no longer be ordered.'; row shows Archived | The dish is archived. It can no longer be ordered. Brands and menu Archived brands and dishes can no longer be ordered. Orders already placed keep the name and price they had. Brands Brand Rename Pho… | PASS (2/2 checks) | [S1_1.5_admin.png](S1/S1_1.5_admin.png) |  |
| 1.6 | customer | Banh mi op la is not on the page | Kitchen Dishes Confirm Done SaigonBite District 1 Hub 45 Le Loi, Ben Nghe Ward, District 1, Ho Chi Minh City · delivery from 15,000 VND This kitchen is quiet: 5,000 VND off the delivery fee. Pho Saig… | PASS (2/2 checks) | [S1_1.6_customer.png](S1/S1_1.6_customer.png) |  |
| 1.7 | customer | HTTP 400 on the menu page, 'Item 5 is not available at SaigonBite District 1 Hub.', no quote | Kitchen Dishes Confirm Done SaigonBite District 1 Hub 45 Le Loi, Ben Nghe Ward, District 1, Ho Chi Minh City · delivery from 15,000 VND This kitchen is quiet: 5,000 VND off the delivery fee. Item 5 i… | PASS (3/3 checks) | [S1_1.7_customer.png](S1/S1_1.7_customer.png) |  |
| 1.8 | customer | HTTP 400 on the menu page, 'Item 8 is not available at SaigonBite District 1 Hub.', no quote | Kitchen Dishes Confirm Done SaigonBite District 1 Hub 45 Le Loi, Ben Nghe Ward, District 1, Ho Chi Minh City · delivery from 15,000 VND This kitchen is quiet: 5,000 VND off the delivery fee. Item 8 i… | PASS (3/3 checks) | [S1_1.8_customer.png](S1/S1_1.8_customer.png) |  |
| 1.9 | customer | quote 30,000 + 15,000 - 5,000 = 40,000; 'Order 9 is placed', 40,000 VND, PLACED | Kitchen Dishes Confirm Done Check your order Nothing is ordered until you press Confirm order. SaigonBite District 1 Hub Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City · 0.39 k… | PASS (7/7 checks) | [S1_1.9_customer.png](S1/S1_1.9_customer.png) | 9 |

## S2 A full hub refuses with a quieter-hub suggestion; the suggestion gives a fresh quote

Expected written first: [`S2/expected.md`](S2/expected.md). Corroboration: [`S2/db_facts.json`](S2/db_facts.json).

| Step | Role | Expected | Actual (page text, shortened) | Result | Screenshot | Order |
|---|---|---|---|---|---|---|
| 2.1 | admin | banner 'The hub is saved.'; BT row 0 / 1 | The hub is saved. Hubs and kitchen capacity Load = orders still to cook (new, confirmed, preparing). A hub at its capacity takes no new orders; below a quarter of it, delivery is 5,000 VND cheaper. N… | PASS (2/2 checks) | [S2_2.1_admin.png](S2/S2_2.1_admin.png) |  |
| 2.2 | customer | quote 60,000 + 25,000 - 5,000 = 80,000; 'Order 10 is placed' | Kitchen Dishes Confirm Done Check your order Nothing is ordered until you press Confirm order. SaigonBite Binh Thanh Hub Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City · 4.06 k… | PASS (6/6 checks) | [S2_2.2_customer.png](S2/S2_2.2_customer.png) | 10 |
| 2.3 | admin | BT shows 1 / 1 and Busy | HUB-BT SaigonBite Binh Thanh Hub 1 / 1 Busy 10,000 VND 1 Edit Menu | PASS (2/2 checks) | [S2_2.3_admin.png](S2/S2_2.3_admin.png) |  |
| 2.4 | tourist | HTTP 409; 'too busy' banner; suggestion D1 with 'Quiet: 5,000 VND off delivery'; BT card 'Busy now'; no quote | Kitchen Dishes Confirm Done Choose a kitchen hub Each hub cooks for several brands. The delivery fee is the hub's base fee plus 3,000 VND per started km, up to 8 km. SaigonBite Binh Thanh Hub is too … | PASS (7/7 checks) | [S2_2.4_tourist.png](S2/S2_2.4_tourist.png) |  |
| 2.5 | tourist | D1 quote: 55,000 + 15,000 - 5,000 = 65,000 | Kitchen Dishes Confirm Done Check your order Nothing is ordered until you press Confirm order. SaigonBite District 1 Hub Deliver to Rex Hotel, 141 Nguyen Hue, District 1, Ho Chi Minh City · 0.06 km a… | PASS (5/5 checks) | [S2_2.5_tourist.png](S2/S2_2.5_tourist.png) |  |
| 2.6 | tourist | still 10 orders and 10 payment rows; nothing from steps 2.4 and 2.5 | [{"id": 1, "customer_id": 1, "hub_id": 1, "state": "DELIVERED", "total_amount": 130000}, {"id": 2, "customer_id": 2, "hub_id": 1, "state": "DELIVERED", "total_amount": 132000}, {"id": 3, "customer_id… | PASS (2/2 checks) | [S2_2.6_tourist.png](S2/S2_2.6_tourist.png) |  |
| 2.7 | admin | banner 'The hub is saved.'; BT 1 / 8 | The hub is saved. Hubs and kitchen capacity Load = orders still to cook (new, confirmed, preparing). A hub at its capacity takes no new orders; below a quarter of it, delivery is 5,000 VND cheaper. N… | PASS (2/2 checks) | [S2_2.7_admin.png](S2/S2_2.7_admin.png) |  |

## S3 An order reaches the kitchen of its own hub only

Expected written first: [`S3/expected.md`](S3/expected.md). Corroboration: [`S3/db_facts.json`](S3/db_facts.json).

| Step | Role | Expected | Actual (page text, shortened) | Result | Screenshot | Order |
|---|---|---|---|---|---|---|
| 3.1 | customer | quote 100,000 + 15,000 - 5,000 = 110,000; 'Order 11 is placed' | Kitchen Dishes Confirm Done Check your order Nothing is ordered until you press Confirm order. SaigonBite District 1 Hub Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City · 0.39 k… | PASS (7/7 checks) | [S3_3.1_customer.png](S3/S3_3.1_customer.png) | 11 |
| 3.2 | kitchen | heading D1; card Order 11 in New with 2 x Pho ga and Confirm; New shows 3 | SaigonBite District 1 Hub Kitchen capacity 14 orders. New, confirmed and preparing orders count towards it. New 3 Order 8 10:10, 23/10/2026 1 x Goi cuon Confirm Reject or replace Order 9 01:22, 27/10… | PASS (5/5 checks) | [S3_3.2_kitchen.png](S3/S3_3.2_kitchen.png) | 11 |
| 3.3 | kitchen_bt | heading BT; card Order 10; no Order 11 | SaigonBite Binh Thanh Hub Kitchen capacity 8 orders. New, confirmed and preparing orders count towards it. New 1 Order 10 01:22, 27/10/2026 1 x Com tam suon bi cha Confirm Reject or replace Confirmed… | PASS (4/4 checks) | [S3_3.3_kitchen_bt.png](S3/S3_3.3_kitchen_bt.png) |  |
| 3.4 | kitchen_bt | HTTP 403 Not allowed, 'This order belongs to another hub.' | Not allowed Error 403 This order belongs to another hub. Back to kitchen board | PASS (3/3 checks) | [S3_3.4_kitchen_bt.png](S3/S3_3.4_kitchen_bt.png) | 11 |
| 3.5 | kitchen_bt | HTTP 403, 'This order belongs to another hub.'; order 11 stays PLACED, confirmed_at empty | Not allowed Error 403 This order belongs to another hub. Back to kitchen board | PASS (4/4 checks) | [S3_3.5_kitchen_bt.png](S3/S3_3.5_kitchen_bt.png) | 11 |
| 3.6 | kitchen | 2 x Pho ga, Total 110,000, Placed, Confirm order and Reject order buttons and the Offer a replacement section | Order 11 Placed 01:22, 27/10/2026 · Placed · COD Dish Unit price Qty Amount Pho ga 50,000 VND 2 100,000 VND Dishes 100,000 VND Delivery fee (0.39 km) 15,000 VND Quiet hub discount -5,000 VND Total 11… | PASS (6/6 checks) | [S3_3.6_kitchen.png](S3/S3_3.6_kitchen.png) | 11 |

## S4 Sold-out dish, cheaper replacement, customer accepts, kitchen cooks, one delivery

Expected written first: [`S4/expected.md`](S4/expected.md). Corroboration: [`S4/db_facts.json`](S4/db_facts.json).

| Step | Role | Expected | Actual (page text, shortened) | Result | Screenshot | Order |
|---|---|---|---|---|---|---|
| 4.1 | kitchen | banner 'Availability updated.'; Pho ga Sold out with 'Available again' | Availability updated. Dishes at SaigonBite District 1 Hub Mark a dish sold out when an ingredient runs out; customers can no longer add it. Dish Brand Status Pho bo tai Pho Saigon Kitchen Available M… | PASS (3/3 checks) | [S4_4.1_kitchen.png](S4/S4_4.1_kitchen.png) |  |
| 4.2 | kitchen | banner 'The replacement is offered...'; 'Replacement offered: Pho ga → Goi cuon'; no Confirm button | The replacement is offered. The order waits for the customer's answer. Order 11 Placed 01:22, 27/10/2026 · Placed · COD Dish Unit price Qty Amount Pho ga 50,000 VND 2 100,000 VND Dishes 100,000 VND D… | PASS (4/4 checks) | [S4_4.2_kitchen.png](S4/S4_4.2_kitchen.png) | 11 |
| 4.3 | customer | 'Your answer needed'; panel: Pho ga has run out... Goi cuon at 35,000 VND instead of 50,000 VND; new total 80,000 VND (now 110,000 VND) | Order 11 SaigonBite District 1 Hub · placed 01:22, 27/10/2026 The kitchen asks about a replacement Pho ga has run out. The kitchen offers Goi cuon at 35,000 VND instead of 50,000 VND. If you accept, … | PASS (4/4 checks) | [S4_4.3_customer.png](S4/S4_4.3_customer.png) | 11 |
| 4.4 | customer | banner 'Replacement accepted...'; Goi cuon 2 x 35,000 = 70,000; Total 80,000; panel gone | Replacement accepted. The kitchen may now confirm your order. Order 11 SaigonBite District 1 Hub · placed 01:22, 27/10/2026 Status Placed Payment COD, pending Deliver to 12 Nguyen Hue, Ben Nghe Ward,… | PASS (5/5 checks) | [S4_4.4_customer.png](S4/S4_4.4_customer.png) | 11 |
| 4.5 | kitchen | three banners; Order 11 under Ready for pickup | Order 11 is confirmed. SaigonBite District 1 Hub Kitchen capacity 14 orders. New, confirmed and preparing orders count towards it. New 2 Order 8 10:10, 23/10/2026 1 x Goi cuon Confirm Reject or repla… | PASS (4/4 checks) | [S4_4.5_kitchen.png](S4/S4_4.5_kitchen.png) | 11 |
| 4.6 | customer | Status Ready | Order 11 SaigonBite District 1 Hub · placed 01:22, 27/10/2026 Status Ready Payment COD, pending Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City Confirmed 01:22, 27/10/2026 Ready… | PASS (1/1 checks) | [S4_4.6_customer.png](S4/S4_4.6_customer.png) | 11 |
| 4.7 | kitchen | banner 'Availability updated.'; Pho ga Available | Availability updated. Dishes at SaigonBite District 1 Hub Mark a dish sold out when an ingredient runs out; customers can no longer add it. Dish Brand Status Pho bo tai Pho Saigon Kitchen Available M… | PASS (2/2 checks) | [S4_4.7_kitchen.png](S4/S4_4.7_kitchen.png) |  |

## S5 Two shippers take the same order together; exact cash; customer sees delivered and paid

Expected written first: [`S5/expected.md`](S5/expected.md). Corroboration: [`S5/db_facts.json`](S5/db_facts.json).

| Step | Role | Expected | Actual (page text, shortened) | Result | Screenshot | Order |
|---|---|---|---|---|---|---|
| 5.1 | shipper | Order 11 under Ready for pickup with 'Cash on delivery: 80,000 VND'; also Order 7 (65,000 VND) | Deliveries On my bike Nothing picked up. Ready for pickup Order 7 ready since 10:15, 23/10/2026 SaigonBite District 1 Hub → 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City (0.39 km) Cash o… | PASS (3/3 checks) | [S5_5.1_shipper.png](S5/S5_5.1_shipper.png)<br>[S5_5.1_shipper2.png](S5/S5_5.1_shipper2.png) | 11 |
| 5.2 | shipper+shipper2 | exactly one winner 'You picked up order 11.' + Picked up; the other 'Order 11 has already been picked up. Nothing was changed.' and 'Back to deliveries' | winner=shipper: You picked up order 11. Order 11 Picked up · from SaigonBite District 1 Hub Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City (0.39 km) Customer Tran Thi Mai · 090… | PASS (5/5 checks) | [S5_5.2_shipper_winner.png](S5/S5_5.2_shipper_winner.png)<br>[S5_5.2_shipper2_loser.png](S5/S5_5.2_shipper2_loser.png) | 11 |
| 5.3 | shipper | refused: 'Collect exactly 80,000 VND in cash and enter that amount.'; still Picked up | Collect exactly 80,000 VND in cash and enter that amount. Order 11 Picked up · from SaigonBite District 1 Hub Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City (0.39 km) Customer … | PASS (2/2 checks) | [S5_5.3_shipper.png](S5/S5_5.3_shipper.png) | 11 |
| 5.4 | shipper | banner 'Order 11 is delivered.'; Delivered; Cash collected 80,000 VND | Order 11 is delivered. Order 11 Delivered · from SaigonBite District 1 Hub Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City (0.39 km) Customer Tran Thi Mai · 0901234567 Payment C… | PASS (4/4 checks) | [S5_5.4_shipper.png](S5/S5_5.4_shipper.png) | 11 |
| 5.5 | customer | Delivered; payment 'COD, paid'; receipt PAID, 80,000 VND, Total T 80,000 VND, Refund owed 0 VND | Order 11 SaigonBite District 1 Hub · placed 01:22, 27/10/2026 Status Delivered Payment COD, paid Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City Confirmed 01:22, 27/10/2026 Read… | PASS (7/7 checks) | [S5_5.5_customer_receipt.png](S5/S5_5.5_customer_receipt.png) | 11 |

## S6 Declined payment, rejected paid order, cancellation, failed delivery

Expected written first: [`S6/expected.md`](S6/expected.md). Corroboration: [`S6/db_facts.json`](S6/db_facts.json).

| Step | Role | Expected | Actual (page text, shortened) | Result | Screenshot | Order |
|---|---|---|---|---|---|---|
| 6a.1 | customer | next screen is the Payment simulator: Amount 20,000 VND, Method E-wallet; no 'price changed' notice | Payment simulator Stands in for the payment provider in this demo. No card or wallet details are asked for and no money moves. Amount: 20,000 VND Method: E-wallet Approve payment Decline payment | PASS (4/4 checks) | [S6_6a.1_customer.png](S6/S6_6a.1_customer.png) |  |
| 6a.2 | customer | HTTP 402 quote page 'The payment was declined. No order was placed. Try again or choose cash on delivery.' | Kitchen Dishes Confirm Done Check your order Nothing is ordered until you press Confirm order. The payment was declined. No order was placed. Try again or choose cash on delivery. SaigonBite District… | PASS (2/2 checks) | [S6_6a.2_customer.png](S6/S6_6a.2_customer.png) |  |
| 6a.3 | customer | 11 orders and 11 payment rows; no order 12 | orders=11 payments=11 | PASS (2/2 checks) | [S6_6a.3_customer.png](S6/S6_6a.3_customer.png) |  |
| 6b.1 | customer | 'Order 12 is placed', 65,000 VND, ONLINE PAID, 'You paid online' | Kitchen Dishes Confirm Done Order 12 is placed The kitchen will confirm it shortly. You paid online: 65,000 VND Order number 12 Status PLACED, waiting for the kitchen to confirm Payment ONLINE (E-wal… | PASS (5/5 checks) | [S6_6b.1_customer.png](S6/S6_6b.1_customer.png) | 12 |
| 6b.2 | kitchen | banner 'Order 12 is rejected and the customer is told why.' | Order 12 is rejected and the customer is told why. Order 12 Placed 01:22, 27/10/2026 · Rejected · ONLINE (paid) Dish Unit price Qty Amount Pho bo tai 55,000 VND 1 55,000 VND Dishes 55,000 VND Deliver… | PASS (1/1 checks) | [S6_6b.2_kitchen.png](S6/S6_6b.2_kitchen.png) | 12 |
| 6b.3 | customer | Rejected + reason; payment refund pending with 65,000 VND named as a refund owed (payout pending), never refunded; receipt: captured C 65,000, REFUND_PENDING, Refund owed 65,000 | Order 12 SaigonBite District 1 Hub · placed 01:22, 27/10/2026 Status Rejected · The beef has run out for today. Payment ONLINE (E-wallet), refund pending · refund owed 65,000 VND, payout pending Deli… | PASS (9/9 checks) | [S6_6b.3_customer_receipt.png](S6/S6_6b.3_customer_receipt.png) | 12 |
| 6c.1 | customer | 'Order 13 is placed', 20,000 VND | Kitchen Dishes Confirm Done Order 13 is placed The kitchen will confirm it shortly. Have this amount ready in cash for the driver: 20,000 VND Order number 13 Status PLACED, waiting for the kitchen to… | PASS (2/2 checks) | [S6_6c.1_customer.png](S6/S6_6c.1_customer.png) | 13 |
| 6c.2 | customer | banner 'Order 13 is cancelled.'; Cancelled; payment 'COD, voided' | Order 13 is cancelled. Order 13 SaigonBite District 1 Hub · placed 01:22, 27/10/2026 Status Cancelled Payment COD, voided Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City Finishe… | PASS (3/3 checks) | [S6_6c.2_customer.png](S6/S6_6c.2_customer.png) | 13 |
| 6c.3 | kitchen | no card for Order 13 | SaigonBite District 1 Hub Kitchen capacity 14 orders. New, confirmed and preparing orders count towards it. New 2 Order 8 10:10, 23/10/2026 1 x Goi cuon Confirm Reject or replace Order 9 01:22, 27/10… | PASS (1/1 checks) | [S6_6c.3_kitchen.png](S6/S6_6c.3_kitchen.png) | 13 |
| 6d.1 | shipper | banner 'You picked up order 7.'; Picked up | You picked up order 7. Order 7 Picked up · from SaigonBite District 1 Hub Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City (0.39 km) Customer Tran Thi Mai · 0901234567 Payment Co… | PASS (2/2 checks) | [S6_6d.1_shipper.png](S6/S6_6d.1_shipper.png) | 7 |
| 6d.2 | shipper | banner 'The failed delivery of order 7 is recorded. Bring the food back to the hub.'; Failed; Problem shows the reason | The failed delivery of order 7 is recorded. Bring the food back to the hub. Order 7 Failed · from SaigonBite District 1 Hub Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City (0.39… | PASS (3/3 checks) | [S6_6d.2_shipper.png](S6/S6_6d.2_shipper.png) | 7 |
| 6d.3 | customer | Delivery failed; Delivery problem shows the reason; payment 'COD, voided' | Order 7 SaigonBite District 1 Hub · placed 10:00, 23/10/2026 Status Delivery failed Payment COD, voided Deliver to 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City Confirmed 10:01, 23/10/20… | PASS (4/4 checks) | [S6_6d.3_customer.png](S6/S6_6d.3_customer.png) | 7 |

## S7 Manager reports against the hand-calculated oracle; archiving a closed order

Expected written first: [`S7/expected.md`](S7/expected.md). Corroboration: [`S7/db_facts.json`](S7/db_facts.json).

| Step | Role | Expected | Actual (page text, shortened) | Result | Screenshot | Order |
|---|---|---|---|---|---|---|
| 7.1 | manager | D1 1/90,000/-10,000/10,000/90,000/10,000/90,000; BT 1/60,000/0/10,000/70,000/0/70,000; All 2/150,000/-10,000/20,000/160,000/10,000/160,000; top items 3 & 1 | {"rows": [["SaigonBite District 1 Hub", "1", "90,000 VND", "-10,000 VND", "10,000 VND", "90,000 VND", "10,000 VND", "90,000 VND"], ["SaigonBite Binh Thanh Hub", "1", "60,000 VND", "0 VND", "10,000 VN… | PASS (5/5 checks) | [S7_7.1_manager.png](S7/S7_7.1_manager.png) |  |
| 7.2 | manager | 1 order, total 70,000 VND, refunds owed 0, net 70,000 | ["SaigonBite Binh Thanh Hub", "1", "60,000 VND", "0 VND", "10,000 VND", "70,000 VND", "0 VND", "70,000 VND"] | PASS (1/1 checks) | [S7_7.2_manager.png](S7/S7_7.2_manager.png) |  |
| 7.3 | manager | overall 2/1/33.3%/20.0 min (n=3)/25.0 min (n=2); D1 1/0/0.0%/10.0 (n=1)/20.0 (n=1); BT 1/1/50.0%/25.0 (n=2)/30.0 (n=1); one shipper = overall | {"overall": ["All deliveries", "2", "1", "33.3%", "20.0 min (n=3)", "25.0 min (n=2)"], "hubs": [["SaigonBite District 1 Hub", "1", "0", "0.0%", "10.0 min (n=1)", "20.0 min (n=1)"], ["SaigonBite Binh … | PASS (4/4 checks) | [S7_7.3_manager.png](S7/S7_7.3_manager.png) |  |
| 7.4 | manager | D1: New 0 Confirmed 0 Preparing 0, 0 / 12; Binh Thanh (Archived): New 1, 1 / 8 | [["SaigonBite District 1 Hub", "0", "0", "0", "0 / 12", "0%", "Quiet", "0", "0"], ["SaigonBite Binh Thanh Hub (Archived)", "1", "0", "0", "1 / 8", "12%", "Quiet", "0", "0"]] | PASS (2/2 checks) | [S7_7.4_manager.png](S7/S7_7.4_manager.png) |  |
| 7.5 | manager | Sales 'No delivered orders in this period.' and 0 / 0 VND; Delivery n/a, n/a (n=0), n/a (n=0) | Sales Delivered orders, counted on the day they were delivered (Ho Chi Minh City time). Rejected, cancelled and failed orders are not sales. From To (inclusive) Hub All hubs SaigonBite District 1 Hub… | PASS (3/3 checks) | [S7_7.5_manager_delivery.png](S7/S7_7.5_manager_delivery.png) |  |
| 7.6 | manager | (reference text for 7.8) | Hub Orders Dishes Vouchers Delivery fees Total Refunds owed Net SaigonBite District 1 Hub 3 320,000 VND -13,000 VND 35,000 VND 342,000 VND 0 VND 342,000 VND SaigonBite Binh Thanh Hub 1 80,000 VND -20… | PASS (1/1 checks) | [S7_7.6_manager.png](S7/S7_7.6_manager.png) |  |
| 7.7 | admin | banner 'The closed order is archived. Its history and reports are kept.'; Recently archived lists order 1; the history page opens | The closed order is archived. Its history and reports are kept. Archive finished orders Delivered, failed, rejected and cancelled orders closed before the chosen day leave the operational screens. No… | PASS (4/4 checks) | [S7_7.7_admin.png](S7/S7_7.7_admin.png) | 1 |
| 7.8 | customer+manager | receipt opens (Receipt · Order 1, Total T 130,000 VND); Sales table text identical; My orders no longer lists Order 1 | Receipt · Order 1 Placed 11:00, 20/10/2026 · SaigonBite District 1 Hub 12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City · Approximate distance 0.39 km Dish Amount Pho bo tai 2 x 55,000 VND … | PASS (5/5 checks) | [S7_7.8_customer_my_orders.png](S7/S7_7.8_customer_my_orders.png)<br>[S7_7.8_manager.png](S7/S7_7.8_manager.png) | 1 |
| 7.9 | admin | banner 'Only a closed, unarchived order can be archived.'; order 9 stays unarchived | Only a closed, unarchived order can be archived. Archive finished orders Delivered, failed, rejected and cancelled orders closed before the chosen day leave the operational screens. Nothing is delete… | PASS (2/2 checks) | [S7_7.9_admin.png](S7/S7_7.9_admin.png) | 9 |

## S8 CSRF: a token on every form; a form without or with a changed token is refused

Expected written first: [`S8/expected.md`](S8/expected.md). Corroboration: [`S8/db_facts.json`](S8/db_facts.json).

| Step | Role | Expected | Actual (page text, shortened) | Result | Screenshot | Order |
|---|---|---|---|---|---|---|
| 8.1 | all roles | 0 post forms without a non-empty csrf_token | 310 post forms on 38 distinct role/page pairs; missing: 0 | PASS (1/1 checks) | [S8_8.1_admin.png](S8/S8_8.1_admin.png) |  |
| 8.2 | admin | HTTP 400 'Form expired' with the expiry message; BT still 1 / 8 | Form expired Error 400 This form has expired or did not come from SaigonBite. Go back, reload the page and try again. Back to hubs | PASS (4/4 checks) | [S8_8.2_admin.png](S8/S8_8.2_admin.png) |  |
| 8.3 | admin | HTTP 400 'Form expired' with the expiry message; BT still 1 / 8 | Form expired Error 400 This form has expired or did not come from SaigonBite. Go back, reload the page and try again. Back to hubs | PASS (4/4 checks) | [S8_8.3_admin.png](S8/S8_8.3_admin.png) |  |
| 8.4 | kitchen | HTTP 400 Form expired; Pho bo tai still Available | Form expired Error 400 This form has expired or did not come from SaigonBite. Go back, reload the page and try again. Back to kitchen board | PASS (3/3 checks) | [S8_8.4_kitchen.png](S8/S8_8.4_kitchen.png) |  |
| 8.5 | customer | HTTP 400 Form expired; order 9 still PLACED | Form expired Error 400 This form has expired or did not come from SaigonBite. Go back, reload the page and try again. Back to order food | PASS (3/3 checks) | [S8_8.5_customer.png](S8/S8_8.5_customer.png) | 9 |

## Notes on specific results

- **Race (5.2).** Both submits were dispatched in the two profiles 7 ms apart and both responses were awaited afterwards; `shipper` won and `shipper2` saw the message. The browser shows the user-facing outcome only; the barrier tests in pytest (`tests/test_p4_delivery.py`, `tests/test_p4_ordering.py`) are the race proof (**Tested**).
- **CSRF (S8).** 340 POST forms were seen on 42 distinct role/page pairs during S1 to S7 (`forms_seen.json`); none lacked a non-empty `csrf_token`. A form with the token removed (8.2, 8.4, 8.5) or changed (8.3) was refused with HTTP 400 'Form expired' and changed nothing.
- **Oracle (S7 A).** The manager's Sales, Delivery performance and Workload screens show exactly the figures of `tests/fixtures/report_oracle_expected.md` for 20/10/2026, for the hub filter and for the empty day (n/a). The report screens never write; the oracle database was only read.
- **Browser events.** 11 steps produced console or HTTP errors; every one is a refusal the step expects (400, 402, 403, 409). No script error and no unexpected response occurred (`events` in `results.json`).

## Defects found in P5 (`defects.csv`)

| Id | Where | Severity | Decision | Fix commit |
|---|---|---|---|---|
| P5-D01 | UC-06 screen capture / admin dish form (admin.edit_item, admin.new_it… | medium (an admin could not save or add a dish at any normal… | Small fix: one template line, no BR, route or money change | b68bfef |
| P5-D02 | UC-01-S04 / S06 quote page, online payment | medium (every online order started with a false warning) | Small fix in template and app.js only: each press fetches the fingerprint of the chosen payment from /order/quote (writes nothing) and then sends the… | ce18bf6 |
| P5-D03 | UC-02-S04 lost pick-up | low to medium | Partly fixed: the error page now links to the user's own first screen ('Back to deliveries'; template only). The double message remains because the r… | 1776293 (+ 5394cee test encoding) |
| P5-D04 | UC-01-S04 quote table | low | Small fix: format the distance with two decimals in the template | 5466f6a (+ 5394cee test encoding) |
| P5-D05 | UC-05 / S6 step 6b.3 order page of a rejected online order | low (wording) | Small fix: template wording 'refund owed 65,000 VND, payout pending' | 252ada1 |
| P5-D06 | UC-05-S08 replacement declined (found by the UC-05 package worker, co… | low (wording) | NOT fixed: the text is in order.py (answer_replacement route), sealed by the G4 dependency policy; a change needs an owner-reviewed seal update. Back… | - |

## What is Demonstrated and what is not

**Demonstrated** (browser, this folder): the six main use cases working together in one running system on a local Flask development server: UC-03/UC-06 catalogue and capacity reaching the customer, UC-01 ordering with busy-hub refusal, fresh quote, COD and online payment, UC-05 replacement and rejection, UC-02 delivery with a lost pick-up and exact cash, UC-04 reports against the hand oracle, order archiving, role and hub isolation, CSRF.
**Tested, not Demonstrated here:** the race proof (pytest barrier tests), the security matrix, the money arithmetic (915 passing tests at the entry commit; see the final receipt for the final count).
**Not claimed:** deployment. The Docker/gunicorn/Caddy build on the GCP VM is phase P6; nothing here is **Deployed**. No real payment: the online payment is the labelled simulator. No push, tag, upload or external contact was made.

