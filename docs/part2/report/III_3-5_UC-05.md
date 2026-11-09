# 3.5 Design for Use Case 5: Decide an incoming order: confirm, reject, or offer a replacement the customer agrees to (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

The design was recorded as a target at C0 (`45ac762`); P4 resolution records 12 UC-05 entries, with their scoped evidence and limitations in the P4 status appendix. The † symbol in a diagram refers to the historical C0 target, not a current implementation verdict.

## 3.5.1 Design Classes in Detailed Design

<!-- include: ../report_docx/p7_inputs/status_refresh/UC-05_design_classes.md -->

## 3.5.2 Design Class Diagram

### i. Domain design class

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-05 domain — selected design members 1/3](../../../models/UC-05/dcd_uc05_domain_PartA.png)

Figure 3.5.2.iA. UC-05 domain detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 domain — selected design members 2/3](../../../models/UC-05/dcd_uc05_domain_PartB.png)

Figure 3.5.2.iB. UC-05 domain detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 domain — selected design members 3/3](../../../models/UC-05/dcd_uc05_domain_PartC.png)

Figure 3.5.2.iC. UC-05 domain detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 domain — relationships 1](../../../models/UC-05/dcd_uc05_domain_links_PartA.png)

Figure 3.5.2.i.R1. UC-05 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 domain — relationships 2](../../../models/UC-05/dcd_uc05_domain_links_PartB.png)

Figure 3.5.2.i.R2. UC-05 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 domain — relationships 3](../../../models/UC-05/dcd_uc05_domain_links_PartC.png)

Figure 3.5.2.i.R3. UC-05 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 domain — relationships 4](../../../models/UC-05/dcd_uc05_domain_links_PartD.png)

Figure 3.5.2.i.R4. UC-05 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 domain — relationships 5](../../../models/UC-05/dcd_uc05_domain_links_PartE.png)

Figure 3.5.2.i.R5. UC-05 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

### ii. Controller


![UC-05 controller — selected design members 1/2](../../../models/UC-05/dcd_uc05_controller_PartA.png)

Figure 3.5.2.iiA. UC-05 controller detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 controller — selected design members 2/2](../../../models/UC-05/dcd_uc05_controller_PartB.png)

Figure 3.5.2.iiB. UC-05 controller detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 controller — relationships 1](../../../models/UC-05/dcd_uc05_controller_links_PartA.png)

Figure 3.5.2.ii.R1. UC-05 controller navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

### iii. UI (view)


![UC-05 view — selected design members 1/1](../../../models/UC-05/dcd_uc05_view.png)

Figure 3.5.2.iii. UC-05 view detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

### iv. Data access


![UC-05 dao — selected design members 1/1](../../../models/UC-05/dcd_uc05_dao.png)

Figure 3.5.2.iv. UC-05 dao detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

### v. Design class (all layers together)


![UC-05 all — selected design members 1/7](../../../models/UC-05/dcd_uc05_all_PartA.png)

Figure 3.5.2.vA. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — selected design members 2/7](../../../models/UC-05/dcd_uc05_all_PartB.png)

Figure 3.5.2.vB. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — selected design members 3/7](../../../models/UC-05/dcd_uc05_all_PartC.png)

Figure 3.5.2.vC. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — selected design members 4/7](../../../models/UC-05/dcd_uc05_all_PartD.png)

Figure 3.5.2.vD. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — selected design members 5/7](../../../models/UC-05/dcd_uc05_all_PartE.png)

Figure 3.5.2.vE. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — selected design members 6/7](../../../models/UC-05/dcd_uc05_all_PartF.png)

Figure 3.5.2.vF. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — selected design members 7/7](../../../models/UC-05/dcd_uc05_all_PartG.png)

Figure 3.5.2.vG. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 1](../../../models/UC-05/dcd_uc05_all_links_PartA.png)

Figure 3.5.2.v.R1. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 2](../../../models/UC-05/dcd_uc05_all_links_PartB.png)

Figure 3.5.2.v.R2. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 3](../../../models/UC-05/dcd_uc05_all_links_PartC.png)

Figure 3.5.2.v.R3. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 4](../../../models/UC-05/dcd_uc05_all_links_PartD.png)

Figure 3.5.2.v.R4. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 5](../../../models/UC-05/dcd_uc05_all_links_PartE.png)

Figure 3.5.2.v.R5. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 6](../../../models/UC-05/dcd_uc05_all_links_PartF.png)

Figure 3.5.2.v.R6. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 7](../../../models/UC-05/dcd_uc05_all_links_PartG.png)

Figure 3.5.2.v.R7. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 8](../../../models/UC-05/dcd_uc05_all_links_PartH.png)

Figure 3.5.2.v.R8. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 9](../../../models/UC-05/dcd_uc05_all_links_PartI.png)

Figure 3.5.2.v.R9. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 10](../../../models/UC-05/dcd_uc05_all_links_PartJ.png)

Figure 3.5.2.v.R10. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 11](../../../models/UC-05/dcd_uc05_all_links_PartK.png)

Figure 3.5.2.v.R11. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


![UC-05 all — relationships 12](../../../models/UC-05/dcd_uc05_all_links_PartL.png)

Figure 3.5.2.v.R12. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

## 3.5.3 OOD with CRC Cards or Communication Diagram

<!-- include: ../report_docx/p7_inputs/status_refresh/UC-05_crc.md -->

## 3.5.4 OOD with Sequence Diagram

Each SSD occurrence has its own operation sequence. Actor → actual blueprint module → controller → domain / typed value. The UC-01 local simulator is described separately. No DAO/SQL lifeline is present. Synchronous calls use closed filled arrowheads; dashed open arrows carry results. Actual `alt`, `opt` and `break` rectangles enclose the messages they govern, including self-call paths. Inside an outcome `alt`, separately guarded regions have mutually exclusive conditions. Denial breaks terminate the current interaction; a continuation retains the same request and lifelines. Successful mutation results follow all atomic saves and COMMIT, whose DAO details remain in 4.3.2. Attribute/property reads are notes. Implicit dataclass «create» is not a business operation. Persistence is loaded/saved through data access; see 4.3.2.

acceptReplacement Parts A–C preserve stale refusal before mutation, then exclusive invalid-target withdrawal versus valid-target replacement. Invalid-target outcome returns only a committed withdrawal/reason or controlled failure; it never executes replace_line. Only the valid-target continuation can return acceptedOrderAndAmounts after successful atomic save and COMMIT. rejectOrder and declineReplacement Parts A/B now return `rejectedOrder` and `rejectedOrderAndAmounts`, respectively, inside the committed branch; failed saves return refusal/controlledFailure with rollback. No result implies implementation or a measured transaction guarantee.

| SSD operation and exact parameters | View → controller adapter; status | Guard / effects and failure guarantee |
|---|---|---|
| `viewKitchenOrders()`<br>`models/UC-05/ssd_uc05_PartA.drawio#05S-M01` | `kitchen.board, GET /kitchen/` → `KitchenController.board(self, user_id: int) -> KitchenBoard`; MATCH | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `viewKitchenOrder(orderId)`<br>`models/UC-05/ssd_uc05_PartA.drawio#05S-M02` | `kitchen.order, GET /kitchen/orders/<int:order_id>` → `KitchenController.get_order(self, user_id: int, order_id: int) -> KitchenOrderView`; MATCH | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `confirmOrder(orderId)`<br>`models/UC-05/ssd_uc05_PartA.drawio#05S-M03` | `kitchen.confirm, POST /kitchen/orders/<int:order_id>/confirm` → `KitchenController.confirm_order(self, user_id: int, order_id: int) -> Order`; P4 status: see Table P4-1 P2-S13; P3-S03 | Active own-hub staff; own PLACED; no open OFFERED. Atomic guarded state change + confirmed_at. No repricing/payment change. Conditional rowcount and busy/write/commit rollback (P2-S13, P3-S03). |
| `rejectOrder(orderId, reason)`<br>`models/UC-05/ssd_uc05_PartA.drawio#05S-M04` | `kitchen.reject, POST /kitchen/orders/<int:order_id>/reject` → `KitchenController.reject_order(self, user_id: int, order_id: int, reason: str) -> Order`; P4 status: see Table P4-1 F-02; P2-S13 | Guard: active own-hub Kitchen staff; PLACED; nonempty reason. Atomic REJECTED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer WITHDRAWN; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback. P4 resolution (see Table P4-1): release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03).<br>Guard: active own-hub Kitchen staff; PLACED; nonempty reason. Atomic REJECTED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer WITHDRAWN; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback. P4 resolution (see Table P4-1): release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03). |
| `offerReplacement(orderId, orderLineId, targetItemId)`<br>`models/UC-05/ssd_uc05_PartA.drawio#05S-M05` | `kitchen.offer, POST /kitchen/orders/<int:order_id>/offer` → `KitchenController.offer_replacement(self, user_id: int, order_id: int, order_line_id: int, new_menu_item_id: int) -> ReplacementOffer`; P4 status: see Table P4-1 F-05; P2-S09; P2-S13 | Active own-hub PLACED; no open offer. Source currently sold out/unlisted/archived. Target active + active Brand, same-hub listed/available, different and absent from other lines; offered unit price ≤ source snapshot. Atomic OFFERED with unchanged quantity/Order PLACED (PC03). Fail/lock/commit rollback; no request waits for Customer. |
| `viewMyOrders()`<br>`models/UC-05/ssd_uc05_PartB.drawio#05S-M06` | `order.my_orders, GET /order/mine` → `OrderTrackingController.list_my_orders(self, user_id: int) -> list[OrderSummary]`; MATCH | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `viewReplacement(orderId)`<br>`models/UC-05/ssd_uc05_PartB.drawio#05S-M07` | `order.detail, GET /order/<int:order_id>` → `OrderTrackingController.get_order(self, user_id: int, order_id: int) -> OrderDetail`; C0 design target; final status in Table P4-1 F-06 | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `acceptReplacement(orderId, offerId)`<br>`models/UC-05/ssd_uc05_PartB.drawio#05S-M08` | `order.answer_replacement, POST /order/<int:order_id>/replacement` → `OrderTrackingController.answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail`; P4 status: see Table P4-1 F-05; F-02; P2-S09; P2-S11; P2-S13 | Before mutation: active owner + own PLACED + exact open OFFERED belongs to order. Recheck target active, active Brand, listed + AVAILABLE at same hub. Ineligible owner/state/offer → staleRefusal, 0 changed rows. Invalid target → only exact offer WITHDRAWN with returned reason; Order/lines/payment unchanged (MG01).<br>Valid acceptance continues atomically: use offered price, whole line, same quantity; Snew; Dnew=min(Dold,Snew), F/Q unchanged; Tnew=Snew−Dnew+F−Q. Read Order.total property, set offer ACCEPTED through data access. COD amount=Tnew; ONLINE state PAID, C unchanged, refund_amount=C−Tnew. Order stays PLACED (PC04), never auto-confirms. Any conditional 0-row/lock/write/commit failure → complete rollback, MG01.<br>Valid acceptance continues atomically: use offered price, whole line, same quantity; Snew; Dnew=min(Dold,Snew), F/Q unchanged; Tnew=Snew−Dnew+F−Q. Read Order.total property, set offer ACCEPTED through data access. COD amount=Tnew; ONLINE state PAID, C unchanged, refund_amount=C−Tnew. Order stays PLACED (PC04), never auto-confirms. Any conditional 0-row/lock/write/commit failure → complete rollback, MG01. |
| `declineReplacement(orderId, offerId)`<br>`models/UC-05/ssd_uc05_PartC.drawio#05S-M09` | `order.answer_replacement, POST /order/<int:order_id>/replacement` → `OrderTrackingController.answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail`; P4 status: see Table P4-1 F-02; P2-S13 | Guard: active own Customer; PLACED; exact open OFFERED with matching order/offer IDs. SUC03-PC04: atomic REJECTED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer DECLINED; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback. P4 resolution (see Table P4-1): release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03).<br>Guard: active own Customer; PLACED; exact open OFFERED with matching order/offer IDs. SUC03-PC04: atomic REJECTED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer DECLINED; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback. P4 resolution (see Table P4-1): release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03). |

The design associates these operation guarantees with named controller methods and atomic/read boundaries. The P4 resolution and scoped test evidence are recorded in Table P4-1.

| SSD operation | Responsible method / boundary | Guarantees | Status |
|---|---|---|---|
| OP-19 `viewKitchenOrders` | `KitchenController.board(self, user_id: int) -> KitchenBoard`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | Matches code |
| OP-20 `viewKitchenOrder` | `KitchenController.get_order(self, user_id: int, order_id: int) -> KitchenOrderView`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | Matches code |
| OP-02 `confirmOrder` | `KitchenController.confirm_order(self, user_id: int, order_id: int) -> Order`; BEGIN IMMEDIATE | UC05-PC01; UC05-MG01 | P4 status: see Table P4-1 P2-S13; P3-S03 |
| OP-03 `rejectOrder` | `KitchenController.reject_order(self, user_id: int, order_id: int, reason: str) -> Order`; BEGIN IMMEDIATE | UC05-PC02 | P4 status: see Table P4-1 F-02; P2-S13 |
| OP-04 `offerReplacement` | `KitchenController.offer_replacement(self, user_id: int, order_id: int, order_line_id: int, new_menu_item_id: int) -> ReplacementOffer`; BEGIN IMMEDIATE | UC05-PC03; UC05-MG01 | P4 status: see Table P4-1 F-05; P2-S09; P2-S13 |
| OP-17 `viewMyOrders` | `OrderTrackingController.list_my_orders(self, user_id: int) -> list[OrderSummary]`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | Matches code |
| OP-18 `viewReplacement` | `OrderTrackingController.get_order(self, user_id: int, order_id: int) -> OrderDetail`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | C0 design target; final status in Table P4-1 F-06 |
| OP-05 `acceptReplacement` | `OrderTrackingController.answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail`; BEGIN IMMEDIATE | UC05-PC04; UC05-MG01 | P4 status: see Table P4-1 F-05; F-02; P2-S09; P2-S11; P2-S13 |
| OP-06 `declineReplacement` | `OrderTrackingController.answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail`; BEGIN IMMEDIATE | SUC03-PC04; UC05-MG01 (decline/reject and BR-17; stale or failed save leaves Order unchanged) | P4 status: see Table P4-1 F-02; P2-S13 |

### OP-19 viewKitchenOrders

![UC-05 viewKitchenOrders](../../../models/UC-05/seq_uc05_viewKitchenOrders.png)

Figure 3.5.4.OP-19. UC-05 viewKitchenOrders — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes.


### OP-20 viewKitchenOrder

![UC-05 viewKitchenOrder](../../../models/UC-05/seq_uc05_viewKitchenOrder.png)

Figure 3.5.4.OP-20. UC-05 viewKitchenOrder — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### OP-02 confirmOrder

![UC-05 confirmOrder](../../../models/UC-05/seq_uc05_confirmOrder.png)

Figure 3.5.4.OP-02. UC-05 confirmOrder — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Active own-hub staff; own PLACED; no open OFFERED. Atomic guarded state change + confirmed_at. No repricing/payment change. Conditional rowcount and busy/write/commit rollback (P2-S13, P3-S03).


### OP-03 rejectOrder

![UC-05 rejectOrder — Part A](../../../models/UC-05/seq_uc05_rejectOrder.png)

Figure 3.5.4.OP-03A. UC-05 rejectOrder — Part A — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Guard: active own-hub Kitchen staff; PLACED; nonempty reason. Atomic REJECTED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer WITHDRAWN; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback. P4 resolution (see Table P4-1): release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03).

![UC-05 rejectOrder — Part B](../../../models/UC-05/seq_uc05_rejectOrder_PartB.png)

Figure 3.5.4.OP-03B. UC-05 rejectOrder — Part B — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### OP-04 offerReplacement

![UC-05 offerReplacement](../../../models/UC-05/seq_uc05_offerReplacement.png)

Figure 3.5.4.OP-04. UC-05 offerReplacement — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Active own-hub PLACED; no open offer. Source currently sold out/unlisted/archived. Target active + active Brand, same-hub listed/available, different and absent from other lines; offered unit price ≤ source snapshot. Atomic OFFERED with unchanged quantity/Order PLACED (PC03). Fail/lock/commit rollback; no request waits for Customer.


### OP-17 viewMyOrders

![UC-05 viewMyOrders](../../../models/UC-05/seq_uc05_viewMyOrders.png)

Figure 3.5.4.OP-17. UC-05 viewMyOrders — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### OP-18 viewReplacement

![UC-05 viewReplacement](../../../models/UC-05/seq_uc05_viewReplacement.png)

Figure 3.5.4.OP-18. UC-05 viewReplacement — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### OP-05 acceptReplacement

![UC-05 acceptReplacement — Part A](../../../models/UC-05/seq_uc05_acceptReplacement_PartA.png)

Figure 3.5.4.OP-05A. UC-05 acceptReplacement — Part A — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Before mutation: active owner + own PLACED + exact open OFFERED belongs to order. Recheck target active, active Brand, listed + AVAILABLE at same hub. Ineligible owner/state/offer → staleRefusal, 0 changed rows. Invalid target → only exact offer WITHDRAWN with returned reason; Order/lines/payment unchanged (MG01).

![UC-05 acceptReplacement — Part B](../../../models/UC-05/seq_uc05_acceptReplacement_PartB.png)

Figure 3.5.4.OP-05B. UC-05 acceptReplacement — Part B — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Valid acceptance continues atomically: use offered price, whole line, same quantity; Snew; Dnew=min(Dold,Snew), F/Q unchanged; Tnew=Snew−Dnew+F−Q. Read Order.total property, set offer ACCEPTED through data access. COD amount=Tnew; ONLINE state PAID, C unchanged, refund_amount=C−Tnew. Order stays PLACED (PC04), never auto-confirms. Any conditional 0-row/lock/write/commit failure → complete rollback, MG01.

![UC-05 acceptReplacement — Part C](../../../models/UC-05/seq_uc05_acceptReplacement_PartC.png)

Figure 3.5.4.OP-05C. UC-05 acceptReplacement — Part C — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).



### OP-06 declineReplacement

![UC-05 declineReplacement — Part A](../../../models/UC-05/seq_uc05_declineReplacement.png)

Figure 3.5.4.OP-06A. UC-05 declineReplacement — Part A — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).

Guard: active own Customer; PLACED; exact open OFFERED with matching order/offer IDs. SUC03-PC04: atomic REJECTED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer DECLINED; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback. P4 resolution (see Table P4-1): release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03).

![UC-05 declineReplacement — Part B](../../../models/UC-05/seq_uc05_declineReplacement_PartB.png)

Figure 3.5.4.OP-06B. UC-05 declineReplacement — Part B — Author: 722I0004 · AI-assisted (Codex) † = element completed during implementation (Table P4-1).


## 3.5.5 Final Design Class Diagram
Author: 722I0004 · AI-assisted (Claude)

The final design class diagram refines the layer views of 3.5.2 with what the sequence diagrams in 3.5.4 and the implementation settled. UC-05 is served by two controllers (KitchenController and OrderTrackingController), so the detail sheets are drawn per controller (A for KitchenController, B for OrderTrackingController); classes shared by both appear on both. Figure 3.5.5A is an overview of all classes; the detail sheets after it give the members of one controller at a time.

- **Overview first, then detail sheets.** Figure 3.5.5A shows every class of the four layers by name, with the calls, the «persists» and «loads» links and the domain associations, drawn as plain lines; their multiplicities and navigability are in the domain views of 3.5.2 and the domain model (2.1.7), because the labels pile up at the small name boxes. The detail sheets leave the associations out. The members are too many to print readably on the same page, so the detail sheets take one controller at a time and show the view functions that call it and the DAOs and domain classes it uses, with member signatures. A controller that needs more than one sheet has them numbered (A1, A2 and so on); each caption says what the sheet shows. Each figure is laid out for its page so that the estimated smallest text is 9 pt or more.
- **Only the members this use case calls.** The sequence diagrams fixed which operations each class must offer; the complete member lists stay in the 3.5.1 tables and 3.5.2 views.
- **Signatures read from the code.** Parameter names and types are read from the source by `models/shared/final_dcd.py` when the figures are generated, and each member is matched with the operation rows of the design model. This is a cross-check at generation time, not a guarantee: the figures must be regenerated after a code change.
- **Navigability and persistence.** Layers run top to bottom (view, controller, data access, domain) and the dashed arrows run the same way: view to controller, controller to the DAOs and domain classes it uses, and DAO to the entity it maps. «persists» marks a DAO that writes the entity's table in this use case (an INSERT, UPDATE or DELETE in a method the use case calls); «loads» marks one that only reads it. The arrow points from the DAO to the entity, so the domain layer does not depend on data access. Domain associations keep their multiplicities from the domain model (2.1.7).

![UC-05 final design class diagram, overview (class names only)](../../../models/UC-05/dcd_uc05_final_overview.png)

Figure 3.5.5A. UC-05 final design class diagram, overview (class names only) — Author: 722I0004 · AI-assisted (Claude).

![UC-05 final design class diagram, detail sheet A1 (KitchenController, view and controller)](../../../models/UC-05/dcd_uc05_final_detail_A1.png)

Figure 3.5.5B. UC-05 final design class diagram, detail sheet A1 (KitchenController, view and controller) — Author: 722I0004 · AI-assisted (Claude).

![UC-05 final design class diagram, detail sheet A2 (KitchenController, controller and domain)](../../../models/UC-05/dcd_uc05_final_detail_A2.png)

Figure 3.5.5C. UC-05 final design class diagram, detail sheet A2 (KitchenController, controller and domain) — Author: 722I0004 · AI-assisted (Claude).

![UC-05 final design class diagram, detail sheet A3 (KitchenController, data access)](../../../models/UC-05/dcd_uc05_final_detail_A3.png)

Figure 3.5.5D. UC-05 final design class diagram, detail sheet A3 (KitchenController, data access) — Author: 722I0004 · AI-assisted (Claude).

![UC-05 final design class diagram, detail sheet B1 (OrderTrackingController, view and controller)](../../../models/UC-05/dcd_uc05_final_detail_B1.png)

Figure 3.5.5E. UC-05 final design class diagram, detail sheet B1 (OrderTrackingController, view and controller) — Author: 722I0004 · AI-assisted (Claude).

![UC-05 final design class diagram, detail sheet B2 (OrderTrackingController, controller and domain)](../../../models/UC-05/dcd_uc05_final_detail_B2.png)

Figure 3.5.5F. UC-05 final design class diagram, detail sheet B2 (OrderTrackingController, controller and domain) — Author: 722I0004 · AI-assisted (Claude).

![UC-05 final design class diagram, detail sheet B3 (OrderTrackingController, data access, part 1 of 2)](../../../models/UC-05/dcd_uc05_final_detail_B3.png)

Figure 3.5.5G. UC-05 final design class diagram, detail sheet B3 (OrderTrackingController, data access, part 1 of 2) — Author: 722I0004 · AI-assisted (Claude).

![UC-05 final design class diagram, detail sheet B4 (OrderTrackingController, data access, part 2 of 2)](../../../models/UC-05/dcd_uc05_final_detail_B4.png)

Figure 3.5.5H. UC-05 final design class diagram, detail sheet B4 (OrderTrackingController, data access, part 2 of 2) — Author: 722I0004 · AI-assisted (Claude).

Behaviour refined between the first design and the final design (each refinement is covered by the tests in 5.1). Every state-changing operation runs in one `BEGIN IMMEDIATE` transaction and checks the row count of each guarded UPDATE, so a stale page, a guessed ID or a competing user changes nothing.

| System operation | Refinement in the final design |
|---|---|
| `offerReplacement` | An offer requires the original dish to be unavailable and the target to be listed and available at the same hub. |
| `acceptReplacement` | Acceptance re-checks that the order is still PLACED, that this exact offer is still open and that the target is still available; otherwise the offer is withdrawn and the order is unchanged. |
| `rejectOrder, declineReplacement` | Rejection records the full online amount as refund owed and withdraws an open offer. |
| `viewReplacement` | The customer sees the old and new line and the new total before answering. |

Editable sources: `models/UC-05/dcd_uc05_final_overview.dot`, `models/UC-05/dcd_uc05_final_detail_A1.dot`, `models/UC-05/dcd_uc05_final_detail_A2.dot`, `models/UC-05/dcd_uc05_final_detail_A3.dot`, `models/UC-05/dcd_uc05_final_detail_B1.dot`, `models/UC-05/dcd_uc05_final_detail_B2.dot`, `models/UC-05/dcd_uc05_final_detail_B3.dot` and `models/UC-05/dcd_uc05_final_detail_B4.dot` (Graphviz, generated by `models/shared/final_dcd.py`), with SVG exports beside them.
