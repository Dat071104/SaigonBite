# UC-01 Place an order: sketch brief (drawn in Figma by Codex (AI-assisted) on 27/10/2026)

Brief authored by 722I0004 with Claude Sonnet 5.5 assistance. Low-fidelity sketches were drawn from this brief in Figma by Codex (AI-assisted) on 27/10/2026; exports and attribution are in `sketch/README.md`.

Device: a phone (390 × 844 portrait), one column. Draw one rectangle per screen, about 10 minutes for all of them.

| Sketch | Screen it becomes | Draw these controls | SSD operation it serves |
|---|---|---|---|
| 1 | UC-01-S01 Choose a kitchen hub | wordmark and 3 role links on top; step bar (Kitchen, Dishes, Confirm, Done); one box per hub with name, fee and a Busy/Quiet note and a wide "Order from this hub" button | OP-13 browseHubs |
| 2 | UC-01-S03 Choose dishes, address and voucher | dishes grouped by brand, each with price and − 0 + stepper; one "Sold out" row; address select; voucher field; sticky bar "2 items · 70,000 VND" with "See the quote" | OP-14 selectHub |
| 3 | UC-01-S04 Check the quote and choose payment | hub and address box; table of lines; rows Dishes, Delivery fee, Quiet hub discount; bold Total; "How will you pay?" with 3 options; "Confirm order" and "Change items" | OP-15 requestQuote, OP-01 confirmCheckout |
| 4 | UC-01-S02 Hub is full | red message "too busy"; box "These hubs can take your order now" with a link; hub list with "Busy now" | OP-15 (refusal, BR-04) |
| 5 | UC-01-S08 Order placed | big total, order number, status, payment line, lines, "Follow this order" | OP-01 |
| 6 | UC-01-S09 Follow an order | status badge, payment, address, lines, "Cancel this order", "Printable receipt" | OP-16 viewReceipt, OP-07 cancelOrder |

Keep: labels in words (no icons), one main button per screen, the total always with "VND".
