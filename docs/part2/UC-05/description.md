# UC-05 — Decide an incoming order: confirm, reject, or offer a replacement the customer agrees to (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

| Item | Content |
|---|---|
| Use case name | UC-05 — Decide an incoming order: confirm, reject, or offer a replacement the customer agrees to. Author: 722I0004 · AI-assisted (Codex) |
| Scenario / trigger | Kitchen staff opens an incoming own-hub PLACED order and chooses confirm, reject or a whole-line replacement for a dish currently unavailable. The customer answers separately through SUC-03; the kitchen request never waits inside a transaction for the answer. |
| Actors | Primary: Kitchen staff. Customer participates in the separate SUC-03 response session (companion fragment with Customer + :System). Every request rechecks active role and owner/hub authorization. |
| Related use cases | Figure 2.1B shows Kitchen staff and Customer participation, with the Customer response served by SUC-03 in Figure 2.1A. UC-01 supplies the original order. SUC-05 starts preparing/marks ready after confirmation; SUC-06 changes own-hub availability. These are serving/sequence links, not invented «include» relations. SUC-04 extends SUC-03 at order action selected when cancellation is requested from PLACED/CONFIRMED. |
| Stakeholders and interests | Kitchen: only own-hub decisions and one open offer. Customer: unchanged quantity, equal/lower offered unit price, consent to replacement amounts and preserved captured payment. Operator: atomic line/totals/offer/payment updates and explicit refund owed without a payout claim. |
| Pre-conditions | An active Kitchen staff session is assigned to a hub. A candidate incoming order exists; its own-hub PLACED state, open-offer status and current source/target eligibility are guards rechecked at each command. Customer response requires a separate active Customer session and own order. |
| Post-conditions | **UC05-PC01** confirm: own-hub PLACED → CONFIRMED<br>**UC05-PC02** reject: REJECTED + reason + BR-17 + offer WITHDRAWN<br>**UC05-PC03** offer: one OFFERED offer per §3.3<br>**UC05-PC04** accepted offer applied per §3.3 5–7<br>**UC05-MG01** wrong hub / open offer / stale / invalid target → order unchanged<br>PC01–PC04 are alternative outcomes at their respective operation boundaries. MG01 preserves Order; invalid-target acceptance may still withdraw the exact offer and return a reason. Later rejection/cancellation is never reversed. |
| Flow of activities | Numbered Actor / System main flow and A01–A05 / E01–E04 below form this field. Main steps 1–5 confirm; A02 rejects; A03 creates an offer; response C1–C6 is an explicitly separate SUC-03 session. |
| Exception conditions | Wrong hub/role/state, open offer on confirm or another offer, invalid source/target, stale answer and write failure produce controlled responses. Every failure ends with UC05-MG01 (Order unchanged); invalid-target acceptance alone changes the exact offer to WITHDRAWN and shows its reason, without adding a persisted reason field. |

## Flow of activities — main success (confirm)

| Actor | System |
|---|---|
| 1. Kitchen staff requests `viewKitchenOrders()`. | Returns `ownHubOrdersAndOffers`; only staff's hub, with PLACED/offer status and permitted kitchen details. Passport is never shown. No writes. |
| 2. Selects an order using `viewKitchenOrder(orderId)`. | Returns `ownHubOrderAndLines`; checks active kitchen role and hub. No writes. |
| 3. Reviews the lines and chooses confirm, submitting `confirmOrder(orderId)`. | Rechecks own hub, PLACED and no open OFFERED offer in the same short transaction as the change. If unavailable source requires a substitution, staff may instead choose A03; staff may reject under A02. |
| 4. — | Moves PLACED→CONFIRMED, sets confirmed_at and commits atomically; returns `confirmedOrder` (UC05-PC01). No payment or line reprice. |
| 5. Receives the confirmed decision. | The board reflects CONFIRMED. SUC-05 may later start preparation (`startPreparing(orderId)`, CONFIRMED→PREPARING, own hub, no open offer) and mark ready (`markReady(orderId)`, PREPARING→READY plus Delivery AWAITING_PICKUP); these remain separate supporting operations and are not SSD messages in this UC package. |

## Alternate flows

| ID | Branch point | Actor / System behaviour | Rejoin / end |
|---|---|---|---|
| A01 | Step 2/5, staff refreshes board/details | Calls `viewKitchenOrders()` / `viewKitchenOrder(orderId)` again; reads current facts without mutation. | Rejoin 2 or end read session; queries never change Order (UC05-MG01 invariant). |
| A02 | Step 3, chooses reject | Staff submits `rejectOrder(orderId, reason)`. System requires own-hub PLACED and nonempty reason; atomically sets REJECTED, reason and closed_at, withdraws any open offer and applies BR-17: COD→VOIDED; ONLINE→REFUND_PENDING with refund_amount=C, replacing any prior partial amount. Returns `rejectedOrder`. | End kitchen decision: UC05-PC02. Wrong/stale/invalid reason→E01; failed save→E04. |
| A03 | Step 3, chooses replacement | Staff submits `offerReplacement(orderId, orderLineId, targetItemId)`. One transaction rechecks own-hub PLACED, no OFFERED offer and selected line belongs to this Order. Source dish must be **currently unavailable at this hub** (sold out, unlisted or archived). Target must be ACTIVE with ACTIVE brand, listed and AVAILABLE at this same hub, different from source, absent from other order lines, and unit price ≤ source snapshot price; cross-brand is allowed. Inserts exactly one OFFERED offer with original/new name and price snapshots, line link and offered_at; quantity unchanged. Returns `offeredReplacement`. Order remains PLACED and still counts toward load. | End kitchen request: UC05-PC03. Continue later in independent C1–C6. Guards fail→E01/E02. |
| A04 | After C5 accepted response | Staff refreshes current board (A01); if another dish is unavailable, another sequential offer may be made while PLACED because resolved offers remain history. If no open offer remains, staff can confirm at step 3. | Rejoin 2/3 in a new request; never automatically confirm on Customer acceptance. |
| A05 | During offer wait or after acceptance | Customer may cancel via SUC-04 from own PLACED/CONFIRMED; open offer→WITHDRAWN, Order→CANCELLED, BR-17 full C (never C+partial). Kitchen may reject PLACED under A02. A concurrent response rechecks serialized current facts. | End that supported action. Later answer uses E03 and cannot revive CANCELLED/REJECTED; UC05-MG01 for refused answer. |

## C1–C6 — Customer response through SUC-03 (separate session)

| Actor | System |
|---|---|
| C1. Customer calls `viewMyOrders()` then `viewReplacement(orderId)`. | Returns `ownOrdersAndOpenOffers`, then `originalAndOfferedLineQuantityTotalRefundOwed`: source/new snapshots, unchanged quantity, proposed S_new, D_new=min(D_old,S_new), unchanged F/Q, T_new and ONLINE refund owed C−T_new, before an answer. Read only. |
| C2. Reviews and chooses accept or decline. | Shows the offer identity and “refund owed”, never a payout assertion. No transaction waits for this choice. |
| C3. Accepts with `acceptReplacement(orderId, offerId)` (decline uses C6). | In one transaction rechecks active Customer ownership, Order PLACED, offer belongs to Order and is the **exact open OFFERED offer**. Stale/repeated/terminal→E03. Rechecks target is still active/not archived, with active brand, listed and AVAILABLE at same hub. Invalid target→E02. |
| C4. — | Valid acceptance replaces the **whole linked line**, keeping quantity and using the **offered unit price**, even if catalogue price has changed. Sets offer ACCEPTED; Order remains PLACED. Recalculates S_new; D_new=min(D_old,S_new) without re-evaluating voucher dates/minimum/terms; F and Q unchanged; T_new=S_new−D_new+F−Q. COD payable becomes T_new. ONLINE amount stays captured C, state stays PAID, refund_amount=C−T_new. Commits all effects atomically. |
| C5. Receives `acceptedOrderAndAmounts`. | UC05-PC04. Staff can later refresh under A04. Cancellation afterwards applies full C through A05/BR-17. No path sets REFUNDED. |
| C6. Instead declines with `declineReplacement(orderId, offerId)`. | Same exact-open/own PLACED guard; atomically sets offer DECLINED, Order REJECTED, reason “customer declined replacement”, closed_at and BR-17 (COD VOIDED; ONLINE REFUND_PENDING and refund_amount=C). Returns `rejectedOrderAndAmounts`. Stale/repeat→E03; failed save→E04. End response, no implicit rejoin to confirmation. |

## Exception flows and minimum guarantee

| ID | Branch point and guard | System response | Rejoin / end |
|---|---|---|---|
| E01 | Steps 1–4/A02/A03: inactive or wrong role, wrong hub, non-PLACED, missing reason; confirm with an open offer; offer with source still available, nonmember line, invalid target or another open offer | Controlled refusal; no Order/line/payment/offer update. Own-hub privacy enforced on reads. | End request: UC05-MG01. A new read may rejoin 1/2. |
| E02 | A03 invalid target; or C3 exact open offer whose target is now ineligible | At offer creation: refusal with no writes. At acceptance: only that offer becomes WITHDRAWN with an explanatory returned/displayed reason (`withdrawnOfferAndReason`); **Order, lines and payment unchanged**. No persisted withdrawal_reason attribute is assumed. | End request: UC05-MG01. Staff can refresh 1/2 and make a new eligible offer. |
| E03 | C3/C6: wrong owner, order no longer PLACED (including CANCELLED/REJECTED), wrong/non-open offer or stale/repeated answer | Returns `staleRefusal`; zero rows changed. Ownership failure discloses no foreign order details. Never revives a terminal order. | End response: UC05-MG01; customer may read again at C1. |
| E04 | Any modifying request: lock, write or commit failure | Controlled retry outcome; atomic rollback of every intended Order/line/offer/payment change. No partial confirmation, rejection, replacement or money change. | End request: UC05-MG01. New read at 1/C1 before retry. |

Fixed contract example (not a test result): S=100,000, D=10,000, F=15,000, Q=5,000 gives T=C=100,000. Accepted replacement S_new=90,000 gives D_new=10,000 and T_new=90,000. COD payable=90,000; ONLINE keeps C=100,000 with 10,000 owed. Later cancel owes full 100,000. A delivered order retains T_new=90,000 for operational sales; the owed 10,000 is separate, never subtracted again.

Source: locked plan §3.3(1–10), §4, BR-12/15/16/17/26; Figure 2.1A–B; operations OP-02–06 and OP-17–20. Contract and Static design inputs only; no runtime results or lecturer approval claimed.
