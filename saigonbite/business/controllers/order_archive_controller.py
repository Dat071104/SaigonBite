"""OrderArchiveController (SUC-09 Archive closed orders).

    previewArchive -> preview(user_id, closed_before)
    archiveOrders  -> archive(user_id, closed_before)
    listArchived   -> list_archived(user_id)

Only finished orders (DELIVERED, DELIVERY_FAILED, REJECTED, CANCELLED) closed before the cutoff day are
archived. An archived order leaves the customer's and staff screens; its lines, payment, delivery and
replacement offers are archived with it (they are reached only through the order), and reports still
read it. Nothing is deleted.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date

from saigonbite.business.domain import Order, Role
from saigonbite.data_access import OrderDAO, immediate_transaction

from .common import BaseController, vn_day_start_utc
from .errors import ValidationError


@dataclass
class ArchivePreview:
    closed_before: str          # the day chosen (Ho Chi Minh City calendar)
    cutoff_utc: str
    count: int


class OrderArchiveController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None):
        super().__init__(conn, clock)
        self.orders = OrderDAO(conn)

    def preview(self, user_id: int, closed_before: str) -> ArchivePreview:
        self._require_admin(user_id)
        day, cutoff = self._cutoff(closed_before)
        return ArchivePreview(day, cutoff, self.orders.count_archivable(cutoff))

    def archive(self, user_id: int, closed_before: str) -> int:
        self._require_admin(user_id)
        _, cutoff = self._cutoff(closed_before)
        with immediate_transaction(self.conn):
            return self.orders.archive_closed_before(cutoff, self._now())

    def list_archived(self, user_id: int) -> list[Order]:
        self._require_admin(user_id)
        return self.orders.list_archived()

    def _require_admin(self, user_id: int) -> None:
        self._require_user(user_id, Role.ADMIN, message="Only administrators can archive orders.")

    def _cutoff(self, closed_before: str) -> tuple[str, str]:
        try:
            day = date.fromisoformat((closed_before or "").strip())
        except ValueError:
            raise ValidationError("Enter the day as YYYY-MM-DD.") from None
        if day.isoformat() > self._today_vn():
            raise ValidationError("Choose today or an earlier day.")
        return day.isoformat(), vn_day_start_utc(day)
