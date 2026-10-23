"""ReplacementOffer persistence (UC-05 offers, the customer decides in SUC-03)."""
from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import OfferState, ReplacementOffer

_COLUMNS = ("id, order_id, order_line_id, original_item_name, original_unit_price, new_menu_item_id, "
            "new_item_name, new_unit_price, state, offered_at, decided_at")


def _to_offer(row: Optional[sqlite3.Row]) -> Optional[ReplacementOffer]:
    if row is None:
        return None
    fields = dict(row)
    fields["state"] = OfferState(fields["state"])
    return ReplacementOffer(**fields)


class ReplacementOfferDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert(self, offer: ReplacementOffer) -> int:
        return self.conn.execute(
            "INSERT INTO replacement_offer (order_id, order_line_id, original_item_name, original_unit_price, "
            "    new_menu_item_id, new_item_name, new_unit_price, state, offered_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (offer.order_id, offer.order_line_id, offer.original_item_name, offer.original_unit_price,
             offer.new_menu_item_id, offer.new_item_name, offer.new_unit_price, offer.state.value,
             offer.offered_at)).lastrowid

    def get_open(self, order_id: int) -> Optional[ReplacementOffer]:
        return _to_offer(self.conn.execute(
            f"SELECT {_COLUMNS} FROM replacement_offer WHERE order_id = ? AND state = 'OFFERED'",
            (order_id,)).fetchone())

    def list_for_order(self, order_id: int) -> list[ReplacementOffer]:
        rows = self.conn.execute(
            f"SELECT {_COLUMNS} FROM replacement_offer WHERE order_id = ? ORDER BY id", (order_id,)).fetchall()
        return [_to_offer(r) for r in rows]

    def decide(self, offer_id: int, to_state: OfferState, now: str) -> bool:
        """OFFERED -> ACCEPTED, DECLINED or WITHDRAWN, once."""
        cur = self.conn.execute(
            "UPDATE replacement_offer SET state = ?, decided_at = ? WHERE id = ? AND state = 'OFFERED'",
            (to_state.value, now, offer_id))
        return cur.rowcount == 1
