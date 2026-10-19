from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import Order, OrderLine, OrderState

_ORDER_COLUMNS = ("id, customer_id, hub_id, address_id, state, delivery_fee, "
                  "idempotency_token, placed_at, archived_at")


class OrderDAO:
    """Order and OrderLine persistence. insert() must run inside the caller's transaction."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert(self, order: Order) -> int:
        """Insert the order header and all lines; return the new order id."""
        cur = self.conn.execute(
            "INSERT INTO orders (customer_id, hub_id, address_id, state, item_subtotal, delivery_fee, "
            "                    total_amount, idempotency_token, placed_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order.customer_id, order.hub_id, order.address_id, order.state.value,
             order.item_subtotal, order.delivery_fee, order.total,
             order.idempotency_token, order.placed_at))
        order_id = cur.lastrowid
        for line in order.lines:
            self.conn.execute(
                "INSERT INTO order_line (order_id, menu_item_id, item_name, unit_price, quantity) "
                "VALUES (?, ?, ?, ?, ?)",
                (order_id, line.menu_item_id, line.item_name, line.unit_price, line.quantity))
        return order_id

    def get_by_id(self, order_id: int) -> Optional[Order]:
        row = self.conn.execute(
            f"SELECT {_ORDER_COLUMNS} FROM orders WHERE id = ?", (order_id,)).fetchone()
        return self._load(row)

    def get_by_token(self, token: str) -> Optional[Order]:
        row = self.conn.execute(
            f"SELECT {_ORDER_COLUMNS} FROM orders WHERE idempotency_token = ?", (token,)).fetchone()
        return self._load(row)

    def _load(self, row: Optional[sqlite3.Row]) -> Optional[Order]:
        if row is None:
            return None
        line_rows = self.conn.execute(
            "SELECT id, menu_item_id, item_name, unit_price, quantity "
            "FROM order_line WHERE order_id = ? ORDER BY id", (row["id"],)).fetchall()
        return Order(id=row["id"], customer_id=row["customer_id"], hub_id=row["hub_id"],
                     address_id=row["address_id"], state=OrderState(row["state"]),
                     delivery_fee=row["delivery_fee"], idempotency_token=row["idempotency_token"],
                     placed_at=row["placed_at"], archived_at=row["archived_at"],
                     lines=[OrderLine(**dict(r)) for r in line_rows])
