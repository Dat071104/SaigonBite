-- SaigonBite demo history, loaded after seed.sql by `python init_db.py` (skip with --no-demo).
-- It gives the kitchen, shipper and manager screens something to show, and it is the oracle dataset
-- for UC-04: the expected report figures in docs/part2/uc04_report_oracle.md were calculated by hand
-- from these rows before the report queries were written. Times are UTC; Ho Chi Minh City is UTC+7.
--
-- #  hub  customer  state            payment                     total    note
-- 1  D1   Mai       DELIVERED        COD PAID                    130,000  delivered 11:55 on 20/10 (VN)
-- 2  D1   Emma      DELIVERED        ONLINE card PAID            132,000  LUNCH10; delivered 00:20 on 21/10 (VN), 17:20 on 20/10 UTC
-- 3  BT   Mai       DELIVERY_FAILED  COD VOIDED                   80,000  customer did not answer
-- 4  D1   Mai       REJECTED         ONLINE e-wallet REFUND_PENDING 60,000
-- 5  D1   Mai       CANCELLED        COD VOIDED                   60,000
-- 6  BT   Emma      DELIVERED        COD PAID                     77,000  WELCOME20K; delivered 11:05 on 22/10 (VN)
-- 7  D1   Mai       READY            COD PENDING                  65,000  waiting for a shipper
-- 8  D1   Emma      PLACED           ONLINE card PAID             45,000  waiting for the kitchen

INSERT INTO orders (id, customer_id, hub_id, address_id, delivery_address_text, distance_km, state,
                    item_subtotal, voucher_id, voucher_discount, delivery_fee, quiet_discount, total_amount,
                    idempotency_token, reject_reason, placed_at, confirmed_at, ready_at, closed_at) VALUES
 (1, 1, 1, 1, '12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City', 0.39, 'DELIVERED',
  120000, NULL, 0, 15000, 5000, 130000, 'seed-1', NULL,
  '2026-10-20T04:00:00+00:00', '2026-10-20T04:02:00+00:00', '2026-10-20T04:20:00+00:00', '2026-10-20T04:55:00+00:00'),
 (2, 2, 1, 3, 'Rex Hotel, 141 Nguyen Hue, District 1, Ho Chi Minh City', 0.06, 'DELIVERED',
  130000, 1, 13000, 15000, 0, 132000, 'seed-2', NULL,
  '2026-10-20T16:40:00+00:00', '2026-10-20T16:42:00+00:00', '2026-10-20T17:00:00+00:00', '2026-10-20T17:20:00+00:00'),
 (3, 1, 2, 1, '12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City', 4.06, 'DELIVERY_FAILED',
  60000, NULL, 0, 25000, 5000, 80000, 'seed-3', NULL,
  '2026-10-21T05:00:00+00:00', '2026-10-21T05:02:00+00:00', '2026-10-21T05:15:00+00:00', '2026-10-21T05:50:00+00:00'),
 (4, 1, 1, 1, '12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City', 0.39, 'REJECTED',
  50000, NULL, 0, 15000, 5000, 60000, 'seed-4', 'Out of chicken today',
  '2026-10-21T06:00:00+00:00', NULL, NULL, '2026-10-21T06:03:00+00:00'),
 (5, 1, 1, 1, '12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City', 0.39, 'CANCELLED',
  50000, NULL, 0, 15000, 5000, 60000, 'seed-5', NULL,
  '2026-10-21T07:00:00+00:00', '2026-10-21T07:01:00+00:00', NULL, '2026-10-21T07:05:00+00:00'),
 (6, 2, 2, 3, 'Rex Hotel, 141 Nguyen Hue, District 1, Ho Chi Minh City', 3.89, 'DELIVERED',
  80000, 2, 20000, 22000, 5000, 77000, 'seed-6', NULL,
  '2026-10-22T03:00:00+00:00', '2026-10-22T03:02:00+00:00', '2026-10-22T03:20:00+00:00', '2026-10-22T04:05:00+00:00'),
 (7, 1, 1, 1, '12 Nguyen Hue, Ben Nghe Ward, District 1, Ho Chi Minh City', 0.39, 'READY',
  55000, NULL, 0, 15000, 5000, 65000, 'seed-7', NULL,
  '2026-10-23T03:00:00+00:00', '2026-10-23T03:01:00+00:00', '2026-10-23T03:15:00+00:00', NULL),
 (8, 2, 1, 3, 'Rex Hotel, 141 Nguyen Hue, District 1, Ho Chi Minh City', 0.06, 'PLACED',
  35000, NULL, 0, 15000, 5000, 45000, 'seed-8', NULL,
  '2026-10-23T03:10:00+00:00', NULL, NULL, NULL);

INSERT INTO order_line (order_id, menu_item_id, item_name, unit_price, quantity) VALUES
 (1, 1, 'Pho bo tai', 55000, 2), (1, 6, 'Tra da', 10000, 1),
 (2, 4, 'Com tam suon bi cha', 60000, 1), (2, 3, 'Goi cuon', 35000, 2),
 (3, 7, 'Banh mi thit nuong', 30000, 2),
 (4, 2, 'Pho ga', 50000, 1),
 (5, 8, 'Banh mi op la', 25000, 2),
 (6, 9, 'Che thai', 30000, 2), (6, 6, 'Tra da', 10000, 2),
 (7, 1, 'Pho bo tai', 55000, 1),
 (8, 3, 'Goi cuon', 35000, 1);

INSERT INTO payment (order_id, method, online_option, provider_ref, state, amount, created_at, updated_at) VALUES
 (1, 'COD',    NULL,                 NULL,         'PAID',           130000, '2026-10-20T04:00:00+00:00', '2026-10-20T04:55:00+00:00'),
 (2, 'ONLINE', 'INTERNATIONAL_CARD', 'SIM-SEED-2', 'PAID',           132000, '2026-10-20T16:40:00+00:00', '2026-10-20T16:40:00+00:00'),
 (3, 'COD',    NULL,                 NULL,         'VOIDED',          80000, '2026-10-21T05:00:00+00:00', '2026-10-21T05:50:00+00:00'),
 (4, 'ONLINE', 'E_WALLET',           'SIM-SEED-4', 'REFUND_PENDING',  60000, '2026-10-21T06:00:00+00:00', '2026-10-21T06:03:00+00:00'),
 (5, 'COD',    NULL,                 NULL,         'VOIDED',          60000, '2026-10-21T07:00:00+00:00', '2026-10-21T07:05:00+00:00'),
 (6, 'COD',    NULL,                 NULL,         'PAID',            77000, '2026-10-22T03:00:00+00:00', '2026-10-22T04:05:00+00:00'),
 (7, 'COD',    NULL,                 NULL,         'PENDING',         65000, '2026-10-23T03:00:00+00:00', '2026-10-23T03:00:00+00:00'),
 (8, 'ONLINE', 'INTERNATIONAL_CARD', 'SIM-SEED-8', 'PAID',            45000, '2026-10-23T03:10:00+00:00', '2026-10-23T03:10:00+00:00');

INSERT INTO delivery (order_id, shipper_id, state, ready_at, picked_up_at, finished_at, failure_reason, cash_collected) VALUES
 (1, 3, 'DELIVERED',       '2026-10-20T04:20:00+00:00', '2026-10-20T04:30:00+00:00', '2026-10-20T04:55:00+00:00', NULL, 130000),
 (2, 8, 'DELIVERED',       '2026-10-20T17:00:00+00:00', '2026-10-20T17:05:00+00:00', '2026-10-20T17:20:00+00:00', NULL, NULL),
 (3, 3, 'FAILED',          '2026-10-21T05:15:00+00:00', '2026-10-21T05:25:00+00:00', '2026-10-21T05:50:00+00:00', 'Customer did not answer the phone', NULL),
 (6, 8, 'DELIVERED',       '2026-10-22T03:20:00+00:00', '2026-10-22T03:35:00+00:00', '2026-10-22T04:05:00+00:00', NULL, 77000),
 (7, NULL, 'AWAITING_PICKUP', '2026-10-23T03:15:00+00:00', NULL, NULL, NULL, NULL);
