from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import OnlineOption, Payment, PaymentMethod, PaymentState


class PaymentDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert(self, payment: Payment) -> int:
        cur = self.conn.execute(
            "INSERT INTO payment (order_id, method, online_option, provider_ref, state, amount, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (payment.order_id, payment.method.value,
             payment.online_option.value if payment.online_option else None, payment.provider_ref,
             payment.state.value, payment.amount, payment.created_at, payment.updated_at or payment.created_at))
        return cur.lastrowid

    def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        r = self.conn.execute(
            "SELECT id, order_id, method, online_option, provider_ref, state, amount, refund_amount, "
            "       created_at, updated_at FROM payment WHERE order_id = ?", (order_id,)).fetchone()
        if r is None:
            return None
        return Payment(id=r["id"], order_id=r["order_id"], method=PaymentMethod(r["method"]),
                       state=PaymentState(r["state"]), amount=r["amount"], created_at=r["created_at"],
                       updated_at=r["updated_at"], refund_amount=r["refund_amount"], provider_ref=r["provider_ref"],
                       online_option=OnlineOption(r["online_option"]) if r["online_option"] else None)

    def change_state(self, order_id: int, from_state: PaymentState, to_state: PaymentState, now: str) -> bool:
        cur = self.conn.execute(
            "UPDATE payment SET state = ?, updated_at = ? WHERE order_id = ? AND state = ?",
            (to_state.value, now, order_id, from_state.value))
        return cur.rowcount == 1

    def set_amounts(self, order_id: int, amount: int, refund_amount: int, now: str) -> None:
        """After an accepted replacement: COD follows the new total; ONLINE records the difference owed."""
        self.conn.execute("UPDATE payment SET amount = ?, refund_amount = ?, updated_at = ? WHERE order_id = ?",
                          (amount, refund_amount, now, order_id))
