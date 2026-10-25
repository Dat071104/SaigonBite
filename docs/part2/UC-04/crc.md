# UC-04 CRC Cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators are real classes/modules linked by the AST-derived shared model (calls or typed attributes); target-only collaborators are identified as P4 targets. Blueprints and helpers remain real modules. No communication diagram is added.

## Hub — domain / «entity»

**Knows:** id: int, code: str, name: str, address_text: str, latitude: float, longitude: float, max_active_orders: int, base_delivery_fee: int, archived_at: Optional[str]
**Does:** Represent a kitchen location, capacity and fee.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

## HubStatus — domain / «entity»

**Knows:** hub: Hub, load: int
**Does:** Derive busy, quiet and load percentage from current load and capacity.; operations: busy, quiet, load_percent
**Collaborators:** Hub

## OrderState — domain / «enumeration»

**Knows:** PLACED: str, CONFIRMED: str, REJECTED: str, PREPARING: str, READY: str, OUT_FOR_DELIVERY: str, DELIVERED: str, DELIVERY_FAILED: str, CANCELLED: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

## DeliveryState — domain / «enumeration»

**Knows:** AWAITING_PICKUP: str, PICKED_UP: str, DELIVERED: str, FAILED: str
**Does:** Hold typed business state and its local rules.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

## ReportController — controller / «controller»

**Knows:** reports: ReportDAO, hubs: HubDAO
**Does:** Authorize Manager requests and construct operational reports without writes.; operations: all_hubs, sales_report †, workload_report †, delivery_report, _require_manager, _hub, _period
**Collaborators:** DeliveryReport, DeliveryRow, Hub, HubDAO, HubStatus, OrderState, Period, ReportDAO, SalesReport, SalesRow, WorkloadReport, WorkloadRow, controllers.common, controllers.report_controller

## BaseController — controller / «controller»

**Knows:** conn: sqlite3.Connection, clock: Any, users: UserDAO
**Does:** Coordinate authorization, domain decisions and data access.; operations: _today_vn, _require_user
**Collaborators:** UserDAO

## controllers.common — controller / «module»

**Knows:** No instance attributes in the shared model.
**Does:** Module functions with their original Python signatures.; operations: vn_day_start_utc
**Collaborators:** OrderState

## controllers.report_controller — controller / «module»

**Knows:** No instance attributes in the shared model.
**Does:** Module functions with their original Python signatures.; operations: _minutes
**Collaborators:** None recorded in this UC view.

## Period — controller / «value»

**Knows:** date_from: str, date_to: str, start_utc: str, end_utc: str
**Does:** Coordinate authorization, domain decisions and data access.; operations: value/module role only.
**Collaborators:** None recorded in this UC view.

## SalesRow — controller / «value»

**Knows:** label: str, orders: int, item_sales: int, voucher_discounts: int, delivery_fees: int, total: int, refunds_owed: int
**Does:** Coordinate authorization, domain decisions and data access.; operations: net †, add
**Collaborators:** None recorded in this UC view.

## SalesReport — controller / «value»

**Knows:** period: Period, hub: Optional[Hub], rows: list[SalesRow], totals: SalesRow, top_items: list[tuple[int, str, int, int]]
**Does:** Coordinate authorization, domain decisions and data access.; operations: value/module role only.
**Collaborators:** Hub, Period, SalesRow

## WorkloadRow — controller / «value»

**Knows:** status: HubStatus, counts: dict[OrderState, int]
**Does:** Coordinate authorization, domain decisions and data access.; operations: label
**Collaborators:** HubStatus, OrderState

## WorkloadReport — controller / «value»

**Knows:** as_of: str, rows: list[WorkloadRow]
**Does:** Coordinate authorization, domain decisions and data access.; operations: value/module role only.
**Collaborators:** WorkloadRow

## DeliveryRow — controller / «value»

**Knows:** label: str, delivered: int, failed: int, waits: list[float], rides: list[float]
**Does:** Coordinate authorization, domain decisions and data access.; operations: failure_rate, avg_wait, avg_ride
**Collaborators:** None recorded in this UC view.

## DeliveryReport — controller / «value»

**Knows:** period: Period, hub: Optional[Hub], by_hub: list[DeliveryRow], by_shipper: list[DeliveryRow], overall: DeliveryRow
**Does:** Coordinate authorization, domain decisions and data access.; operations: value/module role only.
**Collaborators:** DeliveryRow, Hub, Period

## reports — view / «view»

**Knows:** No instance attributes in the shared model.
**Does:** Translate Manager filters and render read-only report results.; operations: _filtered, sales †, workload, delivery
**Collaborators:** ReportController

## ReportDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: sales_by_hub, top_items †, open_orders_by_hub_and_state, finished_deliveries
**Collaborators:** None recorded in this UC view.

## HubDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: list_active, list_all, get_including_archived
**Collaborators:** Hub

## UserDAO — data_access / «DAO»

**Knows:** conn: sqlite3.Connection
**Does:** Read or write parameterized records.; operations: get_by_id
**Collaborators:** None recorded in this UC view.

## Persistence boundary

Period, SalesRow, SalesReport, WorkloadRow, WorkloadReport, DeliveryRow and DeliveryReport are in-memory controller-module values. Filters, report rows, sample counts and returned reports are not persisted; UC-04 has no Report entity or lifecycle. HubStatus is the actual domain value role.

## Architecture correspondence

Actual DAO imports of domain values remain static couplings in these CRC collaborators; they are an upward-dependency P4.9 finding documented in section 4.2, and are not drawn as permitted dependencies in the layered DCD.
