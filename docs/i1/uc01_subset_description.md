> AI-assisted (Claude); reviewed and corrected by the team in October 2026.

# UC-01 Place an order - Iteration 1 subset

Owner: Dat (722I0004). Actor: Customer. Built 19/10/2026 (I1 day D3) as the first increment.
Names in this file are the names used in `db/schema.sql` and the Python code (AC-9). Activity diagram: `activity_uc01_subset.md`.

## 1. Scope of the subset

| In the I1 subset | Not in the subset (later iterations) |
|---|---|
| Login with a seeded customer account | Registering a customer (analysed, not built) |
| One hub per order, chosen from the active hubs | Busy-hub check and "quieter hub" suggestion (I2) |
| Items, quantities, delivery address (customer's own addresses) | Voucher, distance fee, quiet incentive (I3) |
| Quote: item subtotal, flat delivery fee, total | Online payment stub, tourist payment options (I3) |
| Payment method COD only; Payment state `PENDING` | Payment states `PAID`, `FAILED`, `VOIDED`, `REFUND_PENDING` set by later use cases |
| Order created in state `PLACED` | Kitchen board and delivery moving the order on (I2, I3) |

## 2. Preconditions

| ID | Precondition |
|---|---|
| PRE-01 | The database was created by `python init_db.py` (schema and seed loaded). |
| PRE-02 | The user is logged in and the `user_account.role` is `CUSTOMER`. |
| PRE-03 | The customer has at least one `address`. |
| PRE-04 | At least one active hub (`hub.archived_at` is NULL) carries at least one available item (`hub_menu_item.is_available = 1`). |

## 3. Postconditions

Success (the customer confirms a valid quote):

| ID | Postcondition |
|---|---|
| POST-01 | Exactly one `orders` row exists for the checkout form, with `state = 'PLACED'`, and one `order_line` row per ordered item (item name and unit price copied at order time). |
| POST-02 | Exactly one `payment` row exists for the order with `method = 'COD'`, `state = 'PENDING'` and `amount` equal to the order total. |
| POST-03 | `total_amount = item_subtotal + delivery_fee`, where `item_subtotal` is the sum of `unit_price * quantity` and `delivery_fee` is the hub's `delivery_fee_flat`. |
| POST-04 | The order, its lines and its payment were written in one transaction (`BEGIN IMMEDIATE` ... `COMMIT`); a failure leaves none of them. |
| POST-05 | The confirmation page shows the order ID and the total. |
| POST-06 | Submitting the same form again (same `idempotency_token`) writes nothing new and shows the first order. |

Failure (any rule below is broken):

| ID | Postcondition |
|---|---|
| POST-F1 | No `orders`, `order_line` or `payment` row is written, and the customer sees a message that names the problem. The entered quantities stay in the form. |

## 4. Business rules used by the subset

| ID | Rule |
|---|---|
| BR-01 | An order belongs to exactly one hub. |
| BR-02 | The delivery fee is the flat value seeded on the hub (`hub.delivery_fee_flat`) until the client answers question 2 (distance and fee formula). |
| BR-03 | Quantity is a whole number from 1 to 99. A blank quantity means "not ordered". |
| BR-04 | An item can be ordered only if the hub carries it and it is available there. |
| BR-05 | The address must be one of the customer's own addresses. |
| BR-06 | Prices come from the database when the quote and the order are built, never from the browser. |
| BR-07 | Only a logged-in user with role `CUSTOMER` can quote or confirm; the check runs on the server. |
| BR-08 | One checkout form produces at most one order (idempotency token, unique in `orders.idempotency_token`). |
| BR-09 | Payment method is COD; the new payment is `PENDING` (COD is paid when the shipper confirms collection, assumption A-06). |

## 5. Main flow

| Step | Actor / system | Action | System operation (SSD) |
|---|---|---|---|
| 1 | Customer | Logs in with username and password. | `login` |
| 2 | System | Shows the active hubs with their flat delivery fee. | `listHubs` |
| 3 | Customer | Chooses a hub. | `selectHub` |
| 4 | System | Shows the hub's menu (sold-out items marked) and the customer's addresses. | `selectHub` (response) |
| 5 | Customer | Enters quantities, chooses the delivery address and asks for the quote. | `requestQuote` |
| 6 | System | Validates (section 6), prices the cart and shows item subtotal, delivery fee and total with a fresh idempotency token. | `requestQuote` (response) |
| 7 | Customer | Confirms the order. | `confirmOrder` |
| 8 | System | Re-validates and re-prices; if the total still matches the quote, creates in one transaction Order `PLACED`, its OrderLines and Payment `COD` / `PENDING`. | `confirmOrder` |
| 9 | System | Shows the confirmation with the order ID and total. | `viewConfirmation` |

## 6. Exceptions

| ID | At step | Condition | Result (message starts with) | Test |
|---|---|---|---|---|
| E-01 | 5, 7 | Not logged in | Redirect to `/login`; nothing written | `test_T_UC01_40`, `_41` |
| E-02 | 5, 7 | Logged in without role `CUSTOMER` | HTTP 403; nothing written | `test_T_UC01_42`, `_43` |
| E-03 | 5, 7 | No item has a quantity | "Your cart is empty" | `test_T_UC01_20_...[empty_cart]` |
| E-04 | 5, 7 | Quantity 0 or less | "Quantity for ... must be at least 1" | `[quantity_zero]`, `[quantity_negative]` |
| E-05 | 5, 7 | Quantity not a whole number or above 99 | "must be a whole number" / "must be at most 99" | `[quantity_not_a_number]`, `[quantity_too_large]` |
| E-06 | 5, 7 | Item sold out, not carried by the hub, or unknown | "Item N is not available at <hub name>" | `[item_sold_out_at_hub]`, `[item_not_sold_at_hub]`, `[item_does_not_exist]` |
| E-07 | 5, 7 | No address chosen | "Please choose a delivery address" | `[missing_address]` |
| E-08 | 5, 7 | Address belongs to another customer | "The selected delivery address is not valid" | `test_T_UC01_22` |
| E-09 | 7 | Same token submitted again | First order is shown; nothing new written | `test_T_UC01_30`, `_34` |
| E-10 | 7 | Token missing | "This order form has expired" | `test_T_UC01_23` |
| E-11 | 8 | Database error while saving | Transaction rolled back; nothing written | `test_T_UC01_13` |
| E-12 | 8 | A price, fee or item changed after the quote, so the re-priced total differs from the total the customer saw | New quote shown (HTTP 409), "The price changed since your quote"; nothing written until the customer confirms again | `test_T_UC01_50`, `_51` |

## 7. Traceability to the I1 acceptance criteria

| Criterion | Covered by |
|---|---|
| AC-2 seed | `tests/test_seed.py` |
| AC-3 quote | `tests/test_uc01_quote.py` |
| AC-4 one transaction | `tests/test_uc01_confirm.py` (`test_T_UC01_10` to `_13`) |
| AC-5 read back | `tests/test_uc01_confirm.py` (`test_T_UC01_14`) |
| AC-6 validation | `tests/test_uc01_validation.py` |
| AC-7 double submit | `tests/test_uc01_idempotency.py` |
| AC-8 login and role | `tests/test_uc01_access.py` |
| AC-9 same names | `tests/test_docs_consistency.py` |

## 8. Open points for review

- Closed in the review of 20/10: a price change between quote and confirm was saved without asking the customer (all 81 tests passed). Confirm now compares the totals and shows the new quote (E-12).
- Closed in the review of 20/10: the confirmation page lost the hub name once a hub was archived; history now reads archived hubs too (`test_T_UC01_52`).
- CSRF protection is not part of I1 (the stack has no form library); the idempotency token is not a CSRF token.
- The upper quantity limit of 99 is a team default, not a client rule.
