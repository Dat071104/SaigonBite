-- SaigonBite seed data, Iteration 1 (v1). Loaded by init_db.py after schema.sql.
-- Passwords are PBKDF2-SHA256 hashes (werkzeug) of the dev passwords listed in README.md
-- (pattern: dev-<username>). Never use these accounts outside a local development database.

INSERT INTO hub (id, code, name, address_text, latitude, longitude, max_active_orders, delivery_fee_flat) VALUES
 (1, 'HUB-D1', 'SaigonBite District 1 Hub', '45 Le Loi, Ben Nghe Ward, District 1, Ho Chi Minh City', 10.7769, 106.7009, 12, 15000),
 (2, 'HUB-BT', 'SaigonBite Binh Thanh Hub', '210 Xo Viet Nghe Tinh, Ward 21, Binh Thanh District, Ho Chi Minh City', 10.8106, 106.7091, 8, 18000);

INSERT INTO brand (id, name) VALUES
 (1, 'Pho Saigon Kitchen'),
 (2, 'Com Tam Corner'),
 (3, 'Banh Mi Express'),
 (4, 'Sweet Che House');

INSERT INTO menu_item (id, brand_id, name, description, price) VALUES
 (1,  1, 'Pho bo tai',          'Beef noodle soup with rare beef',                              55000),
 (2,  1, 'Pho ga',              'Chicken noodle soup',                                          50000),
 (3,  1, 'Goi cuon',            'Fresh spring rolls, 2 pieces',                                 35000),
 (4,  2, 'Com tam suon bi cha', 'Broken rice, grilled pork, shredded pork skin, egg meatloaf',  60000),
 (5,  2, 'Com tam ga nuong',    'Broken rice with grilled chicken',                             55000),
 (6,  2, 'Tra da',              'Iced tea',                                                     10000),
 (7,  3, 'Banh mi thit nuong',  'Baguette with grilled pork',                                   30000),
 (8,  3, 'Banh mi op la',       'Baguette with fried eggs',                                     25000),
 (9,  4, 'Che thai',            'Thai-style sweet dessert soup',                                30000),
 (10, 4, 'Che chuoi',           'Banana in coconut milk',                                       28000);

-- District 1 hub sells brands 1, 2, 3. Item 5 is sold out there (is_available = 0). Brand 4 is not sold at this hub.
INSERT INTO hub_menu_item (hub_id, menu_item_id, is_available) VALUES
 (1, 1, 1), (1, 2, 1), (1, 3, 1), (1, 4, 1), (1, 5, 0), (1, 6, 1), (1, 7, 1), (1, 8, 1);
-- Binh Thanh hub sells brands 2, 3, 4. Brand 1 (pho) is not sold at this hub.
INSERT INTO hub_menu_item (hub_id, menu_item_id, is_available) VALUES
 (2, 4, 1), (2, 5, 1), (2, 6, 1), (2, 7, 1), (2, 8, 1), (2, 9, 1), (2, 10, 1);

INSERT INTO user_account (id, username, password_hash, display_name, role) VALUES
 (1, 'customer', 'pbkdf2:sha256:100000$Pavi4DHwGDSc35au$74bf904066766030d728a3317e8cff03e7aa470efd1bcb15d7d51aafff2ae1fb', 'Tran Thi Mai',     'CUSTOMER'),
 (2, 'kitchen',  'pbkdf2:sha256:100000$wBrPCGfDly10scIj$7ec46b284625e2eb94bd5a20dcd0213bda94e97559c211d619ed7e494694201e', 'Kitchen Staff D1', 'KITCHEN_STAFF'),
 (3, 'shipper',  'pbkdf2:sha256:100000$SonY8ZAxxBUEE8H1$01e9ebbe9dcd424593bdc84b2f544af33832e7885ff3c6b5d1fdd3f9dae86206', 'Shipper One',      'SHIPPER'),
 (4, 'admin',    'pbkdf2:sha256:100000$xtwS2wzdjue19dju$17fb94a96b1f28314f59aaf8b6db201484c2aea4270f2425129e2c356391092f', 'Admin',            'ADMIN'),
 (5, 'manager',  'pbkdf2:sha256:100000$KMmKLTxVe4i8p6A6$7f8fe621634b6101086cfc85019ba9010fc1ab8b4e2cae5b621e8152dfb0dad2', 'Manager',          'MANAGER');

INSERT INTO customer (id, user_id, full_name, phone, customer_type) VALUES
 (1, 1, 'Tran Thi Mai', '0901234567', 'LOCAL');

INSERT INTO address (id, customer_id, label, full_address, latitude, longitude) VALUES
 (1, 1, 'Home', '12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City', 10.7745, 106.7035);
