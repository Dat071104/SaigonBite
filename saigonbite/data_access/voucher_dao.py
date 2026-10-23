"""Voucher persistence (SUC-07; applied at checkout in UC-01)."""
from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import DiscountType, Voucher

_COLUMNS = ("id, code, description, discount_type, discount_value, min_subtotal, max_discount, valid_from, "
            "valid_until, archived_at")


def _to_voucher(row: Optional[sqlite3.Row]) -> Optional[Voucher]:
    if row is None:
        return None
    fields = dict(row)
    fields["discount_type"] = DiscountType(fields["discount_type"])
    return Voucher(**fields)


class VoucherDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get(self, voucher_id: int) -> Optional[Voucher]:
        return _to_voucher(self.conn.execute(f"SELECT {_COLUMNS} FROM voucher WHERE id = ?",
                                             (voucher_id,)).fetchone())

    def get_by_code(self, code: str) -> Optional[Voucher]:
        """Codes are matched without regard to case."""
        return _to_voucher(self.conn.execute(f"SELECT {_COLUMNS} FROM voucher WHERE upper(code) = upper(?)",
                                             (code,)).fetchone())

    def list_all(self) -> list[Voucher]:
        rows = self.conn.execute(
            f"SELECT {_COLUMNS} FROM voucher ORDER BY archived_at IS NOT NULL, valid_until DESC, code").fetchall()
        return [_to_voucher(r) for r in rows]

    def code_exists(self, code: str, except_id: Optional[int] = None) -> bool:
        row = self.conn.execute("SELECT 1 FROM voucher WHERE upper(code) = upper(?) AND id IS NOT ?",
                                (code, except_id)).fetchone()
        return row is not None

    def insert(self, v: Voucher) -> int:
        return self.conn.execute(
            "INSERT INTO voucher (code, description, discount_type, discount_value, min_subtotal, max_discount, "
            "                     valid_from, valid_until) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (v.code, v.description, v.discount_type.value, v.discount_value, v.min_subtotal, v.max_discount,
             v.valid_from, v.valid_until)).lastrowid

    def update(self, v: Voucher) -> bool:
        cur = self.conn.execute(
            "UPDATE voucher SET code = ?, description = ?, discount_type = ?, discount_value = ?, min_subtotal = ?, "
            "                   max_discount = ?, valid_from = ?, valid_until = ? "
            "WHERE id = ? AND archived_at IS NULL",
            (v.code, v.description, v.discount_type.value, v.discount_value, v.min_subtotal, v.max_discount,
             v.valid_from, v.valid_until, v.id))
        return cur.rowcount == 1

    def archive(self, voucher_id: int, now: str) -> bool:
        cur = self.conn.execute("UPDATE voucher SET archived_at = ? WHERE id = ? AND archived_at IS NULL",
                                (now, voucher_id))
        return cur.rowcount == 1
