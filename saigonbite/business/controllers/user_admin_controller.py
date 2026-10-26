"""UserAdminController (SUC-08 Manage user accounts).

    listUsers        -> list_users(user_id)
    createStaff      -> create_staff(user_id, form)       kitchen staff, shippers, admins, managers
    updateUser       -> update_user(user_id, target_id, form)
    deactivateUser   -> set_active(user_id, target_id, False)   (the archive of a user account)
    reactivateUser   -> set_active(user_id, target_id, True)

Customers register themselves (SUC-02). A deactivated account cannot log in; its orders stay.
"""
from __future__ import annotations

import re
import sqlite3
from typing import Mapping, Optional

from werkzeug.security import generate_password_hash

from saigonbite.business.domain import DeliveryState, Hub, Role, UserAccount
from saigonbite.data_access import CustomerDAO, DeliveryDAO, HubDAO, immediate_transaction

from .common import BaseController
from .errors import ConflictError, NotFoundError, ValidationError

USERNAME = re.compile(r"^[a-z0-9_.]{3,30}$")
STAFF_ROLES = (Role.KITCHEN_STAFF, Role.SHIPPER, Role.ADMIN, Role.MANAGER)


class UserAdminController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None):
        super().__init__(conn, clock)
        self.hubs = HubDAO(conn)

    def list_users(self, user_id: int) -> list[UserAccount]:
        self._require_admin(user_id)
        return self.users.list_all()

    def hubs_for_staff(self) -> list[Hub]:
        return self.hubs.list_active()

    def get_user(self, user_id: int, target_id: int) -> UserAccount:
        self._require_admin(user_id)
        return self._target(target_id)

    def get_customer(self, user_id: int, target_id: int):
        self._require_admin(user_id)
        self._target(target_id)
        return CustomerDAO(self.conn).get_by_user_id(target_id)

    def create_staff(self, user_id: int, form: Mapping[str, str]) -> UserAccount:
        self._require_admin(user_id)
        username = (form.get("username") or "").strip().lower()
        if not USERNAME.match(username):
            raise ValidationError("The username has 3 to 30 small letters, digits, dots or underscores.")
        try:
            role = Role(form.get("role") or "")
        except ValueError:
            role = None
        if role not in STAFF_ROLES:
            raise ValidationError("Choose kitchen staff, shipper, admin or manager. Customers register themselves.")
        display_name = self._display_name(form)
        password = self._password(form, required=True)
        with immediate_transaction(self.conn):
            if self.users.get_by_username(username) is not None:
                raise ValidationError(f"The username {username} is taken.")
            user = UserAccount(id=0, username=username, password_hash=generate_password_hash(password),
                               display_name=display_name, role=role,
                               hub_id=self._hub_for(role, form.get("hub_id")))
            user.id = self.users.insert(user)
        return user

    def update_user(self, user_id: int, target_id: int, form: Mapping[str, str]) -> UserAccount:
        """Display name, the kitchen's hub, and an optional new password. Role and username stay."""
        self._require_admin(user_id)
        with immediate_transaction(self.conn):
            user = self._target(target_id)
            if ('role' in form and form['role'] != user.role.value) or ('username' in form and form['username'].strip().lower() != user.username):
                raise ValidationError('The existing username and role cannot be changed.')
            if user.role is Role.CUSTOMER:
                raise ConflictError("Customers keep their own profile. You can only deactivate a customer account.")
            user.display_name = self._display_name(form)
            user.hub_id = self._hub_for(user.role, form.get("hub_id"))
            password = self._password(form, required=False)
            if password:
                user.password_hash = generate_password_hash(password)
            self.users.update(user)
        return user

    def set_active(self, user_id: int, target_id: int, active: bool) -> UserAccount:
        admin = self._require_admin(user_id)
        if target_id == admin.id:
            raise ConflictError("You cannot deactivate your own account.")
        with immediate_transaction(self.conn):
            user = self._target(target_id)
            if not active and user.role is Role.SHIPPER and DeliveryDAO(self.conn).list_for_shipper(target_id,DeliveryState.PICKED_UP):
                raise ConflictError('A shipper holding a picked-up delivery cannot be deactivated.')
            if not self.users.set_active(target_id, active):
                raise ConflictError(f"{user.username} is already {'active' if active else 'deactivated'}.")
        return self._target(target_id)

    # ---- internals ---------------------------------------------------------------------

    def _require_admin(self, user_id: int) -> UserAccount:
        return self._require_user(user_id, Role.ADMIN, message="Only administrators can manage user accounts.")

    def _target(self, target_id: int) -> UserAccount:
        user = self.users.get_by_id(target_id)
        if user is None:
            raise NotFoundError("User not found.")
        return user

    def _hub_for(self, role: Role, raw_hub_id) -> Optional[int]:
        if role is not Role.KITCHEN_STAFF:
            return None
        try:
            hub = self.hubs.get(int(raw_hub_id or 0))
        except ValueError:
            hub = None
        if hub is None or hub.archived_at is not None:
            raise ValidationError("Kitchen staff need an active hub to work in.")
        return hub.id

    @staticmethod
    def _display_name(form: Mapping[str, str]) -> str:
        name = (form.get("display_name") or "").strip()
        if not (2 <= len(name) <= 60):
            raise ValidationError("Enter a display name of 2 to 60 characters.")
        return name

    @staticmethod
    def _password(form: Mapping[str, str], required: bool) -> str:
        password = form.get("password") or ""
        if not password and not required:
            return ""
        if not (6 <= len(password) <= 72):
            raise ValidationError("The password must have 6 to 72 characters.")
        return password
