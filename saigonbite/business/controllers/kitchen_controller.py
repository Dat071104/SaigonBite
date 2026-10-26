"""KitchenController: everything kitchen staff do, always limited to the hub they work in.

    UC-05 Confirm or reject an incoming order:
        viewIncomingOrders -> board(user_id)
        viewOrder          -> get_order(user_id, order_id)
        confirmOrder       -> confirm_order(user_id, order_id)
        rejectOrder        -> reject_order(user_id, order_id, reason)
        offerReplacement   -> offer_replacement(user_id, order_id, order_line_id, new_menu_item_id)
    SUC-05 Prepare an order and mark it ready -> start_preparing(), mark_ready()
    SUC-06 Set menu item availability at my hub -> list_availability(), set_availability()
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from typing import Optional

from saigonbite.business.domain import (Delivery, DeliveryState, Hub, HubMenuItem, MenuItem, OfferState, Order,
                                        OrderState, Payment, ReplacementOffer, Role, UserAccount)
from saigonbite.data_access import (DeliveryDAO, HubDAO, MenuDAO, OrderDAO, PaymentDAO, ReplacementOfferDAO,
                                    immediate_transaction)

from .common import BaseController, move_order, release_payment
from .errors import AuthorizationError, ConflictError, NotFoundError, ValidationError

BOARD_STATES = (OrderState.PLACED, OrderState.CONFIRMED, OrderState.PREPARING, OrderState.READY)


@dataclass
class BoardEntry:
    order: Order
    awaiting_customer: bool          # an open replacement offer


@dataclass
class KitchenBoard:
    hub: Hub
    columns: dict[OrderState, list[BoardEntry]]


@dataclass
class KitchenOrderView:
    order: Order
    payment: Payment
    open_offer: Optional[ReplacementOffer]
    offers: list[ReplacementOffer]
    candidates: dict[int, list[MenuItem]] = field(default_factory=dict)   # line id -> possible replacements


class KitchenController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None):
        super().__init__(conn, clock)
        self.hubs = HubDAO(conn)
        self.menu = MenuDAO(conn)
        self.orders = OrderDAO(conn)
        self.payments = PaymentDAO(conn)
        self.deliveries = DeliveryDAO(conn)
        self.offers = ReplacementOfferDAO(conn)

    # ---- UC-05 -------------------------------------------------------------------------

    def board(self, user_id: int) -> KitchenBoard:
        staff = self._require_staff(user_id)
        hub = self.hubs.get_including_archived(staff.hub_id)
        columns = {state: [] for state in BOARD_STATES}
        for order in self.orders.list_for_hub(hub.id, BOARD_STATES):
            columns[order.state].append(BoardEntry(order, self.offers.get_open(order.id) is not None))
        return KitchenBoard(hub=hub, columns=columns)

    def get_order(self, user_id: int, order_id: int) -> KitchenOrderView:
        staff = self._require_staff(user_id)
        order = self._hub_order(staff, order_id)
        view = KitchenOrderView(order=order, payment=self.payments.get_by_order_id(order.id),
                                open_offer=self.offers.get_open(order.id),
                                offers=self.offers.list_for_order(order.id))
        if order.state is OrderState.PLACED and view.open_offer is None:
            in_order = {l.menu_item_id for l in order.lines}
            menu = [m.item for m in self.hubs.list_menu(order.hub_id) if m.is_available]
            for line in order.lines:
                view.candidates[line.id] = [i for i in menu
                                            if i.id not in in_order and i.price <= line.unit_price]
        return view

    def confirm_order(self, user_id: int, order_id: int) -> Order:
        staff = self._require_staff(user_id)
        with immediate_transaction(self.conn):
            order = self._hub_order(staff, order_id)
            if self.offers.get_open(order.id) is not None:
                raise ConflictError("The customer has not answered the replacement offer yet.")
            move_order(self.orders, order, OrderState.CONFIRMED, self._now())
        return order

    def reject_order(self, user_id: int, order_id: int, reason: str) -> Order:
        """A-06: COD is voided, an online payment becomes REFUND_PENDING. A reason is required."""
        staff = self._require_staff(user_id)
        reason = (reason or "").strip()
        if not reason:
            raise ValidationError("Please give the reason for rejecting the order.")
        if len(reason) > 200:
            raise ValidationError("The reason must be at most 200 characters.")
        with immediate_transaction(self.conn):
            order = self._hub_order(staff, order_id)
            now = self._now()
            move_order(self.orders, order, OrderState.REJECTED, now, reason)
            offer = self.offers.get_open(order.id)
            if offer is not None:
                if not self.offers.decide(offer.id, OfferState.WITHDRAWN, now):
                    raise ConflictError('The open offer changed. Please reload.')
            release_payment(self.payments, order.id, now)
        return order

    def offer_replacement(self, user_id: int, order_id: int, order_line_id: int,
                          new_menu_item_id: int) -> ReplacementOffer:
        """One open offer per order, while PLACED; same hub, available, equal or lower price (plan §0.1)."""
        staff = self._require_staff(user_id)
        with immediate_transaction(self.conn):
            order = self._hub_order(staff, order_id)
            if order.state is not OrderState.PLACED:
                raise ConflictError(f"Order {order.id} is {order.state.value}; a replacement can only be "
                                    "offered before the order is confirmed.")
            if self.offers.get_open(order.id) is not None:
                raise ConflictError("This order already has an open replacement offer.")
            line = order.line(order_line_id)
            if line is None:
                raise ValidationError("Choose a dish of this order to replace.")
            if self.hubs.get_available_item(order.hub_id, line.menu_item_id) is not None:
                raise ValidationError('A replacement requires a currently unavailable source dish.')
            item = self.hubs.get_available_item(order.hub_id, new_menu_item_id) if new_menu_item_id else None
            if item is None:
                raise ValidationError("The replacement must be a dish available at this hub.")
            if item.id in {l.menu_item_id for l in order.lines}:
                raise ValidationError(f"{item.name} is already in this order.")
            if item.price > line.unit_price:
                raise ValidationError(f"{item.name} costs more than {line.item_name}. "
                                      "Offer a dish at the same or a lower price.")
            offer = ReplacementOffer(order_id=order.id, order_line_id=line.id, original_item_name=line.item_name,
                                     original_unit_price=line.unit_price, new_menu_item_id=item.id,
                                     new_item_name=item.name, new_unit_price=item.price,
                                     state=OfferState.OFFERED, offered_at=self._now())
            offer.id = self.offers.insert(offer)
        return offer

    # ---- SUC-05 ------------------------------------------------------------------------

    def start_preparing(self, user_id: int, order_id: int) -> Order:
        staff = self._require_staff(user_id)
        with immediate_transaction(self.conn):
            order = self._hub_order(staff, order_id)
            if self.offers.get_open(order.id) is not None:
                raise ConflictError('The customer has not answered the open offer.')
            move_order(self.orders, order, OrderState.PREPARING, self._now())
        return order

    def mark_ready(self, user_id: int, order_id: int) -> Order:
        """PREPARING -> READY, and the Delivery is created AWAITING_PICKUP in the same transaction."""
        staff = self._require_staff(user_id)
        with immediate_transaction(self.conn):
            order = self._hub_order(staff, order_id)
            now = self._now()
            move_order(self.orders, order, OrderState.READY, now)
            self.deliveries.insert(Delivery(order_id=order.id, state=DeliveryState.AWAITING_PICKUP, ready_at=now))
        return order

    # ---- SUC-06 ------------------------------------------------------------------------

    def list_availability(self, user_id: int) -> tuple[Hub, list[HubMenuItem]]:
        staff = self._require_staff(user_id)
        return self.hubs.get_including_archived(staff.hub_id), self.hubs.list_menu(staff.hub_id)

    def set_availability(self, user_id: int, menu_item_id: int, available: bool) -> None:
        staff = self._require_staff(user_id)
        with immediate_transaction(self.conn):
            if type(available) is not bool:
                raise ValidationError('Availability must be true or false.')
            if not any(x.item.id == menu_item_id for x in self.hubs.list_menu(staff.hub_id)):
                raise NotFoundError('The active dish is not on your hub menu.')
            if not self.menu.set_available(staff.hub_id, menu_item_id, available):
                raise NotFoundError("This dish is not on your hub's menu.")

    # ---- internals ---------------------------------------------------------------------

    def _require_staff(self, user_id: int) -> UserAccount:
        return self._require_user(user_id, Role.KITCHEN_STAFF, message="Only kitchen staff can use the kitchen screens.")

    def _hub_order(self, staff: UserAccount, order_id: int) -> Order:
        order = self.orders.get_by_id(order_id)
        if order is None:
            raise NotFoundError("Order not found.")
        if order.hub_id != staff.hub_id:
            raise AuthorizationError("This order belongs to another hub.")
        return order
