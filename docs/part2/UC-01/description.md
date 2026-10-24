# UC-01 — Place an order with an accepted full price, voucher and payment choice (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

| Item | Content |
|---|---|
| Use case name | UC-01 — Place an order with an accepted full price, voucher and payment choice. Author: 722I0004 · AI-assisted (Codex) |
| Scenario / trigger | A Customer chooses a hub and dishes and requests a full quote, then submits explicit consent to its content and total. The goal ends with a durable PLACED order or a controlled outcome; receipt and cancellation are supporting follow-up paths. |
| Actors | Primary: Customer, specialized as Local customer or Tourist customer. Payment simulator supports the optional simulated ONLINE payment subgoal. The simulator is local/deterministic; no real provider or card data. |
| Related use cases | Figure 2.1A: UC-01 «include» Validate accepted checkout (mandatory); Simulate online payment «extend» UC-01 at **payment authorization**, guard ONLINE. SUC-04 «extend» SUC-03 at **order action selected**, guard customer requests cancellation and state PLACED or CONFIRMED. SUC-01 authentication, SUC-02 profile/addresses, SUC-03 tracking/receipt, SUC-07 vouchers and UC-03/UC-06 maintained data serve this goal; those serving links do not assert additional include/extend relations. UC-05 handles later kitchen decisions. |
| Stakeholders and interests | Customer: an explicit, accurate full price, own-order privacy, one order per token and clear refund-owed wording. Kitchen: capacity not oversold. Operator: atomic snapshots and payment facts with no partial order. Local and Tourist customers: valid type-specific payment choices. |
| Pre-conditions | An active authenticated Customer session exists (SUC-01), with a valid Local/Tourist profile (BR-12) and an own active address available through SUC-02. Hubs, menus and vouchers may change; eligibility, ownership and capacity are request-time guards, not assumed preconditions. |
| Post-conditions | **UC01-PC01** one PLACED order owned by the customer<br>**UC01-PC02** lines with snapshot names/prices<br>**UC01-PC03** address snapshot + distance<br>**UC01-PC04** S/D/F/Q/T stored and consistent<br>**UC01-PC05** payment PENDING (COD) or PAID (ONLINE, amount C)<br>**UC01-PC06** hub load +1<br>**UC01-MG01** refused/declined/invalid → no order, no payment, no line<br>**UC01-MG02** replay → same single order<br>**UC01-MG03** busy → suggestions, nothing saved<br>PC01–PC06 describe the successful checkout boundary; later supported lifecycle changes do not assert that a cancelled order remains PLACED. MG01 concerns the refused attempt; previously saved orders are retained. |
| Flow of activities | Numbered Actor / System main flow and A01–A05 / E01–E05 below form this field. Steps 1–8 achieve the goal. Step 9 links a read-only receipt; follow-up F01 is SUC-03/SUC-04. |
| Exception conditions | E01 identity/input/menu/radius/voucher/payment refusal; E02 busy capacity; E03 fingerprint or total changed; E04 simulator decline; E05 transaction/commit failure. Each branch below states its point of departure and rejoin/end and the applicable MG. No failed attempt leaves a saved Order, Payment or OrderLine. |

## Flow of activities — main success (COD)

| Actor | System |
|---|---|
| 1. Customer requests `browseHubs()`. | Returns `activeHubsWithLoadAndCapacity`: ACTIVE hubs with BR-01 load (PLACED, CONFIRMED, PREPARING), capacity and derived busy/quiet labels. No writes. |
| 2. Selects a hub using `selectHub(hubId)`. | Returns `availableMenuAndOwnAddresses`; exposes only active brand/item listings AVAILABLE at that hub and own addresses. No writes. |
| 3. Chooses own address, nonempty item/quantity lines, zero or one voucher and COD; submits `requestQuote(hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?)`. | Validates active actor/address ownership, hub/item/listing eligibility, positive quantities and payment choice. Uses raw Haversine district-centroid distance for d ≤ 8.0 and the fee, rounding only display/storage after the check (BR-05–07). Rechecks load/capacity; validates voucher dates inclusively in Vietnam and its limits. Returns `quoteWithFingerprintAndSDFQT`, or E01/E02. |
| 4. Reviews and accepts the full quoted content and total. | Shows approximate distance and fee rule; S, D, F, Q and T=S−D+F−Q. D is FIXED or floor(percent×S/100), subject to minimum, max discount and S; 0≤D≤S. Quiet load before insertion gives Q=min(5,000,F) when load <25% capacity; otherwise Q=0. The full fingerprint covers hub, address, item/quantity/unit price, voucher code+D, F, Q, payment method/option. No quote row is stored. |
| 5. Submits `confirmCheckout(hubId, addressId, lines(itemId, quantity), voucherCode?, paymentMethod, onlineOption?, simulatorOutcome?, quoteFingerprint, quotedTotal, checkoutToken)`. | Begins the short checkout transaction and revalidates active session/role; token is distinct from CSRF. Checks token ownership inside that same atomic boundary: same customer returns the existing order (A01), another customer is denied without disclosure (E01). |
| 6. Waits for the result; no further interaction is required. | **Validate accepted checkout**: continuing the same short write transaction from step 5, rechecks all step-3 guards and capacity, recomputes content fingerprint and T from trusted current facts and compares both to consent (BR-02/10). Busy → E02; invalid → E01; changed → E03. COD needs no simulator authorization. |
| 7. — | Creates exactly one customer-owned PLACED Order, ≥1 OrderLine with snapshot names/prices/quantities, address snapshot+checked distance, S/D/F/Q/T, voucher reference and unique token; exactly one COD PENDING Payment with payable=T. Commits as one unit. PLACED enters hub load (+1). ONLINE uses A02. Any failure through COMMIT uses E05. |
| 8. Receives confirmation. | Returns `placedOrderAndReceipt` only after commit (UC01-PC01–PC06). A replay returns `existingOrder` without another write. |
| 9. Requests `viewReceipt(orderId)` through SUC-03. | Returns `ownOrderReceipt` (read only): order ID/date/hub, address and line snapshots, S/D/F/Q/T, method/option, payment state and refund owed; ONLINE explicitly says “Simulated payment”. Foreign-order requests use E01 without disclosure or mutation. |

## Alternate flows

| ID | Branch point | Actor / System behaviour | Rejoin / end |
|---|---|---|---|
| A01 | Step 5, token already belongs to this customer | System returns the same single existing order and its authorized receipt; does not rerun authorization or insert any row. | Rejoin 8 with `existingOrder`; UC01-MG02. |
| A02 | Step 3/4, Customer chooses ONLINE | Local chooses E_WALLET or BANK_QR; Tourist chooses INTERNATIONAL_CARD. The labelled simulator page collects approve/decline **before** step 6's transaction. At step 6 after validation, Simulate online payment extends at payment authorization: the short deterministic in-process decision runs inside the transaction. Approval creates ONLINE PAID with captured amount C=T alongside all step-7 writes; decline uses E04. No network/provider call or user wait holds the transaction. | Rejoin 7 then 8; UC01-PC05. |
| A03 | E02 busySuggestions result | System gives up to 3 other ACTIVE, non-busy hubs within raw radius, ordered by load ratio, distance, ID; explicitly says menus may differ and a new quote is needed. Empty suggestion list is shown. Customer may select another hub and request a fresh quote or stop. | Rejoin 2 then 3 for a new attempt, or end; refused attempt UC01-MG03 and MG01. |
| A04 | E03 revisedQuote or E04 decline | Customer may accept the revised full fingerprint+T, change basket/voucher/payment, retry ONLINE or choose COD. Any changed choice requires another `requestQuote(...)`; approval choice precedes a new checkout transaction. | Rejoin 3/4 before another 5, or end; failed attempt UC01-MG01. |
| A05 | Step 2, no eligible item/address or no active hub at 1 | Customer uses SUC-02 to maintain an address or ends; menu/catalogue administration remains separate. Browse/selection itself writes zero rows. | Rejoin 1/2 after support or end; no checkout save, UC01-MG01. |

## Exception flows and minimum guarantees

| ID | Branch point and guard | System response | Rejoin / end |
|---|---|---|---|
| E01 | Steps 2,3,5,6: inactive/wrong role, missing/foreign address, invalid quantity, archived/unlisted/sold-out item, d>8.0 raw, invalid voucher or payment option, invalid token; step 9 foreign order | Controlled refusal; does not expose another customer's order, passport or address. Existing orders are retained; this attempt saves no Order/Payment/OrderLine. Queries never write. | End refused attempt: UC01-MG01. Input correction may start again at 2/3. |
| E02 | Step 3 or 6: load ≥ capacity (including a race for the last slot) | Returns `busySuggestions`; nothing saved; no new payment capture. Follows A03 only on a fresh attempt. | End busy attempt: UC01-MG03 and MG01. |
| E03 | Step 6: full fingerprint differs **or** T differs (including same-total content changes) | Returns `revisedQuote`; nothing saved and no authorization retained. Never trusts posted prices. | End changed-consent attempt: UC01-MG01; A04 may rejoin 3/4. |
| E04 | A02 inside step 6: simulator declines | Returns refusal and explains “No order was placed”; no persisted FAILED Payment. | End declined attempt: UC01-MG01; A04 permits a fresh attempt. |
| E05 | Steps 6–7: lock failure, write failure or COMMIT failure | Controlled retry message; rolls back all order/line/payment writes and releases any simulated authorization, including a failure at COMMIT. Nothing saved; no success receipt. | End failed attempt: UC01-MG01. A fresh request/replay still enforces BR-11. |

## F01 — supported follow-up (SUC-03 / SUC-04)

From step 8/9 the Customer may call `viewMyOrders()` to read `ownOrdersAndOpenOffers` and `viewReceipt(orderId)` to read the current authorized receipt. From SUC-03's **order action selected** extension point, `cancelOrder(orderId)` is permitted for own PLACED/CONFIRMED only: Order→CANCELLED, open offer→WITHDRAWN, COD→VOIDED or ONLINE→REFUND_PENDING with refund_amount=C, saved together (BR-15/17). After a prior partial refund owed, the owed amount becomes C, never C+partial. Returns `cancelledOrderAndAmounts`; wrong owner/state or stale repeated cancellation returns refusal with zero lifecycle rows changed under SUC-04's own failure invariant. UC01-MG01 remains a checkout-attempt guarantee; it does not erase a previously saved Order. This supporting path has its own scope and cannot be used to revive an order. Replacement answers use UC-05's SUC-03 companion, not a second checkout.

Source: locked plan §§2–5/P2.3; BR-01–19; Figure 2.1A relations; operation catalogue OP-01, OP-07, OP-13–17. All numeric rules are team defaults pending Q/L answers; this is analysis, not tested application behaviour.
