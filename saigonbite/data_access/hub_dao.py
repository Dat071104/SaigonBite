from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import ACTIVE_ORDER_STATES, Hub, HubMenuItem, MenuItem, rules

_HUB_COLUMNS = ("id, code, name, address_text, latitude, longitude, "
                "max_active_orders, base_delivery_fee, archived_at")
_ACTIVE = ", ".join(f"'{s.value}'" for s in ACTIVE_ORDER_STATES)
_TERMINAL = ", ".join(f"'{s.value}'" for s in rules.TERMINAL_ORDER_STATES)

# Items a customer can order: the item and its brand are not archived.
_ORDERABLE = "m.archived_at IS NULL AND b.archived_at IS NULL"


class HubDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ---- hubs (UC-03) ------------------------------------------------------------------

    def list_active(self) -> list[Hub]:
        rows = self.conn.execute(
            f"SELECT {_HUB_COLUMNS} FROM hub WHERE archived_at IS NULL ORDER BY id").fetchall()
        return [Hub(**dict(r)) for r in rows]

    def list_all(self) -> list[Hub]:
        rows = self.conn.execute(
            f"SELECT {_HUB_COLUMNS} FROM hub ORDER BY archived_at IS NOT NULL, id").fetchall()
        return [Hub(**dict(r)) for r in rows]

    def get(self, hub_id: int) -> Optional[Hub]:
        """Return an active (not archived) hub, or None."""
        row = self.conn.execute(
            f"SELECT {_HUB_COLUMNS} FROM hub WHERE id = ? AND archived_at IS NULL", (hub_id,)).fetchone()
        return Hub(**dict(row)) if row else None

    def get_including_archived(self, hub_id: int) -> Optional[Hub]:
        """Return the hub even if archived: order history must keep showing where it was placed."""
        row = self.conn.execute(f"SELECT {_HUB_COLUMNS} FROM hub WHERE id = ?", (hub_id,)).fetchone()
        return Hub(**dict(row)) if row else None

    def code_exists(self, code: str, except_id: Optional[int] = None) -> bool:
        row = self.conn.execute("SELECT 1 FROM hub WHERE code = ? AND id IS NOT ?", (code, except_id)).fetchone()
        return row is not None

    def insert(self, hub: Hub) -> int:
        cur = self.conn.execute(
            "INSERT INTO hub (code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (hub.code, hub.name, hub.address_text, hub.latitude, hub.longitude, hub.max_active_orders,
             hub.base_delivery_fee))
        return cur.lastrowid

    def update(self, hub: Hub) -> bool:
        """Update an active hub. Returns False if it is archived or missing."""
        cur = self.conn.execute(
            "UPDATE hub SET code = ?, name = ?, address_text = ?, latitude = ?, longitude = ?, "
            "               max_active_orders = ?, base_delivery_fee = ? "
            "WHERE id = ? AND archived_at IS NULL",
            (hub.code, hub.name, hub.address_text, hub.latitude, hub.longitude, hub.max_active_orders,
             hub.base_delivery_fee, hub.id))
        return cur.rowcount == 1

    def archive(self, hub_id: int, now: str) -> bool:
        cur = self.conn.execute("UPDATE hub SET archived_at = ? WHERE id = ? AND archived_at IS NULL",
                                (now, hub_id))
        return cur.rowcount == 1

    # ---- workload (Q1) -----------------------------------------------------------------

    def active_load(self, hub_id: int) -> int:
        """Orders the kitchen still has to cook (PLACED, CONFIRMED, PREPARING)."""
        return self.conn.execute(
            f"SELECT COUNT(*) FROM orders WHERE hub_id = ? AND state IN ({_ACTIVE})", (hub_id,)).fetchone()[0]

    def active_loads(self) -> dict[int, int]:
        rows = self.conn.execute(
            f"SELECT hub_id, COUNT(*) AS n FROM orders WHERE state IN ({_ACTIVE}) GROUP BY hub_id").fetchall()
        return {r["hub_id"]: r["n"] for r in rows}

    def open_order_count(self, hub_id: int) -> int:
        """Orders not yet finished in any way (the archive guard of UC-03)."""
        return self.conn.execute(
            f"SELECT COUNT(*) FROM orders WHERE hub_id = ? AND state NOT IN ({_TERMINAL})", (hub_id,)).fetchone()[0]

    # ---- menu as the customer sees it (UC-01) -------------------------------------------

    def list_menu(self, hub_id: int) -> list[HubMenuItem]:
        """Orderable menu items the hub carries, with their availability flag."""
        rows = self.conn.execute(
            "SELECT m.id, m.brand_id, b.name AS brand_name, m.name, m.description, m.price, "
            "       hm.hub_id, hm.is_available "
            "FROM hub_menu_item hm "
            "JOIN menu_item m ON m.id = hm.menu_item_id "
            "JOIN brand b ON b.id = m.brand_id "
            f"WHERE hm.hub_id = ? AND {_ORDERABLE} ORDER BY b.id, m.id", (hub_id,)).fetchall()
        return [HubMenuItem(hub_id=r["hub_id"], is_available=bool(r["is_available"]),
                            item=MenuItem(id=r["id"], brand_id=r["brand_id"], brand_name=r["brand_name"],
                                          name=r["name"], description=r["description"], price=r["price"]))
                for r in rows]

    def get_available_item(self, hub_id: int, menu_item_id: int) -> Optional[MenuItem]:
        """Return the item only if this hub carries it, it is available and it is not archived."""
        r = self.conn.execute(
            "SELECT m.id, m.brand_id, b.name AS brand_name, m.name, m.description, m.price "
            "FROM hub_menu_item hm "
            "JOIN menu_item m ON m.id = hm.menu_item_id "
            "JOIN brand b ON b.id = m.brand_id "
            f"WHERE hm.hub_id = ? AND hm.menu_item_id = ? AND hm.is_available = 1 AND {_ORDERABLE}",
            (hub_id, menu_item_id)).fetchone()
        return MenuItem(**dict(r)) if r else None
