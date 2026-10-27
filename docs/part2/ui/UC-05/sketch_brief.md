# UC-05 Confirm or reject: sketch brief (drawn in Figma by Codex (AI-assisted) on 27/10/2026)

Brief authored by 722I0004 with Claude Sonnet 5.5 assistance. Low-fidelity sketches were drawn from this brief in Figma by Codex (AI-assisted) on 27/10/2026; exports and attribution are in `sketch/README.md`.

Device: the kitchen board is a wide screen (1440 × 900 landscape, four columns); the customer screens are a phone (390 × 844 portrait, one column).
Draw one rectangle per screen, about 10 minutes for all of them.

| Sketch | Screen it becomes | Draw these controls | SSD operation it serves |
|---|---|---|---|
| 1 | UC-05-S01 Kitchen board | wordmark, "Kitchen board" and "Availability" links, user name and "Log out"; hub name as title; four columns New, Confirmed, Preparing, Ready for pickup, each with a count; in New, cards with order number, time, lines, a "Confirm" button and a "Reject or replace" link | OP-19 viewKitchenOrders |
| 2 | UC-05-S02 Kitchen order | order number, state badge, payment; table of lines with totals; "Confirm order" button; box "Offer a replacement" with a "Replace" drop-down and "Send the offer"; box "Reject the order" with a "Reason for the customer" field and a red "Reject order"; "Back to the board" | OP-20 viewKitchenOrder, OP-02 confirmOrder, OP-03 rejectOrder, OP-04 offerReplacement |
| 3 | UC-05-S03 Replacement offered | green message "The replacement is offered"; highlighted box "Replacement offered: A to B, waiting for the customer"; no Confirm button; the reject box still there | OP-04 offerReplacement |
| 4 | UC-05-S05 My orders: your answer is needed (phone) | one row per order: number and total on the first line, time and hub below, status badge; one row with a warning badge "Your answer needed" | OP-17 viewMyOrders |
| 5 | UC-05-S06 Replacement offer (phone) | highlighted box "The kitchen asks about a replacement": the dish that ran out, the offered dish and both prices, the new total and the consequence of declining; two wide buttons "Accept <dish>" and "Decline"; below it status, address, lines | OP-18 viewReplacement, OP-05 acceptReplacement, OP-06 declineReplacement |
| 6 | UC-05-S09 Offer withdrawn (phone) | grey notice "The replacement is no longer available. The offer was withdrawn"; order unchanged; "Replacement history" line; "Cancel this order" as an outlined red button | OP-05 acceptReplacement (dish gone) |

Keep: labels in words (no icons), the amounts always with "VND", "Reject order" as the only solid red button of the kitchen page, 44 px controls.
