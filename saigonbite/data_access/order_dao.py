from __future__ import annotations

import sqlite3
from typing import Iterable, Optional

from saigonbite.business.domain import Order, OrderLine, OrderState, rules

_ORDER_COLUMNS = ("id, customer_id, hub_id, address_id, state, delivery_fee, idempotency_token, placed_at, "
                  "archived_at, delivery_address_text, distance_km, voucher_id, voucher_discount, quiet_discount, "
                  "reject_reason, confirmed_at, ready_at, closed_at")
_TERMINAL = ", ".join(f"'{s.value}'" for s in rules.TERMINAL_ORDER_STATES)


class OrderDAO:
    """Order and OrderLine persistence. Writes must run inside the caller's transaction."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert(self, order: Order) -> int:
        """Insert the order header and all lines; return the new order id."""
        cur = self.conn.execute(
            "INSERT INTO orders (customer_id, hub_id, address_id, delivery_address_text, distance_km, state, "
            "                    item_subtotal, voucher_id, voucher_discount, delivery_fee, quiet_discount, "
            "                    total_amount, idempotency_token, placed_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order.customer_id, order.hub_id, order.address_id, order.delivery_address_text, order.distance_km,
             order.state.value, order.item_subtotal, order.voucher_id, order.voucher_discount, order.delivery_fee,
             order.quiet_discount, order.total, order.idempotency_token, order.placed_at))
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

    def list_for_customer(self, customer_id: int) -> list[Order]:
        rows = self.conn.execute(
            f"SELECT {_ORDER_COLUMNS} FROM orders WHERE customer_id = ? AND archived_at IS NULL "
            "ORDER BY placed_at DESC, id DESC", (customer_id,)).fetchall()
        return [self._load(r) for r in rows]

    def list_for_hub(self, hub_id: int, states: Iterable[OrderState]) -> list[Order]:
        states = list(states)
        marks = ", ".join("?" for _ in states)
        rows = self.conn.execute(
            f"SELECT {_ORDER_COLUMNS} FROM orders WHERE hub_id = ? AND state IN ({marks}) AND archived_at IS NULL "
            "ORDER BY placed_at, id", (hub_id, *[s.value for s in states])).fetchall()
        return [self._load(r) for r in rows]

    def change_state(self, order_id: int, from_state: OrderState, to_state: OrderState, now: str,
                     reject_reason: Optional[str] = None) -> bool:
        """Move the order only if it is still in from_state (a repeat or a race changes nothing).

        Records the time of the step: confirmed_at, ready_at, or closed_at for a final state.
        """
        stamps = {OrderState.CONFIRMED: "confirmed_at", OrderState.READY: "ready_at"}
        column = "closed_at" if to_state in rules.TERMINAL_ORDER_STATES else stamps.get(to_state)
        sets = "state = ?, reject_reason = COALESCE(?, reject_reason)" + (f", {column} = ?" if column else "")
        params = [to_state.value, reject_reason] + ([now] if column else []) + [order_id, from_state.value]
        cur = self.conn.execute(f"UPDATE orders SET {sets} WHERE id = ? AND state = ?", params)
        return cur.rowcount == 1

    def save_lines_and_totals(self, order: Order) -> bool:
        """Persist an accepted replacement: the changed lines and the recomputed totals."""
        for line in order.lines:
            cur = self.conn.execute(
                "UPDATE order_line SET menu_item_id = ?, item_name = ?, unit_price = ? WHERE id = ? AND order_id = ?",
                (line.menu_item_id, line.item_name, line.unit_price, line.id, order.id))
            if cur.rowcount != 1:
                return False
        cur = self.conn.execute(
            "UPDATE orders SET item_subtotal = ?, voucher_discount = ?, total_amount = ? WHERE id = ? AND state = 'PLACED'",
            (order.item_subtotal, order.voucher_discount, order.total, order.id))
        return cur.rowcount == 1

    # ---- archive (SUC-09) ---------------------------------------------------------------

    def archive_one(self, order_id: int, now: str) -> bool:
        cur = self.conn.execute(
            f"UPDATE orders SET archived_at = ? WHERE id = ? AND archived_at IS NULL AND state IN ({_TERMINAL}) AND closed_at IS NOT NULL",
            (now, order_id))
        return cur.rowcount == 1

    def count_archivable(self, closed_before: str) -> int:
        return self.conn.execute(
            f"SELECT COUNT(*) FROM orders WHERE archived_at IS NULL AND state IN ({_TERMINAL}) AND closed_at < ?",
            (closed_before,)).fetchone()[0]

    def archive_closed_before(self, closed_before: str, now: str) -> int:
        """Archive finished orders closed before the cutoff. Open orders are never archived."""
        cur = self.conn.execute(
            f"UPDATE orders SET archived_at = ? WHERE archived_at IS NULL AND state IN ({_TERMINAL}) "
            "AND closed_at < ?", (now, closed_before))
        return cur.rowcount

    def list_archived(self, limit: int = 50) -> list[Order]:
        rows = self.conn.execute(
            f"SELECT {_ORDER_COLUMNS} FROM orders WHERE archived_at IS NOT NULL ORDER BY archived_at DESC, id DESC "
            "LIMIT ?", (limit,)).fetchall()
        return [self._load(r) for r in rows]

    def _load(self, row: Optional[sqlite3.Row]) -> Optional[Order]:
        if row is None:
            return None
        line_rows = self.conn.execute(
            "SELECT id, menu_item_id, item_name, unit_price, quantity "
            "FROM order_line WHERE order_id = ? ORDER BY id", (row["id"],)).fetchall()
        fields = dict(row)
        fields["state"] = OrderState(fields["state"])
        return Order(**fields, lines=[OrderLine(**dict(r)) for r in line_rows])
