"""SQLite connection helpers. All SQL lives in the DAO classes, never above this layer."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager


class StaleWriteError(RuntimeError):
    """A conditional persistence operation did not update its one expected row."""


def connect(db_path: str) -> sqlite3.Connection:
    """Open a connection in autocommit mode so transactions are explicit (BEGIN IMMEDIATE)."""
    conn = sqlite3.connect(db_path, timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    return conn


@contextmanager
def immediate_transaction(conn: sqlite3.Connection):
    """BEGIN IMMEDIATE ... COMMIT, or ROLLBACK if the block raises.

    BEGIN IMMEDIATE takes SQLite's write lock at once, so two checkouts cannot interleave
    their read-then-insert steps (risk R-03 in the plan; the capacity count joins it in I2).
    """
    started = False
    try:
        conn.execute("BEGIN IMMEDIATE")
        started = True
        yield conn
        conn.execute("COMMIT")
    except BaseException:
        if started and conn.in_transaction:
            try:
                conn.rollback()
            except sqlite3.Error:
                pass  # Preserve the original BEGIN/body/COMMIT failure.
        raise
