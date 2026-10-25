# UC-03 design classes

Author: 722I0004 · AI-assisted (Codex)

Source: `models/shared/design_model.json`, C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`. Evidence label: Static / target design. This table is a filtered projection; no application module was imported. `Any` and absent annotations are explicitly inferred. Python visibility follows leading underscores; dataclass fields are public. Constructors are implicit dataclass construction, not invented methods.

† design target, not yet in code at C0 (see P4 inputs P2-S13/P2-S14/P2-S15/P3-S02/P3-S03). MATCH means static correspondence, not executed success.

Templates: `admin/hubs.html`, `admin/hub_form.html`, shared `error.html`. The `admin` role is the real Flask blueprint module, not a fictional view class.

Types retained as names from code include `Mapping`, `Optional`, `sqlite3.Connection` and business DTOs. A displayed attribute omitted from a narrow figure remains in this table. Association-backing foreign-key IDs remain below but are suppressed on domain DCDs.

## admin

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

## HubController

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

## HubAdminView

Layer: **controller**; stereotype: **«value»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/hub_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ status: HubStatus` | MATCH |
| Attribute | `+ open_orders: int` | MATCH |
| Operation | `+ can_archive() -> bool` | MATCH; property accessor |

## HubStatus

Layer: **domain**; stereotype: **«entity»**; responsibility: Derive busy, quiet and load percentage from current load and capacity. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hub: Hub` | MATCH |
| Attribute | `+ load: int` | MATCH |
| Operation | `+ busy() -> bool` | MATCH; property accessor |
| Operation | `+ quiet() -> bool` | MATCH; property accessor |
| Operation | `+ load_percent() -> int` | MATCH; property accessor |

## Hub

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

## HubDAO

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

## BaseController

Layer: **controller**; stereotype: **«controller»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/common.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Attribute | `+ clock: Any` | MATCH; inferred |
| Attribute | `+ users: UserDAO` | MATCH; inferred |
| Operation | `- _now() -> str` | MATCH |
| Operation | `- _require_user(user_id: int, *roles: Role, message: str = 'Your account cannot do this.') -> UserAccount` | MATCH |

## UserAccount

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
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ get_by_id(user_id: int) -> Optional[UserAccount]` | MATCH |

## Boundary adapters and guarantees

`uid()` always comes from the active server session; posted identity is never accepted. Form adapters retain SSD names while converting camelCase fields to Python keys: `address` → `address_text`, `baseDeliveryFee` → `base_delivery_fee`, `capacity` → `max_active_orders`; `brandId` → `brand_id`. Optional parameters map omitted values to the target defaults. Availability is validated as a boolean. Request.form values are strings; controllers parse and validate them.

OP-23 is a P3-S02 target with `include_archived: bool = True`; existing C0 route/controller omit that argument. Reads inspect archived hubs. `_parse` validates candidate attributes; `create_hub` / `update_hub` enforce uniqueness; `archive_hub` requires zero open orders. `HubStatus.busy/quiet` are properties derived from load/capacity. `HubAdminView.can_archive` derives from open_orders and archive flag, not a persistent state. Capacity below load is allowed. No restore is proposed.

Mutation success is acknowledged only after commit. The P2-S13/P3-S03 targets require rowcount/guard checks and controlled busy or commit-error rollback; the Section III figures intentionally hide DAO/SQL behind the persistence note and Section 4.3.2. Draft validation maxima/coordinate windows remain draft constraints (P2-S17), not newly locked BRs.

## Guarantee responsibility and transaction boundary

`HubStatus` and `HubAdminView` are transient projections, not additional persistent entities.

| Anchor / request | Named responsibility | Boundary |
|---|---|---|
| UC03-PC01 | HubController._parse + create_hub / update_hub; HubDAO.code_exists and insert / update | BEGIN IMMEDIATE; success only after commit † |
| UC03-PC02 | HubController.archive_hub; HubDAO.open_order_count + archive; read consumers exclude archived hubs operationally but retain history | BEGIN IMMEDIATE; no open orders; conditional-save rowcount and commit-error handling † |
| UC03-MG01 | HubController._require_admin / _parse and mutation guard checks; failed write rolls back; BaseController._require_user rejects inactive or wrong-role identity | All create/update/archive changes are atomic †; list/get are read-only |
| listHubs / getHub | HubController.list_hubs / get_hub returns HubAdminView + derived HubStatus; authorized archived inspection is allowed | Read; zero persistent writes |

† These are design targets where P2-S13/P3-S03 or the operation-specific gap is recorded; no transaction success was executed in P3. The full DAO realization is in Section 4.3.2.

Reviewed adapter status: `admin.hubs` is P4-TARGET † (P3-S02). Existing route symbols alone do not qualify those target behaviors as MATCH.
