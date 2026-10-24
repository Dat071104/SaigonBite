# 2.3 Verifying Use Cases for Actor (CRUD)

Author: 722I0004 · AI-assisted (Codex)

These five actor tables implement the locked portfolio under the narrow root reconciliations below. The plan is unchanged. Cells name observable UC/SUC paths, not generic database privileges. An intentional blank grants no operation. All behavior remains an analysis contract; no running CRUD result is claimed before P4.

Scope restrictions apply to every cell: Customer reads/changes own records only; Kitchen staff work only at their hub (BR-26); Shipper sees delivery contact and the saved address snapshot and payment method/state/cash due only (BR-12/25), never passport details; Admin reads authorized account/history data. UserAccount Read SUC-01 in each actor table means own authentication/role context only, with credential verification internal: it grants neither an account-list endpoint nor access to password hashes. Address UC-02 is the saved Order address snapshot, not permission to edit or browse live addresses.

## 2.3.1 Verifying use cases for Customer

Author: 722I0004 · AI-assisted (Codex)

| Data entity / domain class | C R U D | Verified use case |
|---|---|---|
| Hub | Create | — (intentional blank) |
|  | Read / report | UC-01 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| Brand | Create | — (intentional blank) |
|  | Read / report | UC-01 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| MenuItem | Create | — (intentional blank) |
|  | Read / report | UC-01 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| HubMenuItem | Create | — (intentional blank) |
|  | Read / report | UC-01 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| UserAccount | Create | SUC-02 |
|  | Read / report | SUC-01; SUC-02 |
|  | Update | SUC-02 |
|  | Delete (or archive) | — (intentional blank) |
| Customer | Create | SUC-02 |
|  | Read / report | SUC-02; SUC-03 |
|  | Update | SUC-02 |
|  | Delete (or archive) | — (intentional blank) |
| Address | Create | SUC-02 |
|  | Read / report | SUC-02; UC-01 |
|  | Update | SUC-02 |
|  | Delete (or archive) | SUC-02 |
| Voucher | Create | — (intentional blank) |
|  | Read / report | UC-01 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| Order | Create | UC-01 |
|  | Read / report | SUC-03 |
|  | Update | SUC-03; SUC-04 |
|  | Delete (or archive) | — (intentional blank) |
| OrderLine | Create | UC-01 |
|  | Read / report | SUC-03 |
|  | Update | SUC-03 |
|  | Delete (or archive) | — (intentional blank) |
| Payment | Create | UC-01 |
|  | Read / report | SUC-03 |
|  | Update | SUC-03; SUC-04 |
|  | Delete (or archive) | — (intentional blank) |
| Delivery | Create | — (intentional blank) |
|  | Read / report | SUC-03 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| ReplacementOffer | Create | — (intentional blank) |
|  | Read / report | SUC-03 |
|  | Update | SUC-03; SUC-04 |
|  | Delete (or archive) | — (intentional blank) |

## 2.3.2 Verifying use cases for Kitchen staff

Author: 722I0004 · AI-assisted (Codex)

| Data entity / domain class | C R U D | Verified use case |
|---|---|---|
| MenuItem | Create | — (intentional blank) |
|  | Read / report | UC-05 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| HubMenuItem | Create | — (intentional blank) |
|  | Read / report | SUC-06; UC-05 |
|  | Update | SUC-06 |
|  | Delete (or archive) | — (intentional blank) |
| UserAccount | Create | — (intentional blank) |
|  | Read / report | SUC-01 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| Order | Create | — (intentional blank) |
|  | Read / report | SUC-05; UC-05 |
|  | Update | SUC-05; UC-05 |
|  | Delete (or archive) | — (intentional blank) |
| OrderLine | Create | — (intentional blank) |
|  | Read / report | UC-05 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| Payment | Create | — (intentional blank) |
|  | Read / report | — (intentional blank) |
|  | Update | UC-05 |
|  | Delete (or archive) | — (intentional blank) |
| Delivery | Create | SUC-05 |
|  | Read / report | — (intentional blank) |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| ReplacementOffer | Create | UC-05 |
|  | Read / report | UC-05 |
|  | Update | UC-05 |
|  | Delete (or archive) | — (intentional blank) |

## 2.3.3 Verifying use cases for Shipper

Author: 722I0004 · AI-assisted (Codex)

| Data entity / domain class | C R U D | Verified use case |
|---|---|---|
| UserAccount | Create | — (intentional blank) |
|  | Read / report | SUC-01 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| Customer | Create | — (intentional blank) |
|  | Read / report | UC-02 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| Address | Create | — (intentional blank) |
|  | Read / report | UC-02 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| Order | Create | — (intentional blank) |
|  | Read / report | UC-02 |
|  | Update | UC-02 |
|  | Delete (or archive) | — (intentional blank) |
| Payment | Create | — (intentional blank) |
|  | Read / report | UC-02 |
|  | Update | UC-02 |
|  | Delete (or archive) | — (intentional blank) |
| Delivery | Create | — (intentional blank) |
|  | Read / report | UC-02 |
|  | Update | UC-02 |
|  | Delete (or archive) | — (intentional blank) |

## 2.3.4 Verifying use cases for Admin

Author: 722I0004 · AI-assisted (Codex)

| Data entity / domain class | C R U D | Verified use case |
|---|---|---|
| Hub | Create | UC-03 |
|  | Read / report | UC-03 |
|  | Update | UC-03 |
|  | Delete (or archive) | UC-03 |
| Brand | Create | UC-06 |
|  | Read / report | UC-06 |
|  | Update | UC-06 |
|  | Delete (or archive) | UC-06 |
| MenuItem | Create | UC-06 |
|  | Read / report | UC-06 |
|  | Update | UC-06 |
|  | Delete (or archive) | UC-06 |
| HubMenuItem | Create | UC-06 |
|  | Read / report | UC-06 |
|  | Update | UC-06 |
|  | Delete (or archive) | UC-06 |
| UserAccount | Create | SUC-08 |
|  | Read / report | SUC-01; SUC-08 |
|  | Update | SUC-08 |
|  | Delete (or archive) | SUC-08 |
| Customer | Create | — (intentional blank) |
|  | Read / report | SUC-08 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | SUC-08 |
| Voucher | Create | SUC-07 |
|  | Read / report | SUC-07 |
|  | Update | SUC-07 |
|  | Delete (or archive) | SUC-07 |
| Order | Create | — (intentional blank) |
|  | Read / report | SUC-09 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | SUC-09 |
| OrderLine | Create | — (intentional blank) |
|  | Read / report | SUC-09 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | SUC-09 |
| Payment | Create | — (intentional blank) |
|  | Read / report | SUC-09 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | SUC-09 |
| Delivery | Create | — (intentional blank) |
|  | Read / report | SUC-09 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | SUC-09 |
| ReplacementOffer | Create | — (intentional blank) |
|  | Read / report | SUC-09 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | SUC-09 |

## 2.3.5 Verifying use cases for Manager

Author: 722I0004 · AI-assisted (Codex)

| Data entity / domain class | C R U D | Verified use case |
|---|---|---|
| Hub | Create | — (intentional blank) |
|  | Read / report | UC-04 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| UserAccount | Create | — (intentional blank) |
|  | Read / report | SUC-01 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| Order | Create | — (intentional blank) |
|  | Read / report | UC-04 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| OrderLine | Create | — (intentional blank) |
|  | Read / report | UC-04 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| Payment | Create | — (intentional blank) |
|  | Read / report | UC-04 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |
| Delivery | Create | — (intentional blank) |
|  | Read / report | UC-04 |
|  | Update | — (intentional blank) |
|  | Delete (or archive) | — (intentional blank) |

## Union and bidirectional verification

Author: 722I0004 · AI-assisted (Codex)

Every original §2.4 qualified C/R/U/D cell is held by at least one actor above. Every actor cell is in the reconciled union below. Literal omissions in the locked tables are retained as explicit plan issues, rather than claimed to be exact original equality. The six missing qualified reads found by D and the reverse-direction omissions are resolved only within existing UC/SUC scope.

| Persistent class | C | R | U | D / archive | Actors holding cells |
|---|---|---|---|---|---|
| Hub | UC-03 | UC-01; UC-03; UC-04 | UC-03 | UC-03 | Customer; Admin; Manager |
| Brand | UC-06 | UC-01; UC-06 | UC-06 | UC-06 | Customer; Admin |
| MenuItem | UC-06 | UC-01; UC-05; UC-06 | UC-06 | UC-06 | Customer; Kitchen staff; Admin |
| HubMenuItem | UC-06 | SUC-06; UC-01; UC-05; UC-06 | SUC-06; UC-06 | UC-06 | Customer; Kitchen staff; Admin |
| UserAccount | SUC-02; SUC-08 | SUC-01; SUC-02; SUC-08 | SUC-02; SUC-08 | SUC-08 | Customer; Kitchen staff; Shipper; Admin; Manager |
| Customer | SUC-02 | SUC-02; SUC-03; SUC-08; UC-02 | SUC-02 | SUC-08 | Customer; Shipper; Admin |
| Address | SUC-02 | SUC-02; UC-01; UC-02 | SUC-02 | SUC-02 | Customer; Shipper |
| Voucher | SUC-07 | SUC-07; UC-01 | SUC-07 | SUC-07 | Customer; Admin |
| Order | UC-01 | SUC-03; SUC-05; SUC-09; UC-02; UC-04; UC-05 | SUC-03; SUC-04; SUC-05; UC-02; UC-05 | SUC-09 | Customer; Kitchen staff; Shipper; Admin; Manager |
| OrderLine | UC-01 | SUC-03; SUC-09; UC-04; UC-05 | SUC-03 | SUC-09 | Customer; Kitchen staff; Admin; Manager |
| Payment | UC-01 | SUC-03; SUC-09; UC-02; UC-04 | SUC-03; SUC-04; UC-02; UC-05 | SUC-09 | Customer; Kitchen staff; Shipper; Admin; Manager |
| Delivery | SUC-05 | SUC-03; SUC-09; UC-02; UC-04 | UC-02 | SUC-09 | Customer; Kitchen staff; Shipper; Admin; Manager |
| ReplacementOffer | UC-05 | SUC-03; SUC-09; UC-05 | SUC-03; SUC-04; UC-05 | SUC-09 | Customer; Kitchen staff; Admin |

| Comparison | Result |
|---|---|
| Original §2.4 → reconciled actor tables | 0 missing qualified cells |
| Reconciled actor tables → reconciled union | 0 missing qualified cells (union derived from those tables) |
| Additional cells against literal §2.4 | Read-only cells listed below; no new create/update/archive grants |
| Persistent classes / schema tables | 13 / 13; mapping below |

### Root dispositions for literal plan differences

| Discrepancy | Accepted conservative reconciliation |
|---|---|
| UserAccount R SUC-01 lacks an actor assignment in §2.5 | Own authentication-context read for all five human actors, already the All actor scope of SUC-01; no general account read permission. |
| Customer R SUC-03; Address R UC-01 lack matching own-read actor qualifiers | Add only the owning Customer read while tracking / selecting their checkout address. |
| MenuItem R UC-05; HubMenuItem R UC-05 / SUC-06 lack kitchen qualifiers | Read only own-hub replacement candidates/listings; no master-data update. |
| Payment R UC-02 lacks shipper read cell | Read method/state/cash due for delivery under BR-25, without other customer-private data. |
| Admin Customer R is unqualified and absent from §2.4 | Qualify already listed authorized linked-account read as SUC-08. |
| Admin Order/children history R SUC-09 absent from §2.4 | Retain the reads already stated in §2.5 and §2.2 SUC-09, through authorized closed-order history only. |
| Kitchen Order R SUC-05 stated in §2.5 but omitted from §2.4 | Retain the own-hub read required to start/finish preparation; this reverse-direction omission was added by root. |

Added Read qualifiers against literal §2.4: Customer R SUC-08; Order R SUC-09; Order R SUC-05; OrderLine R SUC-09; Payment R SUC-09; Delivery R SUC-09; ReplacementOffer R SUC-09.

No locked plan cell was removed. Proposed owner clarification: add these qualifiers to the next approved plan revision; this phase records the discrepancy without editing the locked contract.

## Archive and persistence notes

An archived parent hides itself and its children from operational lists (boards, menus and checkout). Authorised history, receipts, reports and refund obligations still include them. Archive is an operational visibility rule, not physical child deletion or permission to erase snapshots. SUC-09 accepts only DELIVERED, DELIVERY_FAILED, REJECTED or CANCELLED orders. Customer deactivation is through the linked UserAccount; it does not erase the profile. HubMenuItem unlisting removes only that association row, and historical OrderLine snapshots survive. Seed rows are test setup, never a “Create”.

Not persisted: Quote, ReportFilter, report rows and receipt (computed views). No Shipper class/table: SHIPPER is a UserAccount role linked from Delivery.

## Schema table coverage (Static)

| SQL table | Persistent class |
|---|---|
| `hub` | Hub |
| `brand` | Brand |
| `menu_item` | MenuItem |
| `hub_menu_item` | HubMenuItem |
| `user_account` | UserAccount |
| `customer` | Customer |
| `address` | Address |
| `voucher` | Voucher |
| `orders` | Order |
| `order_line` | OrderLine |
| `payment` | Payment |
| `delivery` | Delivery |
| `replacement_offer` | ReplacementOffer |

All 13 schema tables are covered. Local/Tourist share Customer persistence. State/attribute differences and behavioral guards remain explicitly listed as P4 inputs; this table-coverage result does not qualify the app.
