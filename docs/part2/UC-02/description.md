# UC-02 — Deliver an order: pick up, deliver with cash collection, or report failure (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

## Use case name

UC-02 — Deliver an order: pick up, deliver with cash collection, or report failure.

## Scenario / trigger

A shipper requests ready deliveries, claims an unassigned READY order, and later records either successful handover or a failed delivery. Pickup and finish are separate requests; leaving the session does not undo a successful pickup. Main success below uses COD; ONLINE and failure are explicit alternatives.

## Actors

Primary: Shipper, an authenticated ACTIVE UserAccount with role SHIPPER. The customer receives the food in the business process but does not send a system message in this use case. No payment provider participates: ONLINE was captured by the simulator during UC-01.

## Related use cases

Figure 2.1B associates Shipper with UC-02. It defines no include/extend relation for UC-02. SUC-05 supplies READY orders and their AWAITING_PICKUP Delivery; UC-01 supplies Order/Payment and immutable delivery-address snapshots; SUC-01 supplies authentication; SUC-08 maintains active accounts; UC-04 reads the outcome. These are serving references, not invented UML include/extend relations.

## Stakeholders and interests

Shipper needs a fair atomic claim, minimum necessary contact details and exact cash due. Customer needs correct delivery and no duplicate collection. Kitchen needs an unambiguous handover. Management needs paired Order/Delivery states, times, cash and refund obligations for reports. Admin must not deactivate a shipper holding a PICKED_UP delivery (BR-25).

## Pre-conditions

Every request rechecks the authenticated active SHIPPER context (BR-25); identity comes from the session. Pickup requires Order READY and its single unassigned Delivery AWAITING_PICKUP. Any active shipper can claim any READY order, including while holding other deliveries; there is no one-active-delivery cap. Finish requires the same Order OUT_FOR_DELIVERY, Delivery PICKED_UP and the authenticated shipper assigned to it. Order retains S/D/F/Q/T, address snapshot and Payment; COD is PENDING and due T; ONLINE is already PAID with captured amount C. A prior accepted replacement may leave a partial refund owed while ONLINE remains PAID.

## Post-conditions

The following register text is verbatim. PC01 is the committed pickup milestone; PC02 and PC03 are exclusive terminal outcomes.

| ID | Guarantee |
|---|---|
| UC02-PC01 | one shipper assigned, Delivery PICKED_UP, order OUT_FOR_DELIVERY |
| UC02-PC02 | delivered: Delivery DELIVERED, order DELIVERED, COD PAID with cash = T |
| UC02-PC03 | failed: Delivery FAILED + reason, order DELIVERY_FAILED, BR-17 |
| UC02-MG01 | second shipper / wrong shipper / wrong cash / repeat → 0 rows changed |

Each accepted command saves related state/time/payment facts atomically. Successful ONLINE delivery keeps PAID, C and any partial refund owed; it takes no cash. Failed delivery saves a nonempty failureReason and finished/closed timestamps; COD becomes VOIDED; ONLINE becomes REFUND_PENDING with refund_amount=C, replacing any partial obligation, in the same change (BR-17). Refund payout is deferred, never claimed completed. A refused command changes no rows, preserving any previously committed pickup or finish. Read requests write nothing. BR-12 exposes only delivery contact and the stored address snapshot; passport is excluded from shipper views and logs.

## Flow of activities

| Actor | System |
|---|---|
| 1. Request available and own deliveries: `viewReadyDeliveries()`. | Recheck active role; return `readyAndOwnAssignedDeliveries`. Ready candidates are not reservations. |
| 2. Select an order: `viewDelivery(orderId)`. | Recheck visibility; return `deliveryContactSnapshotAndCashDue`, with permitted contact, address snapshot, status and cash due T for COD or zero for ONLINE; never passport. |
| 3. Pick up the ready order: `takeDelivery(orderId)`. | Atomically recheck active shipper, READY, unassigned AWAITING_PICKUP and win the claim; assign exactly this shipper, record picked_up_at, set PICKED_UP / OUT_FOR_DELIVERY; return `assignedDelivery` (UC02-PC01). |
| 4. Travel to the stored destination and hand over the food. When resuming, use `viewReadyDeliveries()` and `viewDelivery(orderId)` as steps 1–2 to find and inspect an own PICKED_UP delivery; do not claim it again. | Preserve the committed assignment across requests; show the same snapshot and current payment summary. |
| 5. Choose successful delivery; collect exactly T VND for COD and send `confirmDelivered(orderId, cashCollected=T)`. | Recheck active assigned shipper, live states and exact cash. Atomically set Delivery/Order DELIVERED, COD PENDING→PAID, cash_collected=T and finished_at/closed_at; return `deliveredOrderAndPayment` (UC02-PC02). |
| 6. Read the delivery outcome. | Show recorded cash/payment/refund obligation; end successfully. No second charge or refund payout occurs. |

Alternatives (branch and continuation are explicit):

| ID | Branch step | Actor and system behaviour | Rejoin / end |
|---|---|---|---|
| A01 | 5, ONLINE already PAID | Shipper takes no cash and sends `confirmDelivered(orderId, cashCollected=0)` (optional parameter may instead be omitted). System rechecks assignment/states and zero-or-absent cash, saves Delivery/Order DELIVERED and finish/close times, leaves ONLINE PAID/C/refund owed unchanged; returns `deliveredOrderAndPayment`. | Rejoin 6; UC02-PC02's COD clause applies only to COD. |
| A02 | 5, unable to complete delivery | Shipper sends `reportFailure(orderId, reason)` with a nonempty reason. System rechecks active assigned shipper and live states, saves Delivery FAILED + failureReason, Order DELIVERY_FAILED, finish/close times and BR-17 payment effects atomically; returns `failedOrderAndPayment`. | Rejoin 6; end with UC02-PC03. Physical return of food is outside this system interaction. |
| A03 | 1–2, own delivery already PICKED_UP | Inspect own assignment via `viewDelivery(orderId)`, then continue travel. | Rejoin 4, bypass 3; prior UC02-PC01 remains. |
| A04 | 1, no ready or own assignment | System returns an empty set; shipper may end or make a fresh step-1 query. | End read-only, UC02-MG01 (0 rows changed), or rejoin 1. |

## Exception conditions

| ID | Branch step | Condition / response | Rejoin / guaranteed end |
|---|---|---|---|
| E01 | 1–5 and A02 | Missing/inactive/non-SHIPPER session: return `refusal`; disclose no delivery contact and change no rows. | End; UC02-MG01. A fresh authenticated attempt is separate. |
| E02 | 2–3 | Missing/non-ready order, another shipper's assignment, or simultaneous claim lost: return `refusal`; the winner alone retains assignment. | End; UC02-MG01. Refresh via a new step-1 query. |
| E03 | 5 or A01/A02 | Wrong shipper, stale state, repeated finish/failure, or contradictory terminal request: return `refusal`; no payment or lifecycle mutation. | End; UC02-MG01; earlier committed outcome remains. |
| E04 | 5/A01 | COD cash missing, malformed, negative or unequal to T; or nonzero ONLINE cash: return `refusal`; do not mark delivered or paid. | End; UC02-MG01. Corrected submission is a new request from 5. |
| E05 | A02 | Missing/blank failure reason: return `refusal`; no failure or refund obligation is saved. | End; UC02-MG01. Corrected request starts at A02. |
| E06 | 3/5/A01/A02 | Atomic persistence fails: reject/roll back this command's complete change; do not present a success before commit. | End; UC02-MG01; no partial paired update. |
