# S5 Two shippers take the same order together: one wins, exact cash, customer sees delivered and paid

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Written before the run. The browser shows the user-facing outcome; the barrier test in pytest (tests/test_p4_delivery.py and tests/test_p4_ordering.py) is the race proof (Tested).

Start state (after S4): order 11 READY, COD, total 80,000 VND; demo order 7 is also READY (65,000 VND).

| Step | Profile | Action | Expected | Rules |
|---|---|---|---|---|
| 5.1 | shipper, shipper2 | open Deliveries | both boards list "Order 11" under "Ready for pickup" with "Cash on delivery: 80,000 VND" (and Order 7 with 65,000 VND) | BR-25 |
| 5.2 | shipper, shipper2 | open Order 11 in both, then press "Pick up this order" in both profiles with both clicks dispatched before either response is awaited | exactly one profile (the winner) sees "You picked up order 11." and the badge "Picked up"; the other sees the banner "Order 11 has already been picked up. Nothing was changed." and an error page "Not allowed: Another shipper is delivering this order." with a link "Back to deliveries"; the delivery row has one shipper | BR-25 |
| 5.3 | winner | enter 79,000 as cash, "Confirm delivery" | refused: banner "Collect exactly 80,000 VND in cash and enter that amount."; still Picked up; nothing changed | BR-25 |
| 5.4 | winner | enter 80,000, "Confirm delivery" | banner "Order 11 is delivered."; badge "Delivered"; "Cash collected 80,000 VND" | BR-25, BR-09 |
| 5.5 | customer | open Order 11 and its receipt | Status Delivered; payment "COD, paid"; receipt shows Payment state PAID, Payment amount 80,000 VND, Total T 80,000 VND, Refund owed 0 VND | BR-13 |

Corroboration (read-only): order 11 DELIVERED; delivery DELIVERED with one shipper and cash_collected 80,000; payment COD PAID 80,000.
