"""Create the SaigonBite SQLite database: runs db/schema.sql then db/seed.sql.

Usage:  python init_db.py            (creates instance/saigonbite.db)
        python init_db.py --force    (delete and recreate an existing database)
        python init_db.py --db PATH  (use another file, e.g. for tests)
"""
import argparse
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(ROOT, "db", "schema.sql")
SEED_PATH = os.path.join(ROOT, "db", "seed.sql")
DEFAULT_DB = os.path.join(ROOT, "instance", "saigonbite.db")


def build_database(db_path: str) -> None:
    """Create a new database file at db_path with schema and seed data."""
    parent = os.path.dirname(db_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        with open(SCHEMA_PATH, encoding="utf-8") as f:
            conn.executescript(f.read())
        with open(SEED_PATH, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
    except Exception:
        conn.close()
        os.remove(db_path)
        raise
    conn.close()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--db", default=DEFAULT_DB, help="database file (default: instance/saigonbite.db)")
    parser.add_argument("--force", action="store_true", help="recreate the database if it exists")
    args = parser.parse_args(argv)

    if os.path.exists(args.db):
        if not args.force:
            print(f"Database already exists: {args.db}\nRun with --force to recreate it.", file=sys.stderr)
            return 1
        os.remove(args.db)
    build_database(args.db)

    conn = sqlite3.connect(args.db)
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("hub", "brand", "menu_item", "user_account", "customer", "address")}
    conn.close()
    print(f"Created {args.db}")
    print("Seeded: " + ", ".join(f"{n} {t}" for t, n in counts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
