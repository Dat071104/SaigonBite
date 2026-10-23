## 1.5 Business Processes / Flowchart of Requirements

Author: 722I0004 · AI-assisted (Codex)

Figure 1.5 separates the order journey from the independent activities that keep it running. The upper path moves from customer identity and an accepted quote through the kitchen decision, preparation and delivery. Tracking remains available during the journey; its replacement-answer operation happens before kitchen confirmation, as Figure 1.6d shows. Early cancellation closes an order only while it is PLACED or CONFIRMED. Administration and management reporting are independent activities rather than mandatory steps of every order.

![Figure 1.5: Overall business process](../../../models/shared/business_process_v2.png)

**Figure 1.5. Overall business process, Part 2 scope. Author: 722I0004 · AI-assisted (Codex).** [Editable draw.io source](../../../models/shared/business_process_v2.drawio) · [SVG](../../../models/shared/business_process_v2.svg).

The Part 1 business-process source was copied into the Part 2 work area before revision. This version reorganises that source's order, kitchen, delivery, cancellation and management concepts into a readable A4 overview and a set of activity details. It retains the blue/pale-blue style, red exceptions, grey deferred work and distinct final symbols. Part 1 remains frozen. Part 2 supersedes A-08 through D-4: supporting operations are in the build scope, rather than labelled “analysed only”. These models describe the agreed scope; they do not assert that the application has passed its later implementation and test gates.

| Process responsibility | Use cases included |
|---|---|
| Customer ordering | UC-01 Place an order with an accepted full price, voucher and payment choice; SUC-01 Log in / log out; SUC-02 Register (local or tourist), edit profile, manage addresses |
| Customer follow-up | SUC-03 Track my orders, view receipt, answer a replacement offer; SUC-04 Cancel an order (PLACED or CONFIRMED) |
| Kitchen fulfilment | UC-05 Decide an incoming order: confirm, reject, or offer a replacement the customer agrees to; SUC-05 Start preparing and mark ready; SUC-06 Set menu availability at my hub |
| Delivery | UC-02 Deliver an order: pick up, deliver with cash collection, or report failure |
| Administration | UC-03 Maintain hubs and kitchen capacity; UC-06 Maintain brands, menu items and hub listings; SUC-07 Maintain vouchers; SUC-08 Maintain user accounts; deactivate/reactivate; SUC-09 Archive closed orders; read archived history |
| Management | UC-04 Produce management reports: sales, workload, delivery performance |

Grey activities remain part of the wider business picture but are not built in this release: complaints, complaint/refund decisions, refund payout and ratings (A-09 / L3). Recording a refund liability is in scope and does not execute a payout. Loyalty, subscription meals, group orders and scheduled orders remain future possibilities, not implemented functions. Cash handover and office reconciliation described in the original business context remain manual work; UC-02 records the exact cash collected at the door and does not implement a cash-settlement ledger.

## 1.6 Activity Diagram

Author: 722I0004 · AI-assisted (Codex)

The swim-lane model uses Customer, Kitchen staff, Shipper, Admin, Manager and System. The overview is a responsibility index; Parts A-G carry the executable control-flow interpretation. Only relevant lanes are repeated on a detail page. Authentication and role checks apply before each authorised activity. The payment simulator belongs to the System lane and represents no external provider integration.

![Figure 1.6: Swim-lane responsibility overview](../../../models/shared/swimlane_v2.png)

**Figure 1.6. Swim-lane responsibility overview. Author: 722I0004 · AI-assisted (Codex).** [Multi-page draw.io source](../../../models/shared/swimlane_v2.drawio) · [SVG](../../../models/shared/swimlane_v2.svg).

A filled dot starts an activity. A ring containing a dot ends the whole activity shown; the circle containing an X ends one path or unsuccessful request without implying that an existing order has closed. Administration, reports and cancellation requests are separate activities, so their final nodes do not end another activity. Continuation circles P, K, R and D transfer one selected flow between pages, rather than starting concurrent branches: P = checkout confirmation, K = a PLACED order awaiting a kitchen decision, R = an OFFERED replacement awaiting a customer response, D = a READY order available for pickup. Re-entering K after a resolved offer is an alternative continuation, not a join waiting for several inputs.

### Checkout and payment

Part A uses raw distance for the inclusive 8 km limit, then the derived hub-load classification. A refused attempt ends; a changed hub or address requires another quote, including the possibility that no alternative hub is available. The displayed distance uses a district centroid and is explicitly approximate. The customer sees subtotal S, voucher discount D, fee F, quiet concession Q and total T before confirmation (BR-01-BR-10).

![Figure 1.6a: Hub, radius and quote](../../../models/shared/swimlane_v2_PartA.png)

**Figure 1.6a. Select hub, check radius and obtain a quote. Author: 722I0004 · AI-assisted (Codex).** [draw.io](../../../models/shared/swimlane_v2_PartA.drawio) · [SVG](../../../models/shared/swimlane_v2_PartA.svg).

Part B separates a declined simulator attempt from a persisted order. Local customers may select E_WALLET or BANK_QR; tourists may select INTERNATIONAL_CARD; both may choose COD. The simulator page records a selected approve/decline result before the write transaction. Its deterministic in-process decision and all order/line/payment writes belong to the checkout transaction. Capacity, radius, voucher and the complete quote fingerprint are rechecked at confirmation. Any changed quote is shown again, without saving an order. A declined attempt creates neither an Order nor a Payment. A successful COD order starts with payment PENDING; approved ONLINE starts PAID. A commit failure releases the simulated approval and saves nothing. Replaying an accepted checkout token returns that customer's existing order rather than creating another (BR-11, BR-14).

![Figure 1.6b: Checkout and simulator](../../../models/shared/swimlane_v2_PartB.png)

**Figure 1.6b. Confirm checkout and simulated payment. Author: 722I0004 · AI-assisted (Codex).** [draw.io](../../../models/shared/swimlane_v2_PartB.drawio) · [SVG](../../../models/shared/swimlane_v2_PartB.svg).

### Kitchen decision and replacement consent

Part C restricts kitchen operations to the staff member's own hub. A rejection needs a reason. Confirmation requires no open offer; preparation starts from CONFIRMED. Marking READY creates one Delivery in AWAITING_PICKUP. Kitchen availability is per hub: AVAILABLE and SOLD_OUT belong to its listing, not to the MenuItem itself (BR-16, BR-26; plan section 4).

![Figure 1.6c: Kitchen decision and preparation](../../../models/shared/swimlane_v2_PartC.png)

**Figure 1.6c. Decide, prepare and release an order. Author: 722I0004 · AI-assisted (Codex).** [draw.io](../../../models/shared/swimlane_v2_PartC.drawio) · [SVG](../../../models/shared/swimlane_v2_PartC.svg).

Part D requires the exact open OFFERED offer on the customer's own PLACED order. The source line must currently be unavailable; its replacement keeps the quantity, differs from the source, is not already in the order, and has an equal-or-lower offered unit price. Only one open offer is permitted. Acceptance rechecks the target's active brand/item and listed, AVAILABLE status at that hub. An invalid target withdraws the offer and leaves the order unchanged. A valid answer honours the stored offered price, changes the line and total, caps the old voucher concession at the new subtotal, and preserves F and Q. ONLINE keeps captured amount C and state PAID while C minus the new T becomes refund owed. Decline produces DECLINED and REJECTED, with the full unfulfilled liability. Stale/repeated answers change nothing; a cancelled order cannot be revived. “Waiting for customer” is derived from PLACED plus an open offer, not a stored state (plan section 3.3).

![Figure 1.6d: Replacement consent](../../../models/shared/swimlane_v2_PartD.png)

**Figure 1.6d. Customer consent to a replacement. Author: 722I0004 · AI-assisted (Codex).** [draw.io](../../../models/shared/swimlane_v2_PartD.drawio) · [SVG](../../../models/shared/swimlane_v2_PartD.svg).

### Delivery and cancellation

Part E atomically assigns an unclaimed READY order to an active shipper: Order becomes OUT_FOR_DELIVERY and Delivery becomes PICKED_UP. Only that shipper can finish. A successful COD finish requires cash exactly equal to T; success sets Order and Delivery to DELIVERED and COD payment to PAID. A valid failure needs a reason and sets DELIVERY_FAILED / FAILED. Invalid cash or a missing reason leaves the order OUT_FOR_DELIVERY so another valid finish request can be made. There is no redelivery transition. The own-order receipt uses stored snapshots, shows payment state and refund owed, and labels ONLINE as simulated (BR-13, BR-25).

![Figure 1.6e: Delivery and cash](../../../models/shared/swimlane_v2_PartE.png)

**Figure 1.6e. Delivery, cash and completion. Author: 722I0004 · AI-assisted (Codex).** [draw.io](../../../models/shared/swimlane_v2_PartE.drawio) · [SVG](../../../models/shared/swimlane_v2_PartE.svg).

Part F is the customer's cancellation request. Its ownership/state check and effects are one transaction. Only PLACED or CONFIRMED can become CANCELLED; an open offer becomes WITHDRAWN. PREPARING, later and terminal orders remain unchanged when cancellation is refused. Cancellation and kitchen/offer actions must recheck current state rather than rely on the state previously displayed (BR-15).

![Figure 1.6f: Cancellation](../../../models/shared/swimlane_v2_PartF.png)

**Figure 1.6f. Customer cancellation request. Author: 722I0004 · AI-assisted (Codex).** [draw.io](../../../models/shared/swimlane_v2_PartF.drawio) · [SVG](../../../models/shared/swimlane_v2_PartF.svg).

Every unfulfilled terminal outcome in Parts C-F uses the same payment effect: COD becomes VOIDED; ONLINE becomes REFUND_PENDING with refund owed equal to the full captured C. A prior partial amount is replaced by C, never added to it. No path claims a refund was paid or sets REFUNDED. The terminal Order vocabulary is DELIVERED, DELIVERY_FAILED, REJECTED and CANCELLED; other represented Order states are PLACED, CONFIRMED, PREPARING, READY and OUT_FOR_DELIVERY (BR-17; plan section 4).

### Independent administration and management

Part G represents a selected administration task and a separate management-report request. Hub capacity must stay at least one; archiving a hub requires no open orders. Brand/item archive and catalogue price changes preserve existing line snapshots. UserAccount changes between ACTIVE and INACTIVE; a shipper holding a PICKED_UP delivery cannot be deactivated. Order archive requires a terminal order and preserves authorised history, receipts, reporting and refund obligations. Manager reports read records without creating report states or changing data. Their filters and measures follow BR-20-BR-24; report output is not a payment settlement operation (BR-18, BR-19, BR-25).

![Figure 1.6g: Administration and reports](../../../models/shared/swimlane_v2_PartG.png)

**Figure 1.6g. Independent administration and reports. Author: 722I0004 · AI-assisted (Codex).** [draw.io](../../../models/shared/swimlane_v2_PartG.drawio) · [SVG](../../../models/shared/swimlane_v2_PartG.svg).

**Placement and verification.** Insert each complete figure on an A4 landscape page at **230 mm wide** (158.9 mm high), retaining its aspect ratio and its built-in caption/legend. The 1100 × 760 viewBox uses no text smaller than 16 units, giving **9.48 pt** at that placement. Do not shrink below **218.3 mm wide** (9.00 pt). Portrait-width insertion would fail this legibility condition. The overview is not a replacement for the detail pages. Every supplied PNG is a 2200 × 1520 rendering of its matching SVG and was visually inspected; all nine figures were also inspected in 96 dpi A4 landscape proofs at the specified 230 mm placement; geometry and semantic evidence is in `models/shared/business_process_v2.qa.json`. XML parsing and export checks do not claim a native draw.io application review. Final report PDF placement remains a P7 verification item.

Sources: the locked Part 2 plan, sections 1-4 and P1; Case Study PDF pp.1-2; Final Project Requirements PDF pp.2-4 and 8; Report Template headings 1.5-1.6; frozen Part 1 business-process source and `build/proc_*.py` / `notes/diagram_changes.md`. The model and explanation use own wording. Scope clarification L3 remains a team default pending lecturer feedback; no lecturer approval is implied.
