# 2.1 Translate from Business Use Case

Author: 722I0004 · AI-assisted (Codex)

This section describes the proposed Part 2 system contract. It does not claim that planned features are already implemented. Use-case serving links below record scope coverage; Figure 2.1 owns any UML «include» or «extend» choices.

## 2.1.1 System Narrative

Author: 722I0004 · AI-assisted (Codex)

SaigonBite's proposed platform coordinates a delivery order from customer selection through a cloud kitchen and a shipper, then gives managers read-only views of the same operational records. A Customer can register as a local customer or tourist, maintain a profile and delivery addresses, browse active hubs and their brands and available items, and request a full quote for one hub and address. The quote shows the item subtotal (S), voucher discount (D), delivery fee (F), quiet-hub incentive (Q), total (T), and chosen payment method. At most one voucher can be used. Local customers require a Vietnamese mobile number and may choose COD, an e-wallet, or bank QR; tourists provide passport number, nationality and email, may use an optional phone and a hotel address label, and may choose COD or an international card. Passport information is visible only to the customer and Admin, not kitchen or shipper screens. Tourist menu translation is outside this release.

Before checkout saves anything, the system rechecks hub capacity, distance, availability, voucher validity, payment choice and the quote fingerprint. The distance shown is approximate, from hub coordinates to the delivery district's centroid; the raw value is checked before display rounding. The current team default accepts a raw distance of at most 8.0 km and refuses a greater distance; a busy hub may suggest up to three active, non-busy alternatives within range. These figures and related pricing rules are team defaults, not client-confirmed values. A busy result, out-of-range address, invalid or expired voucher, unavailable item, or changed quote does not create an order; a changed quote is shown again for consent. COD creates a pending payment. Online payment uses the team's labelled simulator, not a live provider or card processing: a decline creates no order, payment or line and lets the customer retry or switch to COD. The customer chooses approve/decline before the transaction; its short deterministic decision and all writes occur inside checkout. A failure through COMMIT releases simulated authorization and saves nothing (BR-14). If the simulator approves and the accepted quote still matches, checkout records one PLACED order with item and address snapshots, the full S/D/F/Q/T breakdown, the payment result, and one increase in hub load. Replaying the same customer's checkout token returns that customer's existing order rather than creating another.

Kitchen staff work only on orders for their own hub. For a PLACED order they can confirm it or reject it with a reason. Rejection ends the order as REJECTED and withdraws an open replacement offer; COD is voided, while an online amount is recorded as fully owed back in REFUND_PENDING. If an item becomes unavailable after placement, kitchen staff may offer one eligible replacement for a line. The customer sees the original and proposed item, quantity, revised total and any online refund owed before answering. A valid acceptance changes the line at the offered price; COD payable becomes the new total, while ONLINE remains PAID with the difference recorded as refund owed, not paid out. If the target is no longer valid, the offer is withdrawn and the order is unchanged. A decline ends the order as REJECTED with the same unfulfilled-payment handling. Kitchen staff cannot confirm or start preparation while an offer is open. Customers can track their own orders, view a receipt and cancel only while an order is PLACED or CONFIRMED. Cancellation withdraws any open offer; COD is voided and an online amount is fully owed back. Cancellation is unavailable once preparation has started.

After confirmation, kitchen staff move an order to PREPARING and then READY. Marking it ready creates a delivery waiting for pickup. An active Shipper may take an unassigned READY order; that assignment moves the order to OUT_FOR_DELIVERY. The assigned shipper records delivery completion or a failure reason. For COD, delivery is completed only when the cash collected equals T; success sets the order and delivery to DELIVERED and the payment to PAID. Failure sets the order to DELIVERY_FAILED and delivery to FAILED; the shipper returns the food, COD is voided and an online amount is fully owed back. A separate end-of-shift cash handover and office reconciliation remain outside the software scope.

Admin maintains hubs and capacity, brands, menu items and hub listings, vouchers, and user accounts; Admin can archive closed orders and retrieve their history. Hub archiving is refused while it has an open order, and catalogue changes do not alter existing order snapshots. Kitchen staff can change availability only for listings at their own hub. A Manager requests sales, current workload, or delivery-performance reports; the reports read shared records, apply the stated filters, and write no business rows. Complaint handling and refund decisions, paying out refunds, and customer ratings remain deferred core features under the proposed L3 default. This is a pending scope decision, not lecturer approval. Future loyalty, subscriptions, group orders and scheduled orders are outside the current release.

The analysis follows the locked plan's defaults while the planned lecturer clarifications remain unanswered in the preflight record. Defaults are not approvals: in particular, strict CRUD paths for every persistent class (L1), the online simulator (L2), the proposed deferral of complaint/refund/rating work (L3), and full AI disclosure (L6) must not be described as lecturer-confirmed.

## 2.1.2 Users and Their Goals

Author: 722I0004 · AI-assisted (Codex)

| User | Goals | Use cases |
|---|---|---|
| Customer — local or tourist | Register and maintain the correct customer details and addresses; browse hub-specific availability; see and accept a full price before ordering; pay by an eligible method; track orders, answer a replacement offer, view a receipt, and cancel while permitted. | UC-01; SUC-01–SUC-04 |
| Kitchen staff | See incoming orders for their own hub; confirm, reject or offer an eligible replacement; prepare orders, mark them ready, and maintain that hub's item availability. | UC-05; SUC-01, SUC-05, SUC-06 |
| Shipper | See ready work, take an unassigned delivery, record delivery and exact COD cash, or report a failure. | UC-02; SUC-01 |
| Admin | Maintain hub capacity, brands, menu items, hub listings, vouchers and staff accounts; deactivate/reactivate accounts; archive closed orders and read their history. | UC-03, UC-06; SUC-01, SUC-07–SUC-09 |
| Manager | Review operational sales, current hub workload and delivery performance from shared order and delivery records. | UC-04; SUC-01 |

## 2.1.3 List of Events

Author: 722I0004 · AI-assisted (Codex)

The 12 lifecycle rows use the exact operation names in plan §4. They are **External** events because an actor command triggers each change; the new state is the response, not an autonomous state-event handler. Voucher date boundaries are temporal conditions checked on demand. No scheduler, independent state-event handler or database actor is assumed.

| # | Event | Type | Trigger | Source | Use case | Response | Destination |
|---:|---|---|---|---|---|---|---|
| 1 | `browseHubs` / `selectHub` / `requestQuote` | External | Customer selects an address, hub and lines and asks for a quote. | Customer | UC-01 | Show active hubs, hub-specific availability and a full quote; refuse out-of-range or invalid selections; for a busy hub show eligible alternatives, possibly none. | Customer |
| 2 | Online simulator decline | External | Customer previously chooses the simulated decline outcome; confirmCheckout evaluates that deterministic decision before persistence. | Customer; Payment simulator | UC-01 | Show the decline; create no order, payment or line; allow retry or a COD choice. | Customer |
| 3 | `confirmCheckout` → order becomes PLACED | External | Customer confirms the full quote and chooses COD or ONLINE; the deterministic simulator decision and all guards are evaluated within checkout before persistence. | Customer; Payment simulator for ONLINE | UC-01 | Save one PLACED order, snapshots, S/D/F/Q/T and payment; increase hub load once, or return the existing order on same-customer replay. | Customer; Kitchen staff at the order's hub |
| 4 | `confirmOrder` → order becomes CONFIRMED | External | Kitchen staff confirms an own-hub PLACED order with no open offer. | Kitchen staff | UC-05 | Save CONFIRMED and show the updated order status. | Customer; Kitchen staff |
| 5 | `rejectOrder` → order becomes REJECTED | External | Kitchen staff rejects an own-hub PLACED order and gives a reason. | Kitchen staff | UC-05 | Save REJECTED and the reason; withdraw an open offer; void COD or record the full online refund as REFUND_PENDING. | Customer |
| 6 | `offerReplacement` → offer becomes OFFERED | External | Kitchen staff selects an eligible replacement for a currently unavailable line on an own-hub PLACED order. | Kitchen staff | UC-05 | Save one open offer with original and proposed snapshots; block confirm/preparation until it is resolved. | Customer; Kitchen staff |
| 7 | `acceptReplacement` → offer becomes ACCEPTED | External | Customer accepts the exact open offer while the order is PLACED and the target remains valid. | Customer | SUC-03; UC-05 | Apply the offered price and recalculate the order under §3.3; if the target became invalid, withdraw the offer and leave the order unchanged. | Customer; Kitchen staff |
| 8 | `declineReplacement` → order becomes REJECTED | External | Customer declines the exact open offer. | Customer | SUC-03; UC-05 | Save REJECTED; apply BR-17 to payment; reject stale or repeated answers without changing rows. | Customer |
| 9 | `cancelOrder` → order becomes CANCELLED | External | Customer cancels their own PLACED or CONFIRMED order. | Customer | SUC-04; UC-01 | Save CANCELLED, withdraw an open offer, and apply BR-17; refuse cancellation after PREPARING. | Customer; Kitchen staff |
| 10 | `startPreparing` → order becomes PREPARING | External | Kitchen staff starts an own-hub CONFIRMED order with no open offer. | Kitchen staff | SUC-05; UC-05 | Save PREPARING; refuse an order in another state or hub. | Customer; Kitchen staff |
| 11 | `markReady` → order READY; delivery AWAITING_PICKUP | External | Kitchen staff marks an own-hub PREPARING order ready. | Kitchen staff | SUC-05; UC-02 | Save READY and create its delivery as AWAITING_PICKUP. | Shipper; Customer |
| 12 | `takeDelivery` → order OUT_FOR_DELIVERY; delivery PICKED_UP | External | Active shipper takes an unassigned READY order. | Shipper | UC-02 | Assign one shipper and save pickup time; refuse a competing or repeated pickup without changing rows. | Assigned Shipper; Customer |
| 13 | `confirmDelivered` → order and delivery DELIVERED | External | Assigned shipper records successful delivery; COD cash, if applicable, equals T. | Assigned Shipper | UC-02 | Save DELIVERED and finish time; set COD PAID only for the exact amount. | Customer; Manager's reports |
| 14 | `reportFailure` → order DELIVERY_FAILED; delivery FAILED | External | Assigned shipper reports a failed delivery with a reason. | Assigned Shipper | UC-02 | Save failure reason and finish time; apply BR-17; refuse wrong-shipper or repeated completion without changes. | Customer; Manager's reports |
| 15 | `logIn` / `logOut`; `registerCustomer` / `updateProfile` / address management | External | A human actor authenticates or ends a session; a Customer registers or changes their own profile/address. | Human actor; Customer | SUC-01; SUC-02 | Establish or end the role session; validate Local/Tourist fields and save only the customer's own records. | Requesting actor; Customer |
| 16 | `viewMyOrders` / `viewReceipt` / `viewReplacement` | External | Customer requests only their own order history, receipt or open offer details. | Customer | SUC-03; UC-01; UC-05 | Show authorized status, receipt fields, or replacement comparison and amount owed; deny another customer's order. | Customer |
| 17 | Hub, capacity, catalogue and listing maintenance | External | Admin changes a hub or catalogue/listing; Kitchen staff changes availability at their own hub. | Admin; Kitchen staff | UC-03; UC-06; SUC-06 | Save valid changes; refuse hub archive with open orders; preserve order snapshots and restrict kitchen availability changes to the actor's hub. | Admin; Kitchen staff; affected customer browsing/checkout |
| 18 | Voucher, user-account and closed-order maintenance | External | Admin creates/updates/archives a voucher or account, changes account status, or archives/retrieves a closed order. | Admin | SUC-07; SUC-08; SUC-09 | Apply BR-08, BR-12, BR-25 and terminal-order guards; preserve authorized archived history. | Admin; Customer or staff on their next request |
| 19 | Voucher `valid_from` / `valid_until` boundary | Temporal | A quote, checkout or Admin voucher request arrives on a relevant Vietnam calendar date. | Vietnam calendar date | UC-01; SUC-07 | Check inclusive validity on demand; an invalid voucher is refused for that request. No scheduled job or automatic state change runs. | Customer; Admin |
| 20 | `salesReport` / `workloadReport` / `deliveryReport` | External | Manager requests a report with permitted filters. | Manager | UC-04 | Return the read-only operational figures or a controlled filter/access response; write no business rows. | Manager |

## 2.1.4 List of Actors

Author: 722I0004 · AI-assisted (Codex)

| Actor | Description |
|---|---|
| Customer | General actor for a person using the customer-facing functions; it is specialized into Local customer and Tourist customer, which inherit the Customer goals. |
| Local customer | A Customer who must register a Vietnamese mobile number and may pay COD, by e-wallet, or by bank QR. |
| Tourist customer | A Customer who registers passport number, nationality and email, may provide a phone and label an address as a hotel, and may pay COD or by international card. Passport details are withheld from kitchen and shipper views. |
| Kitchen staff | An authenticated worker assigned to a hub; may view and change orders only for that hub and may set its listing availability. |
| Shipper | An active delivery worker who may take any unassigned READY order; only the assigned shipper may complete it or report its failure. |
| Admin | An authenticated administrator responsible for hub, catalogue, voucher and user-account maintenance and closed-order archiving. |
| Manager | An authenticated read-only report user for sales, workload and delivery performance. |
| Payment simulator | An external system boundary representing the team's deterministic online-payment stub. It returns approve or decline for an eligible option; it is not a live provider and does not process real card data or real funds. |

There is no time-based actor: voucher dates are checked on demand and no scheduler performs expiry work. Office staff are not actors in this release because complaint/refund decisions and cash reconciliation are outside the proposed system scope; the deferral of complaint and refund features remains pending L3, not approved.

## 2.1.5 List of Use Cases and Ownership

Author: 722I0004 · AI-assisted (Codex)

The proposal-owner column preserves the six use-case selections made in the proposal. The actual-author column records the work completed for this Part 2 analysis. The six artifacts in this section are authored by 722I0004; this does not claim work by another team member. Use-case serving links are coverage references only; see Figure 2.1 for any UML relationship choices.

| ID | Use case | Main actor | Group | Short description | Proposal owner | Actual author |
|---|---|---|---|---|---|---|
| UC-01 | Place an order with an accepted full price, voucher and payment choice | Customer | (a) Ordering | Select a hub, available lines and address; review the full price and place only after accepting it and the permitted payment result. | 722I0004 | 722I0004 |
| UC-02 | Deliver an order: pick up, deliver with cash collection, or report failure | Shipper | (b) Fulfilment | Take a READY delivery, record successful delivery and exact cash when due, or report a failure reason. | 523K0049 | 722I0004 |
| UC-03 | Maintain hubs and kitchen capacity | Admin | (c) CRUD management | Create, read, update and archive hubs under the open-order guard; maintain capacity used by ordering decisions. | 722I0004 | 722I0004 |
| UC-04 | Produce management reports: sales, workload, delivery performance | Manager | (d) Reports | Read operational sales, current workload and delivery-performance reports from shared records. | 523K0049 | 722I0004 |
| UC-05 | Decide an incoming order: confirm, reject, or offer a replacement the customer agrees to | Kitchen staff | (b) Fulfilment | Decide an own-hub PLACED order; when a line is unavailable, offer an eligible replacement for the customer's decision. | 523K0050 | 722I0004 |
| UC-06 | Maintain brands, menu items and hub listings | Admin | (c) CRUD management | Maintain brands, items and per-hub listings while preserving order snapshots. | 523K0050 | 722I0004 |

**Group coverage:** (a) Ordering — UC-01; (b) Fulfilment — UC-02 and UC-05; (c) CRUD management — UC-03 and UC-06; (d) Reports — UC-04.

| Supporting UC | Goal | Actor | Main UC served | Actual author |
|---|---|---|---|---|
| SUC-01 Log in / log out | Establish or end the role-based session used by human actors. | All human actors | UC-01–UC-06 | 722I0004 |
| SUC-02 Register (local or tourist), edit profile, manage addresses | Maintain the customer subtype's own registration details, profile and delivery addresses. | Customer | UC-01 | 722I0004 |
| SUC-03 Track my orders, view receipt, answer a replacement offer | Read own orders and receipts and answer an exact open replacement offer. | Customer | UC-01; UC-05 | 722I0004 |
| SUC-04 Cancel an order (PLACED or CONFIRMED) | Cancel the customer's own order before preparation starts. | Customer | UC-01 | 722I0004 |
| SUC-05 Start preparing and mark ready | Move a confirmed own-hub order through preparation to READY and create its pickup delivery. | Kitchen staff | UC-05; UC-02 | 722I0004 |
| SUC-06 Set menu availability at my hub | Change availability of a listing at the kitchen staff member's own hub. | Kitchen staff | UC-05; UC-06 | 722I0004 |
| SUC-07 Maintain vouchers | Create, read, update and archive vouchers used by checkout. | Admin | UC-01 | 722I0004 |
| SUC-08 Maintain user accounts; deactivate/reactivate | Maintain authorized staff accounts and active status. | Admin | UC-01–UC-06 | 722I0004 |
| SUC-09 Archive closed orders; read archived history | Hide terminal orders from operational lists while retaining authorized historical access. | Admin | UC-04 | 722I0004 |

