from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import Payment, PaymentMethod, PaymentState


class PaymentDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert(self, payment: Payment) -> int:
        cur = self.conn.execute(
            "INSERT INTO payment (order_id, method, state, amount, created_at) VALUES (?, ?, ?, ?, ?)",
            (payment.order_id, payment.method.value, payment.state.value, payment.amount,
             payment.created_at))
        return cur.lastrowid

    def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        r = self.conn.execute(
            "SELECT id, order_id, method, state, amount, created_at FROM payment WHERE order_id = ?",
            (order_id,)).fetchone()
        if r is None:
            return None
        return Payment(id=r["id"], order_id=r["order_id"], method=PaymentMethod(r["method"]),
                       state=PaymentState(r["state"]), amount=r["amount"], created_at=r["created_at"])
