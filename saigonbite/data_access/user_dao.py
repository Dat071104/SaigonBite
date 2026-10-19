from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import Role, UserAccount


def _to_user(row: sqlite3.Row) -> UserAccount:
    return UserAccount(id=row["id"], username=row["username"], password_hash=row["password_hash"],
                       display_name=row["display_name"], role=Role(row["role"]),
                       is_active=bool(row["is_active"]))


class UserDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_by_id(self, user_id: int) -> Optional[UserAccount]:
        row = self.conn.execute(
            "SELECT id, username, password_hash, display_name, role, is_active "
            "FROM user_account WHERE id = ?", (user_id,)).fetchone()
        return _to_user(row) if row else None

    def get_by_username(self, username: str) -> Optional[UserAccount]:
        row = self.conn.execute(
            "SELECT id, username, password_hash, display_name, role, is_active "
            "FROM user_account WHERE username = ?", (username,)).fetchone()
        return _to_user(row) if row else None
