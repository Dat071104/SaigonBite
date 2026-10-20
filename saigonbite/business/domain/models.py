"""Domain classes for Iteration 1. Plain dataclasses: no SQL, no Flask.

Money is whole VND (int). The pricing rule for I1 is:
    item_subtotal = sum(unit_price * quantity)
    delivery_fee  = hub.delivery_fee_flat      (flat seeded value, client question 2 is open)
    total         = item_subtotal + delivery_fee
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .enums import CustomerType, OrderState, PaymentMethod, PaymentState, Role

MAX_QUANTITY = 99

# Order state machine v1 (docs/i1/order_state_machine_v1.md). I1 only creates PLACED;
# the remaining transitions are the planned ones and are used from Iteration 2 on.
ALLOWED_TRANSITIONS: dict[OrderState, frozenset[OrderState]] = {
    OrderState.PLACED: frozenset({OrderState.CONFIRMED, OrderState.REJECTED, OrderState.CANCELLED}),
    OrderState.CONFIRMED: frozenset({OrderState.PREPARING, OrderState.CANCELLED}),
    OrderState.PREPARING: frozenset({OrderState.READY}),
    OrderState.READY: frozenset({OrderState.OUT_FOR_DELIVERY}),
    OrderState.OUT_FOR_DELIVERY: frozenset({OrderState.DELIVERED, OrderState.DELIVERY_FAILED}),
    OrderState.REJECTED: frozenset(),
    OrderState.DELIVERED: frozenset(),
    OrderState.DELIVERY_FAILED: frozenset(),
    OrderState.CANCELLED: frozenset(),
}

# Workload definition used by the busy-hub rule from Iteration 2 (assumption A-02).
ACTIVE_ORDER_STATES = (OrderState.PLACED, OrderState.CONFIRMED, OrderState.PREPARING)


class InvalidTransition(Exception):
    """Raised when an order is moved to a state the state machine does not allow."""


@dataclass
class UserAccount:
    id: int
    username: str
    password_hash: str
    display_name: str
    role: Role
    is_active: bool = True


@dataclass
class Customer:
    id: int
    user_id: int
    full_name: str
    phone: str
    customer_type = CustomerType.LOCAL  # class attribute, overridden by subclasses


class LocalCustomer(Customer):
    customer_type = CustomerType.LOCAL


class TouristCustomer(Customer):
    customer_type = CustomerType.TOURIST


def make_customer(customer_type: str, **fields) -> Customer:
    cls = TouristCustomer if CustomerType(customer_type) is CustomerType.TOURIST else LocalCustomer
    return cls(**fields)


@dataclass
class Address:
    id: int
    customer_id: int
    label: str
    full_address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class Hub:
    id: int
    code: str
    name: str
    address_text: str
    max_active_orders: int
    delivery_fee_flat: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    archived_at: Optional[str] = None


@dataclass
class MenuItem:
    id: int
    brand_id: int
    brand_name: str
    name: str
    description: str
    price: int


@dataclass
class HubMenuItem:
    hub_id: int
    item: MenuItem
    is_available: bool


@dataclass
class OrderLine:
    menu_item_id: int
    item_name: str
    unit_price: int
    quantity: int
    id: Optional[int] = None

    @property
    def line_total(self) -> int:
        return self.unit_price * self.quantity


@dataclass
class Quote:
    """Price shown before the customer confirms (AC-3). Not persisted."""
    hub: Hub
    address: Address
    lines: list[OrderLine]

    @property
    def item_subtotal(self) -> int:
        return sum(line.line_total for line in self.lines)

    @property
    def delivery_fee(self) -> int:
        return self.hub.delivery_fee_flat

    @property
    def total(self) -> int:
        return self.item_subtotal + self.delivery_fee


@dataclass
class Payment:
    order_id: int
    method: PaymentMethod
    state: PaymentState
    amount: int
    created_at: str
    id: Optional[int] = None


@dataclass
class Order:
    customer_id: int
    hub_id: int
    address_id: int
    state: OrderState
    delivery_fee: int
    idempotency_token: str
    placed_at: str
    lines: list[OrderLine] = field(default_factory=list)
    id: Optional[int] = None
    archived_at: Optional[str] = None

    @property
    def item_subtotal(self) -> int:
        return sum(line.line_total for line in self.lines)

    @property
    def total(self) -> int:
        return self.item_subtotal + self.delivery_fee

    @classmethod
    def place(cls, customer_id: int, quote: Quote, idempotency_token: str, placed_at: str) -> "Order":
        """Create a new order in state PLACED from an accepted quote."""
        return cls(customer_id=customer_id, hub_id=quote.hub.id, address_id=quote.address.id,
                   state=OrderState.PLACED, delivery_fee=quote.delivery_fee,
                   idempotency_token=idempotency_token, placed_at=placed_at,
                   lines=[OrderLine(l.menu_item_id, l.item_name, l.unit_price, l.quantity)
                          for l in quote.lines])

    def can_move_to(self, new_state: OrderState) -> bool:
        return new_state in ALLOWED_TRANSITIONS[self.state]

    def move_to(self, new_state: OrderState) -> None:
        if not self.can_move_to(new_state):
            raise InvalidTransition(f"Order {self.id}: {self.state.value} -> {new_state.value} is not allowed")
        self.state = new_state
