# UC-01 design classes

Author: 722I0004 · AI-assisted (Codex)

Each table lists the members of one design class. "Matches code" means the member exists in the code with exactly this signature. "Changed during implementation and tested" means the first design (commit C0 = 45ac762, 24/10/2026) was corrected while coding; the reason is given and the tests are listed in Table P4-1 (Appendix).

Properties have signatures for traceability but are read as attributes; dataclass «create» means implicit initialization, not an invented business method. Unannotated types are marked inferred. Templates are presentation resources, not design classes.

## PlaceOrderController

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «controller» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | Changed during implementation and tested (P4.3; Table P4-1 rows 2, 3, 4) |
| Source | `saigonbite/business/controllers/place_order_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ customers: CustomerDAO` **inferred** | Matches code |
| Attribute | `+ hubs: HubDAO` **inferred** | Matches code |
| Attribute | `+ orders: OrderDAO` **inferred** | Matches code |
| Attribute | `+ payments: PaymentDAO` **inferred** | Matches code |
| Attribute | `+ vouchers: VoucherDAO` **inferred** | Matches code |
| Attribute | `+ gateway: Any` **inferred** | Matches code |
| Operation | `+ list_hubs(self) -> list[HubStatus]` | Matches code |
| Operation | `+ select_hub(self, user_id: int, hub_id: int) -> HubMenuView` | Matches code |
| Operation | `+ request_quote(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None) -> Quote` | Changed during implementation and tested (P4.3; Table P4-1 rows 2); Reason: F-04; F-07; P3-S01; Use raw distance; include payment choice and a full quote fingerprint; rank suggestions by load ratio, distance and ID. |
| Operation | `+ confirm_order(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], idempotency_token: str, quoted_total: Optional[int] = None, voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None, quote_fingerprint: Optional[str] = None) -> OrderConfirmation` | Changed during implementation and tested (P4.3; Table P4-1 rows 3); Reason: F-04; F-07; P2-S05; P2-S13; Compare full fingerprint and T; release simulator authorization on every failure through COMMIT. |
| Operation | `- _build_quote(self, customer: Customer, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], voucher_code: Optional[str]) -> Quote` | Matches code |
| Operation | `+ suggest_hubs(self, exclude_hub_id: int, address: Optional[Address]) -> list[HubStatus]` | Changed during implementation and tested (P4.3; Table P4-1 rows 4); Reason: P3-S01; F-04; Draft sorts by load ratio then ID; BR-04 requires distance as the second key and raw distance for range. |
| Operation | `- _require_customer(self, user_id: int) -> Customer` | Matches code |
| Operation | `- _check_payment_choice(customer: Customer, payment: PaymentChoice) -> None` | Matches code |

## order

| Detail | Design |
|---|---|
| Layer / stereotype | view / «view» |
| Responsibility | Translate authenticated customer routes and render quote, receipt and order results. |
| Class status | Changed during implementation and tested (P4.3; Table P4-1 rows 60, 61) |
| Source | `saigonbite/presentation/order.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ choose_hub() -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |
| Operation | `+ choose_items(hub_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |
| Operation | `+ quote() -> Any [inferred return]` **inferred unannotated parameter/return** | Changed during implementation and tested (P4.3; Table P4-1 rows 61); Reason: F-07; Pass payment choice into target quoting and render the full fingerprint. |
| Operation | `+ confirm() -> Any [inferred return]` **inferred unannotated parameter/return** | Changed during implementation and tested (P4.3; Table P4-1 rows 60); Reason: F-07; P2-S05; Bind the posted fingerprint/payment choice to the target confirm method; retain controlled results through COMMIT. |
| Operation | `+ detail(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |
| Operation | `+ my_orders() -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |
| Operation | `+ cancel(order_id: int) -> Any [inferred return]` **inferred unannotated parameter/return** | Matches code |

## HubStatus

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Derive busy, quiet and load percentage from current load and capacity. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hub: Hub` | Matches code |
| Attribute | `+ load: int` | Matches code |
| Read-only property | `+ busy(self) -> bool {property; read as .busy}` | Matches code |
| Read-only property | `+ quiet(self) -> bool {property; read as .quiet}` | Matches code |

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
| Operation | `+ active_loads(self) -> dict[int, int]` | Matches code |
| Operation | `+ list_active(self) -> list[Hub]` | Matches code |
| Operation | `+ active_load(self, hub_id: int) -> int` | Matches code |
| Operation | `+ get(self, hub_id: int) -> Optional[Hub]` | Matches code |
| Operation | `+ list_menu(self, hub_id: int) -> list[HubMenuItem]` | Matches code |
| Operation | `+ get_available_item(self, hub_id: int, menu_item_id: int) -> Optional[MenuItem]` | Matches code |
| Operation | `+ get_including_archived(self, hub_id: int) -> Optional[Hub]` | Matches code |

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
| Operation | `+ list_addresses(self, customer_id: int) -> list[Address]` | Matches code |
| Operation | `+ get_address(self, address_id: int, customer_id: int) -> Optional[Address]` | Matches code |

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
| Operation | `+ distance_to(self, address: Address) -> float` | Changed during implementation and tested (P4.3; Table P4-1 rows 7, 8); Reason: F-04; Keep raw Haversine precision through the radius and fee decisions; round only presentation/storage. |

## Quote

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Compute and bind the complete consented price; not persisted. |
| Class status | Changed during implementation and tested (P4.3; Table P4-1 rows 5, 6) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hub: Hub` | Matches code |
| Attribute | `+ address: Address` | Matches code |
| Attribute | `+ lines: list[OrderLine]` | Matches code |
| Attribute | `+ distance_km: float` | Matches code |
| Attribute | `+ delivery_fee: int` | Matches code |
| Attribute | `+ quiet_discount: int` | Matches code |
| Attribute | `+ voucher: Optional[Voucher]` | Matches code |
| Attribute | `+ voucher_discount: int` | Matches code |
| Operation | `+ fingerprint(self, payment_method: PaymentMethod, online_option: Optional[OnlineOption] = None) -> str` | Changed during implementation and tested (P4.3; Table P4-1 rows 5, 6); Reason: F-07; Bind all consent fields with pure-domain enum inputs; the controller adapts PaymentChoice. |
| Read-only property | `+ total(self) -> int {property; read as .total}` | Matches code |

## Voucher

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «entity» |
| Responsibility | Check date/subtotal eligibility and calculate the bounded discount. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/models.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ id: int` | Matches code |
| Attribute | `+ code: str` | Matches code |
| Attribute | `+ description: str` | Matches code |
| Attribute | `+ discount_type: DiscountType` | Matches code |
| Attribute | `+ discount_value: int` | Matches code |
| Attribute | `+ min_subtotal: int` | Matches code |
| Attribute | `+ max_discount: Optional[int]` | Matches code |
| Attribute | `+ valid_from: str` | Matches code |
| Attribute | `+ valid_until: str` | Matches code |
| Attribute | `+ archived_at: Optional[str]` | Matches code |
| Operation | `+ discount_for(self, item_subtotal: int) -> int` | Matches code |
| Operation | `+ problem(self, item_subtotal: int, today: str) -> Optional[str]` | Matches code |

## VoucherDAO

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «DAO» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/voucher_dao.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Operation | `+ get_by_code(self, code: str) -> Optional[Voucher]` | Matches code |

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
| Operation | `+ place(cls, customer_id: int, quote: Quote, idempotency_token: str, placed_at: str) -> 'Order'` | Matches code |
| Operation | `+ move_to(self, new_state: OrderState) -> None` | Matches code |
| Operation | `+ replace_line(self, line_id: int, menu_item_id: int, item_name: str, unit_price: int) -> None` | Matches code |
| Operation | `+ line(self, line_id: int) -> Optional[OrderLine]` | Matches code |

## PaymentGatewaySimulator

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «gateway» |
| Responsibility | Read or write parameterized records. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/payment_gateway.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ authorise(self, amount: int, option: OnlineOption, outcome: str) -> Authorisation` | Matches code |
| Operation | `+ release(self, reference: str) -> None` | Matches code |

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
| Operation | `+ get_by_id(self, order_id: int) -> Optional[Order]` | Matches code |
| Operation | `+ get_by_token(self, token: str) -> Optional[Order]` | Matches code |
| Operation | `+ insert(self, order: Order) -> int` | Matches code |
| Operation | `+ list_for_customer(self, customer_id: int) -> list[Order]` | Matches code |
| Operation | `+ change_state(self, order_id: int, from_state: OrderState, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> bool` | Matches code |

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
| Operation | `+ insert(self, payment: Payment) -> int` | Matches code |
| Operation | `+ change_state(self, order_id: int, from_state: PaymentState, to_state: PaymentState, now: str) -> bool` | Matches code |
| Operation | `+ set_amounts(self, order_id: int, amount: int, refund_amount: int, now: str) -> bool` | Changed during implementation and tested (P4.4; Table P4-1 rows 46, 47, 48, 49, 50); Reason: F-02; P3-S03; Persist full/partial refund obligations atomically and expose the conditional save outcome. |

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
| Operation | `+ get_order(self, user_id: int, order_id: int) -> OrderDetail` | Matches code |
| Operation | `+ list_my_orders(self, user_id: int) -> list[OrderSummary]` | Matches code |
| Operation | `+ cancel_order(self, user_id: int, order_id: int) -> OrderDetail` | Changed during implementation and tested (P4.4; Table P4-1 rows 15); Reason: F-02; P2-S13; BR-17 full C refund owed and atomic state/amount writes, including COMMIT rollback. |
| Operation | `- _own_order(self, customer: Customer, order_id: int) -> Order` | Matches code |
| Operation | `- _require_customer(self, user_id: int) -> Customer` | Matches code |

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

## PaymentChoice

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/place_order_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ method: PaymentMethod` | Matches code |
| Attribute | `+ option: Optional[OnlineOption]` | Matches code |
| Attribute | `+ outcome: Optional[str]` | Matches code |

## OrderConfirmation

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/place_order_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ order: Order` | Matches code |
| Attribute | `+ payment: Payment` | Matches code |
| Attribute | `+ hub: Hub` | Matches code |
| Attribute | `+ created: bool` | Matches code |

## HubMenuView

| Detail | Design |
|---|---|
| Layer / stereotype | controller / «value» |
| Responsibility | Coordinate authorization, domain decisions and data access. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/controllers/place_order_controller.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ hub: Hub` | Matches code |
| Attribute | `+ status: HubStatus` | Matches code |
| Attribute | `+ menu: list[HubMenuItem]` | Matches code |
| Attribute | `+ addresses: list[Address]` | Matches code |

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

## Authorisation

| Detail | Design |
|---|---|
| Layer / stereotype | data_access / «value» |
| Responsibility | Carry the local simulator decision, reference and message; not persisted. |
| Class status | MATCH (Static) |
| Source | `saigonbite/data_access/payment_gateway.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ approved: bool` | Matches code |
| Attribute | `+ reference: Optional[str]` | Matches code |
| Attribute | `+ message: str` | Matches code |

## domain.rules

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «module» |
| Responsibility | Module functions with their original Python signatures. |
| Class status | Changed during implementation and tested (P4.3; Table P4-1 rows 55) |
| Source | `saigonbite/business/domain/rules.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Operation | `+ delivery_fee(base_fee: int, km: float) -> int` | Matches code |
| Operation | `+ quiet_discount(load: int, capacity: int, fee: int) -> int` | Matches code |

## DiscountType

| Detail | Design |
|---|---|
| Layer / stereotype | domain / «enumeration» |
| Responsibility | Hold typed business state and its local rules. |
| Class status | MATCH (Static) |
| Source | `saigonbite/business/domain/enums.py` |

| Kind | Visible typed member / exact signature | Status / evidence |
|---|---|---|
| Attribute | `+ FIXED: str` **inferred** | Matches code |
| Attribute | `+ PERCENT: str` **inferred** | Matches code |
| Enumeration | FIXED, PERCENT | Matches code |

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

Templates used by the selected blueprint module(s): `order/confirmation.html`, `order/detail.html`, `order/hubs.html`, `order/menu.html`, `order/my_orders.html`, `order/payment_simulator.html`, `order/quote.html`.

Non-persisted values include Quote, PaymentChoice, HubStatus, response dataclasses and Authorisation. Busy/quiet are derived properties; no Busy/Quiet enum is introduced. No refund payout is designed.
