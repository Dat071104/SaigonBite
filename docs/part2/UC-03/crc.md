# UC-03 CRC cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators are actual AST call/typed-field targets or the marked OP-25 / OP-43 targets. Inherited authorization collaborators are explicit. Self-calls remain the same class, not another fictional object.

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| `admin` | Knows: request context. Does: hubs, new_hub, edit_hub, archive_hub, _hubs. | HubController |
| `HubController` | Knows: hubs. Does: list_hubs, get_hub, create_hub, update_hub, archive_hub, _require_admin, _parse. | BaseController, ConflictError, Hub, HubAdminView, HubDAO, HubStatus, NotFoundError, ValidationError, admin |
| `HubAdminView` | Knows: status, open_orders. Does: can_archive. | HubController, HubStatus |
| `HubStatus` | Knows: hub, load. Does: busy, quiet, load_percent. | Hub, HubAdminView, HubController |
| `Hub` | Knows: id, code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee, archived_at. Does: holds typed state; no invented update/archive behavior. | HubController, HubDAO, HubStatus |
| `HubDAO` | Knows: conn. Does: list_all, list_active, get_including_archived, code_exists, insert, update, archive, active_load, active_loads, open_order_count. | Hub, HubController |
| `BaseController` | Knows: conn, clock, users. Does: _require_user, _now. | AuthorizationError, UserDAO |
| `UserAccount` | Knows: id, username, password_hash, display_name, role, is_active, hub_id, created_at. Does: holds typed state; no invented update/archive behavior. | Role |
| `Role` | Knows: CUSTOMER, KITCHEN_STAFF, SHIPPER, ADMIN, MANAGER. Does: holds typed state; no invented update/archive behavior. | UserAccount |
| `UserDAO` | Knows: conn. Does: get_by_id. | BaseController |

The existing admin.hubs route is a behavioral target † for forwarding includeArchived (P3-S02). Its current Python symbol is not evidence that the target filter behavior is already MATCH.
