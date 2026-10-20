> AI-assisted (Claude); reviewed and corrected by the team in October 2026.

# CRUD inventory v1 (Iteration 1)

Table names are those of `db/schema.sql`. "Built in I1" lists what the code does today;
the "Planned" columns follow the team plan (section 3.4) and the open lecturer question on CRUD coverage.

| Class | Table | Create | Read | Update | Delete / archive | Built in I1 |
|---|---|---|---|---|---|---|
| Hub | `hub` | UC-03 (I2) | UC-01 (`HubDAO.list_active`, `HubDAO.get`), UC-03, UC-04 | UC-03 (I2) | UC-03 archive with guard "no active orders" (`archived_at`, I2) | Read only |
| Order | `orders` | UC-01 (`OrderDAO.insert`) | UC-01 confirmation (`OrderDAO.get_by_id`, `OrderDAO.get_by_token`), UC-02, UC-04 | UC-05, kitchen board, UC-02, Cancel order (state change only) | Archive old orders (`archived_at`, analysed) | Create, read |
| OrderLine | `order_line` | UC-01 (`OrderDAO.insert`) | UC-01, UC-04 | Edit order (analysed) | Follows Order | Create, read |
| Payment | `payment` | UC-01 (`PaymentDAO.insert`, COD / `PENDING`) | UC-01 confirmation, UC-04 | UC-02 (`PAID`), reject and failure rules (`VOIDED`, `REFUND_PENDING`) | Follows Order | Create, read |
| Customer (`LocalCustomer`, `TouristCustomer`) | `customer` | Register customer (analysed) | UC-01 (`CustomerDAO.get_by_user_id`) | Register customer | Deactivate (analysed) | Seed + read |
| Address | `address` | Register customer (analysed) | UC-01 (`CustomerDAO.list_addresses`, `CustomerDAO.get_address`) | Register customer | Register customer | Seed + read |
| Brand | `brand` | Manage brands and menu items (analysed) | UC-01 (join in `HubDAO.list_menu`) | Manage brands and menu items | Archive (analysed) | Seed + read |
| MenuItem | `menu_item` | Manage brands and menu items (analysed) | UC-01 (`HubDAO.list_menu`, `HubDAO.get_available_item`) | Manage brands and menu items | Archive (analysed) | Seed + read |
| HubMenuItem | `hub_menu_item` | Manage menu availability (analysed) | UC-01 (`HubDAO.list_menu`, `HubDAO.get_available_item`) | Manage menu availability | Manage menu availability | Seed + read |
| UserAccount | `user_account` | Manage user accounts (analysed) | Login (`UserDAO.get_by_username`, `UserDAO.get_by_id`) | Manage user accounts | Deactivate (analysed) | Seed + read |

Not yet in the schema (added in the iteration that builds them): `delivery` (UC-02, I3) and `voucher` (I3).
Shipper-specific data will be stored on `delivery` and `user_account`.

## Data access classes

| DAO class | File | Tables touched |
|---|---|---|
| `HubDAO` | `saigonbite/data_access/hub_dao.py` | `hub`, `hub_menu_item`, `menu_item`, `brand` |
| `CustomerDAO` | `saigonbite/data_access/customer_dao.py` | `customer`, `address` |
| `UserDAO` | `saigonbite/data_access/user_dao.py` | `user_account` |
| `OrderDAO` | `saigonbite/data_access/order_dao.py` | `orders`, `order_line` |
| `PaymentDAO` | `saigonbite/data_access/payment_dao.py` | `payment` |

## Reading the table

- "Seed + read" means the data comes from `db/seed.sql` and the code only reads it. The matching create, update and delete use cases are analysed, not built (pending lecturer confirmation).
- Nothing is physically deleted in the design: archive flags (`archived_at`) keep rows for reports.
