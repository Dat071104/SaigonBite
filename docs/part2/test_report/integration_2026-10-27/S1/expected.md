# S1 Catalogue and capacity reach the customer; archived and sold-out dishes cannot be ordered

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Written before the run. Money is hand-computed (plan §7.2).

Start state: fresh demo database (history orders 1 to 8). District 1 hub (D1): capacity 12, load 1 (order 8 is PLACED), so it is quiet (1 < 25% of 12). Binh Thanh hub (BT): capacity 8, load 0. Dish 5 (Com tam ga nuong) is sold out at D1 (seed). Customer Mai, address Home (0.39 km from D1: fee 12,000 + 3,000 × 1 = 15,000).

| Step | Profile | Action | Expected (screen text, state) | Rules |
|---|---|---|---|---|
| 1.1 | admin | open Hubs | h1 "Hubs and kitchen capacity"; row HUB-D1 shows "1 / 12" and Quiet; row HUB-BT shows "0 / 8" and Quiet | BR-01, BR-03 |
| 1.2 | admin | Edit D1, capacity 14, Save hub | back on Hubs with the banner "The hub is saved."; row HUB-D1 shows "1 / 14" | BR-01 (capacity 1 to 500) |
| 1.3 | admin | Menu of D1: add "Sweet Che House: Che thai (30,000 VND)", initial availability Available | banner "The dish is on the hub's menu."; the menu table has a row Che thai, Sweet Che House, 30,000 VND, Available | UC-06 listItemAtHub |
| 1.4 | customer | Order food, "Order from this hub" at D1 | the menu shows the brand "Sweet Che House" with Che thai 30,000 VND and a quantity field; "Com tam ga nuong" is shown as "Sold out" with no quantity field | BR-19 |
| 1.5 | admin | Brands and menu: Archive the dish "Banh mi op la" | banner "The dish is archived. It can no longer be ordered."; the dish row shows Archived | BR-19 |
| 1.6 | customer | reload the D1 menu | "Banh mi op la" is not on the page at all (archived dishes are not offered) | BR-19 |
| 1.7 | customer | add the field qty_5 = 1 (the sold-out dish) to the menu form by script, address Home, "See the quote" | refused on the menu page, HTTP 400, banner "Item 5 is not available at SaigonBite District 1 Hub."; no quote page; nothing saved | E01, BR-19 |
| 1.8 | customer | the same with qty_8 = 1 (the archived dish) | refused the same way: "Item 8 is not available at SaigonBite District 1 Hub.", HTTP 400 | E01, BR-19 |
| 1.9 | customer | order 1 × Che thai, Home, cash on delivery | quote: Dishes 30,000 VND; Delivery fee (0.39 km) 15,000 VND; Quiet hub discount -5,000 VND (load 1 < 25% of 14 = 3.5); Total 40,000 VND. After "Confirm order": "Order 9 is placed", 40,000 VND, status PLACED | BR-03, BR-07, BR-09 |

Corroboration after the scenario (read-only DB query): 9 orders; order 9 PLACED at hub 1 with total 40,000; no order line for items 5 or 8 in any order after order 8.
