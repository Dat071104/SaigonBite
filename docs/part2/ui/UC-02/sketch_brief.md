# UC-02 Deliver an order: sketch brief (drawn in Figma by Codex (AI-assisted) on 27/10/2026)

Brief authored by 722I0004 with Claude Sonnet 5.5 assistance. Low-fidelity sketches were drawn from this brief in Figma by Codex (AI-assisted) on 27/10/2026; exports and attribution are in `sketch/README.md`.

Device: the shipper's phone (390 × 844 portrait), one column. Draw one rectangle per screen, about 10 minutes for all of them.

| Sketch | Screen it becomes | Draw these controls | SSD operation it serves |
|---|---|---|---|
| 1 | UC-02-S01 Deliveries | wordmark, "Deliveries" link, name and "Log out"; headings "On my bike" and "Ready for pickup"; cards (grey surface) with order number, ready-since time, hub to address, a big bold "Cash on delivery: amount" and a full-width "Pick up this order" button; table "My recent deliveries" | OP-21 viewReadyDeliveries |
| 2 | UC-02-S02 Delivery waiting for pickup | order number and badge "Awaiting pickup"; list Deliver to, Payment (bold cash), Ready; dishes as "1 x name"; full-width "Pick up this order"; "All deliveries" | OP-22 viewDelivery, OP-10 takeDelivery |
| 3 | UC-02-S03 Picked up | message "You picked up order N"; list incl. Customer with a phone link; box "Delivered" with the field "Cash collected (VND)" and "Confirm delivery"; box "Could not deliver" with "What happened" and a red "Report failed delivery" | OP-10 takeDelivery, OP-11 confirmDelivered, OP-12 reportFailure |
| 4 | UC-02-S04 Pick-up lost | red message "already been picked up"; title "Not allowed", "Error 403"; red box "Another shipper is delivering this order"; button "Back to deliveries" | OP-10 (refusal, BR-25) |
| 5 | UC-02-S05 Cash amount refused | red message "Collect exactly N VND in cash and enter that amount" above the same page as sketch 3 | OP-11 (refusal, exact cash) |
| 6 | UC-02-S06 Delivered | message "Order N is delivered"; badge "Delivered"; list with Finished and Cash collected; no forms; "All deliveries" | OP-11 confirmDelivered |

Keep: labels in words (no icons), the cash to collect as the biggest figure on the screen, one main full-width button per card, 44 px controls.
