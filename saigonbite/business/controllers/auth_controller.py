from __future__ import annotations

import sqlite3
from typing import Optional

from werkzeug.security import check_password_hash

from saigonbite.business.domain import UserAccount
from saigonbite.data_access import UserDAO


class AuthController:
    """Login support for the seeded accounts (US-12)."""

    def __init__(self, conn: sqlite3.Connection):
        self.users = UserDAO(conn)

    def authenticate(self, username: str, password: str) -> Optional[UserAccount]:
        """Return the user if the username exists, is active and the password matches."""
        user = self.users.get_by_username((username or "").strip())
        if user is None or not user.is_active:
            return None
        if not check_password_hash(user.password_hash, password or ""):
            return None
        return user

    def get_user(self, user_id: int) -> Optional[UserAccount]:
        user = self.users.get_by_id(user_id)
        return user if user and user.is_active else None
