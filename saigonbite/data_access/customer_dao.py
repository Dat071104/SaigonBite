from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import Address, Customer, make_customer
from .database import StaleWriteError

_CUSTOMER_COLUMNS = "id, user_id, full_name, customer_type, phone, email, passport_no, nationality"
_ADDRESS_COLUMNS = "id, customer_id, label, full_address, district, latitude, longitude, archived_at"


def _to_customer(row: Optional[sqlite3.Row]) -> Optional[Customer]:
    if row is None:
        return None
    fields = dict(row)
    return make_customer(fields.pop("customer_type"), **fields)


class CustomerDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ---- customer ----------------------------------------------------------------------

    def get_by_user_id(self, user_id: int) -> Optional[Customer]:
        return _to_customer(self.conn.execute(
            f"SELECT {_CUSTOMER_COLUMNS} FROM customer WHERE user_id = ?", (user_id,)).fetchone())

    def get(self, customer_id: int) -> Optional[Customer]:
        return _to_customer(self.conn.execute(
            f"SELECT {_CUSTOMER_COLUMNS} FROM customer WHERE id = ?", (customer_id,)).fetchone())

    def insert(self, customer: Customer) -> int:
        return self.conn.execute(
            "INSERT INTO customer (user_id, full_name, customer_type, phone, email, passport_no, nationality) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (customer.user_id, customer.full_name, customer.customer_type.value, customer.phone,
             customer.email, customer.passport_no, customer.nationality)).lastrowid

    def update(self, customer: Customer) -> None:
        cur = self.conn.execute(
            "UPDATE customer SET full_name = ?, phone = ?, email = ?, passport_no = ?, nationality = ? WHERE id = ? AND user_id = ? AND customer_type = ?",
            (customer.full_name, customer.phone, customer.email, customer.passport_no, customer.nationality,
             customer.id, customer.user_id, customer.customer_type.value))
        if cur.rowcount != 1:
            raise StaleWriteError('The profile changed; reload and retry.')

    # ---- addresses ---------------------------------------------------------------------

    def list_addresses(self, customer_id: int) -> list[Address]:
        """The customer's usable (not archived) addresses."""
        rows = self.conn.execute(
            f"SELECT {_ADDRESS_COLUMNS} FROM address WHERE customer_id = ? AND archived_at IS NULL ORDER BY id",
            (customer_id,)).fetchall()
        return [Address(**dict(r)) for r in rows]

    def get_address(self, address_id: int, customer_id: int) -> Optional[Address]:
        """Return the address only if it belongs to the given customer and is not archived."""
        row = self.conn.execute(
            f"SELECT {_ADDRESS_COLUMNS} FROM address WHERE id = ? AND customer_id = ? AND archived_at IS NULL",
            (address_id, customer_id)).fetchone()
        return Address(**dict(row)) if row else None

    def insert_address(self, address: Address) -> int:
        return self.conn.execute(
            "INSERT INTO address (customer_id, label, full_address, district, latitude, longitude) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (address.customer_id, address.label, address.full_address, address.district, address.latitude,
             address.longitude)).lastrowid

    def update_address(self, address: Address) -> bool:
        cur = self.conn.execute(
            "UPDATE address SET label = ?, full_address = ?, district = ?, latitude = ?, longitude = ? "
            "WHERE id = ? AND customer_id = ? AND archived_at IS NULL",
            (address.label, address.full_address, address.district, address.latitude, address.longitude,
             address.id, address.customer_id))
        return cur.rowcount == 1

    def archive_address(self, address_id: int, customer_id: int, now: str) -> bool:
        cur = self.conn.execute(
            "UPDATE address SET archived_at = ? WHERE id = ? AND customer_id = ? AND archived_at IS NULL",
            (now, address_id, customer_id))
        return cur.rowcount == 1
