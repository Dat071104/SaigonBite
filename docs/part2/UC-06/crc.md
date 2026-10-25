# UC-06 CRC cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators are actual AST call/typed-field targets or the marked OP-25 / OP-43 targets. Inherited authorization collaborators are explicit. Self-calls remain the same class, not another fictional object.

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| `admin` | Knows: request context. Does: catalogue, create_brand, rename_brand, archive_brand, new_item, edit_item, archive_item, hub_menu, list_item, unlist_item, hub_item_availability, _menu, _hubs. | HubController, MenuController |
| `MenuController` | Knows: menu, hubs. Does: catalogue, hub_menu, list_catalogue, create_brand, rename_brand, archive_brand, create_item, update_item, archive_item, list_item_at_hub, unlist_item_at_hub, set_availability, _require_admin, _hub, _active_brand, _active_item, _name, _parse_item. | BaseController, Brand, Catalogue, ConflictError, HubDAO, HubMenu, MenuDAO, MenuItem, NotFoundError, ValidationError, admin; HubMenuItem (logical responsibility via MenuDAO, no direct dataclass method call; OP-25/OP-43 targets † included) |
| `Catalogue` | Knows: brands, items. Does: holds typed state; no invented update/archive behavior. | Brand, MenuController, MenuItem |
| `HubMenu` | Knows: hub, listed, not_listed. Does: holds typed state; no invented update/archive behavior. | Hub, HubMenuItem, MenuController, MenuItem |
| `HubController` | Knows: hubs. Does: list_hubs. | BaseController, Hub, HubAdminView, HubDAO, HubStatus, admin |
| `Hub` | Knows: id, code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee, archived_at. Does: holds typed state; no invented update/archive behavior. | HubController, HubDAO, HubMenu |
| `Brand` | Knows: id, name, archived_at. Does: holds typed state; no invented update/archive behavior. | Catalogue, MenuController, MenuDAO |
| `MenuItem` | Knows: id, brand_id, brand_name, name, description, price, archived_at. Does: holds typed state; no invented update/archive behavior. | Catalogue, HubDAO, HubMenu, HubMenuItem, MenuController, MenuDAO |
| `HubMenuItem` | Knows: hub_id, item, is_available. Does: holds typed state; no invented update/archive behavior. | HubDAO, HubMenu, MenuDAO, MenuItem; MenuController (logical responsibility mediated by MenuDAO) |
| `MenuDAO` | Knows: conn. Does: list_brands, get_brand, brand_name_exists, insert_brand, rename_brand, archive_brand, list_items, get_item, item_name_exists, insert_item, update_item, archive_item, list_hub_items, is_listed, add_listing, remove_listing, set_available. | Brand, HubMenuItem, MenuController, MenuItem |
| `HubDAO` | Knows: conn. Does: list_all, get_including_archived. | Hub, HubController, MenuController |
| `BaseController` | Knows: conn, clock, users. Does: _require_user, _now. | AuthorizationError, UserDAO |
| `UserAccount` | Knows: id, username, password_hash, display_name, role, is_active, hub_id, created_at. Does: holds typed state; no invented update/archive behavior. | Role |
| `Role` | Knows: CUSTOMER, KITCHEN_STAFF, SHIPPER, ADMIN, MANAGER. Does: holds typed state; no invented update/archive behavior. | UserAccount |
| `UserDAO` | Knows: conn. Does: get_by_id. | BaseController |

HubMenuItem is the shared-model association class of Hub and MenuItem. Its independent is_available belongs to one pair. The approved logical MenuController collaborator is deliberately distinguished from a direct Python call target.

The existing admin route functions catalogue/hub_menu/list_item remain marked behavioral targets for the wrapper/initial-availability adapters (P2-S14/P2-S15); symbol existence does not clear those obligations.
