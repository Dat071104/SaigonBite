"""Create a fresh SaigonBite v2 database or validate an existing version read-only.

Usage:  python init_db.py            (creates instance/saigonbite.db: schema, seed and demo history)
        python init_db.py --no-demo  (schema and seed only, no demo orders)
        python init_db.py --force    (delete and recreate an existing database)
        python init_db.py --migrate  (validate v2; refuse unsupported versions without writes)
        python init_db.py --db PATH  (use another file, e.g. for tests)

The schema version is kept in PRAGMA user_version. No migrations are provided.
Use a new path for fresh v2 and preserve retained databases and their sidecars.
"""
import argparse
import glob
import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(ROOT, "db", "schema.sql")
SEED_PATH = os.path.join(ROOT, "db", "seed.sql")
DEMO_PATH = os.path.join(ROOT, "db", "seed_demo.sql")
MIGRATIONS_DIR = os.path.join(ROOT, "db", "migrations")
DEFAULT_DB = os.path.join(ROOT, "instance", "saigonbite.db")


def schema_version() -> int:
    """The version schema.sql creates (its PRAGMA user_version line)."""
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return int(re.search(r"PRAGMA user_version = (\d+);", f.read()).group(1))


def build_database(db_path: str, demo: bool = False) -> None:
    """Create a new database file at db_path with schema and seed data (and the demo history if asked)."""
    if os.path.exists(db_path):
        raise FileExistsError('Fresh v2 requires a new database path; existing data is preserved.')
    parent = os.path.dirname(db_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        scripts = [SCHEMA_PATH, SEED_PATH] + ([DEMO_PATH] if demo else [])
        for path in scripts:
            with open(path, encoding="utf-8") as f:
                conn.executescript(f.read())
        conn.commit()
    except Exception:
        conn.close()
        os.remove(db_path)
        raise
    conn.close()


def migrate(db_path: str) -> list[str]:
    """Validate current v2 read-only. Refuse old/future versions; never claim an upgrade."""
    path = Path(db_path).resolve()
    if not path.is_file():
        raise ValueError('Database not found; choose a new path for fresh v2.')
    conn = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
    try:
        current = conn.execute("PRAGMA user_version").fetchone()[0]
        if current != schema_version():
            raise ValueError(f'Unsupported schema version {current}. No migration is provided. '
                             'Use a new path for fresh v2; preserve the existing database.')
    finally:
        conn.close()
    return []


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--db", default=DEFAULT_DB, help="database file (default: instance/saigonbite.db)")
    parser.add_argument("--force", action="store_true", help="recreate the database if it exists")
    parser.add_argument("--no-demo", action="store_true", help="do not load the demo order history")
    parser.add_argument("--migrate", action="store_true", help="upgrade an existing database in place")
    args = parser.parse_args(argv)

    if args.migrate:
        if not os.path.exists(args.db):
            print(f"Database not found: {args.db}", file=sys.stderr)
            return 1
        try:
            applied = migrate(args.db)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print("Applied: " + (", ".join(applied) if applied else "nothing, the database is up to date"))
        return 0

    if os.path.exists(args.db):
        if not args.force:
            print(f"Database already exists: {args.db}\nRun with --force to recreate it.", file=sys.stderr)
            return 1
        os.remove(args.db)
    build_database(args.db, demo=not args.no_demo)

    conn = sqlite3.connect(args.db)
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("hub", "brand", "menu_item", "user_account", "customer", "address", "voucher", "orders")}
    conn.close()
    print(f"Created {args.db} (schema version {schema_version()})")
    print("Seeded: " + ", ".join(f"{n} {t}" for t, n in counts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
