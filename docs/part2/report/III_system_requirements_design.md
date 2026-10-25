# III. System Requirements Design (15 marks)

Author: 722I0004 · AI-assisted (Codex)

This section assigns each frozen SSD operation to a view route, controller and collaborating domain objects. MATCH is static correspondence at C0; † P4-TARGET/GAP elements describe the target and its named P4 input. No runtime result is claimed. All landscape figures must retain their specified 230 mm width in the final report.

## 3.1 Design for Use Case 1: Place an order with an accepted full price, voucher and payment choice (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

This package is a target design at committed C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`. Read it with the frozen UC description/SSD/state views. It makes no runtime or implementation claim for † behavior.

### 3.1.1 Design Classes in Detailed Design

##### UC-01 design classes

Author: 722I0004 · AI-assisted (Codex)

Static source: C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`; shared source `models/shared/design_model.json`. MATCH records static correspondence. † P4-TARGET/GAP records a required design change, never implementation. Tables retain relation identifiers for exact static mapping; DCDs replace domain FK scalars with associations. Fields are public unless leading underscore; Python dataclasses are not assigned invented private visibility.

Properties have signatures for traceability but are read as attributes; dataclass «create» means implicit initialization, not an invented business method. Unannotated types are marked inferred. Templates are presentation resources, not design classes.

##### PlaceOrderController

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «controller» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/business/controllers/place_order_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customers: CustomerDAO` **inferred** | MATCH |
| Attribute | `+ hubs: HubDAO` **inferred** | MATCH |
| Attribute | `+ orders: OrderDAO` **inferred** | MATCH |
| Attribute | `+ payments: PaymentDAO` **inferred** | MATCH |
| Attribute | `+ vouchers: VoucherDAO` **inferred** | MATCH |
| Attribute | `+ gateway: Any` **inferred** | MATCH |
| Operation | `+ list_hubs(self) -> list[HubStatus]` | MATCH |
| Operation | `+ select_hub(self, user_id: int, hub_id: int) -> HubMenuView` | MATCH |
| Operation | `+ request_quote(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None) -> Quote†` | P4-TARGET† — F-04; F-07; P3-S01; Use raw distance; include payment choice and a full quote fingerprint; rank suggestions by load ratio, distance and ID. |
| Operation | `+ confirm_order(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], idempotency_token: str, quoted_total: Optional[int] = None, voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None, quote_fingerprint: Optional[str] = None) -> OrderConfirmation†` | P4-TARGET† — F-04; F-07; P2-S05; P2-S13; Compare full fingerprint and T; release simulator authorization on every failure through COMMIT. |
| Operation | `- _build_quote(self, customer: Customer, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], voucher_code: Optional[str]) -> Quote` | MATCH |
| Operation | `+ suggest_hubs(self, exclude_hub_id: int, address: Optional[Address]) -> list[HubStatus]†` | P4-TARGET† — P3-S01; F-04; Draft sorts by load ratio then ID; BR-04 requires distance as the second key and raw distance for range. |
| Operation | `- _require_customer(self, user_id: int) -> Customer` | MATCH |
| Operation | `- _check_payment_choice(customer: Customer, payment: PaymentChoice) -> None` | MATCH |

##### order

| Detail | Design |
|---|---|
| Layer / stereotype | view / «view» |
| Responsibility | Translate authenticated customer routes and render quote, receipt and order results. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/presentation/order.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ choose_hub() -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |
| Operation | `+ choose_items(hub_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |
| Operation | `+ quote() -> Any [inferred return]†` **inferred unannotated parameter/return** | P4-TARGET† — F-07; Pass payment choice into target quoting and render the full fingerprint. |
| Operation | `+ confirm() -> Any [inferred return]†` **inferred unannotated parameter/return** | P4-TARGET† — F-07; P2-S05; Bind the posted fingerprint/payment choice to the target confirm method; retain controlled results through COMMIT. |
| Operation | `+ detail(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |
| Operation | `+ my_orders() -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |
| Operation | `+ cancel(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | MATCH |

##### HubStatus

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Derive busy, quiet and load percentage from current load and capacity. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hub: Hub` | MATCH |
| Attribute | `+ load: int` | MATCH |
| Read-only property | `+ busy(self) -> bool {property; read as .busy}` | MATCH |
| Read-only property | `+ quiet(self) -> bool {property; read as .quiet}` | MATCH |

##### HubDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/hub_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ active_loads(self) -> dict[int, int]` | MATCH |
| Operation | `+ list_active(self) -> list[Hub]` | MATCH |
| Operation | `+ active_load(self, hub_id: int) -> int` | MATCH |
| Operation | `+ get(self, hub_id: int) -> Optional[Hub]` | MATCH |
| Operation | `+ list_menu(self, hub_id: int) -> list[HubMenuItem]` | MATCH |
| Operation | `+ get_available_item(self, hub_id: int, menu_item_id: int) -> Optional[MenuItem]` | MATCH |
| Operation | `+ get_including_archived(self, hub_id: int) -> Optional[Hub]` | MATCH |

##### CustomerDAO

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
| Operation | `+ list_addresses(self, customer_id: int) -> list[Address]` | MATCH |
| Operation | `+ get_address(self, address_id: int, customer_id: int) -> Optional[Address]` | MATCH |

##### UserDAO

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

##### Hub

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
| Operation | `+ distance_to(self, address: Address) -> float†` | P4-TARGET† — F-04; Keep raw Haversine precision through the radius and fee decisions; round only presentation/storage. |

##### Quote

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Compute and bind the complete consented price; not persisted. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hub: Hub` | MATCH |
| Attribute | `+ address: Address` | MATCH |
| Attribute | `+ lines: list[OrderLine]` | MATCH |
| Attribute | `+ distance_km: float` | MATCH |
| Attribute | `+ delivery_fee: int` | MATCH |
| Attribute | `+ quiet_discount: int` | MATCH |
| Attribute | `+ voucher: Optional[Voucher]` | MATCH |
| Attribute | `+ voucher_discount: int` | MATCH |
| Operation | `+ fingerprint(self, payment_method: PaymentMethod, online_option: Optional[OnlineOption] = None) -> str†` | GAP† — F-07; Bind all consent fields with pure-domain enum inputs; the controller adapts PaymentChoice. |
| Read-only property | `+ total(self) -> int {property; read as .total}` | MATCH |

##### Voucher

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Check date/subtotal eligibility and calculate the bounded discount. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ code: str` | MATCH |
| Attribute | `+ description: str` | MATCH |
| Attribute | `+ discount_type: DiscountType` | MATCH |
| Attribute | `+ discount_value: int` | MATCH |
| Attribute | `+ min_subtotal: int` | MATCH |
| Attribute | `+ max_discount: Optional[int]` | MATCH |
| Attribute | `+ valid_from: str` | MATCH |
| Attribute | `+ valid_until: str` | MATCH |
| Attribute | `+ archived_at: Optional[str]` | MATCH |
| Operation | `+ discount_for(self, item_subtotal: int) -> int` | MATCH |
| Operation | `+ problem(self, item_subtotal: int, today: str) -> Optional[str]` | MATCH |

##### VoucherDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/voucher_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ get_by_code(self, code: str) -> Optional[Voucher]` | MATCH |

##### Order

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
| Operation | `+ place(cls, customer_id: int, quote: Quote, idempotency_token: str, placed_at: str) -> 'Order'` | MATCH |
| Operation | `+ move_to(self, new_state: OrderState) -> None` | MATCH |
| Operation | `+ replace_line(self, line_id: int, menu_item_id: int, item_name: str, unit_price: int) -> None` | MATCH |
| Operation | `+ line(self, line_id: int) -> Optional[OrderLine]` | MATCH |

##### PaymentGatewaySimulator

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «gateway» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/payment_gateway.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ authorise(self, amount: int, option: OnlineOption, outcome: str) -> Authorisation` | MATCH |
| Operation | `+ release(self, reference: str) -> None` | MATCH |

##### OrderDAO

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
| Operation | `+ get_by_id(self, order_id: int) -> Optional[Order]` | MATCH |
| Operation | `+ get_by_token(self, token: str) -> Optional[Order]` | MATCH |
| Operation | `+ insert(self, order: Order) -> int` | MATCH |
| Operation | `+ list_for_customer(self, customer_id: int) -> list[Order]` | MATCH |
| Operation | `+ change_state(self, order_id: int, from_state: OrderState, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> bool` | MATCH |

##### PaymentDAO

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
| Operation | `+ insert(self, payment: Payment) -> int` | MATCH |
| Operation | `+ change_state(self, order_id: int, from_state: PaymentState, to_state: PaymentState, now: str) -> bool` | MATCH |
| Operation | `+ set_amounts(self, order_id: int, amount: int, refund_amount: int, now: str) -> bool†` | P4-TARGET† — F-02; P3-S03; Persist full/partial refund obligations atomically and expose the conditional save outcome. |

##### OrderTrackingController

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
| Operation | `+ get_order(self, user_id: int, order_id: int) -> OrderDetail` | MATCH |
| Operation | `+ list_my_orders(self, user_id: int) -> list[OrderSummary]` | MATCH |
| Operation | `+ cancel_order(self, user_id: int, order_id: int) -> OrderDetail†` | P4-TARGET† — F-02; P2-S13; BR-17 full C refund owed and atomic state/amount writes, including COMMIT rollback. |
| Operation | `- _own_order(self, customer: Customer, order_id: int) -> Order` | MATCH |
| Operation | `- _require_customer(self, user_id: int) -> Customer` | MATCH |

##### DeliveryDAO

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

##### ReplacementOfferDAO

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

##### Payment

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

##### controllers.common

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

##### ReplacementOffer

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

##### OrderLine

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

##### Customer

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

##### LocalCustomer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Specialize the Customer type and permitted payment options for a local customer. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customer_type: CustomerType` **inferred** | MATCH |

##### TouristCustomer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Specialize Customer identity and permitted payment options for a tourist. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customer_type: CustomerType` **inferred** | MATCH |

##### Address

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

##### MenuItem

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

##### Brand

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

##### HubMenuItem

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

##### UserAccount

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

##### OrderState

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

##### PaymentState

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

##### PaymentMethod

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

##### OnlineOption

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

##### OfferState

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

##### Role

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

##### PaymentChoice

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/place_order_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ method: PaymentMethod` | MATCH |
| Attribute | `+ option: Optional[OnlineOption]` | MATCH |
| Attribute | `+ outcome: Optional[str]` | MATCH |

##### OrderConfirmation

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/place_order_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order: Order` | MATCH |
| Attribute | `+ payment: Payment` | MATCH |
| Attribute | `+ hub: Hub` | MATCH |
| Attribute | `+ created: bool` | MATCH |

##### HubMenuView

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/place_order_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hub: Hub` | MATCH |
| Attribute | `+ status: HubStatus` | MATCH |
| Attribute | `+ menu: list[HubMenuItem]` | MATCH |
| Attribute | `+ addresses: list[Address]` | MATCH |

##### OrderDetail

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

##### OrderSummary

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

##### Authorisation

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «value» |
| Responsibility | Carry the local simulator decision, reference and message; not persisted. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/payment_gateway.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ approved: bool` | MATCH |
| Attribute | `+ reference: Optional[str]` | MATCH |
| Attribute | `+ message: str` | MATCH |

##### domain.rules

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «module» |
| Responsibility | Module functions with their original Python signatures. |
| Class status | P4-TARGET (Static) |
| Source | `saigonbite/business/domain/rules.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ delivery_fee(base_fee: int, km: float) -> int` | MATCH |
| Operation | `+ quiet_discount(load: int, capacity: int, fee: int) -> int` | MATCH |

##### DiscountType

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ FIXED: str` **inferred** | MATCH |
| Attribute | `+ PERCENT: str` **inferred** | MATCH |
| Enumeration | FIXED, PERCENT | MATCH |

##### CustomerType

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

##### Presentation adapter and resources

The `order` / `kitchen` identifiers are actual Flask blueprint modules (`saigonbite/presentation/blueprints/*.py`); each route remains its actual Python function and HTTP rule. The SSD operation is translated at this boundary; session identity and route/form fields supply the controller arguments.

Templates used by the selected blueprint module(s): `order/confirmation.html`, `order/detail.html`, `order/hubs.html`, `order/menu.html`, `order/my_orders.html`, `order/payment_simulator.html`, `order/quote.html`.

Non-persisted values include Quote, PaymentChoice, HubStatus, response dataclasses and Authorisation. Busy/quiet are derived properties; no Busy/Quiet enum is introduced. No refund payout is designed.


### 3.1.2 Design Class Diagram

#### i. Domain design class

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-01 domain — selected design members 1/4](../../../models/UC-01/dcd_uc01_domain_PartA.png)

Figure 3.1.2.iA. UC-01 domain detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 domain — selected design members 2/4](../../../models/UC-01/dcd_uc01_domain_PartB.png)

Figure 3.1.2.iB. UC-01 domain detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 domain — selected design members 3/4](../../../models/UC-01/dcd_uc01_domain_PartC.png)

Figure 3.1.2.iC. UC-01 domain detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 domain — selected design members 4/4](../../../models/UC-01/dcd_uc01_domain_PartD.png)

Figure 3.1.2.iD. UC-01 domain detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 domain — relationships 1](../../../models/UC-01/dcd_uc01_domain_links_PartA.png)

Figure 3.1.2.i.R1. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 domain — relationships 2](../../../models/UC-01/dcd_uc01_domain_links_PartB.png)

Figure 3.1.2.i.R2. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 domain — relationships 3](../../../models/UC-01/dcd_uc01_domain_links_PartC.png)

Figure 3.1.2.i.R3. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 domain — relationships 4](../../../models/UC-01/dcd_uc01_domain_links_PartD.png)

Figure 3.1.2.i.R4. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 domain — relationships 5](../../../models/UC-01/dcd_uc01_domain_links_PartE.png)

Figure 3.1.2.i.R5. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 domain — relationships 6](../../../models/UC-01/dcd_uc01_domain_links_PartF.png)

Figure 3.1.2.i.R6. UC-01 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

#### ii. Controller

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-01 controller — selected design members 1/2](../../../models/UC-01/dcd_uc01_controller_PartA.png)

Figure 3.1.2.iiA. UC-01 controller detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 controller — selected design members 2/2](../../../models/UC-01/dcd_uc01_controller_PartB.png)

Figure 3.1.2.iiB. UC-01 controller detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 controller — relationships 1](../../../models/UC-01/dcd_uc01_controller_links_PartA.png)

Figure 3.1.2.ii.R1. UC-01 controller navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

#### iii. UI (view)

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-01 view — selected design members 1/1](../../../models/UC-01/dcd_uc01_view.png)

Figure 3.1.2.iii. UC-01 view detailed design members — Author: 722I0004 · AI-assisted (Codex)

#### iv. Data access

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-01 dao — selected design members 1/2](../../../models/UC-01/dcd_uc01_dao_PartA.png)

Figure 3.1.2.ivA. UC-01 dao detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 dao — selected design members 2/2](../../../models/UC-01/dcd_uc01_dao_PartB.png)

Figure 3.1.2.ivB. UC-01 dao detailed design members — Author: 722I0004 · AI-assisted (Codex)

#### v. Design class (all layers together)

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-01 all — selected design members 1/9](../../../models/UC-01/dcd_uc01_all_PartA.png)

Figure 3.1.2.vA. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — selected design members 2/9](../../../models/UC-01/dcd_uc01_all_PartB.png)

Figure 3.1.2.vB. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — selected design members 3/9](../../../models/UC-01/dcd_uc01_all_PartC.png)

Figure 3.1.2.vC. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — selected design members 4/9](../../../models/UC-01/dcd_uc01_all_PartD.png)

Figure 3.1.2.vD. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — selected design members 5/9](../../../models/UC-01/dcd_uc01_all_PartE.png)

Figure 3.1.2.vE. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — selected design members 6/9](../../../models/UC-01/dcd_uc01_all_PartF.png)

Figure 3.1.2.vF. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — selected design members 7/9](../../../models/UC-01/dcd_uc01_all_PartG.png)

Figure 3.1.2.vG. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — selected design members 8/9](../../../models/UC-01/dcd_uc01_all_PartH.png)

Figure 3.1.2.vH. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — selected design members 9/9](../../../models/UC-01/dcd_uc01_all_PartI.png)

Figure 3.1.2.vI. UC-01 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 1](../../../models/UC-01/dcd_uc01_all_links_PartA.png)

Figure 3.1.2.v.R1. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 2](../../../models/UC-01/dcd_uc01_all_links_PartB.png)

Figure 3.1.2.v.R2. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 3](../../../models/UC-01/dcd_uc01_all_links_PartC.png)

Figure 3.1.2.v.R3. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 4](../../../models/UC-01/dcd_uc01_all_links_PartD.png)

Figure 3.1.2.v.R4. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 5](../../../models/UC-01/dcd_uc01_all_links_PartE.png)

Figure 3.1.2.v.R5. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 6](../../../models/UC-01/dcd_uc01_all_links_PartF.png)

Figure 3.1.2.v.R6. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 7](../../../models/UC-01/dcd_uc01_all_links_PartG.png)

Figure 3.1.2.v.R7. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 8](../../../models/UC-01/dcd_uc01_all_links_PartH.png)

Figure 3.1.2.v.R8. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 9](../../../models/UC-01/dcd_uc01_all_links_PartI.png)

Figure 3.1.2.v.R9. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 10](../../../models/UC-01/dcd_uc01_all_links_PartJ.png)

Figure 3.1.2.v.R10. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 11](../../../models/UC-01/dcd_uc01_all_links_PartK.png)

Figure 3.1.2.v.R11. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 12](../../../models/UC-01/dcd_uc01_all_links_PartL.png)

Figure 3.1.2.v.R12. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 13](../../../models/UC-01/dcd_uc01_all_links_PartM.png)

Figure 3.1.2.v.R13. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-01 all — relationships 14](../../../models/UC-01/dcd_uc01_all_links_PartN.png)

Figure 3.1.2.v.R14. UC-01 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

### 3.1.3 OOD with CRC Cards or Communication Diagram

##### UC-01 CRC cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators below resolve real AST constructor/function calls or typed collaborators from the shared model. A † operation is a root-annotated target; it is not a claim of code behavior. DAO collaborators appear here and in the DCD; Section III sequences intentionally defer persistence to 4.3.2.

##### PlaceOrderController

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PlaceOrderController | Knows customers, hubs, orders, payments, vouchers, gateway. Does list_hubs, select_hub, request_quote†, confirm_order†, _build_quote, suggest_hubs†, _require_customer, _check_payment_choice. Coordinate authorization, domain decisions and data access. | AuthorizationError, CustomerDAO, Hub, HubDAO, HubMenuView, HubStatus, HubUnavailableError, Order, OrderDAO, OrderLine, Payment, PaymentChoice, PaymentDAO, PaymentDeclinedError, Quote, QuoteChangedError, ValidationError, VoucherDAO, order |

##### order

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| order | Knows selected inputs. Does choose_hub, choose_items, quote†, confirm†, detail, my_orders, cancel. Translate authenticated customer routes and render quote, receipt and order results. | ValidationError |

##### HubStatus

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubStatus | Knows hub, load. Does busy, quiet. Derive busy, quiet and load percentage from current load and capacity. | HubMenuView, PlaceOrderController |

##### HubDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubDAO | Knows conn. Does active_loads, list_active, active_load, get, list_menu, get_available_item, get_including_archived. Read or write parameterized records. | Hub, HubMenuItem, MenuItem, OrderTrackingController, PlaceOrderController |

##### CustomerDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| CustomerDAO | Knows conn. Does get_by_user_id, list_addresses, get_address. Read or write parameterized records. | Address, OrderTrackingController, PlaceOrderController |

##### UserDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| UserDAO | Knows conn. Does get_by_id. Read or write parameterized records. | No outward application call; supplied/read by its typed owner. |

##### Hub

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Hub | Knows id, code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee, archived_at. Does distance_to†. Represent a kitchen location, capacity and fee. | HubDAO, HubMenuView, HubStatus, OrderConfirmation, OrderDetail, PlaceOrderController, Quote |

##### Quote

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Quote | Knows hub, address, lines, distance_km, delivery_fee, quiet_discount, voucher, voucher_discount. Does fingerprint†, total. Compute and bind the complete consented price; not persisted. | Order, PlaceOrderController |

Target collaborators for `fingerprint†`: **PaymentMethod** and **OnlineOption** (pure-domain enum values). The controller adapts PaymentChoice before the call; Quote has no controller-layer collaborator.

##### Voucher

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Voucher | Knows id, code, description, discount_type, discount_value, min_subtotal, max_discount, valid_from, valid_until, archived_at. Does discount_for, problem. Check date/subtotal eligibility and calculate the bounded discount. | PlaceOrderController, Quote, VoucherDAO |

##### VoucherDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| VoucherDAO | Knows conn. Does get_by_code. Read or write parameterized records. | PlaceOrderController |

##### Order

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Order | Knows customer_id, hub_id, address_id, state, delivery_fee, idempotency_token, placed_at, lines, id, archived_at, delivery_address_text, distance_km, voucher_id, voucher_discount, quiet_discount, reject_reason, confirmed_at, ready_at, closed_at. Does place, move_to, replace_line, line. Own the order lifecycle, snapshots and accepted replacement totals. | InvalidTransition, OrderConfirmation, OrderDAO, OrderDetail, OrderLine, OrderSummary, OrderTrackingController, PlaceOrderController, controllers.common |

##### PaymentGatewaySimulator

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentGatewaySimulator | Knows selected inputs. Does authorise, release. Read or write parameterized records. | Authorisation, PlaceOrderController |

##### OrderDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderDAO | Knows conn. Does _load, get_by_id, get_by_token, insert, list_for_customer, change_state. Read or write parameterized records. | Order, OrderLine, OrderState, OrderTrackingController, PlaceOrderController, controllers.common |

##### PaymentDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentDAO | Knows conn. Does get_by_order_id, insert, change_state, set_amounts†. Read or write parameterized records. | OnlineOption, OrderTrackingController, Payment, PaymentMethod, PaymentState, PlaceOrderController, controllers.common |

##### OrderTrackingController

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderTrackingController | Knows customers, orders, payments, hubs, deliveries, offers. Does get_order, list_my_orders, cancel_order†, _own_order, _require_customer. Coordinate authorization, domain decisions and data access. | AuthorizationError, CustomerDAO, HubDAO, NotFoundError, OrderDAO, OrderSummary, ReplacementOfferDAO, controllers.common, order |

##### DeliveryDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| DeliveryDAO | Knows conn. Does get_by_order_id. Read or write parameterized records. | OrderTrackingController |

##### ReplacementOfferDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| ReplacementOfferDAO | Knows conn. Does get_open, list_for_order, decide. Read or write parameterized records. | OrderTrackingController |

##### Payment

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Payment | Knows order_id, method, state, amount, created_at, updated_at, online_option, provider_ref, refund_amount, id. Does release_for_unfulfilled_order†. Hold captured amount C and refund obligations without claiming payout. | OrderConfirmation, OrderDetail, PaymentDAO, PlaceOrderController, controllers.common |

##### controllers.common

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| controllers.common | Knows selected inputs. Does move_order, release_payment†. Module functions with their original Python signatures. | ConflictError, Order, OrderDAO, OrderTrackingController, Payment, PaymentDAO |

##### ReplacementOffer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| ReplacementOffer | Knows order_id, order_line_id, original_item_name, original_unit_price, new_menu_item_id, new_item_name, new_unit_price, state, offered_at, decided_at, id. Does move_to. Hold one proposed whole-line replacement and its decision history. | OrderDetail, ReplacementOfferDAO |

##### OrderLine

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderLine | Knows menu_item_id, item_name, unit_price, quantity, id. Does typed value / enumeration initialization and attribute access. Retain item/name/price/quantity snapshots and derive the line total. | Order, OrderDAO, PlaceOrderController, Quote |

##### Customer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Customer | Knows id, user_id, full_name, phone, email, passport_no, nationality, customer_type. Does typed value / enumeration initialization and attribute access. Represent customer identity and permitted online payment choices. | CustomerDAO, OrderTrackingController, PlaceOrderController |

##### LocalCustomer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| LocalCustomer | Knows customer_type. Does typed value / enumeration initialization and attribute access. Specialize the Customer type and permitted payment options for a local customer. | No outward application call; supplied/read by its typed owner. |

##### TouristCustomer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| TouristCustomer | Knows customer_type. Does typed value / enumeration initialization and attribute access. Specialize Customer identity and permitted payment options for a tourist. | No outward application call; supplied/read by its typed owner. |

##### Address

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Address | Knows id, customer_id, label, full_address, district, latitude, longitude, archived_at. Does typed value / enumeration initialization and attribute access. Hold an owned delivery location and archive flag. | CustomerDAO, Hub, HubMenuView, PlaceOrderController, Quote |

##### MenuItem

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| MenuItem | Knows id, brand_id, brand_name, name, description, price, archived_at. Does typed value / enumeration initialization and attribute access. Hold current catalogue text, whole-VND price and archive flag. | HubDAO, HubMenuItem |

##### Brand

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Brand | Knows id, name, archived_at. Does typed value / enumeration initialization and attribute access. Group menu items and retain the archived brand identity. | No outward application call; supplied/read by its typed owner. |

##### HubMenuItem

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubMenuItem | Knows hub_id, item, is_available. Does typed value / enumeration initialization and attribute access. Represent one hub listing and its independent availability. | HubDAO, HubMenuView |

##### UserAccount

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| UserAccount | Knows id, username, password_hash, display_name, role, is_active, hub_id, created_at. Does typed value / enumeration initialization and attribute access. Hold account identity, role, active flag and optional kitchen-hub assignment. | UserDAO |

##### OrderState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderState | Knows PLACED, CONFIRMED, REJECTED, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, CANCELLED. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Order, OrderDAO, controllers.common |

##### PaymentState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentState | Knows PENDING, PAID, FAILED, VOIDED, REFUND_PENDING, REFUNDED. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Payment, PaymentDAO |

##### PaymentMethod

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentMethod | Knows COD, ONLINE. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Payment, PaymentChoice, PaymentDAO, Quote, order |

##### OnlineOption

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OnlineOption | Knows E_WALLET, BANK_QR, INTERNATIONAL_CARD. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Customer, Payment, PaymentChoice, PaymentDAO, PaymentGatewaySimulator, PlaceOrderController, Quote, order |

##### OfferState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OfferState | Knows OFFERED, ACCEPTED, DECLINED, WITHDRAWN. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | ReplacementOffer, ReplacementOfferDAO |

##### Role

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Role | Knows CUSTOMER, KITCHEN_STAFF, SHIPPER, ADMIN, MANAGER. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | UserAccount |

##### PaymentChoice

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentChoice | Knows method, option, outcome. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | PlaceOrderController, order |

##### OrderConfirmation

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderConfirmation | Knows order, payment, hub, created. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | PlaceOrderController |

##### HubMenuView

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubMenuView | Knows hub, status, menu, addresses. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | PlaceOrderController |

##### OrderDetail

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderDetail | Knows order, payment, hub, delivery, open_offer, offers. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | OrderTrackingController |

##### OrderSummary

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderSummary | Knows order, hub_name, awaiting_answer. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | OrderTrackingController |

##### Authorisation

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Authorisation | Knows approved, reference, message. Does typed value / enumeration initialization and attribute access. Carry the local simulator decision, reference and message; not persisted. | PaymentGatewaySimulator |

##### domain.rules

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| domain.rules | Knows selected inputs. Does delivery_fee, quiet_discount. Module functions with their original Python signatures. | PlaceOrderController, domain.rules |

##### DiscountType

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| DiscountType | Knows FIXED, PERCENT. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Voucher |

##### CustomerType

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| CustomerType | Knows LOCAL, TOURIST. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Customer, LocalCustomer, TouristCustomer |


### 3.1.4 OOD with Sequence Diagram

Each SSD occurrence has its own operation sequence. Actor → actual blueprint module → controller → domain / typed value; UC-01 also uses the local simulator. No DAO/SQL lifeline is present. Calls are synchronous, result arrows dashed, receivers activated, and the `alt` frame names the authorized/success versus main denial/rollback operands. Attribute/property reads are notes. Implicit dataclass «create» is not a business operation. Persistence is loaded/saved through data access — see 4.3.2.

| SSD operation and exact parameters | View → controller adapter; status | Guard / effects and failure guarantee |
|---|---|---|
| `browseHubs()`<br>`models/UC-01/ssd_uc01_PartA.drawio#01S-M01` | `order.choose_hub, GET /order/hubs` → `PlaceOrderController.list_hubs(self) -> list[HubStatus]`; MATCH | Read .busy / .quiet on HubStatus; these are properties, never busy() / quiet() calls. No persistent writes. Active Customer gate belongs to view; select_hub also checks active Customer and hub. |
| `selectHub(hubId)`<br>`models/UC-01/ssd_uc01_PartA.drawio#01S-M02` | `order.choose_items, GET /order/hubs/<int:hub_id>` → `PlaceOrderController.select_hub(self, user_id: int, hub_id: int) -> HubMenuView`; MATCH | Read .busy / .quiet on HubStatus; these are properties, never busy() / quiet() calls. No persistent writes. Active Customer gate belongs to view; select_hub also checks active Customer and hub. |
| `requestQuote(hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?)`<br>`models/UC-01/ssd_uc01_PartA.drawio#01S-M03` | `order.quote, POST /order/quote` → `PlaceOrderController.request_quote(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None) -> Quote`; P4-TARGET† F-04; F-07; P3-S01 | Target: active hub/menu/brand, own active address, integer quantities, load < capacity. Invalid input/refused voucher → no saved rows. Busy suggestions ≤3 ranked (load/capacity, raw distance, ID).<br>Read quote.item_subtotal / quote.total properties. Fingerprint binds hub/address, line IDs, quantities and prices, voucher + D, F, Q and payment choice; full accepted price T=S−D+F−Q. PaymentChoice is a typed adapter value. |
| `confirmCheckout(hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?, simulatorOutcome?, quoteFingerprint, quotedTotal, checkoutToken)`<br>`models/UC-01/ssd_uc01_PartB.drawio#01S-M04` | `order.confirm, POST /order/confirm` → `PlaceOrderController.confirm_order(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], idempotency_token: str, quoted_total: Optional[int] = None, voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None, quote_fingerprint: Optional[str] = None) -> OrderConfirmation`; P4-TARGET† F-04; F-07; P2-S05; P2-S13 | Simulator approve/decline choice precedes this request. Short atomic checkout begins before token lookup. Own existing token → existingOrder, no reprice, authorization or insertion (UC01-MG02). Foreign token → refusal. Unused token rechecks eligibility, raw radius, capacity, voucher and full consent.<br>Deterministic local simulator, no network/wait. COD skips authorise; ONLINE declined → zero Order/Line/Payment. Success atomically saves PLACED + snapshots + COD PENDING / ONLINE PAID, C=T (UC01-PC01–06). Any lock/write/commit failure rolls back all intended writes and releases authorization† (P2-S05/P2-S13). |
| `viewReceipt(orderId)`<br>`models/UC-01/ssd_uc01_PartC.drawio#01S-M05` | `order.detail, GET /order/<int:order_id>` → `OrderTrackingController.get_order(self, user_id: int, order_id: int) -> OrderDetail`; P4-TARGET† F-06 | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out† (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `viewMyOrders()`<br>`models/UC-01/ssd_uc01_PartC.drawio#01S-M06` | `order.my_orders, GET /order/mine` → `OrderTrackingController.list_my_orders(self, user_id: int) -> list[OrderSummary]`; MATCH | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `cancelOrder(orderId)`<br>`models/UC-01/ssd_uc01_PartC.drawio#01S-M07` | `order.cancel, POST /order/<int:order_id>/cancel` → `OrderTrackingController.cancel_order(self, user_id: int, order_id: int) -> OrderDetail`; P4-TARGET† F-02; P2-S13 | Guard: active own Customer; PLACED / CONFIRMED. Atomic CANCELLED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer WITHDRAWN; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback†. Root-adopted P4-TARGET: release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03). |

Operation guarantees are realized by these named controller methods and atomic/read boundaries. They remain Static / target obligations, not execution results.

| SSD operation | Responsible method / boundary | Guarantees | Status |
|---|---|---|---|
| OP-13 `browseHubs` | `PlaceOrderController.list_hubs(self) -> list[HubStatus]`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | MATCH |
| OP-14 `selectHub` | `PlaceOrderController.select_hub(self, user_id: int, hub_id: int) -> HubMenuView`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | MATCH |
| OP-15 `requestQuote` | `PlaceOrderController.request_quote(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None) -> Quote`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | P4-TARGET† F-04; F-07; P3-S01 |
| OP-01 `confirmCheckout` | `PlaceOrderController.confirm_order(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], idempotency_token: str, quoted_total: Optional[int] = None, voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None, quote_fingerprint: Optional[str] = None) -> OrderConfirmation`; BEGIN IMMEDIATE | UC01-PC01; UC01-PC02; UC01-PC03; UC01-PC04; UC01-PC05; UC01-PC06; UC01-MG01; UC01-MG02; UC01-MG03 | P4-TARGET† F-04; F-07; P2-S05; P2-S13 |
| OP-16 `viewReceipt` | `OrderTrackingController.get_order(self, user_id: int, order_id: int) -> OrderDetail`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | P4-TARGET† F-06 |
| OP-17 `viewMyOrders` | `OrderTrackingController.list_my_orders(self, user_id: int) -> list[OrderSummary]`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | MATCH |
| OP-07 `cancelOrder` | `OrderTrackingController.cancel_order(self, user_id: int, order_id: int) -> OrderDetail`; BEGIN IMMEDIATE | SUC04-PC01; SUC04-PC02 (atomic cancellation and full-C obligation); checkout PCs are not asserted by cancellation | P4-TARGET† F-02; P2-S13 |

##### OP-13 browseHubs

![UC-01 browseHubs](../../../models/UC-01/seq_uc01_browseHubs.png)

Figure 3.1.4.OP-13. UC-01 browseHubs design sequence — Author: 722I0004 · AI-assisted (Codex)

Read .busy / .quiet on HubStatus; these are properties, never busy() / quiet() calls. No persistent writes. Active Customer gate belongs to view; select_hub also checks active Customer and hub.


##### OP-14 selectHub

![UC-01 selectHub](../../../models/UC-01/seq_uc01_selectHub.png)

Figure 3.1.4.OP-14. UC-01 selectHub design sequence — Author: 722I0004 · AI-assisted (Codex)

Read .busy / .quiet on HubStatus; these are properties, never busy() / quiet() calls. No persistent writes. Active Customer gate belongs to view; select_hub also checks active Customer and hub.


##### OP-15 requestQuote

![UC-01 requestQuote — Part A](../../../models/UC-01/seq_uc01_requestQuote_PartA.png)

Figure 3.1.4.OP-15A. UC-01 requestQuote design sequence — Author: 722I0004 · AI-assisted (Codex)

Target: active hub/menu/brand, own active address, integer quantities, load < capacity. Invalid input/refused voucher → no saved rows. Busy suggestions ≤3 ranked (load/capacity, raw distance, ID).

![UC-01 requestQuote — Part B](../../../models/UC-01/seq_uc01_requestQuote_PartB.png)

Figure 3.1.4.OP-15B. UC-01 requestQuote design sequence — Author: 722I0004 · AI-assisted (Codex)

Read quote.item_subtotal / quote.total properties. Fingerprint binds hub/address, line IDs, quantities and prices, voucher + D, F, Q and payment choice; full accepted price T=S−D+F−Q. PaymentChoice is a typed adapter value.


##### OP-01 confirmCheckout

![UC-01 confirmCheckout — Part A](../../../models/UC-01/seq_uc01_confirmCheckout_PartA.png)

Figure 3.1.4.OP-01A. UC-01 confirmCheckout design sequence — Author: 722I0004 · AI-assisted (Codex)

Simulator approve/decline choice precedes this request. Short atomic checkout begins before token lookup. Own existing token → existingOrder, no reprice, authorization or insertion (UC01-MG02). Foreign token → refusal. Unused token rechecks eligibility, raw radius, capacity, voucher and full consent.

![UC-01 confirmCheckout — Part B](../../../models/UC-01/seq_uc01_confirmCheckout_PartB.png)

Figure 3.1.4.OP-01B. UC-01 confirmCheckout design sequence — Author: 722I0004 · AI-assisted (Codex)

Deterministic local simulator, no network/wait. COD skips authorise; ONLINE declined → zero Order/Line/Payment. Success atomically saves PLACED + snapshots + COD PENDING / ONLINE PAID, C=T (UC01-PC01–06). Any lock/write/commit failure rolls back all intended writes and releases authorization† (P2-S05/P2-S13).


##### OP-16 viewReceipt

![UC-01 viewReceipt](../../../models/UC-01/seq_uc01_viewReceipt.png)

Figure 3.1.4.OP-16. UC-01 viewReceipt design sequence — Author: 722I0004 · AI-assisted (Codex)

Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out† (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes.


##### OP-17 viewMyOrders

![UC-01 viewMyOrders](../../../models/UC-01/seq_uc01_viewMyOrders.png)

Figure 3.1.4.OP-17. UC-01 viewMyOrders design sequence — Author: 722I0004 · AI-assisted (Codex)

Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes.


##### OP-07 cancelOrder

![UC-01 cancelOrder](../../../models/UC-01/seq_uc01_cancelOrder.png)

Figure 3.1.4.OP-07. UC-01 cancelOrder design sequence — Author: 722I0004 · AI-assisted (Codex)

Guard: active own Customer; PLACED / CONFIRMED. Atomic CANCELLED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer WITHDRAWN; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback†. Root-adopted P4-TARGET: release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03).

### 3.1.5 Final Design Class Diagram

Changes from 3.1.2: **none in the selected member set**. Sequence reconciliation used the same selection from the outset: real route functions, controller methods, domain behavior, module helpers and implicit dataclass initializations are already present. Properties stay attribute reads. The final plates repeat the full selected exact signatures so every call receiver resolves; relation plates provide root-corrected navigation and layer dependencies. The pure-domain fingerprint inputs and full-refund helper target are synchronized with the reviewed shared model. Root-owned targets remain † until P4 and re-verification.

![UC-01 final — selected design members 1/9](../../../models/UC-01/dcd_uc01_final_PartA.png)

Figure 3.1.5A. UC-01 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — selected design members 2/9](../../../models/UC-01/dcd_uc01_final_PartB.png)

Figure 3.1.5B. UC-01 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — selected design members 3/9](../../../models/UC-01/dcd_uc01_final_PartC.png)

Figure 3.1.5C. UC-01 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — selected design members 4/9](../../../models/UC-01/dcd_uc01_final_PartD.png)

Figure 3.1.5D. UC-01 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — selected design members 5/9](../../../models/UC-01/dcd_uc01_final_PartE.png)

Figure 3.1.5E. UC-01 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — selected design members 6/9](../../../models/UC-01/dcd_uc01_final_PartF.png)

Figure 3.1.5F. UC-01 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — selected design members 7/9](../../../models/UC-01/dcd_uc01_final_PartG.png)

Figure 3.1.5G. UC-01 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — selected design members 8/9](../../../models/UC-01/dcd_uc01_final_PartH.png)

Figure 3.1.5H. UC-01 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — selected design members 9/9](../../../models/UC-01/dcd_uc01_final_PartI.png)

Figure 3.1.5I. UC-01 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 1](../../../models/UC-01/dcd_uc01_final_links_PartA.png)

Figure 3.1.5.R1. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 2](../../../models/UC-01/dcd_uc01_final_links_PartB.png)

Figure 3.1.5.R2. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 3](../../../models/UC-01/dcd_uc01_final_links_PartC.png)

Figure 3.1.5.R3. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 4](../../../models/UC-01/dcd_uc01_final_links_PartD.png)

Figure 3.1.5.R4. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 5](../../../models/UC-01/dcd_uc01_final_links_PartE.png)

Figure 3.1.5.R5. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 6](../../../models/UC-01/dcd_uc01_final_links_PartF.png)

Figure 3.1.5.R6. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 7](../../../models/UC-01/dcd_uc01_final_links_PartG.png)

Figure 3.1.5.R7. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 8](../../../models/UC-01/dcd_uc01_final_links_PartH.png)

Figure 3.1.5.R8. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 9](../../../models/UC-01/dcd_uc01_final_links_PartI.png)

Figure 3.1.5.R9. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 10](../../../models/UC-01/dcd_uc01_final_links_PartJ.png)

Figure 3.1.5.R10. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 11](../../../models/UC-01/dcd_uc01_final_links_PartK.png)

Figure 3.1.5.R11. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 12](../../../models/UC-01/dcd_uc01_final_links_PartL.png)

Figure 3.1.5.R12. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 13](../../../models/UC-01/dcd_uc01_final_links_PartM.png)

Figure 3.1.5.R13. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-01 final — relationships 14](../../../models/UC-01/dcd_uc01_final_links_PartN.png)

Figure 3.1.5.R14. UC-01 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

All figures require **230 mm landscape** placement: 24 px / 1600 px × 230 mm × 72 / 25.4 = **9.78 pt**. Split parts name their mutual continuation. Native draw.io editing and final DOCX/PDF placement remain **UNTESTED**.

† design target, not yet in code at C0 (see the method-specific P4 inputs in the class tables and operation table). MATCH means Static correspondence only. Sources: locked plan §§2–5/P3/P4/7.3/10–12; primary report template and marking extracts; Phase 2 descriptions, operation catalogue/membership/register and state/domain models; C0 AST inventory and shared design model.

## 3.2 Design for Use Case 2: Deliver an order: pick up, deliver with cash collection, or report failure (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

Baseline: 45ac76221b0a103174c7c01d17577e6e49cfd665. All application observations below are Static from the frozen AST inventory and shared model. Target behavior marked † is not a test or runtime result.

### 3.2.1 Design Classes in Detailed Design

One typed table per participating class/module follows.

##### UC-02 Design Classes

Author: 722I0004 · AI-assisted (Codex)

C0: 45ac76221b0a103174c7c01d17577e6e49cfd665 · Evidence: Static source correspondence only; this is not runtime or test evidence.

The tables use the sole shared DCD model at C0. Visibility follows the leading-underscore convention; signatures preserve the AST inventory. * marks an inferred/unannotated type or route signature. † marks a P4-TARGET/GAP and does not mean implemented at C0. Domain FK scalar attributes are retained here for mapping but omitted from DCDs in favour of associations.

##### Delivery

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Hold assignment, paired lifecycle times, cash and failure outcome.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute order_id | + | int | MATCH | FK scalar omitted from DCD; shown by association |
| Attribute state | + | DeliveryState | MATCH | — |
| Attribute ready_at | + | str | MATCH | — |
| Attribute shipper_id | + | Optional[int] | MATCH | FK scalar omitted from DCD; shown by association; default=None |
| Attribute picked_up_at | + | Optional[str] | MATCH | default=None |
| Attribute finished_at | + | Optional[str] | MATCH | default=None |
| Attribute failure_reason | + | Optional[str] | MATCH | default=None |
| Attribute cash_collected | + | Optional[int] | MATCH | default=None |
| Attribute id | + | Optional[int] | MATCH | default=None |
| Method move_to | + | move_to(self, new_state: DeliveryState) -> None | MATCH | — |


##### Order

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Own the order lifecycle, snapshots and accepted replacement totals.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute customer_id | + | int | MATCH | FK scalar omitted from DCD; shown by association |
| Attribute hub_id | + | int | MATCH | FK scalar omitted from DCD; shown by association |
| Attribute address_id | + | int | MATCH | FK scalar omitted from DCD; shown by association |
| Attribute state | + | OrderState | MATCH | — |
| Attribute delivery_fee | + | int | MATCH | — |
| Attribute idempotency_token | + | str | MATCH | — |
| Attribute placed_at | + | str | MATCH | — |
| Attribute lines | + | list[OrderLine] | MATCH | default=field(default_factory=list) |
| Attribute id | + | Optional[int] | MATCH | default=None |
| Attribute archived_at | + | Optional[str] | MATCH | default=None |
| Attribute delivery_address_text | + | str | MATCH | default='' |
| Attribute distance_km | + | float | MATCH | default=0.0 |
| Attribute voucher_id | + | Optional[int] | MATCH | FK scalar omitted from DCD; shown by association; default=None |
| Attribute voucher_discount | + | int | MATCH | default=0 |
| Attribute quiet_discount | + | int | MATCH | default=0 |
| Attribute reject_reason | + | Optional[str] | MATCH | default=None |
| Attribute confirmed_at | + | Optional[str] | MATCH | default=None |
| Attribute ready_at | + | Optional[str] | MATCH | default=None |
| Attribute closed_at | + | Optional[str] | MATCH | default=None |
| Method can_move_to | + | can_move_to(self, new_state: OrderState) -> bool | MATCH | — |
| Method move_to | + | move_to(self, new_state: OrderState) -> None | MATCH | — |


##### Payment

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Hold captured amount C and refund obligations without claiming payout.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute order_id | + | int | MATCH | FK scalar omitted from DCD; shown by association |
| Attribute method | + | PaymentMethod | MATCH | — |
| Attribute state | + | PaymentState | MATCH | — |
| Attribute amount | + | int | MATCH | — |
| Attribute created_at | + | str | MATCH | — |
| Attribute updated_at | + | Optional[str] | MATCH | default=None |
| Attribute online_option | + | Optional[OnlineOption] | MATCH | default=None |
| Attribute provider_ref | + | Optional[str] | MATCH | default=None |
| Attribute refund_amount | + | int | MATCH | default=0 |
| Attribute id | + | Optional[int] | MATCH | default=None |
| Method move_to | + | move_to(self, new_state: PaymentState) -> None | MATCH | — |
| Method release_for_unfulfilled_order | + | release_for_unfulfilled_order(self) -> None | P4-TARGET | P4 input: F-02; P2-S01; Set refund_amount=C with REFUND_PENDING; preserve COD VOIDED; no payout operation. |


##### UserAccount

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Hold account identity, role, active flag and optional kitchen-hub assignment.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute id | + | int | MATCH | — |
| Attribute username | + | str | MATCH | — |
| Attribute password_hash | + | str | MATCH | — |
| Attribute display_name | + | str | MATCH | — |
| Attribute role | + | Role | MATCH | — |
| Attribute is_active | + | bool | MATCH | default=True |
| Attribute hub_id | + | Optional[int] | MATCH | FK scalar omitted from DCD; shown by association; default=None |
| Attribute created_at | + | str | GAP | — |


##### Hub

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Represent a kitchen location, capacity and fee.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute id | + | int | MATCH | — |
| Attribute code | + | str | MATCH | — |
| Attribute name | + | str | MATCH | — |
| Attribute address_text | + | str | MATCH | — |
| Attribute latitude | + | float | MATCH | — |
| Attribute longitude | + | float | MATCH | — |
| Attribute max_active_orders | + | int | MATCH | — |
| Attribute base_delivery_fee | + | int | MATCH | — |
| Attribute archived_at | + | Optional[str] | MATCH | default=None |


##### Customer

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Represent customer identity and permitted online payment choices.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute id | + | int | MATCH | — |
| Attribute user_id | + | int | MATCH | FK scalar omitted from DCD; shown by association |
| Attribute full_name | + | str | MATCH | — |
| Attribute phone | + | Optional[str] | MATCH | default=None |
| Attribute email | + | Optional[str] | MATCH | default=None |
| Attribute passport_no | + | Optional[str] | MATCH | default=None |
| Attribute nationality | + | Optional[str] | MATCH | default=None |
| Attribute customer_type | + | CustomerType | MATCH | inferred; default=CustomerType.LOCAL |


##### DeliveryState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute AWAITING_PICKUP | + | str | MATCH | inferred; default='AWAITING_PICKUP' |
| Attribute PICKED_UP | + | str | MATCH | inferred; default='PICKED_UP' |
| Attribute DELIVERED | + | str | MATCH | inferred; default='DELIVERED' |
| Attribute FAILED | + | str | MATCH | inferred; default='FAILED' |


##### OrderState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute PLACED | + | str | MATCH | inferred; default='PLACED' |
| Attribute CONFIRMED | + | str | MATCH | inferred; default='CONFIRMED' |
| Attribute REJECTED | + | str | MATCH | inferred; default='REJECTED' |
| Attribute PREPARING | + | str | MATCH | inferred; default='PREPARING' |
| Attribute READY | + | str | MATCH | inferred; default='READY' |
| Attribute OUT_FOR_DELIVERY | + | str | MATCH | inferred; default='OUT_FOR_DELIVERY' |
| Attribute DELIVERED | + | str | MATCH | inferred; default='DELIVERED' |
| Attribute DELIVERY_FAILED | + | str | MATCH | inferred; default='DELIVERY_FAILED' |
| Attribute CANCELLED | + | str | MATCH | inferred; default='CANCELLED' |


##### PaymentState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute PENDING | + | str | MATCH | inferred; default='PENDING' |
| Attribute PAID | + | str | MATCH | inferred; default='PAID' |
| Attribute FAILED | + | str | MATCH | inferred; default='FAILED' |
| Attribute VOIDED | + | str | MATCH | inferred; default='VOIDED' |
| Attribute REFUND_PENDING | + | str | MATCH | inferred; default='REFUND_PENDING' |
| Attribute REFUNDED | + | str | MATCH | inferred; default='REFUNDED' |


##### Role

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute CUSTOMER | + | str | MATCH | inferred; default='CUSTOMER' |
| Attribute KITCHEN_STAFF | + | str | MATCH | inferred; default='KITCHEN_STAFF' |
| Attribute SHIPPER | + | str | MATCH | inferred; default='SHIPPER' |
| Attribute ADMIN | + | str | MATCH | inferred; default='ADMIN' |
| Attribute MANAGER | + | str | MATCH | inferred; default='MANAGER' |


##### DeliveryController

Layer: controller · Stereotype: «controller» · Module: saigonbite/business/controllers/delivery_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute deliveries | + | DeliveryDAO | MATCH | inferred |
| Attribute orders | + | OrderDAO | MATCH | inferred |
| Attribute payments | + | PaymentDAO | MATCH | inferred |
| Attribute hubs | + | HubDAO | MATCH | inferred |
| Attribute customers | + | CustomerDAO | MATCH | inferred |
| Method board | + | board(self, user_id: int) -> ShipperBoard | MATCH | — |
| Method get_delivery | + | get_delivery(self, user_id: int, order_id: int) -> DeliveryView | MATCH | — |
| Method pick_up | + | pick_up(self, user_id: int, order_id: int) -> DeliveryView | P4-TARGET | P4 input: P2-S13; P3-S03; Guarded writes must check rowcount and handle busy / commit failure without partial effects; shared helper is currently incomplete. |
| Method confirm_delivered | + | confirm_delivered(self, user_id: int, order_id: int, cash_collected: Optional[str]) -> DeliveryView | P4-TARGET | P4 input: P2-S13; P3-S03; Guarded writes must check rowcount and handle busy / commit failure without partial effects; shared helper is currently incomplete. |
| Method report_failure | + | report_failure(self, user_id: int, order_id: int, reason: str) -> DeliveryView | P4-TARGET | P4 input: F-02; P2-S13; BR-17 full C refund owed and atomic state/amount writes, including COMMIT rollback. |
| Method _require_shipper | - | _require_shipper(self, user_id: int) -> UserAccount | MATCH | — |
| Method _delivery | - | _delivery(self, order_id: int) -> Delivery | MATCH | — |
| Method _own_active_delivery | - | _own_active_delivery(self, shipper: UserAccount, order_id: int) -> Delivery | MATCH | — |
| Method _parse_cash | - | _parse_cash(raw: Optional[str]) -> Optional[int] | MATCH | — |
| Method _view | - | _view(self, delivery: Delivery) -> DeliveryView | MATCH | — |


##### BaseController

Layer: controller · Stereotype: «controller» · Module: saigonbite/business/controllers/common.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Attribute clock | + | Any | MATCH | inferred |
| Attribute users | + | UserDAO | MATCH | inferred |
| Method _now | - | _now(self) -> str | MATCH | — |
| Method _require_user | - | _require_user(self, user_id: int, *roles: Role, message: str='Your account cannot do this.') -> UserAccount | MATCH | — |


##### controllers.common

Layer: controller · Stereotype: «module» · Module: saigonbite/business/controllers/common.py

Responsibility: Module functions with their original Python signatures.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method move_order | + | move_order(orders: OrderDAO, order: Order, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> None | MATCH | — |
| Method release_payment | + | release_payment(payments: PaymentDAO, order_id: int, now: str) -> Payment | P4-TARGET | P4 input: F-02; P2-S01; P3-S03; Persist full captured C as refund_amount together with state; changing only the domain object does not save the amount. Check conditional save results in the same transaction. |


##### DeliveryView

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/delivery_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute delivery | + | Delivery | MATCH | — |
| Attribute order | + | Order | MATCH | — |
| Attribute payment | + | Payment | MATCH | — |
| Attribute hub | + | Hub | MATCH | — |
| Attribute customer | + | Customer | MATCH | — |
| Method cash_to_collect | + | cash_to_collect(self) -> int | MATCH | property |


##### ShipperBoard

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/delivery_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute waiting | + | list[DeliveryView] | MATCH | — |
| Attribute mine | + | list[DeliveryView] | MATCH | — |
| Attribute finished | + | list[DeliveryView] | MATCH | — |


##### delivery

Layer: view · Stereotype: «view» · Module: saigonbite/presentation/delivery.py

Responsibility: Translate shipper requests and render contact and cash information.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method board | + | board() | MATCH | inferred |
| Method detail | + | detail(order_id: int) | MATCH | inferred |
| Method pick_up | + | pick_up(order_id: int) | MATCH | inferred |
| Method delivered | + | delivered(order_id: int) | MATCH | inferred |
| Method failed | + | failed(order_id: int) | MATCH | inferred |


##### DeliveryDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/delivery_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_by_order_id | + | get_by_order_id(self, order_id: int) -> Optional[Delivery] | MATCH | — |
| Method list_awaiting_pickup | + | list_awaiting_pickup(self) -> list[Delivery] | MATCH | — |
| Method list_for_shipper | + | list_for_shipper(self, shipper_id: int, state: DeliveryState) -> list[Delivery] | MATCH | — |
| Method take | + | take(self, order_id: int, shipper_id: int, now: str) -> bool | MATCH | — |
| Method finish | + | finish(self, order_id: int, shipper_id: int, to_state: DeliveryState, now: str, failure_reason: Optional[str]=None, cash_collected: Optional[int]=None) -> bool | MATCH | — |


##### OrderDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/order_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_by_id | + | get_by_id(self, order_id: int) -> Optional[Order] | MATCH | — |
| Method change_state | + | change_state(self, order_id: int, from_state: OrderState, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> bool | MATCH | — |
| Method _load | - | _load(self, row: Optional[sqlite3.Row]) -> Optional[Order] | MATCH | — |


##### PaymentDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/payment_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_by_order_id | + | get_by_order_id(self, order_id: int) -> Optional[Payment] | MATCH | — |
| Method change_state | + | change_state(self, order_id: int, from_state: PaymentState, to_state: PaymentState, now: str) -> bool | MATCH | — |
| Method set_amounts | + | set_amounts(self, order_id: int, amount: int, refund_amount: int, now: str) -> bool | P4-TARGET | P4 input: F-02; P3-S03; Persist full/partial refund obligations atomically and expose the conditional save outcome. |


##### CustomerDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/customer_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get | + | get(self, customer_id: int) -> Optional[Customer] | MATCH | — |


##### HubDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/hub_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_including_archived | + | get_including_archived(self, hub_id: int) -> Optional[Hub] | MATCH | — |


##### UserDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/user_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_by_id | + | get_by_id(self, user_id: int) -> Optional[UserAccount] | MATCH | — |


### 3.2.2 Design Class Diagram

#### i. Domain design class

Order, Delivery and Payment retain their real lifecycle roles; their associations carry persisted relationships. Hub, Customer and UserAccount are read participants. Passport is excluded from the shipper projection.

![UC-02 domain design classes: Lifecycle classes continue in Part B for party/hub associations.](../../../models/UC-02/dcd_uc02_domain_PartA.png)

Figure 3.2.2.i-A. UC-02 domain design classes: Lifecycle classes continue in Part B for party/hub associations. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_domain_PartA.drawio) · [SVG](../../../models/UC-02/dcd_uc02_domain_PartA.svg) · [Generator](../../../models/UC-02/dcd_uc02_domain_PartA.py) · [Data](../../../models/UC-02/dcd_uc02_domain_PartA.json)

![UC-02 domain design classes: Part A continues here. Domain FK scalars are omitted in favour of these navigable associations.](../../../models/UC-02/dcd_uc02_domain_PartB.png)

Figure 3.2.2.i-B. UC-02 domain design classes: Part A continues here. Domain FK scalars are omitted in favour of these navigable associations. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_domain_PartB.drawio) · [SVG](../../../models/UC-02/dcd_uc02_domain_PartB.svg) · [Generator](../../../models/UC-02/dcd_uc02_domain_PartB.py) · [Data](../../../models/UC-02/dcd_uc02_domain_PartB.json)

#### ii. Controller

DeliveryController coordinates active-shipper checks, pickup/finish/failure work and the returned delivery view. The shared controllers.common module owns the real order/payment helper functions.

![UC-02 controller/value roles: Read and pickup operations continue in Part B.](../../../models/UC-02/dcd_uc02_controller_PartA.png)

Figure 3.2.2.ii-A. UC-02 controller/value roles: Read and pickup operations continue in Part B. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_controller_PartA.drawio) · [SVG](../../../models/UC-02/dcd_uc02_controller_PartA.svg) · [Generator](../../../models/UC-02/dcd_uc02_controller_PartA.py) · [Data](../../../models/UC-02/dcd_uc02_controller_PartA.json)

![UC-02 controller/value roles: Part A continues through the two mutually exclusive completion outcomes.](../../../models/UC-02/dcd_uc02_controller_PartB.png)

Figure 3.2.2.ii-B. UC-02 controller/value roles: Part A continues through the two mutually exclusive completion outcomes. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_controller_PartB.drawio) · [SVG](../../../models/UC-02/dcd_uc02_controller_PartB.svg) · [Generator](../../../models/UC-02/dcd_uc02_controller_PartB.py) · [Data](../../../models/UC-02/dcd_uc02_controller_PartB.json)

#### iii. UI (view)

saigonbite.presentation.delivery is the «view» blueprint module; its route functions are operations with METHOD/rule metadata, not an invented view class.

![UC-02 view module](../../../models/UC-02/dcd_uc02_view.png)

Figure 3.2.2.iii. UC-02 view module — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_view.drawio) · [SVG](../../../models/UC-02/dcd_uc02_view.svg) · [Generator](../../../models/UC-02/dcd_uc02_view.py) · [Data](../../../models/UC-02/dcd_uc02_view.json)

#### iv. Data access

The DAO projection includes only methods relevant to these five SSD occurrences. Section III shows persistence notes, not DAO or SQL messages; transaction detail is deferred to 4.3.2.

![UC-02 data-access classes](../../../models/UC-02/dcd_uc02_dao.png)

Figure 3.2.2.iv. UC-02 data-access classes — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_dao.drawio) · [SVG](../../../models/UC-02/dcd_uc02_dao.svg) · [Generator](../../../models/UC-02/dcd_uc02_dao.py) · [Data](../../../models/UC-02/dcd_uc02_dao.json)

#### v. Design class (all layers together)

Parts A-J are operation-aligned views across the same four layers, with mutual continuation notes. The integrated DCD keeps receiver names/return types compact; exact signatures remain in the class tables and filtered layer diagrams.

![UC-02 all layers: Ready board authorization and retrieval](../../../models/UC-02/dcd_uc02_all_PartA.png)

Figure 3.2.2.v-A. UC-02 all layers: Ready board authorization and retrieval — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartA.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartA.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartA.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartA.json)

![UC-02 all layers: Board row projection](../../../models/UC-02/dcd_uc02_all_PartB.png)

Figure 3.2.2.v-B. UC-02 all layers: Board row projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartB.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartB.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartB.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartB.json)

![UC-02 all layers: Inspect assignment and access](../../../models/UC-02/dcd_uc02_all_PartC.png)

Figure 3.2.2.v-C. UC-02 all layers: Inspect assignment and access — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartC.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartC.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartC.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartC.json)

![UC-02 all layers: Delivery contact projection](../../../models/UC-02/dcd_uc02_all_PartD.png)

Figure 3.2.2.v-D. UC-02 all layers: Delivery contact projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartD.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartD.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartD.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartD.json)

![UC-02 all layers: Atomic pickup and paired Order transition](../../../models/UC-02/dcd_uc02_all_PartE.png)

Figure 3.2.2.v-E. UC-02 all layers: Atomic pickup and paired Order transition — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartE.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartE.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartE.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartE.json)

![UC-02 all layers: Successful delivery and paired states](../../../models/UC-02/dcd_uc02_all_PartF.png)

Figure 3.2.2.v-F. UC-02 all layers: Successful delivery and paired states — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartF.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartF.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartF.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartF.json)

![UC-02 all layers: Failure state and full refund obligation](../../../models/UC-02/dcd_uc02_all_PartG.png)

Figure 3.2.2.v-G. UC-02 all layers: Failure state and full refund obligation — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartG.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartG.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartG.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartG.json)

![UC-02 all layers: Completion contact and cash projection](../../../models/UC-02/dcd_uc02_all_PartH.png)

Figure 3.2.2.v-H. UC-02 all layers: Completion contact and cash projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartH.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartH.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartH.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartH.json)

![UC-02 all layers: Contact and archived-hub projection](../../../models/UC-02/dcd_uc02_all_PartI.png)

Figure 3.2.2.v-I. UC-02 all layers: Contact and archived-hub projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartI.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartI.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartI.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartI.json)

![UC-02 all layers: Completion contact projection](../../../models/UC-02/dcd_uc02_all_PartJ.png)

Figure 3.2.2.v-J. UC-02 all layers: Completion contact projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_all_PartJ.drawio) · [SVG](../../../models/UC-02/dcd_uc02_all_PartJ.svg) · [Generator](../../../models/UC-02/dcd_uc02_all_PartJ.py) · [Data](../../../models/UC-02/dcd_uc02_all_PartJ.json)

### 3.2.3 OOD with CRC Cards or Communication Diagram

The CRC include lists actual collaborators from the AST-derived call/type model and distinguishes controller values from domain entities.

##### UC-02 CRC Cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators are real classes/modules linked by the AST-derived shared model (calls or typed attributes); target-only collaborators are identified as P4 targets. Blueprints and helpers remain real modules. No communication diagram is added.

##### Delivery — domain / «entity»

**Knows:** state: DeliveryState, ready_at: str, picked_up_at: Optional[str], finished_at: Optional[str], failure_reason: Optional[str], cash_collected: Optional[int], id: Optional[int]
**Does:** Hold assignment, paired lifecycle times, cash and failure outcome.; operations: move_to
**Collaborators:** DeliveryState

##### Order — domain / «entity»

**Knows:** state: OrderState, delivery_fee: int, idempotency_token: str, placed_at: str, lines: list[OrderLine], id: Optional[int], archived_at: Optional[str], delivery_address_text: str, distance_km: float, voucher_discount: int, quiet_discount: int, reject_reason: Optional[str], confirmed_at: Optional[str], ready_at: Optional[str], closed_at: Optional[str]
**Does:** Own the order lifecycle, snapshots and accepted replacement totals.; operations: can_move_to, move_to
**Collaborators:** OrderState

##### Payment — domain / «entity»

**Knows:** method: PaymentMethod, state: PaymentState, amount: int, created_at: str, updated_at: Optional[str], online_option: Optional[OnlineOption], provider_ref: Optional[str], refund_amount: int, id: Optional[int]
**Does:** Hold captured amount C and refund obligations without claiming payout.; operations: move_to, release_for_unfulfilled_order †
**Collaborators:** PaymentState

##### UserAccount — domain / «entity»

**Knows:** id: int, username: str, password_hash: str, display_name: str, role: Role, is_active: bool, created_at: str
**Does:** Hold account identity, role, active flag and optional kitchen-hub assignment.; operations: value/module role only.
**Collaborators:** Role

##### Hub — domain / «entity»

**Knows:** id: int, code: str, name: str, address_text: str, latitude: float, longitude: float, max_active_orders: int, base_delivery_fee: int, archived_at: Optional[str]
**Does:** Represent a kitchen location, capacity and fee.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

##### Customer — domain / «entity»

**Knows:** id: int, full_name: str, phone: Optional[str], email: Optional[str], passport_no: Optional[str], nationality: Optional[str], customer_type: CustomerType
**Does:** Represent customer identity and permitted online payment choices.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

##### DeliveryState — domain / «enumeration»

**Knows:** AWAITING_PICKUP: str, PICKED_UP: str, DELIVERED: str, FAILED: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

##### OrderState — domain / «enumeration»

**Knows:** PLACED: str, CONFIRMED: str, REJECTED: str, PREPARING: str, READY: str, OUT_FOR_DELIVERY: str, DELIVERED: str, DELIVERY_FAILED: str, CANCELLED: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

##### PaymentState — domain / «enumeration»

**Knows:** PENDING: str, PAID: str, FAILED: str, VOIDED: str, REFUND_PENDING: str, REFUNDED: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

##### Role — domain / «enumeration»

**Knows:** CUSTOMER: str, KITCHEN_STAFF: str, SHIPPER: str, ADMIN: str, MANAGER: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

##### DeliveryController — controller / «controller»

**Knows:** deliveries: DeliveryDAO, orders: OrderDAO, payments: PaymentDAO, hubs: HubDAO, customers: CustomerDAO
**Does:** Coordinate authorization, domain decisions and data access.; operations: board, get_delivery, pick_up †, confirm_delivered †, report_failure †, _require_shipper, _delivery, _own_active_delivery, _parse_cash, _view
**Collaborators:** CustomerDAO, Delivery, DeliveryDAO, DeliveryView, HubDAO, OrderDAO, Payment, PaymentDAO, ShipperBoard, UserAccount, controllers.common

##### BaseController — controller / «controller»

**Knows:** conn: sqlite3.Connection, clock: Any, users: UserDAO
**Does:** Coordinate authorization, domain decisions and data access.; operations: _now, _require_user
**Collaborators:** Role, UserAccount, UserDAO

##### controllers.common — controller / «module»

**Knows:** No instance attributes in the shared model.
**Does:** Module functions with their original Python signatures.; operations: move_order, release_payment †
**Collaborators:** Order, OrderDAO, OrderState, Payment, PaymentDAO

##### DeliveryView — controller / «value»

**Knows:** delivery: Delivery, order: Order, payment: Payment, hub: Hub, customer: Customer
**Does:** Coordinate authorization, domain decisions and data access.; operations: cash_to_collect
**Collaborators:** Customer, Delivery, Hub, Order, Payment

##### ShipperBoard — controller / «value»

**Knows:** waiting: list[DeliveryView], mine: list[DeliveryView], finished: list[DeliveryView]
**Does:** Coordinate authorization, domain decisions and data access.; operations: value/module role only.
**Collaborators:** DeliveryView

##### delivery — view / «view»

**Knows:** No instance attributes in the shared model.
**Does:** Translate shipper requests and render contact and cash information.; operations: board, detail, pick_up, delivered, failed
**Collaborators:** DeliveryController

##### DeliveryDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_by_order_id, list_awaiting_pickup, list_for_shipper, take, finish
**Collaborators:** Delivery, DeliveryState, delivery

##### OrderDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_by_id, change_state, _load
**Collaborators:** Order, OrderState

##### PaymentDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_by_order_id, change_state, set_amounts †
**Collaborators:** Payment, PaymentState

##### CustomerDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get
**Collaborators:** Customer

##### HubDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_including_archived
**Collaborators:** Hub

##### UserDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_by_id
**Collaborators:** UserAccount

##### Privacy and assignment boundary

Shipper-facing DeliveryView contains only the permitted contact and stored address snapshot. Customer.passport_no is not part of the shipper projection. The Delivery-to-UserAccount association carries the optional assigned-shipper role; no shipper class is fabricated.

##### Architecture correspondence

Actual DAO imports of domain values remain static couplings in these CRC collaborators; they are an upward-dependency P4.9 finding documented in section 4.2, and are not drawn as permitted dependencies in the layered DCD.


### 3.2.4 OOD with Sequence Diagram

Every sequence keeps the exact SSD operation/parameter string at the actor-to-view boundary, then maps it to real blueprint/controller/domain methods. Solid arrows are calls; dashed arrows are results. Dataclass creation and property reads are distinct from business methods. No DAO or SQL appears; persistence is noted for 4.3.2. † identifies target transaction/rowcount/commit/busy behavior, not C0 success.

##### viewReadyDeliveries — no parameters

OP-21 viewReadyDeliveries() — models/UC-02/ssd_uc02_PartA.drawio#M01

![UC-02 design sequence: viewReadyDeliveries](../../../models/UC-02/seq_uc02_viewReadyDeliveries.png)

Figure 3.2.4.1. UC-02 design sequence: viewReadyDeliveries — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/seq_uc02_viewReadyDeliveries.drawio) · [SVG](../../../models/UC-02/seq_uc02_viewReadyDeliveries.svg) · [Generator](../../../models/UC-02/seq_uc02_viewReadyDeliveries.py) · [Data](../../../models/UC-02/seq_uc02_viewReadyDeliveries.json)

##### viewDelivery — orderId

OP-22 viewDelivery(orderId) — models/UC-02/ssd_uc02_PartA.drawio#M02

![UC-02 design sequence: viewDelivery](../../../models/UC-02/seq_uc02_viewDelivery.png)

Figure 3.2.4.2. UC-02 design sequence: viewDelivery — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/seq_uc02_viewDelivery.drawio) · [SVG](../../../models/UC-02/seq_uc02_viewDelivery.svg) · [Generator](../../../models/UC-02/seq_uc02_viewDelivery.py) · [Data](../../../models/UC-02/seq_uc02_viewDelivery.json)

##### takeDelivery — orderId

OP-10 takeDelivery(orderId) — models/UC-02/ssd_uc02_PartA.drawio#M03

![UC-02 design sequence: takeDelivery](../../../models/UC-02/seq_uc02_takeDelivery.png)

Figure 3.2.4.3. UC-02 design sequence: takeDelivery — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/seq_uc02_takeDelivery.drawio) · [SVG](../../../models/UC-02/seq_uc02_takeDelivery.svg) · [Generator](../../../models/UC-02/seq_uc02_takeDelivery.py) · [Data](../../../models/UC-02/seq_uc02_takeDelivery.json)

##### confirmDelivered — orderId, cashCollected?

OP-11 confirmDelivered(orderId, cashCollected?) — models/UC-02/ssd_uc02_PartB.drawio#M04

![UC-02 design sequence: confirmDelivered](../../../models/UC-02/seq_uc02_confirmDelivered.png)

Figure 3.2.4.4. UC-02 design sequence: confirmDelivered — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/seq_uc02_confirmDelivered.drawio) · [SVG](../../../models/UC-02/seq_uc02_confirmDelivered.svg) · [Generator](../../../models/UC-02/seq_uc02_confirmDelivered.py) · [Data](../../../models/UC-02/seq_uc02_confirmDelivered.json)

##### reportFailure — orderId, reason

OP-12 reportFailure(orderId, reason) — models/UC-02/ssd_uc02_PartB.drawio#M05

![UC-02 design sequence: reportFailure](../../../models/UC-02/seq_uc02_reportFailure.png)

Figure 3.2.4.5. UC-02 design sequence: reportFailure — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/seq_uc02_reportFailure.drawio) · [SVG](../../../models/UC-02/seq_uc02_reportFailure.svg) · [Generator](../../../models/UC-02/seq_uc02_reportFailure.py) · [Data](../../../models/UC-02/seq_uc02_reportFailure.json)

### 3.2.5 Final Design Class Diagram

All message receivers in the five design sequences are present. Changes from 3.2.2: none in the class/method/association set; the final views repeat the operation-partitioned all-layer diagrams after sequence reconciliation.

![UC-02 final design classes: Ready board authorization and retrieval](../../../models/UC-02/dcd_uc02_final_PartA.png)

Figure 3.2.5-A. UC-02 final design classes: Ready board authorization and retrieval — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartA.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartA.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartA.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartA.json)

![UC-02 final design classes: Board row projection](../../../models/UC-02/dcd_uc02_final_PartB.png)

Figure 3.2.5-B. UC-02 final design classes: Board row projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartB.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartB.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartB.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartB.json)

![UC-02 final design classes: Inspect assignment and access](../../../models/UC-02/dcd_uc02_final_PartC.png)

Figure 3.2.5-C. UC-02 final design classes: Inspect assignment and access — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartC.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartC.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartC.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartC.json)

![UC-02 final design classes: Delivery contact projection](../../../models/UC-02/dcd_uc02_final_PartD.png)

Figure 3.2.5-D. UC-02 final design classes: Delivery contact projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartD.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartD.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartD.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartD.json)

![UC-02 final design classes: Atomic pickup and paired Order transition](../../../models/UC-02/dcd_uc02_final_PartE.png)

Figure 3.2.5-E. UC-02 final design classes: Atomic pickup and paired Order transition — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartE.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartE.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartE.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartE.json)

![UC-02 final design classes: Successful delivery and paired states](../../../models/UC-02/dcd_uc02_final_PartF.png)

Figure 3.2.5-F. UC-02 final design classes: Successful delivery and paired states — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartF.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartF.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartF.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartF.json)

![UC-02 final design classes: Failure state and full refund obligation](../../../models/UC-02/dcd_uc02_final_PartG.png)

Figure 3.2.5-G. UC-02 final design classes: Failure state and full refund obligation — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartG.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartG.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartG.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartG.json)

![UC-02 final design classes: Completion contact and cash projection](../../../models/UC-02/dcd_uc02_final_PartH.png)

Figure 3.2.5-H. UC-02 final design classes: Completion contact and cash projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartH.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartH.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartH.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartH.json)

![UC-02 final design classes: Contact and archived-hub projection](../../../models/UC-02/dcd_uc02_final_PartI.png)

Figure 3.2.5-I. UC-02 final design classes: Contact and archived-hub projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartI.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartI.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartI.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartI.json)

![UC-02 final design classes: Completion contact projection](../../../models/UC-02/dcd_uc02_final_PartJ.png)

Figure 3.2.5-J. UC-02 final design classes: Completion contact projection — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-02/dcd_uc02_final_PartJ.drawio) · [SVG](../../../models/UC-02/dcd_uc02_final_PartJ.svg) · [Generator](../../../models/UC-02/dcd_uc02_final_PartJ.py) · [Data](../../../models/UC-02/dcd_uc02_final_PartJ.json)

Every received sequence method appears on its actual receiver in the final DCD: blueprint routes, DeliveryController/BaseController helpers, controllers.common functions, domain move_to/refund behavior and controller value roles. The operation-specific P4 targets remain †; the final DCD does not imply those behaviors already pass at C0.

##### Integration repair evidence

Author: 722I0004 · AI-assisted (Codex)

The diagrams and typed metadata were refreshed against the corrected root-owned shared model. Allowed layered dependencies are drawn; actual upward DAO-to-domain imports are retained only as the static P4.9 architecture finding in report 4.2, not as permitted arrows. Shared transaction targets P2-S13/P3-S03 remain target behavior for guarded writes, commit failures and busy handling. Read paths remain read-only. Native draw.io XML and connected edge endpoints are structurally checked; native-app editing and final report placement remain UNTESTED.

DeliveryController calls the Delivery and Payment domain receivers. The local variable delivery is resolved to Delivery; it is not an upward call to the delivery blueprint.

## 3.3 Design for Use Case 3: Maintain hubs and kitchen capacity (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

### 3.3.1 Design Classes in Detailed Design

##### UC-03 design classes

Author: 722I0004 · AI-assisted (Codex)

Source: `models/shared/design_model.json`, C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`. Evidence label: Static / target design. This table is a filtered projection; no application module was imported. `Any` and absent annotations are explicitly inferred. Python visibility follows leading underscores; dataclass fields are public. Constructors are implicit dataclass construction, not invented methods.

† design target, not yet in code at C0 (see P4 inputs P2-S13/P2-S14/P2-S15/P3-S02/P3-S03). MATCH means static correspondence, not executed success.

Templates: `admin/hubs.html`, `admin/hub_form.html`, shared `error.html`. The `admin` role is the real Flask blueprint module, not a fictional view class.

Types retained as names from code include `Mapping`, `Optional`, `sqlite3.Connection` and business DTOs. A displayed attribute omitted from a narrow figure remains in this table. Association-backing foreign-key IDs remain below but are suppressed on domain DCDs.

##### admin

Layer: **view**; stereotype: **«view»**; responsibility: Translate administrator maintenance routes; never provide business decisions. Source: `saigonbite/presentation/admin.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Operation | `- _hubs() -> HubController` | MATCH |
| Operation | `+ hubs() -> Any [inferred] †` | P4-TARGET †; inferred annotation(s); P3-S02 |
| Operation | `+ new_hub() -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ edit_hub(hub_id: int) -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ archive_hub(hub_id: int) -> Any [inferred]` | MATCH; inferred annotation(s) |

Route adapters (AST):
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/', 'declared_rule': '/', 'methods': ['GET'], 'view_function': 'hubs', 'signature': 'hubs()', 'decorators': ["bp.get('/')", "bp.get('/hubs')", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/hubs', 'declared_rule': '/hubs', 'methods': ['GET'], 'view_function': 'hubs', 'signature': 'hubs()', 'decorators': ["bp.get('/')", "bp.get('/hubs')", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/hubs/new', 'declared_rule': '/hubs/new', 'methods': ['GET', 'POST'], 'view_function': 'new_hub', 'signature': 'new_hub()', 'decorators': ["bp.route('/hubs/new', methods=['GET', 'POST'])", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/hubs/<int:hub_id>', 'declared_rule': '/hubs/<int:hub_id>', 'methods': ['GET', 'POST'], 'view_function': 'edit_hub', 'signature': 'edit_hub(hub_id: int)', 'decorators': ["bp.route('/hubs/<int:hub_id>', methods=['GET', 'POST'])", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/hubs/<int:hub_id>/archive', 'declared_rule': '/hubs/<int:hub_id>/archive', 'methods': ['POST'], 'view_function': 'archive_hub', 'signature': 'archive_hub(hub_id: int)', 'decorators': ["bp.post('/hubs/<int:hub_id>/archive')", 'role_required(Role.ADMIN)']}`

##### HubController

Layer: **controller**; stereotype: **«controller»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/hub_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hubs: HubDAO` | MATCH; inferred |
| Operation | `+ list_hubs(user_id: int, include_archived: bool = True) -> list[HubAdminView] †` | P4-TARGET †; P3-S02 |
| Operation | `+ get_hub(user_id: int, hub_id: int) -> HubAdminView` | MATCH |
| Operation | `+ create_hub(user_id: int, form: Mapping[str, str]) -> Hub †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `+ update_hub(user_id: int, hub_id: int, form: Mapping[str, str]) -> Hub †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `+ archive_hub(user_id: int, hub_id: int) -> Hub †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `- _require_admin(user_id: int) -> None` | MATCH |
| Operation | `- _parse(form: Mapping[str, str], hub_id: Any) -> Hub [inferred]` | MATCH; inferred annotation(s) |

##### HubAdminView

Layer: **controller**; stereotype: **«value»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/hub_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ status: HubStatus` | MATCH |
| Attribute | `+ open_orders: int` | MATCH |
| Operation | `+ can_archive() -> bool` | MATCH; property accessor |

##### HubStatus

Layer: **domain**; stereotype: **«entity»**; responsibility: Derive busy, quiet and load percentage from current load and capacity. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hub: Hub` | MATCH |
| Attribute | `+ load: int` | MATCH |
| Operation | `+ busy() -> bool` | MATCH; property accessor |
| Operation | `+ quiet() -> bool` | MATCH; property accessor |
| Operation | `+ load_percent() -> int` | MATCH; property accessor |

##### Hub

Layer: **domain**; stereotype: **«entity»**; responsibility: Represent a kitchen location, capacity and fee. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
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

##### HubDAO

Layer: **data_access**; stereotype: **«DAO»**; responsibility: Read or write parameterized records. Source: `saigonbite/data_access/hub_dao.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ list_active() -> list[Hub]` | MATCH |
| Operation | `+ list_all() -> list[Hub]` | MATCH |
| Operation | `+ get_including_archived(hub_id: int) -> Optional[Hub]` | MATCH |
| Operation | `+ code_exists(code: str, except_id: Optional[int] = None) -> bool` | MATCH |
| Operation | `+ insert(hub: Hub) -> int` | MATCH |
| Operation | `+ update(hub: Hub) -> bool` | MATCH |
| Operation | `+ archive(hub_id: int, now: str) -> bool` | MATCH |
| Operation | `+ active_load(hub_id: int) -> int` | MATCH |
| Operation | `+ active_loads() -> dict[int, int]` | MATCH |
| Operation | `+ open_order_count(hub_id: int) -> int` | MATCH |

##### BaseController

Layer: **controller**; stereotype: **«controller»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/common.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Attribute | `+ clock: Any` | MATCH; inferred |
| Attribute | `+ users: UserDAO` | MATCH; inferred |
| Operation | `- _now() -> str` | MATCH |
| Operation | `- _require_user(user_id: int, *roles: Role, message: str = 'Your account cannot do this.') -> UserAccount` | MATCH |

##### UserAccount

Layer: **domain**; stereotype: **«entity»**; responsibility: Hold account identity, role, active flag and optional kitchen-hub assignment. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ username: str` | MATCH |
| Attribute | `+ password_hash: str` | MATCH |
| Attribute | `+ display_name: str` | MATCH |
| Attribute | `+ role: Role` | MATCH |
| Attribute | `+ is_active: bool` | MATCH |
| Attribute | `+ hub_id: Optional[int]` | MATCH; association backing ID, omitted on DCD |
| Attribute | `+ created_at: str` | GAP |

##### Role

Layer: **domain**; stereotype: **«enumeration»**; responsibility: Hold typed business state and its local rules. Source: `saigonbite/business/domain/enums.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ CUSTOMER: str` | MATCH; inferred |
| Attribute | `+ KITCHEN_STAFF: str` | MATCH; inferred |
| Attribute | `+ SHIPPER: str` | MATCH; inferred |
| Attribute | `+ ADMIN: str` | MATCH; inferred |
| Attribute | `+ MANAGER: str` | MATCH; inferred |

##### UserDAO

Layer: **data_access**; stereotype: **«DAO»**; responsibility: Read or write parameterized records. Source: `saigonbite/data_access/user_dao.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ get_by_id(user_id: int) -> Optional[UserAccount]` | MATCH |

##### Boundary adapters and guarantees

`uid()` always comes from the active server session; posted identity is never accepted. Form adapters retain SSD names while converting camelCase fields to Python keys: `address` → `address_text`, `baseDeliveryFee` → `base_delivery_fee`, `capacity` → `max_active_orders`; `brandId` → `brand_id`. Optional parameters map omitted values to the target defaults. Availability is validated as a boolean. Request.form values are strings; controllers parse and validate them.

OP-23 is a P3-S02 target with `include_archived: bool = True`; existing C0 route/controller omit that argument. Reads inspect archived hubs. `_parse` validates candidate attributes; `create_hub` / `update_hub` enforce uniqueness; `archive_hub` requires zero open orders. `HubStatus.busy/quiet` are properties derived from load/capacity. `HubAdminView.can_archive` derives from open_orders and archive flag, not a persistent state. Capacity below load is allowed. No restore is proposed.

Mutation success is acknowledged only after commit. The P2-S13/P3-S03 targets require rowcount/guard checks and controlled busy or commit-error rollback; the Section III figures intentionally hide DAO/SQL behind the persistence note and Section 4.3.2. Draft validation maxima/coordinate windows remain draft constraints (P2-S17), not newly locked BRs.

##### Guarantee responsibility and transaction boundary

`HubStatus` and `HubAdminView` are transient projections, not additional persistent entities.

| Anchor / request | Named responsibility | Boundary |
|---|---|---|
| UC03-PC01 | HubController._parse + create_hub / update_hub; HubDAO.code_exists and insert / update | BEGIN IMMEDIATE; success only after commit † |
| UC03-PC02 | HubController.archive_hub; HubDAO.open_order_count + archive; read consumers exclude archived hubs operationally but retain history | BEGIN IMMEDIATE; no open orders; conditional-save rowcount and commit-error handling † |
| UC03-MG01 | HubController._require_admin / _parse and mutation guard checks; failed write rolls back; BaseController._require_user rejects inactive or wrong-role identity | All create/update/archive changes are atomic †; list/get are read-only |
| listHubs / getHub | HubController.list_hubs / get_hub returns HubAdminView + derived HubStatus; authorized archived inspection is allowed | Read; zero persistent writes |

† These are design targets where P2-S13/P3-S03 or the operation-specific gap is recorded; no transaction success was executed in P3. The full DAO realization is in Section 4.3.2.

Reviewed adapter status: `admin.hubs` is P4-TARGET † (P3-S02). Existing route symbols alone do not qualify those target behaviors as MATCH.


### 3.3.2 Design Class Diagram

Each sheet is generated from the shared model. Method-rich layer views and operation projections are split at 230 mm landscape width; sequences use 170 mm portrait width; all parts must be retained. The full typed class table resolves members omitted in narrow operation projections. A downward dashed arrow is a dependency; a solid domain association has multiplicities and navigability. Domain classes own no application dependency.

#### i. Domain design class

![UC-03 domain 1](../../../models/UC-03/dcd_uc03_domain_PartA.png)

Figure 3.3.2iA. UC-03 domain projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 domain 2](../../../models/UC-03/dcd_uc03_domain_PartB.png)

Figure 3.3.2iB. UC-03 domain projection 2 — Author: 722I0004 · AI-assisted (Codex)

#### ii. Controller

![UC-03 controller 1](../../../models/UC-03/dcd_uc03_controller_PartA.png)

Figure 3.3.2iiA. UC-03 controller projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 controller 2](../../../models/UC-03/dcd_uc03_controller_PartB.png)

Figure 3.3.2iiB. UC-03 controller projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 controller 3](../../../models/UC-03/dcd_uc03_controller_PartC.png)

Figure 3.3.2iiC. UC-03 controller projection 3 — Author: 722I0004 · AI-assisted (Codex)

#### iii. UI (view)

![UC-03 view 1](../../../models/UC-03/dcd_uc03_view_PartA.png)

Figure 3.3.2iiiA. UC-03 view projection 1 — Author: 722I0004 · AI-assisted (Codex)

#### iv. Data access

![UC-03 dao 1](../../../models/UC-03/dcd_uc03_dao_PartA.png)

Figure 3.3.2ivA. UC-03 dao projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 dao 2](../../../models/UC-03/dcd_uc03_dao_PartB.png)

Figure 3.3.2ivB. UC-03 dao projection 2 — Author: 722I0004 · AI-assisted (Codex)

#### v. Design class (all layers together)

![UC-03 all 1](../../../models/UC-03/dcd_uc03_all_PartA.png)

Figure 3.3.2vA. UC-03 all projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 all 2](../../../models/UC-03/dcd_uc03_all_PartB.png)

Figure 3.3.2vB. UC-03 all projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 all 3](../../../models/UC-03/dcd_uc03_all_PartC.png)

Figure 3.3.2vC. UC-03 all projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 all 4](../../../models/UC-03/dcd_uc03_all_PartD.png)

Figure 3.3.2vD. UC-03 all projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 all 5](../../../models/UC-03/dcd_uc03_all_PartE.png)

Figure 3.3.2vE. UC-03 all projection 5 — Author: 722I0004 · AI-assisted (Codex)

### 3.3.3 OOD with CRC Cards or Communication Diagram

##### UC-03 CRC cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators are actual AST call/typed-field targets or the marked OP-25 / OP-43 targets. Inherited authorization collaborators are explicit. Self-calls remain the same class, not another fictional object.

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| `admin` | Knows: request context. Does: hubs, new_hub, edit_hub, archive_hub, _hubs. | HubController |
| `HubController` | Knows: hubs. Does: list_hubs, get_hub, create_hub, update_hub, archive_hub, _require_admin, _parse. | BaseController, ConflictError, Hub, HubAdminView, HubDAO, HubStatus, NotFoundError, ValidationError, admin |
| `HubAdminView` | Knows: status, open_orders. Does: can_archive. | HubController, HubStatus |
| `HubStatus` | Knows: hub, load. Does: busy, quiet, load_percent. | Hub, HubAdminView, HubController |
| `Hub` | Knows: id, code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee, archived_at. Does: holds typed state; no invented update/archive behavior. | HubController, HubDAO, HubStatus |
| `HubDAO` | Knows: conn. Does: list_all, list_active, get_including_archived, code_exists, insert, update, archive, active_load, active_loads, open_order_count. | Hub, HubController |
| `BaseController` | Knows: conn, clock, users. Does: _require_user, _now. | AuthorizationError, UserDAO |
| `UserAccount` | Knows: id, username, password_hash, display_name, role, is_active, hub_id, created_at. Does: holds typed state; no invented update/archive behavior. | Role |
| `Role` | Knows: CUSTOMER, KITCHEN_STAFF, SHIPPER, ADMIN, MANAGER. Does: holds typed state; no invented update/archive behavior. | UserAccount |
| `UserDAO` | Knows: conn. Does: get_by_id. | BaseController |

The existing admin.hubs route is a behavioral target † for forwarding includeArchived (P3-S02). Its current Python symbol is not evidence that the target filter behavior is already MATCH.


### 3.3.4 OOD with Sequence Diagram

Place the following sequence figures at **170 mm portrait width** (23 px minimum source text = 9.236 pt at placement). DCD sheets use **230 mm landscape width** (18 px = 9.780 pt).

Each exact SSD boundary request maps to a real blueprint route adapter and controller method. The active server session supplies uid(); camelCase names map to validated Python arguments/form keys in .1. The domain objects are dataclasses: a create arrow denotes implicit construction and a note denotes state inspection; no invented domain archive/update method is called. Return labels name outcomes, not callable methods. Persistence is a note referring to 4.3.2; Section III contains no DAO lifeline or SQL. Every guard is checked again at the mutation boundary. Technical-failure operands require rollback before acknowledging a no-change outcome.

![UC-03 sequence 1](../../../models/UC-03/seq_uc03_listHubs.png)

Figure 3.3.4A. UC-03 sequence projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 sequence 2](../../../models/UC-03/seq_uc03_getHub.png)

Figure 3.3.4B. UC-03 sequence projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 sequence 3](../../../models/UC-03/seq_uc03_createHub.png)

Figure 3.3.4C. UC-03 sequence projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 sequence 4](../../../models/UC-03/seq_uc03_updateHub.png)

Figure 3.3.4D. UC-03 sequence projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 sequence 5](../../../models/UC-03/seq_uc03_archiveHub.png)

Figure 3.3.4E. UC-03 sequence projection 5 — Author: 722I0004 · AI-assisted (Codex)

### 3.3.5 Final Design Class Diagram

Changes from 3.3.2: none in selected signatures. The final figures repeat the reconciled operation projections explicitly; the union includes every view/controller call shown in .4, including `_require_admin`. Domain create/note messages are construction/attribute facts, not additional callable operations. Full attributes and support authorization/DTO collaborators remain in the layer views and .1. Every final part continues the same UC projection set.

![UC-03 final 1](../../../models/UC-03/dcd_uc03_final_PartA.png)

Figure 3.3.5A. UC-03 final projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 final 2](../../../models/UC-03/dcd_uc03_final_PartB.png)

Figure 3.3.5B. UC-03 final projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 final 3](../../../models/UC-03/dcd_uc03_final_PartC.png)

Figure 3.3.5C. UC-03 final projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 final 4](../../../models/UC-03/dcd_uc03_final_PartD.png)

Figure 3.3.5D. UC-03 final projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-03 final 5](../../../models/UC-03/dcd_uc03_final_PartE.png)

Figure 3.3.5E. UC-03 final projection 5 — Author: 722I0004 · AI-assisted (Codex)

† design target, not yet in code at C0 (see the operation-specific P4 input in the figure and `operation_realisation.csv`). Shared busy/commit/rowcount requirements are P2-S13/P3-S03 targets; no runtime correctness is asserted. Native draw.io editing and final DOCX/PDF placement remain UNTESTED.

Integration maintenance (Author: 722I0004 · AI-assisted (Codex)): native draw.io text now has explicit actual font sizes and bold styles matching the SVG/PNG labels: 18 px minimum at 230 mm for DCDs and 23 px minimum at 170 mm for sequences. Native editing remains UNTESTED. Reviewed behavioral targets remain daggered; mere symbol/signature correspondence does not clear them.

## 3.4 Design for Use Case 4: Produce management reports: sales, workload, delivery performance (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

Baseline: 45ac76221b0a103174c7c01d17577e6e49cfd665. All application observations below are Static from the frozen AST inventory and shared model. Target behavior marked † is not a test or runtime result.

### 3.4.1 Design Classes in Detailed Design

One typed table per participating class/module follows.

##### UC-04 Design Classes

Author: 722I0004 · AI-assisted (Codex)

C0: 45ac76221b0a103174c7c01d17577e6e49cfd665 · Evidence: Static source correspondence only; this is not runtime or test evidence.

The tables use the sole shared DCD model at C0. Visibility follows the leading-underscore convention; signatures preserve the AST inventory. * marks an inferred/unannotated type or route signature. † marks a P4-TARGET/GAP and does not mean implemented at C0. Domain FK scalar attributes are retained here for mapping but omitted from DCDs in favour of associations.

##### Hub

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Represent a kitchen location, capacity and fee.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute id | + | int | MATCH | — |
| Attribute code | + | str | MATCH | — |
| Attribute name | + | str | MATCH | — |
| Attribute address_text | + | str | MATCH | — |
| Attribute latitude | + | float | MATCH | — |
| Attribute longitude | + | float | MATCH | — |
| Attribute max_active_orders | + | int | MATCH | — |
| Attribute base_delivery_fee | + | int | MATCH | — |
| Attribute archived_at | + | Optional[str] | MATCH | default=None |


##### HubStatus

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Derive busy, quiet and load percentage from current load and capacity.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute hub | + | Hub | MATCH | — |
| Attribute load | + | int | MATCH | — |
| Method busy | + | busy(self) -> bool | MATCH | property |
| Method quiet | + | quiet(self) -> bool | MATCH | property |
| Method load_percent | + | load_percent(self) -> int | MATCH | property |


##### OrderState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute PLACED | + | str | MATCH | inferred; default='PLACED' |
| Attribute CONFIRMED | + | str | MATCH | inferred; default='CONFIRMED' |
| Attribute REJECTED | + | str | MATCH | inferred; default='REJECTED' |
| Attribute PREPARING | + | str | MATCH | inferred; default='PREPARING' |
| Attribute READY | + | str | MATCH | inferred; default='READY' |
| Attribute OUT_FOR_DELIVERY | + | str | MATCH | inferred; default='OUT_FOR_DELIVERY' |
| Attribute DELIVERED | + | str | MATCH | inferred; default='DELIVERED' |
| Attribute DELIVERY_FAILED | + | str | MATCH | inferred; default='DELIVERY_FAILED' |
| Attribute CANCELLED | + | str | MATCH | inferred; default='CANCELLED' |


##### DeliveryState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute AWAITING_PICKUP | + | str | MATCH | inferred; default='AWAITING_PICKUP' |
| Attribute PICKED_UP | + | str | MATCH | inferred; default='PICKED_UP' |
| Attribute DELIVERED | + | str | MATCH | inferred; default='DELIVERED' |
| Attribute FAILED | + | str | MATCH | inferred; default='FAILED' |


##### ReportController

Layer: controller · Stereotype: «controller» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Authorize Manager requests and construct operational reports without writes.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute reports | + | ReportDAO | MATCH | inferred |
| Attribute hubs | + | HubDAO | MATCH | inferred |
| Method all_hubs | + | all_hubs(self) -> list[Hub] | MATCH | — |
| Method sales_report | + | sales_report(self, user_id: int, date_from: Optional[str]=None, date_to: Optional[str]=None, hub_id: Optional[int]=None) -> SalesReport | P4-TARGET | P4 input: F-03; F-09; Expose T without subtracting refund owed twice; top items retain menu_item_id identity. Carry menu_item_id into SalesReport.top_items and presentation. |
| Method workload_report | + | workload_report(self, user_id: int) -> WorkloadReport | P4-TARGET | P4 input: P2-S18; Use all retained hub identities, including archived hubs with zero open work. |
| Method delivery_report | + | delivery_report(self, user_id: int, date_from: Optional[str]=None, date_to: Optional[str]=None, hub_id: Optional[int]=None) -> DeliveryReport | MATCH | — |
| Method _require_manager | - | _require_manager(self, user_id: int) -> None | MATCH | — |
| Method _hub | - | _hub(self, hub_id: Optional[int]) -> Optional[Hub] | MATCH | — |
| Method _period | - | _period(self, date_from: Optional[str], date_to: Optional[str]) -> Period | MATCH | — |


##### BaseController

Layer: controller · Stereotype: «controller» · Module: saigonbite/business/controllers/common.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Attribute clock | + | Any | MATCH | inferred |
| Attribute users | + | UserDAO | MATCH | inferred |
| Method _today_vn | - | _today_vn(self) -> str | MATCH | — |
| Method _require_user | - | _require_user(self, user_id: int, *roles: Role, message: str='Your account cannot do this.') -> UserAccount | MATCH | — |


##### controllers.common

Layer: controller · Stereotype: «module» · Module: saigonbite/business/controllers/common.py

Responsibility: Module functions with their original Python signatures.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method vn_day_start_utc | + | vn_day_start_utc(day: date) -> str | MATCH | — |


##### controllers.report_controller

Layer: controller · Stereotype: «module» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Module functions with their original Python signatures.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method _minutes | - | _minutes(start: Optional[str], end: Optional[str]) -> Optional[float] | MATCH | — |


##### Period

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute date_from | + | str | MATCH | — |
| Attribute date_to | + | str | MATCH | — |
| Attribute start_utc | + | str | MATCH | — |
| Attribute end_utc | + | str | MATCH | — |


##### SalesRow

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute label | + | str | MATCH | — |
| Attribute orders | + | int | MATCH | default=0 |
| Attribute item_sales | + | int | MATCH | default=0 |
| Attribute voucher_discounts | + | int | MATCH | default=0 |
| Attribute delivery_fees | + | int | MATCH | default=0 |
| Attribute total | + | int | MATCH | default=0 |
| Attribute refunds_owed | + | int | MATCH | default=0 |
| Method net | + | net(self) -> int | P4-TARGET | property; P4 input: F-03; Return total T; refunds_owed is disclosed separately. |
| Method add | + | add(self, other: 'SalesRow') -> None | MATCH | — |


##### SalesReport

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute period | + | Period | MATCH | — |
| Attribute hub | + | Optional[Hub] | MATCH | — |
| Attribute rows | + | list[SalesRow] | MATCH | — |
| Attribute totals | + | SalesRow | MATCH | — |
| Attribute top_items | + | list[tuple[int, str, int, int]] | P4-TARGET | — |


##### WorkloadRow

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute status | + | HubStatus | MATCH | — |
| Attribute counts | + | dict[OrderState, int] | MATCH | — |
| Method label | + | label(self) -> str | MATCH | property |


##### WorkloadReport

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute as_of | + | str | MATCH | — |
| Attribute rows | + | list[WorkloadRow] | MATCH | — |


##### DeliveryRow

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute label | + | str | MATCH | — |
| Attribute delivered | + | int | MATCH | default=0 |
| Attribute failed | + | int | MATCH | default=0 |
| Attribute waits | + | list[float] | MATCH | default=field(default_factory=list) |
| Attribute rides | + | list[float] | MATCH | default=field(default_factory=list) |
| Method failure_rate | + | failure_rate(self) -> Optional[float] | MATCH | property |
| Method avg_wait | + | avg_wait(self) -> Optional[float] | MATCH | property |
| Method avg_ride | + | avg_ride(self) -> Optional[float] | MATCH | property |


##### DeliveryReport

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute period | + | Period | MATCH | — |
| Attribute hub | + | Optional[Hub] | MATCH | — |
| Attribute by_hub | + | list[DeliveryRow] | MATCH | — |
| Attribute by_shipper | + | list[DeliveryRow] | MATCH | — |
| Attribute overall | + | DeliveryRow | MATCH | — |


##### reports

Layer: view · Stereotype: «view» · Module: saigonbite/presentation/reports.py

Responsibility: Translate Manager filters and render read-only report results.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method _filtered | - | _filtered(template: str, run) | MATCH | inferred |
| Method sales | + | sales() | P4-TARGET | inferred; P4 input: F-09; Render the new identity-preserving top-items shape; template unpacking must retain the item identity. |
| Method workload | + | workload() | MATCH | inferred |
| Method delivery | + | delivery() | MATCH | inferred |


##### ReportDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/report_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method sales_by_hub | + | sales_by_hub(self, start_utc: str, end_utc: str, hub_id: Optional[int]) -> list[sqlite3.Row] | MATCH | — |
| Method top_items | + | top_items(self, start_utc: str, end_utc: str, hub_id: Optional[int], limit: int=10) -> list[sqlite3.Row] | P4-TARGET | P4 input: F-09; Select and group by menu_item_id; snapshot name is a label, never the grouping identity. |
| Method open_orders_by_hub_and_state | + | open_orders_by_hub_and_state(self) -> list[sqlite3.Row] | MATCH | — |
| Method finished_deliveries | + | finished_deliveries(self, start_utc: str, end_utc: str, hub_id: Optional[int]) -> list[sqlite3.Row] | MATCH | — |


##### HubDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/hub_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method list_active | + | list_active(self) -> list[Hub] | MATCH | — |
| Method list_all | + | list_all(self) -> list[Hub] | MATCH | — |
| Method get_including_archived | + | get_including_archived(self, hub_id: int) -> Optional[Hub] | MATCH | — |


##### UserDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/user_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_by_id | + | get_by_id(self, user_id: int) -> Optional[UserAccount] | MATCH | — |

##### F-09 identity and presentation target

ReportDAO.top_items retains menu_item_id in grouping and read rows. SalesReport.top_items carries list[tuple[int, str, int, int]] (item ID, snapshot name, quantity, revenue). reports.sales and its template preserve that identity when rendering; these three elements are P4-TARGET under F-09 / P4.8. No target behavior is claimed executed.


### 3.4.2 Design Class Diagram

#### i. Domain design class

HubStatus and Hub are the real domain participants. Period, report rows and report results belong to the actual controller module; no Report domain class or lifecycle is invented.

![UC-04 domain design classes: No Report domain class or lifecycle exists; report values stay in the controller module.](../../../models/UC-04/dcd_uc04_domain.png)

Figure 3.4.2.i-A. UC-04 domain design classes: No Report domain class or lifecycle exists; report values stay in the controller module. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_domain.drawio) · [SVG](../../../models/UC-04/dcd_uc04_domain.svg) · [Generator](../../../models/UC-04/dcd_uc04_domain.py) · [Data](../../../models/UC-04/dcd_uc04_domain.json)

#### ii. Controller

ReportController validates manager access and filters, then builds ephemeral report value objects. DeliveryRow exposes the real wait/ride/failure calculations; zero denominators display n/a.

![UC-04 controller/value roles: Sales value roles continue in Part B; other report operations continue in Parts C–F.](../../../models/UC-04/dcd_uc04_controller_PartA.png)

Figure 3.4.2.ii-A. UC-04 controller/value roles: Sales value roles continue in Part B; other report operations continue in Parts C–F. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartA.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartA.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartA.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartA.json)

![UC-04 controller/value roles: Part A contains authorization/filter helpers; F-03/F-09 remain † targets.](../../../models/UC-04/dcd_uc04_controller_PartB.png)

Figure 3.4.2.ii-B. UC-04 controller/value roles: Part A contains authorization/filter helpers; F-03/F-09 remain † targets. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartB.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartB.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartB.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartB.json)

![UC-04 controller/value roles: Workload value roles continue in Part D.](../../../models/UC-04/dcd_uc04_controller_PartC.png)

Figure 3.4.2.ii-C. UC-04 controller/value roles: Workload value roles continue in Part D. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartC.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartC.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartC.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartC.json)

![UC-04 controller/value roles: Part C contains authorization; workload targets retain archived hubs (P2-S18).](../../../models/UC-04/dcd_uc04_controller_PartD.png)

Figure 3.4.2.ii-D. UC-04 controller/value roles: Part C contains authorization; workload targets retain archived hubs (P2-S18). — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartD.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartD.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartD.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartD.json)

![UC-04 controller/value roles: Delivery metric value roles continue in Part F.](../../../models/UC-04/dcd_uc04_controller_PartE.png)

Figure 3.4.2.ii-E. UC-04 controller/value roles: Delivery metric value roles continue in Part F. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartE.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartE.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartE.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartE.json)

![UC-04 controller/value roles: Part E contains authorization and interval helpers; rows and sample counts are non-persisted.](../../../models/UC-04/dcd_uc04_controller_PartF.png)

Figure 3.4.2.ii-F. UC-04 controller/value roles: Part E contains authorization and interval helpers; rows and sample counts are non-persisted. — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_controller_PartF.drawio) · [SVG](../../../models/UC-04/dcd_uc04_controller_PartF.svg) · [Generator](../../../models/UC-04/dcd_uc04_controller_PartF.py) · [Data](../../../models/UC-04/dcd_uc04_controller_PartF.json)

#### iii. UI (view)

saigonbite.presentation.reports is the «view» blueprint module. It maps the SSD filters to actual route/controller arguments; it is not a fabricated view class.

![UC-04 view module](../../../models/UC-04/dcd_uc04_view.png)

Figure 3.4.2.iii. UC-04 view module — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_view.drawio) · [SVG](../../../models/UC-04/dcd_uc04_view.svg) · [Generator](../../../models/UC-04/dcd_uc04_view.py) · [Data](../../../models/UC-04/dcd_uc04_view.json)

#### iv. Data access

Reports issue read-only selections. Workload’s target retains archived hub identities with zero open work (P2-S18). The F-09/P4.8 target groups by menu_item_id and carries identity through ReportDAO.top_items, SalesReport.top_items and reports.sales. SalesReport.top_items is list[tuple[int, str, int, int]]: item ID, snapshot name, quantity and revenue; equal snapshot names do not merge distinct items.

![UC-04 data-access classes](../../../models/UC-04/dcd_uc04_dao.png)

Figure 3.4.2.iv. UC-04 data-access classes — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_dao.drawio) · [SVG](../../../models/UC-04/dcd_uc04_dao.svg) · [Generator](../../../models/UC-04/dcd_uc04_dao.py) · [Data](../../../models/UC-04/dcd_uc04_dao.json)

#### v. Design class (all layers together)

Parts A-I show operation paths and controller value roles across all four layers, with mutual continuation notes. The integrated DCD keeps receiver names/return types compact; exact signatures remain in the class tables and filtered layer diagrams.

![UC-04 all layers: Sales operation and data grain](../../../models/UC-04/dcd_uc04_all_PartA.png)

Figure 3.4.2.v-A. UC-04 all layers: Sales operation and data grain — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartA.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartA.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartA.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartA.json)

![UC-04 all layers: Manager guard and VN filter helpers](../../../models/UC-04/dcd_uc04_all_PartB.png)

Figure 3.4.2.v-B. UC-04 all layers: Manager guard and VN filter helpers — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartB.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartB.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartB.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartB.json)

![UC-04 all layers: Sales row and filter value objects](../../../models/UC-04/dcd_uc04_all_PartC.png)

Figure 3.4.2.v-C. UC-04 all layers: Sales row and filter value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartC.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartC.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartC.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartC.json)

![UC-04 all layers: Sales report result object](../../../models/UC-04/dcd_uc04_all_PartD.png)

Figure 3.4.2.v-D. UC-04 all layers: Sales report result object — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartD.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartD.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartD.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartD.json)

![UC-04 all layers: Current workload and archived hubs](../../../models/UC-04/dcd_uc04_all_PartE.png)

Figure 3.4.2.v-E. UC-04 all layers: Current workload and archived hubs — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartE.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartE.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartE.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartE.json)

![UC-04 all layers: Workload snapshot value objects](../../../models/UC-04/dcd_uc04_all_PartF.png)

Figure 3.4.2.v-F. UC-04 all layers: Workload snapshot value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartF.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartF.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartF.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartF.json)

![UC-04 all layers: Delivery interval and metric source](../../../models/UC-04/dcd_uc04_all_PartG.png)

Figure 3.4.2.v-G. UC-04 all layers: Delivery interval and metric source — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartG.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartG.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartG.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartG.json)

![UC-04 all layers: Delivery metric and report value objects](../../../models/UC-04/dcd_uc04_all_PartH.png)

Figure 3.4.2.v-H. UC-04 all layers: Delivery metric and report value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartH.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartH.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartH.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartH.json)

![UC-04 all layers: Delivery report result object](../../../models/UC-04/dcd_uc04_all_PartI.png)

Figure 3.4.2.v-I. UC-04 all layers: Delivery report result object — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_all_PartI.drawio) · [SVG](../../../models/UC-04/dcd_uc04_all_PartI.svg) · [Generator](../../../models/UC-04/dcd_uc04_all_PartI.py) · [Data](../../../models/UC-04/dcd_uc04_all_PartI.json)

### 3.4.3 OOD with CRC Cards or Communication Diagram

The CRC include lists actual collaborators from the AST-derived call/type model and distinguishes controller values from domain entities.

##### UC-04 CRC Cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators are real classes/modules linked by the AST-derived shared model (calls or typed attributes); target-only collaborators are identified as P4 targets. Blueprints and helpers remain real modules. No communication diagram is added.

##### Hub — domain / «entity»

**Knows:** id: int, code: str, name: str, address_text: str, latitude: float, longitude: float, max_active_orders: int, base_delivery_fee: int, archived_at: Optional[str]
**Does:** Represent a kitchen location, capacity and fee.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

##### HubStatus — domain / «entity»

**Knows:** hub: Hub, load: int
**Does:** Derive busy, quiet and load percentage from current load and capacity.; operations: busy, quiet, load_percent
**Collaborators:** Hub

##### OrderState — domain / «enumeration»

**Knows:** PLACED: str, CONFIRMED: str, REJECTED: str, PREPARING: str, READY: str, OUT_FOR_DELIVERY: str, DELIVERED: str, DELIVERY_FAILED: str, CANCELLED: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

##### DeliveryState — domain / «enumeration»

**Knows:** AWAITING_PICKUP: str, PICKED_UP: str, DELIVERED: str, FAILED: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

##### ReportController — controller / «controller»

**Knows:** reports: ReportDAO, hubs: HubDAO
**Does:** Authorize Manager requests and construct operational reports without writes.; operations: all_hubs, sales_report †, workload_report †, delivery_report, _require_manager, _hub, _period
**Collaborators:** DeliveryReport, DeliveryRow, Hub, HubDAO, HubStatus, OrderState, Period, ReportDAO, SalesReport, SalesRow, WorkloadReport, WorkloadRow, controllers.common, controllers.report_controller

##### BaseController — controller / «controller»

**Knows:** conn: sqlite3.Connection, clock: Any, users: UserDAO
**Does:** Coordinate authorization, domain decisions and data access.; operations: _today_vn, _require_user
**Collaborators:** UserDAO

##### controllers.common — controller / «module»

**Knows:** No instance attributes in the shared model.
**Does:** Module functions with their original Python signatures.; operations: vn_day_start_utc
**Collaborators:** OrderState

##### controllers.report_controller — controller / «module»

**Knows:** No instance attributes in the shared model.
**Does:** Module functions with their original Python signatures.; operations: _minutes
**Collaborators:** None recorded in this UC view.

##### Period — controller / «value»

**Knows:** date_from: str, date_to: str, start_utc: str, end_utc: str
**Does:** Coordinate authorization, domain decisions and data access.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

##### SalesRow — controller / «value»

**Knows:** label: str, orders: int, item_sales: int, voucher_discounts: int, delivery_fees: int, total: int, refunds_owed: int
**Does:** Coordinate authorization, domain decisions and data access.; operations: net †, add
**Collaborators:** None recorded in this UC view.

##### SalesReport — controller / «value»

**Knows:** period: Period, hub: Optional[Hub], rows: list[SalesRow], totals: SalesRow, top_items: list[tuple[int, str, int, int]]
**Does:** Coordinate authorization, domain decisions and data access.; operations: value/module role only.
**Collaborators:** Hub, Period, SalesRow

##### WorkloadRow — controller / «value»

**Knows:** status: HubStatus, counts: dict[OrderState, int]
**Does:** Coordinate authorization, domain decisions and data access.; operations: label
**Collaborators:** HubStatus, OrderState

##### WorkloadReport — controller / «value»

**Knows:** as_of: str, rows: list[WorkloadRow]
**Does:** Coordinate authorization, domain decisions and data access.; operations: value/module role only.
**Collaborators:** WorkloadRow

##### DeliveryRow — controller / «value»

**Knows:** label: str, delivered: int, failed: int, waits: list[float], rides: list[float]
**Does:** Coordinate authorization, domain decisions and data access.; operations: failure_rate, avg_wait, avg_ride
**Collaborators:** None recorded in this UC view.

##### DeliveryReport — controller / «value»

**Knows:** period: Period, hub: Optional[Hub], by_hub: list[DeliveryRow], by_shipper: list[DeliveryRow], overall: DeliveryRow
**Does:** Coordinate authorization, domain decisions and data access.; operations: value/module role only.
**Collaborators:** DeliveryRow, Hub, Period

##### reports — view / «view»

**Knows:** No instance attributes in the shared model.
**Does:** Translate Manager filters and render read-only report results.; operations: _filtered, sales †, workload, delivery
**Collaborators:** ReportController

##### ReportDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: sales_by_hub, top_items †, open_orders_by_hub_and_state, finished_deliveries
**Collaborators:** None recorded in this UC view.

##### HubDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: list_active, list_all, get_including_archived
**Collaborators:** Hub

##### UserDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_by_id
**Collaborators:** None recorded in this UC view.

##### Persistence boundary

Period, SalesRow, SalesReport, WorkloadRow, WorkloadReport, DeliveryRow and DeliveryReport are in-memory controller-module values. Filters, report rows, sample counts and returned reports are not persisted; UC-04 has no Report entity or lifecycle. HubStatus is the actual domain value role.

##### Architecture correspondence

Actual DAO imports of domain values remain static couplings in these CRC collaborators; they are an upward-dependency P4.9 finding documented in section 4.2, and are not drawn as permitted dependencies in the layered DCD.


### 3.4.4 OOD with Sequence Diagram

Each request independently rechecks active Manager access. Calls use the real view/controller/value roles; DAO/SQL is omitted and noted for 4.3.2. Sales keeps refunds owed separate from T and marks the F-09 item-identity target. Every outcome preserves UC04-MG01; the denial operand carries UC04-MG02.

##### salesReport — startDateVN, endDateVN, hubId?

OP-26 salesReport(startDateVN, endDateVN, hubId?) — models/UC-04/ssd_uc04.drawio#M01

![UC-04 design sequence: salesReport](../../../models/UC-04/seq_uc04_salesReport.png)

Figure 3.4.4.1. UC-04 design sequence: salesReport — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/seq_uc04_salesReport.drawio) · [SVG](../../../models/UC-04/seq_uc04_salesReport.svg) · [Generator](../../../models/UC-04/seq_uc04_salesReport.py) · [Data](../../../models/UC-04/seq_uc04_salesReport.json)

##### workloadReport — no parameters

OP-27 workloadReport() — models/UC-04/ssd_uc04.drawio#M02

![UC-04 design sequence: workloadReport](../../../models/UC-04/seq_uc04_workloadReport.png)

Figure 3.4.4.2. UC-04 design sequence: workloadReport — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/seq_uc04_workloadReport.drawio) · [SVG](../../../models/UC-04/seq_uc04_workloadReport.svg) · [Generator](../../../models/UC-04/seq_uc04_workloadReport.py) · [Data](../../../models/UC-04/seq_uc04_workloadReport.json)

##### deliveryReport — startDateVN, endDateVN, hubId?

OP-28 deliveryReport(startDateVN, endDateVN, hubId?) — models/UC-04/ssd_uc04.drawio#M03

![UC-04 design sequence: deliveryReport](../../../models/UC-04/seq_uc04_deliveryReport.png)

Figure 3.4.4.3. UC-04 design sequence: deliveryReport — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/seq_uc04_deliveryReport.drawio) · [SVG](../../../models/UC-04/seq_uc04_deliveryReport.svg) · [Generator](../../../models/UC-04/seq_uc04_deliveryReport.py) · [Data](../../../models/UC-04/seq_uc04_deliveryReport.json)

### 3.4.5 Final Design Class Diagram

All sequence receiver methods are present. Changes from 3.4.2: no local class/method/association change; final all-layer views repeat the sequence-reconciled design. The accepted shared F-09 annotation marks the DAO grouping, identity-bearing result and reports.sales presentation as P4-TARGET.

![UC-04 final design classes: Sales operation and data grain](../../../models/UC-04/dcd_uc04_final_PartA.png)

Figure 3.4.5-A. UC-04 final design classes: Sales operation and data grain — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartA.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartA.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartA.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartA.json)

![UC-04 final design classes: Manager guard and VN filter helpers](../../../models/UC-04/dcd_uc04_final_PartB.png)

Figure 3.4.5-B. UC-04 final design classes: Manager guard and VN filter helpers — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartB.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartB.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartB.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartB.json)

![UC-04 final design classes: Sales row and filter value objects](../../../models/UC-04/dcd_uc04_final_PartC.png)

Figure 3.4.5-C. UC-04 final design classes: Sales row and filter value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartC.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartC.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartC.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartC.json)

![UC-04 final design classes: Sales report result object](../../../models/UC-04/dcd_uc04_final_PartD.png)

Figure 3.4.5-D. UC-04 final design classes: Sales report result object — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartD.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartD.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartD.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartD.json)

![UC-04 final design classes: Current workload and archived hubs](../../../models/UC-04/dcd_uc04_final_PartE.png)

Figure 3.4.5-E. UC-04 final design classes: Current workload and archived hubs — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartE.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartE.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartE.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartE.json)

![UC-04 final design classes: Workload snapshot value objects](../../../models/UC-04/dcd_uc04_final_PartF.png)

Figure 3.4.5-F. UC-04 final design classes: Workload snapshot value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartF.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartF.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartF.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartF.json)

![UC-04 final design classes: Delivery interval and metric source](../../../models/UC-04/dcd_uc04_final_PartG.png)

Figure 3.4.5-G. UC-04 final design classes: Delivery interval and metric source — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartG.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartG.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartG.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartG.json)

![UC-04 final design classes: Delivery metric and report value objects](../../../models/UC-04/dcd_uc04_final_PartH.png)

Figure 3.4.5-H. UC-04 final design classes: Delivery metric and report value objects — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartH.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartH.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartH.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartH.json)

![UC-04 final design classes: Delivery report result object](../../../models/UC-04/dcd_uc04_final_PartI.png)

Figure 3.4.5-I. UC-04 final design classes: Delivery report result object — Author: 722I0004 · AI-assisted (Codex)

[Editable draw.io](../../../models/UC-04/dcd_uc04_final_PartI.drawio) · [SVG](../../../models/UC-04/dcd_uc04_final_PartI.svg) · [Generator](../../../models/UC-04/dcd_uc04_final_PartI.py) · [Data](../../../models/UC-04/dcd_uc04_final_PartI.json)

No Report state is drawn. Filters, report rows and returned reports are non-persisted controller values. The final DCD keeps † on F-03/F-09/P2-S18 targets; UC04-PC01 remains a required oracle correspondence, not a measured result.

##### Integration repair evidence

Author: 722I0004 · AI-assisted (Codex)

The diagrams and typed metadata were refreshed against the corrected root-owned shared model. Allowed layered dependencies are drawn; actual upward DAO-to-domain imports are retained only as the static P4.9 architecture finding in report 4.2, not as permitted arrows. Shared transaction targets P2-S13/P3-S03 remain target behavior for guarded writes, commit failures and busy handling. Read paths remain read-only. Native draw.io XML and connected edge endpoints are structurally checked; native-app editing and final report placement remain UNTESTED.

## 3.5 Design for Use Case 5: Decide an incoming order: confirm, reject, or offer a replacement the customer agrees to (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

This package is a target design at committed C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`. Read it with the frozen UC description/SSD/state views. It makes no runtime or implementation claim for † behavior.

### 3.5.1 Design Classes in Detailed Design

##### UC-05 design classes

Author: 722I0004 · AI-assisted (Codex)

Static source: C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`; shared source `models/shared/design_model.json`. MATCH records static correspondence. † P4-TARGET/GAP records a required design change, never implementation. Tables retain relation identifiers for exact static mapping; DCDs replace domain FK scalars with associations. Fields are public unless leading underscore; Python dataclasses are not assigned invented private visibility.

Properties have signatures for traceability but are read as attributes; dataclass «create» means implicit initialization, not an invented business method. Unannotated types are marked inferred. Templates are presentation resources, not design classes.

##### KitchenController

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

##### kitchen

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

##### HubDAO

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

##### OrderDAO

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

##### ReplacementOfferDAO

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

##### UserDAO

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

##### PaymentDAO

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

##### Order

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

##### Payment

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

##### OrderTrackingController

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

##### order

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

##### CustomerDAO

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

##### OrderDetail

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

##### DeliveryDAO

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

##### controllers.common

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

##### ReplacementOffer

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

##### OrderLine

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

##### Customer

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

##### LocalCustomer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Specialize the Customer type and permitted payment options for a local customer. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customer_type: CustomerType` **inferred** | MATCH |

##### TouristCustomer

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Specialize Customer identity and permitted payment options for a tourist. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customer_type: CustomerType` **inferred** | MATCH |

##### Address

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

##### MenuItem

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

##### Brand

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

##### HubMenuItem

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

##### UserAccount

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

##### OrderState

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

##### PaymentState

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

##### PaymentMethod

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

##### OnlineOption

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

##### OfferState

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

##### Role

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

##### KitchenBoard

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

##### BoardEntry

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

##### KitchenOrderView

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

##### OrderSummary

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

##### Hub

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

##### CustomerType

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

##### Presentation adapter and resources

The `order` / `kitchen` identifiers are actual Flask blueprint modules (`saigonbite/presentation/blueprints/*.py`); each route remains its actual Python function and HTTP rule. The SSD operation is translated at this boundary; session identity and route/form fields supply the controller arguments.

Templates used by the selected blueprint module(s): `kitchen/availability.html`, `kitchen/board.html`, `kitchen/order.html`, `order/confirmation.html`, `order/detail.html`, `order/hubs.html`, `order/menu.html`, `order/my_orders.html`, `order/payment_simulator.html`, `order/quote.html`.

Non-persisted values include Quote, PaymentChoice, HubStatus, response dataclasses and Authorisation. Busy/quiet are derived properties; no Busy/Quiet enum is introduced. No refund payout is designed.


### 3.5.2 Design Class Diagram

#### i. Domain design class

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-05 domain — selected design members 1/3](../../../models/UC-05/dcd_uc05_domain_PartA.png)

Figure 3.5.2.iA. UC-05 domain detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 domain — selected design members 2/3](../../../models/UC-05/dcd_uc05_domain_PartB.png)

Figure 3.5.2.iB. UC-05 domain detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 domain — selected design members 3/3](../../../models/UC-05/dcd_uc05_domain_PartC.png)

Figure 3.5.2.iC. UC-05 domain detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 domain — relationships 1](../../../models/UC-05/dcd_uc05_domain_links_PartA.png)

Figure 3.5.2.i.R1. UC-05 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 domain — relationships 2](../../../models/UC-05/dcd_uc05_domain_links_PartB.png)

Figure 3.5.2.i.R2. UC-05 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 domain — relationships 3](../../../models/UC-05/dcd_uc05_domain_links_PartC.png)

Figure 3.5.2.i.R3. UC-05 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 domain — relationships 4](../../../models/UC-05/dcd_uc05_domain_links_PartD.png)

Figure 3.5.2.i.R4. UC-05 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 domain — relationships 5](../../../models/UC-05/dcd_uc05_domain_links_PartE.png)

Figure 3.5.2.i.R5. UC-05 domain navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

#### ii. Controller

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-05 controller — selected design members 1/2](../../../models/UC-05/dcd_uc05_controller_PartA.png)

Figure 3.5.2.iiA. UC-05 controller detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 controller — selected design members 2/2](../../../models/UC-05/dcd_uc05_controller_PartB.png)

Figure 3.5.2.iiB. UC-05 controller detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 controller — relationships 1](../../../models/UC-05/dcd_uc05_controller_links_PartA.png)

Figure 3.5.2.ii.R1. UC-05 controller navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

#### iii. UI (view)

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-05 view — selected design members 1/1](../../../models/UC-05/dcd_uc05_view.png)

Figure 3.5.2.iii. UC-05 view detailed design members — Author: 722I0004 · AI-assisted (Codex)

#### iv. Data access

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-05 dao — selected design members 1/1](../../../models/UC-05/dcd_uc05_dao.png)

Figure 3.5.2.iv. UC-05 dao detailed design members — Author: 722I0004 · AI-assisted (Codex)

#### v. Design class (all layers together)

Filtered from the single shared design model. Member projection and relationship plates form one logical DCD; repeated class names identify the same class. Retained relation identifiers are omitted from domain figures; the table above and 4.3.1 retain them.

![UC-05 all — selected design members 1/7](../../../models/UC-05/dcd_uc05_all_PartA.png)

Figure 3.5.2.vA. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — selected design members 2/7](../../../models/UC-05/dcd_uc05_all_PartB.png)

Figure 3.5.2.vB. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — selected design members 3/7](../../../models/UC-05/dcd_uc05_all_PartC.png)

Figure 3.5.2.vC. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — selected design members 4/7](../../../models/UC-05/dcd_uc05_all_PartD.png)

Figure 3.5.2.vD. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — selected design members 5/7](../../../models/UC-05/dcd_uc05_all_PartE.png)

Figure 3.5.2.vE. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — selected design members 6/7](../../../models/UC-05/dcd_uc05_all_PartF.png)

Figure 3.5.2.vF. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — selected design members 7/7](../../../models/UC-05/dcd_uc05_all_PartG.png)

Figure 3.5.2.vG. UC-05 all detailed design members — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 1](../../../models/UC-05/dcd_uc05_all_links_PartA.png)

Figure 3.5.2.v.R1. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 2](../../../models/UC-05/dcd_uc05_all_links_PartB.png)

Figure 3.5.2.v.R2. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 3](../../../models/UC-05/dcd_uc05_all_links_PartC.png)

Figure 3.5.2.v.R3. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 4](../../../models/UC-05/dcd_uc05_all_links_PartD.png)

Figure 3.5.2.v.R4. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 5](../../../models/UC-05/dcd_uc05_all_links_PartE.png)

Figure 3.5.2.v.R5. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 6](../../../models/UC-05/dcd_uc05_all_links_PartF.png)

Figure 3.5.2.v.R6. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 7](../../../models/UC-05/dcd_uc05_all_links_PartG.png)

Figure 3.5.2.v.R7. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 8](../../../models/UC-05/dcd_uc05_all_links_PartH.png)

Figure 3.5.2.v.R8. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 9](../../../models/UC-05/dcd_uc05_all_links_PartI.png)

Figure 3.5.2.v.R9. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 10](../../../models/UC-05/dcd_uc05_all_links_PartJ.png)

Figure 3.5.2.v.R10. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 11](../../../models/UC-05/dcd_uc05_all_links_PartK.png)

Figure 3.5.2.v.R11. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)


![UC-05 all — relationships 12](../../../models/UC-05/dcd_uc05_all_links_PartL.png)

Figure 3.5.2.v.R12. UC-05 all navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

### 3.5.3 OOD with CRC Cards or Communication Diagram

##### UC-05 CRC cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators below resolve real AST constructor/function calls or typed collaborators from the shared model. A † operation is a root-annotated target; it is not a claim of code behavior. DAO collaborators appear here and in the DCD; Section III sequences intentionally defer persistence to 4.3.2.

##### KitchenController

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| KitchenController | Knows hubs, menu, orders, payments, deliveries, offers. Does board, get_order, confirm_order†, reject_order†, offer_replacement†. Coordinate authorization, domain decisions and data access. | BoardEntry, ConflictError, HubDAO, KitchenBoard, KitchenOrderView, Order, OrderDAO, PaymentDAO, ReplacementOffer, ReplacementOfferDAO, ValidationError, controllers.common, kitchen |

##### kitchen

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| kitchen | Knows selected inputs. Does board, order, confirm, reject, offer. Translate own-hub kitchen actions and render their results. | No outward application call; supplied/read by its typed owner. |

##### HubDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubDAO | Knows conn. Does get_including_archived, list_menu, get_available_item. Read or write parameterized records. | Hub, HubMenuItem, KitchenController, MenuItem, OrderTrackingController |

##### OrderDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderDAO | Knows conn. Does _load, list_for_hub, get_by_id, change_state, list_for_customer, save_lines_and_totals†. Read or write parameterized records. | KitchenController, Order, OrderLine, OrderState, OrderTrackingController, controllers.common |

##### ReplacementOfferDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| ReplacementOfferDAO | Knows conn. Does get_open, list_for_order, decide, insert. Read or write parameterized records. | KitchenController, OrderTrackingController |

##### UserDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| UserDAO | Knows conn. Does get_by_id. Read or write parameterized records. | No outward application call; supplied/read by its typed owner. |

##### PaymentDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentDAO | Knows conn. Does get_by_order_id, change_state, set_amounts†. Read or write parameterized records. | KitchenController, OnlineOption, OrderTrackingController, Payment, PaymentMethod, PaymentState, controllers.common |

##### Order

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Order | Knows customer_id, hub_id, address_id, state, delivery_fee, idempotency_token, placed_at, lines, id, archived_at, delivery_address_text, distance_km, voucher_id, voucher_discount, quiet_discount, reject_reason, confirmed_at, ready_at, closed_at. Does move_to, line, replace_line, total. Own the order lifecycle, snapshots and accepted replacement totals. | BoardEntry, InvalidTransition, KitchenController, KitchenOrderView, OrderDAO, OrderDetail, OrderSummary, OrderTrackingController, controllers.common |

##### Payment

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Payment | Knows order_id, method, state, amount, created_at, updated_at, online_option, provider_ref, refund_amount, id. Does release_for_unfulfilled_order†. Hold captured amount C and refund obligations without claiming payout. | KitchenOrderView, OrderDetail, PaymentDAO, controllers.common |

##### OrderTrackingController

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderTrackingController | Knows customers, orders, payments, hubs, deliveries, offers. Does list_my_orders, get_order, answer_replacement†, _own_order, _require_customer. Coordinate authorization, domain decisions and data access. | AuthorizationError, ConflictError, CustomerDAO, HubDAO, NotFoundError, Order, OrderDAO, OrderSummary, PaymentDAO, ReplacementOfferDAO, controllers.common, order |

##### order

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| order | Knows selected inputs. Does my_orders, detail, answer_replacement. Translate authenticated customer routes and render quote, receipt and order results. | kitchen |

##### CustomerDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| CustomerDAO | Knows conn. Does get_by_user_id. Read or write parameterized records. | OrderTrackingController |

##### OrderDetail

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderDetail | Knows order, payment, hub, delivery, open_offer, offers. Does total_if_accepted. Coordinate authorization, domain decisions and data access. | Order, OrderTrackingController |

##### DeliveryDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| DeliveryDAO | Knows conn. Does get_by_order_id. Read or write parameterized records. | KitchenController, OrderTrackingController |

##### controllers.common

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| controllers.common | Knows selected inputs. Does move_order, release_payment†. Module functions with their original Python signatures. | ConflictError, KitchenController, Order, OrderDAO, OrderTrackingController, Payment, PaymentDAO |

##### ReplacementOffer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| ReplacementOffer | Knows order_id, order_line_id, original_item_name, original_unit_price, new_menu_item_id, new_item_name, new_unit_price, state, offered_at, decided_at, id. Does move_to. Hold one proposed whole-line replacement and its decision history. | KitchenController, KitchenOrderView, OrderDetail, ReplacementOfferDAO |

##### OrderLine

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderLine | Knows menu_item_id, item_name, unit_price, quantity, id. Does typed value / enumeration initialization and attribute access. Retain item/name/price/quantity snapshots and derive the line total. | Order, OrderDAO |

##### Customer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Customer | Knows id, user_id, full_name, phone, email, passport_no, nationality, customer_type. Does typed value / enumeration initialization and attribute access. Represent customer identity and permitted online payment choices. | CustomerDAO, OrderTrackingController |

##### LocalCustomer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| LocalCustomer | Knows customer_type. Does typed value / enumeration initialization and attribute access. Specialize the Customer type and permitted payment options for a local customer. | No outward application call; supplied/read by its typed owner. |

##### TouristCustomer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| TouristCustomer | Knows customer_type. Does typed value / enumeration initialization and attribute access. Specialize Customer identity and permitted payment options for a tourist. | No outward application call; supplied/read by its typed owner. |

##### Address

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Address | Knows id, customer_id, label, full_address, district, latitude, longitude, archived_at. Does typed value / enumeration initialization and attribute access. Hold an owned delivery location and archive flag. | CustomerDAO, Hub |

##### MenuItem

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| MenuItem | Knows id, brand_id, brand_name, name, description, price, archived_at. Does typed value / enumeration initialization and attribute access. Hold current catalogue text, whole-VND price and archive flag. | HubDAO, HubMenuItem, KitchenOrderView |

##### Brand

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Brand | Knows id, name, archived_at. Does typed value / enumeration initialization and attribute access. Group menu items and retain the archived brand identity. | No outward application call; supplied/read by its typed owner. |

##### HubMenuItem

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubMenuItem | Knows hub_id, item, is_available. Does typed value / enumeration initialization and attribute access. Represent one hub listing and its independent availability. | HubDAO, KitchenController |

##### UserAccount

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| UserAccount | Knows id, username, password_hash, display_name, role, is_active, hub_id, created_at. Does typed value / enumeration initialization and attribute access. Hold account identity, role, active flag and optional kitchen-hub assignment. | KitchenController, UserDAO |

##### OrderState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderState | Knows PLACED, CONFIRMED, REJECTED, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, CANCELLED. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | KitchenBoard, Order, OrderDAO, controllers.common |

##### PaymentState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentState | Knows PENDING, PAID, FAILED, VOIDED, REFUND_PENDING, REFUNDED. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Payment, PaymentDAO |

##### PaymentMethod

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentMethod | Knows COD, ONLINE. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Payment, PaymentDAO, order |

##### OnlineOption

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OnlineOption | Knows E_WALLET, BANK_QR, INTERNATIONAL_CARD. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Customer, Payment, PaymentDAO, order |

##### OfferState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OfferState | Knows OFFERED, ACCEPTED, DECLINED, WITHDRAWN. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | ReplacementOffer, ReplacementOfferDAO |

##### Role

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Role | Knows CUSTOMER, KITCHEN_STAFF, SHIPPER, ADMIN, MANAGER. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | UserAccount |

##### KitchenBoard

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| KitchenBoard | Knows hub, columns. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | KitchenController |

##### BoardEntry

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| BoardEntry | Knows order, awaiting_customer. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | KitchenBoard, KitchenController |

##### KitchenOrderView

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| KitchenOrderView | Knows order, payment, open_offer, offers, candidates. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | KitchenController |

##### OrderSummary

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderSummary | Knows order, hub_name, awaiting_answer. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | OrderTrackingController |

##### Hub

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Hub | Knows id, code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee, archived_at. Does typed value / enumeration initialization and attribute access. Represent a kitchen location, capacity and fee. | HubDAO, KitchenBoard, KitchenController, OrderDetail |

##### CustomerType

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| CustomerType | Knows LOCAL, TOURIST. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Customer, LocalCustomer, TouristCustomer |


### 3.5.4 OOD with Sequence Diagram

Each SSD occurrence has its own operation sequence. Actor → actual blueprint module → controller → domain / typed value; UC-01 also uses the local simulator. No DAO/SQL lifeline is present. Calls are synchronous, result arrows dashed, receivers activated, and the `alt` frame names the authorized/success versus main denial/rollback operands. Attribute/property reads are notes. Implicit dataclass «create» is not a business operation. Persistence is loaded/saved through data access — see 4.3.2.

| SSD operation and exact parameters | View → controller adapter; status | Guard / effects and failure guarantee |
|---|---|---|
| `viewKitchenOrders()`<br>`models/UC-05/ssd_uc05_PartA.drawio#05S-M01` | `kitchen.board, GET /kitchen/` → `KitchenController.board(self, user_id: int) -> KitchenBoard`; MATCH | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `viewKitchenOrder(orderId)`<br>`models/UC-05/ssd_uc05_PartA.drawio#05S-M02` | `kitchen.order, GET /kitchen/orders/<int:order_id>` → `KitchenController.get_order(self, user_id: int, order_id: int) -> KitchenOrderView`; MATCH | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `confirmOrder(orderId)`<br>`models/UC-05/ssd_uc05_PartA.drawio#05S-M03` | `kitchen.confirm, POST /kitchen/orders/<int:order_id>/confirm` → `KitchenController.confirm_order(self, user_id: int, order_id: int) -> Order`; P4-TARGET† P2-S13; P3-S03 | Active own-hub staff; own PLACED; no open OFFERED. Atomic guarded state change + confirmed_at. No repricing/payment change. Conditional rowcount and busy/write/commit rollback† (P2-S13, P3-S03). |
| `rejectOrder(orderId, reason)`<br>`models/UC-05/ssd_uc05_PartA.drawio#05S-M04` | `kitchen.reject, POST /kitchen/orders/<int:order_id>/reject` → `KitchenController.reject_order(self, user_id: int, order_id: int, reason: str) -> Order`; P4-TARGET† F-02; P2-S13 | Guard: active own-hub Kitchen staff; PLACED; nonempty reason. Atomic REJECTED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer WITHDRAWN; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback†. Root-adopted P4-TARGET: release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03). |
| `offerReplacement(orderId, orderLineId, targetItemId)`<br>`models/UC-05/ssd_uc05_PartA.drawio#05S-M05` | `kitchen.offer, POST /kitchen/orders/<int:order_id>/offer` → `KitchenController.offer_replacement(self, user_id: int, order_id: int, order_line_id: int, new_menu_item_id: int) -> ReplacementOffer`; P4-TARGET† F-05; P2-S09; P2-S13 | Active own-hub PLACED; no open offer. Source currently sold out/unlisted/archived. Target active + active Brand, same-hub listed/available, different and absent from other lines; offered unit price ≤ source snapshot. Atomic OFFERED with unchanged quantity/Order PLACED (PC03). Fail/lock/commit rollback†; no request waits for Customer. |
| `viewMyOrders()`<br>`models/UC-05/ssd_uc05_PartB.drawio#05S-M06` | `order.my_orders, GET /order/mine` → `OrderTrackingController.list_my_orders(self, user_id: int) -> list[OrderSummary]`; MATCH | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `viewReplacement(orderId)`<br>`models/UC-05/ssd_uc05_PartB.drawio#05S-M07` | `order.detail, GET /order/<int:order_id>` → `OrderTrackingController.get_order(self, user_id: int, order_id: int) -> OrderDetail`; P4-TARGET† F-06 | Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out† (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes. |
| `acceptReplacement(orderId, offerId)`<br>`models/UC-05/ssd_uc05_PartB.drawio#05S-M08` | `order.answer_replacement, POST /order/<int:order_id>/replacement` → `OrderTrackingController.answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail`; P4-TARGET† F-05; F-02; P2-S09; P2-S11; P2-S13 | Before mutation†: active owner + own PLACED + exact open OFFERED belongs to order. Recheck target active, active Brand, listed + AVAILABLE at same hub. Ineligible owner/state/offer → staleRefusal, 0 changed rows. Invalid target → only exact offer WITHDRAWN† with returned reason; Order/lines/payment unchanged (MG01).<br>Valid acceptance continues atomically: use offered price, whole line, same quantity; Snew; Dnew=min(Dold,Snew), F/Q unchanged; Tnew=Snew−Dnew+F−Q. Read Order.total property, set offer ACCEPTED through data access. COD amount=Tnew; ONLINE state PAID, C unchanged, refund_amount=C−Tnew. Order stays PLACED (PC04), never auto-confirms. Any conditional 0-row/lock/write/commit failure → complete rollback†, MG01. |
| `declineReplacement(orderId, offerId)`<br>`models/UC-05/ssd_uc05_PartC.drawio#05S-M09` | `order.answer_replacement, POST /order/<int:order_id>/replacement` → `OrderTrackingController.answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail`; P4-TARGET† F-02; P2-S13 | Guard: active own Customer; PLACED; exact open OFFERED with matching order/offer IDs. SUC03-PC04: atomic REJECTED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer DECLINED; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback†. Root-adopted P4-TARGET: release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03). |

Operation guarantees are realized by these named controller methods and atomic/read boundaries. They remain Static / target obligations, not execution results.

| SSD operation | Responsible method / boundary | Guarantees | Status |
|---|---|---|---|
| OP-19 `viewKitchenOrders` | `KitchenController.board(self, user_id: int) -> KitchenBoard`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | MATCH |
| OP-20 `viewKitchenOrder` | `KitchenController.get_order(self, user_id: int, order_id: int) -> KitchenOrderView`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | MATCH |
| OP-02 `confirmOrder` | `KitchenController.confirm_order(self, user_id: int, order_id: int) -> Order`; BEGIN IMMEDIATE | UC05-PC01; UC05-MG01 | P4-TARGET† P2-S13; P3-S03 |
| OP-03 `rejectOrder` | `KitchenController.reject_order(self, user_id: int, order_id: int, reason: str) -> Order`; BEGIN IMMEDIATE | UC05-PC02 | P4-TARGET† F-02; P2-S13 |
| OP-04 `offerReplacement` | `KitchenController.offer_replacement(self, user_id: int, order_id: int, order_line_id: int, new_menu_item_id: int) -> ReplacementOffer`; BEGIN IMMEDIATE | UC05-PC03; UC05-MG01 | P4-TARGET† F-05; P2-S09; P2-S13 |
| OP-17 `viewMyOrders` | `OrderTrackingController.list_my_orders(self, user_id: int) -> list[OrderSummary]`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | MATCH |
| OP-18 `viewReplacement` | `OrderTrackingController.get_order(self, user_id: int, order_id: int) -> OrderDetail`; read | Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation | P4-TARGET† F-06 |
| OP-05 `acceptReplacement` | `OrderTrackingController.answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail`; BEGIN IMMEDIATE | UC05-PC04; UC05-MG01 | P4-TARGET† F-05; F-02; P2-S09; P2-S11; P2-S13 |
| OP-06 `declineReplacement` | `OrderTrackingController.answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail`; BEGIN IMMEDIATE | SUC03-PC04; UC05-MG01 (decline/reject and BR-17; stale or failed save leaves Order unchanged) | P4-TARGET† F-02; P2-S13 |

##### OP-19 viewKitchenOrders

![UC-05 viewKitchenOrders](../../../models/UC-05/seq_uc05_viewKitchenOrders.png)

Figure 3.5.4.OP-19. UC-05 viewKitchenOrders design sequence — Author: 722I0004 · AI-assisted (Codex)

Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes.


##### OP-20 viewKitchenOrder

![UC-05 viewKitchenOrder](../../../models/UC-05/seq_uc05_viewKitchenOrder.png)

Figure 3.5.4.OP-20. UC-05 viewKitchenOrder design sequence — Author: 722I0004 · AI-assisted (Codex)

Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes.


##### OP-02 confirmOrder

![UC-05 confirmOrder](../../../models/UC-05/seq_uc05_confirmOrder.png)

Figure 3.5.4.OP-02. UC-05 confirmOrder design sequence — Author: 722I0004 · AI-assisted (Codex)

Active own-hub staff; own PLACED; no open OFFERED. Atomic guarded state change + confirmed_at. No repricing/payment change. Conditional rowcount and busy/write/commit rollback† (P2-S13, P3-S03).


##### OP-03 rejectOrder

![UC-05 rejectOrder](../../../models/UC-05/seq_uc05_rejectOrder.png)

Figure 3.5.4.OP-03. UC-05 rejectOrder design sequence — Author: 722I0004 · AI-assisted (Codex)

Guard: active own-hub Kitchen staff; PLACED; nonempty reason. Atomic REJECTED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer WITHDRAWN; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback†. Root-adopted P4-TARGET: release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03).


##### OP-04 offerReplacement

![UC-05 offerReplacement](../../../models/UC-05/seq_uc05_offerReplacement.png)

Figure 3.5.4.OP-04. UC-05 offerReplacement design sequence — Author: 722I0004 · AI-assisted (Codex)

Active own-hub PLACED; no open offer. Source currently sold out/unlisted/archived. Target active + active Brand, same-hub listed/available, different and absent from other lines; offered unit price ≤ source snapshot. Atomic OFFERED with unchanged quantity/Order PLACED (PC03). Fail/lock/commit rollback†; no request waits for Customer.


##### OP-17 viewMyOrders

![UC-05 viewMyOrders](../../../models/UC-05/seq_uc05_viewMyOrders.png)

Figure 3.5.4.OP-17. UC-05 viewMyOrders design sequence — Author: 722I0004 · AI-assisted (Codex)

Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes.


##### OP-18 viewReplacement

![UC-05 viewReplacement](../../../models/UC-05/seq_uc05_viewReplacement.png)

Figure 3.5.4.OP-18. UC-05 viewReplacement design sequence — Author: 722I0004 · AI-assisted (Codex)

Read-only active role + own Customer / own kitchen hub checks; denied context discloses no foreign details. Receipt/offer amounts say refund owed, never paid out† (F-06 where applicable). Read snapshots, .total and offer attributes; no fabricated business getters. No persistent writes.


##### OP-05 acceptReplacement

![UC-05 acceptReplacement — Part A](../../../models/UC-05/seq_uc05_acceptReplacement_PartA.png)

Figure 3.5.4.OP-05A. UC-05 acceptReplacement design sequence — Author: 722I0004 · AI-assisted (Codex)

Before mutation†: active owner + own PLACED + exact open OFFERED belongs to order. Recheck target active, active Brand, listed + AVAILABLE at same hub. Ineligible owner/state/offer → staleRefusal, 0 changed rows. Invalid target → only exact offer WITHDRAWN† with returned reason; Order/lines/payment unchanged (MG01).

![UC-05 acceptReplacement — Part B](../../../models/UC-05/seq_uc05_acceptReplacement_PartB.png)

Figure 3.5.4.OP-05B. UC-05 acceptReplacement design sequence — Author: 722I0004 · AI-assisted (Codex)

Valid acceptance continues atomically: use offered price, whole line, same quantity; Snew; Dnew=min(Dold,Snew), F/Q unchanged; Tnew=Snew−Dnew+F−Q. Read Order.total property, set offer ACCEPTED through data access. COD amount=Tnew; ONLINE state PAID, C unchanged, refund_amount=C−Tnew. Order stays PLACED (PC04), never auto-confirms. Any conditional 0-row/lock/write/commit failure → complete rollback†, MG01.


##### OP-06 declineReplacement

![UC-05 declineReplacement](../../../models/UC-05/seq_uc05_declineReplacement.png)

Figure 3.5.4.OP-06. UC-05 declineReplacement design sequence — Author: 722I0004 · AI-assisted (Codex)

Guard: active own Customer; PLACED; exact open OFFERED with matching order/offer IDs. SUC03-PC04: atomic REJECTED + closed_at / reason; COD VOIDED; ONLINE REFUND_PENDING, refund_amount=C replaces any partial owed amount. No payout. Open offer DECLINED; helpers are real module functions. Rowcount, busy and failure-through-COMMIT rollback†. Root-adopted P4-TARGET: release_payment persists the full-C refund amount together with state and checks every conditional save in the same transaction (F-02; P2-S01; P3-S03).

### 3.5.5 Final Design Class Diagram

Changes from 3.5.2: **none in the selected member set**. Sequence reconciliation used the same selection from the outset: real route functions, controller methods, domain behavior, module helpers and implicit dataclass initializations are already present. Properties stay attribute reads. The final plates repeat the full selected exact signatures so every call receiver resolves; relation plates provide root-corrected navigation and layer dependencies. The pure-domain fingerprint inputs and full-refund helper target are synchronized with the reviewed shared model. Root-owned targets remain † until P4 and re-verification.

![UC-05 final — selected design members 1/7](../../../models/UC-05/dcd_uc05_final_PartA.png)

Figure 3.5.5A. UC-05 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — selected design members 2/7](../../../models/UC-05/dcd_uc05_final_PartB.png)

Figure 3.5.5B. UC-05 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — selected design members 3/7](../../../models/UC-05/dcd_uc05_final_PartC.png)

Figure 3.5.5C. UC-05 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — selected design members 4/7](../../../models/UC-05/dcd_uc05_final_PartD.png)

Figure 3.5.5D. UC-05 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — selected design members 5/7](../../../models/UC-05/dcd_uc05_final_PartE.png)

Figure 3.5.5E. UC-05 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — selected design members 6/7](../../../models/UC-05/dcd_uc05_final_PartF.png)

Figure 3.5.5F. UC-05 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — selected design members 7/7](../../../models/UC-05/dcd_uc05_final_PartG.png)

Figure 3.5.5G. UC-05 final detailed design members — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 1](../../../models/UC-05/dcd_uc05_final_links_PartA.png)

Figure 3.5.5.R1. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 2](../../../models/UC-05/dcd_uc05_final_links_PartB.png)

Figure 3.5.5.R2. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 3](../../../models/UC-05/dcd_uc05_final_links_PartC.png)

Figure 3.5.5.R3. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 4](../../../models/UC-05/dcd_uc05_final_links_PartD.png)

Figure 3.5.5.R4. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 5](../../../models/UC-05/dcd_uc05_final_links_PartE.png)

Figure 3.5.5.R5. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 6](../../../models/UC-05/dcd_uc05_final_links_PartF.png)

Figure 3.5.5.R6. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 7](../../../models/UC-05/dcd_uc05_final_links_PartG.png)

Figure 3.5.5.R7. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 8](../../../models/UC-05/dcd_uc05_final_links_PartH.png)

Figure 3.5.5.R8. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 9](../../../models/UC-05/dcd_uc05_final_links_PartI.png)

Figure 3.5.5.R9. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 10](../../../models/UC-05/dcd_uc05_final_links_PartJ.png)

Figure 3.5.5.R10. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 11](../../../models/UC-05/dcd_uc05_final_links_PartK.png)

Figure 3.5.5.R11. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

![UC-05 final — relationships 12](../../../models/UC-05/dcd_uc05_final_links_PartL.png)

Figure 3.5.5.R12. UC-05 final navigation / multiplicities — Author: 722I0004 · AI-assisted (Codex)

All figures require **230 mm landscape** placement: 24 px / 1600 px × 230 mm × 72 / 25.4 = **9.78 pt**. Split parts name their mutual continuation. Native draw.io editing and final DOCX/PDF placement remain **UNTESTED**.

† design target, not yet in code at C0 (see the method-specific P4 inputs in the class tables and operation table). MATCH means Static correspondence only. Sources: locked plan §§2–5/P3/P4/7.3/10–12; primary report template and marking extracts; Phase 2 descriptions, operation catalogue/membership/register and state/domain models; C0 AST inventory and shared design model.

## 3.6 Design for Use Case 6: Maintain brands, menu items and hub listings (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

### 3.6.1 Design Classes in Detailed Design

##### UC-06 design classes

Author: 722I0004 · AI-assisted (Codex)

Source: `models/shared/design_model.json`, C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`. Evidence label: Static / target design. This table is a filtered projection; no application module was imported. `Any` and absent annotations are explicitly inferred. Python visibility follows leading underscores; dataclass fields are public. Constructors are implicit dataclass construction, not invented methods.

† design target, not yet in code at C0 (see P4 inputs P2-S13/P2-S14/P2-S15/P3-S02/P3-S03). MATCH means static correspondence, not executed success.

Templates: `admin/catalogue.html`, `admin/item_form.html`, `admin/hub_menu.html`, shared `error.html`. The `admin` role is the real Flask blueprint module, not a fictional view class.

Types retained as names from code include `Mapping`, `Optional`, `sqlite3.Connection` and business DTOs. A displayed attribute omitted from a narrow figure remains in this table. Association-backing foreign-key IDs remain below but are suppressed on domain DCDs.

##### admin

Layer: **view**; stereotype: **«view»**; responsibility: Translate administrator maintenance routes; never provide business decisions. Source: `saigonbite/presentation/admin.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Operation | `- _hubs() -> HubController` | MATCH |
| Operation | `- _menu() -> MenuController` | MATCH |
| Operation | `+ catalogue() -> Any [inferred] †` | P4-TARGET †; inferred annotation(s); P2-S14 |
| Operation | `+ create_brand() -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ rename_brand(brand_id: int) -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ archive_brand(brand_id: int) -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ new_item() -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ edit_item(item_id: int) -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ archive_item(item_id: int) -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ hub_menu(hub_id: int) -> Any [inferred] †` | P4-TARGET †; inferred annotation(s); P2-S14 |
| Operation | `+ list_item(hub_id: int) -> Any [inferred] †` | P4-TARGET †; inferred annotation(s); P2-S15 |
| Operation | `+ unlist_item(hub_id: int, item_id: int) -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ hub_item_availability(hub_id: int, item_id: int) -> Any [inferred]` | MATCH; inferred annotation(s) |

Route adapters (AST):
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/menu', 'declared_rule': '/menu', 'methods': ['GET'], 'view_function': 'catalogue', 'signature': 'catalogue()', 'decorators': ["bp.get('/menu')", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/brands', 'declared_rule': '/brands', 'methods': ['POST'], 'view_function': 'create_brand', 'signature': 'create_brand()', 'decorators': ["bp.post('/brands')", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/brands/<int:brand_id>', 'declared_rule': '/brands/<int:brand_id>', 'methods': ['POST'], 'view_function': 'rename_brand', 'signature': 'rename_brand(brand_id: int)', 'decorators': ["bp.post('/brands/<int:brand_id>')", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/brands/<int:brand_id>/archive', 'declared_rule': '/brands/<int:brand_id>/archive', 'methods': ['POST'], 'view_function': 'archive_brand', 'signature': 'archive_brand(brand_id: int)', 'decorators': ["bp.post('/brands/<int:brand_id>/archive')", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/items/new', 'declared_rule': '/items/new', 'methods': ['GET', 'POST'], 'view_function': 'new_item', 'signature': 'new_item()', 'decorators': ["bp.route('/items/new', methods=['GET', 'POST'])", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/items/<int:item_id>', 'declared_rule': '/items/<int:item_id>', 'methods': ['GET', 'POST'], 'view_function': 'edit_item', 'signature': 'edit_item(item_id: int)', 'decorators': ["bp.route('/items/<int:item_id>', methods=['GET', 'POST'])", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/items/<int:item_id>/archive', 'declared_rule': '/items/<int:item_id>/archive', 'methods': ['POST'], 'view_function': 'archive_item', 'signature': 'archive_item(item_id: int)', 'decorators': ["bp.post('/items/<int:item_id>/archive')", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/hubs/<int:hub_id>/menu', 'declared_rule': '/hubs/<int:hub_id>/menu', 'methods': ['GET'], 'view_function': 'hub_menu', 'signature': 'hub_menu(hub_id: int)', 'decorators': ["bp.get('/hubs/<int:hub_id>/menu')", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/hubs/<int:hub_id>/menu', 'declared_rule': '/hubs/<int:hub_id>/menu', 'methods': ['POST'], 'view_function': 'list_item', 'signature': 'list_item(hub_id: int)', 'decorators': ["bp.post('/hubs/<int:hub_id>/menu')", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/hubs/<int:hub_id>/menu/<int:item_id>/remove', 'declared_rule': '/hubs/<int:hub_id>/menu/<int:item_id>/remove', 'methods': ['POST'], 'view_function': 'unlist_item', 'signature': 'unlist_item(hub_id: int, item_id: int)', 'decorators': ["bp.post('/hubs/<int:hub_id>/menu/<int:item_id>/remove')", 'role_required(Role.ADMIN)']}`
- `{'blueprint_variable': 'bp', 'blueprint': 'admin', 'rule': '/admin/hubs/<int:hub_id>/menu/<int:item_id>/availability', 'declared_rule': '/hubs/<int:hub_id>/menu/<int:item_id>/availability', 'methods': ['POST'], 'view_function': 'hub_item_availability', 'signature': 'hub_item_availability(hub_id: int, item_id: int)', 'decorators': ["bp.post('/hubs/<int:hub_id>/menu/<int:item_id>/availability')", 'role_required(Role.ADMIN)']}`

##### MenuController

Layer: **controller**; stereotype: **«controller»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/menu_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ menu: MenuDAO` | MATCH; inferred |
| Attribute | `+ hubs: HubDAO` | MATCH; inferred |
| Operation | `+ catalogue(user_id: int) -> Catalogue` | MATCH |
| Operation | `+ create_brand(user_id: int, name: str) -> Brand †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `+ rename_brand(user_id: int, brand_id: int, name: str) -> Brand †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `+ archive_brand(user_id: int, brand_id: int) -> Brand †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `+ create_item(user_id: int, form: Mapping[str, str]) -> MenuItem †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `+ update_item(user_id: int, item_id: int, form: Mapping[str, str]) -> MenuItem †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `+ archive_item(user_id: int, item_id: int) -> MenuItem †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `+ hub_menu(user_id: int, hub_id: int) -> HubMenu` | MATCH |
| Operation | `+ list_item_at_hub(user_id: int, hub_id: int, item_id: int, available: bool = True) -> None †` | P4-TARGET †; P2-S15; P2-S13 |
| Operation | `+ unlist_item_at_hub(user_id: int, hub_id: int, item_id: int) -> None †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `+ set_availability(user_id: int, hub_id: int, item_id: int, available: bool) -> None †` | P4-TARGET †; P2-S13; P3-S03 |
| Operation | `- _require_admin(user_id: int) -> None` | MATCH |
| Operation | `- _hub(hub_id: int) -> Hub` | MATCH |
| Operation | `- _active_brand(brand_id: Any) -> Brand [inferred]` | MATCH; inferred annotation(s) |
| Operation | `- _active_item(item_id: int) -> MenuItem` | MATCH |
| Operation | `- _name(raw: str, label: str, max_len: int = 60) -> str` | MATCH |
| Operation | `- _parse_item(form: Mapping[str, str], item_id: Any) -> MenuItem [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ list_catalogue(user_id: int, hub_id: Optional[int] = None) -> dict[str, object] †` | GAP †; P2-S14 |

##### Catalogue

Layer: **controller**; stereotype: **«value»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/menu_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ brands: list[Brand]` | MATCH |
| Attribute | `+ items: list[MenuItem]` | MATCH |

##### HubMenu

Layer: **controller**; stereotype: **«value»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/menu_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hub: Hub` | MATCH |
| Attribute | `+ listed: list[HubMenuItem]` | MATCH |
| Attribute | `+ not_listed: list[MenuItem]` | MATCH |

##### HubController

Layer: **controller**; stereotype: **«controller»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/hub_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hubs: HubDAO` | MATCH; inferred |
| Operation | `+ list_hubs(user_id: int, include_archived: bool = True) -> list[HubAdminView] †` | P4-TARGET †; P3-S02 |

##### Hub

Layer: **domain**; stereotype: **«entity»**; responsibility: Represent a kitchen location, capacity and fee. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
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

##### Brand

Layer: **domain**; stereotype: **«entity»**; responsibility: Group menu items and retain the archived brand identity. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ name: str` | MATCH |
| Attribute | `+ archived_at: Optional[str]` | MATCH |

##### MenuItem

Layer: **domain**; stereotype: **«entity»**; responsibility: Hold current catalogue text, whole-VND price and archive flag. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ brand_id: int` | MATCH; association backing ID, omitted on DCD |
| Attribute | `+ brand_name: str` | MATCH |
| Attribute | `+ name: str` | MATCH |
| Attribute | `+ description: str` | MATCH |
| Attribute | `+ price: int` | MATCH |
| Attribute | `+ archived_at: Optional[str]` | MATCH |

##### HubMenuItem

Layer: **domain**; stereotype: **«entity»**; responsibility: Represent one hub listing and its independent availability. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hub_id: int` | MATCH; association backing ID, omitted on DCD |
| Attribute | `+ item: MenuItem` | MATCH |
| Attribute | `+ is_available: bool` | MATCH |

##### MenuDAO

Layer: **data_access**; stereotype: **«DAO»**; responsibility: Read or write parameterized records. Source: `saigonbite/data_access/menu_dao.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ list_brands() -> list[Brand]` | MATCH |
| Operation | `+ get_brand(brand_id: int) -> Optional[Brand]` | MATCH |
| Operation | `+ brand_name_exists(name: str, except_id: Optional[int] = None) -> bool` | MATCH |
| Operation | `+ insert_brand(name: str) -> int` | MATCH |
| Operation | `+ rename_brand(brand_id: int, name: str) -> bool` | MATCH |
| Operation | `+ archive_brand(brand_id: int, now: str) -> bool` | MATCH |
| Operation | `+ list_items() -> list[MenuItem]` | MATCH |
| Operation | `+ get_item(item_id: int) -> Optional[MenuItem]` | MATCH |
| Operation | `+ item_name_exists(brand_id: int, name: str, except_id: Optional[int] = None) -> bool` | MATCH |
| Operation | `+ insert_item(item: MenuItem) -> int` | MATCH |
| Operation | `+ update_item(item: MenuItem) -> bool` | MATCH |
| Operation | `+ archive_item(item_id: int, now: str) -> bool` | MATCH |
| Operation | `+ list_hub_items(hub_id: int) -> list[HubMenuItem]` | MATCH |
| Operation | `+ is_listed(hub_id: int, item_id: int) -> bool` | MATCH |
| Operation | `+ add_listing(hub_id: int, item_id: int, available: bool = True) -> None †` | P4-TARGET †; P2-S15 |
| Operation | `+ remove_listing(hub_id: int, item_id: int) -> bool` | MATCH |
| Operation | `+ set_available(hub_id: int, item_id: int, available: bool) -> bool` | MATCH |

##### HubDAO

Layer: **data_access**; stereotype: **«DAO»**; responsibility: Read or write parameterized records. Source: `saigonbite/data_access/hub_dao.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ list_all() -> list[Hub]` | MATCH |
| Operation | `+ get_including_archived(hub_id: int) -> Optional[Hub]` | MATCH |

##### BaseController

Layer: **controller**; stereotype: **«controller»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/common.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Attribute | `+ clock: Any` | MATCH; inferred |
| Attribute | `+ users: UserDAO` | MATCH; inferred |
| Operation | `- _now() -> str` | MATCH |
| Operation | `- _require_user(user_id: int, *roles: Role, message: str = 'Your account cannot do this.') -> UserAccount` | MATCH |

##### UserAccount

Layer: **domain**; stereotype: **«entity»**; responsibility: Hold account identity, role, active flag and optional kitchen-hub assignment. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ username: str` | MATCH |
| Attribute | `+ password_hash: str` | MATCH |
| Attribute | `+ display_name: str` | MATCH |
| Attribute | `+ role: Role` | MATCH |
| Attribute | `+ is_active: bool` | MATCH |
| Attribute | `+ hub_id: Optional[int]` | MATCH; association backing ID, omitted on DCD |
| Attribute | `+ created_at: str` | GAP |

##### Role

Layer: **domain**; stereotype: **«enumeration»**; responsibility: Hold typed business state and its local rules. Source: `saigonbite/business/domain/enums.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ CUSTOMER: str` | MATCH; inferred |
| Attribute | `+ KITCHEN_STAFF: str` | MATCH; inferred |
| Attribute | `+ SHIPPER: str` | MATCH; inferred |
| Attribute | `+ ADMIN: str` | MATCH; inferred |
| Attribute | `+ MANAGER: str` | MATCH; inferred |

##### UserDAO

Layer: **data_access**; stereotype: **«DAO»**; responsibility: Read or write parameterized records. Source: `saigonbite/data_access/user_dao.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ get_by_id(user_id: int) -> Optional[UserAccount]` | MATCH |

##### Boundary adapters and guarantees

`uid()` always comes from the active server session; posted identity is never accepted. Form adapters retain SSD names while converting camelCase fields to Python keys: `address` → `address_text`, `baseDeliveryFee` → `base_delivery_fee`, `capacity` → `max_active_orders`; `brandId` → `brand_id`. Optional parameters map omitted values to the target defaults. Availability is validated as a boolean. Request.form values are strings; controllers parse and validate them.

OP-25 is the GAP `list_catalogue` wrapper, composing `catalogue`, the retained-hub read and optional `hub_menu`; it returns Brand/MenuItem/Hub/HubMenuItem data without adding another SSD operation. The three SSD occurrences remain distinct. OP-43 passes initial `available` into `list_item_at_hub` and `MenuDAO.add_listing` in the same insert (P2-S15). OP-41 uses `brandId` only as current-parent context; `update_item` pins `current.brand_id`, with no reparent/restore. Snapshot OrderLine data is outside every catalogue mutation. A None controller result for listing commands is adapted to a successful acknowledgement called `savedRecord` at the SSD boundary.

Mutation success is acknowledged only after commit. The P2-S13/P3-S03 targets require rowcount/guard checks and controlled busy or commit-error rollback; the Section III figures intentionally hide DAO/SQL behind the persistence note and Section 4.3.2. Draft validation maxima/coordinate windows remain draft constraints (P2-S17), not newly locked BRs.

##### Guarantee responsibility and transaction boundary

`Catalogue` and `HubMenu` are transient result projections, not additional persistent entities. `HubMenuItem` is the association class linking one Hub and one MenuItem; the shared model projects that relationship as Hub 1 → 0..* HubMenuItem and HubMenuItem 0..* → 1 MenuItem. Brand 1 → 0..* MenuItem remains independent of listing availability.

| Anchor / request | Named responsibility | Boundary |
|---|---|---|
| UC06-PC01 | MenuController.create_brand / rename_brand / archive_brand / create_item / update_item / archive_item; the corresponding MenuDAO insert/update/archive methods | BEGIN IMMEDIATE; guards and conditional-save outcomes checked; acknowledge after commit † |
| UC06-PC02 | MenuController.list_item_at_hub / set_availability / unlist_item_at_hub; MenuDAO.add_listing / set_available / remove_listing | BEGIN IMMEDIATE; add_listing writes initial requested flag in the same insert † |
| UC06-PC03 | archive_brand / archive_item / set_availability change archive/availability facts; HubDAO.get_available_item checks hub pair, availability and the orderable-parent predicate for checkout | Atomic fact change †; orderability is rechecked by the consuming order request, never inferred from a prior page |
| UC06-MG01 | update_item / archive_item / archive_brand / unlist_item_at_hub touch only catalogue/listing records; OrderLine snapshot rows are outside these writes | Atomic write/rollback †; successful price changes also leave snapshots unchanged |
| UC06-MG02 | MenuController._name / _parse_item, _active_brand / _active_item, and duplicate checks in public mutators | Guard + uniqueness within BEGIN IMMEDIATE; no partial change † |
| listCatalogue (three occurrences) | MenuController.list_catalogue † composes the existing reads, with optional hub filter; _require_admin / BaseController._require_user rechecks active Admin | Read; zero persistent writes |

† These are design targets where P2-S13/P3-S03 or the operation-specific gap is recorded; no transaction success was executed in P3. The full DAO realization is in Section 4.3.2.

Shared-model classification: `HubMenuItem.association_class = true`. Association class of Hub and MenuItem; one hub_menu_item row per pair, with independent is_available. The controller has a logical persistence responsibility for this class mediated by MenuDAO; this does not assert a direct Python behavior call on the dataclass.

Reviewed adapter status: `admin.catalogue` and `admin.hub_menu` are P4-TARGET † (P2-S14); `admin.list_item` is P4-TARGET † (P2-S15). Existing route symbols alone do not qualify those target behaviors as MATCH.


### 3.6.2 Design Class Diagram

Each sheet is generated from the shared model. Method-rich layer views and operation projections are split at 230 mm landscape width; sequences use 170 mm portrait width; all parts must be retained. The full typed class table resolves members omitted in narrow operation projections. A downward dashed arrow is a dependency; a solid domain association has multiplicities and navigability. Domain classes own no application dependency.

#### i. Domain design class

![UC-06 domain 1](../../../models/UC-06/dcd_uc06_domain_PartA.png)

Figure 3.6.2iA. UC-06 domain projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 domain 2](../../../models/UC-06/dcd_uc06_domain_PartB.png)

Figure 3.6.2iB. UC-06 domain projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 domain 3](../../../models/UC-06/dcd_uc06_domain_PartC.png)

Figure 3.6.2iC. UC-06 domain projection 3 — Author: 722I0004 · AI-assisted (Codex)

#### ii. Controller

![UC-06 controller 1](../../../models/UC-06/dcd_uc06_controller_PartA.png)

Figure 3.6.2iiA. UC-06 controller projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 controller 2](../../../models/UC-06/dcd_uc06_controller_PartB.png)

Figure 3.6.2iiB. UC-06 controller projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 controller 3](../../../models/UC-06/dcd_uc06_controller_PartC.png)

Figure 3.6.2iiC. UC-06 controller projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 controller 4](../../../models/UC-06/dcd_uc06_controller_PartD.png)

Figure 3.6.2iiD. UC-06 controller projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 controller 5](../../../models/UC-06/dcd_uc06_controller_PartE.png)

Figure 3.6.2iiE. UC-06 controller projection 5 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 controller 6](../../../models/UC-06/dcd_uc06_controller_PartF.png)

Figure 3.6.2iiF. UC-06 controller projection 6 — Author: 722I0004 · AI-assisted (Codex)

#### iii. UI (view)

![UC-06 view 1](../../../models/UC-06/dcd_uc06_view_PartA.png)

Figure 3.6.2iiiA. UC-06 view projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 view 2](../../../models/UC-06/dcd_uc06_view_PartB.png)

Figure 3.6.2iiiB. UC-06 view projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 view 3](../../../models/UC-06/dcd_uc06_view_PartC.png)

Figure 3.6.2iiiC. UC-06 view projection 3 — Author: 722I0004 · AI-assisted (Codex)

#### iv. Data access

![UC-06 dao 1](../../../models/UC-06/dcd_uc06_dao_PartA.png)

Figure 3.6.2ivA. UC-06 dao projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 dao 2](../../../models/UC-06/dcd_uc06_dao_PartB.png)

Figure 3.6.2ivB. UC-06 dao projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 dao 3](../../../models/UC-06/dcd_uc06_dao_PartC.png)

Figure 3.6.2ivC. UC-06 dao projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 dao 4](../../../models/UC-06/dcd_uc06_dao_PartD.png)

Figure 3.6.2ivD. UC-06 dao projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 dao 5](../../../models/UC-06/dcd_uc06_dao_PartE.png)

Figure 3.6.2ivE. UC-06 dao projection 5 — Author: 722I0004 · AI-assisted (Codex)

#### v. Design class (all layers together)

![UC-06 all 1](../../../models/UC-06/dcd_uc06_all_PartA.png)

Figure 3.6.2vA. UC-06 all projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 all 2](../../../models/UC-06/dcd_uc06_all_PartB.png)

Figure 3.6.2vB. UC-06 all projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 all 3](../../../models/UC-06/dcd_uc06_all_PartC.png)

Figure 3.6.2vC. UC-06 all projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 all 4](../../../models/UC-06/dcd_uc06_all_PartD.png)

Figure 3.6.2vD. UC-06 all projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 all 5](../../../models/UC-06/dcd_uc06_all_PartE.png)

Figure 3.6.2vE. UC-06 all projection 5 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 all 6](../../../models/UC-06/dcd_uc06_all_PartF.png)

Figure 3.6.2vF. UC-06 all projection 6 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 all 7](../../../models/UC-06/dcd_uc06_all_PartG.png)

Figure 3.6.2vG. UC-06 all projection 7 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 all 8](../../../models/UC-06/dcd_uc06_all_PartH.png)

Figure 3.6.2vH. UC-06 all projection 8 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 all 9](../../../models/UC-06/dcd_uc06_all_PartI.png)

Figure 3.6.2vI. UC-06 all projection 9 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 all 10](../../../models/UC-06/dcd_uc06_all_PartJ.png)

Figure 3.6.2vJ. UC-06 all projection 10 — Author: 722I0004 · AI-assisted (Codex)

### 3.6.3 OOD with CRC Cards or Communication Diagram

##### UC-06 CRC cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators are actual AST call/typed-field targets or the marked OP-25 / OP-43 targets. Inherited authorization collaborators are explicit. Self-calls remain the same class, not another fictional object.

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| `admin` | Knows: request context. Does: catalogue, create_brand, rename_brand, archive_brand, new_item, edit_item, archive_item, hub_menu, list_item, unlist_item, hub_item_availability, _menu, _hubs. | HubController, MenuController |
| `MenuController` | Knows: menu, hubs. Does: catalogue, hub_menu, list_catalogue, create_brand, rename_brand, archive_brand, create_item, update_item, archive_item, list_item_at_hub, unlist_item_at_hub, set_availability, _require_admin, _hub, _active_brand, _active_item, _name, _parse_item. | BaseController, Brand, Catalogue, ConflictError, HubDAO, HubMenu, MenuDAO, MenuItem, NotFoundError, ValidationError, admin; HubMenuItem (logical responsibility via MenuDAO, no direct dataclass method call; OP-25/OP-43 targets † included) |
| `Catalogue` | Knows: brands, items. Does: holds typed state; no invented update/archive behavior. | Brand, MenuController, MenuItem |
| `HubMenu` | Knows: hub, listed, not_listed. Does: holds typed state; no invented update/archive behavior. | Hub, HubMenuItem, MenuController, MenuItem |
| `HubController` | Knows: hubs. Does: list_hubs. | BaseController, Hub, HubAdminView, HubDAO, HubStatus, admin |
| `Hub` | Knows: id, code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee, archived_at. Does: holds typed state; no invented update/archive behavior. | HubController, HubDAO, HubMenu |
| `Brand` | Knows: id, name, archived_at. Does: holds typed state; no invented update/archive behavior. | Catalogue, MenuController, MenuDAO |
| `MenuItem` | Knows: id, brand_id, brand_name, name, description, price, archived_at. Does: holds typed state; no invented update/archive behavior. | Catalogue, HubDAO, HubMenu, HubMenuItem, MenuController, MenuDAO |
| `HubMenuItem` | Knows: hub_id, item, is_available. Does: holds typed state; no invented update/archive behavior. | HubDAO, HubMenu, MenuDAO, MenuItem; MenuController (logical responsibility mediated by MenuDAO) |
| `MenuDAO` | Knows: conn. Does: list_brands, get_brand, brand_name_exists, insert_brand, rename_brand, archive_brand, list_items, get_item, item_name_exists, insert_item, update_item, archive_item, list_hub_items, is_listed, add_listing, remove_listing, set_available. | Brand, HubMenuItem, MenuController, MenuItem |
| `HubDAO` | Knows: conn. Does: list_all, get_including_archived. | Hub, HubController, MenuController |
| `BaseController` | Knows: conn, clock, users. Does: _require_user, _now. | AuthorizationError, UserDAO |
| `UserAccount` | Knows: id, username, password_hash, display_name, role, is_active, hub_id, created_at. Does: holds typed state; no invented update/archive behavior. | Role |
| `Role` | Knows: CUSTOMER, KITCHEN_STAFF, SHIPPER, ADMIN, MANAGER. Does: holds typed state; no invented update/archive behavior. | UserAccount |
| `UserDAO` | Knows: conn. Does: get_by_id. | BaseController |

HubMenuItem is the shared-model association class of Hub and MenuItem. Its independent is_available belongs to one pair. The approved logical MenuController collaborator is deliberately distinguished from a direct Python call target.

The existing admin route functions catalogue/hub_menu/list_item remain marked behavioral targets for the wrapper/initial-availability adapters (P2-S14/P2-S15); symbol existence does not clear those obligations.


### 3.6.4 OOD with Sequence Diagram

Place the following sequence figures at **170 mm portrait width** (23 px minimum source text = 9.236 pt at placement). DCD sheets use **230 mm landscape width** (18 px = 9.780 pt).

Each exact SSD boundary request maps to a real blueprint route adapter and controller method. The active server session supplies uid(); camelCase names map to validated Python arguments/form keys in .1. The domain objects are dataclasses: a create arrow denotes implicit construction and a note denotes state inspection; no invented domain archive/update method is called. Return labels name outcomes, not callable methods. Persistence is a note referring to 4.3.2; Section III contains no DAO lifeline or SQL. Every guard is checked again at the mutation boundary. Technical-failure operands require rollback before acknowledging a no-change outcome.

The listCatalogue PartA/PartB/PartC figures preserve three distinct SSD occurrences of OP-25; they deliberately retain the same system request. Hub-filter routing may use `admin.hub_menu(hub_id)` instead of `admin.catalogue()`; the displayed module role remains `admin`. The GAP wrapper and initial-availability targets remain daggered. OP-41 current-parent context is pinned; no reparent/restore is introduced.

![UC-06 sequence 1](../../../models/UC-06/seq_uc06_listCatalogue_PartA.png)

Figure 3.6.4A. UC-06 sequence projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 2](../../../models/UC-06/seq_uc06_createBrand.png)

Figure 3.6.4B. UC-06 sequence projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 3](../../../models/UC-06/seq_uc06_updateBrand.png)

Figure 3.6.4C. UC-06 sequence projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 4](../../../models/UC-06/seq_uc06_archiveBrand.png)

Figure 3.6.4D. UC-06 sequence projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 5](../../../models/UC-06/seq_uc06_listCatalogue_PartB.png)

Figure 3.6.4E. UC-06 sequence projection 5 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 6](../../../models/UC-06/seq_uc06_createMenuItem.png)

Figure 3.6.4F. UC-06 sequence projection 6 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 7](../../../models/UC-06/seq_uc06_updateMenuItem.png)

Figure 3.6.4G. UC-06 sequence projection 7 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 8](../../../models/UC-06/seq_uc06_archiveMenuItem.png)

Figure 3.6.4H. UC-06 sequence projection 8 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 9](../../../models/UC-06/seq_uc06_listCatalogue_PartC.png)

Figure 3.6.4I. UC-06 sequence projection 9 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 10](../../../models/UC-06/seq_uc06_listItemAtHub.png)

Figure 3.6.4J. UC-06 sequence projection 10 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 11](../../../models/UC-06/seq_uc06_setListingAvailability.png)

Figure 3.6.4K. UC-06 sequence projection 11 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 sequence 12](../../../models/UC-06/seq_uc06_unlistItemAtHub.png)

Figure 3.6.4L. UC-06 sequence projection 12 — Author: 722I0004 · AI-assisted (Codex)

### 3.6.5 Final Design Class Diagram

Changes from 3.6.2: none in selected signatures. The final figures repeat the reconciled operation projections explicitly; the union includes every view/controller call shown in .4, including `_require_admin`. Domain create/note messages are construction/attribute facts, not additional callable operations. Full attributes and support authorization/DTO collaborators remain in the layer views and .1. Every final part continues the same UC projection set.

![UC-06 final 1](../../../models/UC-06/dcd_uc06_final_PartA.png)

Figure 3.6.5A. UC-06 final projection 1 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 final 2](../../../models/UC-06/dcd_uc06_final_PartB.png)

Figure 3.6.5B. UC-06 final projection 2 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 final 3](../../../models/UC-06/dcd_uc06_final_PartC.png)

Figure 3.6.5C. UC-06 final projection 3 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 final 4](../../../models/UC-06/dcd_uc06_final_PartD.png)

Figure 3.6.5D. UC-06 final projection 4 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 final 5](../../../models/UC-06/dcd_uc06_final_PartE.png)

Figure 3.6.5E. UC-06 final projection 5 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 final 6](../../../models/UC-06/dcd_uc06_final_PartF.png)

Figure 3.6.5F. UC-06 final projection 6 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 final 7](../../../models/UC-06/dcd_uc06_final_PartG.png)

Figure 3.6.5G. UC-06 final projection 7 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 final 8](../../../models/UC-06/dcd_uc06_final_PartH.png)

Figure 3.6.5H. UC-06 final projection 8 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 final 9](../../../models/UC-06/dcd_uc06_final_PartI.png)

Figure 3.6.5I. UC-06 final projection 9 — Author: 722I0004 · AI-assisted (Codex)

![UC-06 final 10](../../../models/UC-06/dcd_uc06_final_PartJ.png)

Figure 3.6.5J. UC-06 final projection 10 — Author: 722I0004 · AI-assisted (Codex)

† design target, not yet in code at C0 (see the operation-specific P4 input in the figure and `operation_realisation.csv`). Shared busy/commit/rowcount requirements are P2-S13/P3-S03 targets; no runtime correctness is asserted. Native draw.io editing and final DOCX/PDF placement remain UNTESTED.

Integration maintenance (Author: 722I0004 · AI-assisted (Codex)): native draw.io text now has explicit actual font sizes and bold styles matching the SVG/PNG labels: 18 px minimum at 230 mm for DCDs and 23 px minimum at 170 mm for sequences. Native editing remains UNTESTED. Reviewed behavioral targets remain daggered; mere symbol/signature correspondence does not clear them. The canonical association-class classification of HubMenuItem and the approved logical MenuController → HubMenuItem persistence responsibility are reflected in the regenerated projections; this is mediated by MenuDAO, not a direct dataclass method call.
