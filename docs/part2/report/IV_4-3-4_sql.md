# 4.3.4 SQL Code

Author: 722I0004 · AI-assisted (Codex)

## i. Create database

`python init_db.py --db PATH` creates a new SQLite version 2 database, loads the schema and seed data, and includes demo history by default. The default path is `instance/saigonbite.db`; `--no-demo` omits the demo history. Initialization enables WAL and sets `synchronous = NORMAL`. It refuses an existing path unless `--force` is used. The version check does not migrate older databases.

The following tables are created: `hub`, `brand`, `menu_item`, `hub_menu_item`, `user_account`, `customer`, `address`, `voucher`, `orders`, `order_line`, `payment`, `delivery`, `replacement_offer`.

## ii. Create tables

The complete schema follows: all 13 tables with their primary keys, foreign keys, UNIQUE and CHECK constraints, the three triggers and the indexes. It is the file `db/schema.sql` exactly as the application loads it.

```sql
-- SaigonBite schema v2 (Part 2: six main use cases and their supporting use cases).
-- Table names map 1:1 to domain classes (models/shared/design_model.json):
--   hub, brand, menu_item, hub_menu_item, user_account, customer, address, voucher,
--   orders (class Order), order_line (OrderLine), payment (Payment), delivery (Delivery),
--   replacement_offer (ReplacementOffer).
-- Money is stored as whole VND (INTEGER). Timestamps are ISO-8601 UTC text (YYYY-MM-DDTHH:MM:SS+00:00).
-- State and role values are CHECK-constrained to the same names as the Python enums.
-- Nothing is physically deleted except a hub's menu listing (hub_menu_item): the rest is archived.

PRAGMA foreign_keys = ON;

CREATE TABLE hub (
    id                 INTEGER PRIMARY KEY,
    code               TEXT    NOT NULL UNIQUE,
    name               TEXT    NOT NULL,
    address_text       TEXT    NOT NULL,
    latitude           REAL    NOT NULL,
    longitude          REAL    NOT NULL,
    max_active_orders  INTEGER NOT NULL CHECK (max_active_orders > 0),   -- busy rule (Q1, A-02)
    base_delivery_fee  INTEGER NOT NULL CHECK (base_delivery_fee >= 0),  -- plus a rate per started km (Q2)
    archived_at        TEXT                                              -- NULL = active (UC-03)
);

CREATE TABLE brand (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    archived_at  TEXT                    -- NULL = active (UC-06)
);

CREATE TABLE menu_item (
    id          INTEGER PRIMARY KEY,
    brand_id    INTEGER NOT NULL REFERENCES brand(id),
    name        TEXT    NOT NULL,
    description TEXT    NOT NULL DEFAULT '',
    price       INTEGER NOT NULL CHECK (price > 0),
    archived_at TEXT,                   -- NULL = active; an archived item can no longer be ordered (UC-06)
    UNIQUE (brand_id, name)
);

-- Which menu items a hub sells (association class), and whether each is currently available there.
CREATE TABLE hub_menu_item (
    hub_id       INTEGER NOT NULL REFERENCES hub(id),
    menu_item_id INTEGER NOT NULL REFERENCES menu_item(id),
    is_available INTEGER NOT NULL DEFAULT 1 CHECK (is_available IN (0, 1)),
    PRIMARY KEY (hub_id, menu_item_id)
);

CREATE TABLE user_account (
    created_at     TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S+00:00', 'now')),
    id             INTEGER PRIMARY KEY,
    username       TEXT NOT NULL UNIQUE,
    password_hash  TEXT NOT NULL,
    display_name   TEXT NOT NULL,
    role           TEXT NOT NULL CHECK (role IN ('CUSTOMER', 'KITCHEN_STAFF', 'SHIPPER', 'ADMIN', 'MANAGER')),
    hub_id         INTEGER REFERENCES hub(id),           -- the kitchen a KITCHEN_STAFF account works in
    is_active      INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),   -- 0 = deactivated (archived)
    CHECK ((role = 'KITCHEN_STAFF') = (hub_id IS NOT NULL))
);

-- LocalCustomer and TouristCustomer share this table (single-table inheritance on customer_type).
CREATE TABLE customer (
    id             INTEGER PRIMARY KEY,
    user_id        INTEGER NOT NULL UNIQUE REFERENCES user_account(id),
    full_name      TEXT NOT NULL,
    customer_type  TEXT NOT NULL CHECK (customer_type IN ('LOCAL', 'TOURIST')),
    phone          TEXT,                 -- Vietnamese mobile number, required for LOCAL
    email          TEXT,                 -- required for TOURIST
    passport_no    TEXT,                 -- required for TOURIST
    nationality    TEXT,
    CHECK ((customer_type = 'LOCAL' AND phone IS NOT NULL)
        OR (customer_type = 'TOURIST' AND passport_no IS NOT NULL AND email IS NOT NULL AND nationality IS NOT NULL AND length(trim(nationality)) >= 2))
);


-- P4: profile ownership is a CUSTOMER account, in both update directions.
CREATE TRIGGER customer_role_insert BEFORE INSERT ON customer
WHEN NOT EXISTS (SELECT 1 FROM user_account WHERE id=NEW.user_id AND role='CUSTOMER')
BEGIN SELECT RAISE(ABORT, 'A customer profile requires a CUSTOMER account'); END;
CREATE TRIGGER customer_role_update BEFORE UPDATE OF user_id ON customer
WHEN NOT EXISTS (SELECT 1 FROM user_account WHERE id=NEW.user_id AND role='CUSTOMER')
BEGIN SELECT RAISE(ABORT, 'A customer profile requires a CUSTOMER account'); END;
CREATE TRIGGER linked_customer_role BEFORE UPDATE OF role ON user_account
WHEN NEW.role != 'CUSTOMER' AND EXISTS (SELECT 1 FROM customer WHERE user_id=OLD.id)
BEGIN SELECT RAISE(ABORT, 'A linked customer account must keep its CUSTOMER role'); END;

CREATE TABLE address (
    id           INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customer(id),
    label        TEXT NOT NULL,          -- Home, Office, Hotel ...
    full_address TEXT NOT NULL,
    district     TEXT NOT NULL,
    latitude     REAL NOT NULL,          -- from the district list (no map service, A-14)
    longitude    REAL NOT NULL,
    archived_at  TEXT                    -- NULL = usable; orders keep their own copy of the text
);

CREATE TABLE voucher (
    id             INTEGER PRIMARY KEY,
    code           TEXT    NOT NULL UNIQUE,
    description    TEXT    NOT NULL DEFAULT '',
    discount_type  TEXT    NOT NULL CHECK (discount_type IN ('FIXED', 'PERCENT')),
    discount_value INTEGER NOT NULL CHECK (discount_value > 0),
    min_subtotal   INTEGER NOT NULL DEFAULT 0 CHECK (min_subtotal >= 0),
    max_discount   INTEGER CHECK (max_discount IS NULL OR max_discount > 0),
    valid_from     TEXT    NOT NULL,     -- ISO date, inclusive (Ho Chi Minh City calendar)
    valid_until    TEXT    NOT NULL,     -- ISO date, inclusive
    archived_at    TEXT,
    CHECK (discount_type = 'FIXED' OR discount_value <= 100),
    CHECK (valid_from <= valid_until)
);

CREATE TABLE orders (
    id                    INTEGER PRIMARY KEY,
    customer_id           INTEGER NOT NULL REFERENCES customer(id),
    hub_id                INTEGER NOT NULL REFERENCES hub(id),
    address_id            INTEGER NOT NULL REFERENCES address(id),
    delivery_address_text TEXT    NOT NULL,                 -- address at order time
    distance_km           REAL    NOT NULL CHECK (distance_km >= 0),
    state                 TEXT    NOT NULL CHECK (state IN
                            ('PLACED', 'CONFIRMED', 'REJECTED', 'PREPARING', 'READY',
                             'OUT_FOR_DELIVERY', 'DELIVERED', 'DELIVERY_FAILED', 'CANCELLED')),
    item_subtotal         INTEGER NOT NULL CHECK (item_subtotal >= 0),
    voucher_id            INTEGER REFERENCES voucher(id),   -- at most one voucher per order
    voucher_discount      INTEGER NOT NULL DEFAULT 0 CHECK (voucher_discount >= 0),
    delivery_fee          INTEGER NOT NULL CHECK (delivery_fee >= 0),
    quiet_discount        INTEGER NOT NULL DEFAULT 0 CHECK (quiet_discount >= 0),
    total_amount          INTEGER NOT NULL CHECK (total_amount >= 0),
    idempotency_token     TEXT    NOT NULL UNIQUE,          -- one order per checkout form
    reject_reason         TEXT,
    placed_at             TEXT    NOT NULL,
    confirmed_at          TEXT,
    ready_at              TEXT,
    closed_at             TEXT,                             -- DELIVERED, DELIVERY_FAILED, REJECTED or CANCELLED
    archived_at           TEXT,                             -- NULL = visible on operational screens
    CHECK (total_amount = item_subtotal - voucher_discount + delivery_fee - quiet_discount),
    CHECK (voucher_discount <= item_subtotal AND quiet_discount <= delivery_fee),
    CHECK (voucher_id IS NOT NULL OR voucher_discount = 0)
);

CREATE TABLE order_line (
    id            INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(id),
    menu_item_id  INTEGER NOT NULL REFERENCES menu_item(id),
    item_name     TEXT    NOT NULL,                          -- name at order time
    unit_price    INTEGER NOT NULL CHECK (unit_price >= 0),  -- price at order time
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    UNIQUE (order_id, menu_item_id)
);

CREATE TABLE payment (
    id             INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL UNIQUE REFERENCES orders(id),
    method         TEXT    NOT NULL CHECK (method IN ('COD', 'ONLINE')),
    online_option  TEXT    CHECK (online_option IN ('E_WALLET', 'BANK_QR', 'INTERNATIONAL_CARD')),
    provider_ref   TEXT,                                     -- reference from the payment simulator
    state          TEXT    NOT NULL CHECK (state IN ('PENDING', 'PAID', 'FAILED', 'VOIDED', 'REFUND_PENDING', 'REFUNDED')),
    amount         INTEGER NOT NULL CHECK (amount >= 0),
    refund_amount  INTEGER NOT NULL DEFAULT 0 CHECK (refund_amount >= 0 AND refund_amount <= amount),
    created_at     TEXT    NOT NULL,
    updated_at     TEXT    NOT NULL,
    CHECK ((method = 'COD' AND online_option IS NULL) OR (method = 'ONLINE' AND online_option IS NOT NULL))
);

CREATE TABLE delivery (
    id              INTEGER PRIMARY KEY,
    order_id        INTEGER NOT NULL UNIQUE REFERENCES orders(id),
    shipper_id      INTEGER REFERENCES user_account(id),
    state           TEXT    NOT NULL CHECK (state IN ('AWAITING_PICKUP', 'PICKED_UP', 'DELIVERED', 'FAILED')),
    ready_at        TEXT    NOT NULL,
    picked_up_at    TEXT,
    finished_at     TEXT,                                    -- delivered or failed
    failure_reason  TEXT,
    cash_collected  INTEGER CHECK (cash_collected IS NULL OR cash_collected >= 0),
    CHECK (state = 'AWAITING_PICKUP' OR shipper_id IS NOT NULL),
    CHECK (state <> 'FAILED' OR failure_reason IS NOT NULL)
);

-- The kitchen offers one replacement for an unavailable line; the customer accepts or declines (UC-05).
CREATE TABLE replacement_offer (
    id                   INTEGER PRIMARY KEY,
    order_id             INTEGER NOT NULL REFERENCES orders(id),
    order_line_id        INTEGER NOT NULL REFERENCES order_line(id),
    original_item_name   TEXT    NOT NULL,
    original_unit_price  INTEGER NOT NULL,
    new_menu_item_id     INTEGER NOT NULL REFERENCES menu_item(id),
    new_item_name        TEXT    NOT NULL,
    new_unit_price       INTEGER NOT NULL CHECK (new_unit_price >= 0),
    state                TEXT    NOT NULL CHECK (state IN ('OFFERED', 'ACCEPTED', 'DECLINED', 'WITHDRAWN')),
    offered_at           TEXT    NOT NULL,
    decided_at           TEXT,
    CHECK (new_unit_price <= original_unit_price)
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_hub_state ON orders(hub_id, state);
CREATE INDEX idx_order_line_order ON order_line(order_id);
CREATE INDEX idx_delivery_state ON delivery(state);
CREATE INDEX idx_delivery_finished ON delivery(finished_at);
CREATE INDEX idx_offer_order ON replacement_offer(order_id);
-- At most one open replacement offer per order.
CREATE UNIQUE INDEX idx_offer_one_open ON replacement_offer(order_id) WHERE state = 'OFFERED';

PRAGMA user_version = 2;
```

## iii. Sample data

The seed contains hubs, brands, menu items, accounts, addresses and vouchers. The following excerpt supplies the hub records; `db/seed_demo.sql` adds demo order history.

```sql
INSERT INTO hub (id, code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee) VALUES
 (1, 'HUB-D1', 'SaigonBite District 1 Hub', '45 Le Loi, Ben Nghe Ward, District 1, Ho Chi Minh City', 10.7769, 106.7009, 12, 12000),
 (2, 'HUB-BT', 'SaigonBite Binh Thanh Hub', '210 Xo Viet Nghe Tinh, Ward 21, Binh Thanh District, Ho Chi Minh City', 10.8106, 106.7091, 8, 10000);
```

### Example management queries

The following read-only queries were captured from `saigonbite/data_access/report_dao.py` and executed on 28 October 2026 against a newly initialized database with demo data at source revision `97574bd`. Dates in the SQL define the sample window; returned data is demonstration data. The sample is not evidence of production usage. Full inputs and output are in `Part2/notes/P7/sql_sample_results.json`.

#### Sales By Hub

```sql
SELECT COUNT(*) FROM orders o LEFT JOIN payment p ON p.order_id=o.id LEFT JOIN delivery d ON d.order_id=o.id WHERE (o.state='DELIVERED' AND (p.id IS NULL OR d.id IS NULL OR d.state!='DELIVERED' OR d.finished_at IS NULL)) OR (o.state='DELIVERY_FAILED' AND (p.id IS NULL OR d.id IS NULL OR d.state!='FAILED' OR d.finished_at IS NULL));
SELECT h.id AS hub_id, h.name AS hub_name, COUNT(*) AS orders,        SUM(o.item_subtotal) AS item_sales, SUM(o.voucher_discount) AS voucher_discounts,        SUM(o.delivery_fee - o.quiet_discount) AS delivery_fees, SUM(o.total_amount) AS total,        SUM(p.refund_amount) AS refunds_owed FROM orders o JOIN delivery d ON d.order_id = o.id JOIN payment p ON p.order_id = o.id JOIN hub h ON h.id = o.hub_id WHERE o.state = 'DELIVERED' AND d.finished_at >= '2000-01-01' AND d.finished_at < '2100-01-01'   AND (NULL IS NULL OR o.hub_id = NULL) GROUP BY h.id, h.name ORDER BY h.id;
```

The first statement is an integrity precheck; its result was `0`. The second statement returned the following rows.

| hub_id | hub_name | orders | item_sales | voucher_discounts | delivery_fees | total | refunds_owed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SaigonBite District 1 Hub | 2 | 250000 | 13000 | 25000 | 262000 | 0 |
| 2 | SaigonBite Binh Thanh Hub | 1 | 80000 | 20000 | 17000 | 77000 | 0 |

#### Top Items

```sql
WITH eligible AS (SELECT ol.*, d.finished_at FROM order_line ol JOIN orders o ON o.id=ol.order_id JOIN delivery d ON d.order_id=o.id WHERE o.state='DELIVERED' AND d.finished_at >= '2000-01-01' AND d.finished_at < '2100-01-01' AND (NULL IS NULL OR o.hub_id=NULL)) SELECT ol.menu_item_id, (SELECT n.item_name FROM eligible n WHERE n.menu_item_id=ol.menu_item_id ORDER BY n.finished_at DESC,n.order_id DESC,n.id DESC LIMIT 1) AS item_name, SUM(ol.quantity) AS quantity, SUM(ol.unit_price * ol.quantity) AS revenue FROM eligible ol GROUP BY ol.menu_item_id ORDER BY revenue DESC, ol.menu_item_id LIMIT 10;
```

| menu_item_id | item_name | quantity | revenue |
| --- | --- | --- | --- |
| 1 | Pho bo tai | 2 | 110000 |
| 3 | Goi cuon | 2 | 70000 |
| 4 | Com tam suon bi cha | 1 | 60000 |
| 9 | Che thai | 2 | 60000 |
| 6 | Tra da | 3 | 30000 |

#### Open Orders By Hub And State

```sql
SELECT hub_id, state, COUNT(*) AS n FROM orders WHERE state IN ('PLACED', 'CONFIRMED', 'PREPARING', 'READY', 'OUT_FOR_DELIVERY') GROUP BY hub_id, state;
```

| hub_id | state | n |
| --- | --- | --- |
| 1 | PLACED | 1 |
| 1 | READY | 1 |

#### Finished Deliveries

```sql
SELECT COUNT(*) FROM orders o LEFT JOIN payment p ON p.order_id=o.id LEFT JOIN delivery d ON d.order_id=o.id WHERE (o.state='DELIVERED' AND (p.id IS NULL OR d.id IS NULL OR d.state!='DELIVERED' OR d.finished_at IS NULL)) OR (o.state='DELIVERY_FAILED' AND (p.id IS NULL OR d.id IS NULL OR d.state!='FAILED' OR d.finished_at IS NULL));
SELECT o.id AS order_id, o.hub_id, h.name AS hub_name, d.state, d.ready_at, d.picked_up_at,        d.finished_at, d.shipper_id, u.display_name AS shipper_name FROM delivery d JOIN orders o ON o.id = d.order_id JOIN hub h ON h.id = o.hub_id LEFT JOIN user_account u ON u.id = d.shipper_id WHERE d.state IN ('DELIVERED', 'FAILED') AND d.finished_at >= '2000-01-01' AND d.finished_at < '2100-01-01'   AND (NULL IS NULL OR o.hub_id = NULL) ORDER BY o.hub_id, d.finished_at;
```

The first statement is an integrity precheck; its result was `0`. The second statement returned the following rows.

| order_id | hub_id | hub_name | state | ready_at | picked_up_at | finished_at | shipper_id | shipper_name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | SaigonBite District 1 Hub | DELIVERED | 2026-10-20T04:20:00+00:00 | 2026-10-20T04:30:00+00:00 | 2026-10-20T04:55:00+00:00 | 3 | Shipper One |
| 2 | 1 | SaigonBite District 1 Hub | DELIVERED | 2026-10-20T17:00:00+00:00 | 2026-10-20T17:05:00+00:00 | 2026-10-20T17:20:00+00:00 | 8 | Shipper Two |
| 3 | 2 | SaigonBite Binh Thanh Hub | FAILED | 2026-10-21T05:15:00+00:00 | 2026-10-21T05:25:00+00:00 | 2026-10-21T05:50:00+00:00 | 3 | Shipper One |
| 6 | 2 | SaigonBite Binh Thanh Hub | DELIVERED | 2026-10-22T03:20:00+00:00 | 2026-10-22T03:35:00+00:00 | 2026-10-22T04:05:00+00:00 | 8 | Shipper Two |
