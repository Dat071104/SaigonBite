# S3 An order reaches the kitchen of its own hub only

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Written before the run. Money is hand-computed.

Start state (after S2): D1 load 2 (orders 8, 9), BT load 1 (order 10, capacity 8). Customer Mai, Home.

| Step | Profile | Action | Expected | Rules |
|---|---|---|---|---|
| 3.1 | customer | order 2 × Pho ga at D1, Home, cash on delivery | quote: Dishes 100,000 VND; Delivery fee (0.39 km) 15,000 VND; Quiet hub discount -5,000 VND (load 2 < 3.5); Total 110,000 VND. "Order 11 is placed", 110,000 VND, status PLACED | BR-03, BR-07, BR-09 |
| 3.2 | kitchen (D1) | open the Kitchen board | heading "SaigonBite District 1 Hub"; a card "Order 11" in the New column with "2 x Pho ga" and a Confirm button; New shows 3 (orders 8, 9, 11) | BR-26 |
| 3.3 | kitchen_bt (BT) | open the Kitchen board | heading "SaigonBite Binh Thanh Hub"; a card "Order 10"; no "Order 11" anywhere on the page | BR-26 |
| 3.4 | kitchen_bt | open /kitchen/orders/11 by typing the address | HTTP 403 "Not allowed", message "This order belongs to another hub."; no order data shown | BR-26 |
| 3.5 | kitchen_bt | send a Confirm request for order 11 from the BT session (a real form post with the session's CSRF token) | HTTP 403 "Not allowed", "This order belongs to another hub."; order 11 stays PLACED, confirmed_at empty | BR-26 |
| 3.6 | kitchen (D1) | open Order 11 | the order page lists 2 × Pho ga, Total 110,000 VND, status Placed, with the buttons Confirm order and Reject order and the section Offer a replacement | UC-05 |

Corroboration (read-only): order 11 hub 1, PLACED, confirmed_at NULL.
