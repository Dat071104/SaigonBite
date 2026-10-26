# S4 Sold-out dish, cheaper replacement, customer accepts, kitchen cooks, one delivery

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Written before the run. Money is hand-computed.

Start state (after S3): order 11 PLACED at D1: 2 × Pho ga (50,000 each), S 100,000, F 15,000, Q 5,000, T 110,000. Che thai is listed at D1 (S1); Banh mi op la is archived.

| Step | Profile | Action | Expected | Rules |
|---|---|---|---|---|
| 4.1 | kitchen | Availability: "Mark sold out" on Pho ga | banner "Availability updated."; the Pho ga row shows Sold out and the button "Available again" | UC-05 SUC-06 |
| 4.2 | kitchen | Order 11: choose "Pho ga → Goi cuon (35,000 VND)" and "Send the offer" | banner "The replacement is offered. The order waits for the customer's answer."; the page says "Replacement offered: Pho ga → Goi cuon" and that the customer's answer is awaited; no Confirm button while the offer is open | plan §3.3, BR-26 |
| 4.3 | customer | My orders, then Order 11 | My orders shows "Your answer needed" on Order 11. The order page shows the panel "The kitchen asks about a replacement": "Pho ga has run out. The kitchen offers Goi cuon at 35,000 VND instead of 50,000 VND."; "the new total is 80,000 VND (now 110,000 VND)" (S = 2 × 35,000 = 70,000; 70,000 + 15,000 - 5,000 = 80,000) | UC-05 viewReplacement |
| 4.4 | customer | "Accept Goi cuon" | banner "Replacement accepted. The kitchen may now confirm your order."; the lines show Goi cuon 2 × 35,000 = 70,000 VND and Total 80,000 VND; the panel is gone | UC-05 acceptReplacement |
| 4.5 | kitchen | Confirm order, Start preparing, Mark ready | banners "Order 11 is confirmed.", "Order 11 is being prepared.", "Order 11 is ready. Shippers can now pick it up."; the board shows Order 11 under "Ready for pickup" | UC-05, SUC-05 |
| 4.6 | customer | open Order 11 | Status Ready | |
| 4.7 | kitchen | Availability: "Available again" on Pho ga | banner "Availability updated."; Pho ga Available | |

Corroboration (read-only): order 11 READY, total 80,000; exactly one delivery row for order 11, state AWAITING_PICKUP, no shipper; offer state ACCEPTED.
