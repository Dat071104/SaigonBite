# UC-04 Design Classes

Author: 722I0004 · AI-assisted (Codex)

C0: 45ac76221b0a103174c7c01d17577e6e49cfd665 · Evidence: Static source correspondence only; this is not runtime or test evidence.

The tables use the sole shared DCD model at C0. Visibility follows the leading-underscore convention; signatures preserve the AST inventory. * marks an inferred/unannotated type or route signature. † marks a P4-TARGET/GAP and does not mean implemented at C0. Domain FK scalar attributes are retained here for mapping but omitted from DCDs in favour of associations.

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


## HubStatus

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Derive busy, quiet and load percentage from current load and capacity.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute hub | + | Hub | MATCH | — |
| Attribute load | + | int | MATCH | — |
| Method busy | + | busy(self) -> bool | MATCH | property |
| Method quiet | + | quiet(self) -> bool | MATCH | property |
| Method load_percent | + | load_percent(self) -> int | MATCH | property |


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


## DeliveryState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute AWAITING_PICKUP | + | str | MATCH | inferred; default='AWAITING_PICKUP' |
| Attribute PICKED_UP | + | str | MATCH | inferred; default='PICKED_UP' |
| Attribute DELIVERED | + | str | MATCH | inferred; default='DELIVERED' |
| Attribute FAILED | + | str | MATCH | inferred; default='FAILED' |


## ReportController

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


## BaseController

Layer: controller · Stereotype: «controller» · Module: saigonbite/business/controllers/common.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Attribute clock | + | Any | MATCH | inferred |
| Attribute users | + | UserDAO | MATCH | inferred |
| Method _today_vn | - | _today_vn(self) -> str | MATCH | — |
| Method _require_user | - | _require_user(self, user_id: int, *roles: Role, message: str='Your account cannot do this.') -> UserAccount | MATCH | — |


## controllers.common

Layer: controller · Stereotype: «module» · Module: saigonbite/business/controllers/common.py

Responsibility: Module functions with their original Python signatures.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method vn_day_start_utc | + | vn_day_start_utc(day: date) -> str | MATCH | — |


## controllers.report_controller

Layer: controller · Stereotype: «module» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Module functions with their original Python signatures.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method _minutes | - | _minutes(start: Optional[str], end: Optional[str]) -> Optional[float] | MATCH | — |


## Period

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute date_from | + | str | MATCH | — |
| Attribute date_to | + | str | MATCH | — |
| Attribute start_utc | + | str | MATCH | — |
| Attribute end_utc | + | str | MATCH | — |


## SalesRow

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


## SalesReport

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute period | + | Period | MATCH | — |
| Attribute hub | + | Optional[Hub] | MATCH | — |
| Attribute rows | + | list[SalesRow] | MATCH | — |
| Attribute totals | + | SalesRow | MATCH | — |
| Attribute top_items | + | list[tuple[int, str, int, int]] | P4-TARGET | — |


## WorkloadRow

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute status | + | HubStatus | MATCH | — |
| Attribute counts | + | dict[OrderState, int] | MATCH | — |
| Method label | + | label(self) -> str | MATCH | property |


## WorkloadReport

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute as_of | + | str | MATCH | — |
| Attribute rows | + | list[WorkloadRow] | MATCH | — |


## DeliveryRow

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


## DeliveryReport

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute period | + | Period | MATCH | — |
| Attribute hub | + | Optional[Hub] | MATCH | — |
| Attribute by_hub | + | list[DeliveryRow] | MATCH | — |
| Attribute by_shipper | + | list[DeliveryRow] | MATCH | — |
| Attribute overall | + | DeliveryRow | MATCH | — |


## reports

Layer: view · Stereotype: «view» · Module: saigonbite/presentation/reports.py

Responsibility: Translate Manager filters and render read-only report results.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method _filtered | - | _filtered(template: str, run) | MATCH | inferred |
| Method sales | + | sales() | P4-TARGET | inferred; P4 input: F-09; Render the new identity-preserving top-items shape; template unpacking must retain the item identity. |
| Method workload | + | workload() | MATCH | inferred |
| Method delivery | + | delivery() | MATCH | inferred |


## ReportDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/report_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method sales_by_hub | + | sales_by_hub(self, start_utc: str, end_utc: str, hub_id: Optional[int]) -> list[sqlite3.Row] | MATCH | — |
| Method top_items | + | top_items(self, start_utc: str, end_utc: str, hub_id: Optional[int], limit: int=10) -> list[sqlite3.Row] | P4-TARGET | P4 input: F-09; Select and group by menu_item_id; snapshot name is a label, never the grouping identity. |
| Method open_orders_by_hub_and_state | + | open_orders_by_hub_and_state(self) -> list[sqlite3.Row] | MATCH | — |
| Method finished_deliveries | + | finished_deliveries(self, start_utc: str, end_utc: str, hub_id: Optional[int]) -> list[sqlite3.Row] | MATCH | — |


## HubDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/hub_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method list_active | + | list_active(self) -> list[Hub] | MATCH | — |
| Method list_all | + | list_all(self) -> list[Hub] | MATCH | — |
| Method get_including_archived | + | get_including_archived(self, hub_id: int) -> Optional[Hub] | MATCH | — |


## UserDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/user_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | MATCH | — |
| Method get_by_id | + | get_by_id(self, user_id: int) -> Optional[UserAccount] | MATCH | — |

## F-09 identity and presentation target

ReportDAO.top_items retains menu_item_id in grouping and read rows. SalesReport.top_items carries list[tuple[int, str, int, int]] (item ID, snapshot name, quantity, revenue). reports.sales and its template preserve that identity when rendering; these three elements are P4-TARGET under F-09 / P4.8. No target behavior is claimed executed.
