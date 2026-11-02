# 3.1 Design for Use Case 1: Place an order with an accepted full price, voucher and payment choice (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

The design was recorded as a target at C0 (`45ac762`); P4 resolution records 17 UC-01 entries, with their scoped evidence and limitations in the P4 status appendix. The † symbol in a diagram refers to the historical C0 target, not a current implementation verdict.

**Table P4-1. P4 resolution summary.** The detailed appendix lists all 121 entries, their scoped test evidence and remaining limitations. The policy column records static dependency-policy tests.

| Register group | Rows | Scoped runtime/static evidence | Static dependency-policy evidence |
|---|---:|---:|---:|
| UC-01 | 17 | 17 | 0 |
| UC-02 | 5 | 5 | 0 |
| UC-03 | 4 | 4 | 0 |
| UC-04 | 5 | 5 | 0 |
| UC-05 | 12 | 12 | 0 |
| UC-06 | 21 | 21 | 0 |
| shared / supporting | 57 | 45 | 12 |
| Total | 121 | 109 | 12 |

## 3.1.1 Design Classes in Detailed Design

<!-- include: ../report_docx/p7_inputs/status_refresh/UC-01_design_classes.md -->

## 3.1.2 Design Class Diagram

### i. Domain design class

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-01 domain — selected design members 1/4](../../../models/UC-01/dcd_uc01_domain_PartA.png)

Figure 3.1.2.iA. UC-01 domain detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 domain — selected design members 2/4](../../../models/UC-01/dcd_uc01_domain_PartB.png)

Figure 3.1.2.iB. UC-01 domain detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 domain — selected design members 3/4](../../../models/UC-01/dcd_uc01_domain_PartC.png)

Figure 3.1.2.iC. UC-01 domain detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 domain — selected design members 4/4](../../../models/UC-01/dcd_uc01_domain_PartD.png)

Figure 3.1.2.iD. UC-01 domain detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 domain — relationships 1](../../../models/UC-01/dcd_uc01_domain_links_PartA.png)

Figure 3.1.2.i.R1. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 domain — relationships 2](../../../models/UC-01/dcd_uc01_domain_links_PartB.png)

Figure 3.1.2.i.R2. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 domain — relationships 3](../../../models/UC-01/dcd_uc01_domain_links_PartC.png)

Figure 3.1.2.i.R3. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 domain — relationships 4](../../../models/UC-01/dcd_uc01_domain_links_PartD.png)

Figure 3.1.2.i.R4. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 domain — relationships 5](../../../models/UC-01/dcd_uc01_domain_links_PartE.png)

Figure 3.1.2.i.R5. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 domain — relationships 6](../../../models/UC-01/dcd_uc01_domain_links_PartF.png)

Figure 3.1.2.i.R6. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

### ii. Controller


![UC-01 controller — selected design members 1/2](../../../models/UC-01/dcd_uc01_controller_PartA.png)

Figure 3.1.2.iiA. UC-01 controller detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 controller — selected design members 2/2](../../../models/UC-01/dcd_uc01_controller_PartB.png)

Figure 3.1.2.iiB. UC-01 controller detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 controller — relationships 1](../../../models/UC-01/dcd_uc01_controller_links_PartA.png)

Figure 3.1.2.ii.R1. UC-01 controller navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

### iii. UI (view)


![UC-01 view — selected design members 1/1](../../../models/UC-01/dcd_uc01_view.png)

Figure 3.1.2.iii. UC-01 view detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

### iv. Data access


![UC-01 dao — selected design members 1/2](../../../models/UC-01/dcd_uc01_dao_PartA.png)

Figure 3.1.2.ivA. UC-01 dao detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 dao — selected design members 2/2](../../../models/UC-01/dcd_uc01_dao_PartB.png)

Figure 3.1.2.ivB. UC-01 dao detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

### v. Design class (all layers together)


![UC-01 all — selected design members 1/9](../../../models/UC-01/dcd_uc01_all_PartA.png)

Figure 3.1.2.vA. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — selected design members 2/9](../../../models/UC-01/dcd_uc01_all_PartB.png)

Figure 3.1.2.vB. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — selected design members 3/9](../../../models/UC-01/dcd_uc01_all_PartC.png)

Figure 3.1.2.vC. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — selected design members 4/9](../../../models/UC-01/dcd_uc01_all_PartD.png)

Figure 3.1.2.vD. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — selected design members 5/9](../../../models/UC-01/dcd_uc01_all_PartE.png)

Figure 3.1.2.vE. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — selected design members 6/9](../../../models/UC-01/dcd_uc01_all_PartF.png)

Figure 3.1.2.vF. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — selected design members 7/9](../../../models/UC-01/dcd_uc01_all_PartG.png)

Figure 3.1.2.vG. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — selected design members 8/9](../../../models/UC-01/dcd_uc01_all_PartH.png)

Figure 3.1.2.vH. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — selected design members 9/9](../../../models/UC-01/dcd_uc01_all_PartI.png)

Figure 3.1.2.vI. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 1](../../../models/UC-01/dcd_uc01_all_links_PartA.png)

Figure 3.1.2.v.R1. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 2](../../../models/UC-01/dcd_uc01_all_links_PartB.png)

Figure 3.1.2.v.R2. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 3](../../../models/UC-01/dcd_uc01_all_links_PartC.png)

Figure 3.1.2.v.R3. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 4](../../../models/UC-01/dcd_uc01_all_links_PartD.png)

Figure 3.1.2.v.R4. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 5](../../../models/UC-01/dcd_uc01_all_links_PartE.png)

Figure 3.1.2.v.R5. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 6](../../../models/UC-01/dcd_uc01_all_links_PartF.png)

Figure 3.1.2.v.R6. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 7](../../../models/UC-01/dcd_uc01_all_links_PartG.png)

Figure 3.1.2.v.R7. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 8](../../../models/UC-01/dcd_uc01_all_links_PartH.png)

Figure 3.1.2.v.R8. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 9](../../../models/UC-01/dcd_uc01_all_links_PartI.png)

Figure 3.1.2.v.R9. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 10](../../../models/UC-01/dcd_uc01_all_links_PartJ.png)

Figure 3.1.2.v.R10. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 11](../../../models/UC-01/dcd_uc01_all_links_PartK.png)

Figure 3.1.2.v.R11. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 12](../../../models/UC-01/dcd_uc01_all_links_PartL.png)

Figure 3.1.2.v.R12. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 13](../../../models/UC-01/dcd_uc01_all_links_PartM.png)

Figure 3.1.2.v.R13. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 all — relationships 14](../../../models/UC-01/dcd_uc01_all_links_PartN.png)

Figure 3.1.2.v.R14. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

## 3.1.3 OOD with CRC Cards or Communication Diagram

<!-- include: ../report_docx/p7_inputs/status_refresh/UC-01_crc.md -->

## 3.1.4 OOD with Sequence Diagram

Each SSD occurrence has its own operation sequence. Actor → actual blueprint module → controller → domain / typed value; UC-01 also uses the local simulator. No DAO/SQL lifeline is present. Synchronous calls use closed filled arrowheads; dashed open arrows carry results. Actual `alt`, `opt` and `break` rectangles enclose the messages they govern, including self-call paths. Inside an outcome `alt`, separately guarded regions have mutually exclusive conditions. Denial breaks terminate the current interaction; a continuation retains the same request and lifelines. Successful mutation results follow all atomic saves and COMMIT, whose DAO details remain in 4.3.2. Attribute/property reads are notes. Implicit dataclass «create» is not a business operation. Persistence is loaded/saved through data access — see 4.3.2.

Checkout uses Parts A–E: token replay/denial breaks; quote and fingerprint/T validation; optional ONLINE authorization with a decline break; creation only for COD or approved ONLINE; then exclusive commit success versus rollback. Only the failed branch can release an obtained ONLINE reference. The success branch retains authorization. requestQuote uses Parts A–C: eligibility/distance, Quote initialization, then optional voucher validation/discount and fingerprint. Invalid voucher terminates before discount or a quote result. cancelOrder Parts A/B return `cancelledOrderAndAmounts` only after successful atomic save and COMMIT; the rollback reply remains separate.

| SSD operation and exact parameters | View → controller adapter; status | Guard / effects and failure guarantee |
|---|---|---|
| `browseHubs()`<br>`models/UC-01/ssd_uc01_PartA.drawio#01S-M01` | `order.choose_hub, GET /order/hubs` → `PlaceOrderController.list_hubs(self) -> list[HubStatus]`; MATCH | Read .busy / .quiet on HubStatus; these are properties, never busy() / quiet() calls. No persistent writes. Active Customer gate belongs to view; select_hub also checks active Customer and hub. |
| `selectHub(hubId)`<br>`models/UC-01/ssd_uc01_PartA.drawio#01S-M02` | `order.choose_items, GET /order/hubs/<int:hub_id>` → `PlaceOrderController.select_hub(self, user_id: int, hub_id: int) -> HubMenuView`; MATCH | Read .busy / .quiet on HubStatus; these are properties, never busy() / quiet() calls. No persistent writes. Active Customer gate belongs to view; select_hub also checks active Customer and hub. |
| `requestQuote(hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?)`<br>`models/UC-01/ssd_uc01_PartA.drawio#01S-M03` | `order.quote, POST /order/quote` → `PlaceOrderController.request_quote(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None) -> Quote`; P4 status: see Table P4-1 F-04; F-07; P3-S01 | Target: active hub/menu/brand, own active address, integer quantities, load < capacity. Invalid input/refused voucher → no saved rows. Busy suggestions ≤3 ranked (load/capacity, raw distance, ID).<br>Read quote.item_subtotal / quote.total properties. Fingerprint binds hub/address, line IDs, quantities and prices, voucher + D, F, Q and payment choice; full accepted price T=S−D+F−Q. PaymentChoice is a typed adapter value.<br>Read quote.item_subtotal / quote.total properties. Fingerprint binds hub/address, line IDs, quantities and prices, voucher + D, F, Q and payment choice; full accepted price T=S−D+F−Q. PaymentChoice is a typed adapter value. |
| `confirmCheckout(hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?, simulatorOutcome?, quoteFingerprint, quotedTotal, checkoutToken)`<br>`models/UC-01/ssd_uc01_PartB.drawio#01S-M04` | `order.confirm, POST /order/confirm` → `PlaceOrderController.confirm_order(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], idempotency_token: str, quoted_total: Optional[int] = None, voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None, quote_fingerprint: Optional[str] = None) -> OrderConfirmation`; P4 status: see Table P4-1 F-04; F-07; P2-S05; P2-S13 | Simulator approve/decline choice precedes this request. Short atomic checkout begins before token lookup. Own existing token → existingOrder, no reprice, authorization or insertion (UC01-MG02). Foreign token → refusal. Unused token rechecks eligibility, raw radius, capacity, voucher and full consent.<br>Simulator approve/decline choice precedes this request. Short atomic checkout begins before token lookup. Own existing token → existingOrder, no reprice, authorization or insertion (UC01-MG02). Foreign token → refusal. Unused token rechecks eligibility, raw radius, capacity, voucher and full consent.<br>Deterministic local simulator, no network/wait. COD skips authorise; ONLINE declined → zero Order/Line/Payment. Success atomically saves PLACED + snapshots + COD PENDING / ONLINE PAID, C=T (UC01-PC01–06). Any lock/write/commit failure rolls back all intended writes and releases authorization (P2-S05/P2-S13).<br>Deterministic local simulator, no network/wait. COD skips authorise; ONLINE declined → zero Order/Line/Payment. Success atomically saves PLACED + snapshots + COD PENDING / ONLINE PAID, C=T (UC01-PC01–06). Any lock/write/commit failure rolls back all intended writes and releases authorization (P2-S05/P2-S13).<br>Deterministic local simulator, no network/wait. COD skips authorise; ONLINE declined → zero Order/Line/Payment. Success atomically saves PLACED + snapshots + COD PENDING / ONLINE PAID, C=T (UC01-PC01–06). Any lock/write/commit failure rolls back all intended writes and releases authorization (P2-S05/P2-S13). |
| `viewReceipt(orderId)`<br>`models/UC-01/ssd_uc01_PartC.drawio#01S-M05` | `order.detail, GET /order/<int:order_id>` → `OrderTrackingController.get_order(self, user_id: int, order_id: int) -> OrderDetail`; C0 design target; final status in Table P4-1 F-06 | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `viewMyOrders()`<br>`models/UC-01/ssd_uc01_PartC.drawio#01S-M06` | `order.my_orders, GET /order/mine` → `OrderTrackingController.list_my_orders(self, user_id: int) -> list[OrderSummary]`; MATCH | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `cancelOrder(orderId)`<br>`models/UC-01/ssd_uc01_PartC.drawio#01S-M07` | `order.cancel, POST /order/<int:order_id>/cancel` → `OrderTrackingController.cancel_order(self, user_id: int, order_id: int) -> OrderDetail`; P4 status: see Table P4-1 F-02; P2-S13 | Guard: active own Customer; PLACED / CONFIRMED. Atomic CANCELLED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer WITHDRAWN; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback. P4 resolution (see Table P4-1): release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03).<br>Guard: active own Customer; PLACED / CONFIRMED. Atomic CANCELLED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer WITHDRAWN; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback. P4 resolution (see Table P4-1): release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03). |

The design associates these operation guarantees with named controller methods and atomic/read boundaries. The P4 resolution and scoped test evidence are recorded in Table P4-1.

| SSD operation | Responsible method / boundary | Guarantees | Status |
|---|---|---|---|
| OP-13 `browseHubs` | `PlaceOrderController.list_hubs(self) -> list[HubStatus]`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | Matches code |
| OP-14 `selectHub` | `PlaceOrderController.select_hub(self, user_id: int, hub_id: int) -> HubMenuView`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | Matches code |
| OP-15 `requestQuote` | `PlaceOrderController.request_quote(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None) -> Quote`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | P4 status: see Table P4-1 F-04; F-07; P3-S01 |
| OP-01 `confirmCheckout` | `PlaceOrderController.confirm_order(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], idempotency_token: str, quoted_total: Optional[int] = None, voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None, quote_fingerprint: Optional[str] = None) -> OrderConfirmation`; BEGIN IMMEDIATE | UC01-PC01; UC01-PC02; UC01-PC03; UC01-PC04; UC01-PC05; UC01-PC06; UC01-MG01; UC01-MG02; UC01-MG03 | P4 status: see Table P4-1 F-04; F-07; P2-S05; P2-S13 |
| OP-16 `viewReceipt` | `OrderTrackingController.get_order(self, user_id: int, order_id: int) -> OrderDetail`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | C0 design target; final status in Table P4-1 F-06 |
| OP-17 `viewMyOrders` | `OrderTrackingController.list_my_orders(self, user_id: int) -> list[OrderSummary]`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | Matches code |
| OP-07 `cancelOrder` | `OrderTrackingController.cancel_order(self, user_id: int, order_id: int) -> OrderDetail`; BEGIN IMMEDIATE | SUC04-PC01; SUC04-PC02 (atomic cancellation and full-C obligation); checkout PCs are not asserted by cancellation | P4 status: see Table P4-1 F-02; P2-S13 |

### OP-13 browseHubs

![UC-01 browseHubs](../../../models/UC-01/seq_uc01_browseHubs.png)

Figure 3.1.4.OP-13. UC-01 browseHubs — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Read .busy / .quiet on HubStatus; these are properties, never busy() / quiet() calls. No persistent writes. Active Customer gate belongs to view; select_hub also checks active Customer and hub.


### OP-14 selectHub

![UC-01 selectHub](../../../models/UC-01/seq_uc01_selectHub.png)

Figure 3.1.4.OP-14. UC-01 selectHub — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### OP-15 requestQuote

![UC-01 requestQuote — Part A](../../../models/UC-01/seq_uc01_requestQuote_PartA.png)

Figure 3.1.4.OP-15A. UC-01 requestQuote — Part A — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Target: active hub/menu/brand, own active address, integer quantities, load < capacity. Invalid input/refused voucher → no saved rows. Busy suggestions ≤3 ranked (load/capacity, raw distance, ID).

![UC-01 requestQuote — Part B](../../../models/UC-01/seq_uc01_requestQuote_PartB.png)

Figure 3.1.4.OP-15B. UC-01 requestQuote — Part B — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Read quote.item_subtotal / quote.total properties. Fingerprint binds hub/address, line IDs, quantities and prices, voucher + D, F, Q and payment choice; full accepted price T=S−D+F−Q. PaymentChoice is a typed adapter value.

![UC-01 requestQuote — Part C](../../../models/UC-01/seq_uc01_requestQuote_PartC.png)

Figure 3.1.4.OP-15C. UC-01 requestQuote — Part C — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### OP-01 confirmCheckout

![UC-01 confirmCheckout — Part A](../../../models/UC-01/seq_uc01_confirmCheckout_PartA.png)

Figure 3.1.4.OP-01A. UC-01 confirmCheckout — Part A — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Simulator approve/decline choice precedes this request. Short atomic checkout begins before token lookup. Own existing token → existingOrder, no reprice, authorization or insertion (UC01-MG02). Foreign token → refusal. Unused token rechecks eligibility, raw radius, capacity, voucher and full consent.

![UC-01 confirmCheckout — Part B](../../../models/UC-01/seq_uc01_confirmCheckout_PartB.png)

Figure 3.1.4.OP-01B. UC-01 confirmCheckout — Part B — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 confirmCheckout — Part C](../../../models/UC-01/seq_uc01_confirmCheckout_PartC.png)

Figure 3.1.4.OP-01C. UC-01 confirmCheckout — Part C — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Deterministic local simulator, no network/wait. COD skips authorise; ONLINE declined → zero Order/Line/Payment. Success atomically saves PLACED + snapshots + COD PENDING / ONLINE PAID, C=T (UC01-PC01–06). Any lock/write/commit failure rolls back all intended writes and releases authorization (P2-S05/P2-S13).

![UC-01 confirmCheckout — Part D](../../../models/UC-01/seq_uc01_confirmCheckout_PartD.png)

Figure 3.1.4.OP-01D. UC-01 confirmCheckout — Part D — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-01 confirmCheckout — Part E](../../../models/UC-01/seq_uc01_confirmCheckout_PartE.png)

Figure 3.1.4.OP-01E. UC-01 confirmCheckout — Part E — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### OP-16 viewReceipt

![UC-01 viewReceipt](../../../models/UC-01/seq_uc01_viewReceipt.png)

Figure 3.1.4.OP-16. UC-01 viewReceipt — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes.


### OP-17 viewMyOrders

![UC-01 viewMyOrders](../../../models/UC-01/seq_uc01_viewMyOrders.png)

Figure 3.1.4.OP-17. UC-01 viewMyOrders — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### OP-07 cancelOrder

![UC-01 cancelOrder — Part A](../../../models/UC-01/seq_uc01_cancelOrder.png)

Figure 3.1.4.OP-07A. UC-01 cancelOrder — Part A — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Guard: active own Customer; PLACED / CONFIRMED. Atomic CANCELLED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer WITHDRAWN; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback. P4 resolution (see Table P4-1): release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03).

![UC-01 cancelOrder — Part B](../../../models/UC-01/seq_uc01_cancelOrder_PartB.png)

Figure 3.1.4.OP-07B. UC-01 cancelOrder — Part B — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


## 3.1.5 Final Design Class Diagram
Author: 722I0004 · AI-assisted (Claude)

The final design class diagram refines the layer views of 3.1.2 with what the sequence diagrams in 3.1.4 and the implementation settled: UC-01 is served by two controllers, so the final diagram is drawn in two parts, one per controller; classes shared by both parts appear in each.

- **One diagram, four layers.** View (Flask blueprint functions with their routes), controller, domain and data access are drawn together, so every message in the sequence diagrams can be followed from the screen to the table.
- **Only the members this use case calls.** The sequence diagrams fixed which operations each class must offer; the complete member lists stay in the 3.1.1 tables and 3.1.2 views.
- **Signatures from the code.** Parameter names and types are read from the source at the release commit by `models/shared/final_dcd.py`, so the diagram and the program cannot differ.
- **Navigability and persistence.** Dashed arrows show which layer calls which; each DAO has a «persists» link to the entity it stores; domain associations keep their multiplicities from the domain model (2.1.7).

![UC-01 final design class diagram — part A: PlaceOrderController](../../../models/UC-01/dcd_uc01_final_overview_PartA.png)

Figure 3.1.5A. UC-01 final design class diagram — part A: PlaceOrderController — Author: 722I0004 · AI-assisted (Claude).

![UC-01 final design class diagram — part B: OrderTrackingController](../../../models/UC-01/dcd_uc01_final_overview_PartB.png)

Figure 3.1.5B. UC-01 final design class diagram — part B: OrderTrackingController — Author: 722I0004 · AI-assisted (Claude).

Behaviour refined between the first design and the final design (each refinement is covered by the tests in 5.1). Every state-changing operation runs in one `BEGIN IMMEDIATE` transaction and checks the row count of each guarded UPDATE, so a stale page, a guessed ID or a competing user changes nothing.

| System operation | Refinement in the final design |
|---|---|
| `requestQuote` | The delivery radius is checked on the raw distance, not a rounded one (8.004 km is refused). |
| `requestQuote, confirmCheckout` | Consent compares a fingerprint of the whole quote (hub, address, items, prices, voucher, fees, payment), not only the total; any change asks for a fresh quote. |
| `confirmCheckout` | Capacity is re-counted inside the write transaction, so two customers cannot both take the last slot. |
| `viewReceipt` | The receipt says an amount is "owed", never "refunded", because payout is out of scope. |
| `cancelOrder` | Cancelling an online order records the full captured amount as refund owed. |

Editable sources: `models/UC-01/dcd_uc01_final_overview_PartA.dot` and `dcd_uc01_final_overview_PartB.dot` (Graphviz), with SVG exports beside them.
