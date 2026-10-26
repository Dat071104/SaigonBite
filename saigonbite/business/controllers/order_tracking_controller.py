"""OrderTrackingController: the customer's side after checkout.

    SUC-03 Track my orders       -> list_my_orders(user_id), get_order(user_id, order_id)
    SUC-03 Answer a replacement  -> answer_replacement(user_id, order_id, offer_id, accept)   (UC-05 consent)
    SUC-04 Cancel an order       -> cancel_order(user_id, order_id)
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional

from saigonbite.business.domain import (Customer, Delivery, Hub, OfferState, Order, OrderState, Payment,
                                        PaymentMethod, ReplacementOffer, Role)
from saigonbite.data_access import (CustomerDAO, DeliveryDAO, HubDAO, OrderDAO, PaymentDAO, ReplacementOfferDAO,
                                    immediate_transaction)

from .common import BaseController, move_order, release_payment
from .errors import AuthorizationError, ConflictError, NotFoundError

DECLINED_REASON = "The customer declined the replacement."


@dataclass
class OrderDetail:
    order: Order
    payment: Payment
    hub: Hub
    delivery: Optional[Delivery]
    open_offer: Optional[ReplacementOffer]
    offers: list[ReplacementOffer]
    notice: Optional[str] = None  # Ephemeral result message, never a stored withdrawal-reason column.

    @property
    def can_cancel(self) -> bool:
        return self.order.can_move_to(OrderState.CANCELLED)

    @property
    def total_if_accepted(self) -> Optional[int]:
        """The new total the customer sees before accepting (the quote's price-consent rule)."""
        if self.open_offer is None:
            return None
        line = self.order.line(self.open_offer.order_line_id)
        saving = line.quantity * (self.open_offer.original_unit_price - self.open_offer.new_unit_price)
        new_subtotal = self.order.item_subtotal - saving
        voucher = min(self.order.voucher_discount, new_subtotal)
        return new_subtotal - voucher + self.order.delivery_fee - self.order.quiet_discount


@dataclass
class OrderSummary:
    order: Order
    hub_name: str
    awaiting_answer: bool


class OrderTrackingController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None):
        super().__init__(conn, clock)
        self.customers = CustomerDAO(conn)
        self.orders = OrderDAO(conn)
        self.payments = PaymentDAO(conn)
        self.hubs = HubDAO(conn)
        self.deliveries = DeliveryDAO(conn)
        self.offers = ReplacementOfferDAO(conn)

    def list_my_orders(self, user_id: int) -> list[OrderSummary]:
        customer = self._require_customer(user_id)
        return [OrderSummary(o, self.hubs.get_including_archived(o.hub_id).name,
                             self.offers.get_open(o.id) is not None)
                for o in self.orders.list_for_customer(customer.id)]

    def get_order(self, user_id: int, order_id: int) -> OrderDetail:
        customer = self._require_customer(user_id)
        return self._detail(self._own_order(customer, order_id))

    def answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail:
        """Accept: the line takes the new dish and price, totals are recomputed; COD owes the new total,
        ONLINE records the difference as refund owed (payment stays PAID).
        Decline: the order is REJECTED and the payment released (A-06)."""
        customer = self._require_customer(user_id)
        notice = None
        with immediate_transaction(self.conn):
            order = self._own_order(customer, order_id)
            offer = self.offers.get_open(order.id)
            if order.state is not OrderState.PLACED or offer is None or offer.id != offer_id:
                raise ConflictError("This replacement offer is no longer open. Nothing was changed.")
            now = self._now()
            target_valid = self.hubs.get_available_item(order.hub_id,offer.new_menu_item_id) is not None
            if accept and not target_valid:
                if not self.offers.decide(offer.id,OfferState.WITHDRAWN,now):
                    raise ConflictError('The offer changed. Please reload.')
                notice = 'The replacement is no longer available. The offer was withdrawn; your order and payment are unchanged.'
            elif accept:
                order.replace_line(offer.order_line_id, offer.new_menu_item_id, offer.new_item_name,
                                   offer.new_unit_price)
                if not self.orders.save_lines_and_totals(order):
                    raise ConflictError('The order lines changed. Please reload.')
                payment = self.payments.get_by_order_id(order.id)
                if payment.method is PaymentMethod.COD:
                    saved = self.payments.set_amounts(order.id, order.total, 0, now)
                else:
                    saved = self.payments.set_amounts(order.id, payment.amount, payment.amount - order.total, now)
                if not saved or not self.offers.decide(offer.id, OfferState.ACCEPTED, now):
                    raise ConflictError('The payment or offer changed. Please reload.')
            else:
                if not self.offers.decide(offer.id, OfferState.DECLINED, now):
                    raise ConflictError('The offer changed. Please reload.')
                move_order(self.orders, order, OrderState.REJECTED, now, DECLINED_REASON)
                release_payment(self.payments, order.id, now)
        result = self.get_order(user_id, order_id)
        result.notice = notice
        return result

    def cancel_order(self, user_id: int, order_id: int) -> OrderDetail:
        """Q3: allowed while PLACED or CONFIRMED (before cooking). An open offer is withdrawn."""
        customer = self._require_customer(user_id)
        with immediate_transaction(self.conn):
            order = self._own_order(customer, order_id)
            now = self._now()
            move_order(self.orders, order, OrderState.CANCELLED, now)
            offer = self.offers.get_open(order.id)
            if offer is not None:
                if not self.offers.decide(offer.id, OfferState.WITHDRAWN, now):
                    raise ConflictError('The offer changed. Please reload.')
            release_payment(self.payments, order.id, now)
        return self.get_order(user_id, order_id)

    # ---- internals ---------------------------------------------------------------------

    def _require_customer(self, user_id: int) -> Customer:
        user = self._require_user(user_id, Role.CUSTOMER, message="Only customers can see their orders here.")
        customer = self.customers.get_by_user_id(user.id)
        if customer is None:
            raise AuthorizationError("Only customers can see their orders here.")
        return customer

    def _own_order(self, customer: Customer, order_id: int) -> Order:
        order = self.orders.get_by_id(order_id)
        if order is None:
            raise NotFoundError("Order not found.")
        if order.customer_id != customer.id:
            raise AuthorizationError("This order belongs to another customer.")
        return order

    def _detail(self, order: Order) -> OrderDetail:
        return OrderDetail(order=order, payment=self.payments.get_by_order_id(order.id),
                           hub=self.hubs.get_including_archived(order.hub_id),
                           delivery=self.deliveries.get_by_order_id(order.id),
                           open_offer=self.offers.get_open(order.id),
                           offers=self.offers.list_for_order(order.id))
