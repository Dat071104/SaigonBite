"""VoucherController (SUC-07 Manage vouchers). Applying a voucher at checkout belongs to UC-01.

    listVouchers   -> list_vouchers(user_id)
    createVoucher  -> create_voucher(user_id, form)
    updateVoucher  -> update_voucher(user_id, voucher_id, form)
    archiveVoucher -> archive_voucher(user_id, voucher_id)

Orders keep the voucher id and the discount they got, so editing or archiving a voucher never changes
a past order.
"""
from __future__ import annotations

import re
import sqlite3
from datetime import date
from typing import Mapping

from saigonbite.business.domain import DiscountType, Role, Voucher
from saigonbite.data_access import VoucherDAO, immediate_transaction

from .common import BaseController
from .errors import ConflictError, NotFoundError, ValidationError

CODE = re.compile(r"^[A-Z0-9]{3,20}$")


class VoucherController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None):
        super().__init__(conn, clock)
        self.vouchers = VoucherDAO(conn)

    def list_vouchers(self, user_id: int) -> list[Voucher]:
        self._require_admin(user_id)
        return self.vouchers.list_all()

    def get_voucher(self, user_id: int, voucher_id: int) -> Voucher:
        self._require_admin(user_id)
        voucher = self.vouchers.get(voucher_id)
        if voucher is None:
            raise NotFoundError("Voucher not found.")
        return voucher

    def create_voucher(self, user_id: int, form: Mapping[str, str]) -> Voucher:
        self._require_admin(user_id)
        voucher = self._parse(form, voucher_id=None)
        with immediate_transaction(self.conn):
            if self.vouchers.code_exists(voucher.code):
                raise ValidationError(f"The code {voucher.code} already exists.")
            voucher.id = self.vouchers.insert(voucher)
        return voucher

    def update_voucher(self, user_id: int, voucher_id: int, form: Mapping[str, str]) -> Voucher:
        self._require_admin(user_id)
        voucher = self._parse(form, voucher_id=voucher_id)
        with immediate_transaction(self.conn):
            current = self.vouchers.get(voucher_id)
            if current is None:
                raise NotFoundError("Voucher not found.")
            if current.archived_at is not None:
                raise ConflictError(f"{current.code} is archived and can no longer be changed.")
            if self.vouchers.code_exists(voucher.code, except_id=voucher_id):
                raise ValidationError(f"The code {voucher.code} already exists.")
            self.vouchers.update(voucher)
        return voucher

    def archive_voucher(self, user_id: int, voucher_id: int) -> Voucher:
        self._require_admin(user_id)
        with immediate_transaction(self.conn):
            current = self.vouchers.get(voucher_id)
            if current is None:
                raise NotFoundError("Voucher not found.")
            if not self.vouchers.archive(voucher_id, self._now()):
                raise ConflictError(f"{current.code} is already archived.")
        return self.vouchers.get(voucher_id)

    # ---- internals ---------------------------------------------------------------------

    def _require_admin(self, user_id: int) -> None:
        self._require_user(user_id, Role.ADMIN, message="Only administrators can manage vouchers.")

    @staticmethod
    def _parse(form: Mapping[str, str], voucher_id) -> Voucher:
        code = (form.get("code") or "").strip().upper()
        if not CODE.match(code):
            raise ValidationError("The code has 3 to 20 capital letters or digits, for example LUNCH10.")
        description = (form.get("description") or "").strip()
        if len(description) > 120:
            raise ValidationError("The description must be at most 120 characters.")
        try:
            discount_type = DiscountType(form.get("discount_type") or "")
        except ValueError:
            raise ValidationError("Choose a fixed amount or a percentage.") from None

        def whole(name: str, label: str, required: bool = True):
            raw = (form.get(name) or "").strip().replace(",", "")
            if raw == "" and not required:
                return None
            try:
                value = int(raw)
            except ValueError:
                raise ValidationError(f"The {label} must be a whole number.") from None
            if value < 0:
                raise ValidationError(f"The {label} cannot be negative.")
            return value

        value = whole("discount_value", "discount")
        if value == 0 or (discount_type is DiscountType.PERCENT and value > 100):
            raise ValidationError("A percentage discount is between 1 and 100; a fixed discount is above 0.")
        min_subtotal = whole("min_subtotal", "minimum order", required=False) or 0
        max_discount = whole("max_discount", "maximum discount", required=False)
        if max_discount == 0:
            max_discount = None
        try:
            valid_from = date.fromisoformat(form.get("valid_from") or "").isoformat()
            valid_until = date.fromisoformat(form.get("valid_until") or "").isoformat()
        except ValueError:
            raise ValidationError("Enter both dates as YYYY-MM-DD.") from None
        if valid_from > valid_until:
            raise ValidationError("The voucher must start on or before its last day.")
        return Voucher(id=voucher_id, code=code, description=description, discount_type=discount_type,
                       discount_value=value, min_subtotal=min_subtotal, max_discount=max_discount,
                       valid_from=valid_from, valid_until=valid_until)
