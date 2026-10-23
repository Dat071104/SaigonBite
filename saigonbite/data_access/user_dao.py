from __future__ import annotations

import sqlite3
from typing import Optional

from saigonbite.business.domain import Role, UserAccount

_USER_COLUMNS = "id, username, password_hash, display_name, role, hub_id, is_active"


def _to_user(row: sqlite3.Row) -> UserAccount:
    return UserAccount(id=row["id"], username=row["username"], password_hash=row["password_hash"],
                       display_name=row["display_name"], role=Role(row["role"]),
                       is_active=bool(row["is_active"]), hub_id=row["hub_id"])


class UserDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_by_id(self, user_id: int) -> Optional[UserAccount]:
        row = self.conn.execute(f"SELECT {_USER_COLUMNS} FROM user_account WHERE id = ?", (user_id,)).fetchone()
        return _to_user(row) if row else None

    def get_by_username(self, username: str) -> Optional[UserAccount]:
        row = self.conn.execute(
            f"SELECT {_USER_COLUMNS} FROM user_account WHERE username = ?", (username,)).fetchone()
        return _to_user(row) if row else None

    def list_all(self) -> list[UserAccount]:
        rows = self.conn.execute(
            f"SELECT {_USER_COLUMNS} FROM user_account ORDER BY is_active DESC, role, username").fetchall()
        return [_to_user(r) for r in rows]

    def insert(self, user: UserAccount) -> int:
        return self.conn.execute(
            "INSERT INTO user_account (username, password_hash, display_name, role, hub_id, is_active) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (user.username, user.password_hash, user.display_name, user.role.value, user.hub_id,
             1 if user.is_active else 0)).lastrowid

    def update(self, user: UserAccount) -> None:
        """Display name, hub assignment and password hash. The role and username never change."""
        self.conn.execute(
            "UPDATE user_account SET display_name = ?, hub_id = ?, password_hash = ? WHERE id = ?",
            (user.display_name, user.hub_id, user.password_hash, user.id))

    def set_active(self, user_id: int, active: bool) -> bool:
        cur = self.conn.execute("UPDATE user_account SET is_active = ? WHERE id = ? AND is_active = ?",
                                (1 if active else 0, user_id, 0 if active else 1))
        return cur.rowcount == 1
