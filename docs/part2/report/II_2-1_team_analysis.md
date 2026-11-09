# 2.1 Translate from Business Use Case

Author: 722I0004 · AI-assisted (Codex)

This section describes the proposed Part 2 system contract. It does not claim that planned features are already implemented. Use-case serving links below record scope coverage; Figure 2.1 owns any UML «include» or «extend» choices.

## 2.1.1 System Narrative

Author: 722I0004 · AI-assisted (Codex)

SaigonBite's proposed platform coordinates a delivery order from customer selection through a cloud kitchen and a shipper, then gives managers read-only views of the same operational records. A Customer can register as a local customer or tourist, maintain a profile and delivery addresses, browse active hubs and their brands and available items, and request a full quote for one hub and address. The quote shows the item subtotal (S), voucher discount (D), delivery fee (F), quiet-hub incentive (Q), total (T), and chosen payment method. At most one voucher can be used. Local customers require a Vietnamese mobile number and may choose COD, an e-wallet, or bank QR; tourists provide passport number, nationality and email, may use an optional phone and a hotel address label, and may choose COD or an international card. Passport information is visible only to the customer and Admin, not kitchen or shipper screens. Tourist menu translation is outside this release.

Before checkout saves anything, the system rechecks hub capacity, distance, availability, voucher validity, payment choice and the quote fingerprint. The distance shown is approximate, from hub coordinates to the delivery district's centroid; the raw value is checked before display rounding. The current team default accepts a raw distance of at most 8.0 km and refuses a greater distance; a busy hub may suggest up to three active, non-busy alternatives within range. These figures and related pricing rules are team defaults, not client-confirmed values. A busy result, out-of-range address, invalid or expired voucher, unavailable item, or changed quote does not create an order; a changed quote is shown again for consent. COD creates a pending payment. Online payment uses the team's labelled simulator, not a live provider or card processing: a decline creates no order, payment or line and lets the customer retry or switch to COD. The customer chooses approve/decline before the transaction; its short deterministic decision and all writes occur inside checkout. A failure through COMMIT releases simulated authorization and saves nothing (BR-14). If the simulator approves and the accepted quote still matches, checkout records one PLACED order with item and address snapshots, the full S/D/F/Q/T breakdown, the payment result, and one increase in hub load. Replaying the same customer's checkout token returns that customer's existing order rather than creating another.

Kitchen staff work only on orders for their own hub. For a PLACED order they can confirm it or reject it with a reason. Rejection ends the order as REJECTED and withdraws an open replacement offer; COD is voided, while an online amount is recorded as fully owed back in REFUND_PENDING. If an item becomes unavailable after placement, kitchen staff may offer one eligible replacement for a line. The customer sees the original and proposed item, quantity, revised total and any online refund owed before answering. A valid acceptance changes the line at the offered price; COD payable becomes the new total, while ONLINE remains PAID with the difference recorded as refund owed, not paid out. If the target is no longer valid, the offer is withdrawn and the order is unchanged. A decline ends the order as REJECTED with the same unfulfilled-payment handling. Kitchen staff cannot confirm or start preparation while an offer is open. Customers can track their own orders, view a receipt and cancel only while an order is PLACED or CONFIRMED. Cancellation withdraws any open offer; COD is voided and an online amount is fully owed back. Cancellation is unavailable once preparation has started.

After confirmation, kitchen staff move an order to PREPARING and then READY. Marking it ready creates a delivery waiting for pickup. An active Shipper may take an unassigned READY order; that assignment moves the order to OUT_FOR_DELIVERY. The assigned shipper records delivery completion or a failure reason. For COD, delivery is completed only when the cash collected equals T; success sets the order and delivery to DELIVERED and the payment to PAID. Failure sets the order to DELIVERY_FAILED and delivery to FAILED; the shipper returns the food, COD is voided and an online amount is fully owed back. A separate end-of-shift cash handover and office reconciliation remain outside the software scope.

Admin maintains hubs and capacity, brands, menu items and hub listings, vouchers, and user accounts; Admin can archive closed orders and retrieve their history. Hub archiving is refused while it has an open order, and catalogue changes do not alter existing order snapshots. Kitchen staff can change availability only for listings at their own hub. A Manager requests sales, current workload, or delivery-performance reports; the reports read shared records, apply the stated filters, and write no business rows. Complaint handling and refund decisions, paying out refunds, and customer ratings remain deferred core features as stated in proposal A-09; L3 was accepted at the Part 1 review (no change requested). Future loyalty, subscriptions, group orders and scheduled orders are outside the current release.

The analysis follows the locked plan’s defaults. L1 needs no approval because D-4 provides running CRUD paths for every persistent class beyond the proposal; the online simulator (L2), deferred complaint/refund/rating work (L3), technology (L4) and roster (L5) were accepted at the Part 1 review (no change requested). AI-generated application code (L6) remains open because it was not declared in the Part 1 AI log; no written approval or separate confirmation is claimed.

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

Author: 722I0004 · AI-assisted (Codex, Claude)

The table lists one event per row, using the textbook classification: **external** events start outside the system (an actor does something), **temporal** events are triggered by reaching a point in time, and **state** events happen when something inside the system changes and triggers further processing. The system operation names in brackets are the SSD messages in section 2.2. The table has 27 external, 2 temporal and 3 state events.

| Event | Trigger | Source | Use case | Response | Destination | Type |
|---|---|---|---|---|---|---|
| E01 Customer registers an account | Registration form submitted | Customer | SUC-02 | Validate Local (Vietnamese mobile) or Tourist (passport, nationality, email) fields; create account and customer profile | Customer | External |
| E02 Customer updates profile or addresses | Profile or address form submitted | Customer | SUC-02 | Save own profile; add, edit or archive an address (Hotel allowed) | Customer | External |
| E03 User logs in or out | Credentials entered / logout selected | Any human actor | SUC-01 | Start a role session or end it; refuse an inactive account | User | External |
| E04 Customer browses hubs and menus | Customer opens the order page and selects a hub | Customer | UC-01 | Show active hubs with busy/quiet status and the hub's available listings (`browseHubs`, `selectHub`) | Customer | External |
| E05 Customer requests a quote | Address, items, voucher and payment chosen | Customer | UC-01 | Price items, voucher, distance fee and quiet discount; refuse out-of-range or busy hub and suggest up to three alternatives (`requestQuote`) | Customer | External |
| E06 Customer confirms checkout | Customer accepts the full quote | Customer; Payment simulator for ONLINE | UC-01 | Re-check the quote; save one PLACED order with snapshots and payment; replay returns the same order (`confirmCheckout`) | Customer; Kitchen staff of the hub | External |
| E07 Online payment is declined | Simulator returns DECLINED during checkout | Payment simulator | UC-01 | Show the decline; create no order, line or payment; allow retry or COD | Customer | External |
| E08 Customer views orders or receipt | Customer opens My orders or an order | Customer | SUC-03 | Show own order status, receipt and any amount owed; deny other customers' orders (`viewMyOrders`, `viewReceipt`) | Customer | External |
| E09 Customer cancels an order | Cancel selected while PLACED or CONFIRMED | Customer | SUC-04 | Set CANCELLED; withdraw an open offer; void COD or record online refund owed (`cancelOrder`) | Customer; Kitchen staff | External |
| E10 Kitchen confirms an order | Staff confirms an own-hub PLACED order | Kitchen staff | UC-05 | Set CONFIRMED (`confirmOrder`) | Customer | External |
| E11 Kitchen rejects an order | Staff rejects with a reason | Kitchen staff | UC-05 | Set REJECTED with reason; withdraw an open offer; settle payment (`rejectOrder`) | Customer | External |
| E12 Kitchen offers a replacement | A line is unavailable on a PLACED order | Kitchen staff | UC-05 | Save one OFFERED offer with old and new item snapshots; block confirmation (`offerReplacement`) | Customer | External |
| E13 Customer accepts a replacement | Customer accepts the open offer | Customer | SUC-03; UC-05 | Replace the line, recalculate totals, record any refund owed; withdraw if the target became invalid (`acceptReplacement`) | Customer; Kitchen staff | External |
| E14 Customer declines a replacement | Customer declines the open offer | Customer | SUC-03; UC-05 | Set offer DECLINED and order REJECTED; settle payment (`declineReplacement`) | Customer; Kitchen staff | External |
| E15 Kitchen starts preparing | Staff starts a CONFIRMED order | Kitchen staff | SUC-05 | Set PREPARING; cancellation is no longer allowed (`startPreparing`) | Customer | External |
| E16 Kitchen marks an order ready | Food is packed | Kitchen staff | SUC-05 | Set READY (`markReady`) | Shipper; Customer | External |
| E17 Kitchen changes item availability | An ingredient runs out or returns | Kitchen staff | SUC-06 | Set the own-hub listing AVAILABLE or SOLD_OUT | Customers browsing that hub | External |
| E18 Shipper takes a delivery | Shipper picks a READY order from the board | Shipper | UC-02 | Assign the shipper; order OUT_FOR_DELIVERY, delivery PICKED_UP; a competing pickup is refused (`takeDelivery`) | Shipper; Customer | External |
| E19 Shipper confirms delivery | Food handed over (cash collected for COD) | Shipper | UC-02 | Order and delivery DELIVERED; COD PAID only when cash equals the total (`confirmDelivered`) | Customer; Manager (reports) | External |
| E20 Shipper reports a failed delivery | Customer unreachable or address wrong | Shipper | UC-02 | Order DELIVERY_FAILED, delivery FAILED with reason; settle payment (`reportFailure`) | Customer; Manager (reports) | External |
| E21 Admin maintains hubs and capacity | Hub opened, changed or closed | Admin | UC-03 | Create, update or archive a hub; archive is refused while the hub has open orders (`createHub`, `updateHub`, `archiveHub`) | Admin; Customers (hub list) | External |
| E22 Admin maintains brands and menu items | Catalogue change | Admin | UC-06 | Create, rename, update or archive brands and items; old orders keep their snapshots | Admin; Customers | External |
| E23 Admin lists or unlists an item at a hub | Hub menu change | Admin | UC-06 | Create or remove the hub listing and set its availability (`listItemAtHub`, `unlistItemAtHub`, `setListingAvailability`) | Admin; Customers | External |
| E24 Admin maintains vouchers | Promotion created, changed or ended | Admin | SUC-07 | Create, update or archive a voucher | Customers at checkout | External |
| E25 Admin maintains user accounts | Staff joins or leaves | Admin | SUC-08 | Create, update, deactivate or reactivate an account; refuse deactivating a shipper with an open delivery | Affected user | External |
| E26 Admin archives a closed order | Order history clean-up | Admin | SUC-09 | Archive a terminal order; history stays readable | Admin; Manager | External |
| E27 Manager requests a report | Manager chooses a report and date range | Manager | UC-04 | Return sales, workload or delivery performance; write nothing (`salesReport`, `workloadReport`, `deliveryReport`) | Manager | External |
| E28 Voucher validity date is reached | Vietnam calendar date passes `valid_from` or `valid_until` | Calendar (time) | UC-01; SUC-07 | From that date the voucher is accepted or refused at quote and checkout | Customer | Temporal |
| E29 Time for the nightly backup | 03:00 Vietnam time (20:00 UTC) every day | Calendar (time) | Deployment (5.2) | Make an online SQLite backup, check integrity, upload it to cloud storage, keep seven local copies | Operator (backup storage) | Temporal |
| E30 Hub load reaches capacity | A checkout or capacity change makes active orders ≥ maximum | System state (hub load) | UC-01; UC-03; UC-04 | Hub shows as busy; new checkouts are refused with alternatives; workload report flags it | Customer; Manager | State |
| E31 Order becomes READY | `markReady` changes the order state | System state (order) | UC-02 | Create the delivery record AWAITING_PICKUP so the order appears on every active shipper's board | Shipper | State |
| E32 Order ends unfulfilled | Order becomes REJECTED, CANCELLED or DELIVERY_FAILED | System state (order) | UC-02; UC-05; SUC-04 | Void a COD payment or set an online payment to REFUND_PENDING with the full amount owed | Customer | State |

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

There is no time-based actor: voucher dates are checked on demand and no scheduler performs expiry work. Office staff are not actors in this release because complaint/refund decisions and cash reconciliation are outside the proposed system scope; the L3 deferral was accepted at the Part 1 review (no change requested), as stated in proposal A-09.

## 2.1.5 List of Use Cases and Ownership

Author: 722I0004 · AI-assisted (Codex)

The proposal-owner column preserves the six use-case selections made in the proposal. The actual-author column records the work completed for this Part 2 analysis. The six artifacts in this section are authored by 722I0004; this does not claim work by another team member. Use-case serving links are coverage references only; see Figure 2.1 for any UML relationship choices.

| No. | Use case | Main actor | Short description | Owner (ID) | Group | Actual author |
|---|---|---|---|---|---|---|
| UC-01 | Place an order with an accepted full price, voucher and payment choice | Customer | Select a hub, available lines and address; review the full price and place only after accepting it and the permitted payment result. | 722I0004 | (a) Ordering | 722I0004 |
| UC-02 | Deliver an order: pick up, deliver with cash collection, or report failure | Shipper | Take a READY delivery, record successful delivery and exact cash when due, or report a failure reason. | 523K0049 | (b) Fulfilment | 722I0004 |
| UC-03 | Maintain hubs and kitchen capacity | Admin | Create, read, update and archive hubs under the open-order guard; maintain capacity used by ordering decisions. | 722I0004 | (c) CRUD management | 722I0004 |
| UC-04 | Produce management reports: sales, workload, delivery performance | Manager | Read operational sales, current workload and delivery-performance reports from shared records. | 523K0049 | (d) Reports | 722I0004 |
| UC-05 | Decide an incoming order: confirm, reject, or offer a replacement the customer agrees to | Kitchen staff | Decide an own-hub PLACED order; when a line is unavailable, offer an eligible replacement for the customer's decision. | 523K0050 | (b) Fulfilment | 722I0004 |
| UC-06 | Maintain brands, menu items and hub listings | Admin | Maintain brands, items and per-hub listings while preserving order snapshots. | 523K0050 | (c) CRUD management | 722I0004 |

**Group coverage:** (a) Ordering: UC-01; (b) Fulfilment: UC-02 and UC-05; (c) CRUD management: UC-03 and UC-06; (d) Reports: UC-04.

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
