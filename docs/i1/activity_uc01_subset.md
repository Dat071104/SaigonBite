> AI-assisted (Claude); reviewed and corrected by the team in October 2026.

# UC-01 Place an order - Iteration 1 subset: activity diagram

Owner: Dat (722I0004). Same steps and names as `uc01_subset_description.md` (main flow and exceptions E-01 to E-12).
The full UC-01 (busy hub, voucher, distance fee, online payment) is in Figure 1, Part A, of the proposal.

```mermaid
flowchart TD
    start((start)) --> login[Customer logs in]
    login --> role{role = CUSTOMER?}
    role -- no --> refuse[Show HTTP 403, nothing written] --> f1((end))
    role -- yes --> hubs[System lists active hubs: listHubs]
    hubs --> pick[Customer chooses a hub: selectHub]
    pick --> cart[Customer enters quantities and address: requestQuote]
    cart --> valid{cart, quantities, items and address valid?}
    valid -- no --> msg[Show the message, keep the form] --> cart
    valid -- yes --> quote[System shows subtotal, flat fee, total and a new token]
    quote --> conf[Customer confirms: confirmOrder]
    conf --> seen{token already used?}
    seen -- yes --> first[Show the first order] --> f2((end))
    seen -- no --> reprice{re-priced total = quoted total?}
    reprice -- no --> quote
    reprice -- yes --> save["One transaction: Order PLACED, OrderLines, Payment COD PENDING"]
    save --> show[Show confirmation with order ID and total: viewConfirmation]
    show --> f3((end))
```

Guards in the diagram match the server checks in `PlaceOrderController`; the loop back from "re-priced total"
is review finding C-01 (20/10).
