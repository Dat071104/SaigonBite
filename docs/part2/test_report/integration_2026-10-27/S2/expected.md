# S2 A full hub refuses with a quieter-hub suggestion; the suggestion gives a fresh quote

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Written before the run. Money is hand-computed.

Start state (after S1): 9 orders. D1 capacity 14, load 2 (orders 8 and 9 PLACED), quiet (2 < 3.5). BT capacity 8, load 0. Mai's Home is 4.06 km from BT: fee 10,000 + 3,000 × ceil(4.06) = 10,000 + 15,000 = 25,000. Emma (tourist) has the address Hotel (Rex Hotel, 0.06 km from D1: fee 12,000 + 3,000 × 1 = 15,000).

| Step | Profile | Action | Expected | Rules |
|---|---|---|---|---|
| 2.1 | admin | Edit BT, capacity 1, Save | banner "The hub is saved."; row HUB-BT shows "0 / 1" | BR-01 (lowest capacity is 1) |
| 2.2 | customer | order 1 × Com tam suon bi cha at BT, Home, cash on delivery | quote: Dishes 60,000 VND; Delivery fee (4.06 km) 25,000 VND; Quiet hub discount -5,000 VND (load 0 < 25% of 1); Total 80,000 VND. "Order 10 is placed", 80,000 VND | BR-03, BR-05, BR-07 |
| 2.3 | admin | open Hubs | row HUB-BT shows "1 / 1" and Busy | BR-02 |
| 2.4 | tourist | order 1 × Com tam suon bi cha at BT, address Hotel, "See the quote" | refused, HTTP 409, on the hub list: banner "SaigonBite Binh Thanh Hub is too busy to take new orders right now."; panel "These hubs can take your order now" with a link "SaigonBite District 1 Hub" and the note "Quiet: 5,000 VND off delivery"; the BT card is marked "Busy now"; no quote | BR-02, BR-04 |
| 2.5 | tourist | follow the link to D1, order 1 × Pho bo tai, Hotel, "See the quote" | a fresh quote at D1 (heading names the District 1 hub): Dishes 55,000 VND; Delivery fee (0.06 km) 15,000 VND; Quiet hub discount -5,000 VND; Total 65,000 VND (a different fee and discount from the BT attempt); not confirmed | BR-03, BR-04, BR-07 |
| 2.6 | tourist | leave without confirming | nothing was saved by steps 2.4 and 2.5: still 10 orders in the database | BR-10, MG03 |
| 2.7 | admin | Edit BT, capacity 8, Save | banner "The hub is saved."; row HUB-BT shows "1 / 8" | BR-01 |

Corroboration (read-only): 10 orders; order 10 PLACED at hub 2; no order, line or payment row for Emma after order 8.
