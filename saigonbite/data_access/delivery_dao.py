"""Delivery persistence (UC-02). Every change is conditional on the current state, so two shippers
taking the same order, or a repeated submit, change the row at most once."""
from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import Delivery, DeliveryState

_COLUMNS = ("id, order_id, shipper_id, state, ready_at, picked_up_at, finished_at, failure_reason, "
            "cash_collected")


def _to_delivery(row: Optional[sqlite3.Row]) -> Optional[Delivery]:
    if row is None:
        return None
    fields = dict(row)
    fields["state"] = DeliveryState(fields["state"])
    return Delivery(**fields)


class DeliveryDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert(self, delivery: Delivery) -> int:
        return self.conn.execute(
            "INSERT INTO delivery (order_id, state, ready_at) VALUES (?, ?, ?)",
            (delivery.order_id, delivery.state.value, delivery.ready_at)).lastrowid

    def get_by_order_id(self, order_id: int) -> Optional[Delivery]:
        return _to_delivery(self.conn.execute(
            f"SELECT {_COLUMNS} FROM delivery WHERE order_id = ?", (order_id,)).fetchone())

    def list_awaiting_pickup(self) -> list[Delivery]:
        rows = self.conn.execute(
            f"SELECT {_COLUMNS} FROM delivery WHERE state = 'AWAITING_PICKUP' ORDER BY ready_at, id").fetchall()
        return [_to_delivery(r) for r in rows]

    def list_for_shipper(self, shipper_id: int, state: DeliveryState) -> list[Delivery]:
        rows = self.conn.execute(
            f"SELECT {_COLUMNS} FROM delivery WHERE shipper_id = ? AND state = ? "
            "ORDER BY COALESCE(finished_at, picked_up_at) DESC, id DESC LIMIT 20",
            (shipper_id, state.value)).fetchall()
        return [_to_delivery(r) for r in rows]

    def take(self, order_id: int, shipper_id: int, now: str) -> bool:
        """AWAITING_PICKUP -> PICKED_UP for this shipper. Only the first of two competing shippers wins."""
        cur = self.conn.execute(
            "UPDATE delivery SET shipper_id = ?, state = 'PICKED_UP', picked_up_at = ? "
            "WHERE order_id = ? AND state = 'AWAITING_PICKUP' AND shipper_id IS NULL", (shipper_id, now, order_id))
        return cur.rowcount == 1

    def finish(self, order_id: int, shipper_id: int, to_state: DeliveryState, now: str,
               failure_reason: Optional[str] = None, cash_collected: Optional[int] = None) -> bool:
        """PICKED_UP -> DELIVERED or FAILED, only by the shipper who picked it up."""
        cur = self.conn.execute(
            "UPDATE delivery SET state = ?, finished_at = ?, failure_reason = ?, cash_collected = ? "
            "WHERE order_id = ? AND shipper_id = ? AND state = 'PICKED_UP'",
            (to_state.value, now, failure_reason, cash_collected, order_id, shipper_id))
        return cur.rowcount == 1
