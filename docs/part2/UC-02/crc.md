# UC-02 CRC Cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators are real classes/modules linked by the AST-derived shared model (calls or typed attributes); target-only collaborators are identified as P4 targets. Blueprints and helpers remain real modules. No communication diagram is added.

## Delivery — domain / «entity»

**Knows:** state: DeliveryState, ready_at: str, picked_up_at: Optional[str], finished_at: Optional[str], failure_reason: Optional[str], cash_collected: Optional[int], id: Optional[int]
**Does:** Hold assignment, paired lifecycle times, cash and failure outcome.; operations: move_to
**Collaborators:** DeliveryState

## Order — domain / «entity»

**Knows:** state: OrderState, delivery_fee: int, idempotency_token: str, placed_at: str, lines: list[OrderLine], id: Optional[int], archived_at: Optional[str], delivery_address_text: str, distance_km: float, voucher_discount: int, quiet_discount: int, reject_reason: Optional[str], confirmed_at: Optional[str], ready_at: Optional[str], closed_at: Optional[str]
**Does:** Own the order lifecycle, snapshots and accepted replacement totals.; operations: can_move_to, move_to
**Collaborators:** OrderState

## Payment — domain / «entity»

**Knows:** method: PaymentMethod, state: PaymentState, amount: int, created_at: str, updated_at: Optional[str], online_option: Optional[OnlineOption], provider_ref: Optional[str], refund_amount: int, id: Optional[int]
**Does:** Hold captured amount C and refund obligations without claiming payout.; operations: move_to, release_for_unfulfilled_order †
**Collaborators:** PaymentState

## UserAccount — domain / «entity»

**Knows:** id: int, username: str, password_hash: str, display_name: str, role: Role, is_active: bool, created_at: str
**Does:** Hold account identity, role, active flag and optional kitchen-hub assignment.; operations: value/module role only.
**Collaborators:** Role

## Hub — domain / «entity»

**Knows:** id: int, code: str, name: str, address_text: str, latitude: float, longitude: float, max_active_orders: int, base_delivery_fee: int, archived_at: Optional[str]
**Does:** Represent a kitchen location, capacity and fee.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

## Customer — domain / «entity»

**Knows:** id: int, full_name: str, phone: Optional[str], email: Optional[str], passport_no: Optional[str], nationality: Optional[str], customer_type: CustomerType
**Does:** Represent customer identity and permitted online payment choices.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

## DeliveryState — domain / «enumeration»

**Knows:** AWAITING_PICKUP: str, PICKED_UP: str, DELIVERED: str, FAILED: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

## OrderState — domain / «enumeration»

**Knows:** PLACED: str, CONFIRMED: str, REJECTED: str, PREPARING: str, READY: str, OUT_FOR_DELIVERY: str, DELIVERED: str, DELIVERY_FAILED: str, CANCELLED: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

## PaymentState — domain / «enumeration»

**Knows:** PENDING: str, PAID: str, FAILED: str, VOIDED: str, REFUND_PENDING: str, REFUNDED: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

## Role — domain / «enumeration»

**Knows:** CUSTOMER: str, KITCHEN_STAFF: str, SHIPPER: str, ADMIN: str, MANAGER: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

## DeliveryController — controller / «controller»

**Knows:** deliveries: DeliveryDAO, orders: OrderDAO, payments: PaymentDAO, hubs: HubDAO, customers: CustomerDAO
**Does:** Coordinate authorization, domain decisions and data access.; operations: board, get_delivery, pick_up †, confirm_delivered †, report_failure †, _require_shipper, _delivery, _own_active_delivery, _parse_cash, _view
**Collaborators:** CustomerDAO, Delivery, DeliveryDAO, DeliveryView, HubDAO, OrderDAO, Payment, PaymentDAO, ShipperBoard, UserAccount, controllers.common

## BaseController — controller / «controller»

**Knows:** conn: sqlite3.Connection, clock: Any, users: UserDAO
**Does:** Coordinate authorization, domain decisions and data access.; operations: _now, _require_user
**Collaborators:** Role, UserAccount, UserDAO

## controllers.common — controller / «module»

**Knows:** No instance attributes in the shared model.
**Does:** Module functions with their original Python signatures.; operations: move_order, release_payment †
**Collaborators:** Order, OrderDAO, OrderState, Payment, PaymentDAO

## DeliveryView — controller / «value»

**Knows:** delivery: Delivery, order: Order, payment: Payment, hub: Hub, customer: Customer
**Does:** Coordinate authorization, domain decisions and data access.; operations: cash_to_collect
**Collaborators:** Customer, Delivery, Hub, Order, Payment

## ShipperBoard — controller / «value»

**Knows:** waiting: list[DeliveryView], mine: list[DeliveryView], finished: list[DeliveryView]
**Does:** Coordinate authorization, domain decisions and data access.; operations: value/module role only.
**Collaborators:** DeliveryView

## delivery — view / «view»

**Knows:** No instance attributes in the shared model.
**Does:** Translate shipper requests and render contact and cash information.; operations: board, detail, pick_up, delivered, failed
**Collaborators:** DeliveryController

## DeliveryDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_by_order_id, list_awaiting_pickup, list_for_shipper, take, finish
**Collaborators:** Delivery, DeliveryState, delivery

## OrderDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_by_id, change_state, _load
**Collaborators:** Order, OrderState

## PaymentDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_by_order_id, change_state, set_amounts †
**Collaborators:** Payment, PaymentState

## CustomerDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get
**Collaborators:** Customer

## HubDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_including_archived
**Collaborators:** Hub

## UserDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_by_id
**Collaborators:** UserAccount

## Privacy and assignment boundary

Shipper-facing DeliveryView contains only the permitted contact and stored address snapshot. Customer.passport_no is not part of the shipper projection. The Delivery-to-UserAccount association carries the optional assigned-shipper role; no shipper class is fabricated.

## Architecture correspondence

Actual DAO imports of domain values remain static couplings in these CRC collaborators; they are an upward-dependency P4.9 finding documented in section 4.2, and are not drawn as permitted dependencies in the layered DCD.
