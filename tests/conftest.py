"""Shared fixtures. Every test gets its own temporary SQLite database built from schema.sql + seed.sql."""
import os
import sqlite3
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from init_db import build_database  # noqa: E402
from saigonbite import create_app   # noqa: E402

# Seeded dev accounts (README.md): username -> password is dev-<username>.
SEED_USERS = ("customer", "kitchen", "shipper", "admin", "manager")
HUB_D1, HUB_BT = 1, 2
ADDRESS_HOME = 1
# Menu items (seed.sql): 1 Pho bo tai 55000, 3 Goi cuon 35000, 5 sold out at hub 1, 9 not sold at hub 1
PHO, GOI_CUON, SOLD_OUT_AT_D1, NOT_AT_D1 = 1, 3, 5, 9


@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "test.db")
    build_database(path)
    return path


@pytest.fixture
def app(db_path):
    return create_app({"TESTING": True, "DATABASE": db_path, "SECRET_KEY": "test-secret"})


@pytest.fixture
def client(app):
    return app.test_client()


def login(client, username):
    resp = client.post("/login", data={"username": username, "password": f"dev-{username}"})
    assert resp.status_code == 302, resp.get_data(as_text=True)
    return client


@pytest.fixture
def customer_client(client):
    return login(client, "customer")


def new_connection(db_path):
    """A brand-new sqlite3 connection (used to read persisted data back, AC-5)."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def count(db_path, table):
    conn = new_connection(db_path)
    try:
        return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    finally:
        conn.close()


def _seed_prices():
    """Menu prices and hub fees from seed.sql, so tests can post the total the quote page shows."""
    from init_db import SCHEMA_PATH, SEED_PATH
    conn = sqlite3.connect(":memory:")
    conn.executescript(open(SCHEMA_PATH, encoding="utf-8").read())
    conn.executescript(open(SEED_PATH, encoding="utf-8").read())
    prices = dict(conn.execute("SELECT id, price FROM menu_item"))
    fees = dict(conn.execute("SELECT id, delivery_fee_flat FROM hub"))
    conn.close()
    return prices, fees


PRICES, FEES = _seed_prices()


def quoted_total(hub_id, quantities):
    """The total the quote page shows for valid quantities (seed prices)."""
    return FEES[hub_id] + sum(PRICES[i] * int(q) for i, q in quantities.items() if str(q).strip())


def checkout_form(token="tok-1", hub_id=HUB_D1, address_id=ADDRESS_HOME, quantities=None):
    """Form data as the quote page would post it to /order/confirm (with the quoted total when it can be computed)."""
    data = {"hub_id": hub_id, "idempotency_token": token}
    if address_id is not None:
        data["address_id"] = address_id
    quantities = quantities if quantities is not None else {PHO: "2", GOI_CUON: "1"}
    for item_id, qty in quantities.items():
        data[f"qty_{item_id}"] = qty
    try:
        data["quoted_total"] = quoted_total(hub_id, quantities)
    except (KeyError, ValueError, TypeError):
        pass                            # invalid input: the request is refused before the totals are compared
    return data


def add_second_customer(db_path):
    """Insert a second customer (user 'other') with its own address, for ownership tests."""
    from werkzeug.security import generate_password_hash
    conn = new_connection(db_path)
    conn.execute("INSERT INTO user_account (id, username, password_hash, display_name, role) "
                 "VALUES (10, 'other', ?, 'Other Customer', 'CUSTOMER')",
                 (generate_password_hash("dev-other", method="pbkdf2:sha256:1000"),))
    conn.execute("INSERT INTO customer (id, user_id, full_name, phone, customer_type) "
                 "VALUES (10, 10, 'Other Customer', '0900000000', 'LOCAL')")
    conn.execute("INSERT INTO address (id, customer_id, label, full_address) "
                 "VALUES (10, 10, 'Home', '1 Other Street, District 3, Ho Chi Minh City')")
    conn.commit()
    conn.close()
