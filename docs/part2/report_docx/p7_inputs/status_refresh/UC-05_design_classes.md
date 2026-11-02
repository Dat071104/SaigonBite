# UC-05 design classes

Author: 722I0004 · AI-assisted (Codex)

Each table lists the members of one design class. "Matches code" means the member exists in the code with exactly this signature. "Changed during implementation and tested" means the first design (commit C0 = 45ac762, 24/10/2026) was corrected while coding; the reason is given and the tests are listed in Table P4-1 (Appendix).

Properties have signatures for traceability but are read as attributes; dataclass «create» means implicit initialization, not an invented business method. Unannotated types are marked inferred. Templates are presentation resources, not design classes.

## KitchenController

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «controller» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | P4 scoped evidence (P4.1 + P4.4, P4.4; resolution rows 16, 17, 18, 19, 20, 21) |
| Source | `saigonbite/business/controllers/kitchen_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hubs: HubDAO` **inferred** | Matches code |
| Attribute | `+ menu: MenuDAO` **inferred** | Matches code |
| Attribute | `+ orders: OrderDAO` **inferred** | Matches code |
| Attribute | `+ payments: PaymentDAO` **inferred** | Matches code |
| Attribute | `+ deliveries: DeliveryDAO` **inferred** | Matches code |
| Attribute | `+ offers: ReplacementOfferDAO` **inferred** | Matches code |
| Operation | `+ board(self, user_id: int) -> KitchenBoard` | Matches code |
| Operation | `+ get_order(self, user_id: int, order_id: int) -> KitchenOrderView` | Matches code |
| Operation | `+ confirm_order(self, user_id: int, order_id: int) -> Order` | P4 scoped evidence (P4.1 + P4.4; resolution rows 18); Reason: P2-S13; P3-S03; Guarded writes must check rowcount and handle busy / commit failure without partial effects; shared helper is currently incomplete. |
| Operation | `+ reject_order(self, user_id: int, order_id: int, reason: str) -> Order` | Changed during implementation and tested (P4.4; Table P4-1 rows 16); Reason: F-02; P2-S13; BR-17 full C refund owed and atomic state/amount writes, including COMMIT rollback. |
| Operation | `+ offer_replacement(self, user_id: int, order_id: int, order_line_id: int, new_menu_item_id: int) -> ReplacementOffer` | Changed during implementation and tested (P4.4; Table P4-1 rows 17); Reason: F-05; P2-S09; P2-S13; Require currently unavailable source; target active/listed/available; one open offer; check every conditional save result. |

## kitchen

| Detail | Design |
|---|---|
| Layer / stereotype | view / «view» |
| Responsibility | Translate own-hub kitchen actions and render their results. |
| Class status | MATCH (Static) |
| Source | `saigonbite/presentation/kitchen.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ board() -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |
| Operation | `+ order(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |
| Operation | `+ confirm(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |
| Operation | `+ reject(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |
| Operation | `+ offer(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |

## HubDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/hub_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Operation | `+ get_including_archived(self, hub_id: int) -> Optional[Hub]` | Matches code |
| Operation | `+ list_menu(self, hub_id: int) -> list[HubMenuItem]` | Matches code |
| Operation | `+ get_available_item(self, hub_id: int, menu_item_id: int) -> Optional[MenuItem]` | Matches code |

## OrderDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | Changed during implementation and tested (P4.4, P4.7; Table P4-1 rows 43, 44, 45) |
| Source | `saigonbite/data_access/order_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Operation | `- _load(self, row: Optional[sqlite3.Row]) -> Optional[Order]` | Matches code |
| Operation | `+ list_for_hub(self, hub_id: int, states: Iterable[OrderState]) -> list[Order]` | Matches code |
| Operation | `+ get_by_id(self, order_id: int) -> Optional[Order]` | Matches code |
| Operation | `+ change_state(self, order_id: int, from_state: OrderState, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> bool` | Matches code |
| Operation | `+ list_for_customer(self, customer_id: int) -> list[Order]` | Matches code |
| Operation | `+ save_lines_and_totals(self, order: Order) -> bool` | Changed during implementation and tested (P4.4; Table P4-1 rows 43, 44); Reason: P2-S09; P2-S11; P3-S03; Apply replacement only to expected PLACED order and check each affected line/header rowcount. |

## ReplacementOfferDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/offer_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Operation | `+ get_open(self, order_id: int) -> Optional[ReplacementOffer]` | Matches code |
| Operation | `+ list_for_order(self, order_id: int) -> list[ReplacementOffer]` | Matches code |
| Operation | `+ decide(self, offer_id: int, to_state: OfferState, now: str) -> bool` | Matches code |
| Operation | `+ insert(self, offer: ReplacementOffer) -> int` | Matches code |

## UserDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/user_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Operation | `+ get_by_id(self, user_id: int) -> Optional[UserAccount]` | Matches code |

## PaymentDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | Changed during implementation and tested (P4.4; Table P4-1 rows 46, 47, 48, 49, 50) |
| Source | `saigonbite/data_access/payment_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Operation | `+ get_by_order_id(self, order_id: int) -> Optional[Payment]` | Matches code |
| Operation | `+ change_state(self, order_id: int, from_state: PaymentState, to_state: PaymentState, now: str) -> bool` | Matches code |
| Operation | `+ set_amounts(self, order_id: int, amount: int, refund_amount: int, now: str) -> bool` | Changed during implementation and tested (P4.4; Table P4-1 rows 46, 47, 48, 49, 50); Reason: F-02; P3-S03; Persist full/partial refund obligations atomically and expose the conditional save outcome. |

## Order

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Own the order lifecycle, snapshots and accepted replacement totals. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customer_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ hub_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ address_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ state: OrderState` | Matches code |
| Attribute | `+ delivery_fee: int` | Matches code |
| Attribute | `+ idempotency_token: str` | Matches code |
| Attribute | `+ placed_at: str` | Matches code |
| Attribute | `+ lines: list[OrderLine]` | Matches code |
| Attribute | `+ id: Optional[int]` | Matches code |
| Attribute | `+ archived_at: Optional[str]` | Matches code |
| Attribute | `+ delivery_address_text: str` | Matches code |
| Attribute | `+ distance_km: float` | Matches code |
| Attribute | `+ voucher_id: Optional[int]` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ voucher_discount: int` | Matches code |
| Attribute | `+ quiet_discount: int` | Matches code |
| Attribute | `+ reject_reason: Optional[str]` | Matches code |
| Attribute | `+ confirmed_at: Optional[str]` | Matches code |
| Attribute | `+ ready_at: Optional[str]` | Matches code |
| Attribute | `+ closed_at: Optional[str]` | Matches code |
| Operation | `+ move_to(self, new_state: OrderState) -> None` | Matches code |
| Operation | `+ line(self, line_id: int) -> Optional[OrderLine]` | Matches code |
| Operation | `+ replace_line(self, line_id: int, menu_item_id: int, item_name: str, unit_price: int) -> None` | Matches code |
| Read-only property | `+ total(self) -> int {property; read as .total}` | Matches code |

## Payment

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Hold captured amount C and refund obligations without claiming payout. |
| Class status | Changed during implementation and tested (P4.4; Table P4-1 rows 9, 10, 11, 12) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ method: PaymentMethod` | Matches code |
| Attribute | `+ state: PaymentState` | Matches code |
| Attribute | `+ amount: int` | Matches code |
| Attribute | `+ created_at: str` | Matches code |
| Attribute | `+ updated_at: Optional[str]` | Matches code |
| Attribute | `+ online_option: Optional[OnlineOption]` | Matches code |
| Attribute | `+ provider_ref: Optional[str]` | Matches code |
| Attribute | `+ refund_amount: int` | Matches code |
| Attribute | `+ id: Optional[int]` | Matches code |
| Operation | `+ release_for_unfulfilled_order(self) -> None` | Changed during implementation and tested (P4.4; Table P4-1 rows 9, 10, 11, 12); Reason: F-02; P2-S01; Set refund_amount=C with REFUND_PENDING; preserve COD VOIDED; no payout operation. |

## OrderTrackingController

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «controller» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | Changed during implementation and tested (P4.4; Table P4-1 rows 13, 14, 15) |
| Source | `saigonbite/business/controllers/order_tracking_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customers: CustomerDAO` **inferred** | Matches code |
| Attribute | `+ orders: OrderDAO` **inferred** | Matches code |
| Attribute | `+ payments: PaymentDAO` **inferred** | Matches code |
| Attribute | `+ hubs: HubDAO` **inferred** | Matches code |
| Attribute | `+ deliveries: DeliveryDAO` **inferred** | Matches code |
| Attribute | `+ offers: ReplacementOfferDAO` **inferred** | Matches code |
| Operation | `+ list_my_orders(self, user_id: int) -> list[OrderSummary]` | Matches code |
| Operation | `+ get_order(self, user_id: int, order_id: int) -> OrderDetail` | Matches code |
| Operation | `+ answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail` | Changed during implementation and tested (P4.4; Table P4-1 rows 13, 14); Reason: F-05; F-02; P2-S09; P2-S11; P2-S13; Recheck PLACED and exact open offer; recheck target; invalid target withdraws only the offer; valid accept uses offered price; controlled rollback through COMMIT. |
| Operation | `- _own_order(self, customer: Customer, order_id: int) -> Order` | Matches code |
| Operation | `- _require_customer(self, user_id: int) -> Customer` | Matches code |

## order

| Detail | Design |
|---|---|
| Layer / stereotype | view / «view» |
| Responsibility | Translate authenticated customer routes and render quote, receipt and order results. |
| Class status | Changed during implementation and tested (P4.3; Table P4-1 rows 60, 61) |
| Source | `saigonbite/presentation/order.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ my_orders() -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |
| Operation | `+ detail(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |
| Operation | `+ answer_replacement(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |

## CustomerDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/customer_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Operation | `+ get_by_user_id(self, user_id: int) -> Optional[Customer]` | Matches code |

## OrderDetail

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/order_tracking_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order: Order` | Matches code |
| Attribute | `+ payment: Payment` | Matches code |
| Attribute | `+ hub: Hub` | Matches code |
| Attribute | `+ delivery: Optional[Delivery]` | Matches code |
| Attribute | `+ open_offer: Optional[ReplacementOffer]` | Matches code |
| Attribute | `+ offers: list[ReplacementOffer]` | Matches code |
| Read-only property | `+ total_if_accepted(self) -> Optional[int] {property; read as .total_if_accepted}` | Matches code |

## DeliveryDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/delivery_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Operation | `+ get_by_order_id(self, order_id: int) -> Optional[Delivery]` | Matches code |

## controllers.common

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «module» |
| Responsibility | Module functions with their original Python signatures. |
| Class status | Changed during implementation and tested (P4.4; Table P4-1 rows 54) |
| Source | `saigonbite/business/controllers/common.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ move_order(orders: OrderDAO, order: Order, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> None` | Matches code |
| Operation | `+ release_payment(payments: PaymentDAO, order_id: int, now: str) -> Payment` | Changed during implementation and tested (P4.4; Table P4-1 rows 54); Reason: F-02; P2-S01; P3-S03; Persist full captured C as refund_amount together with state; changing only the domain object does not save the amount. Check conditional save results in the same transaction. |

## ReplacementOffer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Hold one proposed whole-line replacement and its decision history. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ order_line_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ original_item_name: str` | Matches code |
| Attribute | `+ original_unit_price: int` | Matches code |
| Attribute | `+ new_menu_item_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ new_item_name: str` | Matches code |
| Attribute | `+ new_unit_price: int` | Matches code |
| Attribute | `+ state: OfferState` | Matches code |
| Attribute | `+ offered_at: str` | Matches code |
| Attribute | `+ decided_at: Optional[str]` | Matches code |
| Attribute | `+ id: Optional[int]` | Matches code |
| Operation | `+ move_to(self, new_state: OfferState) -> None` | Matches code |

## OrderLine

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Retain item/name/price/quantity snapshots and derive the line total. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ menu_item_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ item_name: str` | Matches code |
| Attribute | `+ unit_price: int` | Matches code |
| Attribute | `+ quantity: int` | Matches code |
| Attribute | `+ id: Optional[int]` | Matches code |

## Customer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Represent customer identity and permitted online payment choices. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | Matches code |
| Attribute | `+ user_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ full_name: str` | Matches code |
| Attribute | `+ phone: Optional[str]` | Matches code |
| Attribute | `+ email: Optional[str]` | Matches code |
| Attribute | `+ passport_no: Optional[str]` | Matches code |
| Attribute | `+ nationality: Optional[str]` | Matches code |
| Attribute | `+ customer_type: CustomerType` **inferred** | Matches code |

## LocalCustomer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Specialize the Customer type and permitted payment options for a local customer. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customer_type: CustomerType` **inferred** | Matches code |

## TouristCustomer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Specialize Customer identity and permitted payment options for a tourist. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customer_type: CustomerType` **inferred** | Matches code |

## Address

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Hold an owned delivery location and archive flag. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | Matches code |
| Attribute | `+ customer_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ label: str` | Matches code |
| Attribute | `+ full_address: str` | Matches code |
| Attribute | `+ district: str` | Matches code |
| Attribute | `+ latitude: float` | Matches code |
| Attribute | `+ longitude: float` | Matches code |
| Attribute | `+ archived_at: Optional[str]` | Matches code |

## MenuItem

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Hold current catalogue text, whole-VND price and archive flag. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | Matches code |
| Attribute | `+ brand_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ brand_name: str` | Matches code |
| Attribute | `+ name: str` | Matches code |
| Attribute | `+ description: str` | Matches code |
| Attribute | `+ price: int` | Matches code |
| Attribute | `+ archived_at: Optional[str]` | Matches code |

## Brand

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Group menu items and retain the archived brand identity. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | Matches code |
| Attribute | `+ name: str` | Matches code |
| Attribute | `+ archived_at: Optional[str]` | Matches code |

## HubMenuItem

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Represent one hub listing and its independent availability. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hub_id: int` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ item: MenuItem` | Matches code |
| Attribute | `+ is_available: bool` | Matches code |

## UserAccount

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Hold account identity, role, active flag and optional kitchen-hub assignment. |
| Class status | Changed during implementation and tested (P4.1; Table P4-1 rows 53) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | Matches code |
| Attribute | `+ username: str` | Matches code |
| Attribute | `+ password_hash: str` | Matches code |
| Attribute | `+ display_name: str` | Matches code |
| Attribute | `+ role: Role` | Matches code |
| Attribute | `+ is_active: bool` | Matches code |
| Attribute | `+ hub_id: Optional[int]` (FK retained here; omitted from DCD) | Matches code |
| Attribute | `+ created_at: str` | Changed during implementation and tested (P4.1; Table P4-1 rows 53); Reason:  |

## OrderState

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ PLACED: str` **inferred** | Matches code |
| Attribute | `+ CONFIRMED: str` **inferred** | Matches code |
| Attribute | `+ REJECTED: str` **inferred** | Matches code |
| Attribute | `+ PREPARING: str` **inferred** | Matches code |
| Attribute | `+ READY: str` **inferred** | Matches code |
| Attribute | `+ OUT_FOR_DELIVERY: str` **inferred** | Matches code |
| Attribute | `+ DELIVERED: str` **inferred** | Matches code |
| Attribute | `+ DELIVERY_FAILED: str` **inferred** | Matches code |
| Attribute | `+ CANCELLED: str` **inferred** | Matches code |
| Enumeration | PLACED, CONFIRMED, REJECTED, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, CANCELLED | Matches code |

## PaymentState

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ PENDING: str` **inferred** | Matches code |
| Attribute | `+ PAID: str` **inferred** | Matches code |
| Attribute | `+ FAILED: str` **inferred** | Matches code |
| Attribute | `+ VOIDED: str` **inferred** | Matches code |
| Attribute | `+ REFUND_PENDING: str` **inferred** | Matches code |
| Attribute | `+ REFUNDED: str` **inferred** | Matches code |
| Enumeration | PENDING, PAID, FAILED, VOIDED, REFUND_PENDING, REFUNDED | Matches code |

## PaymentMethod

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ COD: str` **inferred** | Matches code |
| Attribute | `+ ONLINE: str` **inferred** | Matches code |
| Enumeration | COD, ONLINE | Matches code |

## OnlineOption

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ E_WALLET: str` **inferred** | Matches code |
| Attribute | `+ BANK_QR: str` **inferred** | Matches code |
| Attribute | `+ INTERNATIONAL_CARD: str` **inferred** | Matches code |
| Enumeration | E_WALLET, BANK_QR, INTERNATIONAL_CARD | Matches code |

## OfferState

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ OFFERED: str` **inferred** | Matches code |
| Attribute | `+ ACCEPTED: str` **inferred** | Matches code |
| Attribute | `+ DECLINED: str` **inferred** | Matches code |
| Attribute | `+ WITHDRAWN: str` **inferred** | Matches code |
| Enumeration | OFFERED, ACCEPTED, DECLINED, WITHDRAWN | Matches code |

## Role

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ CUSTOMER: str` **inferred** | Matches code |
| Attribute | `+ KITCHEN_STAFF: str` **inferred** | Matches code |
| Attribute | `+ SHIPPER: str` **inferred** | Matches code |
| Attribute | `+ ADMIN: str` **inferred** | Matches code |
| Attribute | `+ MANAGER: str` **inferred** | Matches code |
| Enumeration | CUSTOMER, KITCHEN_STAFF, SHIPPER, ADMIN, MANAGER | Matches code |

## KitchenBoard

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/kitchen_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hub: Hub` | Matches code |
| Attribute | `+ columns: dict[OrderState, list[BoardEntry]]` | Matches code |

## BoardEntry

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/kitchen_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order: Order` | Matches code |
| Attribute | `+ awaiting_customer: bool` | Matches code |

## KitchenOrderView

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/kitchen_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order: Order` | Matches code |
| Attribute | `+ payment: Payment` | Matches code |
| Attribute | `+ open_offer: Optional[ReplacementOffer]` | Matches code |
| Attribute | `+ offers: list[ReplacementOffer]` | Matches code |
| Attribute | `+ candidates: dict[int, list[MenuItem]]` | Matches code |

## OrderSummary

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/order_tracking_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order: Order` | Matches code |
| Attribute | `+ hub_name: str` | Matches code |
| Attribute | `+ awaiting_answer: bool` | Matches code |

## Hub

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Represent a kitchen location, capacity and fee. |
| Class status | Changed during implementation and tested (P4.3; Table P4-1 rows 7, 8) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | Matches code |
| Attribute | `+ code: str` | Matches code |
| Attribute | `+ name: str` | Matches code |
| Attribute | `+ address_text: str` | Matches code |
| Attribute | `+ latitude: float` | Matches code |
| Attribute | `+ longitude: float` | Matches code |
| Attribute | `+ max_active_orders: int` | Matches code |
| Attribute | `+ base_delivery_fee: int` | Matches code |
| Attribute | `+ archived_at: Optional[str]` | Matches code |

## CustomerType

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ LOCAL: str` **inferred** | Matches code |
| Attribute | `+ TOURIST: str` **inferred** | Matches code |
| Enumeration | LOCAL, TOURIST | Matches code |

## Presentation adapter and resources

The `order` / `kitchen` identifiers are actual Flask blueprint modules (`saigonbite/presentation/blueprints/*.py`); each route remains its actual Python function and HTTP rule. The SSD operation is translated at this boundary; session identity and route/form fields supply the controller arguments.

Templates used by the selected blueprint module(s): `kitchen/availability.html`, `kitchen/board.html`, `kitchen/order.html`, `order/confirmation.html`, `order/detail.html`, `order/hubs.html`, `order/menu.html`, `order/my_orders.html`, `order/payment_simulator.html`, `order/quote.html`.

Non-persisted values include Quote, PaymentChoice, HubStatus, response dataclasses and Authorisation. Busy/quiet are derived properties; no Busy/Quiet enum is introduced. No refund payout is designed.
