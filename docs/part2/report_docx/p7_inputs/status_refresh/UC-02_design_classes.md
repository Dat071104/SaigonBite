# UC-02 Design Classes

Author: 722I0004 · AI-assisted (Codex)

First design commit C0: 45ac762 (24/10/2026). Signatures are compared with the source code; test evidence is in section 5.1.

The tables use the sole shared DCD model at C0. Visibility follows the leading-underscore convention; signatures preserve the AST inventory. * marks an inferred/unannotated type or route signature.  marks a C0 design target (final status in Table P4-1)/C0 design gap (final status in Table P4-1) and does not mean implemented at C0. Domain FK scalar attributes are retained here for mapping but omitted from DCDs in favour of associations.

## Delivery

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Hold assignment, paired lifecycle times, cash and failure outcome.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute order_id | + | int | Matches code | FK scalar omitted from DCD; shown by association |
| Attribute state | + | DeliveryState | Matches code | — |
| Attribute ready_at | + | str | Matches code | — |
| Attribute shipper_id | + | Optional[int] | Matches code | FK scalar omitted from DCD; shown by association; default=None |
| Attribute picked_up_at | + | Optional[str] | Matches code | default=None |
| Attribute finished_at | + | Optional[str] | Matches code | default=None |
| Attribute failure_reason | + | Optional[str] | Matches code | default=None |
| Attribute cash_collected | + | Optional[int] | Matches code | default=None |
| Attribute id | + | Optional[int] | Matches code | default=None |
| Method move_to | + | move_to(self, new_state: DeliveryState) -> None | Matches code | — |


## Order

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Own the order lifecycle, snapshots and accepted replacement totals.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute customer_id | + | int | Matches code | FK scalar omitted from DCD; shown by association |
| Attribute hub_id | + | int | Matches code | FK scalar omitted from DCD; shown by association |
| Attribute address_id | + | int | Matches code | FK scalar omitted from DCD; shown by association |
| Attribute state | + | OrderState | Matches code | — |
| Attribute delivery_fee | + | int | Matches code | — |
| Attribute idempotency_token | + | str | Matches code | — |
| Attribute placed_at | + | str | Matches code | — |
| Attribute lines | + | list[OrderLine] | Matches code | default=field(default_factory=list) |
| Attribute id | + | Optional[int] | Matches code | default=None |
| Attribute archived_at | + | Optional[str] | Matches code | default=None |
| Attribute delivery_address_text | + | str | Matches code | default='' |
| Attribute distance_km | + | float | Matches code | default=0.0 |
| Attribute voucher_id | + | Optional[int] | Matches code | FK scalar omitted from DCD; shown by association; default=None |
| Attribute voucher_discount | + | int | Matches code | default=0 |
| Attribute quiet_discount | + | int | Matches code | default=0 |
| Attribute reject_reason | + | Optional[str] | Matches code | default=None |
| Attribute confirmed_at | + | Optional[str] | Matches code | default=None |
| Attribute ready_at | + | Optional[str] | Matches code | default=None |
| Attribute closed_at | + | Optional[str] | Matches code | default=None |
| Method can_move_to | + | can_move_to(self, new_state: OrderState) -> bool | Matches code | — |
| Method move_to | + | move_to(self, new_state: OrderState) -> None | Matches code | — |


## Payment

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Hold captured amount C and refund obligations without claiming payout.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute order_id | + | int | Matches code | FK scalar omitted from DCD; shown by association |
| Attribute method | + | PaymentMethod | Matches code | — |
| Attribute state | + | PaymentState | Matches code | — |
| Attribute amount | + | int | Matches code | — |
| Attribute created_at | + | str | Matches code | — |
| Attribute updated_at | + | Optional[str] | Matches code | default=None |
| Attribute online_option | + | Optional[OnlineOption] | Matches code | default=None |
| Attribute provider_ref | + | Optional[str] | Matches code | default=None |
| Attribute refund_amount | + | int | Matches code | default=0 |
| Attribute id | + | Optional[int] | Matches code | default=None |
| Method move_to | + | move_to(self, new_state: PaymentState) -> None | Matches code | — |
| Method release_for_unfulfilled_order | + | release_for_unfulfilled_order(self) -> None | Changed during implementation and tested (P4.4; Table P4-1 rows 9, 10, 11, 12) | P4 input: F-02; P2-S01; Set refund_amount=C with REFUND_PENDING; preserve COD VOIDED; no payout operation. |


## UserAccount

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Hold account identity, role, active flag and optional kitchen-hub assignment.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute id | + | int | Matches code | — |
| Attribute username | + | str | Matches code | — |
| Attribute password_hash | + | str | Matches code | — |
| Attribute display_name | + | str | Matches code | — |
| Attribute role | + | Role | Matches code | — |
| Attribute is_active | + | bool | Matches code | default=True |
| Attribute hub_id | + | Optional[int] | Matches code | FK scalar omitted from DCD; shown by association; default=None |
| Attribute created_at | + | str | Changed during implementation and tested (P4.1; Table P4-1 rows 53) | — |


## Hub

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Represent a kitchen location, capacity and fee.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute id | + | int | Matches code | — |
| Attribute code | + | str | Matches code | — |
| Attribute name | + | str | Matches code | — |
| Attribute address_text | + | str | Matches code | — |
| Attribute latitude | + | float | Matches code | — |
| Attribute longitude | + | float | Matches code | — |
| Attribute max_active_orders | + | int | Matches code | — |
| Attribute base_delivery_fee | + | int | Matches code | — |
| Attribute archived_at | + | Optional[str] | Matches code | default=None |


## Customer

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Represent customer identity and permitted online payment choices.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute id | + | int | Matches code | — |
| Attribute user_id | + | int | Matches code | FK scalar omitted from DCD; shown by association |
| Attribute full_name | + | str | Matches code | — |
| Attribute phone | + | Optional[str] | Matches code | default=None |
| Attribute email | + | Optional[str] | Matches code | default=None |
| Attribute passport_no | + | Optional[str] | Matches code | default=None |
| Attribute nationality | + | Optional[str] | Matches code | default=None |
| Attribute customer_type | + | CustomerType | Matches code | inferred; default=CustomerType.LOCAL |


## DeliveryState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute AWAITING_PICKUP | + | str | Matches code | inferred; default='AWAITING_PICKUP' |
| Attribute PICKED_UP | + | str | Matches code | inferred; default='PICKED_UP' |
| Attribute DELIVERED | + | str | Matches code | inferred; default='DELIVERED' |
| Attribute FAILED | + | str | Matches code | inferred; default='FAILED' |


## OrderState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute PLACED | + | str | Matches code | inferred; default='PLACED' |
| Attribute CONFIRMED | + | str | Matches code | inferred; default='CONFIRMED' |
| Attribute REJECTED | + | str | Matches code | inferred; default='REJECTED' |
| Attribute PREPARING | + | str | Matches code | inferred; default='PREPARING' |
| Attribute READY | + | str | Matches code | inferred; default='READY' |
| Attribute OUT_FOR_DELIVERY | + | str | Matches code | inferred; default='OUT_FOR_DELIVERY' |
| Attribute DELIVERED | + | str | Matches code | inferred; default='DELIVERED' |
| Attribute DELIVERY_FAILED | + | str | Matches code | inferred; default='DELIVERY_FAILED' |
| Attribute CANCELLED | + | str | Matches code | inferred; default='CANCELLED' |


## PaymentState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute PENDING | + | str | Matches code | inferred; default='PENDING' |
| Attribute PAID | + | str | Matches code | inferred; default='PAID' |
| Attribute FAILED | + | str | Matches code | inferred; default='FAILED' |
| Attribute VOIDED | + | str | Matches code | inferred; default='VOIDED' |
| Attribute REFUND_PENDING | + | str | Matches code | inferred; default='REFUND_PENDING' |
| Attribute REFUNDED | + | str | Matches code | inferred; default='REFUNDED' |


## Role

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute CUSTOMER | + | str | Matches code | inferred; default='CUSTOMER' |
| Attribute KITCHEN_STAFF | + | str | Matches code | inferred; default='KITCHEN_STAFF' |
| Attribute SHIPPER | + | str | Matches code | inferred; default='SHIPPER' |
| Attribute ADMIN | + | str | Matches code | inferred; default='ADMIN' |
| Attribute MANAGER | + | str | Matches code | inferred; default='MANAGER' |


## DeliveryController

Layer: controller · Stereotype: «controller» · Module: saigonbite/business/controllers/delivery_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute deliveries | + | DeliveryDAO | Matches code | inferred |
| Attribute orders | + | OrderDAO | Matches code | inferred |
| Attribute payments | + | PaymentDAO | Matches code | inferred |
| Attribute hubs | + | HubDAO | Matches code | inferred |
| Attribute customers | + | CustomerDAO | Matches code | inferred |
| Method board | + | board(self, user_id: int) -> ShipperBoard | Matches code | — |
| Method get_delivery | + | get_delivery(self, user_id: int, order_id: int) -> DeliveryView | Matches code | — |
| Method pick_up | + | pick_up(self, user_id: int, order_id: int) -> DeliveryView | P4 scoped evidence (P4.1 + P4.5, P4.4 / P4.5; resolution rows 22, 23, 24) | P4 input: P2-S13; P3-S03; Guarded writes must check rowcount and handle busy / commit failure without partial effects; shared helper is currently incomplete. |
| Method confirm_delivered | + | confirm_delivered(self, user_id: int, order_id: int, cash_collected: Optional[str]) -> DeliveryView | P4 scoped evidence (P4.1 + P4.5, P4.4 / P4.5; resolution rows 22, 23, 24) | P4 input: P2-S13; P3-S03; Guarded writes must check rowcount and handle busy / commit failure without partial effects; shared helper is currently incomplete. |
| Method report_failure | + | report_failure(self, user_id: int, order_id: int, reason: str) -> DeliveryView | P4 scoped evidence (P4.1 + P4.5, P4.4 / P4.5; resolution rows 22, 23, 24) | P4 input: F-02; P2-S13; BR-17 full C refund owed and atomic state/amount writes, including COMMIT rollback. |
| Method _require_shipper | - | _require_shipper(self, user_id: int) -> UserAccount | Matches code | — |
| Method _delivery | - | _delivery(self, order_id: int) -> Delivery | Matches code | — |
| Method _own_active_delivery | - | _own_active_delivery(self, shipper: UserAccount, order_id: int) -> Delivery | Matches code | — |
| Method _parse_cash | - | _parse_cash(raw: Optional[str]) -> Optional[int] | Matches code | — |
| Method _view | - | _view(self, delivery: Delivery) -> DeliveryView | Matches code | — |


## BaseController

Layer: controller · Stereotype: «controller» · Module: saigonbite/business/controllers/common.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Attribute clock | + | Any | Matches code | inferred |
| Attribute users | + | UserDAO | Matches code | inferred |
| Method _now | - | _now(self) -> str | Matches code | — |
| Method _require_user | - | _require_user(self, user_id: int, *roles: Role, message: str='Your account cannot do this.') -> UserAccount | Matches code | — |


## controllers.common

Layer: controller · Stereotype: «module» · Module: saigonbite/business/controllers/common.py

Responsibility: Module functions with their original Python signatures.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method move_order | + | move_order(orders: OrderDAO, order: Order, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> None | Matches code | — |
| Method release_payment | + | release_payment(payments: PaymentDAO, order_id: int, now: str) -> Payment | Changed during implementation and tested (P4.4; Table P4-1 rows 54) | P4 input: F-02; P2-S01; P3-S03; Persist full captured C as refund_amount together with state; changing only the domain object does not save the amount. Check conditional save results in the same transaction. |


## DeliveryView

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/delivery_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute delivery | + | Delivery | Matches code | — |
| Attribute order | + | Order | Matches code | — |
| Attribute payment | + | Payment | Matches code | — |
| Attribute hub | + | Hub | Matches code | — |
| Attribute customer | + | Customer | Matches code | — |
| Method cash_to_collect | + | cash_to_collect(self) -> int | Matches code | property |


## ShipperBoard

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/delivery_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute waiting | + | list[DeliveryView] | Matches code | — |
| Attribute mine | + | list[DeliveryView] | Matches code | — |
| Attribute finished | + | list[DeliveryView] | Matches code | — |


## delivery

Layer: view · Stereotype: «view» · Module: saigonbite/presentation/delivery.py

Responsibility: Translate shipper requests and render contact and cash information.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method board | + | board() | Matches code | inferred |
| Method detail | + | detail(order_id: int) | Matches code | inferred |
| Method pick_up | + | pick_up(order_id: int) | Matches code | inferred |
| Method delivered | + | delivered(order_id: int) | Matches code | inferred |
| Method failed | + | failed(order_id: int) | Matches code | inferred |


## DeliveryDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/delivery_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Method get_by_order_id | + | get_by_order_id(self, order_id: int) -> Optional[Delivery] | Matches code | — |
| Method list_awaiting_pickup | + | list_awaiting_pickup(self) -> list[Delivery] | Matches code | — |
| Method list_for_shipper | + | list_for_shipper(self, shipper_id: int, state: DeliveryState) -> list[Delivery] | Matches code | — |
| Method take | + | take(self, order_id: int, shipper_id: int, now: str) -> bool | Matches code | — |
| Method finish | + | finish(self, order_id: int, shipper_id: int, to_state: DeliveryState, now: str, failure_reason: Optional[str]=None, cash_collected: Optional[int]=None) -> bool | Matches code | — |


## OrderDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/order_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Method get_by_id | + | get_by_id(self, order_id: int) -> Optional[Order] | Matches code | — |
| Method change_state | + | change_state(self, order_id: int, from_state: OrderState, to_state: OrderState, now: str, reject_reason: Optional[str]=None) -> bool | Matches code | — |
| Method _load | - | _load(self, row: Optional[sqlite3.Row]) -> Optional[Order] | Matches code | — |


## PaymentDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/payment_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Method get_by_order_id | + | get_by_order_id(self, order_id: int) -> Optional[Payment] | Matches code | — |
| Method change_state | + | change_state(self, order_id: int, from_state: PaymentState, to_state: PaymentState, now: str) -> bool | Matches code | — |
| Method set_amounts | + | set_amounts(self, order_id: int, amount: int, refund_amount: int, now: str) -> bool | Changed during implementation and tested (P4.4; Table P4-1 rows 46, 47, 48, 49, 50) | P4 input: F-02; P3-S03; Persist full/partial refund obligations atomically and expose the conditional save outcome. |


## CustomerDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/customer_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Method get | + | get(self, customer_id: int) -> Optional[Customer] | Matches code | — |


## HubDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/hub_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Method get_including_archived | + | get_including_archived(self, hub_id: int) -> Optional[Hub] | Matches code | — |


## UserDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/user_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Method get_by_id | + | get_by_id(self, user_id: int) -> Optional[UserAccount] | Matches code | — |
