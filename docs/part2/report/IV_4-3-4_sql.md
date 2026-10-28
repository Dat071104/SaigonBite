# 4.3.4 SQL Code

Author: 722I0004 · AI-assisted (Codex)

## i. Create database

`python init_db.py --db PATH` creates a new SQLite version 2 database, loads the schema and seed data, and includes demo history by default. The default path is `instance/saigonbite.db`; `--no-demo` omits the demo history. Initialization enables WAL and sets `synchronous = NORMAL`. It refuses an existing path unless `--force` is used. The version check does not migrate older databases.

The following tables are created: `hub`, `brand`, `menu_item`, `hub_menu_item`, `user_account`, `customer`, `address`, `voucher`, `orders`, `order_line`, `payment`, `delivery`, `replacement_offer`.

## ii. Create tables

The following excerpt defines the hub table. The full definitions and constraints are in `db/schema.sql` in the repository.

```sql
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
