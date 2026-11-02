# UC-03 design classes

Author: 722I0004 · AI-assisted (Codex)

Source: `models/shared/design_model.json`, C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`. Evidence label: Static / target design. This table is a filtered projection; no application module was imported. `Any` and absent annotations are explicitly inferred. Python visibility follows leading underscores; dataclass fields are public. Constructors are implicit dataclass construction, not invented methods.

 design target, not yet in code at C0 (see P4 inputs P2-S13/P2-S14/P2-S15/P3-S02/P3-S03). MATCH means static correspondence, not executed success.

Templates: `admin/hubs.html`, `admin/hub_form.html`, shared `error.html`. The `admin` role is the real Flask blueprint module, not a fictional view class.

Types retained as names from code include `Mapping`, `Optional`, `sqlite3.Connection` and business DTOs. A displayed attribute omitted from a narrow figure remains in this table. Association-backing foreign-key IDs remain below but are suppressed on domain DCDs.

## admin

Layer: **view**; stereotype: **«view»**; responsibility: Translate administrator maintenance routes; never provide business decisions. Source: `saigonbite/presentation/admin.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Operation | `- _hubs() -> HubController` | Matches code |
| Operation | `+ hubs() -> Any [inferred] ` | Changed during implementation and tested (P4.2; Table P4-1 rows 62); Reason: ; inferred annotation(s); P3-S02 |
| Operation | `+ new_hub() -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ edit_hub(hub_id: int) -> Any [inferred]` | MATCH; inferred annotation(s) |
| Operation | `+ archive_hub(hub_id: int) -> Any [inferred]` | MATCH; inferred annotation(s) |

Route adapters (AST):
- `GET /admin/` → view function `admin.hubs`
- `GET /admin/hubs` → view function `admin.hubs`
- `GET/POST /admin/hubs/new` → view function `admin.new_hub`
- `GET/POST /admin/hubs/<int:hub_id>` → view function `admin.edit_hub`
- `POST /admin/hubs/<int:hub_id>/archive` → view function `admin.archive_hub`
## HubController

Layer: **controller**; stereotype: **«controller»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/hub_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hubs: HubDAO` | MATCH; inferred |
| Operation | `+ list_hubs(user_id: int, include_archived: bool = True) -> list[HubAdminView] ` | Changed during implementation and tested (P4.2; Table P4-1 rows 28); Reason: ; P3-S02 |
| Operation | `+ get_hub(user_id: int, hub_id: int) -> HubAdminView` | Matches code |
| Operation | `+ create_hub(user_id: int, form: Mapping[str, str]) -> Hub ` | P4 scoped evidence (P4.1 + P4.2; resolution rows 29); Reason: ; P2-S13; P3-S03 |
| Operation | `+ update_hub(user_id: int, hub_id: int, form: Mapping[str, str]) -> Hub ` | P4 scoped evidence (P4.1 + P4.2; resolution rows 30); Reason: ; P2-S13; P3-S03 |
| Operation | `+ archive_hub(user_id: int, hub_id: int) -> Hub ` | P4 scoped evidence (P4.1 + P4.2; resolution rows 31); Reason: ; P2-S13; P3-S03 |
| Operation | `- _require_admin(user_id: int) -> None` | Matches code |
| Operation | `- _parse(form: Mapping[str, str], hub_id: Any) -> Hub [inferred]` | MATCH; inferred annotation(s) |

## HubAdminView

Layer: **controller**; stereotype: **«value»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/hub_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ status: HubStatus` | Matches code |
| Attribute | `+ open_orders: int` | Matches code |
| Operation | `+ can_archive() -> bool` | MATCH; property accessor |

## HubStatus

Layer: **domain**; stereotype: **«entity»**; responsibility: Derive busy, quiet and load percentage from current load and capacity. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hub: Hub` | Matches code |
| Attribute | `+ load: int` | Matches code |
| Operation | `+ busy() -> bool` | MATCH; property accessor |
| Operation | `+ quiet() -> bool` | MATCH; property accessor |
| Operation | `+ load_percent() -> int` | MATCH; property accessor |

## Hub

Layer: **domain**; stereotype: **«entity»**; responsibility: Represent a kitchen location, capacity and fee. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
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

## HubDAO

Layer: **data_access**; stereotype: **«DAO»**; responsibility: Read or write parameterized records. Source: `saigonbite/data_access/hub_dao.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Operation | `+ list_active() -> list[Hub]` | Matches code |
| Operation | `+ list_all() -> list[Hub]` | Matches code |
| Operation | `+ get_including_archived(hub_id: int) -> Optional[Hub]` | Matches code |
| Operation | `+ code_exists(code: str, except_id: Optional[int] = None) -> bool` | Matches code |
| Operation | `+ insert(hub: Hub) -> int` | Matches code |
| Operation | `+ update(hub: Hub) -> bool` | Matches code |
| Operation | `+ archive(hub_id: int, now: str) -> bool` | Matches code |
| Operation | `+ active_load(hub_id: int) -> int` | Matches code |
| Operation | `+ active_loads() -> dict[int, int]` | Matches code |
| Operation | `+ open_order_count(hub_id: int) -> int` | Matches code |

## BaseController

Layer: **controller**; stereotype: **«controller»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/common.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Attribute | `+ clock: Any` | MATCH; inferred |
| Attribute | `+ users: UserDAO` | MATCH; inferred |
| Operation | `- _now() -> str` | Matches code |
| Operation | `- _require_user(user_id: int, *roles: Role, message: str = 'Your account cannot do this.') -> UserAccount` | Matches code |

## UserAccount

Layer: **domain**; stereotype: **«entity»**; responsibility: Hold account identity, role, active flag and optional kitchen-hub assignment. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ id: int` | Matches code |
| Attribute | `+ username: str` | Matches code |
| Attribute | `+ password_hash: str` | Matches code |
| Attribute | `+ display_name: str` | Matches code |
| Attribute | `+ role: Role` | Matches code |
| Attribute | `+ is_active: bool` | Matches code |
| Attribute | `+ hub_id: Optional[int]` | MATCH; association backing ID, omitted on DCD |
| Attribute | `+ created_at: str` | Changed during implementation and tested (P4.1; Table P4-1 rows 53); Reason:  |

## Role

Layer: **domain**; stereotype: **«enumeration»**; responsibility: Hold typed business state and its local rules. Source: `saigonbite/business/domain/enums.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ CUSTOMER: str` | MATCH; inferred |
| Attribute | `+ KITCHEN_STAFF: str` | MATCH; inferred |
| Attribute | `+ SHIPPER: str` | MATCH; inferred |
| Attribute | `+ ADMIN: str` | MATCH; inferred |
| Attribute | `+ MANAGER: str` | MATCH; inferred |

## UserDAO

Layer: **data_access**; stereotype: **«DAO»**; responsibility: Read or write parameterized records. Source: `saigonbite/data_access/user_dao.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | Matches code |
| Operation | `+ get_by_id(user_id: int) -> Optional[UserAccount]` | Matches code |

## Boundary adapters and guarantees

`uid()` always comes from the active server session; posted identity is never accepted. Form adapters retain SSD names while converting camelCase fields to Python keys: `address` → `address_text`, `baseDeliveryFee` → `base_delivery_fee`, `capacity` → `max_active_orders`; `brandId` → `brand_id`. Optional parameters map omitted values to the target defaults. Availability is validated as a boolean. Request.form values are strings; controllers parse and validate them.

OP-23 is a P3-S02 target with `include_archived: bool = True`; existing C0 route/controller omit that argument. Reads inspect archived hubs. `_parse` validates candidate attributes; `create_hub` / `update_hub` enforce uniqueness; `archive_hub` requires zero open orders. `HubStatus.busy/quiet` are properties derived from load/capacity. `HubAdminView.can_archive` derives from open_orders and archive flag, not a persistent state. Capacity below load is allowed. No restore is proposed.

Mutation success is acknowledged only after commit. The P2-S13/P3-S03 targets require rowcount/guard checks and controlled busy or commit-error rollback; the Section III figures intentionally hide DAO/SQL behind the persistence note and Section 4.3.2. Draft validation maxima/coordinate windows remain draft constraints (P2-S17), not newly locked BRs.

## Guarantee responsibility and transaction boundary

`HubStatus` and `HubAdminView` are transient projections, not additional persistent entities.

| Anchor / request | Named responsibility | Boundary |
|---|---|---|
| UC03-PC01 | HubController._parse + create_hub / update_hub; HubDAO.code_exists and insert / update | BEGIN IMMEDIATE; success only after commit  |
| UC03-PC02 | HubController.archive_hub; HubDAO.open_order_count + archive; read consumers exclude archived hubs operationally but retain history | BEGIN IMMEDIATE; no open orders; conditional-save rowcount and commit-error handling  |
| UC03-MG01 | HubController._require_admin / _parse and mutation guard checks; failed write rolls back; BaseController._require_user rejects inactive or wrong-role identity | All create/update/archive changes are atomic ; list/get are read-only |
| listHubs / getHub | HubController.list_hubs / get_hub returns HubAdminView + derived HubStatus; authorized archived inspection is allowed | Read; zero persistent writes |

 These are design targets where P2-S13/P3-S03 or the operation-specific gap is recorded; no transaction success was executed in P3. The full DAO realization is in Section 4.3.2.

Reviewed adapter status: `admin.hubs` is C0 design target (final status in Table P4-1)  (P3-S02). Existing route symbols alone do not qualify those target behaviors as MATCH.
