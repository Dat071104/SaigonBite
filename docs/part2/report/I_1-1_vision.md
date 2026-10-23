# 1.1 System Vision and Approval Record

Author: 722I0004 · AI-assisted (Codex)

## Problem Description

Orders reach SaigonBite's delivery kitchens through calls, Zalo and third-party apps, then staff copy them onto paper tickets. People outside a hub cannot see its queue. At lunch and dinner, one kitchen may accumulate orders while a nearby hub is underused. When a dish becomes unavailable, staff call customers to agree on a cancellation or replacement. Shippers are dispatched through individual calls or group chat, and end-of-day cash handovers can be difficult to reconcile. Tourists face registration and foreign-payment barriers; the menu is also Vietnamese-only. Staff apply discount codes by hand, managers handle complaint and refund cases one at a time, and management lacks dependable sales, workload and delivery-time reports.

## System Vision

The planned Part 2 release is one Online Food Delivery Hub Platform (OFDH) with shared order and operating records. It will give customers a reviewed quote and defined order path, give kitchen staff and shippers explicit decisions and delivery outcomes, let administrators maintain hubs and catalogue data, and let managers inspect operational reports. Local and tourist registration and payment choices are in scope; translating the Vietnamese-only menu is not.

## System Capabilities

The locked plan defines six main use cases and nine supporting use cases for this release.

| ID | Capability | Primary actor |
|---|---|---|
| UC-01 | PC01 one PLACED order owned by the customer; PC02 lines with snapshot names/prices; PC03 address snapshot + distance; PC04 S/D/F/Q/T stored and consistent; PC05 payment PENDING (COD) or PAID (ONLINE, amount C); PC06 hub load +1 | Customer |
| UC-02 | PC01 one shipper assigned, Delivery PICKED_UP, order OUT_FOR_DELIVERY; PC02 delivered: Delivery DELIVERED, order DELIVERED, COD PAID with cash = T; PC03 failed: Delivery FAILED + reason, order DELIVERY_FAILED, BR-17 | Shipper |
| UC-03 | PC01 hub created/updated with valid code, coordinates, fee, capacity; PC02 archived hub hidden from browse/checkout, visible in history/reports | Admin |
| UC-04 | PC01 sales, workload, performance equal the hand oracle for the filter; PC02 n/a on empty denominators | Manager |
| UC-05 | PC01 confirm: own-hub PLACED → CONFIRMED; PC02 reject: REJECTED + reason + BR-17 + offer WITHDRAWN; PC03 offer: one OFFERED offer per §3.3; PC04 accepted offer applied per §3.3 5–7 | Kitchen staff |
| UC-06 | PC01 brand/item created, updated, archived; PC02 listing added/removed, availability per hub; PC03 archived/sold-out items not orderable | Admin |
| SUC-01 | Log in / log out | All roles |
| SUC-02 | Register (local or tourist), edit profile, manage addresses | Customer |
| SUC-03 | Track my orders, view receipt, answer a replacement offer | Customer |
| SUC-04 | Cancel an order (PLACED or CONFIRMED) | Customer |
| SUC-05 | Start preparing and mark ready | Kitchen staff |
| SUC-06 | Set menu availability at my hub | Kitchen staff |
| SUC-07 | Maintain vouchers | Admin |
| SUC-08 | Maintain user accounts; deactivate/reactivate | Admin |
| SUC-09 | Archive closed orders; read archived history | Admin |

Online payment is simulated; this release uses no real payment provider or card data. Complaint decisions, refund payouts and ratings are deferred. The application records a refund obligation where the frozen rules require one, but it does not claim a payout.

## Business Benefits

These are expected effects of the planned capabilities, not measured results.

| Current problem | Capability used | Expected business benefit |
|---|---|---|
| Peak demand can overload one hub while another has spare capacity. | UC-01, UC-03 | A capacity check and quieter-hub option can reduce avoidable queue buildup. |
| Stock changes trigger after-order phone calls. | UC-05, UC-06, SUC-03, SUC-06 | Hub-specific availability and a recorded replacement decision make the customer's choice visible to the kitchen. |
| Shipper dispatch and cash handover rely on calls and notes. | UC-02 | Per-order pickup, delivery, COD and failure records give staff a common basis for cash reconciliation. |
| Tourists have difficulty with local registration and payment conventions. | SUC-02, UC-01 | Separate customer and payment paths provide a defined way to order, while the untranslated menu remains a limitation. |
| Voucher codes and order prices are applied manually. | UC-01, SUC-07 | A saved quote and voucher rule make the accepted total inspectable and repeatable. |
| Managers lack comparable sales, workload and delivery information. | UC-04, SUC-09 | Shared order records can support consistent operational reports, including authorised history. |
| Refund follow-up is handled case by case. | UC-01, UC-02, UC-05, SUC-03 | Recording payment state and the amount owed makes the obligation visible; complaint decisions and payout remain outside scope. |

## Approval Record

| Date / status | Source | Feedback or decision | Change made | Where recorded |
|---|---|---|---|---|
| 23/10/2026 | Team decision D-4 in the locked plan | Part 1 assumption A-08 limited supporting use cases to analysis; D-4 adopts minimal running create/read/update/archive paths for persistent classes. This is a team decision, not lecturer approval. | A-08 is superseded. Supporting use cases are in the release backlog and CRUD scope. | This section; report 1.3; later report section 2.3 |
| Status checked 23/10/2026; submitted dates unknown | Locked-plan record for client questions Q1–Q5 | The plan records all five as Submitted; answer and date cells are empty. No client response is recorded. | No answer-driven change is claimed. Defaults remain provisional until the 31/10 checkpoint. | docs/part2/decision_log.md; report 1.4.2 |
| 26/10/2026 — pending | Part 1 live presentation / lecturer feedback | ⟦PENDING: feedback 26/10⟧ | Record actual feedback and any resulting change after the presentation. Silence is not approval. | docs/part2/decision_log.md; update at the 31/10 checkpoint |
| Planned for 26/10/2026; not yet asked as of 23/10 | Course clarifications L1–L6 | No answers are available yet. These are course clarifications, separate from the five client questions. | Use locked-plan defaults until an answer is recorded; assess changes at the 31/10 checkpoint. | docs/part2/decision_log.md; report 1.4.2 |
