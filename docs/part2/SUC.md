# Supporting Use Case Contracts

Author: 722I0004 · AI-assisted (Codex)

These are analysis contracts for the nine supporting use cases. CRUD cells below identify the minimum actor-held paths in plan §2.4; they are planned scope, not evidence of implementation or lecturer approval. Strict CRUD coverage follows the team default D-4 while L1 remains unanswered. Any serving link names the main use case whose goal the supporting case helps; Figure 2.1 owns UML «include» or «extend» choices.

## SUC-01 — Log in / log out

Author: 722I0004 · AI-assisted (Codex)

- **Actor:** All human actors: Customer (Local or Tourist), Kitchen staff, Shipper, Admin and Manager.
- **Precondition:** For login, the person supplies credentials for an existing active account. For logout, an authenticated session exists.
- **Postconditions:** `SUC01-PC01` A valid login establishes the authenticated role context used for authorization. `SUC01-PC02` Logout invalidates the current session; an INACTIVE account is rejected on its next request.
- **Guards:** Credentials and active status are checked under plan §5.4; no role or actor identity is trusted from a posted actor ID.
- **CRUD cells held:** UserAccount — Read (SUC-01); no account-row write is performed by login or logout.
- **Main UC served:** UC-01–UC-06.
- **Failure:** Invalid credentials or an inactive account yields a controlled denial and no domain-row mutation; repeated logout does not change domain data.

## SUC-02 — Register (local or tourist), edit profile, manage addresses

Author: 722I0004 · AI-assisted (Codex)

- **Actor:** Customer, specialized as Local customer or Tourist customer.
- **Precondition:** Registration starts without an existing account for the new customer; profile and address changes require an authenticated session and target only that customer's records.
- **Postconditions:** `SUC02-PC01` Registration creates an ACTIVE UserAccount and the matching Local or Tourist Customer subtype with required fields. `SUC02-PC02` A valid profile edit updates only the customer's own details. `SUC02-PC03` An address can be added, read, updated or archived by its owner, while prior order address snapshots remain unchanged.
- **Guards:** BR-12: Local requires a Vietnamese mobile; Tourist requires passport number, nationality and email, with phone optional; an address may be labelled Hotel. BR-05 applies the address-distance rule at quote time. Passport details are visible only to that customer and Admin.
- **CRUD cells held:** UserAccount — Create/Read/Update; Customer — Create/Read/Update; Address — Create/Read/Update/Archive (SUC-02).
- **Main UC served:** UC-01.
- **Failure:** Invalid or incomplete subtype data, duplicate identity, or an address not owned by the actor is refused without changing another account or any existing order snapshot.

## SUC-03 — Track my orders, view receipt, answer a replacement offer

Author: 722I0004 · AI-assisted (Codex)

- **Actor:** Customer.
- **Precondition:** The customer is authenticated and requests an order they own. An offer answer additionally requires that exact offer to be OFFERED and its order to remain PLACED.
- **Postconditions:** `SUC03-PC01` The customer can read their own order status and history. `SUC03-PC02` The receipt shows the order ID/date, hub, address and line snapshots, S/D/F/Q/T, payment method/state and refund owed; ONLINE is labelled simulated. `SUC03-PC03` A valid acceptance applies the offered line and price, recalculates the total, and records any online refund owed without claiming payout. `SUC03-PC04` A decline rejects the order and applies BR-17. `SUC03-PC05` If the target is no longer valid, the offer becomes WITHDRAWN and the order remains unchanged.
- **Guards:** BR-12 and BR-13; replacement rules §3.3 clauses 4–8; BR-17 for unfulfilled outcomes. An answer cannot revive a cancelled or rejected order; stale/repeated answers do not mutate rows.
- **CRUD cells held:** Customer — Read own contact under SUC-03; Order — Read/Update own on an answer; OrderLine — Read and Update on accepted replacement; Payment — Read and Update amounts/refund owed on offer answer; ReplacementOffer — Read and Update to ACCEPTED/DECLINED; Delivery — Read own (SUC-03).
- **Main UC served:** UC-01; UC-05.
- **Failure:** Another customer's order, a non-open offer, a terminal order or a repeated answer is denied with no unauthorized or stale state change.

## SUC-04 — Cancel an order (PLACED or CONFIRMED)

Author: 722I0004 · AI-assisted (Codex)

- **Actor:** Customer.
- **Precondition:** The customer is authenticated, owns the order, and it is PLACED or CONFIRMED.
- **Postconditions:** `SUC04-PC01` The order becomes CANCELLED and any OFFERED replacement becomes WITHDRAWN. `SUC04-PC02` COD becomes VOIDED; ONLINE remains subject to BR-17 with the full captured amount C recorded as refund owed in REFUND_PENDING.
- **Guards:** BR-15 permits cancellation only from PLACED or CONFIRMED; BR-17 defines the payment result. Cancellation after PREPARING is refused.
- **CRUD cells held:** Order — Update to CANCELLED; Payment — Update state/refund amount; ReplacementOffer — Update to WITHDRAWN where open (SUC-04).
- **Main UC served:** UC-01.
- **Failure:** An order not owned by the actor or outside the permitted states is refused without changing the order, offer or payment.

## SUC-05 — Start preparing and mark ready

Author: 722I0004 · AI-assisted (Codex)

- **Actor:** Kitchen staff.
- **Precondition:** The order belongs to the actor's hub (BR-26). Starting requires CONFIRMED with no open offer; marking ready requires PREPARING.
- **Postconditions:** `SUC05-PC01` Starting preparation moves the own-hub order from CONFIRMED to PREPARING. `SUC05-PC02` Marking it ready moves the order to READY and creates one Delivery in AWAITING_PICKUP with the ready time.
- **Guards:** BR-26 and the no-open-offer rule in §3.3; each action requires its stated source state.
- **CRUD cells held:** Order — Read/Update own-hub to PREPARING/READY; Delivery — Create on mark-ready (SUC-05).
- **Main UC served:** UC-05; UC-02.
- **Failure:** Wrong hub, wrong source state or an open offer blocks the action with no state or delivery-row change.

## SUC-06 — Set menu availability at my hub

Author: 722I0004 · AI-assisted (Codex)

- **Actor:** Kitchen staff.
- **Precondition:** The actor is authenticated, assigned to the hub, and the target HubMenuItem listing exists for that hub.
- **Postconditions:** `SUC06-PC01` The listing's availability changes between AVAILABLE and SOLD_OUT for the actor's own hub; MenuItem master data and historical order-line snapshots are unaffected.
- **Guards:** BR-19 and BR-26; availability is per hub, not a global MenuItem state.
- **CRUD cells held:** HubMenuItem — Read/Update availability at the actor's hub (SUC-06).
- **Main UC served:** UC-05; UC-06.
- **Failure:** A missing listing, archived parent or different hub is refused without changing any listing.

## SUC-07 — Maintain vouchers

Author: 722I0004 · AI-assisted (Codex)

- **Actor:** Admin.
- **Precondition:** The actor has an authenticated Admin role. Creation or update supplies valid voucher fields.
- **Postconditions:** `SUC07-PC01` A voucher can be created, read and updated with its code, type, value, limits and validity dates. `SUC07-PC02` Archiving makes it unusable for a later quote while preserving prior order discount snapshots.
- **Guards:** BR-08: at most one voucher per order; FIXED or PERCENT discount limits, minimum subtotal, inclusive Vietnam-calendar validity dates and archived-voucher rejection. Validity is checked on demand; no scheduled expiry transition is implied.
- **CRUD cells held:** Voucher — Create/Read/Update/Archive (SUC-07).
- **Main UC served:** UC-01.
- **Failure:** Duplicate or invalid fields, an archived voucher, or a voucher outside its valid date window is refused for the request; prior orders are unchanged.

## SUC-08 — Maintain user accounts; deactivate/reactivate

Author: 722I0004 · AI-assisted (Codex)

- **Actor:** Admin.
- **Precondition:** The actor has an authenticated Admin role and the target account exists for an update or status change.
- **Postconditions:** `SUC08-PC01` Admin can create and update staff account details and role/hub assignment. `SUC08-PC02` An account may move between ACTIVE and INACTIVE; an inactive account is rejected at its next request. Admin can read permitted account details and linked Customer details.
- **Guards:** BR-12 limits passport visibility to the Customer and Admin. BR-25 prevents deactivating a shipper who holds a PICKED_UP delivery; BR-26 scopes kitchen work to the assigned hub.
- **CRUD cells held:** UserAccount — Create/Read/Update/Deactivate/Reactivate; Customer — Read and deactivate through the linked account only (SUC-08); the profile is preserved.
- **Main UC served:** UC-01–UC-06.
- **Failure:** Unauthorized fields, invalid role/hub, missing target, or a shipper with a PICKED_UP delivery is refused without changing the account.

## SUC-09 — Archive closed orders; read archived history

Author: 722I0004 · AI-assisted (Codex)

- **Actor:** Admin.
- **Precondition:** The actor has an authenticated Admin role. An order can be archived only after DELIVERED, DELIVERY_FAILED, REJECTED or CANCELLED.
- **Postconditions:** `SUC09-PC01` Archiving hides the terminal Order and its children from operational lists without physically deleting them. `SUC09-PC02` Admin can retrieve authorized archived history; receipts and reports continue to include the relevant snapshots and obligations.
- **Guards:** Terminal Order states; BR-24 keeps archived orders in reports. Archive is a lifecycle flag, not deletion of OrderLine, Payment, Delivery or ReplacementOffer history.
- **CRUD cells held:** Order — Read/Archive; OrderLine, Payment, Delivery and ReplacementOffer — Read/Archive through the parent Order (SUC-09).
- **Main UC served:** UC-04.
- **Failure:** An open order or unauthorized archive request is refused with the Order and its children unchanged.
