# UC-05 design classes

Author: 722I0004 · AI-assisted (Codex)

Static source: C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`; shared source `models/shared/design_model.json`. MATCH records static correspondence. † P4-TARGET/GAP records a required design change, never implementation. Tables retain relation identifiers for exact static mapping; DCDs replace domain FK scalars with associations. Fields are public unless leading underscore; Python dataclasses are not assigned invented private visibility.

Properties have signatures for traceability but are read as attributes; dataclass «create» means implicit initialization, not an invented business method. Unannotated types are marked inferred. Templates are presentation resources, not design classes.

## KitchenController

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «controller» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/business/controllers/kitchen_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hubs: HubDAO` **inferred** | MATCH |
| Attribute | `+ menu: MenuDAO` **inferred** | MATCH |
| Attribute | `+ orders: OrderDAO` **inferred** | MATCH |
| Attribute | `+ payments: PaymentDAO` **inferred** | MATCH |
| Attribute | `+ deliveries: DeliveryDAO` **inferred** | MATCH |
| Attribute | `+ offers: ReplacementOfferDAO` **inferred** | MATCH |
| Operation | `+ board(self, user_id: int) -> KitchenBoard` | MATCH |
| Operation | `+ get_order(self, user_id: int, order_id: int) -> KitchenOrderView` | MATCH |
| Operation | `+ confirm_order(self, user_id: int, order_id: int) -> Order†` | P4-TARGET† — P2-S13; P3-S03; Guarded writes must check rowcount and handle busy / commit failure without partial effects; shared helper is currently incomplete. |
| Operation | `+ reject_order(self, user_id: int, order_id: int, reason: str) -> Order†` | P4-TARGET† — F-02; P2-S13; BR-17 full C refund owed and atomic state/amount writes, including COMMIT rollback. |
| Operation | `+ offer_replacement(self, user_id: int, order_id: int, order_line_id: int, new_menu_item_id: int) -> ReplacementOffer†` | P4-TARGET† — F-05; P2-S09; P2-S13; Require currently unavailable source; target active/listed/available; one open offer; check every conditional save result. |

## kitchen

| Detail | Design |
|---|---|
| Layer / stereotype | view / «view» |
| Responsibility | Translate own-hub kitchen actions and render their results. |
| Class status | MATCH (Static) |
| Source | `saigonbite/presentation/kitchen.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ board() -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |
| Operation | `+ order(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |
| Operation | `+ confirm(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |
| Operation | `+ reject(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |
| Operation | `+ offer(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |

## HubDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/hub_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ get_including_archived(self, hub_id: int) -> Optional[Hub]` | MATCH |
| Operation | `+ list_menu(self, hub_id: int) -> list[HubMenuItem]` | MATCH |
| Operation | `+ get_available_item(self, hub_id: int, menu_item_id: int) -> Optional[MenuItem]` | MATCH |

## OrderDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/data_access/order_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `- _load(self, row: Optional[sqlite3.Row]) -> Optional[Order]` | MATCH |
| Operation | `+ list_for_hub(self, hub_id: int, states: Iterable[OrderState]) -> list[Order]` | MATCH |
| Operation | `+ get_by_id(self, order_id: int) -> Optional[Order]` | MATCH |
| Operation | `+ change_state(self, order_id: int, from_state: OrderState, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> bool` | MATCH |
| Operation | `+ list_for_customer(self, customer_id: int) -> list[Order]` | MATCH |
| Operation | `+ save_lines_and_totals(self, order: Order) -> bool†` | P4-TARGET† — P2-S09; P2-S11; P3-S03; Apply replacement only to expected PLACED order and check each affected line/header rowcount. |

## ReplacementOfferDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/offer_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ get_open(self, order_id: int) -> Optional[ReplacementOffer]` | MATCH |
| Operation | `+ list_for_order(self, order_id: int) -> list[ReplacementOffer]` | MATCH |
| Operation | `+ decide(self, offer_id: int, to_state: OfferState, now: str) -> bool` | MATCH |
| Operation | `+ insert(self, offer: ReplacementOffer) -> int` | MATCH |

## UserDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/user_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ get_by_id(self, user_id: int) -> Optional[UserAccount]` | MATCH |

## PaymentDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/data_access/payment_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ get_by_order_id(self, order_id: int) -> Optional[Payment]` | MATCH |
| Operation | `+ change_state(self, order_id: int, from_state: PaymentState, to_state: PaymentState, now: str) -> bool` | MATCH |
| Operation | `+ set_amounts(self, order_id: int, amount: int, refund_amount: int, now: str) -> bool†` | P4-TARGET† — F-02; P3-S03; Persist full/partial refund obligations atomically and expose the conditional save outcome. |

## Order

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Own the order lifecycle, snapshots and accepted replacement totals. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customer_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ hub_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ address_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ state: OrderState` | MATCH |
| Attribute | `+ delivery_fee: int` | MATCH |
| Attribute | `+ idempotency_token: str` | MATCH |
| Attribute | `+ placed_at: str` | MATCH |
| Attribute | `+ lines: list[OrderLine]` | MATCH |
| Attribute | `+ id: Optional[int]` | MATCH |
| Attribute | `+ archived_at: Optional[str]` | MATCH |
| Attribute | `+ delivery_address_text: str` | MATCH |
| Attribute | `+ distance_km: float` | MATCH |
| Attribute | `+ voucher_id: Optional[int]` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ voucher_discount: int` | MATCH |
| Attribute | `+ quiet_discount: int` | MATCH |
| Attribute | `+ reject_reason: Optional[str]` | MATCH |
| Attribute | `+ confirmed_at: Optional[str]` | MATCH |
| Attribute | `+ ready_at: Optional[str]` | MATCH |
| Attribute | `+ closed_at: Optional[str]` | MATCH |
| Operation | `+ move_to(self, new_state: OrderState) -> None` | MATCH |
| Operation | `+ line(self, line_id: int) -> Optional[OrderLine]` | MATCH |
| Operation | `+ replace_line(self, line_id: int, menu_item_id: int, item_name: str, unit_price: int) -> None` | MATCH |
| Read-only property | `+ total(self) -> int {property; read as .total}` | MATCH |

## Payment

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Hold captured amount C and refund obligations without claiming payout. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ method: PaymentMethod` | MATCH |
| Attribute | `+ state: PaymentState` | MATCH |
| Attribute | `+ amount: int` | MATCH |
| Attribute | `+ created_at: str` | MATCH |
| Attribute | `+ updated_at: Optional[str]` | MATCH |
| Attribute | `+ online_option: Optional[OnlineOption]` | MATCH |
| Attribute | `+ provider_ref: Optional[str]` | MATCH |
| Attribute | `+ refund_amount: int` | MATCH |
| Attribute | `+ id: Optional[int]` | MATCH |
| Operation | `+ release_for_unfulfilled_order(self) -> None†` | P4-TARGET† — F-02; P2-S01; Set refund_amount=C with REFUND_PENDING; preserve COD VOIDED; no payout operation. |

## OrderTrackingController

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «controller» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/business/controllers/order_tracking_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customers: CustomerDAO` **inferred** | MATCH |
| Attribute | `+ orders: OrderDAO` **inferred** | MATCH |
| Attribute | `+ payments: PaymentDAO` **inferred** | MATCH |
| Attribute | `+ hubs: HubDAO` **inferred** | MATCH |
| Attribute | `+ deliveries: DeliveryDAO` **inferred** | MATCH |
| Attribute | `+ offers: ReplacementOfferDAO` **inferred** | MATCH |
| Operation | `+ list_my_orders(self, user_id: int) -> list[OrderSummary]` | MATCH |
| Operation | `+ get_order(self, user_id: int, order_id: int) -> OrderDetail` | MATCH |
| Operation | `+ answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail†` | P4-TARGET† — F-05; F-02; P2-S09; P2-S11; P2-S13; Recheck PLACED and exact open offer; recheck target; invalid target withdraws only the offer; valid accept uses offered price; controlled rollback through COMMIT. |
| Operation | `- _own_order(self, customer: Customer, order_id: int) -> Order` | MATCH |
| Operation | `- _require_customer(self, user_id: int) -> Customer` | MATCH |

## order

| Detail | Design |
|---|---|
| Layer / stereotype | view / «view» |
| Responsibility | Translate authenticated customer routes and render quote, receipt and order results. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/presentation/order.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ my_orders() -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |
| Operation | `+ detail(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |
| Operation | `+ answer_replacement(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |

## CustomerDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/customer_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ get_by_user_id(self, user_id: int) -> Optional[Customer]` | MATCH |

## OrderDetail

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/order_tracking_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order: Order` | MATCH |
| Attribute | `+ payment: Payment` | MATCH |
| Attribute | `+ hub: Hub` | MATCH |
| Attribute | `+ delivery: Optional[Delivery]` | MATCH |
| Attribute | `+ open_offer: Optional[ReplacementOffer]` | MATCH |
| Attribute | `+ offers: list[ReplacementOffer]` | MATCH |
| Read-only property | `+ total_if_accepted(self) -> Optional[int] {property; read as .total_if_accepted}` | MATCH |

## DeliveryDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/delivery_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ get_by_order_id(self, order_id: int) -> Optional[Delivery]` | MATCH |

## controllers.common

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «module» |
| Responsibility | Module functions with their original Python signatures. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/business/controllers/common.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ move_order(orders: OrderDAO, order: Order, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> None` | MATCH |
| Operation | `+ release_payment(payments: PaymentDAO, order_id: int, now: str) -> Payment†` | P4-TARGET† — F-02; P2-S01; P3-S03; Persist full captured C as refund_amount together with state; changing only the domain object does not save the amount. Check conditional save results in the same transaction. |

## ReplacementOffer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Hold one proposed whole-line replacement and its decision history. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ order_line_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ original_item_name: str` | MATCH |
| Attribute | `+ original_unit_price: int` | MATCH |
| Attribute | `+ new_menu_item_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ new_item_name: str` | MATCH |
| Attribute | `+ new_unit_price: int` | MATCH |
| Attribute | `+ state: OfferState` | MATCH |
| Attribute | `+ offered_at: str` | MATCH |
| Attribute | `+ decided_at: Optional[str]` | MATCH |
| Attribute | `+ id: Optional[int]` | MATCH |
| Operation | `+ move_to(self, new_state: OfferState) -> None` | MATCH |

## OrderLine

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Retain item/name/price/quantity snapshots and derive the line total. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ menu_item_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ item_name: str` | MATCH |
| Attribute | `+ unit_price: int` | MATCH |
| Attribute | `+ quantity: int` | MATCH |
| Attribute | `+ id: Optional[int]` | MATCH |

## Customer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Represent customer identity and permitted online payment choices. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ user_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ full_name: str` | MATCH |
| Attribute | `+ phone: Optional[str]` | MATCH |
| Attribute | `+ email: Optional[str]` | MATCH |
| Attribute | `+ passport_no: Optional[str]` | MATCH |
| Attribute | `+ nationality: Optional[str]` | MATCH |
| Attribute | `+ customer_type: CustomerType` **inferred** | MATCH |

## LocalCustomer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Specialize the Customer type and permitted payment options for a local customer. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customer_type: CustomerType` **inferred** | MATCH |

## TouristCustomer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Specialize Customer identity and permitted payment options for a tourist. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customer_type: CustomerType` **inferred** | MATCH |

## Address

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Hold an owned delivery location and archive flag. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ customer_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ label: str` | MATCH |
| Attribute | `+ full_address: str` | MATCH |
| Attribute | `+ district: str` | MATCH |
| Attribute | `+ latitude: float` | MATCH |
| Attribute | `+ longitude: float` | MATCH |
| Attribute | `+ archived_at: Optional[str]` | MATCH |

## MenuItem

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Hold current catalogue text, whole-VND price and archive flag. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ brand_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ brand_name: str` | MATCH |
| Attribute | `+ name: str` | MATCH |
| Attribute | `+ description: str` | MATCH |
| Attribute | `+ price: int` | MATCH |
| Attribute | `+ archived_at: Optional[str]` | MATCH |

## Brand

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Group menu items and retain the archived brand identity. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ name: str` | MATCH |
| Attribute | `+ archived_at: Optional[str]` | MATCH |

## HubMenuItem

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Represent one hub listing and its independent availability. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hub_id: int` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ item: MenuItem` | MATCH |
| Attribute | `+ is_available: bool` | MATCH |

## UserAccount

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Hold account identity, role, active flag and optional kitchen-hub assignment. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ username: str` | MATCH |
| Attribute | `+ password_hash: str` | MATCH |
| Attribute | `+ display_name: str` | MATCH |
| Attribute | `+ role: Role` | MATCH |
| Attribute | `+ is_active: bool` | MATCH |
| Attribute | `+ hub_id: Optional[int]` (FK retained here; omitted from DCD) | MATCH |
| Attribute | `+ created_at: str` | GAP |

## OrderState

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ PLACED: str` **inferred** | MATCH |
| Attribute | `+ CONFIRMED: str` **inferred** | MATCH |
| Attribute | `+ REJECTED: str` **inferred** | MATCH |
| Attribute | `+ PREPARING: str` **inferred** | MATCH |
| Attribute | `+ READY: str` **inferred** | MATCH |
| Attribute | `+ OUT_FOR_DELIVERY: str` **inferred** | MATCH |
| Attribute | `+ DELIVERED: str` **inferred** | MATCH |
| Attribute | `+ DELIVERY_FAILED: str` **inferred** | MATCH |
| Attribute | `+ CANCELLED: str` **inferred** | MATCH |
| Enumeration | PLACED, CONFIRMED, REJECTED, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, CANCELLED | MATCH |

## PaymentState

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ PENDING: str` **inferred** | MATCH |
| Attribute | `+ PAID: str` **inferred** | MATCH |
| Attribute | `+ FAILED: str` **inferred** | MATCH |
| Attribute | `+ VOIDED: str` **inferred** | MATCH |
| Attribute | `+ REFUND_PENDING: str` **inferred** | MATCH |
| Attribute | `+ REFUNDED: str` **inferred** | MATCH |
| Enumeration | PENDING, PAID, FAILED, VOIDED, REFUND_PENDING, REFUNDED | MATCH |

## PaymentMethod

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ COD: str` **inferred** | MATCH |
| Attribute | `+ ONLINE: str` **inferred** | MATCH |
| Enumeration | COD, ONLINE | MATCH |

## OnlineOption

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ E_WALLET: str` **inferred** | MATCH |
| Attribute | `+ BANK_QR: str` **inferred** | MATCH |
| Attribute | `+ INTERNATIONAL_CARD: str` **inferred** | MATCH |
| Enumeration | E_WALLET, BANK_QR, INTERNATIONAL_CARD | MATCH |

## OfferState

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ OFFERED: str` **inferred** | MATCH |
| Attribute | `+ ACCEPTED: str` **inferred** | MATCH |
| Attribute | `+ DECLINED: str` **inferred** | MATCH |
| Attribute | `+ WITHDRAWN: str` **inferred** | MATCH |
| Enumeration | OFFERED, ACCEPTED, DECLINED, WITHDRAWN | MATCH |

## Role

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ CUSTOMER: str` **inferred** | MATCH |
| Attribute | `+ KITCHEN_STAFF: str` **inferred** | MATCH |
| Attribute | `+ SHIPPER: str` **inferred** | MATCH |
| Attribute | `+ ADMIN: str` **inferred** | MATCH |
| Attribute | `+ MANAGER: str` **inferred** | MATCH |
| Enumeration | CUSTOMER, KITCHEN_STAFF, SHIPPER, ADMIN, MANAGER | MATCH |

## KitchenBoard

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/kitchen_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hub: Hub` | MATCH |
| Attribute | `+ columns: dict[OrderState, list[BoardEntry]]` | MATCH |

## BoardEntry

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/kitchen_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order: Order` | MATCH |
| Attribute | `+ awaiting_customer: bool` | MATCH |

## KitchenOrderView

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/kitchen_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order: Order` | MATCH |
| Attribute | `+ payment: Payment` | MATCH |
| Attribute | `+ open_offer: Optional[ReplacementOffer]` | MATCH |
| Attribute | `+ offers: list[ReplacementOffer]` | MATCH |
| Attribute | `+ candidates: dict[int, list[MenuItem]]` | MATCH |

## OrderSummary

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/order_tracking_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order: Order` | MATCH |
| Attribute | `+ hub_name: str` | MATCH |
| Attribute | `+ awaiting_answer: bool` | MATCH |

## Hub

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Represent a kitchen location, capacity and fee. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ code: str` | MATCH |
| Attribute | `+ name: str` | MATCH |
| Attribute | `+ address_text: str` | MATCH |
| Attribute | `+ latitude: float` | MATCH |
| Attribute | `+ longitude: float` | MATCH |
| Attribute | `+ max_active_orders: int` | MATCH |
| Attribute | `+ base_delivery_fee: int` | MATCH |
| Attribute | `+ archived_at: Optional[str]` | MATCH |

## CustomerType

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ LOCAL: str` **inferred** | MATCH |
| Attribute | `+ TOURIST: str` **inferred** | MATCH |
| Enumeration | LOCAL, TOURIST | MATCH |

## Presentation adapter and resources

The `order` / `kitchen` identifiers are actual Flask blueprint modules (`saigonbite/presentation/blueprints/*.py`); each route remains its actual Python function and HTTP rule. The SSD operation is translated at this boundary; session identity and route/form fields supply the controller arguments.

Templates used by the selected blueprint module(s): `kitchen/availability.html`, `kitchen/board.html`, `kitchen/order.html`, `order/confirmation.html`, `order/detail.html`, `order/hubs.html`, `order/menu.html`, `order/my_orders.html`, `order/payment_simulator.html`, `order/quote.html`.

Non-persisted values include Quote, PaymentChoice, HubStatus, response dataclasses and Authorisation. Busy/quiet are derived properties; no Busy/Quiet enum is introduced. No refund payout is designed.
