"""Brands, menu items and hub listings (UC-06, SUC-06)."""
from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import Brand, HubMenuItem, MenuItem

_ITEM_SELECT = ("SELECT m.id, m.brand_id, b.name AS brand_name, m.name, m.description, m.price, m.archived_at "
                "FROM menu_item m JOIN brand b ON b.id = m.brand_id ")


class MenuDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ---- brands ------------------------------------------------------------------------

    def list_brands(self) -> list[Brand]:
        rows = self.conn.execute(
            "SELECT id, name, archived_at FROM brand ORDER BY archived_at IS NOT NULL, id").fetchall()
        return [Brand(**dict(r)) for r in rows]

    def get_brand(self, brand_id: int) -> Optional[Brand]:
        row = self.conn.execute("SELECT id, name, archived_at FROM brand WHERE id = ?", (brand_id,)).fetchone()
        return Brand(**dict(row)) if row else None

    def brand_name_exists(self, name: str, except_id: Optional[int] = None) -> bool:
        row = self.conn.execute("SELECT 1 FROM brand WHERE lower(name) = lower(?) AND id IS NOT ?",
                                (name, except_id)).fetchone()
        return row is not None

    def insert_brand(self, name: str) -> int:
        return self.conn.execute("INSERT INTO brand (name) VALUES (?)", (name,)).lastrowid

    def rename_brand(self, brand_id: int, name: str) -> bool:
        cur = self.conn.execute("UPDATE brand SET name = ? WHERE id = ? AND archived_at IS NULL", (name, brand_id))
        return cur.rowcount == 1

    def archive_brand(self, brand_id: int, now: str) -> bool:
        cur = self.conn.execute("UPDATE brand SET archived_at = ? WHERE id = ? AND archived_at IS NULL",
                                (now, brand_id))
        return cur.rowcount == 1

    # ---- menu items --------------------------------------------------------------------

    def list_items(self) -> list[MenuItem]:
        rows = self.conn.execute(_ITEM_SELECT + "ORDER BY m.archived_at IS NOT NULL, b.id, m.id").fetchall()
        return [MenuItem(**dict(r)) for r in rows]

    def get_item(self, item_id: int) -> Optional[MenuItem]:
        row = self.conn.execute(_ITEM_SELECT + "WHERE m.id = ?", (item_id,)).fetchone()
        return MenuItem(**dict(row)) if row else None

    def item_name_exists(self, brand_id: int, name: str, except_id: Optional[int] = None) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM menu_item WHERE brand_id = ? AND lower(name) = lower(?) AND id IS NOT ?",
            (brand_id, name, except_id)).fetchone()
        return row is not None

    def insert_item(self, item: MenuItem) -> int:
        return self.conn.execute(
            "INSERT INTO menu_item (brand_id, name, description, price) VALUES (?, ?, ?, ?)",
            (item.brand_id, item.name, item.description, item.price)).lastrowid

    def update_item(self, item: MenuItem) -> bool:
        """Change name, description or price. Order lines keep their own copy, so history is unchanged."""
        cur = self.conn.execute(
            "UPDATE menu_item SET name = ?, description = ?, price = ? WHERE id = ? AND archived_at IS NULL",
            (item.name, item.description, item.price, item.id))
        return cur.rowcount == 1

    def archive_item(self, item_id: int, now: str) -> bool:
        cur = self.conn.execute("UPDATE menu_item SET archived_at = ? WHERE id = ? AND archived_at IS NULL",
                                (now, item_id))
        return cur.rowcount == 1

    # ---- hub listings (association class HubMenuItem) -------------------------------------

    def list_hub_items(self, hub_id: int) -> list[HubMenuItem]:
        """Everything listed at the hub, archived items included (marked by archived_at)."""
        rows = self.conn.execute(
            "SELECT m.id, m.brand_id, b.name AS brand_name, m.name, m.description, m.price, "
            "       CASE WHEN m.archived_at IS NOT NULL THEN m.archived_at ELSE b.archived_at END AS archived_at, "
            "       hm.hub_id, hm.is_available "
            "FROM hub_menu_item hm JOIN menu_item m ON m.id = hm.menu_item_id JOIN brand b ON b.id = m.brand_id "
            "WHERE hm.hub_id = ? ORDER BY b.id, m.id", (hub_id,)).fetchall()
        return [HubMenuItem(hub_id=r["hub_id"], is_available=bool(r["is_available"]),
                            item=MenuItem(id=r["id"], brand_id=r["brand_id"], brand_name=r["brand_name"],
                                          name=r["name"], description=r["description"], price=r["price"],
                                          archived_at=r["archived_at"]))
                for r in rows]

    def is_listed(self, hub_id: int, item_id: int) -> bool:
        row = self.conn.execute("SELECT 1 FROM hub_menu_item WHERE hub_id = ? AND menu_item_id = ?",
                                (hub_id, item_id)).fetchone()
        return row is not None

    def add_listing(self, hub_id: int, item_id: int) -> None:
        self.conn.execute("INSERT INTO hub_menu_item (hub_id, menu_item_id, is_available) VALUES (?, ?, 1)",
                          (hub_id, item_id))

    def remove_listing(self, hub_id: int, item_id: int) -> bool:
        cur = self.conn.execute("DELETE FROM hub_menu_item WHERE hub_id = ? AND menu_item_id = ?", (hub_id, item_id))
        return cur.rowcount == 1

    def set_available(self, hub_id: int, item_id: int, available: bool) -> bool:
        cur = self.conn.execute("UPDATE hub_menu_item SET is_available = ? WHERE hub_id = ? AND menu_item_id = ?",
                                (1 if available else 0, hub_id, item_id))
        return cur.rowcount == 1
