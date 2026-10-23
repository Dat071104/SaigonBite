"""Domain classes. Plain dataclasses: no SQL, no Flask.

Money is whole VND (int). Pricing (plan §0.1):
    item_subtotal = sum(unit_price * quantity)
    delivery_fee  = hub.base_delivery_fee + PER_KM_FEE * started km      (Q2)
    total         = item_subtotal - voucher_discount + delivery_fee - quiet_discount
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from . import rules
from .enums import (CustomerType, DeliveryState, DiscountType, OfferState, OnlineOption, OrderState,
                    PaymentMethod, PaymentState, Role)

MAX_QUANTITY = rules.MAX_QUANTITY
ACTIVE_ORDER_STATES = rules.ACTIVE_ORDER_STATES

# Order state machine (docs/part2/state_machines.md, Figure 1 of Part 1).
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

# Payment state machine. FAILED belongs to a declined online attempt, which never creates an order,
# so it is shown and logged but never stored. REFUNDED is the deferred payout (A-09).
PAYMENT_TRANSITIONS: dict[PaymentState, frozenset[PaymentState]] = {
    PaymentState.PENDING: frozenset({PaymentState.PAID, PaymentState.VOIDED}),
    PaymentState.PAID: frozenset({PaymentState.REFUND_PENDING}),
    PaymentState.REFUND_PENDING: frozenset({PaymentState.REFUNDED}),
    PaymentState.FAILED: frozenset(),
    PaymentState.VOIDED: frozenset(),
    PaymentState.REFUNDED: frozenset(),
}

# Delivery state machine (UC-02). A Delivery is created AWAITING_PICKUP when its order is READY.
DELIVERY_TRANSITIONS: dict[DeliveryState, frozenset[DeliveryState]] = {
    DeliveryState.AWAITING_PICKUP: frozenset({DeliveryState.PICKED_UP}),
    DeliveryState.PICKED_UP: frozenset({DeliveryState.DELIVERED, DeliveryState.FAILED}),
    DeliveryState.DELIVERED: frozenset(),
    DeliveryState.FAILED: frozenset(),
}

OFFER_TRANSITIONS: dict[OfferState, frozenset[OfferState]] = {
    OfferState.OFFERED: frozenset({OfferState.ACCEPTED, OfferState.DECLINED, OfferState.WITHDRAWN}),
    OfferState.ACCEPTED: frozenset(),
    OfferState.DECLINED: frozenset(),
    OfferState.WITHDRAWN: frozenset(),
}


class InvalidTransition(Exception):
    """Raised when an object is moved to a state its state machine does not allow."""


def _check_move(table: dict, current, new, what: str) -> None:
    if new not in table[current]:
        raise InvalidTransition(f"{what}: {current.value} -> {new.value} is not allowed")


@dataclass
class UserAccount:
    id: int
    username: str
    password_hash: str
    display_name: str
    role: Role
    is_active: bool = True
    hub_id: Optional[int] = None          # set for KITCHEN_STAFF only


@dataclass
class Customer:
    id: int
    user_id: int
    full_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    passport_no: Optional[str] = None
    nationality: Optional[str] = None
    customer_type = CustomerType.LOCAL  # class attribute, overridden by subclasses

    @property
    def online_options(self) -> tuple[OnlineOption, ...]:
        return rules.ONLINE_OPTIONS[self.customer_type]


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
    district: str
    latitude: float
    longitude: float
    archived_at: Optional[str] = None


@dataclass
class Hub:
    id: int
    code: str
    name: str
    address_text: str
    latitude: float
    longitude: float
    max_active_orders: int
    base_delivery_fee: int
    archived_at: Optional[str] = None

    def distance_to(self, address: Address) -> float:
        return rules.distance_km(self.latitude, self.longitude, address.latitude, address.longitude)


@dataclass
class HubStatus:
    """A hub with its current workload (derived, never stored)."""
    hub: Hub
    load: int

    @property
    def busy(self) -> bool:
        return rules.is_busy(self.load, self.hub.max_active_orders)

    @property
    def quiet(self) -> bool:
        return rules.is_quiet(self.load, self.hub.max_active_orders)

    @property
    def load_percent(self) -> int:
        return round(100 * self.load / self.hub.max_active_orders)


@dataclass
class Brand:
    id: int
    name: str
    archived_at: Optional[str] = None


@dataclass
class MenuItem:
    id: int
    brand_id: int
    brand_name: str
    name: str
    description: str
    price: int
    archived_at: Optional[str] = None


@dataclass
class HubMenuItem:
    hub_id: int
    item: MenuItem
    is_available: bool


@dataclass
class Voucher:
    id: int
    code: str
    description: str
    discount_type: DiscountType
    discount_value: int
    min_subtotal: int
    max_discount: Optional[int]
    valid_from: str            # ISO date, inclusive
    valid_until: str           # ISO date, inclusive
    archived_at: Optional[str] = None

    def problem(self, item_subtotal: int, today: str) -> Optional[str]:
        """Why this voucher cannot be used on an order today, or None."""
        if self.archived_at is not None:
            return f"Voucher {self.code} is no longer offered."
        if not (self.valid_from <= today <= self.valid_until):
            return f"Voucher {self.code} is not valid today."
        if item_subtotal < self.min_subtotal:
            return f"Voucher {self.code} needs dishes worth at least {self.min_subtotal:,} VND."
        return None

    def discount_for(self, item_subtotal: int) -> int:
        if self.discount_type is DiscountType.PERCENT:
            amount = item_subtotal * self.discount_value // 100
        else:
            amount = self.discount_value
        if self.max_discount is not None:
            amount = min(amount, self.max_discount)
        return min(amount, item_subtotal)


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
    """Price shown before the customer confirms. Not persisted."""
    hub: Hub
    address: Address
    lines: list[OrderLine]
    distance_km: float
    delivery_fee: int
    quiet_discount: int = 0
    voucher: Optional[Voucher] = None
    voucher_discount: int = 0

    @property
    def item_subtotal(self) -> int:
        return sum(line.line_total for line in self.lines)

    @property
    def total(self) -> int:
        return self.item_subtotal - self.voucher_discount + self.delivery_fee - self.quiet_discount


@dataclass
class Payment:
    order_id: int
    method: PaymentMethod
    state: PaymentState
    amount: int
    created_at: str
    updated_at: Optional[str] = None
    online_option: Optional[OnlineOption] = None
    provider_ref: Optional[str] = None
    refund_amount: int = 0
    id: Optional[int] = None

    def move_to(self, new_state: PaymentState) -> None:
        _check_move(PAYMENT_TRANSITIONS, self.state, new_state, f"Payment of order {self.order_id}")
        self.state = new_state

    def release_for_unfulfilled_order(self) -> None:
        """Rejection, cancellation or failed delivery (A-06): COD is voided, an online payment is owed back."""
        self.move_to(PaymentState.VOIDED if self.method is PaymentMethod.COD else PaymentState.REFUND_PENDING)


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
    delivery_address_text: str = ""
    distance_km: float = 0.0
    voucher_id: Optional[int] = None
    voucher_discount: int = 0
    quiet_discount: int = 0
    reject_reason: Optional[str] = None
    confirmed_at: Optional[str] = None
    ready_at: Optional[str] = None
    closed_at: Optional[str] = None

    @property
    def item_subtotal(self) -> int:
        return sum(line.line_total for line in self.lines)

    @property
    def total(self) -> int:
        return self.item_subtotal - self.voucher_discount + self.delivery_fee - self.quiet_discount

    @property
    def is_closed(self) -> bool:
        return self.state in rules.TERMINAL_ORDER_STATES

    @classmethod
    def place(cls, customer_id: int, quote: Quote, idempotency_token: str, placed_at: str) -> "Order":
        """Create a new order in state PLACED from an accepted quote."""
        return cls(customer_id=customer_id, hub_id=quote.hub.id, address_id=quote.address.id,
                   state=OrderState.PLACED, delivery_fee=quote.delivery_fee,
                   idempotency_token=idempotency_token, placed_at=placed_at,
                   delivery_address_text=quote.address.full_address, distance_km=quote.distance_km,
                   voucher_id=quote.voucher.id if quote.voucher else None,
                   voucher_discount=quote.voucher_discount, quiet_discount=quote.quiet_discount,
                   lines=[OrderLine(l.menu_item_id, l.item_name, l.unit_price, l.quantity)
                          for l in quote.lines])

    def can_move_to(self, new_state: OrderState) -> bool:
        return new_state in ALLOWED_TRANSITIONS[self.state]

    def move_to(self, new_state: OrderState) -> None:
        if not self.can_move_to(new_state):
            raise InvalidTransition(f"Order {self.id}: {self.state.value} -> {new_state.value} is not allowed")
        self.state = new_state

    def line(self, line_id: int) -> Optional[OrderLine]:
        return next((l for l in self.lines if l.id == line_id), None)

    def replace_line(self, line_id: int, menu_item_id: int, item_name: str, unit_price: int) -> None:
        """Apply an accepted replacement. The voucher discount agreed at checkout is kept,
        but never more than the new item subtotal, so the total can only stay the same or fall."""
        line = self.line(line_id)
        if line is None:
            raise ValueError(f"Order {self.id} has no line {line_id}")
        line.menu_item_id, line.item_name, line.unit_price = menu_item_id, item_name, unit_price
        self.voucher_discount = min(self.voucher_discount, self.item_subtotal)


@dataclass
class Delivery:
    order_id: int
    state: DeliveryState
    ready_at: str
    shipper_id: Optional[int] = None
    picked_up_at: Optional[str] = None
    finished_at: Optional[str] = None
    failure_reason: Optional[str] = None
    cash_collected: Optional[int] = None
    id: Optional[int] = None

    def move_to(self, new_state: DeliveryState) -> None:
        _check_move(DELIVERY_TRANSITIONS, self.state, new_state, f"Delivery of order {self.order_id}")
        self.state = new_state


@dataclass
class ReplacementOffer:
    order_id: int
    order_line_id: int
    original_item_name: str
    original_unit_price: int
    new_menu_item_id: int
    new_item_name: str
    new_unit_price: int
    state: OfferState
    offered_at: str
    decided_at: Optional[str] = None
    id: Optional[int] = None

    def move_to(self, new_state: OfferState) -> None:
        _check_move(OFFER_TRANSITIONS, self.state, new_state, f"Replacement offer {self.id}")
        self.state = new_state
