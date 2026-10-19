"""PlaceOrderController: one method per system operation of UC-01 (docs/i1/ssd_uc01_subset.md).

    listHubs        -> list_hubs()
    selectHub       -> select_hub(user_id, hub_id)
    requestQuote    -> request_quote(user_id, hub_id, address_id, quantities)
    confirmOrder    -> confirm_order(user_id, hub_id, address_id, quantities, idempotency_token)
    viewConfirmation-> get_confirmation(user_id, order_id)

All rules are enforced here, on the server, whatever the browser sent.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping, Optional

from saigonbite.business.domain import (MAX_QUANTITY, Address, Customer, Hub, HubMenuItem, Order,
                                        OrderLine, Payment, PaymentMethod, PaymentState, Quote, Role)
from saigonbite.data_access import (CustomerDAO, HubDAO, OrderDAO, PaymentDAO, UserDAO,
                                    immediate_transaction)

from .errors import AuthorizationError, NotFoundError, ValidationError


@dataclass
class HubMenuView:
    hub: Hub
    menu: list[HubMenuItem]
    addresses: list[Address]


@dataclass
class OrderConfirmation:
    order: Order
    payment: Payment
    hub: Hub
    address: Address
    created: bool = True     # False when a repeated submit returned the existing order


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class PlaceOrderController:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.users = UserDAO(conn)
        self.customers = CustomerDAO(conn)
        self.hubs = HubDAO(conn)
        self.orders = OrderDAO(conn)
        self.payments = PaymentDAO(conn)

    # ---- system operations -------------------------------------------------------------

    def list_hubs(self) -> list[Hub]:
        return self.hubs.list_active()

    def select_hub(self, user_id: int, hub_id: int) -> HubMenuView:
        customer = self._require_customer(user_id)
        hub = self._require_hub(hub_id)
        return HubMenuView(hub=hub, menu=self.hubs.list_menu(hub.id),
                           addresses=self.customers.list_addresses(customer.id))

    def request_quote(self, user_id: int, hub_id: int, address_id: Optional[int],
                      quantities: Mapping[int, str]) -> Quote:
        """Price the cart (AC-3). Writes nothing."""
        customer = self._require_customer(user_id)
        return self._build_quote(customer, hub_id, address_id, quantities)

    def confirm_order(self, user_id: int, hub_id: int, address_id: Optional[int],
                      quantities: Mapping[int, str], idempotency_token: str) -> OrderConfirmation:
        """Create Order(PLACED) + OrderLines + Payment(COD, PENDING) in ONE transaction (AC-4).

        A repeated call with the same token returns the first order and writes nothing (AC-7).
        """
        customer = self._require_customer(user_id)
        token = (idempotency_token or "").strip()
        if not token:
            raise ValidationError("This order form has expired. Please start the order again.")

        with immediate_transaction(self.conn):
            existing = self.orders.get_by_token(token)
            if existing is not None:
                if existing.customer_id != customer.id:
                    raise AuthorizationError("This order belongs to another customer.")
                return self._confirmation(existing, created=False)

            # Re-validate and re-price inside the write lock: never trust the quote page.
            quote = self._build_quote(customer, hub_id, address_id, quantities)
            now = _now()
            order = Order.place(customer.id, quote, token, now)
            order.id = self.orders.insert(order)
            self.payments.insert(Payment(order_id=order.id, method=PaymentMethod.COD,
                                         state=PaymentState.PENDING, amount=order.total, created_at=now))
        return self._confirmation(self.orders.get_by_id(order.id), created=True)

    def get_confirmation(self, user_id: int, order_id: int) -> OrderConfirmation:
        customer = self._require_customer(user_id)
        order = self.orders.get_by_id(order_id)
        if order is None:
            raise NotFoundError("Order not found.")
        if order.customer_id != customer.id:
            raise AuthorizationError("This order belongs to another customer.")
        return self._confirmation(order, created=False)

    # ---- internals ---------------------------------------------------------------------

    def _require_customer(self, user_id: int) -> Customer:
        user = self.users.get_by_id(user_id)
        if user is None or not user.is_active or user.role is not Role.CUSTOMER:
            raise AuthorizationError("Only logged-in customers can place orders.")
        customer = self.customers.get_by_user_id(user.id)
        if customer is None:
            raise AuthorizationError("Only logged-in customers can place orders.")
        return customer

    def _require_hub(self, hub_id: int) -> Hub:
        hub = self.hubs.get(hub_id) if hub_id else None
        if hub is None:
            raise ValidationError("Please choose a hub.")
        return hub

    def _build_quote(self, customer: Customer, hub_id: int, address_id: Optional[int],
                     quantities: Mapping[int, str]) -> Quote:
        hub = self._require_hub(hub_id)

        lines: list[OrderLine] = []
        for menu_item_id, raw in quantities.items():
            raw = (raw or "").strip()
            if raw == "":
                continue                      # blank = item not ordered
            item = self.hubs.get_available_item(hub.id, menu_item_id)
            if item is None:
                raise ValidationError(f"Item {menu_item_id} is not available at {hub.name}.")
            try:
                qty = int(raw)
            except ValueError:
                raise ValidationError(f"Quantity for {item.name} must be a whole number.") from None
            if qty <= 0:
                raise ValidationError(f"Quantity for {item.name} must be at least 1.")
            if qty > MAX_QUANTITY:
                raise ValidationError(f"Quantity for {item.name} must be at most {MAX_QUANTITY}.")
            lines.append(OrderLine(menu_item_id=item.id, item_name=item.name,
                                   unit_price=item.price, quantity=qty))
        if not lines:
            raise ValidationError("Your cart is empty. Choose at least one item.")

        if not address_id:
            raise ValidationError("Please choose a delivery address.")
        address = self.customers.get_address(address_id, customer.id)
        if address is None:
            raise ValidationError("The selected delivery address is not valid.")

        return Quote(hub=hub, address=address, lines=lines)

    def _confirmation(self, order: Order, created: bool) -> OrderConfirmation:
        payment = self.payments.get_by_order_id(order.id)
        hub = self.hubs.get(order.hub_id)
        customer_addresses = self.customers.list_addresses(order.customer_id)
        address = next(a for a in customer_addresses if a.id == order.address_id)
        return OrderConfirmation(order=order, payment=payment, hub=hub, address=address, created=created)
