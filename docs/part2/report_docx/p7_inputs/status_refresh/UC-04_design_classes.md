# UC-04 Design Classes

Author: 722I0004 · AI-assisted (Codex)

First design commit C0: 45ac762 (24/10/2026). Signatures are compared with the source code; test evidence is in section 5.1.

The tables use the sole shared DCD model at C0. Visibility follows the leading-underscore convention; signatures preserve the AST inventory. * marks an inferred/unannotated type or route signature.  marks a C0 design target (final status in Table P4-1)/C0 design gap (final status in Table P4-1) and does not mean implemented at C0. Domain FK scalar attributes are retained here for mapping but omitted from DCDs in favour of associations.

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


## HubStatus

Layer: domain · Stereotype: «entity» · Module: saigonbite/business/domain/models.py

Responsibility: Derive busy, quiet and load percentage from current load and capacity.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute hub | + | Hub | Matches code | — |
| Attribute load | + | int | Matches code | — |
| Method busy | + | busy(self) -> bool | Matches code | property |
| Method quiet | + | quiet(self) -> bool | Matches code | property |
| Method load_percent | + | load_percent(self) -> int | Matches code | property |


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


## DeliveryState

Layer: domain · Stereotype: «enumeration» · Module: saigonbite/business/domain/enums.py

Responsibility: Hold typed business state and its local rules.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute AWAITING_PICKUP | + | str | Matches code | inferred; default='AWAITING_PICKUP' |
| Attribute PICKED_UP | + | str | Matches code | inferred; default='PICKED_UP' |
| Attribute DELIVERED | + | str | Matches code | inferred; default='DELIVERED' |
| Attribute FAILED | + | str | Matches code | inferred; default='FAILED' |


## ReportController

Layer: controller · Stereotype: «controller» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Authorize Manager requests and construct operational reports without writes.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute reports | + | ReportDAO | Matches code | inferred |
| Attribute hubs | + | HubDAO | Matches code | inferred |
| Method all_hubs | + | all_hubs(self) -> list[Hub] | Matches code | — |
| Method sales_report | + | sales_report(self, user_id: int, date_from: Optional[str]=None, date_to: Optional[str]=None, hub_id: Optional[int]=None) -> SalesReport | Changed during implementation and tested (P4.8; Table P4-1 rows 25, 26) | P4 input: F-03; F-09; Expose T without subtracting refund owed twice; top items retain menu_item_id identity. Carry menu_item_id into SalesReport.top_items and presentation. |
| Method workload_report | + | workload_report(self, user_id: int) -> WorkloadReport | Changed during implementation and tested (P4.8; Table P4-1 rows 25, 26) | P4 input: P2-S18; Use all retained hub identities, including archived hubs with zero open work. |
| Method delivery_report | + | delivery_report(self, user_id: int, date_from: Optional[str]=None, date_to: Optional[str]=None, hub_id: Optional[int]=None) -> DeliveryReport | Matches code | — |
| Method _require_manager | - | _require_manager(self, user_id: int) -> None | Matches code | — |
| Method _hub | - | _hub(self, hub_id: Optional[int]) -> Optional[Hub] | Matches code | — |
| Method _period | - | _period(self, date_from: Optional[str], date_to: Optional[str]) -> Period | Matches code | — |


## BaseController

Layer: controller · Stereotype: «controller» · Module: saigonbite/business/controllers/common.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Attribute clock | + | Any | Matches code | inferred |
| Attribute users | + | UserDAO | Matches code | inferred |
| Method _today_vn | - | _today_vn(self) -> str | Matches code | — |
| Method _require_user | - | _require_user(self, user_id: int, *roles: Role, message: str='Your account cannot do this.') -> UserAccount | Matches code | — |


## controllers.common

Layer: controller · Stereotype: «module» · Module: saigonbite/business/controllers/common.py

Responsibility: Module functions with their original Python signatures.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method vn_day_start_utc | + | vn_day_start_utc(day: date) -> str | Matches code | — |


## controllers.report_controller

Layer: controller · Stereotype: «module» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Module functions with their original Python signatures.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method _minutes | - | _minutes(start: Optional[str], end: Optional[str]) -> Optional[float] | Matches code | — |


## Period

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute date_from | + | str | Matches code | — |
| Attribute date_to | + | str | Matches code | — |
| Attribute start_utc | + | str | Matches code | — |
| Attribute end_utc | + | str | Matches code | — |


## SalesRow

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute label | + | str | Matches code | — |
| Attribute orders | + | int | Matches code | default=0 |
| Attribute item_sales | + | int | Matches code | default=0 |
| Attribute voucher_discounts | + | int | Matches code | default=0 |
| Attribute delivery_fees | + | int | Matches code | default=0 |
| Attribute total | + | int | Matches code | default=0 |
| Attribute refunds_owed | + | int | Matches code | default=0 |
| Method net | + | net(self) -> int | Changed during implementation and tested (P4.8; Table P4-1 rows 27) | property; P4 input: F-03; Return total T; refunds_owed is disclosed separately. |
| Method add | + | add(self, other: 'SalesRow') -> None | Matches code | — |


## SalesReport

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute period | + | Period | Matches code | — |
| Attribute hub | + | Optional[Hub] | Matches code | — |
| Attribute rows | + | list[SalesRow] | Matches code | — |
| Attribute totals | + | SalesRow | Matches code | — |
| Attribute top_items | + | list[tuple[int, str, int, int]] | Changed during implementation and tested (P4.8; Table P4-1 rows 59) | — |


## WorkloadRow

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute status | + | HubStatus | Matches code | — |
| Attribute counts | + | dict[OrderState, int] | Matches code | — |
| Method label | + | label(self) -> str | Matches code | property |


## WorkloadReport

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute as_of | + | str | Matches code | — |
| Attribute rows | + | list[WorkloadRow] | Matches code | — |


## DeliveryRow

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute label | + | str | Matches code | — |
| Attribute delivered | + | int | Matches code | default=0 |
| Attribute failed | + | int | Matches code | default=0 |
| Attribute waits | + | list[float] | Matches code | default=field(default_factory=list) |
| Attribute rides | + | list[float] | Matches code | default=field(default_factory=list) |
| Method failure_rate | + | failure_rate(self) -> Optional[float] | Matches code | property |
| Method avg_wait | + | avg_wait(self) -> Optional[float] | Matches code | property |
| Method avg_ride | + | avg_ride(self) -> Optional[float] | Matches code | property |


## DeliveryReport

Layer: controller · Stereotype: «value» · Module: saigonbite/business/controllers/report_controller.py

Responsibility: Coordinate authorization, domain decisions and data access.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute period | + | Period | Matches code | — |
| Attribute hub | + | Optional[Hub] | Matches code | — |
| Attribute by_hub | + | list[DeliveryRow] | Matches code | — |
| Attribute by_shipper | + | list[DeliveryRow] | Matches code | — |
| Attribute overall | + | DeliveryRow | Matches code | — |


## reports

Layer: view · Stereotype: «view» · Module: saigonbite/presentation/reports.py

Responsibility: Translate Manager filters and render read-only report results.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Method _filtered | - | _filtered(template: str, run) | Matches code | inferred |
| Method sales | + | sales() | Changed during implementation and tested (P4.8; Table P4-1 rows 66) | inferred; P4 input: F-09; Render the new identity-preserving top-items shape; template unpacking must retain the item identity. |
| Method workload | + | workload() | Matches code | inferred |
| Method delivery | + | delivery() | Matches code | inferred |


## ReportDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/report_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Method sales_by_hub | + | sales_by_hub(self, start_utc: str, end_utc: str, hub_id: Optional[int]) -> list[sqlite3.Row] | Matches code | — |
| Method top_items | + | top_items(self, start_utc: str, end_utc: str, hub_id: Optional[int], limit: int=10) -> list[sqlite3.Row] | Changed during implementation and tested (P4.8; Table P4-1 rows 58) | P4 input: F-09; Select and group by menu_item_id; snapshot name is a label, never the grouping identity. |
| Method open_orders_by_hub_and_state | + | open_orders_by_hub_and_state(self) -> list[sqlite3.Row] | Matches code | — |
| Method finished_deliveries | + | finished_deliveries(self, start_utc: str, end_utc: str, hub_id: Optional[int]) -> list[sqlite3.Row] | Matches code | — |


## HubDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/hub_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Method list_active | + | list_active(self) -> list[Hub] | Matches code | — |
| Method list_all | + | list_all(self) -> list[Hub] | Matches code | — |
| Method get_including_archived | + | get_including_archived(self, hub_id: int) -> Optional[Hub] | Matches code | — |


## UserDAO

Layer: data_access · Stereotype: «DAO» · Module: saigonbite/data_access/user_dao.py

Responsibility: Read or write parameterized records.

| Element | Visibility | Type / full signature | Status | Notes |
|---|---|---|---|---|
| Attribute conn | + | sqlite3.Connection | Matches code | — |
| Method get_by_id | + | get_by_id(self, user_id: int) -> Optional[UserAccount] | Matches code | — |

## F-09 identity and presentation target

ReportDAO.top_items retains menu_item_id in grouping and read rows. SalesReport.top_items carries list[tuple[int, str, int, int]] (item ID, snapshot name, quantity, revenue). reports.sales and its template preserve that identity when rendering; these three elements are C0 design target (final status in Table P4-1) under F-09 / P4.8. No target behavior is claimed executed.
