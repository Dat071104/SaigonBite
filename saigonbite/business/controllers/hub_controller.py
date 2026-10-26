"""HubController (UC-03 Manage hubs and kitchen capacity): one method per system operation of the SSD.

    listHubs    -> list_hubs(user_id)
    viewHub     -> get_hub(user_id, hub_id)
    createHub   -> create_hub(user_id, form)
    updateHub   -> update_hub(user_id, hub_id, form)
    archiveHub  -> archive_hub(user_id, hub_id)

Hub state machine: ACTIVE -> ARCHIVED (busy and quiet are derived from the load, never stored).
"""
from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from typing import Mapping

from saigonbite.business.domain import Hub, HubStatus, Role
from saigonbite.data_access import HubDAO, immediate_transaction

from .common import BaseController
from .errors import ConflictError, NotFoundError, ValidationError

CODE_PATTERN = re.compile(r"^HUB-[A-Z0-9]{2,8}$")
MAX_CAPACITY = 500
MAX_BASE_FEE = 100000
# Ho Chi Minh City area: a typo in the coordinates should not put a hub in another country.
LAT_RANGE, LON_RANGE = (10.3, 11.2), (106.3, 107.1)


@dataclass
class HubAdminView:
    status: HubStatus
    open_orders: int

    @property
    def can_archive(self) -> bool:
        return self.status.hub.archived_at is None and self.open_orders == 0


class HubController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None):
        super().__init__(conn, clock)
        self.hubs = HubDAO(conn)

    def list_hubs(self, user_id: int, include_archived: bool = True) -> list[HubAdminView]:
        self._require_admin(user_id)
        loads = self.hubs.active_loads()
        return [HubAdminView(HubStatus(h, loads.get(h.id, 0)), self.hubs.open_order_count(h.id))
                for h in (self.hubs.list_all() if include_archived else self.hubs.list_active())]

    def get_hub(self, user_id: int, hub_id: int) -> HubAdminView:
        self._require_admin(user_id)
        hub = self.hubs.get_including_archived(hub_id)
        if hub is None:
            raise NotFoundError("Hub not found.")
        return HubAdminView(HubStatus(hub, self.hubs.active_load(hub.id)), self.hubs.open_order_count(hub.id))

    def create_hub(self, user_id: int, form: Mapping[str, str]) -> Hub:
        self._require_admin(user_id)
        hub = self._parse(form, hub_id=None)
        with immediate_transaction(self.conn):
            if self.hubs.code_exists(hub.code):
                raise ValidationError(f"The code {hub.code} is already used by another hub.")
            if any(h.name.casefold() == hub.name.casefold() for h in self.hubs.list_all()):
                raise ValidationError('The hub name is already retained by another hub.')
            hub.id = self.hubs.insert(hub)
        return hub

    def update_hub(self, user_id: int, hub_id: int, form: Mapping[str, str]) -> Hub:
        """Capacity may go below the current load: the hub then refuses new orders until the load falls."""
        self._require_admin(user_id)
        hub = self._parse(form, hub_id=hub_id)
        with immediate_transaction(self.conn):
            current = self.hubs.get_including_archived(hub_id)
            if current is None:
                raise NotFoundError("Hub not found.")
            if current.archived_at is not None:
                raise ConflictError(f"{current.name} is archived and can no longer be changed.")
            if self.hubs.code_exists(hub.code, except_id=hub_id):
                raise ValidationError(f"The code {hub.code} is already used by another hub.")
            if any(h.id != hub_id and h.name.casefold() == hub.name.casefold() for h in self.hubs.list_all()):
                raise ValidationError('The hub name is already retained by another hub.')
            if not self.hubs.update(hub):
                raise ConflictError('The hub changed before saving. Please reload.')
        return hub

    def archive_hub(self, user_id: int, hub_id: int) -> Hub:
        """Guard: no open orders (anything not yet delivered, failed, rejected or cancelled).
        Archived hubs leave browsing and checkout; order history still shows them."""
        self._require_admin(user_id)
        with immediate_transaction(self.conn):
            hub = self.hubs.get_including_archived(hub_id)
            if hub is None:
                raise NotFoundError("Hub not found.")
            if hub.archived_at is not None:
                raise ConflictError(f"{hub.name} is already archived.")
            open_orders = self.hubs.open_order_count(hub_id)
            if open_orders:
                raise ConflictError(f"{hub.name} still has {open_orders} open order(s). "
                                    "Archive it when they are finished.")
            if not self.hubs.archive(hub_id, self._now()):
                raise ConflictError('The hub changed before archive. Please reload.')
        return self.hubs.get_including_archived(hub_id)

    # ---- internals ---------------------------------------------------------------------

    def _require_admin(self, user_id: int) -> None:
        self._require_user(user_id, Role.ADMIN, message="Only administrators can manage hubs.")

    @staticmethod
    def _parse(form: Mapping[str, str], hub_id) -> Hub:
        def text(name: str, label: str, max_len: int) -> str:
            value = (form.get(name) or "").strip()
            if not value:
                raise ValidationError(f"Please enter the {label}.")
            if len(value) > max_len:
                raise ValidationError(f"The {label} must be at most {max_len} characters.")
            return value

        def number(name: str, label: str, cast, low, high):
            raw = (form.get(name) or "").strip().replace(",", "")
            try:
                value = cast(raw)
            except ValueError:
                raise ValidationError(f"The {label} must be a number.") from None
            if not (low <= value <= high):
                raise ValidationError(f"The {label} must be between {low:,} and {high:,}.")
            return value

        code = text("code", "hub code", 12).upper()
        if not CODE_PATTERN.match(code):
            raise ValidationError("The hub code looks like HUB-D1: 'HUB-' and 2 to 8 letters or digits.")
        return Hub(id=hub_id, code=code, name=text("name", "hub name", 80),
                   address_text=text("address_text", "address", 200),
                   latitude=number("latitude", "latitude", float, *LAT_RANGE),
                   longitude=number("longitude", "longitude", float, *LON_RANGE),
                   max_active_orders=number("max_active_orders", "kitchen capacity", int, 1, MAX_CAPACITY),
                   base_delivery_fee=number("base_delivery_fee", "base delivery fee", int, 0, MAX_BASE_FEE))
