# UC-02 Design Classes

Author: 722I0004 · AI-assisted (Codex)

C0: 45ac76221b0a103174c7c01d17577e6e49cfd665 · Evidence: Static source correspondence only; this is not runtime or test evidence.

The tables use the sole shared DCD model at C0. Visibility follows the leading-underscore convention; signatures preserve the AST inventory. * marks an inferred/unannotated type or route signature. † marks a P4-TARGET/GAP and does not mean implemented at C0. Domain FK scalar attributes are retained here for mapping but omitted from DCDs in favour of associations.

## Delivery

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


## Order

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


## Payment

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


## UserAccount

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


## Hub

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


## Customer

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


## DeliveryState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute AWAITING_PICKUP | + | str | MATCH | inferred; default='AWAITING_PICKUP' |
| Attribute PICKED_UP | + | str | MATCH | inferred; default='PICKED_UP' |
| Attribute DELIVERED | + | str | MATCH | inferred; default='DELIVERED' |
| Attribute FAILED | + | str | MATCH | inferred; default='FAILED' |


## OrderState

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


## PaymentState

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


## Role

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute CUSTOMER | + | str | MATCH | inferred; default='CUSTOMER' |
| Attribute KITCHEN_STAFF | + | str | MATCH | inferred; default='KITCHEN_STAFF' |
| Attribute SHIPPER | + | str | MATCH | inferred; default='SHIPPER' |
| Attribute ADMIN | + | str | MATCH | inferred; default='ADMIN' |
| Attribute MANAGER | + | str | MATCH | inferred; default='MANAGER' |


## DeliveryController

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


## BaseController

Layer: controller · Stereotype: «controller» · Module: saigonbite/business/controllers/common.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Attribute clock | + | Any | MATCH | inferred |
| Attribute users | + | UserDAO | MATCH | inferred |
| Method _now | - | _now(self) -> str | MATCH | — |
| Method _require_user | - | _require_user(self, user_id: int, *roles: Role, message: str='Your account cannot do this.') -> UserAccount | MATCH | — |


## controllers.common

Layer: controller · Stereotype: «module» · Module: saigonbite/business/controllers/common.py

Responsibility: Module functions with their original Python signatures.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method move_order | + | move_order(orders: OrderDAO, order: Order, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> None | MATCH | — |
| Method release_payment | + | release_payment(payments: PaymentDAO, order_id: int, now: str) -> Payment | P4-TARGET | P4 input: F-02; P2-S01; P3-S03; Persist full captured C as refund_amount together with state; changing only the domain object does not save the amount. Check conditional save results in the same transaction. |


## DeliveryView

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


## ShipperBoard

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/delivery_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute waiting | + | list[DeliveryView] | MATCH | — |
| Attribute mine | + | list[DeliveryView] | MATCH | — |
| Attribute finished | + | list[DeliveryView] | MATCH | — |


## delivery

Layer: view · Stereotype: «view» · Module: saigonbite/presentation/delivery.py

Responsibility: Translate shipper requests and render contact and cash information.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method board | + | board() | MATCH | inferred |
| Method detail | + | detail(order_id: int) | MATCH | inferred |
| Method pick_up | + | pick_up(order_id: int) | MATCH | inferred |
| Method delivered | + | delivered(order_id: int) | MATCH | inferred |
| Method failed | + | failed(order_id: int) | MATCH | inferred |


## DeliveryDAO

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


## OrderDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/order_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_by_id | + | get_by_id(self, order_id: int) -> Optional[Order] | MATCH | — |
| Method change_state | + | change_state(self, order_id: int, from_state: OrderState, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> bool | MATCH | — |
| Method _load | - | _load(self, row: Optional[sqlite3.Row]) -> Optional[Order] | MATCH | — |


## PaymentDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/payment_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_by_order_id | + | get_by_order_id(self, order_id: int) -> Optional[Payment] | MATCH | — |
| Method change_state | + | change_state(self, order_id: int, from_state: PaymentState, to_state: PaymentState, now: str) -> bool | MATCH | — |
| Method set_amounts | + | set_amounts(self, order_id: int, amount: int, refund_amount: int, now: str) -> bool | P4-TARGET | P4 input: F-02; P3-S03; Persist full/partial refund obligations atomically and expose the conditional save outcome. |


## CustomerDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/customer_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get | + | get(self, customer_id: int) -> Optional[Customer] | MATCH | — |


## HubDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/hub_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_including_archived | + | get_including_archived(self, hub_id: int) -> Optional[Hub] | MATCH | — |


## UserDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/user_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_by_id | + | get_by_id(self, user_id: int) -> Optional[UserAccount] | MATCH | — |
