from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import Address, Customer, make_customer


class CustomerDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_by_user_id(self, user_id: int) -> Optional[Customer]:
        row = self.conn.execute(
            "SELECT id, user_id, full_name, phone, customer_type "
            "FROM customer WHERE user_id = ?", (user_id,)).fetchone()
        if row is None:
            return None
        return make_customer(row["customer_type"], id=row["id"], user_id=row["user_id"],
                             full_name=row["full_name"], phone=row["phone"])

    def list_addresses(self, customer_id: int) -> list[Address]:
        rows = self.conn.execute(
            "SELECT id, customer_id, label, full_address, latitude, longitude "
            "FROM address WHERE customer_id = ? ORDER BY id", (customer_id,)).fetchall()
        return [Address(**dict(r)) for r in rows]

    def get_address(self, address_id: int, customer_id: int) -> Optional[Address]:
        """Return the address only if it belongs to the given customer."""
        row = self.conn.execute(
            "SELECT id, customer_id, label, full_address, latitude, longitude "
            "FROM address WHERE id = ? AND customer_id = ?", (address_id, customer_id)).fetchone()
        return Address(**dict(row)) if row else None
