"""PlaceOrderController (UC-01 Place an order): one method per system operation of the SSD.

    listHubs         -> list_hubs()
    selectHub        -> select_hub(user_id, hub_id)
    requestQuote     -> request_quote(user_id, hub_id, address_id, quantities, voucher_code)
    confirmOrder     -> confirm_order(user_id, hub_id, address_id, quantities, idempotency_token,
                                      quoted_total, voucher_code, payment)
    viewConfirmation -> get_confirmation(user_id, order_id)

All rules are enforced here, on the server, whatever the browser sent.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Mapping, Optional

from saigonbite.business.domain import (MAX_QUANTITY, Address, Customer, Hub, HubMenuItem, HubStatus,
                                        OnlineOption, Order, OrderLine, Payment, PaymentMethod, PaymentState,
                                        Quote, Role, rules)
from saigonbite.data_access import (CustomerDAO, HubDAO, OrderDAO, PaymentDAO, PaymentGatewaySimulator,
                                    VoucherDAO, immediate_transaction)

from .common import BaseController
from .errors import (AuthorizationError, HubUnavailableError, NotFoundError, PaymentDeclinedError,
                     QuoteChangedError, ValidationError)


@dataclass
class HubMenuView:
    hub: Hub
    status: HubStatus
    menu: list[HubMenuItem]
    addresses: list[Address]


@dataclass
class OrderConfirmation:
    order: Order
    payment: Payment
    hub: Hub
    created: bool = True     # False when a repeated submit returned the existing order


@dataclass
class PaymentChoice:
    """How the customer pays. outcome is the payment simulator's answer (APPROVE or DECLINE) for ONLINE."""
    method: PaymentMethod = PaymentMethod.COD
    option: Optional[OnlineOption] = None
    outcome: Optional[str] = None


class PlaceOrderController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None, gateway: Optional[PaymentGatewaySimulator] = None):
        super().__init__(conn, clock)
        self.customers = CustomerDAO(conn)
        self.hubs = HubDAO(conn)
        self.orders = OrderDAO(conn)
        self.payments = PaymentDAO(conn)
        self.vouchers = VoucherDAO(conn)
        self.gateway = gateway or PaymentGatewaySimulator()

    # ---- system operations -------------------------------------------------------------

    def list_hubs(self) -> list[HubStatus]:
        loads = self.hubs.active_loads()
        return [HubStatus(hub, loads.get(hub.id, 0)) for hub in self.hubs.list_active()]

    def select_hub(self, user_id: int, hub_id: int) -> HubMenuView:
        customer = self._require_customer(user_id)
        hub = self._require_hub(hub_id)
        return HubMenuView(hub=hub, status=HubStatus(hub, self.hubs.active_load(hub.id)),
                           menu=self.hubs.list_menu(hub.id),
                           addresses=self.customers.list_addresses(customer.id))

    def payment_options(self, user_id: int) -> tuple[OnlineOption, ...]:
        """Q4: the online options this customer's type may use (cash on delivery is always offered)."""
        return self._require_customer(user_id).online_options

    def request_quote(self, user_id: int, hub_id: int, address_id: Optional[int],
                      quantities: Mapping[int, str], voucher_code: Optional[str] = None,
                      payment: Optional[PaymentChoice] = None) -> Quote:
        """Price the cart. Writes nothing."""
        customer = self._require_customer(user_id)
        self._check_payment_choice(customer, payment or PaymentChoice())
        return self._build_quote(customer, hub_id, address_id, quantities, voucher_code)

    def confirm_order(self, user_id: int, hub_id: int, address_id: Optional[int],
                      quantities: Mapping[int, str], idempotency_token: str,
                      quoted_total: Optional[int] = None, voucher_code: Optional[str] = None,
                      payment: Optional[PaymentChoice] = None,
                      quote_fingerprint: Optional[str] = None) -> OrderConfirmation:
        """Create Order(PLACED) + OrderLines + Payment in ONE transaction.

        Payment is COD PENDING, or ONLINE PAID when the simulator approved it (A-06: the money is taken
        when the order is saved; a failed save releases the authorisation).
        A repeated call with the same token returns the first order and writes nothing.
        The capacity rule is checked again inside the write lock, so two customers cannot both take
        the last slot of a hub (R-03).
        quoted_total is the total the customer saw on the quote page. It is only compared, never
        used as a price: if it is missing or the re-priced total differs, no order is written and
        QuoteChangedError carries the current quote for the customer to confirm.
        """
        customer = self._require_customer(user_id)
        token = (idempotency_token or "").strip()
        if not token:
            raise ValidationError("This order form has expired. Please start the order again.")
        payment = payment or PaymentChoice()
        reference = None
        try:
            with immediate_transaction(self.conn):
                customer = self._require_customer(user_id)
                existing = self.orders.get_by_token(token)
                if existing is not None:
                    if existing.customer_id != customer.id:
                        raise AuthorizationError("This order belongs to another customer.")
                    return self._confirmation(existing, created=False)
                self._check_payment_choice(customer, payment)
                quote = self._build_quote(customer, hub_id, address_id, quantities, voucher_code)
                if quoted_total is None or not quote_fingerprint:
                    raise QuoteChangedError(quote, QuoteChangedError.MISSING)
                if quoted_total != quote.total or quote_fingerprint != quote.fingerprint(payment.method,payment.option):
                    raise QuoteChangedError(quote)
                if payment.method is PaymentMethod.ONLINE:
                    auth = self.gateway.authorise(quote.total, payment.option, payment.outcome)
                    if not auth.approved:
                        raise PaymentDeclinedError(quote, f"{auth.message} No order was placed. Try again or choose cash on delivery.")
                    reference = auth.reference
                now = self._now()
                order = Order.place(customer.id, quote, token, now)
                order.id = self.orders.insert(order)
                self.payments.insert(Payment(
                    order_id=order.id, method=payment.method, online_option=payment.option,
                    provider_ref=reference, amount=order.total, created_at=now,
                    state=PaymentState.PAID if payment.method is PaymentMethod.ONLINE else PaymentState.PENDING))
        except BaseException:
            if reference:
                self.gateway.release(reference)
            raise
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
        user = self._require_user(user_id, Role.CUSTOMER, message="Only logged-in customers can place orders.")
        customer = self.customers.get_by_user_id(user.id)
        if customer is None:
            raise AuthorizationError("Only logged-in customers can place orders.")
        return customer

    def _require_hub(self, hub_id: int) -> Hub:
        hub = self.hubs.get(hub_id) if hub_id else None
        if hub is None:
            raise ValidationError("Please choose a hub.")
        return hub

    @staticmethod
    def _check_payment_choice(customer: Customer, payment: PaymentChoice) -> None:
        if not isinstance(payment.method, PaymentMethod):
            raise ValidationError('Please choose a valid payment method.')
        if payment.method is PaymentMethod.COD:
            if payment.option is not None:
                raise ValidationError('Cash on delivery has no online option.')
            return
        if payment.option not in customer.online_options:
            allowed = ", ".join(o.value.replace("_", " ").lower() for o in customer.online_options)
            raise ValidationError(f"This payment option is not offered to your account. You can pay by {allowed} "
                                  "or cash on delivery.")

    def suggest_hubs(self, exclude_hub_id: int, address: Optional[Address]) -> list[HubStatus]:
        """Other active hubs that are not busy and can reach the address, quietest first."""
        options = []
        for status in self.list_hubs():
            if status.hub.id == exclude_hub_id or status.busy:
                continue
            if address is not None and status.hub.distance_to(address) > rules.MAX_DELIVERY_KM:
                continue
            options.append(status)
        options.sort(key=lambda s: (s.load / s.hub.max_active_orders,
                                   s.hub.distance_to(address) if address is not None else 0, s.hub.id))
        return options[:rules.MAX_SUGGESTIONS]

    def _build_quote(self, customer: Customer, hub_id: int, address_id: Optional[int],
                     quantities: Mapping[int, str], voucher_code: Optional[str]) -> Quote:
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

        km = hub.distance_to(address)
        if km > rules.MAX_DELIVERY_KM:
            raise HubUnavailableError(
                f"{address.label} is {km} km from {hub.name}. We deliver up to {rules.MAX_DELIVERY_KM:g} km.",
                self.suggest_hubs(hub.id, address))
        load = self.hubs.active_load(hub.id)
        if rules.is_busy(load, hub.max_active_orders):
            raise HubUnavailableError(f"{hub.name} is too busy to take new orders right now.",
                                      self.suggest_hubs(hub.id, address))

        quote = Quote(hub=hub, address=address, lines=lines, distance_km=km,
                      delivery_fee=rules.delivery_fee(hub.base_delivery_fee, km))
        quote.quiet_discount = rules.quiet_discount(load, hub.max_active_orders, quote.delivery_fee)

        code = (voucher_code or "").strip()
        if code:
            voucher = self.vouchers.get_by_code(code)
            if voucher is None:
                raise ValidationError(f"Voucher {code} does not exist.")
            problem = voucher.problem(quote.item_subtotal, self._today_vn())
            if problem:
                raise ValidationError(problem)
            quote.voucher, quote.voucher_discount = voucher, voucher.discount_for(quote.item_subtotal)
        return quote

    def _confirmation(self, order: Order, created: bool) -> OrderConfirmation:
        return OrderConfirmation(order=order, payment=self.payments.get_by_order_id(order.id),
                                 hub=self.hubs.get_including_archived(order.hub_id), created=created)
