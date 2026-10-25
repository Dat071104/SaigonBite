## 4.3.2 Modifying Sequence Diagrams

Author: 722I0004 · AI-assisted (Codex)

The following eight operations expand the corresponding report III design sequences with the actual DAO responsibilities and the database resource. Their SSD operation names, parameter strings and occurrence pointers are unchanged. Each set of Parts A–… is one request; a continuation does not start another operation or a new transaction. Focused plates retain the actor, view and controller, show the relevant domain/helper/value lifelines, and add the relevant DAOs and `:Database`. This resource is not an application class. Mechanical object loading is scoped in the responsibility table below so the high-risk writes remain readable.

The baseline is committed application `C0 = 45ac76221b0a103174c7c01d17577e6e49cfd665`. `MATCH` means static correspondence at that baseline. A dagger (`†`) marks `P4-TARGET` or `GAP`, with specific F-/P2-/P3 input IDs on each figure. The diagrams specify the target design where the draft differs; they provide no runtime, transaction-race, payment, numerical-report or test qualification.

For writes, the transaction extends from `BEGIN IMMEDIATE` to successful `COMMIT`, including all intended DAO writes. Every conditional DAO boolean is checked by the controller or its named helper. A guard failure, zero rowcount or false save result stops subsequent writes and rolls back the active transaction. A write or COMMIT error rolls back if a transaction remains active. A failed BEGIN does not trigger an unconditional ROLLBACK. An exhausted `database is locked` outcome produces **“Busy, please retry; nothing was changed”**. P2-S13/P3-S03 keep incomplete controller/helper and commit-failure handling marked as targets. The summary band on every write plate is a key for the entire request; the arrows show where its actions actually occur.

P2-S12 remains a connection-configuration target: `foreign_keys=ON`, `journal_mode=WAL`, `synchronous=NORMAL`, and `busy_timeout=10000` on each connection, as specified in plan §5.2. These settings are not asserted as observed at runtime. No user interaction or external request occurs while a write lock is held; the checkout simulator decision is a short deterministic local call.

**Responsibility table and mechanical-read scope**

| UC / SSD operation | Real controller and transaction | Focused persistence work | Mechanical reads retained by reference | PC/MG |
|---|---|---|---|---|
| UC-01 / `confirmCheckout` | `PlaceOrderController.confirm_order`; BEGIN IMMEDIATE | Token read before authorization; current quote eligibility; order/line/payment INSERTs; release through COMMIT failure. | UserDAO.get_by_id and CustomerDAO.get_by_user_id for authentication/customer mapping; VoucherDAO and HubDAO helpers inside _build_quote; OrderDAO._load line loading and PaymentDAO.get_by_order_id / HubDAO.get_including_archived in _confirmation. list_active/active_loads serve busy suggestions; no auto-resubmission. | UC01-PC01; UC01-PC02; UC01-PC03; UC01-PC04; UC01-PC05; UC01-PC06; UC01-MG01; UC01-MG02; UC01-MG03 |
| UC-02 / `takeDelivery` | `DeliveryController.pick_up`; BEGIN IMMEDIATE | DeliveryDAO.take and OrderDAO.change_state; both rowcounts checked. | UserDAO.get_by_id via BaseController; _delivery uses DeliveryDAO; get_delivery uses OrderDAO._load, PaymentDAO.get_by_order_id, HubDAO.get_including_archived, CustomerDAO.get for committed DeliveryView. | UC02-PC01; UC02-MG01 |
| UC-02 / `confirmDelivered` | `DeliveryController.confirm_delivered`; BEGIN IMMEDIATE | COD PaymentDAO.change_state, DeliveryDAO.finish and OrderDAO.change_state; all checked. | UserDAO.get_by_id and OrderDAO.get_by_id/_load guard reads; committed get_delivery loads hub, customer, payment and lines for DeliveryView. | UC02-PC02; UC02-MG01 |
| UC-03 / `archiveHub` | `HubController.archive_hub`; BEGIN IMMEDIATE | HubDAO.open_order_count and conditional HubDAO.archive; nullable archive flag. | UserDAO.get_by_id via _require_admin; get_including_archived retains authorised historical display. | UC03-PC02; UC03-MG01 |
| UC-04 / `salesReport` | `ReportController.sales_report`; read | ReportDAO.sales_by_hub / top_items SELECTs; no business writes on any branch. | UserDAO.get_by_id via BaseController; HubDAO.get_including_archived via _hub; filter-panel all_hubs performs a read only. | UC04-PC01; UC04-MG01; UC04-MG02 |
| UC-05 / `rejectOrder` | `KitchenController.reject_order`; BEGIN IMMEDIATE | Order rejection, open-offer withdrawal, full captured-C obligation and payment state saved together. | UserDAO.get_by_id via _require_staff; OrderDAO._load line snapshots via _hub_order; no historical rows deleted. | UC05-PC02 |
| UC-05 / `acceptReplacement` | `OrderTrackingController.answer_replacement`; BEGIN IMMEDIATE | Exact offer and target recheck; committed invalid-target withdrawal OR atomic valid line/totals/payment/offer acceptance. | UserDAO and CustomerDAO authenticate owner; OrderDAO._load snapshots; committed get_order uses DeliveryDAO.get_by_order_id, HubDAO.get_including_archived, PaymentDAO.get_by_order_id and ReplacementOfferDAO.list_for_order. | UC05-PC04; UC05-MG01 |
| UC-06 / `updateMenuItem` | `MenuController.update_item`; BEGIN IMMEDIATE | MenuDAO duplicate query and conditional update_item; no order_line write. | UserDAO.get_by_id via _require_admin; _active_item uses MenuDAO.get_item; _parse_item validates current parent and fields; final get_item is a read. | UC06-PC01; UC06-MG01; UC06-MG02 |

DAO details are expanded from the AST inventory, not executed. The full per-operation DAO call list and read/write table scope remain in `docs/part2/design/operation_realisation.csv`. Calls nested in a helper are labelled with that helper; omitted SELECTs do not imply omitted ownership, role, state or catalogue guards. Short SQL notes state statement kind, table and predicate only; full SQL/code excerpts belong to P7.

**UC-01 — confirmCheckout (`OP-01`)**

A new token revalidates the owner/address, active hub and catalogue, current load/capacity, quantities, voucher and raw distance inside the write transaction. `Quote.fingerprint(payment.method, payment.option)` takes the pure-domain enums carried by the real `PaymentChoice` fields. Both full fingerprint and T must match consent (F-07); the F-04 radius/fee decision uses raw distance. An own-token replay returns the existing order without authorization, repricing or insertion; a foreign token is refused without disclosure. ONLINE decline saves zero Order/Line/Payment rows. Successful checkout inserts one order header, its N snapshots and one payment; it does not simulate a conditional state UPDATE. COD is PENDING, ONLINE is PAID with C=T. P2-S05 releases authorization on every later failure through COMMIT. UC01-PC01…PC06 and MG01…MG03 are the contract anchors.

SSD parameters: `hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?, simulatorOutcome?, quoteFingerprint, quotedTotal, checkoutToken`. Occurrence: `models/UC-01/ssd_uc01_PartB.drawio#01S-M04`.

![Figure 4.3.2.1.OP-01.A — confirmCheckout Part A](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartA.png)

Figure 4.3.2.1.OP-01.A. UC-01 confirmCheckout — Part A — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartA.drawio); vector: [SVG](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartA.svg).

![Figure 4.3.2.1.OP-01.B — confirmCheckout Part B](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartB.png)

Figure 4.3.2.1.OP-01.B. UC-01 confirmCheckout — Part B — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartB.drawio); vector: [SVG](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartB.svg).

![Figure 4.3.2.1.OP-01.C — confirmCheckout Part C](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartC.png)

Figure 4.3.2.1.OP-01.C. UC-01 confirmCheckout — Part C — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartC.drawio); vector: [SVG](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartC.svg).

![Figure 4.3.2.1.OP-01.D — confirmCheckout Part D](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartD.png)

Figure 4.3.2.1.OP-01.D. UC-01 confirmCheckout — Part D — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartD.drawio); vector: [SVG](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartD.svg).

![Figure 4.3.2.1.OP-01.E — confirmCheckout Part E](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartE.png)

Figure 4.3.2.1.OP-01.E. UC-01 confirmCheckout — Part E — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartE.drawio); vector: [SVG](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartE.svg).

![Figure 4.3.2.1.OP-01.F — confirmCheckout Part F](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartF.png)

Figure 4.3.2.1.OP-01.F. UC-01 confirmCheckout — Part F — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartF.drawio); vector: [SVG](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartF.svg).

![Figure 4.3.2.1.OP-01.G — confirmCheckout Part G](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartG.png)

Figure 4.3.2.1.OP-01.G. UC-01 confirmCheckout — Part G — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartG.drawio); vector: [SVG](../../../models/UC-01/seqdao_uc01_confirmCheckout_PartG.svg).

**UC-02 — takeDelivery (`OP-10`)**

The active shipper checks the live delivery is unassigned/AWAITING_PICKUP and the order is READY. DeliveryDAO.take uses the actual AWAITING_PICKUP predicate; a true rowcount result is required before the paired READY→OUT_FOR_DELIVERY save. Any later failure rolls back the pickup as well. Only one competing take may commit; this is a design guarantee to test in P4, not a measured race result. No additional one-active-delivery rule is introduced.

SSD parameters: `orderId`. Occurrence: `models/UC-02/ssd_uc02_PartA.drawio#M03`.

![Figure 4.3.2.2.OP-10.A — takeDelivery Part A](../../../models/UC-02/seqdao_uc02_takeDelivery_PartA.png)

Figure 4.3.2.2.OP-10.A. UC-02 takeDelivery — Part A — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_takeDelivery_PartA.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_takeDelivery_PartA.svg).

![Figure 4.3.2.2.OP-10.B — takeDelivery Part B](../../../models/UC-02/seqdao_uc02_takeDelivery_PartB.png)

Figure 4.3.2.2.OP-10.B. UC-02 takeDelivery — Part B — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_takeDelivery_PartB.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_takeDelivery_PartB.svg).

![Figure 4.3.2.2.OP-10.C — takeDelivery Part C](../../../models/UC-02/seqdao_uc02_takeDelivery_PartC.png)

Figure 4.3.2.2.OP-10.C. UC-02 takeDelivery — Part C — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_takeDelivery_PartC.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_takeDelivery_PartC.svg).

![Figure 4.3.2.2.OP-10.D — takeDelivery Part D](../../../models/UC-02/seqdao_uc02_takeDelivery_PartD.png)

Figure 4.3.2.2.OP-10.D. UC-02 takeDelivery — Part D — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_takeDelivery_PartD.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_takeDelivery_PartD.svg).

![Figure 4.3.2.2.OP-10.E — takeDelivery Part E](../../../models/UC-02/seqdao_uc02_takeDelivery_PartE.png)

Figure 4.3.2.2.OP-10.E. UC-02 takeDelivery — Part E — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_takeDelivery_PartE.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_takeDelivery_PartE.svg).

**UC-02 — confirmDelivered (`OP-11`)**

Only the assigned shipper may finish a PICKED_UP delivery paired with an OUT_FOR_DELIVERY order. COD cash must equal T; the PENDING→PAID update is conditional and checked. ONLINE accepts no cash and preserves captured C and any partial refund owed. DeliveryDAO.finish checks order_id, assigned shipper_id and PICKED_UP. The paired order update, finish and any COD write commit together; a zero result on any one reverses prior writes.

SSD parameters: `orderId, cashCollected?`. Occurrence: `models/UC-02/ssd_uc02_PartB.drawio#M04`.

![Figure 4.3.2.2.OP-11.A — confirmDelivered Part A](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartA.png)

Figure 4.3.2.2.OP-11.A. UC-02 confirmDelivered — Part A — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartA.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartA.svg).

![Figure 4.3.2.2.OP-11.B — confirmDelivered Part B](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartB.png)

Figure 4.3.2.2.OP-11.B. UC-02 confirmDelivered — Part B — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartB.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartB.svg).

![Figure 4.3.2.2.OP-11.C — confirmDelivered Part C](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartC.png)

Figure 4.3.2.2.OP-11.C. UC-02 confirmDelivered — Part C — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartC.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartC.svg).

![Figure 4.3.2.2.OP-11.D — confirmDelivered Part D](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartD.png)

Figure 4.3.2.2.OP-11.D. UC-02 confirmDelivered — Part D — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartD.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartD.svg).

![Figure 4.3.2.2.OP-11.E — confirmDelivered Part E](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartE.png)

Figure 4.3.2.2.OP-11.E. UC-02 confirmDelivered — Part E — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartE.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartE.svg).

![Figure 4.3.2.2.OP-11.F — confirmDelivered Part F](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartF.png)

Figure 4.3.2.2.OP-11.F. UC-02 confirmDelivered — Part F — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartF.drawio); vector: [SVG](../../../models/UC-02/seqdao_uc02_confirmDelivered_PartF.svg).

**UC-03 — archiveHub (`OP-36`)**

Only an active admin may archive. The same write lock covers the open-order count and archive. Any order outside DELIVERED, DELIVERY_FAILED, REJECTED or CANCELLED blocks it. HubDAO.archive uses `id` plus `archived_at IS NULL`; the design does not invent an archive enum or a WHERE-state predicate. A successful archive hides operational access while preserving orders, receipts and authorised history (UC03-PC02/MG01).

SSD parameters: `hubId`. Occurrence: `models/UC-03/ssd_uc03.drawio#M03-05`.

![Figure 4.3.2.3.OP-36.A — archiveHub Part A](../../../models/UC-03/seqdao_uc03_archiveHub_PartA.png)

Figure 4.3.2.3.OP-36.A. UC-03 archiveHub — Part A — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-03/seqdao_uc03_archiveHub_PartA.drawio); vector: [SVG](../../../models/UC-03/seqdao_uc03_archiveHub_PartA.svg).

![Figure 4.3.2.3.OP-36.B — archiveHub Part B](../../../models/UC-03/seqdao_uc03_archiveHub_PartB.png)

Figure 4.3.2.3.OP-36.B. UC-03 archiveHub — Part B — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-03/seqdao_uc03_archiveHub_PartB.drawio); vector: [SVG](../../../models/UC-03/seqdao_uc03_archiveHub_PartB.svg).

![Figure 4.3.2.3.OP-36.C — archiveHub Part C](../../../models/UC-03/seqdao_uc03_archiveHub_PartC.png)

Figure 4.3.2.3.OP-36.C. UC-03 archiveHub — Part C — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-03/seqdao_uc03_archiveHub_PartC.drawio); vector: [SVG](../../../models/UC-03/seqdao_uc03_archiveHub_PartC.svg).

![Figure 4.3.2.3.OP-36.D — archiveHub Part D](../../../models/UC-03/seqdao_uc03_archiveHub_PartD.png)

Figure 4.3.2.3.OP-36.D. UC-03 archiveHub — Part D — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-03/seqdao_uc03_archiveHub_PartD.drawio); vector: [SVG](../../../models/UC-03/seqdao_uc03_archiveHub_PartD.svg).

**UC-04 — salesReport (`OP-26`)**

UC04-MG01 applies to success, empty output, Manager denial (UC04-MG02), invalid filters and read failures: no business data is written. ReportDAO.sales_by_hub selects DELIVERED orders by delivery finish time in the half-open UTC range derived from Vietnam calendar days; archived records remain included. Order-level sums have no order_line join. F-03 makes operational sales T, with refunds owed shown separately. F-09 makes item identity menu_item_id and retains it through SalesReport.top_items; a snapshot name is only a display label. Period, SalesRow and SalesReport are non-persisted values. No computed metric is claimed to pass an oracle.

SSD parameters: `startDateVN, endDateVN, hubId?`. Occurrence: `models/UC-04/ssd_uc04.drawio#M01`.

![Figure 4.3.2.4.OP-26.A — salesReport Part A](../../../models/UC-04/seqdao_uc04_salesReport_PartA.png)

Figure 4.3.2.4.OP-26.A. UC-04 salesReport — Part A — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-04/seqdao_uc04_salesReport_PartA.drawio); vector: [SVG](../../../models/UC-04/seqdao_uc04_salesReport_PartA.svg).

![Figure 4.3.2.4.OP-26.B — salesReport Part B](../../../models/UC-04/seqdao_uc04_salesReport_PartB.png)

Figure 4.3.2.4.OP-26.B. UC-04 salesReport — Part B — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-04/seqdao_uc04_salesReport_PartB.drawio); vector: [SVG](../../../models/UC-04/seqdao_uc04_salesReport_PartB.svg).

![Figure 4.3.2.4.OP-26.C — salesReport Part C](../../../models/UC-04/seqdao_uc04_salesReport_PartC.png)

Figure 4.3.2.4.OP-26.C. UC-04 salesReport — Part C — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-04/seqdao_uc04_salesReport_PartC.drawio); vector: [SVG](../../../models/UC-04/seqdao_uc04_salesReport_PartC.svg).

![Figure 4.3.2.4.OP-26.D — salesReport Part D](../../../models/UC-04/seqdao_uc04_salesReport_PartD.png)

Figure 4.3.2.4.OP-26.D. UC-04 salesReport — Part D — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-04/seqdao_uc04_salesReport_PartD.drawio); vector: [SVG](../../../models/UC-04/seqdao_uc04_salesReport_PartD.svg).

**UC-05 — rejectOrder (`OP-03`)**

Own-hub PLACED order and valid reason precede rejection. A conditional order transition, optional exact open-offer withdrawal, checked PaymentDAO.set_amounts target and conditional payment state save share one transaction. F-02/P2-S01 persist full captured C as the ONLINE refund obligation even after an earlier partial obligation; COD becomes VOIDED and ONLINE becomes REFUND_PENDING. The operation records an obligation and performs no payout. A zero rowcount on a later payment or offer save rolls back the intended rejection too.

SSD parameters: `orderId, reason`. Occurrence: `models/UC-05/ssd_uc05_PartA.drawio#05S-M04`.

![Figure 4.3.2.5.OP-03.A — rejectOrder Part A](../../../models/UC-05/seqdao_uc05_rejectOrder_PartA.png)

Figure 4.3.2.5.OP-03.A. UC-05 rejectOrder — Part A — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_rejectOrder_PartA.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_rejectOrder_PartA.svg).

![Figure 4.3.2.5.OP-03.B — rejectOrder Part B](../../../models/UC-05/seqdao_uc05_rejectOrder_PartB.png)

Figure 4.3.2.5.OP-03.B. UC-05 rejectOrder — Part B — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_rejectOrder_PartB.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_rejectOrder_PartB.svg).

![Figure 4.3.2.5.OP-03.C — rejectOrder Part C](../../../models/UC-05/seqdao_uc05_rejectOrder_PartC.png)

Figure 4.3.2.5.OP-03.C. UC-05 rejectOrder — Part C — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_rejectOrder_PartC.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_rejectOrder_PartC.svg).

![Figure 4.3.2.5.OP-03.D — rejectOrder Part D](../../../models/UC-05/seqdao_uc05_rejectOrder_PartD.png)

Figure 4.3.2.5.OP-03.D. UC-05 rejectOrder — Part D — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_rejectOrder_PartD.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_rejectOrder_PartD.svg).

![Figure 4.3.2.5.OP-03.E — rejectOrder Part E](../../../models/UC-05/seqdao_uc05_rejectOrder_PartE.png)

Figure 4.3.2.5.OP-03.E. UC-05 rejectOrder — Part E — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_rejectOrder_PartE.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_rejectOrder_PartE.svg).

![Figure 4.3.2.5.OP-03.F — rejectOrder Part F](../../../models/UC-05/seqdao_uc05_rejectOrder_PartF.png)

Figure 4.3.2.5.OP-03.F. UC-05 rejectOrder — Part F — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_rejectOrder_PartF.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_rejectOrder_PartF.svg).

**UC-05 — acceptReplacement (`OP-05`)**

Ownership, PLACED state and exact open OFFERED offer are checked before target eligibility is rechecked (F-05). A stale/guard mismatch refuses unchanged. An invalid target intentionally saves only that exact offer as WITHDRAWN, checks the DAO boolean, then COMMITs; Order/Line/Payment stay unchanged. A failed withdrawal is rolled back. A valid branch uses the offered price/name for the whole line with unchanged quantity; Dnew=min(Dold,Snew), F/Q unchanged, and Tnew recomputed. COD payable becomes Tnew; ONLINE captured C stays unchanged with refund owed C−Tnew and state PAID. Checked line/header saves (P2-S09/S11), checked payment amounts and exact OFFERED→ACCEPTED all precede COMMIT. Order remains PLACED with no automatic confirmation. F-02, F-05, P2-S09/S11/S13 and P3-S03 remain explicit targets.

SSD parameters: `orderId, offerId`. Occurrence: `models/UC-05/ssd_uc05_PartB.drawio#05S-M08`.

![Figure 4.3.2.5.OP-05.A — acceptReplacement Part A](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartA.png)

Figure 4.3.2.5.OP-05.A. UC-05 acceptReplacement — Part A — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartA.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartA.svg).

![Figure 4.3.2.5.OP-05.B — acceptReplacement Part B](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartB.png)

Figure 4.3.2.5.OP-05.B. UC-05 acceptReplacement — Part B — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartB.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartB.svg).

![Figure 4.3.2.5.OP-05.C — acceptReplacement Part C](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartC.png)

Figure 4.3.2.5.OP-05.C. UC-05 acceptReplacement — Part C — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartC.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartC.svg).

![Figure 4.3.2.5.OP-05.D — acceptReplacement Part D](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartD.png)

Figure 4.3.2.5.OP-05.D. UC-05 acceptReplacement — Part D — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartD.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartD.svg).

![Figure 4.3.2.5.OP-05.E — acceptReplacement Part E](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartE.png)

Figure 4.3.2.5.OP-05.E. UC-05 acceptReplacement — Part E — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartE.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartE.svg).

![Figure 4.3.2.5.OP-05.F — acceptReplacement Part F](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartF.png)

Figure 4.3.2.5.OP-05.F. UC-05 acceptReplacement — Part F — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartF.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartF.svg).

![Figure 4.3.2.5.OP-05.G — acceptReplacement Part G](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartG.png)

Figure 4.3.2.5.OP-05.G. UC-05 acceptReplacement — Part G — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartG.drawio); vector: [SVG](../../../models/UC-05/seqdao_uc05_acceptReplacement_PartG.svg).

**UC-06 — updateMenuItem (`OP-41`)**

The admin edits name, description and valid positive price after active-item and duplicate checks. The parent is current.brand_id; the posted brandId is context and cannot reparent a dish. MenuDAO.update_item has the actual `id AND archived_at IS NULL` predicate and returns rowcount==1. The target controller must check it. The only write is to menu_item; existing order_line name/price/quantity snapshots remain unchanged (UC06-MG01). Invalid prices and duplicates refuse without a write (UC06-MG02).

SSD parameters: `itemId, brandId, name, description, price`. Occurrence: `models/UC-06/ssd_uc06_PartB.drawio#M06-B03`.

![Figure 4.3.2.6.OP-41.A — updateMenuItem Part A](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartA.png)

Figure 4.3.2.6.OP-41.A. UC-06 updateMenuItem — Part A — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartA.drawio); vector: [SVG](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartA.svg).

![Figure 4.3.2.6.OP-41.B — updateMenuItem Part B](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartB.png)

Figure 4.3.2.6.OP-41.B. UC-06 updateMenuItem — Part B — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartB.drawio); vector: [SVG](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartB.svg).

![Figure 4.3.2.6.OP-41.C — updateMenuItem Part C](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartC.png)

Figure 4.3.2.6.OP-41.C. UC-06 updateMenuItem — Part C — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartC.drawio); vector: [SVG](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartC.svg).

![Figure 4.3.2.6.OP-41.D — updateMenuItem Part D](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartD.png)

Figure 4.3.2.6.OP-41.D. UC-06 updateMenuItem — Part D — Author: 722I0004 · AI-assisted (Codex).
Editable source: [draw.io](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartD.drawio); vector: [SVG](../../../models/UC-06/seqdao_uc06_updateMenuItem_PartD.svg).

**Validation boundary and reproducibility**

Each figure has an adjacent standalone Python generator and JSON metadata. The generator reads the sole reviewed shared model, refreshes call daggers from its explicit statuses, and refuses changed signatures until an explicit reviewed alias/lane refresh. It clears behavior-target daggers only after the operation and selected methods have explicit MATCH status; a matching name/signature alone never qualifies behavior. Re-run a figure with the bundled Python `-X utf8 -I <figure.py>`. No application module is imported.

All plates use a 1600 × 1250 landscape canvas placed at 230 mm, with 24 px minimum text (9.78 pt). Native XML font sizes/styles agree with the SVG; author labels exist in the editable sources. Own-file QA parses XML, resolves receiver members against the shared model, checks exact SSD identity, validates actual edge attachments and label bounds, and checks visible transaction/rowcount/busy labels. Every PNG and independently rasterized SVG is opened for visual inspection; physical A4 proofs and hash receipts are retained outside the repository in `Part2/notes/P3-F/`. Native draw.io editing and final DOCX/PDF placement remain UNTESTED.
