# Part 2 business rules

Author: 722I0004 · AI-assisted (Codex)

Source: locked plan §3. Tests remain blank until P4. Q links identify open questions, not client confirmation.

All values not fixed by the case are **team defaults, not client-confirmed**. Constants live in `saigonbite/business/domain/rules.py`; each rule has a stable ID cited by tests and by the Assumption Log. Assumption Log keeps A-01…A-11 from Part 1; new entries start at A-12.

### 3.1 Ordering and pricing

| ID | Rule | Default | Assumption  Q link | Tests |
|---|---|---|------|---|
| BR-01 | Kitchen load = orders in PLACED, CONFIRMED, PREPARING (a PLACED order waiting on an offer counts). Capacity ≥ 1. | — | A-02  Q1 | |
| BR-02 | Busy: load ≥ `max_active_orders` → refuse. Rechecked inside the write transaction at confirm; two customers racing for the last slot cannot both get an order. | — | A-02  Q1 | |
| BR-03 | Quiet: load (before inserting the new order) < 25 % of capacity → discount `min(5,000, delivery fee)`. Stored on the order; later load changes never reprice. | 25 %, 5,000 VND | A-03 → A-12 (figures)  Q1 | |
| BR-04 | Busy hub → up to 3 other ACTIVE, non-busy hubs within range, ordered by load ratio, then distance, then ID. Text says the menu may differ and a new quote is needed. Empty list handled. | 3 | A-13  Q1; Q2 | |
| BR-05 | Distance = Haversine km between hub coordinates and the **district centroid** of the address (labelled "approximate" on the quote). Raw value used for rules; rounded only for display and storage after the check. | — | A-04 → A-14  Q2 | |
| BR-06 | Radius: accept `d ≤ 8.0` km raw; reject `d > 8.0`. | 8.0 km | A-14  Q2 | |
| BR-07 | Fee = `hub.base_delivery_fee + 3,000 × max(1, ceil(d))` whole VND; rule shown on the quote. | 3,000 VND/started km, min 1 | A-15  Q2 | |
| BR-08 | Voucher: 0 or 1 per order. FIXED or PERCENT of item subtotal; percent rounds down; capped by `max_discount` and by subtotal; `min_subtotal`; valid_from/valid_until inclusive Vietnam calendar dates; archived = unusable. | — | Case; A-16  — | |
| BR-09 | Total `T = S − D + F − Q` with `0 ≤ D ≤ S`, `0 ≤ Q ≤ F`; all stored; table CHECK enforces it. | — | A-16  — | |
| BR-10 | Consent: confirm recomputes the quote and compares a **fingerprint** (hub, address, lines item/qty/unit price, voucher code + D, F, Q, payment method/option) and T. Any difference → new quote shown, nothing saved. Client-posted prices never trusted. | — | A-17  — | |
| BR-11 | Replay: the same checkout token returns the existing order of that customer; UNIQUE constraint on the token; another customer's token never reveals an order. | — | I1  — | |
| BR-12 | Customer types: Local = Vietnamese mobile required (validation pattern documented). Tourist = passport no., nationality, e-mail; phone optional; may label an address "Hotel". Passport shown only to the customer and admin, never on kitchen/shipper boards or logs. | — | Case; A-18  — | |
| BR-13 | Receipt: own-order page has a printable receipt: order ID, date, hub, address snapshot, lines (snapshot name/price/qty), S, D, F, Q, T, method/option, payment state, refund owed. "Simulated payment" label on ONLINE. | — | Case; A-19  — | |
| BR-14 | Payment options: COD for all. ONLINE: Local → E_WALLET or BANK_QR; Tourist → INTERNATIONAL_CARD. Team simulator approves/declines; decline → no order, no payment row. The simulator page (customer choosing approve/decline) happens **before** the transaction. The short, deterministic, in-process simulator decision and the order/line/payment writes run inside the checkout transaction; approve → payment PAID (captured). If the transaction fails at any point up to and including COMMIT, the simulated authorisation is released and nothing is saved (tested by forcing a failure at commit, not only at an insert). No real card data. A future real provider would need a separately designed authorisation/commit/recovery boundary (out of scope). | — | A-05, A-06  Q4; L2 | |

### 3.2 Order lifecycle rules

| ID | Rule  Q link | Tests |
|---|------|---|
| BR-15 | Customer cancels while PLACED or CONFIRMED (Q3). Open offer → WITHDRAWN.  Q3 | |
| BR-16 | Kitchen rejects PLACED with a reason. Open offer → WITHDRAWN.  — | |
| BR-17 | Unfulfilled terminal outcome (reject, cancel, decline, delivery failure): COD → VOIDED; ONLINE → REFUND_PENDING **and** `refund_amount = C` (full captured amount, replacing any partial amount). State and amount saved together.  Q3 | |
| BR-18 | Hub archive only with no open orders (any state other than DELIVERED, DELIVERY_FAILED, REJECTED, CANCELLED). Capacity may be lowered below current load (hub then refuses until load drops), never below 1.  — | |
| BR-19 | Brand/item archive or price change never touches existing order lines (snapshots). Archived brand/item cannot be listed or ordered.  — | |
| BR-25 | Shipper: any active shipper may take any READY order (no one-active-delivery limit); take is atomic; only the assigned shipper finishes; COD cash must equal T exactly. Admin cannot deactivate a shipper who holds a PICKED_UP delivery.  — | |
| BR-26 | Kitchen staff act only on orders of their own hub (`user_account.hub_id`).  — | |

### 3.3 Replacement and money (UC-05 + SUC-03)

1. Kitchen offers a replacement only for a line of an own-hub PLACED order whose dish is **currently unavailable** at that hub (sold out, unlisted or archived). Whole line replaced; quantity unchanged.
2. At most one OFFERED offer per order at a time (UNIQUE partial index). Resolved offers stay as history; another offer is allowed while still PLACED.
3. Target: ACTIVE, listed and AVAILABLE at the hub, different from the source, not already a line of the order, unit price ≤ source snapshot price. Cross-brand allowed (stated default).
4. The offer stores original and new names/prices. The customer sees original line, new line, quantity, new total and refund owed (ONLINE) before answering. Kitchen confirm/start preparing blocked while an offer is open.
5. Accept (one transaction): recheck ownership, order PLACED, offer is the exact open one, target still listed/available/not archived. Target invalid → offer WITHDRAWN with reason, order unchanged, message shown. Valid → line replaced at the **offered** price even if the catalogue price changed since.
6. Voucher after accept: `D_new = min(D_old, S_new)` (service-recovery concession; voucher terms are not re-evaluated). F and Q unchanged. (Already in code.)
7. COD: payable = new T. ONLINE: `payment.amount` stays C (captured); state stays PAID; `refund_amount = C − T_new` (owed, not paid). UI: "refund owed", never "refunded".
8. Decline → order REJECTED (reason "customer declined replacement"), BR-17. Stale/repeated answers change nothing. Accept-then-cancel is a valid sequence; an answer can never revive a CANCELLED/REJECTED order.
9. After a partial refund owed, a later cancel sets `refund_amount = C` (not C + partial).
10. Payout deferred (L3): no path sets REFUNDED or says "refunded".

Oracle example (used as a fixed test): S = 100,000, D = 10,000, F = 15,000, Q = 5,000 → T = C = 100,000. Replacement lowers S to 90,000 → D stays 10,000 → T = 90,000. COD owes 90,000; ONLINE refund owed 10,000. Cancel afterwards → ONLINE refund owed 100,000. Delivered instead → sales total 90,000, refund owed 10,000 shown separately, **not** subtracted again.

### 3.4 Reports (UC-04)

| ID | Rule  Q link | Tests |
|---|------|---|
| BR-20 | Timestamps stored UTC. Report dates entered as Asia/Ho_Chi_Minh calendar days; query `[start 00:00 VN, end+1 00:00 VN)` converted to UTC.  Q5 | |
| BR-21 | Sales: DELIVERED orders by delivery finish time. Columns: orders, item sales (S), voucher discounts (D), net delivery fees (F − Q), order totals (T), refunds owed (shown, never subtracted from T). Labelled operational sales, not accounting.  Q5 | |
| BR-22 | Workload: current snapshot per hub: cooking load vs capacity, plus READY and OUT_FOR_DELIVERY counts. Not date-filtered (labelled "now").  Q1; Q5 | |
| BR-23 | Delivery performance (deliveries finished in period): mean wait READY → PICKED_UP, mean ride PICKED_UP → DELIVERED (successful only), failure rate = failed ÷ (delivered + failed), "n/a" if 0; sample size shown per figure.  Q5 | |
| BR-24 | Order-level sums from `orders` only (no line join); line-level sums grouped by `menu_item_id` (name shown from snapshot). Archived orders included. Reports never write.  Q5 | |

---
