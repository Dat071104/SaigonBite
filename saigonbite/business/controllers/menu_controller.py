"""MenuController (UC-06 Manage brands and menu items): one method per system operation of the SSD.

    listCatalogue    -> catalogue(user_id)
    createBrand      -> create_brand(user_id, name)
    renameBrand      -> rename_brand(user_id, brand_id, name)
    archiveBrand     -> archive_brand(user_id, brand_id)
    createMenuItem   -> create_item(user_id, form)
    updateMenuItem   -> update_item(user_id, item_id, form)
    archiveMenuItem  -> archive_item(user_id, item_id)
    viewHubMenu      -> hub_menu(user_id, hub_id)
    listItemAtHub    -> list_item_at_hub(user_id, hub_id, item_id)
    unlistItemAtHub  -> unlist_item_at_hub(user_id, hub_id, item_id)
    setAvailability  -> set_availability(user_id, hub_id, item_id, available)

MenuItem state machine: ACTIVE -> ARCHIVED. An archived item (or an item of an archived brand) can no
longer be ordered; order lines keep the name and price copied at order time, so history never changes.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Mapping, Optional

from saigonbite.business.domain import Brand, Hub, HubMenuItem, MenuItem, Role
from saigonbite.data_access import HubDAO, MenuDAO, immediate_transaction

from .common import BaseController
from .errors import ConflictError, NotFoundError, ValidationError

MAX_PRICE = 1_000_000


@dataclass
class Catalogue:
    brands: list[Brand]
    items: list[MenuItem]


@dataclass
class HubMenu:
    hub: Hub
    listed: list[HubMenuItem]
    not_listed: list[MenuItem]      # active items this hub could add


class MenuController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None):
        super().__init__(conn, clock)
        self.menu = MenuDAO(conn)
        self.hubs = HubDAO(conn)

    def catalogue(self, user_id: int) -> Catalogue:
        self._require_admin(user_id)
        return Catalogue(brands=self.menu.list_brands(), items=self.menu.list_items())

    def list_catalogue(self, user_id: int, hub_id: Optional[int] = None) -> dict[str, object]:
        """One SSD operation composes catalogue, retained hubs and applicable listings."""
        self._require_admin(user_id)
        catalogue = self.catalogue(user_id)
        hubs = self.hubs.list_all()
        selected = self.hub_menu(user_id,hub_id) if hub_id is not None else None
        return dict(catalogue=catalogue,brands=catalogue.brands,items=catalogue.items,hubs=hubs,
                    hub_menu=selected,listings={h.id:self.menu.list_hub_items(h.id)
                    for h in hubs if hub_id is None or h.id==hub_id})

    # ---- brands ------------------------------------------------------------------------

    def create_brand(self, user_id: int, name: str) -> Brand:
        self._require_admin(user_id)
        name = self._name(name, "brand name")
        with immediate_transaction(self.conn):
            if self.menu.brand_name_exists(name):
                raise ValidationError(f"A brand called {name} already exists.")
            brand = Brand(id=self.menu.insert_brand(name), name=name)
        return brand

    def rename_brand(self, user_id: int, brand_id: int, name: str) -> Brand:
        self._require_admin(user_id)
        name = self._name(name, "brand name")
        with immediate_transaction(self.conn):
            self._active_brand(brand_id)
            if self.menu.brand_name_exists(name, except_id=brand_id):
                raise ValidationError(f"A brand called {name} already exists.")
            if not self.menu.rename_brand(brand_id, name):
                raise ConflictError('The brand changed before saving.')
        return self.menu.get_brand(brand_id)

    def archive_brand(self, user_id: int, brand_id: int) -> Brand:
        """The brand's dishes disappear from every hub menu; past orders keep their copied lines."""
        self._require_admin(user_id)
        with immediate_transaction(self.conn):
            self._active_brand(brand_id)
            if not self.menu.archive_brand(brand_id, self._now()):
                raise ConflictError('The brand changed before archive.')
        return self.menu.get_brand(brand_id)

    # ---- menu items --------------------------------------------------------------------

    def create_item(self, user_id: int, form: Mapping[str, str]) -> MenuItem:
        self._require_admin(user_id)
        item = self._parse_item(form, item_id=None)
        with immediate_transaction(self.conn):
            brand = self._active_brand(item.brand_id)
            if self.menu.item_name_exists(brand.id, item.name):
                raise ValidationError(f"{brand.name} already has a dish called {item.name}.")
            item.id = self.menu.insert_item(item)
        return self.menu.get_item(item.id)

    def update_item(self, user_id: int, item_id: int, form: Mapping[str, str]) -> MenuItem:
        """Name, description and price. The brand of a dish does not change."""
        self._require_admin(user_id)
        with immediate_transaction(self.conn):
            current = self._active_item(item_id)
            self._active_brand(current.brand_id)
            try:
                context = int(form.get('brand_id') or 0)
            except ValueError:
                context = 0
            if context != current.brand_id:
                raise ValidationError('The brand context must match the current parent; reparenting is not supported.')
            item = self._parse_item({**form, "brand_id": str(current.brand_id)}, item_id=item_id)
            if self.menu.item_name_exists(current.brand_id, item.name, except_id=item_id):
                raise ValidationError(f"{current.brand_name} already has a dish called {item.name}.")
            if not self.menu.update_item(item):
                raise ConflictError('The item changed before saving.')
        return self.menu.get_item(item_id)

    def archive_item(self, user_id: int, item_id: int) -> MenuItem:
        self._require_admin(user_id)
        with immediate_transaction(self.conn):
            self._active_item(item_id)
            if not self.menu.archive_item(item_id, self._now()):
                raise ConflictError('The item changed before archive.')
        return self.menu.get_item(item_id)

    # ---- hub listings ------------------------------------------------------------------

    def hub_menu(self, user_id: int, hub_id: int) -> HubMenu:
        self._require_admin(user_id)
        hub = self._hub(hub_id)
        listed = self.menu.list_hub_items(hub.id)
        listed_ids = {m.item.id for m in listed}
        active_brands = {b.id for b in self.menu.list_brands() if b.archived_at is None}
        not_listed = [i for i in self.menu.list_items()
                      if i.archived_at is None and i.brand_id in active_brands and i.id not in listed_ids]
        return HubMenu(hub=hub, listed=listed, not_listed=not_listed)

    def list_item_at_hub(self, user_id: int, hub_id: int, item_id: int, available: bool = True) -> None:
        self._require_admin(user_id)
        with immediate_transaction(self.conn):
            if type(available) is not bool:
                raise ValidationError('Availability must be true or false.')
            hub = self._hub(hub_id)
            if hub.archived_at is not None:
                raise ConflictError(f"{hub.name} is archived.")
            item = self._active_item(item_id)
            if self.menu.get_brand(item.brand_id).archived_at is not None:
                raise ConflictError(f"The brand {item.brand_name} is archived.")
            if self.menu.is_listed(hub_id, item_id):
                raise ConflictError(f"{item.name} is already on the menu of {hub.name}.")
            self.menu.add_listing(hub_id, item_id, available)

    def unlist_item_at_hub(self, user_id: int, hub_id: int, item_id: int) -> None:
        """Removes the listing row (the only physical delete): orders reference the menu item, not the listing."""
        self._require_admin(user_id)
        with immediate_transaction(self.conn):
            self._hub(hub_id)
            if not self.menu.remove_listing(hub_id, item_id):
                raise NotFoundError("This dish is not on the hub's menu.")

    def set_availability(self, user_id: int, hub_id: int, item_id: int, available: bool) -> None:
        self._require_admin(user_id)
        with immediate_transaction(self.conn):
            if type(available) is not bool:
                raise ValidationError('Availability must be true or false.')
            if self._hub(hub_id).archived_at is not None:
                raise ConflictError('The hub is archived.')
            self._active_brand(self._active_item(item_id).brand_id)
            if not self.menu.set_available(hub_id, item_id, available):
                raise NotFoundError("This dish is not on the hub's menu.")

    # ---- internals ---------------------------------------------------------------------

    def _require_admin(self, user_id: int) -> None:
        self._require_user(user_id, Role.ADMIN, message="Only administrators can manage brands and menus.")

    def _hub(self, hub_id: int) -> Hub:
        hub = self.hubs.get_including_archived(hub_id)
        if hub is None:
            raise NotFoundError("Hub not found.")
        return hub

    def _active_brand(self, brand_id) -> Brand:
        brand = self.menu.get_brand(brand_id) if brand_id else None
        if brand is None:
            raise ValidationError("Please choose a brand.")
        if brand.archived_at is not None:
            raise ConflictError(f"The brand {brand.name} is archived.")
        return brand

    def _active_item(self, item_id: int) -> MenuItem:
        item = self.menu.get_item(item_id)
        if item is None:
            raise NotFoundError("Dish not found.")
        if item.archived_at is not None:
            raise ConflictError(f"{item.name} is archived and can no longer be changed.")
        return item

    @staticmethod
    def _name(raw: str, label: str, max_len: int = 60) -> str:
        value = (raw or "").strip()
        if not value:
            raise ValidationError(f"Please enter the {label}.")
        if len(value) > max_len:
            raise ValidationError(f"The {label} must be at most {max_len} characters.")
        return value

    @classmethod
    def _parse_item(cls, form: Mapping[str, str], item_id) -> MenuItem:
        try:
            brand_id = int(form.get("brand_id") or 0)
        except ValueError:
            brand_id = 0
        name = cls._name(form.get("name"), "dish name")
        description = (form.get("description") or "").strip()
        if len(description) > 200:
            raise ValidationError("The description must be at most 200 characters.")
        raw = (form.get("price") or "").strip().replace(",", "")
        try:
            price = int(raw)
        except ValueError:
            raise ValidationError("The price must be a whole number of VND.") from None
        if not (1 <= price <= MAX_PRICE):
            raise ValidationError(f"The price must be between 1 and {MAX_PRICE:,} VND.")
        return MenuItem(id=item_id, brand_id=brand_id, brand_name="", name=name, description=description,
                        price=price)
