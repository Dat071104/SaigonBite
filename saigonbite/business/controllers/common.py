"""Shared controller support: the clock, the role check and the order/payment steps that several
use cases share (A-06: rejection, cancellation and failed delivery release the payment the same way)."""
from __future__ import annotations

import sqlite3
from datetime import date, datetime, time, timedelta, timezone
from typing import Callable, Optional

from saigonbite.business.domain import InvalidTransition, Order, OrderState, Payment, Role, UserAccount
from saigonbite.data_access import OrderDAO, PaymentDAO, UserDAO

from .errors import AuthorizationError, ConflictError

VN_TZ = timezone(timedelta(hours=7))


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def vn_day_start_utc(day: date) -> str:
    """00:00 of a Ho Chi Minh City calendar day, as a stored UTC timestamp (17:00 of the day before)."""
    return datetime.combine(day, time(0, 0), tzinfo=VN_TZ).astimezone(timezone.utc).isoformat(timespec="seconds")


class BaseController:
    def __init__(self, conn: sqlite3.Connection, clock: Optional[Callable[[], datetime]] = None):
        self.conn = conn
        self.clock = clock or utc_now
        self.users = UserDAO(conn)

    def _now(self) -> str:
        """Stored timestamp format: ISO-8601 UTC, seconds."""
        return self.clock().astimezone(timezone.utc).isoformat(timespec="seconds")

    def _today_vn(self) -> str:
        return self.clock().astimezone(VN_TZ).date().isoformat()

    def _require_user(self, user_id: int, *roles: Role, message: str = "Your account cannot do this.") -> UserAccount:
        user = self.users.get_by_id(user_id) if user_id else None
        if user is None or not user.is_active or user.role not in roles:
            raise AuthorizationError(message)
        return user


def move_order(orders: OrderDAO, order: Order, to_state: OrderState, now: str,
               reject_reason: Optional[str] = None) -> None:
    """Check the step on the Order state machine, then write it only if nobody moved the order first."""
    from_state = order.state
    try:
        order.move_to(to_state)
    except InvalidTransition:
        raise ConflictError(f"Order {order.id} is {from_state.value}, so it cannot become "
                            f"{to_state.value}. Nothing was changed.") from None
    if not orders.change_state(order.id, from_state, to_state, now, reject_reason):
        raise ConflictError(f"Order {order.id} was changed by someone else. Nothing was changed; please reload.")


def release_payment(payments: PaymentDAO, order_id: int, now: str) -> Payment:
    """A-06: COD becomes VOIDED, a paid online payment becomes REFUND_PENDING (owed back in full)."""
    payment = payments.get_by_order_id(order_id)
    from_state = payment.state
    try:
        payment.release_for_unfulfilled_order()
    except InvalidTransition:
        raise ConflictError(f"The payment of order {order_id} is {from_state.value}. Nothing was changed.") from None
    if not payments.change_state(order_id, from_state, payment.state, now):
        raise ConflictError(f"The payment of order {order_id} was changed by someone else. Please reload.")
    if not payments.set_amounts(order_id, payment.amount, payment.refund_amount, now):
        raise ConflictError('The payment amounts changed before saving. Please reload.')
    return payment
