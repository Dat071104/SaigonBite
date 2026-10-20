> AI-assisted (Claude); reviewed and corrected by the team in October 2026.

# Order state machine v1

State names are frozen (BRIEF) and are the values of `OrderState` in
`saigonbite/business/domain/enums.py` and the `orders.state` CHECK constraint in `db/schema.sql`.
The transitions are the table `ALLOWED_TRANSITIONS` in `saigonbite/business/domain/models.py`.
**In Iteration 1 only the initial state `PLACED` is created.** The other transitions are the planned ones.

```mermaid
stateDiagram-v2
    [*] --> PLACED : confirmOrder (UC-01)
    PLACED --> CONFIRMED : kitchen confirms
    PLACED --> REJECTED : kitchen rejects
    PLACED --> CANCELLED : customer cancels
    CONFIRMED --> CANCELLED : customer cancels
    CONFIRMED --> PREPARING : kitchen starts
    PREPARING --> READY : kitchen marks ready
    READY --> OUT_FOR_DELIVERY : shipper picks up
    OUT_FOR_DELIVERY --> DELIVERED : delivery succeeds
    OUT_FOR_DELIVERY --> DELIVERY_FAILED : delivery fails
    REJECTED --> [*]
    CANCELLED --> [*]
    DELIVERED --> [*]
    DELIVERY_FAILED --> [*]
```

## Transition table

| From | To | Trigger | Actor | Use case | Built in I1? |
|---|---|---|---|---|---|
| (start) | `PLACED` | Customer confirms a valid quote | Customer | UC-01 | Yes |
| `PLACED` | `CONFIRMED` | Kitchen confirms | Kitchen staff | UC-07 | No (I2) |
| `PLACED` | `REJECTED` | Kitchen rejects (for example an item ran out) | Kitchen staff | UC-07 | No (I2) |
| `PLACED` | `CANCELLED` | Customer cancels before cooking starts | Customer | Cancel order (analysed) | No |
| `CONFIRMED` | `CANCELLED` | Customer cancels before cooking starts | Customer | Cancel order (analysed) | No |
| `CONFIRMED` | `PREPARING` | Kitchen starts cooking | Kitchen staff | Kitchen board (UC-08, supporting) | No (I2) |
| `PREPARING` | `READY` | Kitchen marks ready | Kitchen staff | Kitchen board (UC-08, supporting) | No (I2) |
| `READY` | `OUT_FOR_DELIVERY` | Shipper picks up (Delivery becomes PICKED_UP) | Shipper | UC-02 | No (I3) |
| `OUT_FOR_DELIVERY` | `DELIVERED` | Shipper confirms hand-over | Shipper | UC-02 | No (I3) |
| `OUT_FOR_DELIVERY` | `DELIVERY_FAILED` | Shipper reports failure | Shipper | UC-02 | No (I3) |

`REJECTED`, `CANCELLED`, `DELIVERED` and `DELIVERY_FAILED` are final: no transition leaves them.
`Order.move_to()` raises `InvalidTransition` for any other pair (tests `test_T_DOM_02` to `_04`).

Cancellation rule (proposed default, client question 3): the customer may cancel while the order is `PLACED` or `CONFIRMED`, that is before the kitchen starts cooking (`PREPARING`). When cancellation is built, the check and the state change must run in one transaction so a cancel cannot race the kitchen starting the order.

## Active orders (workload)

The busy-hub rule from I2 counts orders in `ACTIVE_ORDER_STATES` = `PLACED`, `CONFIRMED`, `PREPARING` against `hub.max_active_orders` (assumption A-02). The constant exists in the domain; the rule is not enforced in I1.

## Payment states (separate from the order state)

`DELIVERED` (order) is not the same as `PAID` (payment). Payment states are the values of `PaymentState` and the `payment.state` CHECK constraint.

| Payment state | Meaning | Set by | Built in I1? |
|---|---|---|---|
| `PENDING` | Payment created, money not yet confirmed | UC-01 on confirm | Yes (COD) |
| `PAID` | COD: shipper confirmed the cash was collected | UC-02 | No |
| `FAILED` | Online payment failed | Online stub | No |
| `VOIDED` | COD order rejected, cancelled or failed: nothing to collect | UC-07, Cancel order, UC-02 | No |
| `REFUND_PENDING` | Online order rejected, cancelled or failed: the money is owed back by policy, no approval needed | UC-07, Cancel order, UC-02 | No |
| `REFUNDED` | The refund was paid (automatic refund, or a complaint refund approved by office staff) | Refund (deferred) | No |

Refund policy (proposed default, A-06 and client question 3): a rejected, cancelled or failed online order is refunded in full without a decision. Only a complaint goes to office staff; if they deny it, the payment stays `PAID` and the customer is told the reason.

Payment methods: `COD` (used in I1) and `ONLINE` (team-built stub from I3).
