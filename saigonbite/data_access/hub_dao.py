from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import Hub, HubMenuItem, MenuItem

_HUB_COLUMNS = ("id, code, name, address_text, latitude, longitude, "
                "max_active_orders, delivery_fee_flat, archived_at")


class HubDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list_active(self) -> list[Hub]:
        rows = self.conn.execute(
            f"SELECT {_HUB_COLUMNS} FROM hub WHERE archived_at IS NULL ORDER BY id").fetchall()
        return [Hub(**dict(r)) for r in rows]

    def get(self, hub_id: int) -> Optional[Hub]:
        """Return an active (not archived) hub, or None."""
        row = self.conn.execute(
            f"SELECT {_HUB_COLUMNS} FROM hub WHERE id = ? AND archived_at IS NULL", (hub_id,)).fetchone()
        return Hub(**dict(row)) if row else None

    def list_menu(self, hub_id: int) -> list[HubMenuItem]:
        """All menu items the hub carries, with their availability flag."""
        rows = self.conn.execute(
            "SELECT m.id, m.brand_id, b.name AS brand_name, m.name, m.description, m.price, "
            "       hm.hub_id, hm.is_available "
            "FROM hub_menu_item hm "
            "JOIN menu_item m ON m.id = hm.menu_item_id "
            "JOIN brand b ON b.id = m.brand_id "
            "WHERE hm.hub_id = ? ORDER BY b.id, m.id", (hub_id,)).fetchall()
        return [HubMenuItem(hub_id=r["hub_id"], is_available=bool(r["is_available"]),
                            item=MenuItem(id=r["id"], brand_id=r["brand_id"], brand_name=r["brand_name"],
                                          name=r["name"], description=r["description"], price=r["price"]))
                for r in rows]

    def get_available_item(self, hub_id: int, menu_item_id: int) -> Optional[MenuItem]:
        """Return the item only if this hub carries it and it is currently available."""
        r = self.conn.execute(
            "SELECT m.id, m.brand_id, b.name AS brand_name, m.name, m.description, m.price "
            "FROM hub_menu_item hm "
            "JOIN menu_item m ON m.id = hm.menu_item_id "
            "JOIN brand b ON b.id = m.brand_id "
            "WHERE hm.hub_id = ? AND hm.menu_item_id = ? AND hm.is_available = 1",
            (hub_id, menu_item_id)).fetchone()
        return MenuItem(**dict(r)) if r else None
