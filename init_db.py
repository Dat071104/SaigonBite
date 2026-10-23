"""Create or upgrade the SaigonBite SQLite database.

Usage:  python init_db.py            (creates instance/saigonbite.db: schema, seed and demo history)
        python init_db.py --no-demo  (schema and seed only, no demo orders)
        python init_db.py --force    (delete and recreate an existing database)
        python init_db.py --migrate  (upgrade an existing database with db/migrations; never deletes data)
        python init_db.py --db PATH  (use another file, e.g. for tests)

The schema version is kept in PRAGMA user_version. A deployed database is upgraded with --migrate,
never recreated, so routine deployments keep the orders (plan §2.2).
"""
import argparse
import glob
import os
import re
import sqlite3
import sys

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
    """Apply db/migrations/NNN_name.sql files whose number is above the database's user_version.

    Each file runs in one transaction and ends by setting user_version to its number. Returns the
    names of the files applied.
    """
    conn = sqlite3.connect(db_path)
    applied = []
    try:
        current = conn.execute("PRAGMA user_version").fetchone()[0]
        for path in sorted(glob.glob(os.path.join(MIGRATIONS_DIR, "*.sql"))):
            number = int(os.path.basename(path).split("_", 1)[0])
            if number <= current:
                continue
            with open(path, encoding="utf-8") as f:
                conn.executescript("BEGIN;\n" + f.read() + f"\nPRAGMA user_version = {number};\nCOMMIT;")
            applied.append(os.path.basename(path))
    finally:
        conn.close()
    return applied


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
        applied = migrate(args.db)
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
