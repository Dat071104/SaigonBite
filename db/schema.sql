-- SaigonBite schema, Iteration 1 (v1).
-- Table names map 1:1 to domain classes (see docs/i1/domain_model_v1.md):
--   hub, brand, menu_item, hub_menu_item, user_account, customer, address,
--   orders (class Order), order_line (OrderLine), payment (Payment).
-- Money is stored as whole VND (INTEGER). Timestamps are ISO-8601 UTC text.
-- State and role values are CHECK-constrained to the same names as the Python enums.

PRAGMA foreign_keys = ON;

CREATE TABLE hub (
    id                 INTEGER PRIMARY KEY,
    code               TEXT    NOT NULL UNIQUE,
    name               TEXT    NOT NULL,
    address_text       TEXT    NOT NULL,
    latitude           REAL,
    longitude          REAL,
    max_active_orders  INTEGER NOT NULL CHECK (max_active_orders > 0),  -- capacity rule is enforced from I2
    delivery_fee_flat  INTEGER NOT NULL CHECK (delivery_fee_flat >= 0), -- flat fee until the client answers question 2
    archived_at        TEXT                                             -- NULL = active (UC-03 archives in I2)
);

CREATE TABLE brand (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE menu_item (
    id          INTEGER PRIMARY KEY,
    brand_id    INTEGER NOT NULL REFERENCES brand(id),
    name        TEXT    NOT NULL,
    description TEXT    NOT NULL DEFAULT '',
    price       INTEGER NOT NULL CHECK (price >= 0)
);

-- Which menu items a hub sells, and whether each is currently available there.
CREATE TABLE hub_menu_item (
    hub_id       INTEGER NOT NULL REFERENCES hub(id),
    menu_item_id INTEGER NOT NULL REFERENCES menu_item(id),
    is_available INTEGER NOT NULL DEFAULT 1 CHECK (is_available IN (0, 1)),
    PRIMARY KEY (hub_id, menu_item_id)
);

CREATE TABLE user_account (
    id             INTEGER PRIMARY KEY,
    username       TEXT NOT NULL UNIQUE,
    password_hash  TEXT NOT NULL,
    display_name   TEXT NOT NULL,
    role           TEXT NOT NULL CHECK (role IN ('CUSTOMER', 'KITCHEN_STAFF', 'SHIPPER', 'ADMIN', 'MANAGER')),
    is_active      INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
);

CREATE TABLE customer (
    id             INTEGER PRIMARY KEY,
    user_id        INTEGER NOT NULL UNIQUE REFERENCES user_account(id),
    full_name      TEXT NOT NULL,
    phone          TEXT NOT NULL,
    customer_type  TEXT NOT NULL CHECK (customer_type IN ('LOCAL', 'TOURIST'))
);

CREATE TABLE address (
    id           INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customer(id),
    label        TEXT NOT NULL,
    full_address TEXT NOT NULL,
    latitude     REAL,
    longitude    REAL
);

CREATE TABLE orders (
    id                 INTEGER PRIMARY KEY,
    customer_id        INTEGER NOT NULL REFERENCES customer(id),
    hub_id             INTEGER NOT NULL REFERENCES hub(id),
    address_id         INTEGER NOT NULL REFERENCES address(id),
    state              TEXT    NOT NULL CHECK (state IN
                         ('PLACED', 'CONFIRMED', 'REJECTED', 'PREPARING', 'READY',
                          'OUT_FOR_DELIVERY', 'DELIVERED', 'DELIVERY_FAILED', 'CANCELLED')),
    item_subtotal      INTEGER NOT NULL CHECK (item_subtotal >= 0),
    delivery_fee       INTEGER NOT NULL CHECK (delivery_fee >= 0),
    total_amount       INTEGER NOT NULL,
    idempotency_token  TEXT    NOT NULL UNIQUE,   -- one order per checkout form (AC-7)
    placed_at          TEXT    NOT NULL,
    archived_at        TEXT,                      -- NULL = visible; archive use case is analysed, not built
    CHECK (total_amount = item_subtotal + delivery_fee)
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
    id          INTEGER PRIMARY KEY,
    order_id    INTEGER NOT NULL UNIQUE REFERENCES orders(id),
    method      TEXT    NOT NULL CHECK (method IN ('COD', 'ONLINE')),
    state       TEXT    NOT NULL CHECK (state IN ('PENDING', 'PAID', 'FAILED', 'VOIDED', 'REFUND_PENDING', 'REFUNDED')),
    amount      INTEGER NOT NULL CHECK (amount >= 0),
    created_at  TEXT    NOT NULL
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_hub_state ON orders(hub_id, state);
CREATE INDEX idx_order_line_order ON order_line(order_id);
