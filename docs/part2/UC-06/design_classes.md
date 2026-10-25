# UC-06 design classes

Author: 722I0004 · AI-assisted (Codex)

Source: `models/shared/design_model.json`, C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`. Evidence label: Static / target design. This table is a filtered projection; no application module was imported. `Any` and absent annotations are explicitly inferred. Python visibility follows leading underscores; dataclass fields are public. Constructors are implicit dataclass construction, not invented methods.

† design target, not yet in code at C0 (see P4 inputs P2-S13/P2-S14/P2-S15/P3-S02/P3-S03). MATCH means static correspondence, not executed success.

Templates: `admin/catalogue.html`, `admin/item_form.html`, `admin/hub_menu.html`, shared `error.html`. The `admin` role is the real Flask blueprint module, not a fictional view class.

Types retained as names from code include `Mapping`, `Optional`, `sqlite3.Connection` and business DTOs. A displayed attribute omitted from a narrow figure remains in this table. Association-backing foreign-key IDs remain below but are suppressed on domain DCDs.

## admin

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

## MenuController

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

## Catalogue

Layer: **controller**; stereotype: **«value»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/menu_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ brands: list[Brand]` | MATCH |
| Attribute | `+ items: list[MenuItem]` | MATCH |

## HubMenu

Layer: **controller**; stereotype: **«value»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/menu_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hub: Hub` | MATCH |
| Attribute | `+ listed: list[HubMenuItem]` | MATCH |
| Attribute | `+ not_listed: list[MenuItem]` | MATCH |

## HubController

Layer: **controller**; stereotype: **«controller»**; responsibility: Coordinate authorization, domain decisions and data access. Source: `saigonbite/business/controllers/hub_controller.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hubs: HubDAO` | MATCH; inferred |
| Operation | `+ list_hubs(user_id: int, include_archived: bool = True) -> list[HubAdminView] †` | P4-TARGET †; P3-S02 |

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

## Brand

Layer: **domain**; stereotype: **«entity»**; responsibility: Group menu items and retain the archived brand identity. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ id: int` | MATCH |
| Attribute | `+ name: str` | MATCH |
| Attribute | `+ archived_at: Optional[str]` | MATCH |

## MenuItem

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

## HubMenuItem

Layer: **domain**; stereotype: **«entity»**; responsibility: Represent one hub listing and its independent availability. Source: `saigonbite/business/domain/models.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ hub_id: int` | MATCH; association backing ID, omitted on DCD |
| Attribute | `+ item: MenuItem` | MATCH |
| Attribute | `+ is_available: bool` | MATCH |

## MenuDAO

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

## HubDAO

Layer: **data_access**; stereotype: **«DAO»**; responsibility: Read or write parameterized records. Source: `saigonbite/data_access/hub_dao.py`.

| Element | Typed declaration | Status / qualification |
|---|---|---|
| Attribute | `+ conn: sqlite3.Connection` | MATCH |
| Operation | `+ list_all() -> list[Hub]` | MATCH |
| Operation | `+ get_including_archived(hub_id: int) -> Optional[Hub]` | MATCH |

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

OP-25 is the GAP `list_catalogue` wrapper, composing `catalogue`, the retained-hub read and optional `hub_menu`; it returns Brand/MenuItem/Hub/HubMenuItem data without adding another SSD operation. The three SSD occurrences remain distinct. OP-43 passes initial `available` into `list_item_at_hub` and `MenuDAO.add_listing` in the same insert (P2-S15). OP-41 uses `brandId` only as current-parent context; `update_item` pins `current.brand_id`, with no reparent/restore. Snapshot OrderLine data is outside every catalogue mutation. A None controller result for listing commands is adapted to a successful acknowledgement called `savedRecord` at the SSD boundary.

Mutation success is acknowledged only after commit. The P2-S13/P3-S03 targets require rowcount/guard checks and controlled busy or commit-error rollback; the Section III figures intentionally hide DAO/SQL behind the persistence note and Section 4.3.2. Draft validation maxima/coordinate windows remain draft constraints (P2-S17), not newly locked BRs.

## Guarantee responsibility and transaction boundary

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
