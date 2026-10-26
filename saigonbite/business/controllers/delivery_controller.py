"""DeliveryController (UC-02 Deliver an order): one method per system operation of the SSD.

    viewReadyOrders   -> board(user_id)
    viewDelivery      -> get_delivery(user_id, order_id)
    pickUpOrder       -> pick_up(user_id, order_id)
    confirmDelivered  -> confirm_delivered(user_id, order_id, cash_collected)
    reportFailure     -> report_failure(user_id, order_id, reason)

Delivery, Order and Payment change together in one transaction:
    pick up    Delivery PICKED_UP   Order OUT_FOR_DELIVERY
    delivered  Delivery DELIVERED   Order DELIVERED         COD Payment PAID (online stays PAID)
    failed     Delivery FAILED      Order DELIVERY_FAILED   COD VOIDED / online REFUND_PENDING
"""
from __future__ import annotations

import sqlite3
import re
from dataclasses import dataclass
from typing import Optional

from saigonbite.business.domain import (Customer, Delivery, DeliveryState, Hub, Order, OrderState, Payment,
                                        PaymentMethod, PaymentState, Role, UserAccount)
from saigonbite.data_access import (CustomerDAO, DeliveryDAO, HubDAO, OrderDAO, PaymentDAO,
                                    immediate_transaction)

from .common import BaseController, move_order, release_payment
from .errors import AuthorizationError, ConflictError, NotFoundError, ValidationError


@dataclass
class DeliveryView:
    delivery: Delivery
    order: Order
    payment: Payment
    hub: Hub
    customer: Customer

    @property
    def cash_to_collect(self) -> int:
        """COD: the full order total. Online: nothing, the customer has already paid."""
        return self.payment.amount if self.payment.method is PaymentMethod.COD else 0


@dataclass
class ShipperBoard:
    waiting: list[DeliveryView]       # READY orders nobody has taken yet
    mine: list[DeliveryView]          # picked up by me, not finished
    finished: list[DeliveryView]      # my recent deliveries


class DeliveryController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None):
        super().__init__(conn, clock)
        self.deliveries = DeliveryDAO(conn)
        self.orders = OrderDAO(conn)
        self.payments = PaymentDAO(conn)
        self.hubs = HubDAO(conn)
        self.customers = CustomerDAO(conn)

    def board(self, user_id: int) -> ShipperBoard:
        shipper = self._require_shipper(user_id)
        finished = (self.deliveries.list_for_shipper(shipper.id, DeliveryState.DELIVERED)
                    + self.deliveries.list_for_shipper(shipper.id, DeliveryState.FAILED))
        finished.sort(key=lambda d: d.finished_at or "", reverse=True)
        return ShipperBoard(waiting=[self._view(d) for d in self.deliveries.list_awaiting_pickup()],
                            mine=[self._view(d) for d in self.deliveries.list_for_shipper(shipper.id,
                                                                                         DeliveryState.PICKED_UP)],
                            finished=[self._view(d) for d in finished[:10]])

    def get_delivery(self, user_id: int, order_id: int) -> DeliveryView:
        shipper = self._require_shipper(user_id)
        delivery = self._delivery(order_id)
        if delivery.shipper_id not in (None, shipper.id):
            raise AuthorizationError("Another shipper is delivering this order.")
        return self._view(delivery)

    def pick_up(self, user_id: int, order_id: int) -> DeliveryView:
        """Atomic: when two shippers press Pick up together, only the first one gets the order."""
        shipper = self._require_shipper(user_id)
        with immediate_transaction(self.conn):
            delivery = self._delivery(order_id)
            if delivery.state is not DeliveryState.AWAITING_PICKUP or delivery.shipper_id is not None:
                raise ConflictError(f"Order {order_id} has already been picked up. Nothing was changed.")
            now = self._now()
            if not self.deliveries.take(order_id, shipper.id, now):
                raise ConflictError(f"Order {order_id} has already been picked up. Nothing was changed.")
            move_order(self.orders, self.orders.get_by_id(order_id), OrderState.OUT_FOR_DELIVERY, now)
        return self.get_delivery(user_id, order_id)

    def confirm_delivered(self, user_id: int, order_id: int, cash_collected: Optional[str]) -> DeliveryView:
        """COD: the cash entered must equal the order total, and the payment becomes PAID once.
        Online: no cash is taken (the field must be empty or 0)."""
        shipper = self._require_shipper(user_id)
        with immediate_transaction(self.conn):
            delivery = self._own_active_delivery(shipper, order_id)
            payment = self.payments.get_by_order_id(order_id)
            order = self.orders.get_by_id(order_id)
            cash = self._parse_cash(cash_collected)
            now = self._now()
            if payment.method is PaymentMethod.COD:
                if cash != order.total or payment.amount != order.total:
                    raise ValidationError(f"Collect exactly {payment.amount:,} VND in cash and enter that amount.")
                payment.move_to(PaymentState.PAID)
                if not self.payments.change_state(order_id, PaymentState.PENDING, PaymentState.PAID, now):
                    raise ConflictError("The payment was already recorded. Nothing was changed.")
            else:
                if payment.state is not PaymentState.PAID:
                    raise ConflictError('The online payment is not in a fulfilled-payment state.')
                if cash not in (None, 0):
                    raise ValidationError("This order was paid online. Do not take cash from the customer.")
                cash = None
            delivery.move_to(DeliveryState.DELIVERED)
            if not self.deliveries.finish(order_id, shipper.id, DeliveryState.DELIVERED, now, cash_collected=cash):
                raise ConflictError("This delivery was already finished. Nothing was changed.")
            move_order(self.orders, self.orders.get_by_id(order_id), OrderState.DELIVERED, now)
        return self.get_delivery(user_id, order_id)

    def report_failure(self, user_id: int, order_id: int, reason: str) -> DeliveryView:
        shipper = self._require_shipper(user_id)
        reason = (reason or "").strip()
        if not reason:
            raise ValidationError("Please say why the delivery failed.")
        if len(reason) > 200:
            raise ValidationError("The reason must be at most 200 characters.")
        with immediate_transaction(self.conn):
            delivery = self._own_active_delivery(shipper, order_id)
            now = self._now()
            delivery.move_to(DeliveryState.FAILED)
            if not self.deliveries.finish(order_id, shipper.id, DeliveryState.FAILED, now, failure_reason=reason):
                raise ConflictError("This delivery was already finished. Nothing was changed.")
            move_order(self.orders, self.orders.get_by_id(order_id), OrderState.DELIVERY_FAILED, now)
            release_payment(self.payments, order_id, now)
        return self.get_delivery(user_id, order_id)

    # ---- internals ---------------------------------------------------------------------

    def _require_shipper(self, user_id: int) -> UserAccount:
        return self._require_user(user_id, Role.SHIPPER, message="Only shippers can use the delivery screens.")

    def _delivery(self, order_id: int) -> Delivery:
        delivery = self.deliveries.get_by_order_id(order_id)
        if delivery is None:
            raise NotFoundError("There is no delivery for this order. It may not be ready yet.")
        return delivery

    def _own_active_delivery(self, shipper: UserAccount, order_id: int) -> Delivery:
        delivery = self._delivery(order_id)
        if delivery.shipper_id != shipper.id:
            raise AuthorizationError("Only the shipper who picked up this order can finish it.")
        if delivery.state is not DeliveryState.PICKED_UP:
            raise ConflictError(f"This delivery is already {delivery.state.value}. Nothing was changed.")
        if self.orders.get_by_id(order_id).state is not OrderState.OUT_FOR_DELIVERY:
            raise ConflictError('The order is no longer out for delivery. Nothing was changed.')
        return delivery

    @staticmethod
    def _parse_cash(raw: Optional[str]) -> Optional[int]:
        raw = (raw or "").strip()
        if raw == "":
            return None
        if not re.fullmatch(r'(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+|[0-9]{1,3}(?:\.[0-9]{3})+)',raw):
            raise ValidationError('Enter a nonnegative whole VND amount, with optional thousands separators.')
        raw = raw.replace(',', '').replace('.', '')
        try:
            value = int(raw)
        except ValueError:
            raise ValidationError("Enter the cash amount as a whole number of VND.") from None
        if value < 0:
            raise ValidationError("The cash amount cannot be negative.")
        return value

    def _view(self, delivery: Delivery) -> DeliveryView:
        order = self.orders.get_by_id(delivery.order_id)
        return DeliveryView(delivery=delivery, order=order, payment=self.payments.get_by_order_id(order.id),
                            hub=self.hubs.get_including_archived(order.hub_id),
                            customer=self.customers.get(order.customer_id))
