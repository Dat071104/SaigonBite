-- SaigonBite seed data v2. Loaded by init_db.py after schema.sql. Synthetic data only.
-- Every account uses the demo password 123456 (PBKDF2-SHA256 hashes, werkzeug). Demo only.
-- Delivery fees (rules.py): base fee + 3,000 VND per started km. Home -> District 1 hub is 0.39 km
-- (fee 15,000); Home -> Binh Thanh hub is 4.06 km (fee 25,000); the Thu Duc office is 9.91 km from
-- the District 1 hub, beyond the 8 km limit.

INSERT INTO hub (id, code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee) VALUES
 (1, 'HUB-D1', 'SaigonBite District 1 Hub', '45 Le Loi, Ben Nghe Ward, District 1, Ho Chi Minh City', 10.7769, 106.7009, 12, 12000),
 (2, 'HUB-BT', 'SaigonBite Binh Thanh Hub', '210 Xo Viet Nghe Tinh, Ward 21, Binh Thanh District, Ho Chi Minh City', 10.8106, 106.7091, 8, 10000);

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

INSERT INTO user_account (id, username, password_hash, display_name, role, hub_id) VALUES
 (1, 'customer',   'pbkdf2:sha256:100000$PhSM7peDBNn8Sqnv$2a2e2efda712e6b381fa0f460b78977355de602bdbf827a3aab7327a6185e2a9', 'Tran Thi Mai',     'CUSTOMER',      NULL),
 (2, 'kitchen',    'pbkdf2:sha256:100000$va70Ry6f66c3wV2z$43b879d083d626bd2fd22a3650cee75494fe2ac3b34852acb9945292f7d6acaa', 'Kitchen Staff D1', 'KITCHEN_STAFF', 1),
 (3, 'shipper',    'pbkdf2:sha256:100000$DzClandDgQSZAum8$0b8e9589fa9c3063b6b4238b74c79316b2db3dd649ffca0f7336d7926a3c30d2', 'Shipper One',      'SHIPPER',       NULL),
 (4, 'admin',      'pbkdf2:sha256:100000$mQyIk1Madu2LRMmR$8ba8d34cd406e14ce39d917c224a99c62f9f7eee3a516dc4aca954e62c4a24e7', 'Admin',            'ADMIN',         NULL),
 (5, 'manager',    'pbkdf2:sha256:100000$yW7pPwKhrFtfOfwW$c013d40da1e780407b75290218b243d9616cb30a14823235626979b86dc4fd1a', 'Manager',          'MANAGER',       NULL),
 (6, 'tourist',    'pbkdf2:sha256:100000$UyEdmvGwZLsxzi8g$6c88a2b80ceb06d8c8e9210978304fb32301b17afbd5422372a1e75d688929fb', 'Emma Wilson',      'CUSTOMER',      NULL),
 (7, 'kitchen_bt', 'pbkdf2:sha256:100000$NH6YHGWOrVVovQie$f776731c444333ac77b1f1ea5beaa28667870377b9941b68e59886f2aa35c304', 'Kitchen Staff BT', 'KITCHEN_STAFF', 2),
 (8, 'shipper2',   'pbkdf2:sha256:100000$CYTSBMFPtAoTpzoj$82afe7e6e1da155da643f6cd3b4a642d0d2b948bee77b55c383779dbce15a1bc', 'Shipper Two',      'SHIPPER',       NULL);

INSERT INTO customer (id, user_id, full_name, customer_type, phone, email, passport_no, nationality) VALUES
 (1, 1, 'Tran Thi Mai', 'LOCAL',   '0901234567', NULL,                      NULL,        NULL),
 (2, 6, 'Emma Wilson',  'TOURIST', NULL,         'emma.wilson@example.com', 'X1234567',  'Australia');

INSERT INTO address (id, customer_id, label, full_address, district, latitude, longitude) VALUES
 (1, 1, 'Home',   '12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City', 'District 1', 10.7745, 106.7035),
 (2, 1, 'Office', '1 Vo Van Ngan, Thu Duc, Ho Chi Minh City',                   'Thu Duc',    10.8494, 106.7537),
 (3, 2, 'Hotel',  'Rex Hotel, 141 Nguyen Hue, District 1, Ho Chi Minh City',    'District 1', 10.7765, 106.7012);

INSERT INTO voucher (id, code, description, discount_type, discount_value, min_subtotal, max_discount, valid_from, valid_until) VALUES
 (1, 'LUNCH10',    '10% off dishes from 100,000 VND, at most 20,000 VND', 'PERCENT', 10,    100000, 20000, '2026-10-01', '2027-12-31'),
 (2, 'WELCOME20K', '20,000 VND off dishes from 80,000 VND',               'FIXED',   20000, 80000,  NULL,  '2026-10-01', '2027-12-31'),
 (3, 'SUMMER15',   '15% off, summer 2026 (expired)',                      'PERCENT', 15,    0,      NULL,  '2026-06-01', '2026-08-31');
