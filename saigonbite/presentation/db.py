"""Per-request database connection for the View layer."""
import os
import sqlite3

from flask import current_app, g

from saigonbite.data_access import connect


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        path = current_app.config["DATABASE"]
        if not os.path.exists(path):
            raise RuntimeError(f"Database not found at {path}. Run: python init_db.py")
        g.db = connect(path)
    return g.db


def close_db(_exc=None) -> None:
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()
